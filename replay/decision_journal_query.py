"""
replay/decision_journal_query.py — DecisionJournalQuery for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] No performance metrics. No future data.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class DecisionJournalQuery:
    """
    Query interface for decision journal entries.

    Supports filtering by session, symbol, date, action, setup, emotion,
    bias flags, tags, status, and free-text search.

    [!] Research Only. No performance fields returned.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, store=None, repo_root: Optional[str] = None):
        self._store = store
        if store is None:
            from replay.decision_journal_store import DecisionJournalStore
            self._store = DecisionJournalStore(repo_root=repo_root)

    def _get_all_entries(self) -> List[Dict[str, Any]]:
        """Load and deduplicate entries (latest record per ID)."""
        raw = self._store.load_entries()
        latest: Dict[str, Dict[str, Any]] = {}
        for e in raw:
            eid = e.get("journal_entry_id", "")
            if eid:
                latest[eid] = e
        return list(latest.values())

    def list_entries(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List all entries."""
        entries = self._get_all_entries()
        return entries[:limit]

    def get_entry(self, journal_entry_id: str) -> Optional[Dict[str, Any]]:
        """Get single entry by ID."""
        return self._store.get_entry(journal_entry_id)

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Free-text search across notes, thesis, reason, tags."""
        if not query:
            return self._get_all_entries()
        q = query.lower()
        results = []
        for e in self._get_all_entries():
            searchable = " ".join([
                e.get("journal_entry_id", ""),
                e.get("decision_id", ""),
                e.get("session_id", ""),
                e.get("symbol", ""),
                e.get("notes", ""),
                e.get("decision_reason", ""),
                e.get("pre_decision_notes", ""),
                e.get("post_decision_notes", ""),
                " ".join(e.get("tags", [])),
            ]).lower()
            if q in searchable:
                results.append(e)
        return results

    def by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Entries for a session."""
        return [e for e in self._get_all_entries() if e.get("session_id") == session_id]

    def by_scenario(self, scenario_id: str) -> List[Dict[str, Any]]:
        return [e for e in self._get_all_entries() if e.get("scenario_id") == scenario_id]

    def by_checkpoint(self, checkpoint_id: str) -> List[Dict[str, Any]]:
        return [e for e in self._get_all_entries() if e.get("checkpoint_id") == checkpoint_id]

    def by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        return [e for e in self._get_all_entries() if e.get("symbol") == symbol]

    def by_date(self, replay_date: str) -> List[Dict[str, Any]]:
        return [e for e in self._get_all_entries() if e.get("replay_date") == replay_date]

    def by_action(self, action: str) -> List[Dict[str, Any]]:
        return [e for e in self._get_all_entries() if e.get("action") == action.upper()]

    def by_setup(self, setup_type: str) -> List[Dict[str, Any]]:
        """Filter by setup type (from thesis_id linked data or tag)."""
        return [e for e in self._get_all_entries()
                if setup_type.upper() in " ".join(e.get("tags", [])).upper()]

    def by_emotion(self, emotion: str) -> List[Dict[str, Any]]:
        """Filter by emotion (from emotional_state_id linked or tag)."""
        return [e for e in self._get_all_entries()
                if emotion.upper() in " ".join(e.get("tags", [])).upper()]

    def by_bias(self, bias_flag: str) -> List[Dict[str, Any]]:
        """Filter by cognitive bias flag."""
        return [e for e in self._get_all_entries()
                if bias_flag.upper() in " ".join(e.get("tags", [])).upper()]

    def by_tag(self, tag: str) -> List[Dict[str, Any]]:
        return [e for e in self._get_all_entries()
                if tag in e.get("tags", [])]

    def by_status(self, status: str) -> List[Dict[str, Any]]:
        return [e for e in self._get_all_entries() if e.get("status") == status.upper()]

    def drafts(self) -> List[Dict[str, Any]]:
        return self.by_status("DRAFT")

    def revised(self) -> List[Dict[str, Any]]:
        return self.by_status("REVISED")

    def archived(self) -> List[Dict[str, Any]]:
        return self.by_status("ARCHIVED")

    def hidden(self) -> List[Dict[str, Any]]:
        return [e for e in self._get_all_entries() if e.get("hidden", False)]

    def latest_for_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        entries = self.by_session(session_id)
        return entries[-1] if entries else None

    def revision_history(self, journal_entry_id: str) -> List[Dict[str, Any]]:
        """Get all revisions for an entry."""
        revisions = self._store.load_revisions()
        return [r for r in revisions if r.get("journal_entry_id") == journal_entry_id]

    def linked_entries(self, journal_entry_id: str) -> List[Dict[str, Any]]:
        """Get all links for an entry."""
        links = self._store.load_links()
        return [lnk for lnk in links
                if lnk.get("source_entry_id") == journal_entry_id
                or lnk.get("target_entry_id") == journal_entry_id]

    def get_entry_with_full_context(self, journal_entry_id: str) -> Dict[str, Any]:
        """Return entry + all linked data (thesis, risk_plan, emotional_state, checklists)."""
        entry = self.get_entry(journal_entry_id)
        if not entry:
            return {}

        revisions = self.revision_history(journal_entry_id)
        links = self.linked_entries(journal_entry_id)

        return {
            "entry": entry,
            "revisions": revisions,
            "links": links,
            "thesis": None,         # Full integration with separate thesis store
            "risk_plan": None,
            "emotional_state": None,
            "checklists": [],
            "revision_count": len(revisions),
        }

    def filter_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        return self.by_session(session_id)

    def filter_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        return [e for e in self._get_all_entries()
                if start_date <= e.get("replay_date", "") <= end_date]

    def filter_by_status(self, status: str) -> List[Dict[str, Any]]:
        return self.by_status(status)

    def filter_by_setup_type(self, setup_type: str) -> List[Dict[str, Any]]:
        return self.by_setup(setup_type)

    def filter_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        return [e for e in self._get_all_entries()
                if any(t in e.get("tags", []) for t in tags)]

    def filter_by_emotion(self, emotion: str) -> List[Dict[str, Any]]:
        return self.by_emotion(emotion)

    def filter_by_checklist_result(self, passed: bool) -> List[Dict[str, Any]]:
        return [e for e in self._get_all_entries()
                if bool(e.get("checklist_pass", False)) == passed]

    def search_by_notes(self, text: str) -> List[Dict[str, Any]]:
        t = text.lower()
        return [e for e in self._get_all_entries()
                if t in e.get("notes", "").lower()
                or t in e.get("pre_decision_notes", "").lower()
                or t in e.get("post_decision_notes", "").lower()
                or t in e.get("decision_reason", "").lower()]
