"""
reports/replay_review_queue_report.py — Replay Review Queue Report v1.2.6

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def build_replay_review_queue_report(
    queue_summary: Optional[Dict[str, Any]] = None,
    queue_items: Optional[List[Dict[str, Any]]] = None,
    mode: str = "real",
) -> str:
    """Build queue report markdown."""
    data  = queue_summary or {}
    items = queue_items or []
    now   = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    open_items = [i for i in items if i.get("status") == "OPEN"]
    p0_items   = [i for i in open_items if i.get("priority") == "P0"]
    p1_items   = [i for i in open_items if i.get("priority") == "P1"]

    lines = [
        f"# Replay Review Queue Report",
        f"**Generated:** {now}  ",
        f"**Version:** 1.2.6  ",
        f"**Mode:** {mode}  ",
        f"**Research Only:** True  ",
        "",
        "## Safety Declaration",
        "> [!] Research Only. No Real Orders. Not Investment Advice.",
        "> [!] complete() does NOT auto-confirm mistakes or auto-reveal outcomes.",
        "",
        "## Queue Summary",
        f"- Total Items: {data.get('total', len(items))}",
        f"- Open: {data.get('open_count', len(open_items))}",
        f"- In Review: {data.get('in_review', 0)}",
        f"- Completed: {data.get('completed', 0)}",
        f"- Blocked: {data.get('blocked', 0)}",
        f"- Dismissed: {data.get('dismissed', 0)}",
        "",
        "## P0 Items (Critical)",
    ]
    if p0_items:
        for item in p0_items[:10]:
            lines.append(f"- [{item.get('queue_type','?')}] {item.get('session_id','?')}: {item.get('title','')}")
    else:
        lines.append("- None")

    lines += [
        "",
        "## P1 Items (High Priority)",
    ]
    if p1_items:
        for item in p1_items[:10]:
            lines.append(f"- [{item.get('queue_type','?')}] {item.get('session_id','?')}: {item.get('title','')}")
    else:
        lines.append("- None")

    lines += [
        "",
        "---",
        "> [!] Research Only. No Real Orders. Not Investment Advice.",
    ]
    return "\n".join(lines)
