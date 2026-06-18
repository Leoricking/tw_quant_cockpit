"""
reports/replay_multi_timeframe_timeline_report.py — MultiTimeframeTimelineReport v1.2.5

Timeline report for multi-timeframe replay sessions.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class MultiTimeframeTimelineReport:
    """
    Timeline report for multi-timeframe replay.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None) -> None:
        self._repo_root = repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._reports_dir = os.path.join(self._repo_root, "reports")
        os.makedirs(self._reports_dir, exist_ok=True)

    def build(
        self,
        session_id: str,
        events: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """Build and save timeline report. Returns report path."""
        content = self._build_content(session_id, events or [])
        filename = f"replay_multi_timeframe_timeline_{session_id}.md"
        path = os.path.join(self._reports_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def _build_content(self, session_id: str, events: List[Dict[str, Any]]) -> str:
        now = datetime.now(timezone.utc).isoformat()
        lines = [
            "# Multi-timeframe Replay Timeline Report v1.2.5",
            "",
            "> Research Only | No Real Orders | No Future Outcomes",
            "",
            f"**Session ID**: {session_id}",
            f"**Generated**: {now}",
            f"**Event Count**: {len(events)}",
            "",
            "## Timeline Events",
            "",
            "| Timestamp | Type | Timeframe | Description |",
            "|-----------|------|-----------|-------------|",
        ]
        for ev in events[:100]:  # limit for readability
            ts  = ev.get("event_timestamp", "")
            typ = ev.get("event_type", "")
            tf  = ev.get("timeframe") or "—"
            desc = ev.get("description", "")[:60]
            lines.append(f"| {ts} | {typ} | {tf} | {desc} |")

        lines += [
            "",
            "---",
            "*Research Only. No Future Outcomes. Not Investment Advice.*",
        ]
        return "\n".join(lines)
