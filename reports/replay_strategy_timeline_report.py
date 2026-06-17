"""
reports/replay_strategy_timeline_report.py — Signal timeline report v1.2.4.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
import os
from datetime import datetime, timezone
from typing import Optional
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStrategyTimelineReportBuilder:
    """
    Builds signal timeline reports.
    Output: reports/replay_strategy_timeline_<session_id>.md
    """
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None):
        self.repo_root = repo_root or "."

    def build(self, session_id: str) -> str:
        """Build and save report. Returns output path."""
        try:
            from replay.strategy_replay_query import StrategyReplayQuery
            q = StrategyReplayQuery(repo_root=self.repo_root)
            timeline = q.signal_timeline(session_id)
        except Exception as exc:
            timeline = []
            logger.warning("Timeline load error: %s", exc)

        lines = [
            "# Strategy Signal Timeline Report",
            f"**Session ID:** {session_id}",
            f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
            "",
            f"Timeline Records: {len(timeline)}",
            "",
            "Research Only — Not Investment Advice — No Real Orders",
        ]
        content = "\n".join(lines)
        reports_dir = os.path.join(self.repo_root, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        path = os.path.join(reports_dir, f"replay_strategy_timeline_{session_id}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
