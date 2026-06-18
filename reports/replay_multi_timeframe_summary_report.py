"""
reports/replay_multi_timeframe_summary_report.py — MultiTimeframeSummaryReport v1.2.5

Summary report for multi-timeframe replay.
Never claims strategy effectiveness.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] Never claims strategy effectiveness.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
NEVER_CLAIMS_EFFECTIVENESS = True


class MultiTimeframeSummaryReport:
    """
    Summary report for multi-timeframe replay.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] Never claims strategy effectiveness.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    NEVER_CLAIMS_EFFECTIVENESS = True

    def __init__(self, repo_root: Optional[str] = None) -> None:
        self._repo_root = repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._reports_dir = os.path.join(self._repo_root, "reports")
        os.makedirs(self._reports_dir, exist_ok=True)

    def build(self, summary: Optional[Dict[str, Any]] = None) -> str:
        """Build and save summary report. Returns report path."""
        summary = summary or {}
        content = self._build_content(summary)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"replay_multi_timeframe_summary_{ts}.md"
        path = os.path.join(self._reports_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def _build_content(self, summary: Dict[str, Any]) -> str:
        now = datetime.now(timezone.utc).isoformat()
        lines = [
            "# Multi-timeframe Replay Summary Report v1.2.5",
            "",
            "> Research Only | No Real Orders | Never Claims Strategy Effectiveness",
            "",
            f"**Generated**: {now}",
            "",
            "## Overview",
            "",
            f"- **Total Sessions**: {summary.get('total_sessions', 0)}",
            f"- **Total Snapshots**: {summary.get('total_snapshots', 0)}",
            f"- **Timeframe Availability**: {summary.get('timeframe_availability', {})}",
            f"- **Partial Bar Count**: {summary.get('partial_bar_count', 0)}",
            f"- **PIT Failures**: {summary.get('point_in_time_failures', 0)}",
            f"- **Data Gaps**: {summary.get('data_gaps', [])}",
            f"- **Real/Mock**: {summary.get('real_mock_separation', 'N/A')}",
            f"- **Confidence**: {summary.get('confidence', 'OBSERVATIONAL')}",
            f"- **Insufficient Count**: {summary.get('insufficient_count', 0)}",
            "",
            "## Limitations",
            "",
            "- This summary describes training observations only",
            "- Agreement/conflict distribution ≠ strategy effectiveness",
            "- Unavailable timeframe ≠ bearish signal",
            "- Partial bars not used for confirmed indicators",
            "- Batch total elapsed shown for timing reference only",
            "",
            "---",
            "*Never claims strategy effectiveness. Research Only. Not Investment Advice.*",
        ]
        return "\n".join(lines)
