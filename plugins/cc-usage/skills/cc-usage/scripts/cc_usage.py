#!/usr/bin/env python3
"""Claude Code usage analyzer - reads JSONL session data and outputs formatted usage report.

Inspired by paulrobello/par_cc_usage. Zero dependencies (stdlib only).
"""

from __future__ import annotations

import json
import os
import sys
import glob as glob_mod
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Model pricing (per token) - hardcoded for offline use
# Source: Anthropic pricing page, March 2026
# ---------------------------------------------------------------------------
MODEL_PRICING: dict[str, dict[str, float]] = {
    "opus": {
        "input": 15e-6, "output": 75e-6,
        "cache_create": 18.75e-6, "cache_read": 1.5e-6,
    },
    "sonnet": {
        "input": 3e-6, "output": 15e-6,
        "cache_create": 3.75e-6, "cache_read": 0.3e-6,
    },
    "haiku": {
        "input": 0.8e-6, "output": 4e-6,
        "cache_create": 1e-6, "cache_read": 0.08e-6,
    },
}

# Model name -> pricing tier mapping
MODEL_TIER: dict[str, str] = {}
for _tier, _keywords in [
    ("opus", ["opus"]),
    ("sonnet", ["sonnet"]),
    ("haiku", ["haiku"]),
]:
    for _kw in _keywords:
        MODEL_TIER[_kw] = _tier

BLOCK_DURATION_HOURS = 5

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_claude_dirs() -> list[Path]:
    """Find Claude Code project directories."""
    candidates = []
    config_dir = os.environ.get("CLAUDE_CONFIG_DIR")
    if config_dir:
        candidates.append(Path(config_dir) / "projects")

    home = Path.home()
    candidates.append(home / ".config" / "claude" / "projects")
    candidates.append(home / ".claude" / "projects")

    return [d for d in candidates if d.is_dir()]


def get_model_tier(model_name: str) -> str:
    """Map a model name to a pricing tier."""
    if not model_name:
        return "unknown"
    lower = model_name.lower()
    for keyword, tier in MODEL_TIER.items():
        if keyword in lower:
            return tier
    return "unknown"


def get_pricing(tier: str) -> dict[str, float]:
    """Get pricing for a model tier."""
    return MODEL_PRICING.get(tier, MODEL_PRICING["sonnet"])


def parse_timestamp(ts: str) -> datetime | None:
    """Parse ISO 8601 timestamp."""
    if not ts:
        return None
    try:
        # Handle Z suffix
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)
    except (ValueError, TypeError):
        return None


def format_tokens(n: int) -> str:
    """Format token count for display."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def format_cost(cost: float) -> str:
    """Format cost for display."""
    if cost == 0:
        return "$0.00"
    if cost < 0.01:
        return f"${cost:.4f}"
    if cost < 1:
        return f"${cost:.3f}"
    return f"${cost:.2f}"


def bar_chart(value: int, max_value: int, width: int = 20) -> str:
    """Create a simple text bar chart."""
    if max_value == 0:
        return " " * width
    filled = min(int((value / max_value) * width), width)
    return "#" * filled + "-" * (width - filled)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class TokenUsage:
    __slots__ = (
        "input_tokens", "output_tokens",
        "cache_create_tokens", "cache_read_tokens",
        "model", "timestamp", "cost_usd",
        "tools_used", "request_id",
    )

    def __init__(self) -> None:
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self.cache_create_tokens: int = 0
        self.cache_read_tokens: int = 0
        self.model: str = ""
        self.timestamp: datetime | None = None
        self.cost_usd: float | None = None
        self.tools_used: list[str] = []
        self.request_id: str | None = None

    @property
    def total_input(self) -> int:
        return self.input_tokens + self.cache_create_tokens + self.cache_read_tokens

    @property
    def total(self) -> int:
        return self.total_input + self.output_tokens

    def estimated_cost(self) -> float:
        """Calculate estimated cost from token counts and model pricing."""
        if self.cost_usd is not None:
            return self.cost_usd
        tier = get_model_tier(self.model)
        pricing = get_pricing(tier)
        return (
            self.input_tokens * pricing["input"]
            + self.output_tokens * pricing["output"]
            + self.cache_create_tokens * pricing["cache_create"]
            + self.cache_read_tokens * pricing["cache_read"]
        )


class SessionData:
    def __init__(self, session_id: str, project_name: str) -> None:
        self.session_id = session_id
        self.project_name = project_name
        self.usages: list[TokenUsage] = []
        self.first_ts: datetime | None = None
        self.last_ts: datetime | None = None

    def add_usage(self, u: TokenUsage) -> None:
        self.usages.append(u)
        if u.timestamp:
            if self.first_ts is None or u.timestamp < self.first_ts:
                self.first_ts = u.timestamp
            if self.last_ts is None or u.timestamp > self.last_ts:
                self.last_ts = u.timestamp

    @property
    def total_tokens(self) -> int:
        return sum(u.total for u in self.usages)

    @property
    def total_input(self) -> int:
        return sum(u.total_input for u in self.usages)

    @property
    def total_output(self) -> int:
        return sum(u.output_tokens for u in self.usages)

    @property
    def total_cost(self) -> float:
        return sum(u.estimated_cost() for u in self.usages)

    @property
    def message_count(self) -> int:
        return len(self.usages)


class BillingBlock:
    """A 5-hour billing window."""
    def __init__(self, start: datetime) -> None:
        # Floor to hour boundary
        self.start = start.replace(minute=0, second=0, microsecond=0)
        self.end = self.start + timedelta(hours=BLOCK_DURATION_HOURS)
        self.usages: list[TokenUsage] = []

    def contains(self, ts: datetime) -> bool:
        return self.start <= ts < self.end

    @property
    def total_tokens(self) -> int:
        return sum(u.total for u in self.usages)

    @property
    def total_cost(self) -> float:
        return sum(u.estimated_cost() for u in self.usages)

    def tokens_by_model(self) -> dict[str, int]:
        result: dict[str, int] = defaultdict(int)
        for u in self.usages:
            tier = get_model_tier(u.model)
            result[tier] += u.total
        return dict(result)

    def cost_by_model(self) -> dict[str, float]:
        result: dict[str, float] = defaultdict(float)
        for u in self.usages:
            tier = get_model_tier(u.model)
            result[tier] += u.estimated_cost()
        return dict(result)


# ---------------------------------------------------------------------------
# JSONL parser
# ---------------------------------------------------------------------------

def parse_jsonl_file(filepath: Path, project_name: str) -> SessionData | None:
    """Parse a single JSONL session file."""
    session_id = filepath.stem
    session = SessionData(session_id, project_name)
    seen_request_ids: set[str] = set()

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Only process assistant messages with usage data
                msg = data.get("message")
                if not isinstance(msg, dict):
                    continue
                if msg.get("role") != "assistant":
                    continue

                usage_data = msg.get("usage")
                if not isinstance(usage_data, dict):
                    continue

                # Dedup by request_id
                req_id = data.get("requestId")
                if req_id:
                    if req_id in seen_request_ids:
                        continue
                    seen_request_ids.add(req_id)

                u = TokenUsage()
                u.input_tokens = usage_data.get("input_tokens", 0) or 0
                u.output_tokens = usage_data.get("output_tokens", 0) or 0
                u.cache_create_tokens = usage_data.get("cache_creation_input_tokens", 0) or 0
                u.cache_read_tokens = usage_data.get("cache_read_input_tokens", 0) or 0
                u.model = msg.get("model", "")
                u.timestamp = parse_timestamp(data.get("timestamp", ""))
                u.cost_usd = data.get("costUSD")
                u.request_id = req_id

                # Extract tool usage from content
                content = msg.get("content")
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "tool_use":
                            name = block.get("name", "")
                            if name:
                                u.tools_used.append(name)

                session.add_usage(u)
    except (OSError, PermissionError):
        return None

    if not session.usages:
        return None
    return session


# ---------------------------------------------------------------------------
# Data collection
# ---------------------------------------------------------------------------

def collect_all_sessions(
    days: int = 7,
    project_filter: str | None = None,
) -> list[SessionData]:
    """Collect all session data from Claude Code directories."""
    claude_dirs = find_claude_dirs()
    if not claude_dirs:
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    sessions: list[SessionData] = []

    for projects_dir in claude_dirs:
        if not projects_dir.is_dir():
            continue
        for project_dir in projects_dir.iterdir():
            if not project_dir.is_dir():
                continue
            project_name = project_dir.name

            if project_filter and project_filter.lower() not in project_name.lower():
                continue

            for jsonl_file in project_dir.glob("*.jsonl"):
                # Quick check: skip files older than cutoff by mtime
                try:
                    mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime, tz=timezone.utc)
                    if mtime < cutoff:
                        continue
                except OSError:
                    continue

                session = parse_jsonl_file(jsonl_file, project_name)
                if session and session.last_ts and session.last_ts >= cutoff:
                    sessions.append(session)

    return sessions


def find_current_block(sessions: list[SessionData]) -> BillingBlock | None:
    """Find the current active billing block."""
    now = datetime.now(timezone.utc)
    all_usages: list[TokenUsage] = []
    for s in sessions:
        all_usages.extend(s.usages)

    if not all_usages:
        return None

    # Sort by timestamp
    timed = [u for u in all_usages if u.timestamp]
    timed.sort(key=lambda u: u.timestamp)  # type: ignore

    # Build blocks
    blocks: list[BillingBlock] = []
    current_block: BillingBlock | None = None

    for u in timed:
        ts = u.timestamp
        assert ts is not None

        if current_block is None or not current_block.contains(ts):
            # Check for gap (>5h since last activity)
            if current_block and current_block.usages:
                last_in_block = max(x.timestamp for x in current_block.usages if x.timestamp)
                if ts - last_in_block > timedelta(hours=BLOCK_DURATION_HOURS):  # type: ignore
                    current_block = BillingBlock(ts)
                    blocks.append(current_block)
                elif not current_block.contains(ts):
                    current_block = BillingBlock(ts)
                    blocks.append(current_block)
            else:
                current_block = BillingBlock(ts)
                blocks.append(current_block)

        current_block.usages.append(u)

    # Find block containing now, or most recent
    for block in reversed(blocks):
        if block.contains(now):
            return block

    # Return most recent if none contains now
    return blocks[-1] if blocks else None


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    sessions: list[SessionData],
    days: int = 7,
    show_block: bool = True,
    show_projects: bool = True,
    show_tools: bool = True,
    show_sessions: bool = True,
    top_n: int = 10,
) -> str:
    """Generate a formatted usage report."""
    lines: list[str] = []
    now = datetime.now(timezone.utc)

    if not sessions:
        lines.append("No Claude Code usage data found.")
        lines.append("")
        lines.append("Looked in:")
        for d in find_claude_dirs():
            lines.append(f"  - {d}")
        if not find_claude_dirs():
            lines.append("  (no Claude Code directories found)")
        return "\n".join(lines)

    # Aggregate stats
    total_tokens = sum(s.total_tokens for s in sessions)
    total_input = sum(s.total_input for s in sessions)
    total_output = sum(s.total_output for s in sessions)
    total_cost = sum(s.total_cost for s in sessions)
    total_messages = sum(s.message_count for s in sessions)

    # Model breakdown
    model_tokens: dict[str, int] = defaultdict(int)
    model_cost: dict[str, float] = defaultdict(float)
    model_messages: dict[str, int] = defaultdict(int)
    tool_counts: dict[str, int] = defaultdict(int)

    for s in sessions:
        for u in s.usages:
            tier = get_model_tier(u.model)
            model_tokens[tier] += u.total
            model_cost[tier] += u.estimated_cost()
            model_messages[tier] += 1
            for tool in u.tools_used:
                tool_counts[tool] += 1

    # --- Header ---
    lines.append(f"## Claude Code Usage Report ({days}d)")
    lines.append("")

    # --- Overview ---
    lines.append("### Overview")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Period | Last {days} days |")
    lines.append(f"| Sessions | {len(sessions)} |")
    lines.append(f"| Messages | {total_messages:,} |")
    lines.append(f"| Total tokens | {format_tokens(total_tokens)} |")
    lines.append(f"| Input tokens | {format_tokens(total_input)} |")
    lines.append(f"| Output tokens | {format_tokens(total_output)} |")
    lines.append(f"| Estimated cost | {format_cost(total_cost)} |")
    lines.append("")

    # --- Current billing block ---
    if show_block:
        block = find_current_block(sessions)
        if block:
            remaining = block.end - now
            remaining_min = max(0, int(remaining.total_seconds() / 60))
            remaining_h = remaining_min // 60
            remaining_m = remaining_min % 60

            lines.append("### Current Billing Block")
            lines.append("")
            lines.append(f"| Metric | Value |")
            lines.append(f"|--------|-------|")
            lines.append(f"| Block start | {block.start.strftime('%Y-%m-%d %H:%M UTC')} |")
            lines.append(f"| Block end | {block.end.strftime('%Y-%m-%d %H:%M UTC')} |")
            if block.contains(now):
                lines.append(f"| Remaining | {remaining_h}h {remaining_m}m |")
            else:
                lines.append(f"| Status | Expired |")
            lines.append(f"| Block tokens | {format_tokens(block.total_tokens)} |")
            lines.append(f"| Block cost | {format_cost(block.total_cost)} |")
            lines.append(f"| Messages | {len(block.usages)} |")
            lines.append("")

            # Per-model in block
            btm = block.tokens_by_model()
            bcm = block.cost_by_model()
            if btm:
                lines.append("**Block by model:**")
                lines.append("")
                lines.append("| Model | Tokens | Cost |")
                lines.append("|-------|--------|------|")
                for tier in sorted(btm, key=btm.get, reverse=True):  # type: ignore
                    lines.append(f"| {tier} | {format_tokens(btm[tier])} | {format_cost(bcm.get(tier, 0))} |")
                lines.append("")

            # Burn rate
            if block.contains(now):
                elapsed = (now - block.start).total_seconds()
                if elapsed > 0:
                    tokens_per_min = block.total_tokens / (elapsed / 60)
                    cost_per_hour = (block.total_cost / elapsed) * 3600
                    lines.append("**Burn rate:**")
                    lines.append("")
                    lines.append(f"| Metric | Value |")
                    lines.append(f"|--------|-------|")
                    lines.append(f"| Tokens/min | {tokens_per_min:.0f} |")
                    lines.append(f"| Cost/hour | {format_cost(cost_per_hour)} |")
                    if remaining_min > 0:
                        projected = block.total_cost + cost_per_hour * (remaining_min / 60)
                        lines.append(f"| Projected block total | {format_cost(projected)} |")
                    lines.append("")

    # --- Model breakdown ---
    lines.append("### Usage by Model")
    lines.append("")
    lines.append("| Model | Tokens | Messages | Cost | Share |")
    lines.append("|-------|--------|----------|------|-------|")
    for tier in sorted(model_tokens, key=model_tokens.get, reverse=True):  # type: ignore
        share = (model_tokens[tier] / total_tokens * 100) if total_tokens > 0 else 0
        lines.append(
            f"| {tier} | {format_tokens(model_tokens[tier])} | "
            f"{model_messages[tier]:,} | {format_cost(model_cost[tier])} | "
            f"{share:.0f}% |"
        )
    lines.append("")

    # --- Tool usage ---
    if show_tools and tool_counts:
        lines.append("### Tool Usage")
        lines.append("")
        sorted_tools = sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)
        max_tool_count = sorted_tools[0][1] if sorted_tools else 1
        lines.append("| Tool | Calls | |")
        lines.append("|------|-------|-|")
        for tool, count in sorted_tools[:top_n]:
            lines.append(f"| {tool} | {count:,} | {bar_chart(count, max_tool_count, 15)} |")
        if len(sorted_tools) > top_n:
            others = sum(c for _, c in sorted_tools[top_n:])
            lines.append(f"| *({len(sorted_tools) - top_n} more)* | {others:,} | |")
        lines.append("")

    # --- Project breakdown ---
    if show_projects:
        project_data: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"tokens": 0, "cost": 0.0, "messages": 0, "sessions": 0}
        )
        for s in sessions:
            pd = project_data[s.project_name]
            pd["tokens"] += s.total_tokens
            pd["cost"] += s.total_cost
            pd["messages"] += s.message_count
            pd["sessions"] += 1

        sorted_projects = sorted(project_data.items(), key=lambda x: x[1]["tokens"], reverse=True)

        lines.append("### Projects")
        lines.append("")
        lines.append("| Project | Tokens | Messages | Sessions | Cost |")
        lines.append("|---------|--------|----------|----------|------|")
        for name, pd in sorted_projects[:top_n]:
            # Shorten long project names
            display_name = name
            if len(display_name) > 40:
                display_name = "..." + display_name[-37:]
            lines.append(
                f"| {display_name} | {format_tokens(pd['tokens'])} | "
                f"{pd['messages']:,} | {pd['sessions']} | {format_cost(pd['cost'])} |"
            )
        if len(sorted_projects) > top_n:
            lines.append(f"| *({len(sorted_projects) - top_n} more projects)* | | | | |")
        lines.append("")

    # --- Recent sessions ---
    if show_sessions:
        recent = sorted(
            [s for s in sessions if s.last_ts],
            key=lambda s: s.last_ts,  # type: ignore
            reverse=True,
        )[:top_n]

        if recent:
            lines.append("### Recent Sessions")
            lines.append("")
            lines.append("| Project | Last Active | Messages | Tokens | Cost |")
            lines.append("|---------|-------------|----------|--------|------|")
            for s in recent:
                project_short = s.project_name
                if len(project_short) > 30:
                    project_short = "..." + project_short[-27:]
                last = s.last_ts.strftime("%m-%d %H:%M") if s.last_ts else "?"  # type: ignore
                lines.append(
                    f"| {project_short} | {last} | "
                    f"{s.message_count} | {format_tokens(s.total_tokens)} | "
                    f"{format_cost(s.total_cost)} |"
                )
            lines.append("")

    # --- Daily breakdown (last 7 days) ---
    daily_tokens: dict[str, int] = defaultdict(int)
    daily_cost: dict[str, float] = defaultdict(float)
    daily_messages: dict[str, int] = defaultdict(int)

    for s in sessions:
        for u in s.usages:
            if u.timestamp:
                day = u.timestamp.strftime("%Y-%m-%d")
                daily_tokens[day] += u.total
                daily_cost[day] += u.estimated_cost()
                daily_messages[day] += 1

    if daily_tokens:
        lines.append("### Daily Breakdown")
        lines.append("")
        sorted_days = sorted(daily_tokens.keys(), reverse=True)[:days]
        max_daily = max(daily_tokens.values()) if daily_tokens else 1

        lines.append("| Date | Tokens | Messages | Cost | |")
        lines.append("|------|--------|----------|------|-|")
        for day in sorted_days:
            lines.append(
                f"| {day} | {format_tokens(daily_tokens[day])} | "
                f"{daily_messages[day]:,} | {format_cost(daily_cost[day])} | "
                f"{bar_chart(daily_tokens[day], max_daily, 15)} |"
            )
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Claude Code usage analyzer")
    parser.add_argument("-d", "--days", type=int, default=7, help="Number of days to analyze (default: 7)")
    parser.add_argument("-p", "--project", type=str, default=None, help="Filter by project name (substring match)")
    parser.add_argument("--no-block", action="store_true", help="Hide billing block info")
    parser.add_argument("--no-projects", action="store_true", help="Hide project breakdown")
    parser.add_argument("--no-tools", action="store_true", help="Hide tool usage")
    parser.add_argument("--no-sessions", action="store_true", help="Hide recent sessions")
    parser.add_argument("-n", "--top", type=int, default=10, help="Number of top items to show (default: 10)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON data")

    args = parser.parse_args()

    sessions = collect_all_sessions(days=args.days, project_filter=args.project)

    if args.json:
        # JSON output mode
        data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "days": args.days,
            "sessions_count": len(sessions),
            "total_tokens": sum(s.total_tokens for s in sessions),
            "total_cost": sum(s.total_cost for s in sessions),
            "total_messages": sum(s.message_count for s in sessions),
            "projects": {},
        }
        for s in sessions:
            if s.project_name not in data["projects"]:
                data["projects"][s.project_name] = {
                    "tokens": 0, "cost": 0.0, "messages": 0, "sessions": 0
                }
            pd = data["projects"][s.project_name]
            pd["tokens"] += s.total_tokens
            pd["cost"] += s.total_cost
            pd["messages"] += s.message_count
            pd["sessions"] += 1
        print(json.dumps(data, indent=2))
    else:
        report = generate_report(
            sessions,
            days=args.days,
            show_block=not args.no_block,
            show_projects=not args.no_projects,
            show_tools=not args.no_tools,
            show_sessions=not args.no_sessions,
            top_n=args.top,
        )
        print(report)


if __name__ == "__main__":
    # Ensure UTF-8 output on Windows
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore
    main()
