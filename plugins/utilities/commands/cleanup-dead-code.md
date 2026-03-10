---
description: "Find and remove dead code -- auto-detects language: Knip for TypeScript/JavaScript, vulture + ruff for Python"
argument-hint: "[path] [--dry-run] [--dependencies-only] [--exports-only] [--production]"
---

# Cleanup Dead Code

Detect and remove unused code. Auto-detects the project language and uses the appropriate tooling.

## CRITICAL RULES

1. **Run tests before and after.** Establish a baseline, then verify no regressions.
2. **If `--dry-run`, report only.** Show findings without modifying files.
3. **Revert on test failure.** If any test fails after a change, undo it immediately.
4. **Never remove code that is used via side effects.** Check dynamic imports, decorators, and framework conventions.

## Step 1: Detect Language

```bash
# Check for TS/JS project
ls package.json 2>/dev/null

# Check for Python project
ls pyproject.toml setup.py setup.cfg 2>/dev/null
find . -maxdepth 3 -name "*.py" -print -quit 2>/dev/null
```

### Decision tree

**Knip mode** (TS/JS) -- `package.json` exists:
- Use Knip for dead code detection
- Proceed to Step 2A

**Python mode** -- `*.py` files, `pyproject.toml`, or `setup.py` exist (no `package.json`):
- Use vulture + ruff for dead code detection
- Proceed to Step 2B

**Both exist** -- ask the user which to analyze, or run both sequentially.

---

## Step 2A: Knip Analysis (TypeScript/JavaScript)

### Verify Knip is available

```bash
bunx knip --version 2>/dev/null || npx knip --version 2>/dev/null
```

If not available, install it:
```bash
bun add --dev knip 2>/dev/null || npm install --save-dev knip
```

### Determine scope

From `$ARGUMENTS`:
- If a path is given: focus analysis on that directory
- If `--dependencies-only`: only check unused dependencies
- If `--exports-only`: only check unused exports
- If `--production`: use `--production` flag (skip devDependencies)
- If no flags: run full analysis

### Run Knip

```bash
# Full analysis (default)
bunx knip 2>/dev/null || npx knip

# Or scoped by flags
bunx knip --dependencies  # --dependencies-only
bunx knip --exports       # --exports-only
bunx knip --production    # --production
```

Capture the output and categorize findings:
- **Unused files** - files not imported anywhere
- **Unused dependencies** - packages in package.json not referenced
- **Unused exports** - exported symbols never imported elsewhere
- **Unused types** - type/interface exports never used

Proceed to Step 3 with Knip findings.

---

## Step 2B: Python Analysis (vulture + ruff)

### Verify tools are available

```bash
uv run vulture --version 2>/dev/null || vulture --version 2>/dev/null
uv run ruff --version 2>/dev/null || ruff --version 2>/dev/null
```

If not available:
```bash
uv tool install vulture 2>/dev/null || pip install vulture
uv tool install ruff 2>/dev/null || pip install ruff
```

### Determine scope

From `$ARGUMENTS`:
- If a path is given: focus analysis on that directory
- If no path: scan the project root (excluding venv, .venv, __pycache__, .git)

### Run analysis

```bash
# Vulture: detect unused code (functions, variables, imports, classes)
uv run vulture [target] --min-confidence 80 2>/dev/null || vulture [target] --min-confidence 80

# Ruff: detect unused imports (F401) and unused variables (F841)
uv run ruff check [target] --select F401,F841 2>/dev/null || ruff check [target] --select F401,F841
```

Capture the output and categorize findings:
- **Unused imports** - imports never referenced (F401)
- **Unused variables** - assigned but never used (F841)
- **Unused functions** - functions never called (vulture)
- **Unused classes** - classes never instantiated or referenced (vulture)
- **Unreachable code** - code after return/raise/break (vulture)

**Important:** Vulture may flag false positives. Cross-reference findings:
- Check if functions are used via `getattr`, decorators, or framework conventions (Django views, Flask routes, pytest fixtures, click commands)
- Check if `__all__` exports the symbol
- Check if the symbol is part of a public API used by external packages

Proceed to Step 3 with Python findings.

---

## Step 3: Present Findings

```
Dead code analysis for: [target] ([Knip mode / Python mode])

[For Knip mode:]
Unused dependencies ([count]):
- [package-name] (devDependencies)

Unused exports ([count]):
- [file:line] - [export-name]

Unused files ([count]):
- [file-path]

Unused types ([count]):
- [file:line] - [type-name]

[For Python mode:]
Unused imports ([count]):
- [file:line] - [import-name]

Unused variables ([count]):
- [file:line] - [variable-name]

Unused functions ([count]):
- [file:line] - [function-name]

Unused classes ([count]):
- [file:line] - [class-name]

Recommended actions:
1. Remove all findings
2. Remove specific categories only
3. Cancel
```

If `--dry-run`, stop here.

## Step 4: Establish Test Baseline

```bash
# TS/JS
npm test 2>/dev/null || bun test 2>/dev/null || npx vitest run 2>/dev/null

# Python
pytest -v 2>/dev/null || python -m pytest -v 2>/dev/null
```

Record passing/failing tests. If no tests exist, warn:

```
No tests found. Dead code removal can't be automatically validated.

1. Proceed anyway - I'll verify imports and references manually
2. Cancel - set up tests first
```

## Step 5: Apply Cleanup

Based on user selection, apply changes in this order (safest first):

### Knip mode (TS/JS)
1. **Unused dependencies**: `bun remove [package]` or `npm uninstall [package]`
2. **Unused exports**: Remove `export` keyword or delete entire unused function/const
3. **Unused types**: Remove type/interface declarations
4. **Unused files**: Delete files

### Python mode
1. **Unused imports**: Remove import statements
2. **Unused variables**: Remove assignments (or replace with `_` if in unpacking)
3. **Unused functions/classes**: Delete definitions (after verifying no dynamic usage)

For each change:
- Verify no dynamic imports, side-effect usage, or framework conventions
- Remove in small batches and validate

## Step 6: Validate & Report

```bash
# TS/JS
npm test 2>/dev/null || bun test 2>/dev/null || npx vitest run 2>/dev/null

# Python
pytest -v 2>/dev/null || python -m pytest -v 2>/dev/null
```

If any test fails: revert the last batch and report which removal caused the failure.

Present summary:

```
Dead code cleanup complete for: [target]

Removed:
- [category]: [count]
- ...

Tests: [all passing / X failures - reverted problematic removals]

Review the changes with: git diff
```

## What It Does

### TypeScript/JavaScript (Knip)
- Finds unused npm dependencies and removes them from package.json
- Detects exported symbols that are never imported and removes the exports
- Identifies files that aren't referenced anywhere and deletes them
- Finds unused type/interface exports and removes them

### Python (vulture + ruff)
- Finds unused imports and removes them
- Detects unused variables and removes assignments
- Identifies unused functions and classes and deletes them
- Finds unreachable code blocks and removes them

## What It Does NOT Do

- Does not remove code used via side effects, dynamic imports, or reflection
- Does not modify framework-convention files (e.g., Next.js pages/, Django views, pytest fixtures)
- Does not remove dependencies used only in scripts
- Does not touch test files unless they reference removed symbols

$ARGUMENTS
