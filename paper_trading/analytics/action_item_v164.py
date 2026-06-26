"""
paper_trading/analytics/action_item_v164.py — Action Item Management v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Append-only history. Actor+reason required. No auto-complete. No auto-deploy.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from paper_trading.analytics.enums_v164 import ActionItemStatus, VALID_ACTION_ITEM_TRANSITIONS
from paper_trading.analytics.models_v164 import ActionItem, ActionItemHistoryEntry

NO_REAL_ORDERS = True
PAPER_ONLY = True
AUTO_COMPLETE_ENABLED = False
AUTO_DEPLOYMENT_ENABLED = False
STRATEGY_DEPLOYMENT_ENABLED = False


class ActionItemManager:
    """
    Manages action items with append-only history.
    All transitions require actor + reason.
    Cannot auto-complete. Cannot deploy strategy.
    """

    def __init__(self) -> None:
        self._items: List[ActionItem] = []

    def create(
        self,
        review_id: str,
        category: str,
        title: str,
        description: str,
        owner: str,
        priority: str,
        due_date: Optional[datetime] = None,
        evidence_refs: Optional[List[str]] = None,
    ) -> ActionItem:
        now = datetime.now(tz=timezone.utc)
        item = ActionItem(
            action_item_id=str(uuid.uuid4()),
            review_id=review_id,
            category=category,
            title=title,
            description=description,
            owner=owner,
            status=ActionItemStatus.OPEN,
            priority=priority,
            due_date=due_date,
            evidence_refs=evidence_refs or [],
            created_at=now,
            updated_at=now,
            history=[],
        )
        self._items.append(item)
        return item

    def transition(
        self,
        action_item_id: str,
        to_status: ActionItemStatus,
        actor: str,
        reason: str,
    ) -> ActionItem:
        item = self._get(action_item_id)
        if item is None:
            raise KeyError(f"ActionItem {action_item_id} not found")
        now = datetime.now(tz=timezone.utc)
        item.transition(to_status, actor, reason, now)
        return item

    def list_all(self) -> List[ActionItem]:
        return list(self._items)

    def get(self, action_item_id: str) -> Optional[ActionItem]:
        return self._get(action_item_id)

    def list_by_status(self, status: ActionItemStatus) -> List[ActionItem]:
        return [i for i in self._items if i.status == status]

    def _get(self, action_item_id: str) -> Optional[ActionItem]:
        for item in self._items:
            if item.action_item_id == action_item_id:
                return item
        return None


__all__ = ["ActionItemManager", "AUTO_COMPLETE_ENABLED", "AUTO_DEPLOYMENT_ENABLED"]
