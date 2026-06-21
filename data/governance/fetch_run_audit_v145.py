"""
data/governance/fetch_run_audit_v145.py — Fetch Run Audit Service v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Invariants: records_written <= records_valid, requests_succeeded <= requests_executed.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from data.governance.models_v145 import FetchRunAudit

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class FetchRunAuditService:
    """
    Audit service for fetch runs.
    Enforces invariants: records_written <= records_valid, requests_succeeded <= requests_executed.
    """

    def __init__(self) -> None:
        self._runs: Dict[str, FetchRunAudit] = {}
        self._order: List[str] = []

    def create_run(
        self,
        provider_id: str,
        requested_by: str,
        mode: str,
        dry_run: bool = True,
        request_budget: int = 0,
    ) -> FetchRunAudit:
        fetch_run_id = str(uuid.uuid4())
        run = FetchRunAudit(
            fetch_run_id=fetch_run_id,
            provider_id=provider_id,
            requested_by=requested_by,
            mode=mode,
            dry_run=dry_run,
            planned_at=_now(),
            request_budget=request_budget,
            overall_status="PLANNED",
        )
        self._runs[fetch_run_id] = run
        self._order.append(fetch_run_id)
        return run

    def start_run(self, fetch_run_id: str) -> None:
        run = self._runs.get(fetch_run_id)
        if run is None:
            return
        run.started_at = _now()
        run.overall_status = "RUNNING"

    def record_request_outcome(
        self,
        fetch_run_id: str,
        status: str,
        records: int = 0,
        cache_hit: bool = False,
    ) -> None:
        run = self._runs.get(fetch_run_id)
        if run is None:
            return
        run.requests_executed += 1
        if status in ("COMPLETED", "SUCCESS"):
            run.requests_succeeded += 1
            run.records_received += records
            run.records_valid += records
        elif status == "FAILED":
            run.requests_failed += 1
        elif status == "RATE_LIMITED":
            run.requests_rate_limited += 1
        elif status == "QUOTA_BLOCKED":
            run.requests_quota_blocked += 1
        if cache_hit:
            run.cache_hits += 1

    def complete_run(
        self,
        fetch_run_id: str,
        database_updated: bool = False,
        lineage_created: int = 0,
    ) -> None:
        run = self._runs.get(fetch_run_id)
        if run is None:
            return
        run.finished_at = _now()
        run.database_updated = database_updated
        run.lineage_records_created = lineage_created
        if run.requests_failed > 0 and run.requests_succeeded > 0:
            run.partial_success = True
            run.overall_status = "PARTIAL_SUCCESS"
        elif run.requests_failed > 0 and run.requests_succeeded == 0:
            run.overall_status = "FAILED"
        else:
            run.overall_status = "SUCCESS"

    def fail_run(self, fetch_run_id: str, errors: Optional[List[str]] = None) -> None:
        run = self._runs.get(fetch_run_id)
        if run is None:
            return
        run.finished_at = _now()
        run.overall_status = "FAILED"
        if errors:
            run.errors.extend(errors)

    def cancel_run(self, fetch_run_id: str) -> None:
        run = self._runs.get(fetch_run_id)
        if run is None:
            return
        run.finished_at = _now()
        run.overall_status = "CANCELLED"
        run.cancellation_status = "CANCELLED"

    def get_run(self, fetch_run_id: str) -> Optional[FetchRunAudit]:
        return self._runs.get(fetch_run_id)

    def list_runs(
        self,
        provider_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        runs = [self._runs[rid] for rid in self._order]
        if provider_id:
            runs = [r for r in runs if r.provider_id == provider_id]
        return [r.to_dict() for r in runs[-limit:]]
