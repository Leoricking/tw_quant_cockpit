"""
replay/timeframe_query.py — TimeframeQueryEngine v1.2.5

Query engine for multi-timeframe replay data.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class TimeframeQueryEngine:
    """
    Query engine for multi-timeframe replay snapshots, agreements, conflicts, timeline.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None) -> None:
        self._store = store

    def snapshots(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return all timeframe snapshots, optionally filtered by session."""
        if self._store:
            return self._store.get_snapshots(session_id=session_id)
        return []

    def snapshot(
        self,
        session_id: str,
        timestamp: str,
        timeframe: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return snapshot for session at timestamp, optionally for specific TF."""
        snaps = self.snapshots(session_id)
        for s in snaps:
            if s.get("replay_timestamp", "") == timestamp:
                if timeframe is None or s.get("timeframe") == timeframe:
                    return s
        return None

    def multi_snapshot(
        self, session_id: str, timestamp: str
    ) -> Optional[Dict[str, Any]]:
        """Return multi-timeframe snapshot for session at timestamp."""
        if self._store:
            return self._store.get_multi_snapshot(session_id, timestamp)
        return None

    def agreements(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return all agreement results."""
        if self._store:
            return self._store.get_agreements(session_id=session_id)
        return []

    def conflicts(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return all conflict records."""
        if self._store:
            return self._store.get_conflicts(session_id=session_id)
        return []

    def timeline(
        self, session_id: str, timeframe: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Return timeline events for session."""
        if self._store:
            events = self._store.get_timeline(session_id)
            if timeframe:
                events = [e for e in events if e.get("timeframe") == timeframe]
            return events
        return []

    def by_timeframe(
        self, timeframe: str, session_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Return all snapshots for a specific timeframe."""
        snaps = self.snapshots(session_id)
        return [s for s in snaps if s.get("timeframe") == timeframe]

    def by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        """Return all snapshots for a symbol."""
        snaps = self.snapshots()
        return [s for s in snaps if s.get("symbol") == symbol]

    def by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Return all snapshots for a session."""
        return self.snapshots(session_id)

    def partial_bars(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return snapshots with partial bars."""
        snaps = self.snapshots(session_id)
        return [
            s for s in snaps
            if s.get("current_bar") and s["current_bar"].get("is_partial")
        ]

    def blocked_timeframes(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return alignment results where status=BLOCKED."""
        if self._store:
            aligns = self._store.get_alignment_results(session_id=session_id)
            return [a for a in aligns if a.get("status") == "BLOCKED"]
        return []

    def unavailable_timeframes(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return snapshots with unavailable timeframes."""
        if self._store:
            aligns = self._store.get_alignment_results(session_id=session_id)
            return [a for a in aligns if a.get("status") == "UNAVAILABLE"]
        return []

    def latest_snapshot(
        self, session_id: str, timeframe: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Return latest snapshot for session."""
        snaps = self.by_session(session_id)
        if timeframe:
            snaps = [s for s in snaps if s.get("timeframe") == timeframe]
        if not snaps:
            return None
        return max(snaps, key=lambda s: s.get("replay_timestamp", ""))

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search snapshots by keyword."""
        snaps = self.snapshots()
        query_lower = query.lower()
        results = []
        for s in snaps:
            searchable = str(s).lower()
            if query_lower in searchable:
                results.append(s)
        return results
