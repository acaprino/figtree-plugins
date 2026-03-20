---
name: cc-usage
description: >
  Analyze Claude Code token usage, costs, billing blocks, and tool activity from local session data.
  TRIGGER WHEN: the user asks about their usage, costs, burn rate, or wants a usage dashboard/report.
  DO NOT TRIGGER WHEN: the task is outside the specific scope of this component.
---

# Claude Code Usage Analyzer

Analyze Claude Code session data to generate usage reports with token counts, cost estimates, billing block tracking, tool usage stats, and per-project breakdowns.

Inspired by [paulrobello/par_cc_usage](https://github.com/paulrobello/par_cc_usage).

## How it works

Claude Code stores session data as JSONL files in:
- `~/.config/claude/projects/` (primary)
- `~/.claude/projects/` (legacy)
- Custom path via `CLAUDE_CONFIG_DIR` env var

The script parses these files, extracts assistant message token usage, deduplicates by request ID, and computes:
- Total token usage (input, output, cache)
- Cost estimates using Anthropic pricing
- 5-hour billing block tracking with burn rate
- Per-model breakdown (Opus vs Sonnet)
- Tool usage frequency
- Per-project and per-session stats
- Daily usage trends

## Usage

Run the analysis script:

```bash
python plugins/cc-usage/skills/cc-usage/scripts/cc_usage.py
```

### Options

| Flag | Description |
|------|-------------|
| `-d`, `--days N` | Number of days to analyze (default: 7) |
| `-p`, `--project NAME` | Filter by project name (substring match) |
| `--no-block` | Hide current billing block section |
| `--no-projects` | Hide project breakdown |
| `--no-tools` | Hide tool usage stats |
| `--no-sessions` | Hide recent sessions list |
| `-n`, `--top N` | Number of top items per section (default: 10) |
| `--json` | Output raw JSON instead of formatted markdown |

### Examples

```bash
# Last 7 days, full report
python cc_usage.py

# Last 30 days, filter to one project
python cc_usage.py -d 30 -p "my-project"

# Quick overview, no details
python cc_usage.py --no-tools --no-sessions -n 5

# Machine-readable JSON output
python cc_usage.py --json
```

## When to invoke

Run this script for the user when they ask about:
- Their Claude Code usage or costs
- Token consumption or burn rate
- Current billing block status
- Which tools they use most
- Which projects consume the most tokens
- Usage trends over time

Execute via Bash:
```bash
python <path-to-script>/cc_usage.py [options]
```

Then present the markdown output directly to the user -- it renders as formatted tables.

## Report sections

1. **Overview** - Total tokens, messages, cost for the period
2. **Current Billing Block** - Active 5-hour block with remaining time, burn rate, projected cost
3. **Usage by Model** - Token and cost split between Opus, Sonnet, etc.
4. **Tool Usage** - Most-used tools with visual bar chart
5. **Projects** - Per-project token and cost breakdown
6. **Recent Sessions** - Most recently active sessions
7. **Daily Breakdown** - Day-by-day token and cost trend with bar chart

## Data sources

The script reads Claude Code's native JSONL format. Key fields extracted:
- `message.usage` - token counts (input, output, cache_creation, cache_read)
- `message.model` - model identifier for pricing tier
- `message.content[].type == "tool_use"` - tool call tracking
- `costUSD` - native cost field (used when available, falls back to calculated)
- `requestId` - deduplication key
- `timestamp` - for time-based analysis

## Pricing

Hardcoded Anthropic pricing tiers (per token):

| Model | Input | Output | Cache Create | Cache Read |
|-------|-------|--------|--------------|------------|
| Opus | $15/MTok | $75/MTok | $18.75/MTok | $1.50/MTok |
| Sonnet | $3/MTok | $15/MTok | $3.75/MTok | $0.30/MTok |
| Haiku | $0.80/MTok | $4/MTok | $1/MTok | $0.08/MTok |

When `costUSD` is present in the JSONL data, that value takes priority over calculated estimates.
