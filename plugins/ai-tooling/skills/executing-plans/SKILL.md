---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints. Also use when a plan file exists in docs/plans/ or when resuming complex multi-step work from a previous session -- executes tasks in batches with verification between each batch.
  TRIGGER when: user says 'execute the plan', 'run the plan', 'implement the plan', 'start implementing', 'execute this', 'follow the plan', or a plan file exists in docs/plans/ and user wants to build it.
  DO NOT TRIGGER when: user wants to write a plan (use writing-plans), wants to brainstorm (use brainstorming), or is doing ad-hoc implementation without a plan file.
---

Source: Ported from [obra/superpowers](https://github.com/obra/superpowers) -- `skills/executing-plans`

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** This skill works best on platforms with subagent support (such as Claude Code or Codex). When subagents are available, prefer dispatching a fresh subagent per task for higher quality results.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Verify all tests pass
- Present summary of what was built
- Offer options: merge to main, create PR, or clean up branch (squash commits, update docs)

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Related skills and practices:**
- **ai-tooling:writing-plans** - Creates the plan this skill executes
- Use a git worktree or dedicated branch to isolate work before starting
- After completion: verify tests pass, then merge, create PR, or clean up branch
