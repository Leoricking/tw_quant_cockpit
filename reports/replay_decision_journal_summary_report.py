"""
reports/replay_decision_journal_summary_report.py — ReplayDecisionJournalSummaryReport v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] FORBIDDEN stats NOT included: win_rate, return_rate, pnl, accuracy, alpha, sharpe,
    hindsight_score, realized_return, future_return, final_result.
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

FORBIDDEN_SUMMARY_FIELDS = [
    "win_rate", "return_rate", "pnl", "accuracy", "alpha", "sharpe",
    "hindsight_score", "realized_return", "future_return", "final_result",
    "future_max_gain", "future_max_loss",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplayDecisionJournalSummaryReport:
    """
    Generates a period/multi-session summary report for the decision journal.

    [!] FORBIDDEN stats not included: win_rate, return_rate, pnl, accuracy,
        alpha, sharpe, hindsight_score, realized_return, future_return, final_result.
    [!] Only allowed stats: entry counts, status distributions, action distributions,
        setup distributions, confidence distributions (buckets), revision counts.
    """

    no_real_orders = True
    research_only = True

    FORBIDDEN_FIELDS = FORBIDDEN_SUMMARY_FIELDS

    def __init__(self, store=None, repo_root: Optional[str] = None):
        self._store = store
        self._repo_root = repo_root or ""
        if store is None:
            try:
                from replay.decision_journal_store import DecisionJournalStore
                self._store = DecisionJournalStore(repo_root=repo_root)
            except Exception as exc:
                logger.warning("Could not init store: %s", exc)

    def _check_forbidden(self, data: Dict[str, Any]) -> None:
        for f in self.FORBIDDEN_FIELDS:
            if f in data:
                raise ValueError(
                    f"[!] FORBIDDEN stat '{f}' attempted in summary report. "
                    "Blocked. Research only."
                )

    def build(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        session_ids: Optional[List[str]] = None,
        output_dir: Optional[str] = None,
    ) -> str:
        """
        Build the period summary report. Returns markdown string.

        Args:
            date_from: ISO date string for start of period (inclusive).
            date_to: ISO date string for end of period (inclusive).
            session_ids: Optional list of session IDs to restrict to.
            output_dir: If provided, write file to this directory.
        """
        entries: List[Dict[str, Any]] = []
        revisions: List[Dict[str, Any]] = []

        if self._store:
            try:
                entries = self._store.load_entries()
                revisions = self._store.load_revisions()
            except Exception as exc:
                logger.warning("Store load error: %s", exc)

        # Filter by session
        if session_ids:
            entries = [e for e in entries if e.get("session_id") in session_ids]

        # Filter by date range
        if date_from:
            entries = [e for e in entries if (e.get("replay_date") or "") >= date_from]
        if date_to:
            entries = [e for e in entries if (e.get("replay_date") or "") <= date_to]

        # Filter revisions to match
        entry_ids = {e.get("journal_entry_id") for e in entries}
        revisions = [r for r in revisions if r.get("journal_entry_id") in entry_ids]

        # Compute allowed stats
        total_entries = len(entries)
        total_revisions = len(revisions)

        status_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}
        setup_counts: Dict[str, int] = {}
        emotion_counts: Dict[str, int] = {}
        session_counts: Dict[str, int] = {}
        tag_counts: Dict[str, int] = {}

        confidence_buckets = {
            "0-20": 0, "21-40": 0, "41-60": 0, "61-80": 0, "81-100": 0,
        }

        entries_with_thesis = 0
        entries_with_risk_plan = 0
        entries_with_emotion = 0
        entries_with_checklist = 0

        for e in entries:
            s = e.get("status", "UNKNOWN")
            status_counts[s] = status_counts.get(s, 0) + 1

            a = e.get("action", "UNKNOWN")
            action_counts[a] = action_counts.get(a, 0) + 1

            setup = e.get("setup_type", "")
            if setup:
                setup_counts[setup] = setup_counts.get(setup, 0) + 1

            emotion = e.get("primary_emotion", "")
            if emotion:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

            sess = e.get("session_id", "")
            if sess:
                session_counts[sess] = session_counts.get(sess, 0) + 1

            for tag in (e.get("tags") or []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

            conf = e.get("confidence")
            if conf is not None:
                try:
                    c = int(conf)
                    if c <= 20:
                        confidence_buckets["0-20"] += 1
                    elif c <= 40:
                        confidence_buckets["21-40"] += 1
                    elif c <= 60:
                        confidence_buckets["41-60"] += 1
                    elif c <= 80:
                        confidence_buckets["61-80"] += 1
                    else:
                        confidence_buckets["81-100"] += 1
                except (TypeError, ValueError):
                    pass

            if e.get("thesis_id"):
                entries_with_thesis += 1
            if e.get("risk_plan_id"):
                entries_with_risk_plan += 1
            if e.get("emotional_state_id"):
                entries_with_emotion += 1
            if e.get("checklist_ids"):
                entries_with_checklist += 1

        # Build period label
        period_label = "All Time"
        if date_from and date_to:
            period_label = f"{date_from} to {date_to}"
        elif date_from:
            period_label = f"From {date_from}"
        elif date_to:
            period_label = f"Up to {date_to}"

        lines = [
            "# Replay Decision Journal Summary Report v1.2.2",
            "",
            "> **[!] Summary Report Only | No Performance Metrics | No Hindsight**",
            "> **[!] No Real Orders | Broker Disabled | Not Investment Advice**",
            "> **[!] Simulation Decision Only | Research Only**",
            "",
            "## I. Summary Overview",
            "",
            f"- **Period**: {period_label}",
        ]

        if session_ids:
            lines.append(f"- **Sessions Filter**: {', '.join(session_ids)}")
        lines.extend([
            f"- **Total Entries**: {total_entries}",
            f"- **Total Revisions**: {total_revisions}",
            f"- **Unique Sessions**: {len(session_counts)}",
            f"- **Report Generated**: {_now_utc()}",
            "",
        ])

        # Status distribution
        lines.extend([
            "## II. Entry Status Distribution",
            "",
        ])
        if status_counts:
            lines.append("| Status | Count |")
            lines.append("|--------|-------|")
            for s, cnt in sorted(status_counts.items()):
                lines.append(f"| {s} | {cnt} |")
        else:
            lines.append("_No entries._")
        lines.append("")

        # Action distribution
        lines.extend([
            "## III. Action Distribution",
            "",
        ])
        if action_counts:
            lines.append("| Action | Count |")
            lines.append("|--------|-------|")
            for a, cnt in sorted(action_counts.items(), key=lambda x: -x[1]):
                lines.append(f"| {a} | {cnt} |")
        else:
            lines.append("_No entries._")
        lines.append("")

        # Setup type distribution
        lines.extend([
            "## IV. Setup Type Distribution",
            "",
        ])
        if setup_counts:
            lines.append("| Setup Type | Count |")
            lines.append("|------------|-------|")
            for st, cnt in sorted(setup_counts.items(), key=lambda x: -x[1]):
                lines.append(f"| {st} | {cnt} |")
        else:
            lines.append("_No setup type data._")
        lines.append("")

        # Confidence distribution
        lines.extend([
            "## V. Confidence Distribution (Buckets)",
            "",
            "| Bucket | Count |",
            "|--------|-------|",
        ])
        for bucket, cnt in confidence_buckets.items():
            lines.append(f"| {bucket} | {cnt} |")
        lines.append("")

        # Emotional state distribution
        lines.extend([
            "## VI. Reported Emotional State Distribution",
            "",
            "> **[!] Self-reported only. NOT a psychological assessment.**",
            "",
        ])
        if emotion_counts:
            lines.append("| Emotion | Count |")
            lines.append("|---------|-------|")
            for em, cnt in sorted(emotion_counts.items(), key=lambda x: -x[1]):
                lines.append(f"| {em} | {cnt} |")
        else:
            lines.append("_No emotional state data._")
        lines.append("")

        # Revision stats
        revision_freq = round(total_revisions / total_entries, 2) if total_entries > 0 else 0.0
        lines.extend([
            "## VII. Revision Statistics",
            "",
            f"- **Total Revisions**: {total_revisions}",
            f"- **Revision Frequency** (revisions/entry): {revision_freq}",
            "",
        ])

        # Completeness stats
        lines.extend([
            "## VIII. Entry Completeness",
            "",
            "| Component | Entries with Data | % Complete |",
            "|-----------|-------------------|------------|",
        ])
        for label, count in [
            ("Trade Thesis", entries_with_thesis),
            ("Risk Plan", entries_with_risk_plan),
            ("Emotional State", entries_with_emotion),
            ("Discipline Checklist", entries_with_checklist),
        ]:
            pct = round(count / total_entries * 100, 1) if total_entries > 0 else 0.0
            lines.append(f"| {label} | {count} | {pct}% |")
        lines.append("")

        # Top tags
        if tag_counts:
            lines.extend([
                "## IX. Top Tags",
                "",
                "| Tag | Count |",
                "|-----|-------|",
            ])
            top_tags = sorted(tag_counts.items(), key=lambda x: -x[1])[:15]
            for tag, cnt in top_tags:
                lines.append(f"| {tag} | {cnt} |")
            lines.append("")

        # Session breakdown
        if len(session_counts) > 1:
            lines.extend([
                "## X. Per-Session Entry Count",
                "",
                "| Session ID | Entries |",
                "|------------|---------|",
            ])
            for sess, cnt in sorted(session_counts.items(), key=lambda x: -x[1])[:20]:
                lines.append(f"| {sess} | {cnt} |")
            lines.append("")

        # Safety declaration
        lines.extend([
            "## Safety Declaration",
            "",
            "- **Summary Statistics Only — No Performance Metrics**",
            "- **Decision Journal Only**",
            "- **Simulation Decision Only**",
            "- **No Auto Scoring**",
            "- **No Auto Generation**",
            "- **No Auto Execution**",
            "- **No Real Orders**",
            "- **Broker Disabled**",
            "- **Not Investment Advice**",
        ])

        md = "\n".join(lines)

        if output_dir:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            filename = f"replay_decision_journal_summary_report_{today}.md"
            path = Path(output_dir) / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(md)
            logger.info("Journal summary report saved: %s", path)

        return md

    def generate(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        session_ids: Optional[List[str]] = None,
        output_dir: Optional[str] = None,
    ) -> str:
        """Alias for build."""
        return self.build(
            date_from=date_from,
            date_to=date_to,
            session_ids=session_ids,
            output_dir=output_dir,
        )


# Backward-compat alias
ReplayDecisionJournalSummaryReportBuilder = ReplayDecisionJournalSummaryReport
