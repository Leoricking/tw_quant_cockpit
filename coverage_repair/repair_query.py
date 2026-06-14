"""
coverage_repair/repair_query.py — RepairQuery for TW Quant Cockpit v1.1.2.

Read-only queries over saved repair data.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional, Dict

from coverage_repair.coverage_repair_schema import (
    REPAIR_STATUS_FAILED, REPAIR_STATUS_BLOCKED,
    REPAIR_STATUS_MANUAL, REPAIR_STATUS_OK,
    ACTION_MANUAL_REVIEW, ACTION_SOURCE_REQUIRED,
    PRIORITY_P0, PRIORITY_P1,
)

logger = logging.getLogger(__name__)


class RepairQuery:
    """Read-only queries over saved repair data.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def __init__(self, output_dir: Optional[str] = None) -> None:
        from coverage_repair.repair_store import RepairStore, DEFAULT_OUTPUT_DIR
        self._store = RepairStore(output_dir=output_dir or DEFAULT_OUTPUT_DIR)

    def list_failed(self) -> List[dict]:
        """All failed repair results from latest summary."""
        summary = self._store.load_latest_summary()
        if summary is None:
            return []
        return [r.to_dict() for r in summary.results if r.status == REPAIR_STATUS_FAILED]

    def list_blocked(self) -> List[dict]:
        """All blocked repair results from latest summary."""
        summary = self._store.load_latest_summary()
        if summary is None:
            return []
        return [r.to_dict() for r in summary.results if r.status == REPAIR_STATUS_BLOCKED]

    def list_manual_review(self) -> List[dict]:
        """All manual review results from latest summary."""
        summary = self._store.load_latest_summary()
        if summary is None:
            return []
        return [r.to_dict() for r in summary.results if r.status == REPAIR_STATUS_MANUAL]

    def list_succeeded(self) -> List[dict]:
        """All succeeded repair results from latest summary."""
        summary = self._store.load_latest_summary()
        if summary is None:
            return []
        return [r.to_dict() for r in summary.results if r.status == REPAIR_STATUS_OK]

    def list_source_required(self) -> List[dict]:
        """All tasks requiring source data from latest plan."""
        plan = self._store.load_latest_plan()
        if plan is None:
            return []
        return [t.to_dict() for t in plan.tasks if t.action == ACTION_SOURCE_REQUIRED]

    def list_critical(self) -> List[dict]:
        """All P0/P1 tasks from latest plan."""
        plan = self._store.load_latest_plan()
        if plan is None:
            return []
        return [t.to_dict() for t in plan.tasks if t.priority in (PRIORITY_P0, PRIORITY_P1)]

    def get_latest_summary(self) -> Optional[dict]:
        summary = self._store.load_latest_summary()
        return summary.to_dict() if summary else None

    def get_latest_plan(self) -> Optional[dict]:
        plan = self._store.load_latest_plan()
        return plan.to_dict() if plan else None

    def summarize_status(self) -> Dict[str, object]:
        """Return summary dict of latest repair batch."""
        summary = self._store.load_latest_summary()
        if summary is None:
            return {"status": "no_data", "research_only": True, "no_real_orders": True}
        return {
            "total_tasks":   summary.total_tasks,
            "succeeded":     summary.succeeded,
            "partial":       summary.partial,
            "failed":        summary.failed,
            "skipped":       summary.skipped,
            "blocked":       summary.blocked,
            "manual_review": summary.manual_review,
            "dry_run":       summary.dry_run,
            "research_only": True,
            "no_real_orders": True,
        }
