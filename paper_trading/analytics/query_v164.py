"""
paper_trading/analytics/query_v164.py — Analytics Query Service v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from paper_trading.analytics.enums_v164 import ReviewStatus, ReviewScope, ActionItemStatus
from paper_trading.analytics.store_v164 import OperationalAnalyticsStore


NO_REAL_ORDERS = True
NO_BROKER = True
PAPER_ONLY = True


class AnalyticsQueryService:
    """Query facade for operational analytics store."""

    def __init__(self, store: Optional[OperationalAnalyticsStore] = None) -> None:
        if store is None:
            from paper_trading.analytics.store_v164 import get_default_store
            store = get_default_store()
        self._store = store

    # ── Analytics ──────────────────────────────────────────────────────
    def list_analytics(self) -> List[Any]:
        return self._store.list_analytics()

    def get_analytics(self, analytics_id: str) -> Optional[Any]:
        return self._store.get_analytics(analytics_id)

    def find_analytics_by_session(self, session_id: str) -> List[Any]:
        return self._store.find_analytics_by_session(session_id)

    # ── Reviews ────────────────────────────────────────────────────────
    def list_reviews(self) -> List[Any]:
        return self._store.list_reviews()

    def get_review(self, review_id: str) -> Optional[Any]:
        return self._store.get_review(review_id)

    def list_reviews_by_status(self, status: ReviewStatus) -> List[Any]:
        return [r for r in self._store.list_reviews() if getattr(r, "status", None) == status]

    def list_reviews_by_scope(self, scope: ReviewScope) -> List[Any]:
        return [r for r in self._store.list_reviews() if getattr(r, "review_scope", None) == scope]

    # ── Action Items ───────────────────────────────────────────────────
    def list_action_items(self) -> List[Any]:
        return self._store.list_action_items()

    def get_action_item(self, action_item_id: str) -> Optional[Any]:
        return self._store.get_action_item(action_item_id)

    def list_action_items_by_status(self, status: ActionItemStatus) -> List[Any]:
        return [i for i in self._store.list_action_items() if getattr(i, "status", None) == status]

    # ── Lessons ────────────────────────────────────────────────────────
    def list_lessons(self) -> List[Any]:
        return self._store.list_lessons()

    # ── Anomalies & Attribution ────────────────────────────────────────
    def query_anomalies(self, session_id: Optional[str] = None) -> List[Any]:
        return self._store.query_anomalies(session_id=session_id)

    def query_attributions(self, session_id: Optional[str] = None) -> List[Any]:
        return self._store.query_attributions(session_id=session_id)

    # ── Snapshots ──────────────────────────────────────────────────────
    def list_snapshots(self) -> List[Any]:
        return self._store.list_snapshots()

    def get_snapshot(self, snapshot_id: str) -> Optional[Any]:
        return self._store.get_snapshot(snapshot_id)

    # ── Summary ────────────────────────────────────────────────────────
    def summary(self) -> Dict[str, Any]:
        return {
            "total_analytics": len(self.list_analytics()),
            "total_reviews": len(self.list_reviews()),
            "total_action_items": len(self.list_action_items()),
            "total_lessons": len(self.list_lessons()),
            "total_snapshots": len(self.list_snapshots()),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
        }


__all__ = ["AnalyticsQueryService"]
