---
description: "Launch a multi-reviewer parallel code review with specialized review dimensions"
argument-hint: "<target> [--reviewers auto|security,performance,...] [--base-branch main] [--all]"
---

# Team Review

Orchestrate a multi-reviewer parallel code review where each reviewer focuses on a specific quality dimension. **Auto-detects which dimensions are relevant** based on the changed files and codebase context. Produces a consolidated, deduplicated report organized by severity.

## Skills to Load

Before starting, invoke these skills to inform the review process:
- `agent-teams:multi-reviewer-patterns` -- dimension allocation, deduplication rules, severity calibration
- `senior-review:defect-taxonomy` -- 140+ defect subcategories with CWE/OWASP mappings
- `agent-teams:team-communication-protocols` -- message type selection, shutdown protocol

## Pre-flight Checks

1. Verify `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set
2. Parse `$ARGUMENTS`:
   - `<target>`: file path, directory, git diff range (e.g., `main...HEAD`), or PR number (e.g., `#123`)
   - `--reviewers`: comma-separated dimensions OR `auto` (default: `auto`)
   - `--base-branch`: base branch for diff comparison (default: `main`)
   - `--all`: force all dimensions regardless of auto-detection

## Phase 1: Target Resolution

1. Determine target type:
   - **File/Directory**: Use as-is for review scope
   - **Git diff range**: Use Bash to run `git diff {range} --name-only` to get changed files
   - **PR number**: Use Bash to run `gh pr diff {number} --name-only` to get changed files
2. Collect the full diff content for distribution to reviewers
3. Collect the list of changed file paths and extensions for Phase 1b

## Phase 1b: Context Detection (when `--reviewers auto` or omitted)

Analyze the changed files and codebase to determine which review dimensions are relevant. Skip this phase if explicit `--reviewers` list was provided.

### Always-on dimensions (run for every review)

| Dimension | Agent | Rationale |
|-----------|-------|-----------|
| Security | `senior-review:security-auditor` | Every change can introduce vulnerabilities |
| Architecture | `senior-review:code-auditor` | Coupling, abstractions, failure flows, pattern consistency, scoring |
| Dead code & lint | `general-purpose` | Catch unused imports, variables, unreachable code introduced by the diff |

### Conditional dimensions (auto-detected from context)

Run these checks against the changed files and codebase to decide which extra reviewers to spawn:

| Signal | Detection rule | Dimension activated | Agent |
|--------|---------------|---------------------|-------|
| **UI/frontend files** | Changed files include `.tsx`, `.jsx`, `.vue`, `.svelte`, `.component.ts`, or files containing scroll/focus/layout manipulation | UI race conditions | `senior-review:ui-race-auditor` |
| **React project** | `package.json` has `react` in dependencies AND changed files include `.tsx`/`.jsx` | React performance | `react-development:react-performance-optimizer` |
| **Non-React frontend** | Frontend files detected but no React dependency | General performance | `agent-teams:team-reviewer` (performance dimension) |
| **Fullstack app** | 2+ signals: frontend framework in `package.json`, backend framework config, API route definitions, `docker-compose.yml` with multiple services, Tauri/Electron config | Platform compliance | `platform-engineering:platform-reviewer` |
| **Multi-service / messaging** | Changed files touch API routes, message handlers, gRPC definitions, queue consumers/producers, or `docker-compose.yml` with multiple services | Distributed flows | `senior-review:distributed-flow-auditor` |
| **Init/startup code** | Changed files touch startup sequences, dependency injection, config bootstrap, migration runners, or service registration | Circular dependencies | `senior-review:chicken-egg-detector` |
| **Test files** | Changed files match `test_*`, `*_test.*`, `*.spec.*`, `*.test.*`, `conftest.py`, `__tests__/` | Testing quality | `agent-teams:team-reviewer` (testing dimension) |
| **API files** | Changed files touch route definitions, serializers, OpenAPI/Swagger specs, GraphQL schemas | API contracts | `agent-teams:team-reviewer` (API dimension) |
| **Migration files** | Changed files match database migration patterns (Alembic, Django, Rails, Prisma, SQL migrations) | Data migrations | `agent-teams:team-reviewer` (migration dimension) |

### Detection implementation

Run these bash commands to gather signals:

```bash
# 1. Classify changed file extensions
echo "$CHANGED_FILES" | sed 's/.*\.//' | sort | uniq -c | sort -rn

# 2. Check for React
cat package.json 2>/dev/null | grep -q '"react"' && echo "REACT=true"

# 3. Check for fullstack signals (count matches)
FULLSTACK_SIGNALS=0
[ -f package.json ] && grep -qE '"(react|vue|svelte|angular|next|nuxt)"' package.json && FULLSTACK_SIGNALS=$((FULLSTACK_SIGNALS+1))
grep -rql 'fastapi\|django\|flask\|express\|nest\|hono\|actix\|axum' pyproject.toml Cargo.toml package.json 2>/dev/null && FULLSTACK_SIGNALS=$((FULLSTACK_SIGNALS+1))
ls -d */routes */api */endpoints 2>/dev/null && FULLSTACK_SIGNALS=$((FULLSTACK_SIGNALS+1))
[ -f docker-compose.yml ] && grep -c 'image:\|build:' docker-compose.yml | awk '$1>1{print "MULTI_SERVICE"}' && FULLSTACK_SIGNALS=$((FULLSTACK_SIGNALS+1))

# 4. Check for multi-service / messaging patterns in diff
echo "$DIFF_CONTENT" | grep -qiE 'rabbitmq\|amqp\|kafka\|grpc\|pubsub\|queue\|celery\|dramatiq' && echo "MESSAGING=true"
echo "$CHANGED_FILES" | grep -qiE 'routes?\b|api/|endpoints?/|handlers?/' && echo "API_FILES=true"

# 5. Check for init/startup patterns in diff
echo "$DIFF_CONTENT" | grep -qiE 'def main\b|if __name__|app\.on_startup|@app\.on_event|lifespan|create_app|bootstrap|init_' && echo "STARTUP=true"

# 6. Check for test and migration files
echo "$CHANGED_FILES" | grep -qiE 'test_|_test\.|\.spec\.|\.test\.|conftest|__tests__' && echo "TEST_FILES=true"
echo "$CHANGED_FILES" | grep -qiE 'migrat|alembic|versions/' && echo "MIGRATION_FILES=true"
```

### Display detected dimensions

After detection, display the plan to the user:

```
Context detection complete:
  - Always: security, architecture, dead-code
  - Detected: ui-races (6 .tsx files), react-perf (React project), distributed-flows (API routes + RabbitMQ)
  - Skipped: platform (not fullstack), chicken-egg (no startup code), testing (no test files changed)

Spawning {N} reviewers for {M} dimensions.
```

## Phase 2: Team Spawn

1. Use `Teammate` tool with `operation: "spawnTeam"`, team name: `review-{timestamp}`
2. For each selected dimension (always-on + detected conditional), use `Task` tool to spawn a teammate using the **most specialized agent**:

### Dimension-to-agent mapping

| Dimension | subagent_type |
|-----------|---------------|
| Security | `senior-review:security-auditor` |
| Architecture (+ failure flows, patterns, scoring) | `senior-review:code-auditor` |
| Dead code & lint | `general-purpose` |
| UI race conditions | `senior-review:ui-race-auditor` |
| React performance | `react-development:react-performance-optimizer` |
| General performance | `agent-teams:team-reviewer` |
| Platform compliance | `platform-engineering:platform-reviewer` |
| Distributed flows | `senior-review:distributed-flow-auditor` |
| Circular dependencies | `senior-review:chicken-egg-detector` |
| Testing quality | `agent-teams:team-reviewer` |
| API contracts | `agent-teams:team-reviewer` |
| Data migrations | `agent-teams:team-reviewer` |

- `name`: `{dimension}-reviewer` (e.g., "security-reviewer", "ui-race-reviewer")
- `prompt`: Include the dimension assignment, target files, diff content, and dimension-specific checklist (use the detailed agent prompts from `/senior-review:code-review` Steps 3A-3I as templates)

3. Use `TaskCreate` for each reviewer's task:
   - Subject: "Review {target} for {dimension} issues"
   - Description: Include file list, diff content, and dimension-specific checklist

## Phase 3: Monitor and Collect

1. Wait for all review tasks to complete (check `TaskList` periodically)
2. As each reviewer completes, collect their structured findings
3. Track progress: "{completed}/{total} reviews complete"

## Phase 4: Consolidation

1. **Deduplicate**: Merge findings that reference the same file:line location
2. **Resolve conflicts**: If reviewers disagree on severity, use the higher rating
3. **Organize by severity**: Group findings as Critical, High, Medium, Low
4. **Cross-reference**: Note findings that appear in multiple dimensions

## Phase 5: Report and Cleanup

1. Present consolidated report:

   ```
   ## Code Review Report: {target}

   Reviewed by: {dimensions}
   Files reviewed: {count}

   ### Critical ({count})
   [findings...]

   ### High ({count})
   [findings...]

   ### Medium ({count})
   [findings...]

   ### Low ({count})
   [findings...]

   ### Summary
   Total findings: {count} (Critical: N, High: N, Medium: N, Low: N)
   ```

2. Send `shutdown_request` to all reviewers
3. Call `Teammate` cleanup to remove team resources
