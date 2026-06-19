"""coverage_repair/queue.py — CoverageRepairQueue for v1.3.3.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Invalid status transitions raise ValueError.
[!] Task errors do not corrupt queue.
[!] History preserved (append-only log).
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from coverage_repair.models_v133 import (
    CoverageRepairTask,
    RepairTaskStatus,
    _now_iso,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class CoverageRepairQueue:
    """In-memory coverage repair task queue with optional JSON persistence.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Invalid transitions raise ValueError.
    [!] Duplicate OPEN tasks (same dedup_key) are not re-added.
    """

    no_real_orders = True
    production_trading_blocked = True

    def __init__(self, persist_path: Optional[str] = None) -> None:
        self._tasks: Dict[str, CoverageRepairTask] = {}
        self._history: List[Dict[str, Any]] = []  # append-only
        self._claimed: set = set()
        self._persist_path = persist_path
        if persist_path and os.path.exists(persist_path):
            self._load_from_file(persist_path)

    # ------------------------------------------------------------------
    # Add / dedup
    # ------------------------------------------------------------------

    def add_task(self, task: CoverageRepairTask) -> bool:
        """Add task to queue. Returns False if duplicate OPEN task exists."""
        try:
            dedup = task.dedup_key or task.build_dedup_key()
            task.dedup_key = dedup
            # Check for duplicate OPEN tasks
            for existing in self._tasks.values():
                if (existing.dedup_key == dedup and
                        existing.status not in (RepairTaskStatus.RESOLVED,
                                                RepairTaskStatus.CANCELLED,
                                                RepairTaskStatus.IGNORED)):
                    return False
            task.updated_at = _now_iso()
            self._tasks[task.task_id] = task
            self._append_history("add_task", task.task_id, task.status, "")
            self._persist()
            return True
        except Exception as exc:
            logger.warning("add_task error: %s", exc)
            return False

    def add_tasks(self, tasks: List[CoverageRepairTask]) -> Dict[str, int]:
        """Add multiple tasks. Returns {'added': N, 'skipped': M}."""
        added = 0
        skipped = 0
        for t in tasks:
            if self.add_task(t):
                added += 1
            else:
                skipped += 1
        return {"added": added, "skipped": skipped}

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def get_task(self, task_id: str) -> Optional[CoverageRepairTask]:
        return self._tasks.get(task_id)

    def list_tasks(self) -> List[CoverageRepairTask]:
        return list(self._tasks.values())

    def filter_tasks(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        symbol: Optional[str] = None,
        profile: Optional[str] = None,
        issue_type: Optional[str] = None,
    ) -> List[CoverageRepairTask]:
        result = []
        for t in self._tasks.values():
            if status and t.status != status:
                continue
            if priority and t.priority != priority:
                continue
            if symbol and t.symbol != symbol:
                continue
            if profile and t.profile != profile:
                continue
            if issue_type and t.issue_type != issue_type:
                continue
            result.append(t)
        return result

    def list_open(self) -> List[CoverageRepairTask]:
        return self.filter_tasks(status=RepairTaskStatus.OPEN)

    def list_blocked(self) -> List[CoverageRepairTask]:
        return self.filter_tasks(status=RepairTaskStatus.BLOCKED)

    def list_retryable(self) -> List[CoverageRepairTask]:
        return [t for t in self._tasks.values() if t.retryable and t.status in (
            RepairTaskStatus.OPEN, RepairTaskStatus.READY_TO_RETRY, RepairTaskStatus.FAILED
        )]

    def list_by_symbol(self, symbol: str) -> List[CoverageRepairTask]:
        return self.filter_tasks(symbol=symbol)

    def list_by_profile(self, profile: str) -> List[CoverageRepairTask]:
        return self.filter_tasks(profile=profile)

    def list_by_priority(self, priority: str) -> List[CoverageRepairTask]:
        return self.filter_tasks(priority=priority)

    def list_by_status(self, status: str) -> List[CoverageRepairTask]:
        return self.filter_tasks(status=status)

    # ------------------------------------------------------------------
    # Claim / release
    # ------------------------------------------------------------------

    def claim_task(self, task_id: str) -> bool:
        """Claim a task for processing (marks IN_PROGRESS)."""
        task = self._tasks.get(task_id)
        if task is None:
            return False
        if task_id in self._claimed:
            return False
        try:
            self._transition(task, RepairTaskStatus.IN_PROGRESS, "claimed")
            self._claimed.add(task_id)
            return True
        except ValueError:
            return False

    def release_task(self, task_id: str) -> bool:
        """Release a claimed task back to OPEN."""
        task = self._tasks.get(task_id)
        if task is None:
            return False
        self._claimed.discard(task_id)
        try:
            self._transition(task, RepairTaskStatus.OPEN, "released")
            return True
        except ValueError:
            return False

    # ------------------------------------------------------------------
    # Status updates
    # ------------------------------------------------------------------

    def update_status(self, task_id: str, new_status: str, reason: str = "") -> bool:
        """Update task status. Raises ValueError on invalid transition."""
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")
        self._transition(task, new_status, reason)
        return True

    def mark_resolved(self, task_id: str, reason: str = "") -> bool:
        task = self._tasks.get(task_id)
        if task is None:
            return False
        self._transition(task, RepairTaskStatus.RESOLVED, reason)
        task.resolved_at = _now_iso()
        task.resolution_reason = reason
        self._persist()
        return True

    def mark_partial(self, task_id: str, reason: str = "") -> bool:
        task = self._tasks.get(task_id)
        if task is None:
            return False
        self._transition(task, RepairTaskStatus.PARTIALLY_RESOLVED, reason)
        self._persist()
        return True

    def mark_failed(self, task_id: str, reason: str = "") -> bool:
        task = self._tasks.get(task_id)
        if task is None:
            return False
        self._transition(task, RepairTaskStatus.FAILED, reason)
        self._persist()
        return True

    def mark_ignored(self, task_id: str, reason: str = "") -> bool:
        task = self._tasks.get(task_id)
        if task is None:
            return False
        self._transition(task, RepairTaskStatus.IGNORED, reason)
        self._persist()
        return True

    def cancel_task(self, task_id: str, reason: str = "") -> bool:
        task = self._tasks.get(task_id)
        if task is None:
            return False
        self._transition(task, RepairTaskStatus.CANCELLED, reason)
        self._persist()
        return True

    def reopen_task(self, task_id: str, reason: str = "") -> bool:
        task = self._tasks.get(task_id)
        if task is None:
            return False
        self._transition(task, RepairTaskStatus.OPEN, reason)
        self._persist()
        return True

    # ------------------------------------------------------------------
    # Summary / maintenance
    # ------------------------------------------------------------------

    def summarize(self) -> Dict[str, Any]:
        total = len(self._tasks)
        by_status: Dict[str, int] = {}
        by_priority: Dict[str, int] = {}
        for t in self._tasks.values():
            by_status[t.status] = by_status.get(t.status, 0) + 1
            by_priority[t.priority] = by_priority.get(t.priority, 0) + 1
        return {
            "total": total,
            "by_status": by_status,
            "by_priority": by_priority,
            "open": by_status.get(RepairTaskStatus.OPEN, 0),
            "in_progress": by_status.get(RepairTaskStatus.IN_PROGRESS, 0),
            "blocked": by_status.get(RepairTaskStatus.BLOCKED, 0),
            "resolved": by_status.get(RepairTaskStatus.RESOLVED, 0),
            "failed": by_status.get(RepairTaskStatus.FAILED, 0),
            "history_events": len(self._history),
            "no_real_orders": True,
            "production_trading_blocked": True,
        }

    def prune_resolved(self) -> int:
        """Remove RESOLVED and CANCELLED tasks. Returns count removed."""
        to_remove = [tid for tid, t in self._tasks.items()
                     if t.status in (RepairTaskStatus.RESOLVED, RepairTaskStatus.CANCELLED)]
        for tid in to_remove:
            del self._tasks[tid]
        if to_remove:
            self._persist()
        return len(to_remove)

    def rebuild_from_scan(self, tasks: List[CoverageRepairTask]) -> Dict[str, int]:
        """Replace open tasks with a new scan result. Returns added/skipped."""
        added = 0
        skipped = 0
        for t in tasks:
            if self.add_task(t):
                added += 1
            else:
                skipped += 1
        return {"added": added, "skipped": skipped}

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": "1.3.3",
            "tasks": {tid: t.to_dict() for tid, t in self._tasks.items()},
            "history": self._history,
            "no_real_orders": True,
            "production_trading_blocked": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any], persist_path: Optional[str] = None) -> "CoverageRepairQueue":
        q = cls(persist_path=None)
        for tid, tdata in (d.get("tasks") or {}).items():
            try:
                t = CoverageRepairTask.from_dict(tdata)
                q._tasks[tid] = t
            except Exception as exc:
                logger.warning("from_dict task %s error: %s", tid, exc)
        q._history = list(d.get("history") or [])
        q._persist_path = persist_path
        return q

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _transition(self, task: CoverageRepairTask, new_status: str, reason: str) -> None:
        old_status = task.status
        if not RepairTaskStatus.can_transition(old_status, new_status):
            raise ValueError(
                f"Invalid transition {old_status} -> {new_status} for task {task.task_id}"
            )
        task.status = new_status
        task.updated_at = _now_iso()
        self._append_history("status_change", task.task_id, new_status, reason, old_status)

    def _append_history(self, event: str, task_id: str, status: str, reason: str,
                        old_status: str = "") -> None:
        self._history.append({
            "event": event,
            "task_id": task_id,
            "status": status,
            "old_status": old_status,
            "reason": reason,
            "at": _now_iso(),
        })

    def _persist(self) -> None:
        if not self._persist_path:
            return
        try:
            os.makedirs(os.path.dirname(self._persist_path), exist_ok=True)
            with open(self._persist_path, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as exc:
            logger.warning("queue persist error: %s", exc)

    def _load_from_file(self, path: str) -> None:
        try:
            with open(path, encoding="utf-8") as f:
                d = json.load(f)
            for tid, tdata in (d.get("tasks") or {}).items():
                try:
                    t = CoverageRepairTask.from_dict(tdata)
                    self._tasks[tid] = t
                except Exception as exc:
                    logger.warning("load task %s error: %s", tid, exc)
            self._history = list(d.get("history") or [])
        except Exception as exc:
            logger.warning("queue load from file error: %s", exc)
