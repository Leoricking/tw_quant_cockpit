"""coverage_repair/query.py — CoverageRepairQueryService for v1.3.3.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from coverage_repair.models_v133 import (
    CoverageRepairTask,
    RepairTaskStatus,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class CoverageRepairQueryService:
    """Read-only query service for coverage repair tasks.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    no_real_orders = True
    production_trading_blocked = True

    def __init__(self, queue=None, store=None) -> None:
        """Accept optional queue and store for integration."""
        self._queue = queue
        self._store = store

    def _all_tasks(self) -> List[CoverageRepairTask]:
        if self._queue is not None:
            return self._queue.list_tasks()
        if self._store is not None:
            tasks = []
            for tid in self._store.list_task_ids():
                t = self._store.load_task(tid)
                if t is not None:
                    tasks.append(t)
            return tasks
        return []

    def get_task(self, task_id: str) -> Optional[CoverageRepairTask]:
        """Get a single task by ID."""
        if self._queue is not None:
            return self._queue.get_task(task_id)
        if self._store is not None:
            return self._store.load_task(task_id)
        return None

    def list_recent(self, limit: int = 20) -> List[CoverageRepairTask]:
        """Return most recently updated tasks (up to limit)."""
        tasks = self._all_tasks()
        tasks_sorted = sorted(tasks, key=lambda t: t.updated_at or "", reverse=True)
        return tasks_sorted[:limit]

    def list_open(self) -> List[CoverageRepairTask]:
        return [t for t in self._all_tasks() if t.status == RepairTaskStatus.OPEN]

    def list_resolved(self) -> List[CoverageRepairTask]:
        return [t for t in self._all_tasks() if t.status == RepairTaskStatus.RESOLVED]

    def list_failed(self) -> List[CoverageRepairTask]:
        return [t for t in self._all_tasks() if t.status == RepairTaskStatus.FAILED]

    def list_conflicts(self) -> List[CoverageRepairTask]:
        return [t for t in self._all_tasks() if t.status == RepairTaskStatus.CONFLICT_REVIEW]

    def list_waiting_source(self) -> List[CoverageRepairTask]:
        return [t for t in self._all_tasks() if t.status == RepairTaskStatus.WAITING_SOURCE]

    def list_waiting_auth(self) -> List[CoverageRepairTask]:
        return [t for t in self._all_tasks() if t.status == RepairTaskStatus.WAITING_AUTH]

    def list_by_symbol(self, symbol: str) -> List[CoverageRepairTask]:
        return [t for t in self._all_tasks() if t.symbol == symbol]

    def list_by_universe(self, universe_id: str) -> List[CoverageRepairTask]:
        return [t for t in self._all_tasks() if t.universe_id == universe_id]

    def list_by_provider(self, provider_id: str) -> List[CoverageRepairTask]:
        return [t for t in self._all_tasks() if t.provider_id == provider_id]

    def list_by_profile(self, profile: str) -> List[CoverageRepairTask]:
        return [t for t in self._all_tasks() if t.profile == profile]

    def summarize(self) -> Dict[str, Any]:
        """Return a summary dict of all tasks."""
        tasks = self._all_tasks()
        total = len(tasks)
        by_status: Dict[str, int] = {}
        by_priority: Dict[str, int] = {}
        by_issue: Dict[str, int] = {}
        for t in tasks:
            by_status[t.status] = by_status.get(t.status, 0) + 1
            by_priority[t.priority] = by_priority.get(t.priority, 0) + 1
            by_issue[t.issue_type] = by_issue.get(t.issue_type, 0) + 1
        return {
            "total": total,
            "by_status": by_status,
            "by_priority": by_priority,
            "by_issue_type": by_issue,
            "open": by_status.get(RepairTaskStatus.OPEN, 0),
            "blocked": by_status.get(RepairTaskStatus.BLOCKED, 0),
            "resolved": by_status.get(RepairTaskStatus.RESOLVED, 0),
            "failed": by_status.get(RepairTaskStatus.FAILED, 0),
            "conflict_review": by_status.get(RepairTaskStatus.CONFLICT_REVIEW, 0),
            "waiting_source": by_status.get(RepairTaskStatus.WAITING_SOURCE, 0),
            "waiting_auth": by_status.get(RepairTaskStatus.WAITING_AUTH, 0),
            "no_real_orders": True,
            "production_trading_blocked": True,
            "schema_version": "1.3.3",
        }
