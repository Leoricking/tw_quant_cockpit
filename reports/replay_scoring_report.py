"""
reports/replay_scoring_report.py — ReplayScoringReportBuilder for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Reports are for research training purposes only. Not Investment Advice.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayScoringReportBuilder:
    """
    Builds scoring reports for replay sessions.
    [!] Research Only. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None):
        self._repo_root = repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._reports_dir = os.path.join(self._repo_root, "reports")
        os.makedirs(self._reports_dir, exist_ok=True)

    def build_session_report(
        self,
        session_id: str,
        process_score: Optional[Dict[str, Any]] = None,
        composite_score: Optional[Dict[str, Any]] = None,
        mistakes: Optional[List[Dict[str, Any]]] = None,
        reveal_record: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build a markdown report for a session's scoring."""
        lines = [
            f"# Replay Scoring Report — {session_id}",
            f"",
            f"> [!] Research Only. No Real Orders. Simulation Training Only.",
            f"> [!] This report is for training feedback only. Not Investment Advice.",
            f"",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            f"",
        ]

        if process_score:
            total = process_score.get("total_score", 0.0)
            status = process_score.get("status", "?")
            confidence = process_score.get("confidence_level", "?")
            lines += [
                f"## Process Score",
                f"- Total: **{total:.1f} / 100**",
                f"- Status: {status}",
                f"- Confidence: {confidence}",
                f"",
            ]
            components = process_score.get("components", [])
            if components:
                lines.append("### Dimension Breakdown")
                lines.append("| Dimension | Raw | Weight | Weighted |")
                lines.append("|-----------|-----|--------|----------|")
                for comp in components:
                    lines.append(
                        f"| {comp.get('dimension', '?')} "
                        f"| {comp.get('raw_score', 0):.2f} "
                        f"| {comp.get('weight', 0)} "
                        f"| {comp.get('weighted_score', 0):.1f} |"
                    )
                lines.append("")

        if reveal_record:
            reveal_status = reveal_record.get("status", "BLOCKED")
            lines += [
                f"## Outcome Reveal",
                f"- Status: {reveal_status}",
                f"- Window: {reveal_record.get('reveal_window_bars', 0)} bars",
                f"",
            ]

        if composite_score:
            clf = composite_score.get("classification", "?")
            lines += [
                f"## Composite Score",
                f"- Classification: **{clf}**",
                f"- Score: {composite_score.get('composite_score', 'N/A')}",
                f"- Status: {composite_score.get('status', '?')}",
                f"",
            ]

        if mistakes:
            lines += [
                f"## Mistakes ({len(mistakes)} detected)",
            ]
            for m in mistakes:
                lines.append(
                    f"- **{m.get('mistake_type', '?')}** "
                    f"[{m.get('status', '?')}] — {m.get('description', '')[:80]}"
                )
            lines.append("")

        lines += [
            f"---",
            f"*[!] Research Only | No Real Orders | Simulation Training | Not Investment Advice*",
        ]

        return "\n".join(lines)

    def save_session_report(self, session_id: str, content: str) -> str:
        """Save session report to file."""
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        safe_id = session_id.replace("/", "_").replace("\\", "_")
        filename = f"replay_scoring_report_{safe_id}_{ts}.md"
        path = os.path.join(self._reports_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
