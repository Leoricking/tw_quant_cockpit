"""
replay/review_queue.py — ReplayReviewQueueManager v1.2.6

Manages the review queue with append-only history.
complete() does NOT auto-confirm mistakes or auto-reveal outcomes.

[!] Research Only. No Real Orders. Replay Training Only.
[!] complete() != auto Confirm Mistake. complete() != auto Reveal Outcome.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from replay.review_dashboard_schema import (
    ReplayReviewQueueItem,
    QueueItemStatus,
    QueueItemPriority,
    QueueItemType,
    _new_id,
    _now_utc,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayReviewQueueManager:
    """
    Manages the replay review queue with append-only history.

    [!] complete() does NOT auto-confirm mistakes or auto-reveal outcome.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    AUTO_CONFIRM_ON_COMPLETE = False
    AUTO_REVEAL_ON_COMPLETE  = False

    def __init__(self, store=None) -> None:
        self._store = store
        self._items: Dict[str, ReplayReviewQueueItem] = {}
        self._history: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Build / query
    # ------------------------------------------------------------------

    def build_queue(self, sessions: Optional[List[Dict[str, Any]]] = None) -> List[ReplayReviewQueueItem]:
        """Build queue items from session list."""
        if not sessions:
            return []
        items = []
        for s in sessions:
            session_id = s.get("session_id", "")
            if not s.get("review_complete"):
                item = ReplayReviewQueueItem(
                    queue_item_id=_new_id("QI-"),
                    session_id=session_id,
                    queue_type=QueueItemType.SESSION_INCOMPLETE.value,
                    priority=QueueItemPriority.P2.value,
                    status=QueueItemStatus.OPEN.value,
                    title=f"Review incomplete: {session_id}",
                    symbol=s.get("symbol"),
                    scenario_id=s.get("scenario_id"),
                )
                self._items[item.queue_item_id] = item
                items.append(item)
        return items

    def list_open(self) -> List[ReplayReviewQueueItem]:
        """Return all open queue items."""
        return [i for i in self._items.values() if i.status == QueueItemStatus.OPEN.value]

    def list_by_type(self, queue_type: str) -> List[ReplayReviewQueueItem]:
        """Return items filtered by type."""
        return [i for i in self._items.values() if i.queue_type == queue_type]

    def list_by_priority(self, priority: str) -> List[ReplayReviewQueueItem]:
        """Return items filtered by priority."""
        return [i for i in self._items.values() if i.priority == priority]

    # ------------------------------------------------------------------
    # State transitions (append-only history)
    # ------------------------------------------------------------------

    def start_review(self, queue_item_id: str) -> Dict[str, Any]:
        """Mark item as IN_REVIEW."""
        item = self._items.get(queue_item_id)
        if not item:
            return {"status": "NOT_FOUND", "queue_item_id": queue_item_id}
        item.status     = QueueItemStatus.IN_REVIEW.value
        item.started_at = _now_utc()
        self._append_history(queue_item_id, "start_review", "")
        return {"status": "OK", "queue_item_id": queue_item_id, "new_status": item.status}

    def complete(self, queue_item_id: str, note: str = "") -> Dict[str, Any]:
        """
        Mark item as COMPLETED (metadata review only).

        [!] Does NOT auto-confirm mistakes.
        [!] Does NOT auto-reveal outcome.
        [!] Research Only.
        """
        item = self._items.get(queue_item_id)
        if not item:
            return {"status": "NOT_FOUND", "queue_item_id": queue_item_id}
        item.status       = QueueItemStatus.COMPLETED.value
        item.completed_at = _now_utc()
        item.note         = note
        item.auto_confirm_on_complete = False
        item.auto_reveal_on_complete  = False
        self._append_history(queue_item_id, "complete", note)
        return {
            "status":                  "OK",
            "queue_item_id":           queue_item_id,
            "new_status":              item.status,
            "auto_confirm_mistake":    False,
            "auto_reveal_outcome":     False,
            "research_only":           True,
        }

    def dismiss(self, queue_item_id: str, reason: str = "") -> Dict[str, Any]:
        """Mark item as DISMISSED."""
        item = self._items.get(queue_item_id)
        if not item:
            return {"status": "NOT_FOUND", "queue_item_id": queue_item_id}
        item.status        = QueueItemStatus.DISMISSED.value
        item.dismissed_at  = _now_utc()
        item.dismiss_reason = reason
        self._append_history(queue_item_id, "dismiss", reason)
        return {"status": "OK", "queue_item_id": queue_item_id, "new_status": item.status}

    def block(self, queue_item_id: str, reason: str = "") -> Dict[str, Any]:
        """Mark item as BLOCKED."""
        item = self._items.get(queue_item_id)
        if not item:
            return {"status": "NOT_FOUND", "queue_item_id": queue_item_id}
        item.status       = QueueItemStatus.BLOCKED.value
        item.blocked_at   = _now_utc()
        item.block_reason = reason
        self._append_history(queue_item_id, "block", reason)
        return {"status": "OK", "queue_item_id": queue_item_id, "new_status": item.status}

    def reopen(self, queue_item_id: str, reason: str = "") -> Dict[str, Any]:
        """Reopen a COMPLETED/DISMISSED/BLOCKED item."""
        item = self._items.get(queue_item_id)
        if not item:
            return {"status": "NOT_FOUND", "queue_item_id": queue_item_id}
        item.status        = QueueItemStatus.OPEN.value
        item.reopen_reason = reason
        self._append_history(queue_item_id, "reopen", reason)
        return {"status": "OK", "queue_item_id": queue_item_id, "new_status": item.status}

    def refresh_item(self, queue_item_id: str) -> Optional[ReplayReviewQueueItem]:
        """Return current state of an item."""
        return self._items.get(queue_item_id)

    def deduplicate(self) -> int:
        """Remove duplicate open items for the same session+type. Returns removed count."""
        seen: set = set()
        to_remove = []
        for qid, item in self._items.items():
            key = (item.session_id, item.queue_type)
            if key in seen and item.status == QueueItemStatus.OPEN.value:
                to_remove.append(qid)
            seen.add(key)
        for qid in to_remove:
            del self._items[qid]
        return len(to_remove)

    def history(self) -> List[Dict[str, Any]]:
        """Return append-only history."""
        return list(self._history)

    def summary(self) -> Dict[str, Any]:
        """Return queue summary counts."""
        items = list(self._items.values())
        by_status: Dict[str, int] = {}
        for item in items:
            by_status[item.status] = by_status.get(item.status, 0) + 1
        return {
            "total":         len(items),
            "open_count":    by_status.get(QueueItemStatus.OPEN.value, 0),
            "in_review":     by_status.get(QueueItemStatus.IN_REVIEW.value, 0),
            "completed":     by_status.get(QueueItemStatus.COMPLETED.value, 0),
            "dismissed":     by_status.get(QueueItemStatus.DISMISSED.value, 0),
            "blocked":       by_status.get(QueueItemStatus.BLOCKED.value, 0),
            "by_status":     by_status,
            "research_only": True,
            "no_real_orders": True,
            "auto_confirm_on_complete": False,
            "auto_reveal_on_complete":  False,
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _append_history(self, queue_item_id: str, action: str, note: str) -> None:
        self._history.append({
            "queue_item_id": queue_item_id,
            "action":        action,
            "note":          note,
            "timestamp":     _now_utc(),
            "research_only": True,
        })
