---
description: "Review frontend code changes made in the current Claude Code session — React, performance, UX, CSS — and output a visual HTML report"
argument-hint: "[--strict-mode] [--framework react|vue|svelte]"
---

# Review Recent Frontend Changes (Visual Report)

You are a frontend code reviewer. Review the **frontend code changes made in the current session** and produce a **visual HTML report** file. Focus on React/JS/TS/CSS — not backend code, not documentation.

## CRITICAL RULES

1. **Diff first.** Start from `git diff HEAD` — this is ground truth of what changed.
2. **Frontend files only.** Include: `.js`, `.jsx`, `.ts`, `.tsx`, `.css`, `.scss`, `.sass`, `.less`, `.vue`, `.svelte`, `.html` (template changes). Skip `.md`, backend files, config-only changes.
3. **Run review agents in parallel.** Fire all agents in a single response.
4. **Write an HTML report.** Final output is a `.frontend-review/report.html` file — visual, color-coded, openable in a browser.
5. **Never enter plan mode.** Execute immediately.

## Step 1: Identify Changed Frontend Files

```bash
git diff HEAD --name-only
git diff --name-only
git diff --cached --name-only
```

Filter to frontend extensions only: `.js`, `.jsx`, `.ts`, `.tsx`, `.css`, `.scss`, `.sass`, `.less`, `.vue`, `.svelte`, `.html`.

If no frontend files changed, say so and stop.

List the files you'll review.

## Step 2: Get Diff Content

```bash
git diff HEAD -- <frontend files only>
```

If diff is large (>400 lines), prioritize new files and heavily changed ones.

## Step 3: Run Parallel Frontend Review Agents

Fire all three agents **in parallel** in a single response:

### Agent A: React & Performance

```
Task:
  subagent_type: "react-performance-optimizer"
  description: "React and performance review of recent frontend changes"
  prompt: |
    Review the following frontend code changes for React quality and performance issues.

    ## Changed Files
    [list of changed frontend files]

    ## Diff
    [paste the git diff output]

    ## Instructions
    Analyze for:
    1. **React patterns**: Incorrect hook usage, missing deps, stale closures, unnecessary re-renders
    2. **Performance**: Missing memoization (useMemo/useCallback/memo), expensive computations in render, N+1 effect chains
    3. **Bundle impact**: Heavy imports, missing lazy loading, large inline assets
    4. **State management**: Prop drilling, redundant state, state duplication across components
    5. **React 19 opportunities**: Can React Compiler handle this? Server Component candidates?
    6. **Accessibility basics**: Missing ARIA roles, keyboard handlers, focus management

    For each finding: severity (Critical/High/Medium/Low), file + line, specific fix.
    Also note what was done well.

    Return structured JSON at the end:
    ```json
    {
      "findings": [
        { "severity": "High", "category": "Performance", "file": "...", "line": 42, "issue": "...", "fix": "..." }
      ],
      "positives": ["..."],
      "score": { "performance": 7, "code_quality": 8, "overall": 7 }
    }
    ```
```

### Agent B: UX & Component Design

```
Task:
  subagent_type: "ui-ux-designer"
  description: "UX and component design review of recent frontend changes"
  prompt: |
    Review the following frontend code changes for UX and component design quality.

    ## Changed Files
    [list of changed frontend files]

    ## Diff
    [paste the git diff output]

    ## Instructions
    Analyze for:
    1. **Component design**: Is component responsibility well-defined? Are props sensible?
    2. **UX patterns**: Are interactions intuitive? Loading/error/empty states handled?
    3. **Accessibility**: ARIA attributes, semantic HTML, keyboard navigation, color contrast indicators
    4. **Design system consistency**: Are spacing, color, and typography tokens used correctly vs hardcoded values?
    5. **Responsive design**: Are breakpoints and fluid layouts considered?
    6. **User feedback**: Are async operations communicated (loading spinners, toasts, error messages)?

    For each finding: severity (Critical/High/Medium/Low), file + line, specific fix.
    Also note what was done well.

    Return structured JSON at the end:
    ```json
    {
      "findings": [
        { "severity": "Medium", "category": "Accessibility", "file": "...", "line": 15, "issue": "...", "fix": "..." }
      ],
      "positives": ["..."],
      "score": { "ux": 7, "accessibility": 6, "overall": 7 }
    }
    ```
```

### Agent C: CSS & Visual Polish

```
Task:
  subagent_type: "ui-polisher"
  description: "CSS and visual polish review of recent frontend changes"
  prompt: |
    Review the following frontend code changes for CSS quality and visual polish.

    ## Changed Files
    [list of changed frontend files]

    ## Diff
    [paste the git diff output]

    ## Instructions
    Analyze for:
    1. **CSS quality**: Specificity conflicts, redundant rules, missing resets, hardcoded px vs rem/em
    2. **Modern CSS**: Opportunities for CSS variables, container queries, logical properties, grid/flexbox improvements
    3. **Animation & transitions**: Missing or janky transitions, GPU-accelerated properties, reduced-motion support
    4. **Visual consistency**: Inconsistent shadows, border-radius, spacing values vs design tokens
    5. **Dark mode support**: Are colors and images adapted for dark mode if the project uses it?
    6. **Paint performance**: Avoid layout-triggering properties in animations, will-change abuse

    For each finding: severity (Critical/High/Medium/Low), file + line, specific fix.
    Also note what was done well.

    Return structured JSON at the end:
    ```json
    {
      "findings": [
        { "severity": "Low", "category": "CSS Quality", "file": "...", "line": 8, "issue": "...", "fix": "..." }
      ],
      "positives": ["..."],
      "score": { "css_quality": 8, "visual_polish": 7, "overall": 8 }
    }
    ```
```

## Step 4: Generate Visual HTML Report

After all agents complete, create `.frontend-review/` directory and write `report.html`:

The HTML report must be a **self-contained, single-file** dashboard with inline CSS and no external dependencies. Design it to be beautiful, scannable, and print-friendly. Use this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Frontend Review — [date]</title>
  <style>
    /* --- DESIGN TOKENS --- */
    :root {
      --c-bg: #0f1117;
      --c-surface: #1a1d27;
      --c-border: #2a2d3a;
      --c-text: #e2e8f0;
      --c-muted: #8892a4;
      --c-critical: #ef4444;
      --c-high: #f97316;
      --c-medium: #eab308;
      --c-low: #3b82f6;
      --c-good: #22c55e;
      --c-accent: #6366f1;
      --radius: 10px;
      --font: 'Inter', system-ui, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--c-bg);
      color: var(--c-text);
      font-family: var(--font);
      font-size: 14px;
      line-height: 1.6;
      padding: 32px 24px;
      max-width: 960px;
      margin: 0 auto;
    }

    /* HEADER */
    header {
      border-bottom: 1px solid var(--c-border);
      padding-bottom: 24px;
      margin-bottom: 32px;
    }
    header h1 { font-size: 24px; font-weight: 700; color: #fff; }
    header .meta { color: var(--c-muted); font-size: 13px; margin-top: 6px; }
    header .files-list {
      margin-top: 12px;
      display: flex; flex-wrap: wrap; gap: 6px;
    }
    header .file-tag {
      background: var(--c-surface);
      border: 1px solid var(--c-border);
      border-radius: 4px;
      padding: 2px 8px;
      font-size: 12px;
      font-family: monospace;
      color: var(--c-muted);
    }

    /* SCORE ROW */
    .scores {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
    }
    .score-card {
      background: var(--c-surface);
      border: 1px solid var(--c-border);
      border-radius: var(--radius);
      padding: 20px 16px;
      text-align: center;
    }
    .score-card .label { font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--c-muted); margin-bottom: 8px; }
    .score-card .value { font-size: 36px; font-weight: 800; line-height: 1; }
    .score-card .bar { height: 4px; border-radius: 2px; background: var(--c-border); margin-top: 10px; overflow: hidden; }
    .score-card .bar-fill { height: 100%; border-radius: 2px; transition: width .6s ease; }
    .score-high   .bar-fill, .score-high   .value { background: var(--c-good);     color: var(--c-good); }
    .score-medium .bar-fill, .score-medium .value { background: var(--c-medium);   color: var(--c-medium); }
    .score-low    .bar-fill, .score-low    .value { background: var(--c-critical); color: var(--c-critical); }

    /* FINDINGS SECTION */
    .section { margin-bottom: 32px; }
    .section h2 {
      font-size: 16px; font-weight: 600; color: #fff;
      margin-bottom: 16px;
      display: flex; align-items: center; gap: 8px;
    }
    .section h2 .count {
      font-size: 12px; font-weight: 500;
      background: var(--c-surface);
      border: 1px solid var(--c-border);
      border-radius: 99px;
      padding: 2px 8px;
      color: var(--c-muted);
    }

    /* FINDING CARD */
    .finding {
      background: var(--c-surface);
      border: 1px solid var(--c-border);
      border-left: 3px solid var(--c-border);
      border-radius: var(--radius);
      padding: 14px 16px;
      margin-bottom: 10px;
    }
    .finding.critical { border-left-color: var(--c-critical); }
    .finding.high     { border-left-color: var(--c-high); }
    .finding.medium   { border-left-color: var(--c-medium); }
    .finding.low      { border-left-color: var(--c-low); }

    .finding-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; flex-wrap: wrap; }
    .badge {
      font-size: 11px; font-weight: 600; padding: 2px 7px;
      border-radius: 4px; text-transform: uppercase; letter-spacing: .05em;
    }
    .badge.critical { background: rgba(239,68,68,.15); color: var(--c-critical); }
    .badge.high     { background: rgba(249,115,22,.15); color: var(--c-high); }
    .badge.medium   { background: rgba(234,179,8,.15);  color: var(--c-medium); }
    .badge.low      { background: rgba(59,130,246,.15); color: var(--c-low); }
    .badge.category { background: rgba(99,102,241,.12); color: #a5b4fc; }

    .file-ref { font-family: monospace; font-size: 12px; color: var(--c-muted); }
    .finding-issue { color: var(--c-text); margin-bottom: 6px; }
    .finding-fix {
      background: rgba(34,197,94,.06);
      border: 1px solid rgba(34,197,94,.15);
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 13px;
      color: #86efac;
    }
    .finding-fix::before { content: "Fix: "; font-weight: 600; }

    /* POSITIVES */
    .positives {
      background: rgba(34,197,94,.06);
      border: 1px solid rgba(34,197,94,.15);
      border-radius: var(--radius);
      padding: 16px 20px;
      margin-bottom: 32px;
    }
    .positives h2 { color: var(--c-good); margin-bottom: 10px; font-size: 15px; }
    .positives ul { padding-left: 18px; }
    .positives li { margin-bottom: 4px; color: #bbf7d0; }

    /* SUMMARY BAR */
    .summary-bar {
      display: flex; gap: 8px; flex-wrap: wrap;
      margin-bottom: 32px;
    }
    .summary-pill {
      display: flex; align-items: center; gap: 6px;
      padding: 6px 14px; border-radius: 99px;
      font-size: 13px; font-weight: 500;
    }
    .summary-pill.critical { background: rgba(239,68,68,.12); color: var(--c-critical); border: 1px solid rgba(239,68,68,.3); }
    .summary-pill.high     { background: rgba(249,115,22,.12); color: var(--c-high);     border: 1px solid rgba(249,115,22,.3); }
    .summary-pill.medium   { background: rgba(234,179,8,.12);  color: var(--c-medium);   border: 1px solid rgba(234,179,8,.3); }
    .summary-pill.low      { background: rgba(59,130,246,.12); color: var(--c-low);      border: 1px solid rgba(59,130,246,.3); }

    footer { border-top: 1px solid var(--c-border); padding-top: 20px; color: var(--c-muted); font-size: 12px; }

    @media print {
      body { background: #fff; color: #111; max-width: 100%; }
      .finding, .score-card, .positives { border-color: #ddd; }
    }
  </style>
</head>
<body>

<header>
  <h1>Frontend Code Review</h1>
  <div class="meta">Session review · [DATE] · [N] files changed</div>
  <div class="files-list">
    <!-- one .file-tag per changed file -->
  </div>
</header>

<!-- SCORE CARDS -->
<div class="scores">
  <!-- For each score dimension, pick class: score-high (8-10), score-medium (5-7), score-low (1-4) -->
  <div class="score-card score-[level]">
    <div class="label">Performance</div>
    <div class="value">X</div>
    <div class="bar"><div class="bar-fill" style="width: X0%"></div></div>
  </div>
  <div class="score-card score-[level]">
    <div class="label">UX Quality</div>
    <div class="value">X</div>
    <div class="bar"><div class="bar-fill" style="width: X0%"></div></div>
  </div>
  <div class="score-card score-[level]">
    <div class="label">CSS Quality</div>
    <div class="value">X</div>
    <div class="bar"><div class="bar-fill" style="width: X0%"></div></div>
  </div>
  <div class="score-card score-[level]">
    <div class="label">Accessibility</div>
    <div class="value">X</div>
    <div class="bar"><div class="bar-fill" style="width: X0%"></div></div>
  </div>
  <div class="score-card score-[level]" style="border-color: var(--c-accent)">
    <div class="label">Overall</div>
    <div class="value" style="color: #a5b4fc">X</div>
    <div class="bar"><div class="bar-fill" style="width: X0%; background: var(--c-accent)"></div></div>
  </div>
</div>

<!-- SUMMARY PILLS -->
<div class="summary-bar">
  <span class="summary-pill critical">● X Critical</span>
  <span class="summary-pill high">● X High</span>
  <span class="summary-pill medium">● X Medium</span>
  <span class="summary-pill low">● X Low</span>
</div>

<!-- FINDINGS: Critical & High -->
<div class="section">
  <h2>Critical & High Priority <span class="count">X findings</span></h2>
  <!-- For each Critical/High finding: -->
  <div class="finding critical">
    <div class="finding-header">
      <span class="badge critical">Critical</span>
      <span class="badge category">Performance</span>
      <span class="file-ref">ComponentName.tsx:42</span>
    </div>
    <div class="finding-issue">Missing dependency array in useEffect causes infinite re-render loop.</div>
    <div class="finding-fix">Add [data, id] to the dependency array: useEffect(() => { ... }, [data, id])</div>
  </div>
</div>

<!-- FINDINGS: Medium & Low -->
<div class="section">
  <h2>Medium & Low Priority <span class="count">X findings</span></h2>
  <!-- medium/low findings here -->
</div>

<!-- POSITIVES -->
<div class="positives">
  <h2>✓ What Was Done Well</h2>
  <ul>
    <li>...</li>
  </ul>
</div>

<footer>
  Generated by /review-frontend-changes · comprehensive-review + frontend plugins · [TIMESTAMP]
</footer>

</body>
</html>
```

Populate the template with all findings from the three agents. Merge and deduplicate overlapping findings. Order within each section by severity, then file name.

**Open the file** for the user:

```bash
start .frontend-review/report.html   # Windows
open .frontend-review/report.html    # macOS
xdg-open .frontend-review/report.html # Linux
```

Then print a short summary in the conversation:

```
Frontend review complete.

Report: .frontend-review/report.html

Overall Score: X/10
Critical: X | High: X | Medium: X | Low: X

Top issues:
1. [highest severity finding summary]
2. [second]
3. [third]
```

If `--strict-mode` is passed and there are Critical findings, warn:
```
⚠️  STRICT MODE: Critical issues found. Fix before committing.
```
