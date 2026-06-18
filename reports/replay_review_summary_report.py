"""
reports/replay_review_summary_report.py — Replay Review Summary Report v1.2.6

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def build_replay_review_summary_report(
    summary: Optional[Dict[str, Any]] = None,
    mode: str = "real",
) -> str:
    """Build global summary report markdown."""
    data = summary or {}
    now  = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"# Replay Review Summary Report",
        f"**Generated:** {now}  ",
        f"**Version:** 1.2.6  ",
        f"**Mode:** {mode}  ",
        f"**Research Only:** True  ",
        "",
        "## Safety Declaration",
        "> [!] Research Only. No Real Orders. Not Investment Advice.",
        "",
        "## Session Counts",
        f"- Total Sessions: {data.get('total_sessions', 0)}",
        f"- Real Sessions: {data.get('real_sessions', 0)}",
        f"- Mock Sessions: {data.get('mock_sessions', 0)}",
        f"- Review Complete: {data.get('review_complete', 0)}",
        f"- Review Incomplete: {data.get('review_incomplete', 0)}",
        "",
        "## Review Completion",
        f"- Sufficient: {data.get('review_complete', 0)}",
        f"- Insufficient: {data.get('insufficient', 0)}",
        "",
        "## Scores (Process Only)",
        f"- Avg Process Score: {data.get('avg_process_score', 'N/A')}",
        "- Avg Outcome Score: HIDDEN (aggregate not revealed)",
        "> [!] Process and outcome are strictly separated.",
        "",
        "## Mistakes",
        f"- Suggested: {data.get('suggested_mistakes', 0)}",
        f"- Confirmed: {data.get('confirmed_mistakes', 0)}",
        "",
        "## Conflicts",
        f"- Strategy Conflicts: {data.get('strategy_conflicts', 0)}",
        f"- Timeframe Conflicts: {data.get('timeframe_conflicts', 0)}",
        "",
        "## Confidence",
        f"- Low Confidence: {data.get('low_confidence', 0)}",
        f"- Insufficient: {data.get('insufficient', 0)}",
        "",
        "---",
        "> [!] Research Only. No Real Orders. Not Investment Advice.",
    ]
    return "\n".join(lines)
