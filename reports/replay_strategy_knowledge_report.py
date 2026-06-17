"""
reports/replay_strategy_knowledge_report.py — Strategy Knowledge Replay report v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
[!] NEVER claims strategy effectiveness.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStrategyKnowledgeReportBuilder:
    """
    Builds markdown reports for strategy knowledge replay sessions.
    Output: reports/replay_strategy_knowledge_report_<session_id>.md
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None):
        self.repo_root = repo_root or "."

    def build(self, session_id: str) -> str:
        """Build and save report. Returns output path."""
        try:
            from replay.strategy_replay_query import StrategyReplayQuery
            from replay.strategy_replay_summary import StrategyReplaySummaryBuilder
            q = StrategyReplayQuery(repo_root=self.repo_root)
            sb = StrategyReplaySummaryBuilder(repo_root=self.repo_root)
            snapshot = q.latest_snapshot(session_id)
            summary = sb.session_summary(session_id)
            agreements = q.agreements(session_id)
            conflicts = q.conflicts(session_id)
            reviews = q.rule_reviews(session_id)
        except Exception as exc:
            snapshot = None
            summary = {}
            agreements = []
            conflicts = []
            reviews = []
            logger.warning("Report data load error: %s", exc)

        lines = self._build_markdown(session_id, snapshot, summary, agreements, conflicts, reviews)
        content = "\n".join(lines)
        output_path = self._save(session_id, content)
        return output_path

    def _build_markdown(
        self, session_id, snapshot, summary, agreements, conflicts, reviews
    ):
        lines = [
            f"# Strategy Knowledge Replay Report",
            f"**Session ID:** {session_id}",
            f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
            "",
            "## Safety Declaration",
            "- Research Only. No Real Orders.",
            "- Strategy Knowledge Replay NEVER triggers paper orders or broker execution.",
            "- Point-in-time verified. No forward return. No outcome before explicit reveal.",
            "- Auto Strategy Decision: DISABLED",
            "- Auto Strategy Execution: DISABLED",
            "- Auto Strategy Weight Change: DISABLED",
            "- Not Investment Advice.",
            "",
            "## Session Overview",
            f"- Snapshots: {summary.get('snapshots_count', 0)}",
            f"- Sample Count: {summary.get('sample_count', 0)}",
            f"- Confidence: {summary.get('confidence', 'OBSERVATIONAL')}",
            "",
            "## Point-in-Time Verification",
        ]

        if snapshot:
            lines += [
                f"- Latest Snapshot ID: {snapshot.get('strategy_snapshot_id', '')}",
                f"- Replay Date: {snapshot.get('replay_date', '')}",
                f"- Point-in-Time Verified: {snapshot.get('point_in_time_verified', False)}",
                f"- Future Fields Blocked: {snapshot.get('future_fields_blocked', [])}",
                "",
            ]

        lines += [
            "## Current Strategy Snapshot",
        ]
        if snapshot:
            lines += [
                f"- Agreement Score: {snapshot.get('agreement_score', 0):.3f}",
                f"- Conflict Score: {snapshot.get('conflict_score', 0):.3f}",
                f"- Bullish Modules: {snapshot.get('bullish_modules', [])}",
                f"- Bearish Modules: {snapshot.get('bearish_modules', [])}",
                f"- Warning Modules: {snapshot.get('warning_modules', [])}",
                f"- Unavailable Modules: {snapshot.get('unavailable_modules', [])}",
            ]
        else:
            lines.append("- No snapshot available.")

        lines += ["", "## Review Mode Comparison"]
        lines.append("NOT_REVEALED — Outcome reveal not performed. No forward return shown.")

        lines += [
            "",
            "## Limitations",
            "- Module availability depends on data quality and completeness.",
            "- Timing of fundamental announcements may be approximate.",
            "- OBSERVATIONAL confidence only — not statistically validated.",
            "- NEVER claims strategy effectiveness.",
            "",
            "## Safety Declaration",
            "Research Only — Not Investment Advice — No Real Orders",
            "No broker execution. VALIDATED does not enable trading.",
        ]
        return lines

    def _save(self, session_id: str, content: str) -> str:
        reports_dir = os.path.join(self.repo_root, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        filename = f"replay_strategy_knowledge_report_{session_id}.md"
        path = os.path.join(reports_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
