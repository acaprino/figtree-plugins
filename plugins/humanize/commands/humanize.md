---
description: "Rewrite source code to be more readable and human-friendly -- improves naming, removes AI boilerplate, simplifies structure, adds clarity comments -- without changing behavior"
argument-hint: "<file or directory> [--dry-run] [--strict] [--yes]"
---

# Humanize Code

Use the `humanize` agent to rewrite source code for readability without changing behavior.

## CRITICAL RULES

1. **Run tests before and after.** Establish a baseline, then verify no regressions.
2. **If `--dry-run`, preview only.** Show proposed changes without modifying files.
3. **Revert on test failure.** If any test fails after a change, revert with `git restore <file>` immediately.
4. **Ask for confirmation** at Steps 2 and 3, unless `--yes` flag is provided.

## Step 1: Identify Target

From `$ARGUMENTS`, determine files to humanize:
- If a file path: humanize that file
- If a directory: humanize all source files in it
- Filter out test files (unless they reference renamed symbols)

List the files to be humanized and their language.

## Step 2: Establish Test Baseline

Detect the test runner by inspecting project files (e.g. `package.json` -> `npm test`, `pyproject.toml`/`setup.py` -> `pytest`, `Cargo.toml` -> `cargo test`, `go.mod` -> `go test`, `Makefile` with test target -> `make test`). Run the detected command and capture both stdout and stderr -- do NOT suppress stderr.

Record passing/failing tests. If no tests exist, warn the user:

```
No tests found. Humanization changes can't be automatically validated.

1. Proceed anyway -- I'll be extra careful
2. Cancel -- set up tests first
```

If `--yes` flag is provided, proceed automatically (option 1).

## Step 3: Preview Changes (always for --dry-run, ask otherwise)

If `--dry-run` flag is set, or if the target is a directory with >3 files, show a preview first.
If `--yes` flag is provided, apply all changes after showing the preview without asking.

For each file, analyze and propose:
- Variable/function renames (vague → domain-meaningful)
- Boilerplate comments to remove (paraphrase comments, empty docstrings)
- Why-comments to add (non-obvious business logic)
- Structural simplifications (flatten nesting, remove redundant abstractions, consolidate logic)

Present the preview:

```
Humanization preview for: [target]

[file1]:
- Rename `data` → `user_profile` (line 23)
- Rename `proc` → `process_payment` (line 45)
- Remove boilerplate docstring (line 12-15)
- Flatten nested if/else chain (line 30-50)
- Add comment explaining retry logic (line 67)

[file2]:
- ...

Total changes: [count] across [file count] files

1. Apply all changes
2. Apply to specific files only
3. Cancel
```

If `--dry-run`, stop after the preview.

## Step 4: Apply Changes

Use the `humanize` agent:

```
Task:
  subagent_type: "humanize"
  description: "Humanize [target] for readability"
  prompt: |
    Improve the readability and human-friendliness of this code.
    Do NOT change behavior -- only improve naming, comments, structure, and clarity.

    ## Files to Humanize
    [list of files]

    ## Approved Changes
    [from preview, if applicable]

    ## Instructions
    For each file:
    1. Rename vague variables and parameters to domain-meaningful names
    2. Remove paraphrase comments and empty boilerplate docstrings
    3. Add brief why-comments for non-obvious business logic
    4. Simplify structure: flatten nesting with early returns, remove redundant
       wrappers, consolidate scattered logic, replace nested ternaries with
       switch/if-else, choose clarity over brevity

    Do NOT:
    - Change any behavior or logic
    - Reorder top-level code or extract functions (UNLESS --strict flag is present in $ARGUMENTS, in which case you may do so carefully)
    - Remove error handling, validations, or imports
    - Modify test files (except renaming symbols renamed in source)
    - Add type annotations to unchanged code
    - Over-simplify: keep abstractions that aid testing/extension
    - Combine too many concerns into one function
```

## Step 5: Validate & Report

After changes, re-run the same test command detected in Step 2. Capture both stdout and stderr.

If any test that was passing in the baseline now fails: immediately revert the changes using `git restore <file>` and report which file caused the regression.

Present summary:

```
Humanization complete for: [target]

Files modified: [count]
Changes made:
- Renames: [count]
- Comments removed: [count]
- Comments added: [count]
- Structural simplifications: [count]

Tests: [all passing / X failures -- reverted problematic changes]

Review the changes with: git diff
```

If `--strict` flag is set, also flag any remaining readability concerns that weren't auto-fixable.

## What It Does

- Renames vague variables and parameters to domain-meaningful names
- Removes paraphrase comments and empty boilerplate docstrings
- Adds brief why-comments for non-obvious business logic
- Simplifies structure: flattens nesting, removes redundant abstractions, consolidates logic

## What It Does NOT Do

- Does not reorder top-level code, extract functions, or change APIs (unless `--strict`)
- Does not remove error handling, validations, or imports
- Does not modify test files (unless renaming symbols renamed in source)
- Does not over-simplify: keeps abstractions that aid testing or extension

For deeper restructuring, use `/python-refactor` for metrics-driven refactoring.

Humanize the following:

$ARGUMENTS
