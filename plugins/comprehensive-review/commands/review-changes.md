---
description: "Review the code changes made in the current Claude Code session by analyzing git diff and running focused architecture, security, and pattern analysis — no documentation review"
argument-hint: "[--security-focus] [--strict-mode]"
---

# Review Recent Changes

You are a focused code reviewer. Your job is to review the **code changes made in the current session** — files Claude just modified, created, or deleted. This is NOT a full project review. You look only at what changed, not at documentation.

## CRITICAL RULES

1. **Read git diff first.** Always start from `git diff HEAD` (or `git diff` for unstaged + `git diff --cached` for staged). This is the ground truth of what changed.
2. **Skip documentation files.** Ignore `.md`, `.txt`, `.rst`, `README*`, `CHANGELOG*`, `LICENSE*`. Focus only on code.
3. **Run agents in parallel.** Fire all review agents in a single response using multiple Task tool calls.
4. **Never enter plan mode.** Execute immediately.
5. **Output a single concise report.** No intermediate files needed — deliver findings directly in the conversation.

## Step 1: Identify Changed Code Files

Run these commands to get the changed files:

```bash
git diff HEAD --name-only
git diff --name-only          # unstaged
git diff --cached --name-only # staged
```

Filter out non-code files (`.md`, `.txt`, `.json` config-only, images, etc.).

If git shows no changes, check the conversation context for files that were explicitly edited in this session and use those.

List the code files you will review. If there are no code changes (only docs), say so and stop.

## Step 2: Get the Diff Content

```bash
git diff HEAD -- <code files only>
```

If the diff is very large (>500 lines), focus on the most changed files — prioritize new files and heavily modified ones.

## Step 3: Run Parallel Review Agents

Run all three agents **in parallel** in a single response:

### Agent A: Architecture & Code Quality

```
Task:
  subagent_type: "architect-review"
  description: "Architecture and code quality review of recent changes"
  prompt: |
    Review the following code changes made in the current Claude Code session.
    Focus ONLY on code quality and architectural concerns. Skip documentation.

    ## Changed Files
    [list of changed code files]

    ## Diff
    [paste the git diff output]

    ## Instructions
    Analyze for:
    1. **Design concerns**: Are the changes architecturally sound? Any inappropriate coupling or broken abstractions?
    2. **Code quality**: Naming, function length, complexity, duplication
    3. **Error handling**: Missing or incorrect error handling
    4. **Consistency**: Do the changes follow the patterns already in the codebase?
    5. **Over-engineering or under-engineering**: Is the solution appropriately scoped?

    For each finding: severity (Critical/High/Medium/Low), file + line, and a concrete fix recommendation.
    Also note what was done well.

    Keep the response focused and concise — this is a targeted review, not a full audit.
```

### Agent B: Security Assessment

```
Task:
  subagent_type: "security-auditor"
  description: "Security review of recent changes"
  prompt: |
    Review the following code changes made in the current Claude Code session for security issues.
    Skip documentation files. Focus only on code.

    ## Changed Files
    [list of changed code files]

    ## Diff
    [paste the git diff output]

    ## Instructions
    Check for:
    1. **Injection risks**: SQL, command, LDAP, XPath injection in new or modified code
    2. **Input validation**: Missing or insufficient validation of user-controlled input
    3. **Authentication/authorization**: Flawed logic, missing checks, privilege issues
    4. **Secrets exposure**: Hardcoded credentials, tokens, keys in changed code
    5. **Insecure defaults**: Debug mode, verbose errors, permissive settings introduced
    6. **Dependency risks**: New packages added — are they trustworthy and up to date?

    For each finding: severity, CWE if applicable, file + line, attack scenario, concrete fix.
    If no security issues found, say so clearly.

    Keep the response concise — targeted review only.
```

### Agent C: Pattern Consistency & Scoring

```
Task:
  subagent_type: "pattern-quality-scorer"
  description: "Pattern consistency and quality scoring of recent changes"
  prompt: |
    Analyze the following code changes for pattern consistency and assign a quality score.

    ## Changed Files
    [list of changed code files]

    ## Diff
    [paste the git diff output]

    ## Instructions

    ### Pattern Consistency
    For each changed file, identify:
    - The dominant patterns already present (error handling style, async patterns, naming conventions, etc.)
    - Any deviations introduced by these changes
    - Anti-patterns introduced: swallowed exceptions, tight coupling, mutable globals, TODO in critical paths, etc.

    ### Mental Models (apply all six)
    - **Security Engineer**: Is all input treated as malicious?
    - **Performance Engineer**: Any O(n²) loops, N+1 queries, blocking I/O?
    - **Team Lead**: Will a junior dev understand this in 6 months?
    - **Systems Architect**: How does this fail? Blast radius?
    - **SRE**: What breaks at 3 AM?
    - **Pattern Detective**: What patterns exist, and did this change violate them?

    ### Quality Score for These Changes
    Score only the changed code (not the whole project):

    | Category        | Score |
    |-----------------|-------|
    | Code Quality    | X/10  |
    | Security        | X/10  |
    | Consistency     | X/10  |
    | **Overall**     | **X/10** |

    Scoring guide: 9-10 excellent, 7-8 good, 5-6 adequate, 3-4 poor, 1-2 critical.
    Include 2-3 sentence rationale per score.
```

## Step 4: Consolidated Summary

After all three agents complete, synthesize their findings into a final summary directly in the conversation:

```
## Review Summary — Recent Changes

### Changed Files
[list]

### Overall Score: X/10

### Critical & High Issues
[merged list from all agents, deduplicated, ordered by severity]

### Medium & Low Issues
[merged list]

### What Was Done Well
[positive observations from agents]

### Top 3 Recommended Actions
1. [highest priority fix]
2. [second priority]
3. [third priority]
```

If `--strict-mode` is passed and there are Critical findings, append:

```
⚠️  STRICT MODE: Critical issues found. Recommend fixing before committing.
```

Keep the entire output concise. This is a quick review, not a full audit report.
