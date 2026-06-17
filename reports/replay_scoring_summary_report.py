"""
reports/replay_scoring_summary_report.py — Scoring summary report for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayScoringSummaryReport:
    """
    Builds summary report across all scored sessions.
    [!] Research Only. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None):
        self._repo_root = repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._reports_dir = os.path.join(self._repo_root, "reports")
        os.makedirs(self._reports_dir, exist_ok=True)

    def build(self, summary: Optional[Dict[str, Any]] = None) -> str:
        if summary is None:
            from replay.scoring_summary import ReplayScoringSummaryBuilder
            builder = ReplayScoringSummaryBuilder(repo_root=self._repo_root)
            summary = builder.overall_summary()

        lines = [
            "# Replay Scoring Summary Report v1.2.3",
            "",
            "> [!] Research Only. No Real Orders. Simulation Training Only.",
            "> [!] This report is for training feedback only. Not Investment Advice.",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "## Overall Statistics",
            f"- Total Process Scores: {summary.get('total_process_scores', 0)}",
            f"- Total Composite Scores: {summary.get('total_composite_scores', 0)}",
            f"- Total Reveals: {summary.get('total_reveals', 0)}",
            f"- Confirmed Reveals: {summary.get('confirmed_reveals', 0)}",
            f"- Total Mistakes: {summary.get('total_mistakes', 0)}",
            f"- Avg Process Score: {summary.get('avg_process_score', 0.0):.1f} / 100",
            f"- Confidence: {summary.get('confidence_note', 'N/A')}",
            "",
        ]

        clf = summary.get("classification_breakdown", {})
        if clf:
            lines.append("## Classification Breakdown")
            for k, v in sorted(clf.items()):
                lines.append(f"- {k}: {v}")
            lines.append("")

        mt = summary.get("mistake_type_breakdown", {})
        if mt:
            lines.append("## Top Mistake Types")
            sorted_mt = sorted(mt.items(), key=lambda x: x[1], reverse=True)
            for k, v in sorted_mt[:10]:
                lines.append(f"- {k}: {v}")
            lines.append("")

        lines += [
            "---",
            "*[!] Research Only | No Real Orders | Not Investment Advice*",
        ]
        return "\n".join(lines)

    def save(self, summary: Optional[Dict[str, Any]] = None) -> str:
        content = self.build(summary)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self._reports_dir, f"replay_scoring_summary_report_{ts}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
