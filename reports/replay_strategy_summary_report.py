"""
reports/replay_strategy_summary_report.py — Strategy replay summary report v1.2.4.
[!] Research Only. No Real Orders. NEVER claims strategy effectiveness. Not Investment Advice.
"""
from __future__ import annotations
import logging
import os
from datetime import datetime, timezone
from typing import Optional
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStrategySummaryReportBuilder:
    """
    Builds global summary reports.
    Output: reports/replay_strategy_summary_YYYY-MM-DD.md
    NEVER claims strategy effectiveness.
    """
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None):
        self.repo_root = repo_root or "."

    def build(self) -> str:
        """Build and save report. Returns output path."""
        try:
            from replay.strategy_replay_summary import StrategyReplaySummaryBuilder
            sb = StrategyReplaySummaryBuilder(repo_root=self.repo_root)
            summary = sb.global_summary()
        except Exception as exc:
            summary = {}
            logger.warning("Summary load error: %s", exc)

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        lines = [
            "# Strategy Replay Summary Report",
            f"**Date:** {today}",
            f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
            "",
            f"Sessions: {summary.get('total_sessions', 0)}",
            f"Snapshots: {summary.get('total_snapshots', 0)}",
            f"Rule Reviews: {summary.get('total_rule_reviews', 0)}",
            f"Suggested Reviews: {summary.get('suggested_reviews', 0)}",
            f"Confirmed Reviews: {summary.get('confirmed_reviews', 0)}",
            "",
            "NEVER claims strategy effectiveness.",
            "Research Only — Not Investment Advice — No Real Orders",
        ]
        content = "\n".join(lines)
        reports_dir = os.path.join(self.repo_root, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        path = os.path.join(reports_dir, f"replay_strategy_summary_{today}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
