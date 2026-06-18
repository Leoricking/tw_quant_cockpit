"""
replay/review_report.py — ReplayReviewReportBuilder v1.2.6

Outputs:
  reports/replay_review_dashboard_{session_id}.md
  reports/replay_review_summary_YYYY-MM-DD.md
  reports/replay_review_queue_YYYY-MM-DD.md

[!] Research Only. No Real Orders. Outcome hidden until revealed.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


class ReplayReviewReportBuilder:
    """
    Builds markdown reports for replay review dashboard, summary, and queue.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, reports_dir: Optional[str] = None) -> None:
        if reports_dir:
            self._reports_dir = Path(reports_dir)
        else:
            repo_root = Path(__file__).parent.parent
            self._reports_dir = repo_root / "reports"
        self._reports_dir.mkdir(parents=True, exist_ok=True)

    def build_session_report(
        self,
        session_id: str,
        session_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build session review report. Returns markdown string."""
        data = session_data or {}
        now = _now_date()
        lines = [
            f"# Replay Review Dashboard — Session {session_id}",
            f"**Date:** {now}  ",
            f"**Version:** 1.2.6  ",
            f"**Research Only:** True  ",
            f"**No Real Orders:** True  ",
            "",
            "## Safety Declaration",
            "> [!] Research Only. No Real Orders. No Auto Review Complete.",
            "> [!] No Auto Outcome Reveal. No Auto Confirm. No Score-to-Trade.",
            "> [!] Not Investment Advice.",
            "",
            "## Session Overview",
            f"- Session ID: {session_id}",
            f"- Symbol: {data.get('symbol', 'N/A')}",
            f"- Status: {data.get('status', 'UNKNOWN')}",
            f"- Mode: {data.get('mode', 'real')}",
            "",
            "## Review Progress",
            f"- Review Progress: {data.get('review_progress', 'NOT_STARTED')}",
            f"- Review Complete: {data.get('review_complete', False)}",
            "",
            "## Process Score",
            f"- Process Score: {data.get('process_score', 'N/A')}",
            "> [!] Process score uses NO future data, NO outcome, NO PnL.",
            "",
            "## Outcome Score",
            "- Outcome Score: NOT_REVEALED" if not data.get("outcome_revealed") else
            f"- Outcome Score: {data.get('outcome_score', 'N/A')}",
            "> [!] Outcome hidden until explicit reveal.",
            "",
            "## Mistakes",
            f"- Suggested Mistakes: {data.get('mistake_count', 0)}",
            f"- Confirmed Mistakes: {data.get('confirmed_mistake_count', 0)}",
            "> [!] Suggested only. System cannot auto-confirm.",
            "",
            "## Strategy Conflicts",
            f"- Strategy Conflicts: {data.get('strategy_conflicts', 0)}",
            "> [!] Training Only. No Auto-Trade. No Auto-Block.",
            "",
            "## Multi-Timeframe",
            f"- MTF Conflicts: {data.get('mtf_conflicts', 0)}",
            "",
            "## PIT Integrity",
            f"- Point-in-Time Verified: {data.get('pit_verified', False)}",
            "",
            "## Limitations",
            "- This report reflects replay training data only.",
            "- No real orders, no broker execution, no live trading.",
            "- Not Investment Advice.",
            "",
        ]
        return "\n".join(lines)

    def write_session_report(
        self,
        session_id: str,
        session_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Write session report to disk. Returns file path."""
        content = self.build_session_report(session_id, session_data)
        path = self._reports_dir / f"replay_review_dashboard_{session_id}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("Session report written: %s", path)
        return str(path)

    def build_summary_report(
        self, summary: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build global summary report."""
        data = summary or {}
        now  = _now_date()
        lines = [
            f"# Replay Review Summary — {now}",
            f"**Version:** 1.2.6  ",
            f"**Research Only:** True  ",
            "",
            "## Safety Declaration",
            "> [!] Research Only. No Real Orders. Not Investment Advice.",
            "",
            "## Session Counts",
            f"- Total: {data.get('total_sessions', 0)}",
            f"- Real: {data.get('real_sessions', 0)}",
            f"- Mock: {data.get('mock_sessions', 0)}",
            f"- Review Complete: {data.get('review_complete', 0)}",
            f"- Review Incomplete: {data.get('review_incomplete', 0)}",
            "",
            "## Scores",
            f"- Avg Process Score: {data.get('avg_process_score', 'N/A')}",
            "- Avg Outcome Score: HIDDEN",
            "",
            "## Mistakes",
            f"- Suggested: {data.get('suggested_mistakes', 0)}",
            f"- Confirmed: {data.get('confirmed_mistakes', 0)}",
            "",
            "## Conflicts",
            f"- Strategy Conflicts: {data.get('strategy_conflicts', 0)}",
            f"- Timeframe Conflicts: {data.get('timeframe_conflicts', 0)}",
            "",
        ]
        return "\n".join(lines)

    def write_summary_report(self, summary: Optional[Dict[str, Any]] = None) -> str:
        """Write summary report to disk."""
        content = self.build_summary_report(summary)
        now = _now_date()
        path = self._reports_dir / f"replay_review_summary_{now}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return str(path)

    def build_queue_report(self, queue: Optional[List[Dict[str, Any]]] = None) -> str:
        """Build review queue report."""
        items = queue or []
        now   = _now_date()
        open_items = [i for i in items if i.get("status") == "OPEN"]
        lines = [
            f"# Replay Review Queue — {now}",
            f"**Version:** 1.2.6  ",
            f"**Research Only:** True  ",
            "",
            "## Safety Declaration",
            "> [!] Research Only. No Real Orders. Not Investment Advice.",
            "",
            f"## Queue Status",
            f"- Total Items: {len(items)}",
            f"- Open: {len(open_items)}",
            "",
            "## Open Items",
        ]
        for item in open_items[:20]:
            lines.append(
                f"- [{item.get('priority','?')}] {item.get('session_id','?')} "
                f"— {item.get('queue_type','?')} — {item.get('title','')}"
            )
        return "\n".join(lines)

    def write_queue_report(self, queue: Optional[List[Dict[str, Any]]] = None) -> str:
        """Write queue report to disk."""
        content = self.build_queue_report(queue)
        now = _now_date()
        path = self._reports_dir / f"replay_review_queue_{now}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return str(path)
