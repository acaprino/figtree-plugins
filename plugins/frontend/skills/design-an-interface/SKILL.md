---
name: design-an-interface
description: >
  Generate multiple radically different interface designs for a module using parallel sub-agents.
  Use when user wants to design an API, explore interface options, compare module shapes, or
  mentions "design it twice".
---

# Design an Interface

"Your first idea is unlikely to be the best." -- Ousterhout, *A Philosophy of Software Design*

Spawn 3+ parallel sub-agents to generate radically different interface/component designs, then compare them systematically. The goal is structural divergence -- exploring fundamentally different shapes before committing to one.

## Phase 1: Gather Requirements

Before spawning any agents, understand the problem space:

- **What** does the module/component do? Core responsibility in one sentence
- **Who** calls it? List the callers and their contexts
- **Key operations** -- what are the 3-5 things users must be able to do?
- **Constraints** -- performance, compatibility, platform, bundle size
- **What to hide** -- implementation details that callers should never see
- **What to expose** -- the minimal surface callers actually need

Ask the user if any of these are unclear. Do not proceed to generation with ambiguous requirements.

## Phase 2: Generate Designs

Spawn 3-4 sub-agents in parallel using the Task tool. Each agent gets the same requirements but a different design constraint that forces a radically different solution shape:

**Agent 1 -- Minimal Surface**
> "Design an interface with 1-3 methods/props maximum. Hide everything possible. Callers should barely know what's inside."

**Agent 2 -- Maximum Flexibility**
> "Design an interface that supports many use cases and edge cases. Prioritize extensibility and composition over simplicity."

**Agent 3 -- Common Case Optimized**
> "Design an interface optimized for the single most common use case. Make that path trivial -- one line if possible. Other cases can be harder."

**Agent 4 (optional) -- Paradigm Shift**
> "Design an interface inspired by [specific paradigm: declarative, event-driven, builder pattern, hooks, etc.]. Break the mold."

Each agent must produce:
- Interface signature (types, props, methods, or component API)
- 2-3 usage examples showing real caller code
- What it hides vs. what it exposes
- One paragraph: why this shape fits the requirements

## Phase 3: Present Designs

Present each design sequentially. For each:
1. Name it (e.g., "Minimal Gateway", "Swiss Army Knife", "Happy Path")
2. Show the interface signature
3. Show the usage examples
4. State what it hides

Do not editorialize yet -- just present.

## Phase 4: Compare Designs

Evaluate all designs against these axes. Use prose, not tables -- tables flatten nuance.

- **Interface simplicity** -- how small is the surface? Can a new developer use it in 5 minutes?
- **General-purpose vs. specialized** -- does it serve many callers or optimize for one?
- **Implementation efficiency** -- which shape leads to the cleanest implementation?
- **Depth** -- small interface hiding significant complexity = deep module (good). Large interface with thin implementation = shallow module (bad)
- **Ease of correct use vs. ease of misuse** -- which design makes it hard to use wrong?

Highlight where designs make fundamentally different trade-offs. Name the trade-off explicitly (e.g., "Design A trades flexibility for simplicity").

## Phase 5: Synthesize

- Identify insights that emerged from the comparison
- Note if one design clearly dominates or if the best path combines elements from multiple
- Ask the user which direction fits their context best
- Do NOT implement -- this skill is purely about interface shape

## Anti-Patterns

- **Convergent designs** -- if two agents produce similar shapes, the constraints were too weak. Rerun with sharper constraints
- **Skipping comparison** -- presenting designs without systematic evaluation defeats the purpose. Always run Phase 4
- **Premature implementation** -- this skill produces interface signatures and usage examples, not working code. Implementation comes after the user chooses a direction
- **Table-driven comparison** -- tables compress trade-offs into cells. Use prose to explain why each axis matters for this specific problem
