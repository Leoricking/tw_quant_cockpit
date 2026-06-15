"""
reports/replay_training_session_report.py — ReplayTrainingSessionReportBuilder v1.2.0

Builds session report as markdown.
Output: reports/replay_training_session_report_{session_id}.md
v1.2.0: does NOT include future performance data.

[!] Research Only. No Real Orders. Replay Training Only.
[!] No Future Performance Evaluation.
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


class ReplayTrainingSessionReportBuilder:
    """
    Builds session report as markdown.
    Output: reports/replay_training_session_report_{session_id}.md
    v1.2.0: does NOT include future performance data.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root=None):
        self.repo_root = Path(repo_root) if repo_root else Path(".")
        self.reports_dir = self.repo_root / "reports"

    def build(self, session_id: Optional[str] = None, summary: Optional[Dict[str, Any]] = None) -> str:
        """Build markdown report. Returns markdown string."""
        if summary is None and session_id:
            summary = self._load_summary(session_id)
        if summary is None:
            summary = {"session_id": session_id or "unknown"}

        lines = []
        lines.append(f"# Replay Training Session Report — v1.2.0")
        lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
        lines.append("")
        lines.append("> [!] Research Only | No Real Orders | Replay Training Only | Not Investment Advice")
        lines.append("> [!] v1.2.0: No Future Performance Evaluation included in this report.")
        lines.append("")

        # 1. Session Overview
        lines.append("## 1. Session Overview")
        meta = summary.get("metadata", {})
        state = summary.get("state", {})
        lines.append(f"| Field | Value |")
        lines.append(f"|-------|-------|")
        lines.append(f"| Session ID | `{summary.get('session_id', '')}` |")
        lines.append(f"| Session Name | {meta.get('session_name', '')} |")
        lines.append(f"| Symbol | {meta.get('symbol', '')} |")
        lines.append(f"| Mode | {meta.get('mode', '')} |")
        lines.append(f"| Start Date | {meta.get('start_date', '')} |")
        lines.append(f"| End Date | {meta.get('end_date', '')} |")
        lines.append(f"| Current Date | {meta.get('current_date', '')} |")
        progress = summary.get("timeline_progress", {})
        lines.append(f"| Progress | {progress.get('current_index', 0)}/{progress.get('total_steps', 0)} ({progress.get('progress_pct', 0)}%) |")
        lines.append(f"| Status | {meta.get('status', '')} |")
        lines.append(f"| Qualification | {summary.get('qualification', 'UNKNOWN')} |")
        lines.append("")

        # 2. Point-in-Time Verification
        lines.append("## 2. Point-in-Time Verification")
        da = summary.get("data_availability", {})
        lines.append(f"| Check | Value |")
        lines.append(f"|-------|-------|")
        lines.append(f"| Qualification | {da.get('qualification', 'UNKNOWN')} |")
        lines.append(f"| Available Records | {da.get('available_records', 0)} |")
        lines.append(f"| Visible From | {da.get('visible_from', '')} |")
        lines.append(f"| Visible To | {da.get('visible_to', '')} |")
        lines.append("")

        # 3. Current Market Snapshot (placeholder - real data would come from snapshot)
        lines.append("## 3. Current Market Snapshot")
        lines.append("_Snapshot data available via `replay-current --session-id SESSION_ID`_")
        lines.append("")

        # 4. Quality Gate
        lines.append("## 4. Quality Gate")
        lines.append(f"- Qualification: **{summary.get('qualification', 'UNKNOWN')}**")
        lines.append("")

        # 5. Strategy Knowledge
        lines.append("## 5. Strategy Knowledge")
        lines.append("_Strategy knowledge context available via `replay-current` command._")
        lines.append("")

        # 6. Decisions
        lines.append("## 6. Decisions")
        dc = summary.get("decision_counts", {})
        dist = summary.get("action_distribution", {})
        lines.append(f"- Total Decisions: {dc.get('total', 0)}")
        lines.append(f"- Simulation Decision Only: {dc.get('simulation_decision_only', True)}")
        if dist:
            lines.append("")
            lines.append("| Action | Count |")
            lines.append("|--------|-------|")
            for action, count in sorted(dist.items()):
                lines.append(f"| {action} | {count} |")
        lines.append("")

        # 7. Annotations
        lines.append("## 7. Annotations")
        lines.append(f"- Total Annotations: {summary.get('annotation_count', 0)}")
        lines.append("")

        # 8. Warnings
        lines.append("## 8. Warnings")
        warnings = summary.get("warnings", [])
        if warnings:
            for w in warnings:
                lines.append(f"- {w}")
        else:
            lines.append("_No warnings._")
        lines.append("")

        # 9. Safety Declaration
        lines.append("## 9. Safety Declaration")
        safety = summary.get("safety_status", {})
        lines.append("| Safety Check | Status |")
        lines.append("|-------------|--------|")
        lines.append(f"| Replay Training Only | {safety.get('replay_training_only', True)} |")
        lines.append(f"| No Real Orders | {safety.get('no_real_orders', True)} |")
        lines.append(f"| Broker Execution Disabled | {safety.get('broker_execution_disabled', True)} |")
        lines.append(f"| Simulation Decision Only | {safety.get('simulation_decision_only', True)} |")
        lines.append(f"| No Future Performance Evaluation | {safety.get('no_future_performance_evaluation', True)} |")
        lines.append(f"| Not Investment Advice | {safety.get('not_investment_advice', True)} |")
        lines.append("")
        lines.append("---")
        lines.append("_This report is for research and training purposes only. Not Investment Advice._")

        return "\n".join(lines)

    def save(self, content: str, session_id: str) -> str:
        """Save report to file. Returns file path."""
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        filename = f"replay_training_session_report_{session_id}.md"
        path = self.reports_dir / filename
        with open(str(path), "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("[ReplayReport] Saved report to %s", path)
        return str(path)

    def _load_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load summary from replay engine."""
        try:
            from replay.replay_training_engine import ReplayTrainingEngine
            engine = ReplayTrainingEngine(repo_root=str(self.repo_root))
            return engine.build_summary(session_id)
        except Exception as exc:
            logger.warning("[ReplayReport] Could not load summary for %s: %s", session_id, exc)
            return None
