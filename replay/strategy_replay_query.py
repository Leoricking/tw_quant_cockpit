"""
replay/strategy_replay_query.py — Query interface for strategy replay store.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class StrategyReplayQuery:
    """
    Query interface for strategy replay store.
    All methods are read-only.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None, repo_root: Optional[str] = None):
        if store is not None:
            self._store = store
        else:
            from replay.strategy_replay_store import StrategyReplayStore
            self._store = StrategyReplayStore(repo_root=repo_root)

    def snapshots(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if session_id:
            return self._store.load_by_session("snapshot", session_id)
        return self._store.load_snapshots()

    def snapshot(self, snapshot_id: str) -> Optional[Dict[str, Any]]:
        for snap in self._store.load_snapshots():
            if snap.get("strategy_snapshot_id") == snapshot_id:
                return snap
        return None

    def module_results(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if session_id:
            return self._store.load_by_session("module_result", session_id)
        return self._store.load_module_results()

    def signal_timeline(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if session_id:
            return self._store.load_by_session("timeline", session_id)
        return self._store.load_timeline()

    def agreements(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if session_id:
            return self._store.load_by_session("agreement", session_id)
        return self._store.load_agreements()

    def conflicts(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if session_id:
            return self._store.load_by_session("conflict", session_id)
        return self._store.load_conflicts()

    def rule_reviews(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if session_id:
            return self._store.load_by_session("rule_review", session_id)
        return self._store.load_rule_reviews()

    def pending_reviews(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        reviews = self.rule_reviews(session_id)
        return [r for r in reviews if r.get("status") in ("SUGGESTED", "NEEDS_REVIEW")]

    def confirmed_reviews(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        reviews = self.rule_reviews(session_id)
        return [r for r in reviews if r.get("status") == "CONFIRMED"]

    def by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        return self._store.load_by_symbol("snapshot", symbol)

    def by_scenario(self, scenario_id: str) -> List[Dict[str, Any]]:
        return [
            s for s in self._store.load_snapshots()
            if s.get("source_metadata", {}).get("scenario_id") == scenario_id
        ]

    def by_module(self, module_name: str) -> List[Dict[str, Any]]:
        return [
            r for r in self._store.load_module_results()
            if r.get("module_name") == module_name
        ]

    def by_signal(self, signal: str) -> List[Dict[str, Any]]:
        return [
            r for r in self._store.load_module_results()
            if str(r.get("signal", "")).lower() == signal.lower()
        ]

    def by_warning(self, warning_contains: str) -> List[Dict[str, Any]]:
        return [
            r for r in self._store.load_module_results()
            if warning_contains.lower() in str(r.get("warning", "")).lower()
        ]

    def latest_snapshot(self, session_id: str) -> Optional[Dict[str, Any]]:
        snaps = self._store.load_by_session("snapshot", session_id)
        if not snaps:
            return None
        return sorted(snaps, key=lambda s: s.get("replay_date", ""), reverse=True)[0]

    def compare_records(
        self, session_id: str, date_a: str, date_b: str
    ) -> Dict[str, Any]:
        all_snaps = self._store.load_by_session("snapshot", session_id)
        snap_a = next((s for s in all_snaps if s.get("replay_date") == date_a), None)
        snap_b = next((s for s in all_snaps if s.get("replay_date") == date_b), None)
        if not snap_a or not snap_b:
            return {"error": "One or both snapshots not found", "date_a": date_a, "date_b": date_b}
        from replay.strategy_replay_comparator import StrategyReplayComparator
        comp = StrategyReplayComparator()
        return comp.compare_snapshots(snap_a, snap_b)

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Full text search across snapshots."""
        q = query.lower()
        results = []
        for snap in self._store.load_snapshots():
            text = json_text(snap)
            if q in text.lower():
                results.append(snap)
        return results


def json_text(obj: Any) -> str:
    import json
    try:
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return str(obj)
