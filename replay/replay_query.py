"""
replay/replay_query.py — ReplayQuery v1.2.0

Query interface for replay session data.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayQuery:
    """Query interface for replay session data."""

    def __init__(self, store=None):
        self._store = store

    def list_sessions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List all sessions, most recent first."""
        if not self._store:
            return []
        sessions = self._store.list_sessions()
        return sessions[-limit:]

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session config for session_id."""
        if not self._store:
            return None
        return self._store.load_session_config(session_id)

    def active_sessions(self) -> List[Dict[str, Any]]:
        """Return sessions with status PLAYING or READY."""
        sessions = self.list_sessions(limit=1000)
        states = []
        for s in sessions:
            sid = s.get("session_id", "")
            state = self._store.load_session_state(sid) if self._store else None
            if state and state.get("status") in ("PLAYING", "READY", "PAUSED"):
                states.append({**s, "state": state})
        return states

    def completed_sessions(self) -> List[Dict[str, Any]]:
        """Return sessions with status COMPLETED."""
        sessions = self.list_sessions(limit=1000)
        result = []
        for s in sessions:
            sid = s.get("session_id", "")
            state = self._store.load_session_state(sid) if self._store else None
            if state and state.get("status") == "COMPLETED":
                result.append({**s, "state": state})
        return result

    def archived_sessions(self) -> List[Dict[str, Any]]:
        """Return sessions with status ARCHIVED."""
        sessions = self.list_sessions(limit=1000)
        result = []
        for s in sessions:
            sid = s.get("session_id", "")
            state = self._store.load_session_state(sid) if self._store else None
            if state and state.get("status") == "ARCHIVED":
                result.append({**s, "state": state})
        return result

    def session_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current state for session_id."""
        if not self._store:
            return None
        return self._store.load_session_state(session_id)

    def session_decisions(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all decisions for session_id."""
        if not self._store:
            return []
        return self._store.load_decisions(session_id)

    def session_events(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all events for session_id."""
        if not self._store:
            return []
        return self._store.load_events(session_id)

    def session_annotations(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all annotations for session_id."""
        if not self._store:
            return []
        return self._store.load_annotations(session_id)

    def latest_session(self, symbol: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get the most recent session, optionally filtered by symbol."""
        sessions = self.list_sessions(limit=1000)
        if symbol:
            sessions = [s for s in sessions if s.get("symbol") == symbol]
        return sessions[-1] if sessions else None

    def search_sessions(self, query: str) -> List[Dict[str, Any]]:
        """Search sessions by id, name, symbol, date range, status, action, tag."""
        all_sessions = self.list_sessions(limit=1000)
        q = query.lower()
        result = []
        for s in all_sessions:
            sid = s.get("session_id", "").lower()
            name = s.get("session_name", "").lower()
            symbol = s.get("symbol", "").lower()
            start = s.get("start_date", "").lower()
            end = s.get("end_date", "").lower()
            if (q in sid or q in name or q in symbol or q in start or q in end):
                result.append(s)
            else:
                # Check state
                state = self._store.load_session_state(s.get("session_id", "")) if self._store else None
                if state:
                    status = state.get("status", "").lower()
                    if q in status:
                        result.append(s)
        return result

    # v1.2.1 extended query methods

    def filter_sessions(
        self, symbol=None, scenario=None, status=None, qualification=None,
        date_from=None, date_to=None, tag=None, archived=None,
        active=None, completed=None, blocked=None,
    ) -> List[Dict[str, Any]]:
        """Filter sessions with multiple criteria."""
        all_sessions = self.list_sessions(limit=1000)
        results = []
        for s in all_sessions:
            sid = s.get("session_id", "")
            state = self._store.load_session_state(sid) if self._store else None
            if symbol and s.get("symbol") != symbol:
                continue
            if scenario and s.get("scenario_id") != scenario:
                continue
            if status and (state or {}).get("status") != status:
                continue
            if archived is not None:
                is_arch = (state or {}).get("status") == "ARCHIVED"
                if archived != is_arch:
                    continue
            if active is not None:
                is_active = (state or {}).get("status") in ("PLAYING", "READY", "PAUSED")
                if active != is_active:
                    continue
            if completed is not None:
                is_comp = (state or {}).get("status") == "COMPLETED"
                if completed != is_comp:
                    continue
            if blocked is not None:
                is_blocked = (state or {}).get("status") == "BLOCKED"
                if blocked != is_blocked:
                    continue
            results.append(s)
        return results

    def by_scenario(self, scenario_id: str) -> List[Dict[str, Any]]:
        all_sessions = self.list_sessions(limit=1000)
        return [s for s in all_sessions if s.get("scenario_id") == scenario_id]

    def by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        all_sessions = self.list_sessions(limit=1000)
        return [s for s in all_sessions if s.get("symbol") == symbol]

    def by_status(self, status: str) -> List[Dict[str, Any]]:
        all_sessions = self.list_sessions(limit=1000)
        results = []
        for s in all_sessions:
            sid = s.get("session_id", "")
            state = self._store.load_session_state(sid) if self._store else None
            if state and state.get("status") == status:
                results.append(s)
        return results

    def by_tag(self, tag: str) -> List[Dict[str, Any]]:
        all_sessions = self.list_sessions(limit=1000)
        return [s for s in all_sessions if tag in s.get("tags", [])]

    def active(self) -> List[Dict[str, Any]]:
        return self.active_sessions()

    def completed(self) -> List[Dict[str, Any]]:
        return self.completed_sessions()

    def blocked(self) -> List[Dict[str, Any]]:
        return self.by_status("BLOCKED")

    def archived(self) -> List[Dict[str, Any]]:
        return self.archived_sessions()

    def hidden(self) -> List[Dict[str, Any]]:
        all_sessions = self.list_sessions(limit=1000)
        results = []
        for s in all_sessions:
            sid = s.get("session_id", "")
            state = self._store.load_session_state(sid) if self._store else None
            if state and state.get("hidden", False):
                results.append(s)
        return results

    def session_checkpoints(self, session_id: str) -> List[Dict[str, Any]]:
        if not self._store:
            return []
        return self._store.load_checkpoints_index() if hasattr(self._store, "load_checkpoints_index") else []

    def session_children(self, session_id: str) -> List[Dict[str, Any]]:
        all_sessions = self.list_sessions(limit=1000)
        return [s for s in all_sessions if s.get("parent_session_id") == session_id]

    def session_parent(self, session_id: str) -> Optional[Dict[str, Any]]:
        s = self.get_session(session_id)
        if not s:
            return None
        parent_id = s.get("parent_session_id")
        if not parent_id:
            return None
        return self.get_session(parent_id)

    def session_lineage(self, session_id: str) -> Optional[Dict[str, Any]]:
        if not self._store or not hasattr(self._store, "load_lineage_entries"):
            return None
        entries = self._store.load_lineage_entries()
        for e in entries:
            if e.get("session_id") == session_id:
                return e
        return None

    def latest_checkpoint(self, session_id: str) -> Optional[Dict[str, Any]]:
        cps = self.session_checkpoints(session_id)
        if not cps:
            return None
        return sorted(cps, key=lambda c: c.get("created_at", ""))[-1]

    def session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary for session_id."""
        config = self.get_session(session_id) or {}
        state = self.session_state(session_id) or {}
        decisions = self.session_decisions(session_id)
        annotations = self.session_annotations(session_id)
        events = self.session_events(session_id)
        return {
            "session_id": session_id,
            "config": config,
            "state": state,
            "decision_count": len(decisions),
            "annotation_count": len(annotations),
            "event_count": len(events),
            "research_only": True,
            "no_real_orders": True,
        }
