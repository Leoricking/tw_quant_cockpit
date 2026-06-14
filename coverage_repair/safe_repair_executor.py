"""
coverage_repair/safe_repair_executor.py — Safe execution of coverage repair tasks.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] allow_write=False default. dry_run=True default.
[!] INVALID OHLC: never auto-modify. CONFLICT: never auto-overwrite.
[!] Synthetic price repair: DISABLED. No external downloads.
[!] destructive=False always enforced.

Permitted operations:
  DEDUPLICATE_IDENTICAL — identical symbol/date/OHLCV rows only, keep one.
  NORMALIZE_SCHEMA      — safe column rename / dtype / date format only.
  NORMALIZE_DATE        — only clearly parseable formats, no guessing.
  REIMPORT_SAFE         — calls existing onboarding importer, never copies write logic.
  REFRESH_COVERAGE      — calls UniverseCoverageAnalyzer / UniverseStore.
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime
from typing import List, Optional

from coverage_repair.repair_schema import (
    CoverageRepairPlan, CoverageRepairTask, CoverageRepairResult,
    REPAIR_MODE_DRY_RUN, REPAIR_MODE_DEDUPLICATE_IDENTICAL,
    REPAIR_MODE_NORMALIZE_SAFE, REPAIR_MODE_REIMPORT_SAFE,
    REPAIR_MODE_MANUAL_REVIEW, REPAIR_MODE_BLOCKED,
    RESULT_STATUS_DRY_RUN, RESULT_STATUS_REPAIRED, RESULT_STATUS_BLOCKED,
    RESULT_STATUS_MANUAL, RESULT_STATUS_SKIPPED, RESULT_STATUS_FAILED,
    RESULT_STATUS_SOURCE_REQUIRED,
    STATUS_NEEDS_SOURCE_DATA, STATUS_NEEDS_REVIEW, STATUS_BLOCKED,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SafeCoverageRepairExecutor:
    """Executes only the safe subset of coverage repair tasks.

    [!] Research Only. No Real Orders.
    [!] allow_write=False default — nothing written without explicit flag.
    [!] INVALID OHLC tasks always BLOCKED.
    [!] CONFLICT tasks always MANUAL_REVIEW.
    [!] destructive tasks always BLOCKED.
    """

    NO_REAL_ORDERS                  = True
    RESEARCH_ONLY                   = True
    DRY_RUN_DEFAULT                 = True
    DESTRUCTIVE_REPAIR_DISABLED     = True
    SYNTHETIC_PRICE_REPAIR_ENABLED  = False
    EXTERNAL_DATA_DOWNLOAD_ENABLED  = False
    CONFLICT_AUTO_OVERWRITE_ENABLED = False

    def execute(self, plan: CoverageRepairPlan, allow_write: bool = False) -> "RepairRunSummary":
        """Execute all tasks in a plan. Returns a RepairRunSummary.

        Without allow_write=True all tasks produce DRY_RUN / BLOCKED results.
        """
        results: List[CoverageRepairResult] = []
        for task in plan.tasks:
            try:
                if not allow_write:
                    result = self.dry_run_task(task)
                else:
                    result = self.execute_task(task)
            except Exception as exc:
                logger.warning("Task %s failed: %s", task.task_id, exc)
                result = self._make_result(task, plan.plan_id, RESULT_STATUS_FAILED, error=str(exc))
            results.append(result)

        return RepairRunSummary(
            run_id=f"run_{uuid.uuid4().hex[:8]}",
            plan_id=plan.plan_id,
            executed_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            results=results,
            dry_run=not allow_write,
        )

    def execute_task(self, task: CoverageRepairTask) -> CoverageRepairResult:
        """Execute a single task. Enforces safety invariants."""
        plan_id = getattr(task, "_plan_id", "unknown")

        repair_mode = getattr(task, "repair_mode", REPAIR_MODE_DRY_RUN)
        destructive = getattr(task, "destructive", False)
        status      = getattr(task, "status", "OPEN")
        blocked_reason = getattr(task, "blocked_reason", None)

        # Hard blocks — never overrideable
        if destructive:
            return self._make_result(task, plan_id, RESULT_STATUS_BLOCKED,
                                     error="Destructive repair is permanently disabled.")

        if repair_mode == REPAIR_MODE_BLOCKED:
            return self._make_result(task, plan_id, RESULT_STATUS_BLOCKED,
                                     error=blocked_reason or "Task is BLOCKED.")

        if repair_mode == REPAIR_MODE_MANUAL_REVIEW:
            return self._make_result(task, plan_id, RESULT_STATUS_MANUAL,
                                     error="Manual review required — cannot auto-execute.")

        if status in (STATUS_NEEDS_SOURCE_DATA,):
            return self._make_result(task, plan_id, RESULT_STATUS_SOURCE_REQUIRED,
                                     error="Source data required before this task can execute.")

        if status in (STATUS_NEEDS_REVIEW, STATUS_BLOCKED):
            return self._make_result(task, plan_id, RESULT_STATUS_BLOCKED,
                                     error=f"Task status is {status} — cannot auto-execute.")

        # Permitted operations
        if repair_mode == REPAIR_MODE_DEDUPLICATE_IDENTICAL:
            return self.deduplicate_identical(task)

        if repair_mode == REPAIR_MODE_NORMALIZE_SAFE:
            return self.normalize_schema(task)

        if repair_mode == REPAIR_MODE_REIMPORT_SAFE:
            return self.reimport_safe(task)

        # Default: skip unknown modes safely
        return self._make_result(task, plan_id, RESULT_STATUS_SKIPPED,
                                 error=f"Repair mode '{repair_mode}' not executed in this run.")

    def dry_run_task(self, task: CoverageRepairTask) -> CoverageRepairResult:
        """Simulate task execution without writing any data."""
        plan_id = getattr(task, "_plan_id", "unknown")
        repair_mode    = getattr(task, "repair_mode", REPAIR_MODE_DRY_RUN)
        destructive    = getattr(task, "destructive", False)
        status         = getattr(task, "status", "OPEN")
        blocked_reason = getattr(task, "blocked_reason", None)
        action         = getattr(task, "action", "")

        if repair_mode == REPAIR_MODE_BLOCKED or destructive:
            return self._make_result(task, plan_id, RESULT_STATUS_BLOCKED,
                                     error=blocked_reason or "Blocked.")

        if repair_mode == REPAIR_MODE_MANUAL_REVIEW:
            return self._make_result(task, plan_id, RESULT_STATUS_MANUAL)

        # Also handle old-schema action-based routing
        if action in ("MANUAL_REVIEW", "BLOCKED"):
            if action == "BLOCKED":
                return self._make_result(task, plan_id, RESULT_STATUS_BLOCKED,
                                         error=blocked_reason or "Blocked.")
            return self._make_result(task, plan_id, RESULT_STATUS_MANUAL)

        if status == STATUS_NEEDS_SOURCE_DATA or action == "SOURCE_REQUIRED":
            return self._make_result(task, plan_id, RESULT_STATUS_SOURCE_REQUIRED)

        return self._make_result(task, plan_id, RESULT_STATUS_DRY_RUN)

    def deduplicate_identical(self, task: CoverageRepairTask) -> CoverageRepairResult:
        """Remove only rows that are 100% identical (same symbol/date/OHLCV).

        [!] Does NOT remove conflicting rows. Does NOT modify OHLCV values.
        """
        plan_id = getattr(task, "_plan_id", "unknown")
        try:
            data_path = self._locate_data_file(task)
            if not data_path or not os.path.exists(data_path):
                return self._make_result(
                    task, plan_id, RESULT_STATUS_SKIPPED,
                    warning=f"Data file not found for {task.symbol}/{task.dataset}",
                )

            import csv
            rows = self._read_csv(data_path)
            if not rows:
                return self._make_result(task, plan_id, RESULT_STATUS_SKIPPED,
                                         warning="Empty data file.")

            before_count = len(rows)
            # Keep only first occurrence of each fully-identical row
            seen = set()
            unique_rows = []
            for row in rows:
                key = tuple(sorted(row.items()))
                if key not in seen:
                    seen.add(key)
                    unique_rows.append(row)

            duplicates_removed = before_count - len(unique_rows)
            if duplicates_removed == 0:
                return self._make_result(task, plan_id, RESULT_STATUS_SKIPPED,
                                         warning="No identical duplicates found.")

            self._write_csv(data_path, unique_rows, fieldnames=list(rows[0].keys()))
            return CoverageRepairResult(
                result_id=f"res_{task.task_id}_{uuid.uuid4().hex[:6]}",
                plan_id=plan_id,
                task_id=task.task_id,
                symbol=task.symbol,
                issue_type=getattr(task, "repair_mode", getattr(task, "action", REPAIR_MODE_DRY_RUN)),
                status=RESULT_STATUS_REPAIRED,
                rows_before=before_count,
                rows_after=len(unique_rows),
                duplicates_removed=duplicates_removed,
                dry_run=False,
            )
        except Exception as exc:
            return self._make_result(task, plan_id, RESULT_STATUS_FAILED, error=str(exc))

    def normalize_schema(self, task: CoverageRepairTask) -> CoverageRepairResult:
        """Normalize column names / dtypes / date formats only.

        [!] Does NOT change OHLCV values.
        """
        plan_id = getattr(task, "_plan_id", "unknown")
        try:
            data_path = self._locate_data_file(task)
            if not data_path or not os.path.exists(data_path):
                return self._make_result(
                    task, plan_id, RESULT_STATUS_SKIPPED,
                    warning=f"Data file not found for {task.symbol}/{task.dataset}",
                )

            rows = self._read_csv(data_path)
            if not rows:
                return self._make_result(task, plan_id, RESULT_STATUS_SKIPPED,
                                         warning="Empty data file.")

            # Only safe renames: lowercase column headers
            normalized_rows = [
                {k.lower().strip(): v for k, v in row.items()}
                for row in rows
            ]
            self._write_csv(data_path, normalized_rows, fieldnames=list(normalized_rows[0].keys()))

            return CoverageRepairResult(
                result_id=f"res_{task.task_id}_{uuid.uuid4().hex[:6]}",
                plan_id=plan_id,
                task_id=task.task_id,
                symbol=task.symbol,
                issue_type=getattr(task, "repair_mode", getattr(task, "action", REPAIR_MODE_DRY_RUN)),
                status=RESULT_STATUS_REPAIRED,
                rows_before=len(rows),
                rows_after=len(normalized_rows),
                metadata_normalized=True,
                dry_run=False,
            )
        except Exception as exc:
            return self._make_result(task, plan_id, RESULT_STATUS_FAILED, error=str(exc))

    def normalize_date(self, task: CoverageRepairTask) -> CoverageRepairResult:
        """Normalize clearly parseable date formats only.

        [!] Does NOT guess ambiguous dates. Does NOT move future dates backward.
        """
        plan_id = getattr(task, "_plan_id", "unknown")
        return self._make_result(task, plan_id, RESULT_STATUS_DRY_RUN,
                                 warning="normalize_date: manual verification required before executing.")

    def reimport_safe(self, task: CoverageRepairTask) -> CoverageRepairResult:
        """Trigger safe reimport via existing onboarding importer.

        [!] Calls existing onboarding / importer — never copies write logic.
        """
        plan_id = getattr(task, "_plan_id", "unknown")
        if not task.source_path:
            return self._make_result(task, plan_id, RESULT_STATUS_SOURCE_REQUIRED,
                                     error="No source_path provided for reimport.")
        # Delegate to existing onboarding pipeline if available
        try:
            from data_onboarding.batch_import_executor import BatchImportExecutor
            executor = BatchImportExecutor(dry_run=task.dry_run)
            result_info = executor.import_single(task.source_path, symbol=task.symbol)
            status = RESULT_STATUS_REPAIRED if not task.dry_run else RESULT_STATUS_DRY_RUN
            return CoverageRepairResult(
                result_id=f"res_{task.task_id}_{uuid.uuid4().hex[:6]}",
                plan_id=plan_id,
                task_id=task.task_id,
                symbol=task.symbol,
                issue_type=getattr(task, "repair_mode", getattr(task, "action", REPAIR_MODE_DRY_RUN)),
                status=status,
                dry_run=task.dry_run,
                warning=str(result_info) if result_info else None,
            )
        except Exception as exc:
            return self._make_result(task, plan_id, RESULT_STATUS_FAILED, error=str(exc))

    def refresh_coverage(self, symbols: List[str]) -> dict:
        """Refresh universe coverage for the given symbols.

        [!] Calls UniverseCoverageAnalyzer — does not recalculate strategies.
        """
        try:
            from universe.universe_coverage_analyzer import UniverseCoverageAnalyzer
            from universe.universe_store import UniverseStore
            analyzer = UniverseCoverageAnalyzer()
            store = UniverseStore()
            results = {}
            for symbol in symbols:
                try:
                    cov = analyzer.analyze_symbol(symbol)
                    store.save_symbol_coverage(symbol, cov)
                    results[symbol] = "refreshed"
                except Exception as exc:
                    results[symbol] = f"error: {exc}"
            return results
        except Exception as exc:
            return {"error": str(exc)}

    def rollback_task(self, task: CoverageRepairTask) -> dict:
        """Placeholder rollback — returns metadata only (no destructive ops)."""
        return {
            "task_id": task.task_id,
            "symbol":  task.symbol,
            "status":  "rollback_not_implemented",
            "note":    "Manual restoration from backup required for full rollback.",
        }

    def build_audit_result(self, task: CoverageRepairTask) -> dict:
        """Build a minimal audit record for a task."""
        return {
            "task_id":      task.task_id,
            "issue_id":     task.issue_id,
            "symbol":       task.symbol,
            "action":       task.action,
            "repair_mode":  getattr(task, "repair_mode", getattr(task, "action", REPAIR_MODE_DRY_RUN)),
            "dry_run":      task.dry_run,
            "destructive":  task.destructive,
            "status":       task.status,
            "audited_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _locate_data_file(self, task: CoverageRepairTask) -> Optional[str]:
        return os.path.join(BASE_DIR, "data", "import", task.dataset, f"{task.symbol}.csv")

    def _read_csv(self, path: str) -> list:
        import csv
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _write_csv(self, path: str, rows: list, fieldnames: list) -> None:
        import csv
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _make_result(
        self,
        task: CoverageRepairTask,
        plan_id: str,
        status: str,
        warning: Optional[str] = None,
        error: Optional[str] = None,
    ) -> CoverageRepairResult:
        repair_mode = getattr(task, "repair_mode", getattr(task, "action", REPAIR_MODE_DRY_RUN))
        return CoverageRepairResult(
            result_id=f"res_{task.task_id}_{uuid.uuid4().hex[:6]}",
            plan_id=plan_id,
            task_id=task.task_id,
            symbol=task.symbol,
            issue_type=repair_mode,
            status=status,
            dry_run=getattr(task, "dry_run", True),
            warning=warning,
            error=error,
        )


# ---------------------------------------------------------------------------
# RepairRunSummary — lightweight result container
# ---------------------------------------------------------------------------

class RepairRunSummary:
    """Summary of a repair execution run."""

    def __init__(
        self,
        run_id: str,
        plan_id: str,
        executed_at: str,
        results: List[CoverageRepairResult],
        dry_run: bool = True,
    ):
        self.run_id = run_id
        self.plan_id = plan_id
        self.executed_at = executed_at
        self.results = results
        self.dry_run = dry_run
        self.research_only = True
        self.no_real_orders = True

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def repaired(self) -> int:
        return sum(1 for r in self.results if r.status == RESULT_STATUS_REPAIRED)

    @property
    def blocked(self) -> int:
        return sum(1 for r in self.results if r.status == RESULT_STATUS_BLOCKED)

    @property
    def dry_run_count(self) -> int:
        return sum(1 for r in self.results if r.status == RESULT_STATUS_DRY_RUN)

    @property
    def manual(self) -> int:
        return sum(1 for r in self.results if r.status == RESULT_STATUS_MANUAL)

    @property
    def source_required(self) -> int:
        return sum(1 for r in self.results if r.status == RESULT_STATUS_SOURCE_REQUIRED)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.status == RESULT_STATUS_FAILED)

    def to_dict(self) -> dict:
        return {
            "run_id":          self.run_id,
            "plan_id":         self.plan_id,
            "executed_at":     self.executed_at,
            "dry_run":         self.dry_run,
            "total":           self.total,
            "repaired":        self.repaired,
            "blocked":         self.blocked,
            "dry_run_count":   self.dry_run_count,
            "manual":          self.manual,
            "source_required": self.source_required,
            "failed":          self.failed,
            "research_only":   self.research_only,
            "no_real_orders":  self.no_real_orders,
            "results":         [r.to_dict() for r in self.results],
        }
