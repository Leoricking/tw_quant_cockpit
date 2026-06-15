"""
replay/decision_journal_summary.py — DecisionJournalSummaryBuilder for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] FORBIDDEN stats: win_rate, return_rate, pnl, accuracy, alpha, sharpe, hindsight_score
[!] Only allowed: entry counts, distributions, checklists, revision stats.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

FORBIDDEN_SUMMARY_FIELDS = [
    "win_rate", "return_rate", "pnl", "accuracy", "alpha", "sharpe", "hindsight_score",
    "realized_return", "future_return", "final_result",
]


def _check_forbidden(d: Dict[str, Any]) -> None:
    """Raise ValueError if any forbidden stat present."""
    found = [k for k in FORBIDDEN_SUMMARY_FIELDS if k in d]
    if found:
        raise ValueError(
            f"Forbidden stats in summary: {found}. "
            "Decision Journal Summary must NOT include performance metrics."
        )


class DecisionJournalSummaryBuilder:
    """
    Builds summary stats for decision journal entries.

    [!] NO performance metrics. Only process/behavior stats.
    Allowed: entry_count, draft_count, recorded_count, revised_count,
    archived_count, setup_type_distribution, emotion_distribution,
    checklist_pass_rate, tag_frequency, revision_frequency.
    """

    no_real_orders = True
    research_only = True

    FORBIDDEN_FIELDS = FORBIDDEN_SUMMARY_FIELDS

    def __init__(self, store=None, repo_root: Optional[str] = None):
        self._store = store
        if store is None:
            from replay.decision_journal_store import DecisionJournalStore
            self._store = DecisionJournalStore(repo_root=repo_root)

    def _get_all_entries(self) -> List[Dict[str, Any]]:
        raw = self._store.load_entries()
        latest: Dict[str, Dict[str, Any]] = {}
        for e in raw:
            eid = e.get("journal_entry_id", "")
            if eid:
                latest[eid] = e
        return list(latest.values())

    def build_summary(self, session_id: str) -> Dict[str, Any]:
        """Build per-session summary."""
        all_entries = self._get_all_entries()
        entries = [e for e in all_entries if e.get("session_id") == session_id]
        summary = self._build_from_entries(entries, scope=f"session:{session_id}")
        _check_forbidden(summary)
        return summary

    def build_period_summary(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Build summary across a date range."""
        all_entries = self._get_all_entries()
        entries = [
            e for e in all_entries
            if start_date <= e.get("replay_date", "") <= end_date
        ]
        summary = self._build_from_entries(entries, scope=f"period:{start_date}~{end_date}")
        _check_forbidden(summary)
        return summary

    def _build_from_entries(
        self, entries: List[Dict[str, Any]], scope: str = ""
    ) -> Dict[str, Any]:
        """Build summary dict from a list of entries."""
        total = len(entries)
        draft_count = sum(1 for e in entries if e.get("status") == "DRAFT")
        recorded_count = sum(1 for e in entries if e.get("status") == "RECORDED")
        revised_count = sum(1 for e in entries if e.get("status") == "REVISED")
        archived_count = sum(1 for e in entries if e.get("status") == "ARCHIVED")
        blocked_count = sum(1 for e in entries if e.get("status") == "BLOCKED")
        hidden_count = sum(1 for e in entries if e.get("hidden", False))

        # Setup type distribution (from tags)
        setup_dist: Dict[str, int] = {}
        for e in entries:
            for tag in e.get("tags", []):
                setup_dist[tag] = setup_dist.get(tag, 0) + 1

        # Action distribution
        action_dist: Dict[str, int] = {}
        for e in entries:
            a = e.get("action", "UNKNOWN")
            action_dist[a] = action_dist.get(a, 0) + 1

        # Confidence distribution
        conf_buckets = {"0-25": 0, "26-50": 0, "51-75": 0, "76-100": 0}
        for e in entries:
            c = int(e.get("confidence", 50))
            if c <= 25:
                conf_buckets["0-25"] += 1
            elif c <= 50:
                conf_buckets["26-50"] += 1
            elif c <= 75:
                conf_buckets["51-75"] += 1
            else:
                conf_buckets["76-100"] += 1

        # Revision stats
        all_revisions = self._store.load_revisions()
        session_revisions = [r for r in all_revisions
                             if any(r.get("journal_entry_id") == e.get("journal_entry_id") for e in entries)]
        total_revisions = len(session_revisions)
        revision_frequency = (total_revisions / total) if total > 0 else 0.0

        # Point-in-time warnings
        pit_warnings = sum(1 for e in entries if not e.get("point_in_time_verified", False))

        return {
            "scope": scope,
            "entry_count": total,
            "draft_count": draft_count,
            "recorded_count": recorded_count,
            "revised_count": revised_count,
            "archived_count": archived_count,
            "blocked_count": blocked_count,
            "hidden_count": hidden_count,
            "action_distribution": action_dist,
            "setup_type_distribution": setup_dist,
            "confidence_distribution": conf_buckets,
            "total_revisions": total_revisions,
            "revision_frequency": round(revision_frequency, 3),
            "point_in_time_warnings": pit_warnings,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    def session_overview(self, session_id: str) -> Dict[str, Any]:
        """Alias for build_summary."""
        return self.build_summary(session_id)
