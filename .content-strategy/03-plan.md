# Content Strategy Plan

## Findings Summary

| Category | Critical | Important | Nice-to-have |
|----------|----------|-----------|--------------|
| UX & Conversion | 3 | 3 | 1 |
| Content & Copy | 3 | 7 | 2 |
| Social & Visual | 1 | 4 | 3 |
| **Total** | **7** | **14** | **6** |

---

## Quick Wins (high impact, low effort)

### 1. Add GitHub badges after H1
**Before:** Title followed immediately by description.
**After:**
```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Marketplace](https://img.shields.io/badge/marketplace-v1.53.0-green.svg)](.claude-plugin/marketplace.json)
[![Plugins](https://img.shields.io/badge/plugins-22-orange.svg)](#plugins-overview)
```

### 2. Rewrite opening paragraph (benefit-driven + stats)
**Before:** "Custom Claude Code plugin marketplace with development workflow agents, skills, and commands for Python development, code review, Tauri/Rust, frontend, AI tooling, Obsidian plugins, constraint programming, and more."
**After:** "22 ready-to-install plugins for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) -- an AI coding CLI by Anthropic. Specialized agents, skills, and commands for Python, code review, frontend, Tauri/Rust, AI tooling, Obsidian, and more -- so you spend less time prompting and more time shipping."

Plus stats line: **22 plugins | 21 agents | 25 skills | 18 commands** -- install only what you need.

### 3. Trim install block to 3 examples + reference
**Before:** All 22 `claude plugin install` commands listed.
**After:** 3 representative examples + "See [Plugins Overview](#plugins-overview) for all 22 available plugins."

### 4. Move totals line to top (after opening paragraph)
Remove from bottom of file, incorporate as stats line near top.

### 5. Add "What is Claude Code?" context link
One-line context for users discovering via search: link to Anthropic docs.

### 6. Add author link in License section
`Created and maintained by [Alfio](https://github.com/acaprino).`

---

## Medium Effort

### 7. Add "Why use these plugins?" section before Installation
4-6 benefit bullets:
- Specialized agents outperform generic prompts
- Multi-agent orchestration (3 review agents run in parallel)
- Cross-plugin workflows chain brainstorm -> plan -> implement -> review -> cleanup
- Install only what you need -- no runtime dependencies
- Community-driven, open source

### 8. Add concepts explainer (agents vs skills vs commands)
Brief section after "Why" explaining the three plugin types with one-sentence definitions.

### 9. Move Usage Examples above individual plugin details
Relocate from line 1472 to right after the overview table. Rename to "Quick Start Workflows."

### 10. Group TOC by category
- **Development:** python-development, typescript-development, tauri-development, obsidian-development, browser-extensions
- **Frontend:** frontend, frontend-design
- **Review & Quality:** code-review, humanize, deep-dive-analysis, code-documentation
- **AI & Planning:** ai-tooling, research, project-setup
- **Infrastructure:** messaging, csp, stripe, business
- **Tools & Workflows:** utilities, workflows, app-explorer, mobile-development, digital-marketing

### 11. Rewrite overview table descriptions (feature -> benefit)
| Current | Suggested |
|---------|-----------|
| "Modern Python, Django, FastAPI, testing, packaging" | "Build production-ready Python apps faster with Django, FastAPI, testing, and packaging agents" |
| "Multi-agent review orchestration (architecture, security, patterns)" | "Catch bugs before they ship -- 3 agents review architecture, security, and patterns in parallel" |
| "Cross-plugin orchestration pipelines" | "Run entire dev workflows with one command -- brainstorm to review to cleanup" |
| "Code humanization -- readable naming, no AI boilerplate" | "Make AI-generated code look human-written -- fixes names, removes boilerplate" |

### 12. Add differentiation lines for similar plugins
- frontend vs frontend-design: "Use `frontend` for React/CSS optimization. Use `frontend-design` for designing new interfaces from scratch."

### 13. Wrap project structure in `<details>` collapsible
Reduces visible length by ~137 lines for casual readers.

---

## Major Recommendations

### 14. Create social preview image (1280x640)
Design: project name, tagline, stats, category keywords. Set via GitHub Settings > Social preview.

### 15. Record terminal demo GIF
Show: marketplace add -> plugin install -> use a command. Place after Installation header.

### 16. Split into multi-page docs (long-term)
Keep README as ~200-line landing page. Move individual plugin details to `docs/plugins/<name>.md`. Link from overview table.

### 17. Rewrite all 22 plugin blockquotes for benefit framing
Transform each `> Feature list` into `> Outcome statement`.

---

## Estimated Conversion Impact

| Change | Expected Impact | Effort |
|--------|----------------|--------|
| Benefit-driven opening + stats | High -- first impression drives install decision | 10 min |
| GitHub badges | Medium -- credibility at a glance | 5 min |
| "Why use this?" section | High -- answers the key question before install | 15 min |
| Move Usage Examples up | High -- demonstrates value before detail overload | 10 min |
| TOC grouping by category | Medium -- faster navigation for returning users | 15 min |
| Trim install block | Medium -- reduces overwhelm for new users | 5 min |
| Overview table benefit rewrites | Medium -- each row becomes a selling point | 20 min |
| Social preview image | High -- transforms every share into branding | 30-60 min |
| Concepts explainer | Medium -- removes confusion for new users | 10 min |
| `<details>` for project structure | Low -- reduces visual noise | 5 min |
