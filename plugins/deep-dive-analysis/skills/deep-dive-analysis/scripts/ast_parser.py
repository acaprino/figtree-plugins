"""
AST Parser Module for Deep Dive Analysis.

Extracts code structure from Python files using AST:
- Classes with methods and attributes
- Functions with signatures
- Imports (internal and external)
- Constants and global variables
- External calls (database, network, filesystem, messaging, ipc)
"""

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

__all__ = [
    "ParameterInfo",
    "FunctionInfo",
    "ClassInfo",
    "ImportInfo",
    "ExternalCallInfo",
    "ParseResult",
    "parse_file",
    "parse_content",
]


@dataclass
class ParameterInfo:
    """Information about a function parameter."""

    name: str
    annotation: str | None = None
    default: str | None = None


@dataclass
class FunctionInfo:
    """Information about a function or method."""

    name: str
    parameters: list[ParameterInfo] = field(default_factory=list)
    return_annotation: str | None = None
    is_async: bool = False
    is_classmethod: bool = False
    is_staticmethod: bool = False
    is_property: bool = False
    docstring: str | None = None
    line_number: int = 0


@dataclass
class ClassInfo:
    """Information about a class."""

    name: str
    bases: list[str] = field(default_factory=list)
    methods: list[FunctionInfo] = field(default_factory=list)
    class_variables: list[str] = field(default_factory=list)
    docstring: str | None = None
    line_number: int = 0


@dataclass
class ImportInfo:
    """Information about an import statement."""

    module: str
    names: list[str] = field(default_factory=list)
    is_from_import: bool = False
    is_internal: bool = False  # True if from project's own modules


@dataclass
class ExternalCallInfo:
    """Information about external system calls."""

    call_type: Literal["database", "network", "filesystem", "messaging", "ipc", "other"]
    pattern: str
    line_number: int
    context: str  # The line of code


@dataclass
class ParseResult:
    """Complete parse result for a file."""

    file_path: str
    classes: list[ClassInfo] = field(default_factory=list)
    functions: list[FunctionInfo] = field(default_factory=list)
    imports: list[ImportInfo] = field(default_factory=list)
    constants: list[str] = field(default_factory=list)
    external_calls: list[ExternalCallInfo] = field(default_factory=list)
    exported_symbols: list[str] = field(default_factory=list)


# AST-based external call detection patterns.
# Maps (receiver_name, method_name) pairs to call types.
# receiver_name can be None to match any receiver.
_DB_METHODS = frozenset([
    "find_one", "find_many", "insert_one", "insert_many",
    "update_one", "update_many", "delete_one", "delete_many",
    "aggregate", "execute", "executemany", "fetchone", "fetchall", "fetchmany",
    "commit", "rollback",
])
_DB_RECEIVERS = frozenset([
    "cursor", "collection", "session", "conn", "connection", "db", "database",
])
_DB_MODULES = frozenset([
    "motor", "beanie", "pymongo", "sqlalchemy", "sqlite3", "psycopg2",
    "asyncpg", "databases", "tortoise", "peewee", "mongoengine",
])

_NETWORK_MODULES = frozenset([
    "aiohttp", "httpx", "requests", "urllib", "urllib3", "grpc",
])
_NETWORK_METHODS = frozenset([
    "get", "post", "put", "delete", "patch", "head", "options", "fetch",
    "request",
])
_NETWORK_CONSTRUCTORS = frozenset([
    "ClientSession", "AsyncClient", "Session", "Client",
])

_FS_METHODS = frozenset([
    "read_text", "write_text", "read_bytes", "write_bytes",
    "mkdir", "rmdir", "unlink", "rename", "replace",
])
_FS_FUNCTIONS = frozenset(["open"])
_FS_MODULES = frozenset(["shutil", "os", "os.path"])

_MSG_METHODS = frozenset([
    "publish", "consume", "subscribe", "basic_publish", "basic_consume",
    "send_message", "receive",
])
_MSG_MODULES = frozenset([
    "kafka", "redis", "celery", "kombu", "pika", "aio_pika", "nats",
])

_IPC_MODULES = frozenset([
    "subprocess", "multiprocessing", "mmap",
])
_IPC_CONSTRUCTORS = frozenset([
    "Popen", "Process", "Pool",
])


def get_annotation_str(node: ast.expr | None) -> str | None:
    """Convert an AST annotation node to string."""
    if node is None:
        return None
    return ast.unparse(node)


def get_default_str(node: ast.expr | None) -> str | None:
    """Convert an AST default value node to string."""
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return "..."


def extract_docstring(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> str | None:
    """Extract docstring from a function or class node."""
    if (
        node.body
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, ast.Constant)
        and isinstance(node.body[0].value.value, str)
    ):
        return node.body[0].value.value.strip()
    return None


def get_decorators(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[bool, bool, bool]:
    """Check for classmethod, staticmethod, property decorators."""
    is_classmethod = False
    is_staticmethod = False
    is_property = False

    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name):
            if decorator.id == "classmethod":
                is_classmethod = True
            elif decorator.id == "staticmethod":
                is_staticmethod = True
            elif decorator.id == "property":
                is_property = True

    return is_classmethod, is_staticmethod, is_property


def parse_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> FunctionInfo:
    """Parse a function definition node."""
    params = []

    # Parse arguments
    args = node.args

    # Positional args (without defaults)
    num_defaults = len(args.defaults)
    num_args = len(args.args)
    non_default_args = num_args - num_defaults

    for i, arg in enumerate(args.args):
        default = None
        if i >= non_default_args:
            default_idx = i - non_default_args
            default = get_default_str(args.defaults[default_idx])

        params.append(
            ParameterInfo(
                name=arg.arg,
                annotation=get_annotation_str(arg.annotation),
                default=default,
            )
        )

    # Keyword-only args
    num_kw_defaults = len(args.kw_defaults)
    for i, arg in enumerate(args.kwonlyargs):
        default = None
        if i < num_kw_defaults and args.kw_defaults[i] is not None:
            default = get_default_str(args.kw_defaults[i])

        params.append(
            ParameterInfo(
                name=arg.arg,
                annotation=get_annotation_str(arg.annotation),
                default=default,
            )
        )

    is_classmethod, is_staticmethod, is_property = get_decorators(node)

    return FunctionInfo(
        name=node.name,
        parameters=params,
        return_annotation=get_annotation_str(node.returns),
        is_async=isinstance(node, ast.AsyncFunctionDef),
        is_classmethod=is_classmethod,
        is_staticmethod=is_staticmethod,
        is_property=is_property,
        docstring=extract_docstring(node),
        line_number=node.lineno,
    )


def parse_class(node: ast.ClassDef) -> ClassInfo:
    """Parse a class definition node."""
    # Get base classes
    bases = []
    for base in node.bases:
        try:
            bases.append(ast.unparse(base))
        except Exception:
            bases.append("?")

    # Get methods
    methods = []
    class_vars = []

    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods.append(parse_function(item))
        elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            class_vars.append(item.target.id)
        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    class_vars.append(target.id)

    return ClassInfo(
        name=node.name,
        bases=bases,
        methods=methods,
        class_variables=class_vars,
        docstring=extract_docstring(node),
        line_number=node.lineno,
    )


# Common third-party and stdlib prefixes (non-exhaustive, for heuristic only)
_COMMON_EXTERNAL_PREFIXES = frozenset([
    "os", "sys", "re", "json", "typing", "collections", "dataclasses",
    "pathlib", "asyncio", "logging", "datetime", "time", "random",
    "functools", "itertools", "contextlib", "abc", "enum", "uuid",
    "hashlib", "base64", "urllib", "http", "email", "html", "xml",
    "sqlite3", "socket", "threading", "multiprocessing", "subprocess",
    "unittest", "pytest", "mock", "requests", "aiohttp", "httpx",
    "pydantic", "sqlalchemy", "django", "flask", "fastapi", "celery",
    "redis", "kafka", "boto3", "numpy", "pandas", "scipy",
])


def _is_likely_internal_module(module: str) -> bool:
    """
    Heuristic to detect likely internal (project) modules.

    Returns True if the module doesn't match common external patterns.
    This is a best-effort heuristic; accuracy depends on project structure.
    """
    if not module:
        return False

    # Get the top-level package name
    top_level = module.split(".")[0]

    # If it starts with underscore, likely internal
    if top_level.startswith("_"):
        return True

    # If it matches common external packages, not internal
    if top_level.lower() in _COMMON_EXTERNAL_PREFIXES:
        return False

    # Relative imports are internal
    if module.startswith("."):
        return True

    # Default: assume internal if not recognized
    # This errs on the side of marking unknown modules as internal
    return True


def parse_imports(tree: ast.Module) -> list[ImportInfo]:
    """Extract all import statements from the AST."""
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    ImportInfo(
                        module=alias.name,
                        names=[alias.asname or alias.name],
                        is_from_import=False,
                        is_internal=_is_likely_internal_module(alias.name),
                    )
                )
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = [alias.name for alias in node.names]
            imports.append(
                ImportInfo(
                    module=module,
                    names=names,
                    is_from_import=True,
                    is_internal=_is_likely_internal_module(module),
                )
            )

    return imports


class _ExternalCallVisitor(ast.NodeVisitor):
    """AST visitor that detects external system calls by inspecting Call nodes."""

    def __init__(self, lines: list[str]):
        self.calls: list[ExternalCallInfo] = []
        self.lines = lines

    def _context(self, lineno: int) -> str:
        if 0 < lineno <= len(self.lines):
            return self.lines[lineno - 1].strip()[:100]
        return ""

    def _get_call_parts(self, node: ast.Call) -> tuple[str | None, str | None]:
        """Extract (receiver, method) from a Call node."""
        func = node.func
        if isinstance(func, ast.Attribute):
            method = func.attr
            if isinstance(func.value, ast.Name):
                return func.value.id, method
            if isinstance(func.value, ast.Attribute):
                return ast.unparse(func.value), method
            return None, method
        if isinstance(func, ast.Name):
            return None, func.id
        return None, None

    def visit_Call(self, node: ast.Call) -> None:
        receiver, method = self._get_call_parts(node)
        if method is None:
            self.generic_visit(node)
            return

        call_type = self._classify(receiver, method)
        if call_type:
            pattern = f"{receiver}.{method}" if receiver else method
            self.calls.append(ExternalCallInfo(
                call_type=call_type,
                pattern=pattern,
                line_number=node.lineno,
                context=self._context(node.lineno),
            ))

        self.generic_visit(node)

    def _classify(self, receiver: str | None, method: str) -> str | None:
        # Database
        if method in _DB_METHODS:
            if receiver and (receiver in _DB_RECEIVERS or receiver.split(".")[0] in _DB_MODULES):
                return "database"
            if receiver is None:
                return None  # bare execute() etc. - too ambiguous
            return "database" if receiver in _DB_RECEIVERS else None
        if receiver and receiver.split(".")[0] in _DB_MODULES:
            return "database"

        # Network
        if receiver and receiver.split(".")[0] in _NETWORK_MODULES:
            return "network"
        if method in _NETWORK_CONSTRUCTORS:
            return "network"
        if method in _NETWORK_METHODS and receiver and receiver.split(".")[0] in _NETWORK_MODULES:
            return "network"

        # Filesystem
        if method in _FS_FUNCTIONS:
            return "filesystem"
        if method in _FS_METHODS:
            return "filesystem"
        if receiver and receiver.split(".")[0] in _FS_MODULES:
            return "filesystem"

        # Messaging
        if method in _MSG_METHODS:
            if receiver and receiver.split(".")[0] in _MSG_MODULES:
                return "messaging"
            return "messaging" if receiver and any(kw in receiver.lower() for kw in ("channel", "queue", "topic", "producer", "consumer")) else None
        if receiver and receiver.split(".")[0] in _MSG_MODULES:
            return "messaging"

        # IPC
        if receiver and receiver.split(".")[0] in _IPC_MODULES:
            return "ipc"
        if method in _IPC_CONSTRUCTORS:
            return "ipc"

        return None


def find_external_calls(content: str) -> list[ExternalCallInfo]:
    """
    Find potential external system calls using AST analysis.

    Walks the AST to inspect actual Call nodes, checking receiver names and
    method names against known patterns. This eliminates false positives from
    regex matching against comments, strings, or unrelated method names.
    """
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []

    lines = content.split("\n")
    visitor = _ExternalCallVisitor(lines)
    visitor.visit(tree)
    return visitor.calls


def find_constants(tree: ast.Module) -> list[str]:
    """Find module-level constants (UPPER_CASE assignments)."""
    constants = []

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    constants.append(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id.isupper():
                constants.append(node.target.id)

    return constants


def find_exported_symbols(tree: ast.Module) -> list[str]:
    """Find symbols that would be exported (public classes, functions)."""
    exported = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            exported.append(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                exported.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith("_"):
                    exported.append(target.id)

    return exported


def parse_file(file_path: Path) -> ParseResult:
    """
    Parse a Python file and extract its structure.

    Args:
        file_path: Path to the Python file

    Returns:
        ParseResult with complete file structure
    """
    content = file_path.read_text(encoding="utf-8")
    tree = ast.parse(content)

    classes = []
    functions = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes.append(parse_class(node))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(parse_function(node))

    return ParseResult(
        file_path=str(file_path),
        classes=classes,
        functions=functions,
        imports=parse_imports(tree),
        constants=find_constants(tree),
        external_calls=find_external_calls(content),
        exported_symbols=find_exported_symbols(tree),
    )


def parse_content(content: str, file_path: str = "<string>") -> ParseResult:
    """
    Parse Python content from a string.

    Args:
        content: Python source code
        file_path: Optional path for identification

    Returns:
        ParseResult with complete structure
    """
    tree = ast.parse(content)

    classes = []
    functions = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes.append(parse_class(node))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(parse_function(node))

    return ParseResult(
        file_path=file_path,
        classes=classes,
        functions=functions,
        imports=parse_imports(tree),
        constants=find_constants(tree),
        external_calls=find_external_calls(content),
        exported_symbols=find_exported_symbols(tree),
    )


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) > 1:
        test_file = Path(sys.argv[1])
        if test_file.exists():
            result = parse_file(test_file)

            # Convert to dict for JSON output
            output = {
                "file_path": result.file_path,
                "classes": [
                    {
                        "name": c.name,
                        "bases": c.bases,
                        "methods": [m.name for m in c.methods],
                        "class_variables": c.class_variables,
                        "line_number": c.line_number,
                    }
                    for c in result.classes
                ],
                "functions": [
                    {
                        "name": f.name,
                        "is_async": f.is_async,
                        "parameters": [p.name for p in f.parameters],
                        "line_number": f.line_number,
                    }
                    for f in result.functions
                ],
                "imports": {
                    "internal": [
                        i.module for i in result.imports if i.is_internal
                    ],
                    "external": [
                        i.module for i in result.imports if not i.is_internal
                    ],
                },
                "constants": result.constants,
                "external_calls": [
                    {"type": c.call_type, "pattern": c.pattern, "line": c.line_number}
                    for c in result.external_calls[:10]  # Limit output
                ],
                "exported_symbols": result.exported_symbols,
            }

            print(json.dumps(output, indent=2))
        else:
            print(f"File not found: {test_file}")
    else:
        print("Usage: python ast_parser.py <file_path>")
