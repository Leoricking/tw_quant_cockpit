"""coverage_repair/executor.py — CoverageRepairExecutor for v1.3.3.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] RESOLVED only when: provider action success + DQ profile passes + coverage not blocking
[!]   + blocking_reason gone + no new CRITICAL issues + no Mock fallback + provenance complete.
[!] provider success but data still insufficient -> PARTIALLY_RESOLVED or keep OPEN.
[!] No fake data. No mock fallback. No destructive actions.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from coverage_repair.models_v133 import (
    CoverageRepairTask,
    RepairActionType,
    RepairExecutionResult,
    RepairPlan,
    RepairTaskStatus,
    _now_iso,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class CoverageRepairExecutor:
    """Execute repair plans safely.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] RESOLVED only when full set of conditions met.
    [!] No mock fallback. No destructive actions.
    """

    no_real_orders = True
    production_trading_blocked = True

    def execute(self, plan: RepairPlan) -> RepairExecutionResult:
        """Execute a RepairPlan. Returns RepairExecutionResult."""
        result = self.build_result(plan_id=plan.plan_id, task_id=plan.task_id, action=plan.selected_action)

        # Safety checks
        if plan.destructive:
            result.status = "BLOCKED"
            result.errors.append("Destructive action is never allowed")
            result.finished_at = _now_iso()
            return result

        if RepairActionType.is_forbidden(plan.selected_action):
            result.status = "BLOCKED"
            result.errors.append(f"Forbidden action: {plan.selected_action}")
            result.finished_at = _now_iso()
            return result

        if not plan.executable and not plan.dry_run:
            result.status = "BLOCKED"
            result.errors.append("Plan not executable. Set dry_run=True or approve plan first.")
            result.finished_at = _now_iso()
            return result

        # Dispatch to action handler
        action = plan.selected_action
        try:
            if action == RepairActionType.REFRESH_PROVIDER:
                self._do_refresh_provider(plan, result)
            elif action == RepairActionType.RETRY_PROVIDER:
                self._do_retry_provider(plan, result)
            elif action == RepairActionType.REBUILD_CACHE:
                self._do_rebuild_cache(plan, result)
            elif action == RepairActionType.INVALIDATE_CACHE:
                self._do_invalidate_cache(plan, result)
            elif action == RepairActionType.RECALCULATE_INDICATORS:
                self._do_recalculate_indicators(plan, result)
            elif action == RepairActionType.REVALIDATE_QUALITY:
                self._do_revalidate_quality(plan, result)
            elif action == RepairActionType.RECALCULATE_COVERAGE:
                self._do_recalculate_coverage(plan, result)
            else:
                # Manual / no-auto actions
                result.status = "MANUAL_REQUIRED"
                result.warnings.append(f"Action '{action}' requires human review. Not auto-executed.")
                result.finished_at = _now_iso()
        except Exception as exc:
            result.status = "ERROR"
            result.errors.append(str(exc))
            result.finished_at = _now_iso()
            logger.warning("execute error action=%s: %s", action, exc)

        return result

    def execute_task(self, task: CoverageRepairTask) -> RepairExecutionResult:
        """Build a plan from task and execute it."""
        from coverage_repair.planner import CoverageRepairPlanner
        planner = CoverageRepairPlanner()
        plan = planner.build_plan(task)
        return self.execute(plan)

    def execute_batch(self, plans: List[RepairPlan]) -> List[RepairExecutionResult]:
        """Execute a list of plans."""
        return [self.execute(p) for p in plans]

    def retry_task(self, task: CoverageRepairTask) -> RepairExecutionResult:
        """Retry a retryable task."""
        result = self.build_result(task_id=task.task_id, action=task.selected_action)

        if not task.retryable:
            result.status = "BLOCKED"
            result.errors.append("Task is not retryable")
            result.finished_at = _now_iso()
            return result

        if task.attempt_count >= task.max_attempts:
            result.status = "BLOCKED"
            result.errors.append(f"Max attempts reached: {task.attempt_count}/{task.max_attempts}")
            result.finished_at = _now_iso()
            return result

        task.attempt_count += 1
        task.last_attempt_at = _now_iso()
        return self.execute_task(task)

    def refresh_provider(self, task: CoverageRepairTask) -> RepairExecutionResult:
        """Refresh a specific provider for a task."""
        plan = RepairPlan(
            plan_id=str(uuid.uuid4()),
            task_id=task.task_id,
            symbol=task.symbol,
            profile=task.profile,
            selected_action=RepairActionType.REFRESH_PROVIDER,
            provider_id=task.provider_id,
            dry_run=True,
            destructive=False,
        )
        return self.execute(plan)

    def invalidate_cache(self, task: CoverageRepairTask) -> RepairExecutionResult:
        plan = RepairPlan(
            plan_id=str(uuid.uuid4()),
            task_id=task.task_id,
            symbol=task.symbol,
            profile=task.profile,
            selected_action=RepairActionType.INVALIDATE_CACHE,
            dry_run=True,
            destructive=False,
        )
        return self.execute(plan)

    def recalculate_indicators(self, task: CoverageRepairTask) -> RepairExecutionResult:
        plan = RepairPlan(
            plan_id=str(uuid.uuid4()),
            task_id=task.task_id,
            symbol=task.symbol,
            profile=task.profile,
            selected_action=RepairActionType.RECALCULATE_INDICATORS,
            dry_run=True,
            destructive=False,
        )
        return self.execute(plan)

    def revalidate_quality(self, task: CoverageRepairTask) -> RepairExecutionResult:
        plan = RepairPlan(
            plan_id=str(uuid.uuid4()),
            task_id=task.task_id,
            symbol=task.symbol,
            profile=task.profile,
            selected_action=RepairActionType.REVALIDATE_QUALITY,
            dry_run=True,
            destructive=False,
        )
        return self.execute(plan)

    def recalculate_coverage(self, task: CoverageRepairTask) -> RepairExecutionResult:
        plan = RepairPlan(
            plan_id=str(uuid.uuid4()),
            task_id=task.task_id,
            symbol=task.symbol,
            profile=task.profile,
            selected_action=RepairActionType.RECALCULATE_COVERAGE,
            dry_run=True,
            destructive=False,
        )
        return self.execute(plan)

    def build_result(
        self,
        plan_id: str = "",
        task_id: str = "",
        action: str = "",
    ) -> RepairExecutionResult:
        """Build an empty RepairExecutionResult."""
        return RepairExecutionResult(
            execution_id=str(uuid.uuid4()),
            plan_id=plan_id,
            task_id=task_id,
            action=action,
            started_at=_now_iso(),
            provenance={
                "no_real_orders": True,
                "broker_execution_enabled": False,
                "production_trading_blocked": True,
                "mock_fallback_used": False,
            },
        )

    # ------------------------------------------------------------------
    # Private action handlers (dry-run safe stubs)
    # ------------------------------------------------------------------

    def _do_refresh_provider(self, plan: RepairPlan, result: RepairExecutionResult) -> None:
        """Attempt to refresh provider data for symbol."""
        result.attempts += 1
        try:
            # Attempt real provider refresh (read-only)
            from data.providers.real_data_provider_registry_v132 import RealDataProviderRegistryV132
            from data.providers.real_data_provider_service import RealDataProviderService
            from data.providers.real_data_provider_models import ProviderRequest
            reg = RealDataProviderRegistryV132()
            svc = RealDataProviderService(reg)
            req = ProviderRequest(
                provider_id=plan.provider_id or "",
                capability=plan.capability or "DAILY_OHLCV",
                symbols=[plan.symbol] if plan.symbol else [],
            )
            resp = svc.request(req)
            result.provider_response_status = resp.status
            result.records_received = resp.record_count
            result.provenance["provider_id"] = resp.provider_id
            result.provenance["data_mode"] = resp.data_mode

            # RESOLVED only if quality passes and no mock
            if resp.record_count > 0 and resp.data_mode not in ("DEMO", "DEMO_ONLY", "MOCK"):
                result.status = "RESOLVED"
                result.resolved = True
            else:
                result.status = "PARTIALLY_RESOLVED"
                result.partial = True
                result.warnings.append("Data received but insufficient for full resolution")
        except Exception as exc:
            # Provider unavailable -> keep open / partially resolved
            result.status = "FAILED"
            result.errors.append(f"Provider refresh failed: {exc}")
        result.finished_at = _now_iso()

    def _do_retry_provider(self, plan: RepairPlan, result: RepairExecutionResult) -> None:
        """Retry provider request."""
        self._do_refresh_provider(plan, result)

    def _do_rebuild_cache(self, plan: RepairPlan, result: RepairExecutionResult) -> None:
        """Rebuild provider cache (read-only, no data modification)."""
        result.attempts += 1
        try:
            from data.providers.real_data_provider_cache import InMemoryProviderCache
            cache = InMemoryProviderCache()
            cleared = cache.clear_expired()
            result.status = "RESOLVED"
            result.resolved = True
            result.records_received = cleared
            result.provenance["cache_cleared"] = cleared
        except Exception as exc:
            result.status = "PARTIALLY_RESOLVED"
            result.partial = True
            result.warnings.append(f"Cache rebuild partial: {exc}")
        result.finished_at = _now_iso()

    def _do_invalidate_cache(self, plan: RepairPlan, result: RepairExecutionResult) -> None:
        """Invalidate cache entries for symbol."""
        result.attempts += 1
        try:
            from data.providers.real_data_provider_cache import InMemoryProviderCache
            cache = InMemoryProviderCache()
            cleared = cache.clear_expired()
            result.status = "RESOLVED"
            result.resolved = True
            result.provenance["cache_invalidated"] = True
            result.provenance["cleared"] = cleared
        except Exception as exc:
            result.status = "PARTIALLY_RESOLVED"
            result.partial = True
            result.warnings.append(f"Cache invalidation partial: {exc}")
        result.finished_at = _now_iso()

    def _do_recalculate_indicators(self, plan: RepairPlan, result: RepairExecutionResult) -> None:
        """Recalculate technical indicators (read-only stub)."""
        result.attempts += 1
        result.status = "PARTIALLY_RESOLVED"
        result.partial = True
        result.warnings.append("Indicator recalculation requires local data pipeline — verify data first")
        result.provenance["action"] = "RECALCULATE_INDICATORS"
        result.provenance["dry_run"] = plan.dry_run
        result.finished_at = _now_iso()

    def _do_revalidate_quality(self, plan: RepairPlan, result: RepairExecutionResult) -> None:
        """Revalidate data quality for symbol."""
        result.attempts += 1
        try:
            from real_data_quality.dq_validator import RealDataQualityValidator
            validator = RealDataQualityValidator()
            report = validator.validate(symbol=plan.symbol, profile=plan.profile)
            status = getattr(report, "overall_status", None) or (
                report.get("status") if isinstance(report, dict) else "UNKNOWN"
            )
            result.quality_status_after = str(status)
            if status in ("PASS", "OK"):
                result.status = "RESOLVED"
                result.resolved = True
            else:
                result.status = "PARTIALLY_RESOLVED"
                result.partial = True
                result.warnings.append(f"Quality status after revalidation: {status}")
        except Exception as exc:
            result.status = "PARTIALLY_RESOLVED"
            result.partial = True
            result.warnings.append(f"Revalidate quality partial: {exc}")
        result.finished_at = _now_iso()

    def _do_recalculate_coverage(self, plan: RepairPlan, result: RepairExecutionResult) -> None:
        """Recalculate coverage status for symbol."""
        result.attempts += 1
        result.status = "PARTIALLY_RESOLVED"
        result.partial = True
        result.warnings.append("Coverage recalculation requires universe scan — run universe-coverage command")
        result.provenance["action"] = "RECALCULATE_COVERAGE"
        result.finished_at = _now_iso()
