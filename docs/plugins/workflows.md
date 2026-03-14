# Workflows Plugin

> Run entire development workflows with one command. Chains brainstorming, planning, implementation, code review, and cleanup into automated pipelines with checkpoints at each stage.

## Commands

### `/feature-e2e`

End-to-end feature pipeline: brainstorm design, write implementation plan, execute with TDD checkpoints, review changes (architecture + security + patterns), and humanize code.

| | |
|---|---|
| **Invoke** | `/feature-e2e <feature description> [--skip-brainstorm] [--skip-humanize] [--strict-mode]` |
| **Pipeline** | brainstorming -> writing-plans -> executing-plans -> senior-review -> humanize |
| **Checkpoints** | After design, plan, execution, and review phases |
| **Dependencies** | ai-tooling, senior-review, humanize plugins |

### `/frontend-redesign`

Full frontend redesign pipeline: UX audit, layout system design, implementation, React performance optimization, UI polish, and final design audit with visual report. Use this to **improve existing frontend code** -- not for planning or building from scratch.

| | |
|---|---|
| **Invoke** | `/frontend-redesign <target path> [--framework react\|vue\|svelte] [--skip-performance] [--strict-mode]` |
| **Pipeline** | ui-ux-designer -> ui-layout-designer -> frontend-design -> react-performance-optimizer -> ui-polisher -> design audit |
| **Checkpoints** | After layout spec and polish phases |
| **Output** | `.frontend-redesign/report.md` -- actionable checklist with before/after comparison |
| **Dependencies** | frontend plugin |

> **Not sure which to use?** `/frontend:premium-web-consultant` for strategy ("what to build"), `/frontend:ui-studio` for new builds ("build it from scratch"), `/frontend-redesign` for existing code ("improve what we have").

### `/mobile-intel`

Competitive mobile intelligence: analyze competitor Android app via ADB, brainstorm differentiating features, design improved UX, write implementation plan, and scaffold Tauri 2 mobile app.

| | |
|---|---|
| **Invoke** | `/mobile-intel <app-package-name> [--device <device-id>] [--skip-scaffold]` |
| **Pipeline** | analyze-mobile-app -> brainstorming -> ui-ux-designer -> writing-plans -> tauri2-mobile |
| **Checkpoints** | After analysis, brainstorm, and plan phases |
| **Pre-flight** | Verifies ADB device connection |
| **Dependencies** | mobile-development, ai-tooling, frontend, tauri-development plugins |

### `/tauri-pipeline`

End-to-end Tauri 2 desktop app pipeline: Rust backend review, Tauri IPC optimization, React performance, layout composition, and UI polish.

| | |
|---|---|
| **Invoke** | `/tauri-pipeline <target path> [--rust-only] [--frontend-only] [--strict-mode]` |
| **Pipeline** | rust-engineer -> tauri-optimizer -> react-performance-optimizer -> ui-layout-designer -> ui-polisher |
| **Checkpoints** | After Tauri IPC review |
| **Pre-flight** | Verifies `src-tauri/` directory and `tauri.conf.json` exist |
| **Dependencies** | tauri-development, frontend plugins |

### `/full-review`

Full codebase review pipeline: deep-dive structural analysis followed by senior multi-agent code review with consolidated scoring.

| | |
|---|---|
| **Invoke** | `/full-review <target path or description> [--skip-deep-dive] [--security-focus] [--performance-critical] [--strict-mode] [--framework react\|spring\|django\|rails]` |
| **Pipeline** | deep-dive-analysis -> architect-review -> security-auditor -> pattern-quality-scorer -> consolidated report |
| **Checkpoints** | After deep-dive and after architecture/security phases |
| **Dependencies** | deep-dive-analysis, senior-review plugins |

### `/mobile-tauri-pipeline`

End-to-end mobile app pipeline: competitor analysis via ADB, brainstorm features, UX design, implementation plan, scaffold Tauri 2 mobile app, Rust backend review, and IPC optimization.

| | |
|---|---|
| **Invoke** | `/mobile-tauri-pipeline <app-package-name or description> [--device <device-id>] [--skip-scaffold] [--skip-review] [--strict-mode]` |
| **Pipeline** | analyze-mobile-app -> brainstorming -> ui-ux-designer -> writing-plans -> tauri2-mobile -> rust-engineer -> tauri-optimizer |
| **Checkpoints** | After analysis, brainstorm, plan, and scaffold phases |
| **Dependencies** | mobile-development, ai-tooling, frontend, tauri-development plugins |

### `/ui-studio`

End-to-end UI development pipeline: brainstorm product concept, design direction, layout, UX patterns, write implementation plan, execute with TDD, polish, performance review, and code review.

| | |
|---|---|
| **Invoke** | `/ui-studio <product goal or feature description> [--skip-brainstorm] [--skip-review] [--skip-humanize] [--strict-mode] [--framework react\|vue\|svelte\|html]` |
| **Pipeline** | brainstorming -> ui-ux-designer -> ui-layout-designer -> writing-plans -> executing-plans -> ui-polisher -> react-performance-optimizer -> code-review -> humanize |
| **Checkpoints** | After design, plan, execution, polish, and review phases |
| **Dependencies** | ai-tooling, frontend, senior-review, humanize plugins |
