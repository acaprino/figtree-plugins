---
description: "Full design, layout, and CSS audit of the entire frontend — UX patterns, component hierarchy, spacing system, typography, accessibility, and visual consistency — outputs a visual HTML report"
argument-hint: "[src-path] [--framework react|vue|svelte] [--strict-mode]"
---

# Full Frontend Design & CSS Review (Visual Report)

You are a senior frontend design auditor. Perform a **comprehensive design, layout, and CSS review** of the entire frontend codebase — not just recent changes. Evaluate UX patterns, visual consistency, accessibility, layout system, typography, and CSS architecture. Output a **visual HTML report**.

## CRITICAL RULES

1. **Scan the whole frontend.** Use `src/`, `app/`, `components/`, `pages/`, `styles/` — or the path from `$ARGUMENTS` if provided.
2. **Design + CSS only.** Ignore backend files, API routes, build config. Focus on components, stylesheets, layout files.
3. **Run all agents in parallel.** Fire all in a single response.
4. **Write an HTML report.** Final output is `.design-review/report.html` — visual, color-coded, openable in a browser.
5. **Never enter plan mode.** Execute immediately.

## Step 1: Discover Frontend Files

```bash
find src -type f \( -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" -o -name "*.css" -o -name "*.scss" -o -name "*.sass" \) | head -80
```

Or use the path from `$ARGUMENTS` if provided. List what you find — components, pages, and stylesheet files.

If no frontend files are found, stop and say so.

## Step 2: Sample Key Files

Read a representative cross-section:
- Entry layout files (e.g., `App.tsx`, `Layout.tsx`, `_app.tsx`, `root.tsx`)
- 3-5 core components
- Primary stylesheet(s) or `globals.css` / `tailwind.config`
- Design token files (`tokens.ts`, `theme.ts`, `variables.css`)

This gives you the design language and patterns to evaluate against.

## Step 3: Run Parallel Review Agents

Fire all three agents **in parallel** in a single response:

### Agent A: UX Patterns & Component Architecture

```
Task:
  subagent_type: "ui-ux-designer"
  description: "Full UX and component architecture design audit"
  prompt: |
    Perform a full UX and component architecture audit of this frontend codebase.

    ## Scope
    [list of key files sampled]

    ## File Contents
    [paste sampled component and layout file contents]

    ## Instructions
    Evaluate:
    1. **Component responsibility**: God components, missing abstractions, component prop explosion
    2. **UX patterns**: Consistency of interaction patterns (forms, modals, navigation, data loading)
    3. **Empty/loading/error states**: Are all three states handled everywhere they're needed?
    4. **Information hierarchy**: Is visual hierarchy consistent? Do primary/secondary/tertiary actions follow a system?
    5. **User flows**: Are there obvious dead ends, missing feedback, or confusing navigation?
    6. **Design system adherence**: Are colors, spacing, and typography from a token system, or are they scattered arbitrary values?
    7. **Accessibility audit**: Semantic HTML, ARIA roles, keyboard navigation, focus management, color contrast awareness

    For each finding: severity (Critical/High/Medium/Low), file, issue, specific fix recommendation.
    Note what's working well.

    Return structured JSON at the end:
    ```json
    {
      "findings": [
        { "severity": "High", "category": "Accessibility", "file": "...", "issue": "...", "fix": "..." }
      ],
      "positives": ["..."],
      "score": { "ux_consistency": 7, "accessibility": 5, "component_design": 8, "overall": 7 }
    }
    ```
```

### Agent B: Layout System & Spatial Design

```
Task:
  subagent_type: "ui-layout-designer"
  description: "Layout system, grid, and spatial design audit"
  prompt: |
    Audit the layout system, grid, spacing, and spatial design of this frontend codebase.

    ## Scope
    [list of key files sampled]

    ## File Contents
    [paste sampled layout and stylesheet file contents]

    ## Instructions
    Evaluate:
    1. **Layout system**: Is there a consistent grid/layout pattern (CSS Grid, Flexbox, utility classes)? Or ad-hoc layouts per component?
    2. **Spacing scale**: Is spacing derived from a consistent scale (4px/8px/rem)? Or arbitrary pixel values scattered everywhere?
    3. **Responsive strategy**: Are breakpoints consistent? Mobile-first vs desktop-first? Are there layout shifts on resize?
    4. **Typography system**: Font scale, line-height, letter-spacing — are they tokens or raw values?
    5. **Alignment & rhythm**: Do elements align to a clear baseline? Is vertical rhythm maintained?
    6. **Above-the-fold**: Is the critical viewport optimized? Is the most important content immediately visible?
    7. **Container strategy**: Max-widths, centering, content containers — are they consistent?

    For each finding: severity (Critical/High/Medium/Low), file, issue, specific fix.
    Note what's done well.

    Return structured JSON at the end:
    ```json
    {
      "findings": [
        { "severity": "Medium", "category": "Spacing", "file": "...", "issue": "...", "fix": "..." }
      ],
      "positives": ["..."],
      "score": { "layout_system": 7, "responsive": 8, "typography": 6, "overall": 7 }
    }
    ```
```

### Agent C: CSS Architecture & Visual Polish

```
Task:
  subagent_type: "ui-polisher"
  description: "CSS architecture and visual polish audit"
  prompt: |
    Audit the CSS architecture, code quality, and visual polish of this frontend codebase.

    ## Scope
    [list of key files sampled]

    ## File Contents
    [paste sampled stylesheet and component file contents]

    ## Instructions
    Evaluate:
    1. **CSS architecture**: Global styles pollution, specificity wars, selector depth, !important abuse
    2. **Modern CSS usage**: Are CSS custom properties used? Container queries? Logical properties? Or legacy patterns?
    3. **Animation quality**: Transitions feel smooth? GPU-accelerated properties? prefers-reduced-motion respected?
    4. **Visual consistency**: Border-radius, shadow elevation, color palette — are they consistent or scattered?
    5. **Dark mode**: Is dark mode supported? Are colors properly adapted or just inverted?
    6. **CSS performance**: Unnecessary repaints, layout-triggering animations, oversized background images
    7. **Dead CSS**: Unused selectors, legacy overrides, commented-out blocks
    8. **Component isolation**: Are styles scoped or do they leak? CSS Modules / Tailwind / CSS-in-JS used correctly?

    For each finding: severity (Critical/High/Medium/Low), file, issue, specific fix.
    Note what's done well.

    Return structured JSON at the end:
    ```json
    {
      "findings": [
        { "severity": "Low", "category": "CSS Architecture", "file": "...", "issue": "...", "fix": "..." }
      ],
      "positives": ["..."],
      "score": { "css_architecture": 8, "visual_polish": 7, "animations": 9, "overall": 8 }
    }
    ```
```

## Step 4: Generate Visual HTML Report

After all agents complete, create `.design-review/` directory and write `report.html`.

The HTML report must be a **self-contained, single-file** dashboard — beautiful, scannable, no external dependencies. Use this structure and design system:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Design & CSS Review — [date]</title>
  <style>
    :root {
      --c-bg: #0f1117;
      --c-surface: #1a1d27;
      --c-surface-2: #22263a;
      --c-border: #2a2d3a;
      --c-text: #e2e8f0;
      --c-muted: #8892a4;
      --c-critical: #ef4444;
      --c-high: #f97316;
      --c-medium: #eab308;
      --c-low: #3b82f6;
      --c-good: #22c55e;
      --c-accent: #8b5cf6;
      --c-ux: #06b6d4;
      --c-layout: #f59e0b;
      --c-css: #ec4899;
      --radius: 10px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--c-bg);
      color: var(--c-text);
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 14px;
      line-height: 1.6;
      padding: 40px 28px;
      max-width: 1020px;
      margin: 0 auto;
    }

    /* HEADER */
    header { margin-bottom: 36px; }
    header h1 { font-size: 26px; font-weight: 800; color: #fff; letter-spacing: -.02em; }
    .subtitle { color: var(--c-muted); margin-top: 6px; font-size: 13px; }
    .tag-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; }
    .tag {
      font-size: 11px; padding: 3px 9px; border-radius: 99px;
      border: 1px solid var(--c-border); background: var(--c-surface); color: var(--c-muted);
      font-family: monospace;
    }

    /* CATEGORY LEGEND */
    .legend { display: flex; gap: 20px; margin-bottom: 28px; flex-wrap: wrap; }
    .legend-item { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--c-muted); }
    .legend-dot { width: 10px; height: 10px; border-radius: 50%; }

    /* SCORES */
    .scores {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 14px;
      margin-bottom: 36px;
    }
    .score-card {
      background: var(--c-surface);
      border: 1px solid var(--c-border);
      border-radius: var(--radius);
      padding: 22px 18px 18px;
      text-align: center;
      position: relative;
      overflow: hidden;
    }
    .score-card::before {
      content: '';
      position: absolute; top: 0; left: 0; right: 0;
      height: 3px;
    }
    .score-card.cat-ux::before     { background: var(--c-ux); }
    .score-card.cat-layout::before { background: var(--c-layout); }
    .score-card.cat-css::before    { background: var(--c-css); }
    .score-card.cat-overall::before { background: var(--c-accent); }
    .score-card .label { font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--c-muted); margin-bottom: 10px; }
    .score-card .value { font-size: 42px; font-weight: 900; line-height: 1; }
    .score-card .sub  { font-size: 12px; color: var(--c-muted); margin-top: 4px; }
    .score-card .gauge { margin-top: 12px; height: 5px; border-radius: 99px; background: var(--c-border); overflow: hidden; }
    .score-card .gauge-fill { height: 100%; border-radius: 99px; }
    .score-good   .value, .score-good   .gauge-fill { color: var(--c-good);     background: var(--c-good); }
    .score-mid    .value, .score-mid    .gauge-fill { color: var(--c-medium);   background: var(--c-medium); }
    .score-bad    .value, .score-bad    .gauge-fill { color: var(--c-critical); background: var(--c-critical); }
    .cat-overall .value { color: #c4b5fd; }
    .cat-overall .gauge-fill { background: var(--c-accent); }

    /* FINDINGS */
    .pillrow { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 28px; }
    .pill {
      display: inline-flex; align-items: center; gap: 5px;
      padding: 5px 14px; border-radius: 99px;
      font-size: 13px; font-weight: 600;
    }
    .pill.critical { background: rgba(239,68,68,.12); color: var(--c-critical); border: 1px solid rgba(239,68,68,.3); }
    .pill.high     { background: rgba(249,115,22,.12); color: var(--c-high);     border: 1px solid rgba(249,115,22,.3); }
    .pill.medium   { background: rgba(234,179,8,.12);  color: var(--c-medium);   border: 1px solid rgba(234,179,8,.3); }
    .pill.low      { background: rgba(59,130,246,.12); color: var(--c-low);      border: 1px solid rgba(59,130,246,.3); }

    /* TABS */
    .tabs { display: flex; gap: 2px; margin-bottom: 20px; border-bottom: 1px solid var(--c-border); }
    .tab {
      padding: 8px 16px; font-size: 13px; font-weight: 500; cursor: pointer;
      color: var(--c-muted); border-bottom: 2px solid transparent;
      background: none; border-top: none; border-left: none; border-right: none;
      margin-bottom: -1px; transition: color .15s;
    }
    .tab.active { color: #fff; border-bottom-color: var(--c-accent); }

    .tab-content { display: none; }
    .tab-content.active { display: block; }

    /* SECTION */
    .section { margin-bottom: 28px; }
    .section-title {
      font-size: 14px; font-weight: 600; color: var(--c-muted);
      text-transform: uppercase; letter-spacing: .06em;
      margin-bottom: 12px;
      display: flex; align-items: center; gap: 8px;
    }
    .section-title .cnt {
      font-size: 12px; font-weight: 500; color: var(--c-muted);
      background: var(--c-surface); border: 1px solid var(--c-border);
      border-radius: 99px; padding: 1px 8px;
    }

    /* FINDING */
    .finding {
      background: var(--c-surface);
      border: 1px solid var(--c-border);
      border-left: 3px solid transparent;
      border-radius: var(--radius);
      padding: 14px 16px;
      margin-bottom: 10px;
    }
    .finding.critical { border-left-color: var(--c-critical); }
    .finding.high     { border-left-color: var(--c-high); }
    .finding.medium   { border-left-color: var(--c-medium); }
    .finding.low      { border-left-color: var(--c-low); }

    .finding-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }
    .badge {
      font-size: 10px; font-weight: 700; padding: 2px 7px;
      border-radius: 4px; text-transform: uppercase; letter-spacing: .05em;
    }
    .badge.critical { background: rgba(239,68,68,.15); color: var(--c-critical); }
    .badge.high     { background: rgba(249,115,22,.15); color: var(--c-high); }
    .badge.medium   { background: rgba(234,179,8,.15);  color: var(--c-medium); }
    .badge.low      { background: rgba(59,130,246,.15); color: var(--c-low); }
    .badge.cat-ux     { background: rgba(6,182,212,.1);   color: #67e8f9; }
    .badge.cat-layout { background: rgba(245,158,11,.1);  color: #fcd34d; }
    .badge.cat-css    { background: rgba(236,72,153,.1);  color: #f9a8d4; }
    .badge.cat-other  { background: rgba(99,102,241,.1);  color: #a5b4fc; }

    .file-ref { font-family: monospace; font-size: 11px; color: var(--c-muted); }
    .finding-text { color: var(--c-text); margin-bottom: 8px; }
    .fix-box {
      background: rgba(34,197,94,.07);
      border: 1px solid rgba(34,197,94,.18);
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 12px; color: #86efac;
    }
    .fix-box b { font-weight: 600; }

    /* POSITIVES */
    .positives-box {
      background: rgba(34,197,94,.05);
      border: 1px solid rgba(34,197,94,.18);
      border-radius: var(--radius);
      padding: 20px;
      margin-bottom: 28px;
    }
    .positives-box h3 { color: var(--c-good); font-size: 14px; font-weight: 600; margin-bottom: 10px; }
    .positives-box ul { padding-left: 18px; }
    .positives-box li { color: #bbf7d0; margin-bottom: 4px; }

    /* ACTION PLAN */
    .action-plan {
      background: var(--c-surface);
      border: 1px solid var(--c-border);
      border-radius: var(--radius);
      padding: 20px;
      margin-bottom: 36px;
    }
    .action-plan h3 { font-size: 15px; font-weight: 600; margin-bottom: 14px; }
    .action-item {
      display: flex; gap: 12px;
      padding: 10px 0;
      border-bottom: 1px solid var(--c-border);
    }
    .action-item:last-child { border-bottom: none; padding-bottom: 0; }
    .action-num {
      flex-shrink: 0;
      width: 24px; height: 24px; border-radius: 50%;
      background: var(--c-accent); color: #fff;
      font-size: 12px; font-weight: 700;
      display: flex; align-items: center; justify-content: center;
    }
    .action-text { font-size: 13px; }

    footer {
      border-top: 1px solid var(--c-border);
      padding-top: 18px;
      font-size: 11px; color: var(--c-muted);
    }

    @media print {
      body { background: #fff; color: #111; }
      .finding, .score-card { border-color: #ccc; }
      .tab-content { display: block !important; }
      .tabs { display: none; }
    }
  </style>
  <script>
    function switchTab(tabId, btn) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      btn.classList.add('active');
    }
  </script>
</head>
<body>

<header>
  <h1>Design & CSS Review</h1>
  <div class="subtitle">Full frontend audit · [DATE] · [N] components · [M] stylesheets</div>
  <div class="tag-row">
    <!-- one .tag per key scanned directory/file -->
  </div>
</header>

<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:var(--c-ux)"></div> UX & Components</div>
  <div class="legend-item"><div class="legend-dot" style="background:var(--c-layout)"></div> Layout & Spacing</div>
  <div class="legend-item"><div class="legend-dot" style="background:var(--c-css)"></div> CSS Architecture</div>
</div>

<!-- SCORES -->
<div class="scores">
  <div class="score-card cat-ux score-[good|mid|bad]">
    <div class="label">UX Quality</div>
    <div class="value">X</div>
    <div class="sub">/10</div>
    <div class="gauge"><div class="gauge-fill" style="width:X0%"></div></div>
  </div>
  <div class="score-card cat-layout score-[good|mid|bad]">
    <div class="label">Layout System</div>
    <div class="value">X</div>
    <div class="sub">/10</div>
    <div class="gauge"><div class="gauge-fill" style="width:X0%"></div></div>
  </div>
  <div class="score-card cat-css score-[good|mid|bad]">
    <div class="label">CSS Architecture</div>
    <div class="value">X</div>
    <div class="sub">/10</div>
    <div class="gauge"><div class="gauge-fill" style="width:X0%"></div></div>
  </div>
  <div class="score-card cat-ux score-[good|mid|bad]">
    <div class="label">Accessibility</div>
    <div class="value">X</div>
    <div class="sub">/10</div>
    <div class="gauge"><div class="gauge-fill" style="width:X0%"></div></div>
  </div>
  <div class="score-card cat-layout score-[good|mid|bad]">
    <div class="label">Typography</div>
    <div class="value">X</div>
    <div class="sub">/10</div>
    <div class="gauge"><div class="gauge-fill" style="width:X0%"></div></div>
  </div>
  <div class="score-card cat-overall" style="border-color: rgba(139,92,246,.4)">
    <div class="label">Overall</div>
    <div class="value">X</div>
    <div class="sub">/10</div>
    <div class="gauge"><div class="gauge-fill" style="width:X0%"></div></div>
  </div>
</div>

<!-- SEVERITY SUMMARY -->
<div class="pillrow">
  <span class="pill critical">● X Critical</span>
  <span class="pill high">● X High</span>
  <span class="pill medium">● X Medium</span>
  <span class="pill low">● X Low</span>
</div>

<!-- TABBED FINDINGS -->
<div class="tabs">
  <button class="tab active" onclick="switchTab('tab-all', this)">All Findings</button>
  <button class="tab" onclick="switchTab('tab-ux', this)">UX & Components</button>
  <button class="tab" onclick="switchTab('tab-layout', this)">Layout & Spacing</button>
  <button class="tab" onclick="switchTab('tab-css', this)">CSS Architecture</button>
</div>

<div id="tab-all" class="tab-content active">
  <div class="section">
    <div class="section-title">Critical & High <span class="cnt">X</span></div>
    <!-- critical/high findings from all agents -->
    <div class="finding critical">
      <div class="finding-meta">
        <span class="badge critical">Critical</span>
        <span class="badge cat-ux">UX</span>
        <span class="file-ref">Button.tsx</span>
      </div>
      <div class="finding-text">Interactive element has no keyboard handler — users cannot activate via Enter/Space.</div>
      <div class="fix-box"><b>Fix:</b> Add onKeyDown handler or replace div with a native button element.</div>
    </div>
  </div>
  <div class="section">
    <div class="section-title">Medium & Low <span class="cnt">X</span></div>
    <!-- medium/low findings -->
  </div>
</div>

<div id="tab-ux" class="tab-content">
  <!-- UX-only findings -->
</div>

<div id="tab-layout" class="tab-content">
  <!-- Layout-only findings -->
</div>

<div id="tab-css" class="tab-content">
  <!-- CSS-only findings -->
</div>

<!-- POSITIVES -->
<div class="positives-box">
  <h3>✓ What's Working Well</h3>
  <ul>
    <li>Consistent use of design tokens for colors across all components</li>
    <!-- more from agents -->
  </ul>
</div>

<!-- ACTION PLAN -->
<div class="action-plan">
  <h3>Recommended Action Plan</h3>
  <div class="action-item">
    <div class="action-num">1</div>
    <div class="action-text">[Top priority action from critical findings]</div>
  </div>
  <div class="action-item">
    <div class="action-num">2</div>
    <div class="action-text">[Second priority]</div>
  </div>
  <div class="action-item">
    <div class="action-num">3</div>
    <div class="action-text">[Third priority]</div>
  </div>
</div>

<footer>
  Generated by /review-design · frontend plugin · [TIMESTAMP]
</footer>

</body>
</html>
```

**Populate the report:**
- Score classes: `score-good` for 8-10, `score-mid` for 5-7, `score-bad` for 1-4
- Category badge classes: `cat-ux`, `cat-layout`, `cat-css`
- Tab sections: duplicate relevant findings into each tab
- Action plan: ordered list of top 5 concrete improvements, starting with Critical

**Open the file:**

```bash
start .design-review/report.html     # Windows
open .design-review/report.html      # macOS
xdg-open .design-review/report.html  # Linux
```

**Print a short summary** in the conversation:

```
Design & CSS review complete.

Report: .design-review/report.html

Overall Score: X/10
UX: X/10 | Layout: X/10 | CSS: X/10 | Accessibility: X/10

Critical: X | High: X | Medium: X | Low: X

Top 3 issues:
1. [critical issue summary]
2. [high issue summary]
3. [high issue summary]
```

If `--strict-mode` is set and Critical findings exist:
```
⚠️  STRICT MODE: X critical design issues found. Recommend addressing before shipping.
```
