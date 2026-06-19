"""data_freshness/repair_integration_v134.py — v1.3.4 Freshness-Repair Integration.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No auto execution, no auto refresh, no auto download.
[!] Repair tasks only created when create_task=True (explicit).
[!] Uses CoverageRepairQueue dedup — no duplicate tasks.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from data_freshness.models_v134 import FreshnessRecord, FreshnessStatus, FreshnessAlert

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FRESHNESS_AUTO_REPAIR_ENABLED = False
FRESHNESS_AUTO_REFRESH_ENABLED = False

# Mapping from FreshnessStatus -> RepairIssueType string
_STATUS_TO_ISSUE: Dict[str, str] = {
    FreshnessStatus.STALE:               "STALE_DATA",
    FreshnessStatus.CRITICALLY_STALE:    "STALE_DATA",
    FreshnessStatus.NEVER_RECEIVED:      "MISSING_DATA",
    FreshnessStatus.PROVIDER_DELAYED:    "UNAVAILABLE_SOURCE",
    FreshnessStatus.PROVIDER_UNAVAILABLE:"UNAVAILABLE_SOURCE",
    FreshnessStatus.FUTURE_TIMESTAMP:    "BLOCKED_DATA",
    FreshnessStatus.INVALID_TIMESTAMP:   "INVALID_SCHEMA",
    # Legacy statuses from v1.1.x
    "STALE":                             "STALE_DATA",
    "CACHE_STALE":                       "CACHE_STALE",
    "INTERRUPTED":                       "UNAVAILABLE_SOURCE",
    "MISSING":                           "MISSING_DATA",
}


class FreshnessRepairIntegration:
    """Bridge between freshness status and coverage repair workflow.

    [!] Research Only. No auto-repair, no auto-execution.
    [!] create_repair_task() only queues a task when create_task=True.
    """

    def map_freshness_to_repair_issue(self, freshness_status: str) -> str:
        """Map a FreshnessStatus string to a RepairIssueType string."""
        return _STATUS_TO_ISSUE.get(freshness_status, "UNKNOWN")

    def create_repair_task(
        self,
        record: FreshnessRecord,
        queue=None,
        create_task: bool = False,
    ) -> Optional[str]:
        """Create a repair task for a stale record.

        [!] Only creates task when create_task=True.
        [!] Uses CoverageRepairQueue dedup — does not create duplicate tasks.
        [!] Returns task_id string or None.
        """
        if not create_task:
            logger.debug(
                "create_repair_task: create_task=False — not creating task for %s/%s",
                record.symbol, record.dataset_type,
            )
            return None

        issue_type = self.map_freshness_to_repair_issue(record.freshness_status)

        if queue is None:
            try:
                from coverage_repair.queue import CoverageRepairQueue
                queue = CoverageRepairQueue()
            except ImportError:
                logger.warning("CoverageRepairQueue not available; cannot create repair task")
                return None

        try:
            from coverage_repair.models_v133 import CoverageRepairTask, RepairTaskStatus
            import uuid
            from data_freshness.models_v134 import _now_iso

            task_id = str(uuid.uuid4())
            task = CoverageRepairTask(
                task_id=task_id,
                symbol=record.symbol,
                market=record.market or "TWSE",
                dataset_type=record.dataset_type,
                issue_type=issue_type,
                status=RepairTaskStatus.OPEN,
                priority="HIGH" if FreshnessStatus.is_blocking(record.freshness_status) else "NORMAL",
                created_at=_now_iso(),
                source="freshness_monitor_v134",
                metadata={
                    "freshness_status": record.freshness_status,
                    "age_seconds": record.age_seconds,
                    "policy_id": record.policy_id,
                },
            )
            queue.add(task)
            logger.info("Created repair task %s for %s/%s", task_id, record.symbol, record.dataset_type)
            return task_id
        except Exception as exc:
            logger.warning("create_repair_task: error: %s", exc)
            return None

    def attach_repair_task_id(self, alert: FreshnessAlert, task_id: str) -> None:
        """Attach a repair task_id to an alert."""
        alert.repair_task_id = task_id
        alert.metadata["repair_task_id"] = task_id

    def revalidate_after_repair(
        self,
        record: FreshnessRecord,
        task: Any,
    ) -> FreshnessRecord:
        """Re-evaluate freshness after a repair task has run.

        [!] Does not auto-execute repair — task must have already run externally.
        """
        from data_freshness.evaluator_v134 import DataFreshnessEvaluator
        evaluator = DataFreshnessEvaluator()
        new_record = evaluator.evaluate(
            symbol=record.symbol,
            dataset_type=record.dataset_type,
            observed_ts=record.observed_timestamp,
            source_ts=record.source_timestamp,
            fetched_at=record.fetched_at,
            provider_id=record.provider_id,
            data_mode=record.data_mode,
            market=record.market,
        )
        new_record.metadata["revalidated_after_task"] = str(getattr(task, "task_id", ""))
        return new_record

    def summarize_repair_candidates(
        self, records: List[FreshnessRecord]
    ) -> List[Dict[str, Any]]:
        """Return list of repair candidate dicts for actionable records."""
        candidates = []
        for rec in records:
            if rec.freshness_status not in (
                FreshnessStatus.FRESH, FreshnessStatus.NEAR_STALE,
                FreshnessStatus.MARKET_CLOSED_VALID, FreshnessStatus.NON_TRADING_DAY_VALID,
                FreshnessStatus.DEMO_ONLY, FreshnessStatus.UNKNOWN,
            ):
                issue = self.map_freshness_to_repair_issue(rec.freshness_status)
                candidates.append({
                    "symbol": rec.symbol,
                    "dataset_type": rec.dataset_type,
                    "freshness_status": rec.freshness_status,
                    "repair_issue_type": issue,
                    "age_seconds": rec.age_seconds,
                    "blocks_analysis": rec.blocks_analysis,
                    "priority": "HIGH" if FreshnessStatus.is_blocking(rec.freshness_status) else "NORMAL",
                    "note": "NOT_REAL_DATA" if rec.data_mode in ("MOCK", "DEMO_ONLY") else "REAL_DATA",
                })
        return candidates
