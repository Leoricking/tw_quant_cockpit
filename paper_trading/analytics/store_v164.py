"""
paper_trading/analytics/store_v164.py — Analytics Local Store v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
Append-only, immutable analytics snapshots. No production DB. No Portfolio Ledger writes.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

NO_REAL_ORDERS = True
NO_BROKER = True
PAPER_ONLY = True
RESEARCH_ONLY = True
PRODUCTION_DB_ENABLED = False
PORTFOLIO_LEDGER_WRITE_ENABLED = False


class OperationalAnalyticsStore:
    """
    In-memory append-only store for analytics results and reviews.
    Immutable analytics snapshots. Reviews are version-tracked.
    No overwrite of historical records.
    """

    def __init__(self) -> None:
        self._analytics: List[Any] = []
        self._reviews: List[Any] = []
        self._action_items: List[Any] = []
        self._lessons: List[Any] = []
        self._snapshots: List[Any] = []
        self._audit: List[Dict[str, Any]] = []

    # ── Analytics ──────────────────────────────────────────────────────
    def save_analytics(self, result: Any) -> str:
        """Append analytics result (immutable). Returns analytics_id."""
        self._analytics.append(result)
        self._audit.append({
            "op": "save_analytics",
            "id": getattr(result, "analytics_id", None),
            "at": datetime.now(tz=timezone.utc).isoformat(),
        })
        return getattr(result, "analytics_id", "")

    def get_analytics(self, analytics_id: str) -> Optional[Any]:
        for r in self._analytics:
            if getattr(r, "analytics_id", None) == analytics_id:
                return r
        return None

    def list_analytics(self) -> List[Any]:
        return list(self._analytics)

    def find_analytics_by_session(self, session_id: str) -> List[Any]:
        return [r for r in self._analytics if getattr(r, "session_id", None) == session_id]

    # ── Reviews ────────────────────────────────────────────────────────
    def save_review(self, review: Any) -> str:
        self._reviews.append(review)
        self._audit.append({
            "op": "save_review",
            "id": getattr(review, "review_id", None),
            "at": datetime.now(tz=timezone.utc).isoformat(),
        })
        return getattr(review, "review_id", "")

    def get_review(self, review_id: str) -> Optional[Any]:
        # Return latest version
        for r in reversed(self._reviews):
            if getattr(r, "review_id", None) == review_id:
                return r
        return None

    def list_reviews(self) -> List[Any]:
        # Return latest version of each review_id
        seen: set = set()
        result: List[Any] = []
        for r in reversed(self._reviews):
            rid = getattr(r, "review_id", None)
            if rid not in seen:
                seen.add(rid)
                result.append(r)
        return list(reversed(result))

    # ── Action Items ───────────────────────────────────────────────────
    def save_action_item(self, item: Any) -> str:
        self._action_items.append(item)
        return getattr(item, "action_item_id", "")

    def get_action_item(self, action_item_id: str) -> Optional[Any]:
        for item in reversed(self._action_items):
            if getattr(item, "action_item_id", None) == action_item_id:
                return item
        return None

    def list_action_items(self) -> List[Any]:
        seen: set = set()
        result: List[Any] = []
        for item in reversed(self._action_items):
            aid = getattr(item, "action_item_id", None)
            if aid not in seen:
                seen.add(aid)
                result.append(item)
        return list(reversed(result))

    # ── Lessons ────────────────────────────────────────────────────────
    def save_lesson(self, lesson: Any) -> str:
        self._lessons.append(lesson)
        return getattr(lesson, "lesson_id", "")

    def list_lessons(self) -> List[Any]:
        return list(self._lessons)

    # ── Snapshots ──────────────────────────────────────────────────────
    def save_snapshot(self, snapshot: Any) -> str:
        self._snapshots.append(snapshot)
        return getattr(snapshot, "snapshot_id", "")

    def get_snapshot(self, snapshot_id: str) -> Optional[Any]:
        for s in self._snapshots:
            if getattr(s, "snapshot_id", None) == snapshot_id:
                return s
        return None

    def list_snapshots(self) -> List[Any]:
        return list(self._snapshots)

    # ── Queries ────────────────────────────────────────────────────────
    def query_anomalies(self, session_id: Optional[str] = None) -> List[Any]:
        results: List[Any] = []
        for r in self._analytics:
            if session_id and getattr(r, "session_id", None) != session_id:
                continue
            results.extend(getattr(r, "anomalies", []))
        return results

    def query_attributions(self, session_id: Optional[str] = None) -> List[Any]:
        results: List[Any] = []
        for r in self._analytics:
            if session_id and getattr(r, "session_id", None) != session_id:
                continue
            results.extend(getattr(r, "attributions", []))
        return results

    def audit_trail(self) -> List[Dict[str, Any]]:
        return list(self._audit)


# Module-level default store instance (research only, in-memory)
_DEFAULT_STORE: Optional[OperationalAnalyticsStore] = None


def get_default_store() -> OperationalAnalyticsStore:
    global _DEFAULT_STORE
    if _DEFAULT_STORE is None:
        _DEFAULT_STORE = OperationalAnalyticsStore()
    return _DEFAULT_STORE


__all__ = ["OperationalAnalyticsStore", "get_default_store"]
