# Frontend Plugin Restructure Implementation Plan

> **For agentic workers:** Use subagent-driven execution (if subagents available) or ai-tooling:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge 3 web-specific agents into one `web-designer` agent and consolidate CSS + agent references into a unified `frontend` skill.

**Architecture:** Move reference files via `git mv` to preserve history. Create new `web-designer.md` agent by merging content from `ui-ux-designer`, `ui-polisher`, and `css-master`. Create unified `frontend/SKILL.md` as entry point to all moved references. Update marketplace, docs, and CLAUDE.md.

**Tech Stack:** Markdown, YAML frontmatter, JSON (marketplace.json)

**Spec:** `docs/plans/2026-03-17-frontend-plugin-restructure-design.md`

---

## Chunk 1: File moves and unified skill

### Task 1: Create unified frontend skill directory and move references

All paths relative to repo root `D:/Projects/anvil-toolset`.

**Files:**
- Create: `plugins/frontend/skills/frontend/references/` (directory)
- Move: 6 reference files into it
- Delete: `plugins/frontend/skills/css-master/SKILL.md`, `plugins/frontend/skills/css-master/` directory, `plugins/frontend/agents/references/` directory

- [ ] **Step 1: Create target directory and move css-master skill references**

```bash
cd D:/Projects/anvil-toolset
mkdir -p plugins/frontend/skills/frontend/references
git mv plugins/frontend/skills/css-master/references/css-patterns.md plugins/frontend/skills/frontend/references/
git mv plugins/frontend/skills/css-master/references/argyle-cacadia-2025-deck.md plugins/frontend/skills/frontend/references/
```

- [ ] **Step 2: Move agent references**

```bash
git mv plugins/frontend/agents/references/flow-patterns.md plugins/frontend/skills/frontend/references/
git mv plugins/frontend/agents/references/layout-patterns.md plugins/frontend/skills/frontend/references/
git mv plugins/frontend/agents/references/ui-pattern-guide.md plugins/frontend/skills/frontend/references/
git mv plugins/frontend/agents/references/ux-patterns.md plugins/frontend/skills/frontend/references/
```

- [ ] **Step 3: Delete old css-master SKILL.md and empty directories**

```bash
git rm plugins/frontend/skills/css-master/SKILL.md
rm -rf plugins/frontend/skills/css-master
rm -rf plugins/frontend/agents/references
```

- [ ] **Step 4: Verify moves**

```bash
ls plugins/frontend/skills/frontend/references/
# Expected: argyle-cacadia-2025-deck.md  css-patterns.md  flow-patterns.md  layout-patterns.md  ui-pattern-guide.md  ux-patterns.md
```

### Task 2: Create unified frontend SKILL.md

**Files:**
- Create: `plugins/frontend/skills/frontend/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

Create `plugins/frontend/skills/frontend/SKILL.md` with:
- Frontmatter: `name: frontend`, description covering CSS, UX patterns, UI patterns, flow patterns, layout patterns
- Upstream source comment for `argyle-cacadia-2025-deck.md` (paulirish/dotfiles)
- Sections for each knowledge area with links to the 6 reference files:
  - CSS Architecture & Modern Features -> `references/css-patterns.md`, `references/argyle-cacadia-2025-deck.md`
  - UX Patterns -> `references/ux-patterns.md`
  - UI Pattern Guide -> `references/ui-pattern-guide.md`
  - Layout Patterns -> `references/layout-patterns.md`
  - Flow & Onboarding Patterns -> `references/flow-patterns.md`

- [ ] **Step 2: Verify all links resolve**

```bash
cd plugins/frontend/skills/frontend
grep -oE 'references/[a-z-]+\.md' SKILL.md | sort -u | while read f; do
  if [ -f "$f" ]; then echo "OK: $f"; else echo "MISSING: $f"; fi
done
```

Expected: all OK, no MISSING.

- [ ] **Step 3: Commit file moves and new skill**

```bash
git add plugins/frontend/skills/frontend/SKILL.md
git commit -m "Move references into unified frontend skill and create SKILL.md"
```

---

## Chunk 2: Agent merge

### Task 3: Create web-designer.md agent

**Files:**
- Create: `plugins/frontend/agents/web-designer.md`
- Source content from: `plugins/frontend/agents/ui-ux-designer.md`, `plugins/frontend/agents/ui-polisher.md`, `plugins/frontend/agents/css-master.md`

- [ ] **Step 1: Read all 3 source agents**

Read the full content of:
- `plugins/frontend/agents/ui-ux-designer.md`
- `plugins/frontend/agents/ui-polisher.md`
- `plugins/frontend/agents/css-master.md`

- [ ] **Step 2: Write web-designer.md**

Create `plugins/frontend/agents/web-designer.md` with merged content:

**Frontmatter:**
```yaml
---
name: web-designer
description: >
  Web-specific frontend expert covering CSS architecture, animations/micro-interactions,
  design systems, UX psychology, accessibility, and visual polish. Use PROACTIVELY
  for any web UI work -- styling, motion design, design tokens, component specification,
  or interface aesthetics.
model: opus
tools: Read, Write, Edit, Bash, Glob, Grep
color: purple
---
```

**Body structure** (~500-560 lines max per CLAUDE.md conventions):

1. **Intro** (2-3 lines): Senior web designer combining CSS architecture, motion design, and UX expertise
2. **Core Philosophy** (`<core_philosophy>` tag): merge key principles from all 3:
   - Native CSS first, specificity is architecture (css-master)
   - Animation is communication, restraint over excess (ui-polisher)
   - Design tokens first, accessibility baked in from wireframe stage (ui-ux-designer)
   - Performance-aware, 60fps animations or nothing
3. **Core Expertise** (bulleted list): CSS architecture + modern features, animations + micro-interactions + motion narrative, design systems + UX psychology + accessibility, visual styles + aesthetics, dark mode + theming
4. **Execution Flow**: context discovery -> design execution -> polish pass -> handoff (merged from all 3)
5. **CSS Architecture** (condensed from css-master agent): core expertise list, architecture rules, migration patterns, modern CSS priorities
6. **Animation & Motion** (condensed from ui-polisher): technical stack (Motion, GSAP, AutoAnimate), animation constants + easing rules, implementation patterns (hover lift, stagger, page transitions, skeleton shimmer), modern browser APIs (View Transitions, @starting-style, scroll-driven animations, transition-behavior: allow-discrete)
7. **Design Systems & UX** (condensed from ui-ux-designer): design token management, accessibility (WCAG), UX psychology laws, common UI patterns, visual styles & aesthetics, production details (5-second test, letter spacing, nested corners, spacing, HSB colors, card design, kill lines, button copy)
8. **Rules to Enforce** (`<rules_to_enforce>` tag): merge CSS architecture rules + animation constants/easing + UX laws + production details
9. **Quality Checklist**: merge all 3 agent checklists into one unified list
10. **Tool Directives** (`<tool_directives>` tag): merge all 3 (CSS grep patterns, animation patterns, design token patterns)
11. **Testing Directives** (`<testing_directives>` tag): merge all 3 (visual regression, axe-core, cross-browser, reduced-motion, viewport testing)
12. **Agent Delegation** (`<agent_delegation>` tag):
    - Layout structure/grid/breakpoints -> recommend `ui-layout-designer`
    - React re-render performance -> recommend `react-performance-optimizer`
    - This agent owns: CSS, animations, design tokens, UX, accessibility, visual polish
    - NO references to ui-polisher, ui-ux-designer, or css-master (they no longer exist)
13. **Reference pointers**: direct reader to `frontend` skill references via Read tool paths (updated to `plugins/frontend/skills/frontend/references/`)

**Key constraints:**
- Stay under ~560 lines
- Condense overlapping content (don't duplicate patterns that appear in 2+ agents)
- Keep all code examples that are unique/useful
- Remove all `<agent_delegation>` cross-references between the 3 merged agents
- Update reference file paths from `plugins/frontend/agents/references/` to `plugins/frontend/skills/frontend/references/`

### Task 4: Delete old agent files

**Files:**
- Delete: `plugins/frontend/agents/ui-polisher.md`
- Delete: `plugins/frontend/agents/ui-ux-designer.md`
- Delete: `plugins/frontend/agents/css-master.md`

- [ ] **Step 1: Remove old agents**

```bash
git rm plugins/frontend/agents/ui-polisher.md
git rm plugins/frontend/agents/ui-ux-designer.md
git rm plugins/frontend/agents/css-master.md
```

- [ ] **Step 2: Verify agent directory**

```bash
ls plugins/frontend/agents/
# Expected: ui-layout-designer.md  web-designer.md
```

### Task 5: Update ui-layout-designer.md references

**Files:**
- Modify: `plugins/frontend/agents/ui-layout-designer.md`

The ui-layout-designer agent has:
- Read tool paths pointing to `plugins/frontend/agents/references/` (old location)
- `<agent_delegation>` section referencing `ui-polisher`, `ui-ux-designer`, `css-master`

- [ ] **Step 1: Update reference paths**

Change all occurrences of `plugins/frontend/agents/references/` to `plugins/frontend/skills/frontend/references/` in `ui-layout-designer.md`.

- [ ] **Step 2: Update agent delegation section**

Replace references to `ui-polisher`, `ui-ux-designer`, and `css-master` with `web-designer` in the `<agent_delegation>` section.

- [ ] **Step 3: Commit agent changes**

```bash
git add plugins/frontend/agents/web-designer.md plugins/frontend/agents/ui-layout-designer.md
git commit -m "Add web-designer agent merging 3 web agents, update ui-layout-designer refs"
```

---

## Chunk 3: Marketplace, docs, and CLAUDE.md

### Task 6: Update marketplace.json

**Files:**
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Update frontend plugin entry**

In the `frontend` plugin entry:
- Change `agents` array to: `["./agents/web-designer.md", "./agents/ui-layout-designer.md"]`
- Change `skills` array: replace `"./skills/css-master"` with `"./skills/frontend"`, keep other 5 unchanged
- Keep `commands` array unchanged: `["./commands/review-design.md"]`
- Bump `version` from `"3.4.0"` to `"3.5.0"`

- [ ] **Step 2: Bump metadata version**

Increment `metadata.version` (current value + 1).

- [ ] **Step 3: Validate JSON**

```bash
python -c "import json; json.load(open('.claude-plugin/marketplace.json'))"
# Expected: no output (valid JSON)
```

### Task 7: Update docs/plugins/frontend.md

**Files:**
- Modify: `docs/plugins/frontend.md`

- [ ] **Step 1: Rewrite docs page**

Update to reflect:
- 2 agents: `web-designer` (web-specific CSS + polish + UX) and `ui-layout-designer` (universal layout)
- 6 skills: `frontend` (unified web knowledge), `frontend-design`, `premium-web-consultant`, `shadcn-ui`, `daisyui`, `radix-ui`
- 1 command: `review-design`
- Update agent descriptions, invocation examples
- Replace css-master skill listing with frontend skill listing
- Update the references table for the new frontend skill (6 references)

### Task 8: Update CLAUDE.md upstream sync table

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update upstream sync table row**

Find the `frontend (css-master)` row in the upstream sync table. Change:
- Row identifier: `frontend (css-master)` -> `frontend (frontend)`
- Local files column: `plugins/frontend/skills/css-master/SKILL.md`, `plugins/frontend/skills/css-master/references/argyle-cacadia-2025-deck.md` -> `plugins/frontend/skills/frontend/SKILL.md`, `plugins/frontend/skills/frontend/references/argyle-cacadia-2025-deck.md`

- [ ] **Step 2: Update gh api sync commands**

In the "How to sync a plugin" section, update the `paulirish/dotfiles` example comments and local target path references from `plugins/frontend/skills/css-master/` to `plugins/frontend/skills/frontend/`.

- [ ] **Step 3: Commit marketplace, docs, and CLAUDE.md**

```bash
git add .claude-plugin/marketplace.json docs/plugins/frontend.md CLAUDE.md
git commit -m "Update marketplace, docs, and CLAUDE.md for frontend plugin restructure"
```

---

## Chunk 4: Verification

### Task 9: Final verification

- [ ] **Step 1: Verify reference files**

```bash
ls plugins/frontend/skills/frontend/references/
# Expected 6 files: argyle-cacadia-2025-deck.md  css-patterns.md  flow-patterns.md  layout-patterns.md  ui-pattern-guide.md  ux-patterns.md
```

- [ ] **Step 2: Verify agents**

```bash
ls plugins/frontend/agents/
# Expected 2 files: ui-layout-designer.md  web-designer.md
```

- [ ] **Step 3: Verify skills**

```bash
ls plugins/frontend/skills/
# Expected 6 dirs: daisyui  frontend  frontend-design  premium-web-consultant  radix-ui  shadcn-ui
```

- [ ] **Step 4: Validate marketplace JSON**

```bash
python -c "import json; json.load(open('.claude-plugin/marketplace.json'))"
```

- [ ] **Step 5: Verify no orphan files in old directories**

```bash
ls plugins/frontend/skills/css-master 2>&1
# Expected: "No such file or directory"
ls plugins/frontend/agents/references 2>&1
# Expected: "No such file or directory"
```

- [ ] **Step 6: Verify SKILL.md links**

```bash
cd plugins/frontend/skills/frontend
grep -oE 'references/[a-z-]+\.md' SKILL.md | sort -u | while read f; do
  if [ -f "$f" ]; then echo "OK: $f"; else echo "MISSING: $f"; fi
done
# Expected: all OK
```

- [ ] **Step 7: Verify ui-layout-designer references updated**

```bash
grep 'agents/references/' plugins/frontend/agents/ui-layout-designer.md
# Expected: no output (all paths updated to skills/frontend/references/)
```

- [ ] **Step 8: Push to remote**

```bash
git push
```
