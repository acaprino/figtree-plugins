---
description: "Unified frontend design review -- auto-detects scope: diff mode for changed frontend files, or full audit for entire frontend. UX patterns, component hierarchy, spacing, typography, accessibility, CSS architecture, and React performance -- outputs an actionable markdown report"
argument-hint: "[src-path] [--full] [--framework react|vue|svelte] [--strict-mode]"
---

# Frontend Design & Performance Review

You are a senior frontend design auditor. Review frontend code for design quality, layout, CSS architecture, and performance. Auto-detects scope based on git state.

## CRITICAL RULES

1. **Auto-detect scope.** Check git diff for frontend file changes first. If found, review only changed files (diff mode, 3 agents). If no diff or `--full` flag, audit the entire frontend (full mode, 4 agents).
2. **Design + CSS + Performance.** Ignore backend files, API routes, build config. Focus on components, stylesheets, layout files, state management.
3. **Run all agents in parallel.** Fire all in a single response.
4. **Write markdown report.** Output is `.design-review/report.md` -- an actionable checklist with scores, findings, and fix instructions.
5. **Never enter plan mode.** Execute immediately.

## Step 1: Detect Scope

### Check for changed frontend files

```bash
git diff HEAD --name-only | grep -E '\.(tsx|jsx|vue|svelte|css|scss|sass|less|html)$'
git diff --name-only | grep -E '\.(tsx|jsx|vue|svelte|css|scss|sass|less|html)$'
git diff --cached --name-only | grep -E '\.(tsx|jsx|vue|svelte|css|scss|sass|less|html)$'
```

### Decision tree

**Diff mode** (changed frontend files exist AND `--full` is NOT set):
- Review only the changed frontend files
- Get the diff: `git diff HEAD -- <frontend files>`
- Run 3 agents: UX & Components, CSS & Visual Polish, React Performance
- This is the default when uncommitted frontend changes exist

**Full mode** (no frontend changes in diff, OR `--full` flag set):
- Scan entire frontend: `src/`, `app/`, `components/`, `pages/`, `styles/` -- or path from `$ARGUMENTS`
- Run 4 agents: UX & Components, Layout System, CSS & Visual Polish, React Performance

### Discover frontend files (full mode only)

```bash
find src -type f \( -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" -o -name "*.css" -o -name "*.scss" -o -name "*.sass" \) | head -80
```

Or use the path from `$ARGUMENTS` if provided. List what you find -- components, pages, and stylesheet files.

If no frontend files are found, stop and say so.

## Step 2: Sample Key Files & Gather Context

Read a representative cross-section:
- Entry layout files (e.g., `App.tsx`, `Layout.tsx`, `_app.tsx`, `root.tsx`)
- 3-5 core components
- Primary stylesheet(s) or `globals.css` / `tailwind.config`
- Design token files (`tokens.ts`, `theme.ts`, `variables.css`)
- State management files (stores, contexts, atoms)

This gives you the design language, patterns, and architecture to evaluate against.

**UI Studio brief check:** Look for a product brief file (`brief.md`, `product-brief.md`, or similar) in the project root or docs directory. If found, use it as the north star for evaluating design coherence -- every UX, layout, and aesthetic decision should align with the stated goal, audience, and aesthetic tone from the brief. Pass the brief content to all agents as evaluation context.

## Step 3: Run Parallel Review Agents

Fire all agents **in parallel** in a single response (3 in diff mode, 4 in full mode):

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

    ## Product Brief (if available)
    [paste brief content or "No product brief found -- evaluate against general UX best practices"]

    ## Instructions
    Evaluate:
    1. **Component responsibility**: God components, missing abstractions, component prop explosion
    2. **UX patterns**: Consistency of interaction patterns (forms, modals, navigation, data loading)
    3. **Empty/loading/error states**: Are all three states handled everywhere they're needed?
    4. **Information hierarchy**: Is visual hierarchy consistent? Do primary/secondary/tertiary actions follow a system?
    5. **User flows**: Are there obvious dead ends, missing feedback, or confusing navigation?
    6. **Design system adherence**: Are colors, spacing, and typography from a token system, or are they scattered arbitrary values?
    7. **Accessibility audit**: Semantic HTML, ARIA roles, keyboard navigation, focus management, color contrast awareness
    8. **Brief alignment** (if brief provided): Does the UX serve the stated goal and audience? Are interaction patterns appropriate for the target user?

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

    ## Product Brief (if available)
    [paste brief content or "No product brief found -- evaluate against general layout best practices"]

    ## Instructions
    Evaluate:
    1. **Layout system**: Is there a consistent grid/layout pattern (CSS Grid, Flexbox, utility classes)? Or ad-hoc layouts per component?
    2. **Spacing scale**: Is spacing derived from a consistent scale (4px/8px/rem)? Or arbitrary pixel values scattered everywhere?
    3. **Responsive strategy**: Are breakpoints consistent? Mobile-first vs desktop-first? Are there layout shifts on resize?
    4. **Typography system**: Font scale, line-height, letter-spacing -- are they tokens or raw values?
    5. **Alignment & rhythm**: Do elements align to a clear baseline? Is vertical rhythm maintained?
    6. **Above-the-fold**: Is the critical viewport optimized? Is the most important content immediately visible?
    7. **Container strategy**: Max-widths, centering, content containers -- are they consistent?
    8. **Brief alignment** (if brief provided): Does the layout serve the stated audience and aesthetic tone? Is the spatial hierarchy appropriate?

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

    ## Product Brief (if available)
    [paste brief content or "No product brief found -- evaluate against general CSS and visual polish best practices"]

    ## Instructions
    Evaluate:
    1. **CSS architecture**: Global styles pollution, specificity wars, selector depth, !important abuse
    2. **Modern CSS usage**: Are CSS custom properties used? Container queries? Logical properties? Or legacy patterns?
    3. **Animation quality**: Transitions feel smooth? GPU-accelerated properties? prefers-reduced-motion respected?
    4. **Visual consistency**: Border-radius, shadow elevation, color palette -- are they consistent or scattered?
    5. **Dark mode**: Is dark mode supported? Are colors properly adapted or just inverted?
    6. **CSS performance**: Unnecessary repaints, layout-triggering animations, oversized background images
    7. **Dead CSS**: Unused selectors, legacy overrides, commented-out blocks
    8. **Component isolation**: Are styles scoped or do they leak? CSS Modules / Tailwind / CSS-in-JS used correctly?
    9. **Brief alignment** (if brief provided): Does the visual polish match the stated aesthetic tone? Is motion appropriate for the audience?

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

### Agent D: React Performance (React/Next.js projects only)

Skip this agent if the project does not use React/Next.js.

```
Task:
  subagent_type: "react-performance-optimizer"
  description: "React performance and bundle optimization audit"
  prompt: |
    Audit the React performance, state management, and bundle optimization of this frontend codebase.

    ## Scope
    [list of key files sampled]

    ## File Contents
    [paste sampled component, state management, and config file contents]

    ## Product Brief (if available)
    [paste brief content -- especially performance budget and stack info -- or "No product brief found"]

    ## Instructions
    Evaluate:
    1. **Re-render prevention**: External store selectors returning objects/arrays without useShallow, missing memoization, component splitting
    2. **State management**: Zustand/Jotai/Redux selector patterns, prop drilling, state duplication, useEffect chains
    3. **React Compiler readiness**: Patterns the compiler can optimize vs patterns requiring manual intervention
    4. **Bundle optimization**: Heavy imports, missing code splitting, lazy loading opportunities, tree-shaking blockers
    5. **Virtualization**: Large lists/tables not using virtual scrolling
    6. **Caching strategy**: TanStack Query config, stale times, cache invalidation patterns
    7. **useEffect cleanup**: Missing AbortControllers, unsubscribed listeners, memory leak vectors
    8. **Performance budget** (if brief provided): Does the current state meet the stated Core Web Vitals or performance targets?

    For each finding: severity (Critical/High/Medium/Low), file, issue, specific fix with code example.
    Note what's done well.

    Return structured JSON at the end:
    ```json
    {
      "findings": [
        { "severity": "Critical", "category": "Re-renders", "file": "...", "issue": "...", "fix": "..." }
      ],
      "positives": ["..."],
      "score": { "re_render_control": 6, "state_management": 7, "bundle": 8, "overall": 7 }
    }
    ```
```

## Step 4: Generate Markdown Report

After all agents complete, create `.design-review/` directory and write `report.md`.

Merge and deduplicate overlapping findings from all agents. Order by severity, then file name. Group findings by category (UX, Layout, CSS, Performance).

**Output file:** `.design-review/report.md`

```markdown
# Design & Performance Review -- [date]

Full frontend audit · [N] components · [M] stylesheets

## Product Brief Context

[If a product brief was found, summarize goal, audience, aesthetic tone, and performance budget. If not, note "No product brief found -- reviewed against general best practices."]

## Scores

| Category | Score |
|----------|-------|
| UX Quality | X/10 |
| Layout System | X/10 |
| CSS Architecture | X/10 |
| Accessibility | X/10 |
| Typography | X/10 |
| React Performance | X/10 |
| **Overall** | **X/10** |

Critical: X | High: X | Medium: X | Low: X

## Files Audited

- `Component.tsx`, `Layout.tsx`, `globals.css`, ...

---

## Critical & High Issues

### UX & Components

#### `Button.tsx` -- [issue title]
- **Severity**: Critical
- **Issue**: [description]
- **Fix**: [concrete fix instruction]
- [ ] Fixed

### Layout & Spacing

#### `Layout.tsx` -- [issue title]
- **Severity**: High
- **Issue**: [description]
- **Fix**: [fix instruction]
- [ ] Fixed

### CSS Architecture

#### `globals.css` -- [issue title]
- **Severity**: High
- **Issue**: [description]
- **Fix**: [fix instruction]
- [ ] Fixed

### React Performance

#### `Store.ts` -- [issue title]
- **Severity**: Critical
- **Issue**: [description]
- **Fix**: [fix instruction with code]
- [ ] Fixed

---

## Medium & Low Issues

### UX & Components
[Same format as above]

### Layout & Spacing
[Same format]

### CSS Architecture
[Same format]

### React Performance
[Same format]

---

## What's Working Well

- [positive observation from agents]
- [another positive]

---

## Action Plan

1. [ ] [top priority fix -- from critical findings]
2. [ ] [second priority]
3. [ ] [third priority]
4. [ ] [fourth priority]
5. [ ] [fifth priority]
```

**Print a short summary** in the conversation:

```
Design & performance review complete.

Report: .design-review/report.md

Overall Score: X/10
UX: X/10 | Layout: X/10 | CSS: X/10 | Performance: X/10 | Accessibility: X/10

Critical: X | High: X | Medium: X | Low: X

Top 3 issues:
1. [critical issue summary]
2. [high issue summary]
3. [high issue summary]
```

If `--strict-mode` is set and Critical findings exist:
```
STRICT MODE: X critical design/performance issues found. Recommend addressing before shipping.
```
