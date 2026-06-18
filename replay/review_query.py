"""
replay/review_query.py — ReplayReviewQuery v1.2.6

Query engine for all replay review data: dashboards, sessions, queue,
progress, checklists, notes, tags, history.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayReviewQuery:
    """
    Query engine for replay review data.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None) -> None:
        self._store = store

    def _store_or_empty(self, method: str, *args, **kwargs) -> List[Dict[str, Any]]:
        if self._store and hasattr(self._store, method):
            try:
                return getattr(self._store, method)(*args, **kwargs) or []
            except Exception as exc:
                logger.warning("Store method %s failed: %s", method, exc)
        return []

    def dashboards(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._store_or_empty("get_snapshots", limit)

    def sessions(self) -> List[Dict[str, Any]]:
        try:
            from replay.review_dashboard_adapter import ReplayReviewDashboardAdapter
            adapter = ReplayReviewDashboardAdapter()
            result = adapter.load_sessions()
            return result.get("data", []) or []
        except Exception as exc:
            logger.warning("sessions query failed: %s", exc)
            return []

    def session(self, session_id: str) -> Optional[Dict[str, Any]]:
        rows = self.sessions()
        for r in rows:
            if r.get("session_id") == session_id:
                return r
        return None

    def queue(self) -> List[Dict[str, Any]]:
        return self._store_or_empty("get_queue")

    def progress(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self._store_or_empty("get_progress", session_id)

    def checklists(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self._store_or_empty("get_checklists", session_id)

    def notes(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self._store_or_empty("get_notes", session_id)

    def tags(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self._store_or_empty("get_tags", session_id)

    def review_history(self) -> List[Dict[str, Any]]:
        return self._store_or_empty("get_history")

    def pending_reviews(self) -> List[Dict[str, Any]]:
        q = self.queue()
        return [i for i in q if i.get("status") == "OPEN"]

    def completed_reviews(self) -> List[Dict[str, Any]]:
        q = self.queue()
        return [i for i in q if i.get("status") == "COMPLETED"]

    def blocked_reviews(self) -> List[Dict[str, Any]]:
        q = self.queue()
        return [i for i in q if i.get("status") == "BLOCKED"]

    def by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        return [r for r in self.sessions() if r.get("symbol") == symbol]

    def by_scenario(self, scenario_id: str) -> List[Dict[str, Any]]:
        return [r for r in self.sessions() if r.get("scenario_id") == scenario_id]

    def by_classification(self, classification: str) -> List[Dict[str, Any]]:
        return [r for r in self.sessions() if r.get("classification") == classification]

    def by_mistake(self, min_mistakes: int = 1) -> List[Dict[str, Any]]:
        return [r for r in self.sessions() if r.get("mistake_count", 0) >= min_mistakes]

    def by_strategy_conflict(self) -> List[Dict[str, Any]]:
        return [r for r in self.sessions() if r.get("strategy_conflicts", 0) > 0]

    def by_timeframe_conflict(self) -> List[Dict[str, Any]]:
        return [r for r in self.sessions() if r.get("mtf_conflicts", 0) > 0]

    def search(self, query: str) -> List[Dict[str, Any]]:
        from replay.review_search import ReplayReviewSearch
        searcher = ReplayReviewSearch()
        return searcher.search(self.sessions(), query)
