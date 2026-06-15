"""
reports/replay_decision_journal_report.py — ReplayDecisionJournalReport v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] No performance metrics. No hindsight. No future data.
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


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplayDecisionJournalReport:
    """
    Generates per-session journal entry detail report.

    [!] FORBIDDEN stats not included: win_rate, return_rate, pnl, accuracy,
        alpha, sharpe, hindsight_score, realized_return, future_return.
    """

    no_real_orders = True
    research_only = True

    FORBIDDEN_FIELDS = [
        "win_rate", "return_rate", "pnl", "accuracy", "alpha", "sharpe",
        "hindsight_score", "realized_return", "future_return", "final_result",
    ]

    def __init__(self, store=None, repo_root: Optional[str] = None):
        self._store = store
        self._repo_root = repo_root or ""
        if store is None:
            try:
                from replay.decision_journal_store import DecisionJournalStore
                self._store = DecisionJournalStore(repo_root=repo_root)
            except Exception as exc:
                logger.warning("Could not init store: %s", exc)

    def build(self, session_id: str, output_dir: Optional[str] = None) -> str:
        """Build the journal report for a session. Returns markdown string."""
        entries = []
        revisions = []

        if self._store:
            all_entries = self._store.load_entries()
            entries = [e for e in all_entries if e.get("session_id") == session_id]
            all_revisions = self._store.load_revisions()
            revisions = [r for r in all_revisions
                         if any(r.get("journal_entry_id") == e.get("journal_entry_id") for e in entries)]

        lines = [
            "# Replay Decision Journal Report v1.2.2",
            "",
            "> **[!] Decision Journal Only | Simulation Decision Only | No Auto Scoring**",
            "> **[!] No Real Orders | Broker Disabled | Not Investment Advice**",
            "",
            "## I. Journal Overview",
            "",
            f"- **Session ID**: {session_id}",
            f"- **Total Entries**: {len(entries)}",
            f"- **Total Revisions**: {len(revisions)}",
            f"- **Report Generated**: {_now_utc()}",
            "",
        ]

        # Status breakdown
        status_counts: Dict[str, int] = {}
        for e in entries:
            s = e.get("status", "UNKNOWN")
            status_counts[s] = status_counts.get(s, 0) + 1

        lines.append("### Entry Status Distribution")
        lines.append("")
        for s, cnt in status_counts.items():
            lines.append(f"- {s}: {cnt}")
        lines.append("")

        # Entry list
        lines.append("## II. Decision Timeline")
        lines.append("")
        lines.append("| Entry ID | Date | Action | Confidence | Status | Revisions |")
        lines.append("|----------|------|--------|------------|--------|-----------|")
        for e in entries:
            rev_count = sum(1 for r in revisions if r.get("journal_entry_id") == e.get("journal_entry_id"))
            lines.append(
                f"| {e.get('journal_entry_id', '')} "
                f"| {e.get('replay_date', '')} "
                f"| {e.get('action', '')} "
                f"| {e.get('confidence', '')} "
                f"| {e.get('status', '')} "
                f"| {rev_count} |"
            )
        lines.append("")

        # Revision history
        lines.append("## III. Revision History")
        lines.append("")
        if revisions:
            lines.append("| Revision ID | Entry ID | Rev# | Reason | Confidence Before | After |")
            lines.append("|-------------|----------|------|--------|-------------------|-------|")
            for r in revisions:
                lines.append(
                    f"| {r.get('revision_id', '')} "
                    f"| {r.get('journal_entry_id', '')} "
                    f"| {r.get('revision_number', '')} "
                    f"| {r.get('reason', '')[:40]} "
                    f"| {r.get('confidence_before', '')} "
                    f"| {r.get('confidence_after', '')} |"
                )
        else:
            lines.append("_No revisions recorded._")
        lines.append("")

        # Safety declaration
        lines.append("## IV. Safety Declaration")
        lines.append("")
        lines.append("- **Decision Journal Only**")
        lines.append("- **Simulation Decision Only**")
        lines.append("- **No Auto Scoring**")
        lines.append("- **No Auto Generation**")
        lines.append("- **No Auto Execution**")
        lines.append("- **No Real Orders**")
        lines.append("- **Broker Disabled**")
        lines.append("- **Not Investment Advice**")

        md = "\n".join(lines)

        if output_dir:
            path = Path(output_dir) / f"replay_decision_journal_report_{session_id}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(md)
            logger.info("Journal report saved: %s", path)

        return md

    def generate(self, session_id: str, output_dir: Optional[str] = None) -> str:
        """Alias for build."""
        return self.build(session_id, output_dir=output_dir)


# Backward-compat alias
ReplayDecisionJournalReportBuilder = ReplayDecisionJournalReport
