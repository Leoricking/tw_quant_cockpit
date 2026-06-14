"""
coverage_repair/repair_executor.py — CoverageRepairExecutor for TW Quant Cockpit v1.1.2.

Executes a RepairPlan. dry_run=True by default.
execute() requires allow_write=True to write. Without it → BLOCKED.

Safety invariants:
  - CONFLICT → MANUAL (never auto-overwrite)
  - INVALID  → BLOCKED (never auto-modify OHLC)
  - SOURCE_REQUIRED → SKIPPED (no external downloads)
  - Synthetic OHLC: DISABLED
  - Volume zero-fill: DISABLED
  - Mock data repair: DISABLED
  - Universe coverage refresh triggered after successful write

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

from coverage_repair.coverage_repair_schema import (
    RepairPlan, RepairResult, RepairSummary,
    CoverageRepairTask,
    ACTION_AUTO_SAFE, ACTION_MANUAL_REVIEW, ACTION_SOURCE_REQUIRED, ACTION_BLOCKED,
    ISSUE_DUPLICATE, ISSUE_INVALID, ISSUE_CONFLICT,
    REPAIR_STATUS_OK, REPAIR_STATUS_DRY_RUN, REPAIR_STATUS_SKIPPED,
    REPAIR_STATUS_BLOCKED, REPAIR_STATUS_MANUAL, REPAIR_STATUS_FAILED, REPAIR_STATUS_PARTIAL,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CoverageRepairExecutor:
    """Executes a RepairPlan with safety guards.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] allow_write=False by default (dry_run only).
    [!] INVALID OHLC: always BLOCKED.
    [!] CONFLICT: always MANUAL (never auto-overwrite).
    [!] Synthetic OHLC: DISABLED.
    [!] Volume zero-fill: DISABLED.
    """

    research_only  = True
    no_real_orders = True

    def execute(self, plan: RepairPlan, allow_write: bool = False) -> RepairSummary:
        """Execute a RepairPlan. Returns RepairSummary.

        If allow_write=False, all tasks are treated as dry-run (no data modification).
        If allow_write=True, only AUTO_SAFE tasks are executed.
        BLOCKED, MANUAL_REVIEW, SOURCE_REQUIRED tasks are never executed regardless of allow_write.
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary_id = f"repair_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        results: List[RepairResult] = []
        succeeded = partial = failed = skipped = blocked = manual_review = 0

        for task in plan.tasks:
            result = self._execute_task(task, allow_write=allow_write)
            results.append(result)

            s = result.status
            if s == REPAIR_STATUS_OK:
                succeeded += 1
            elif s == REPAIR_STATUS_PARTIAL:
                partial += 1
            elif s == REPAIR_STATUS_FAILED:
                failed += 1
            elif s in (REPAIR_STATUS_SKIPPED, REPAIR_STATUS_DRY_RUN):
                skipped += 1
            elif s == REPAIR_STATUS_BLOCKED:
                blocked += 1
            elif s == REPAIR_STATUS_MANUAL:
                manual_review += 1

        # Refresh universe coverage if any writes occurred
        if allow_write and succeeded > 0:
            repaired_symbols = list({r.symbol for r in results if r.status == REPAIR_STATUS_OK})
            self._refresh_universe_coverage(repaired_symbols)

        return RepairSummary(
            summary_id=summary_id,
            plan_id=plan.plan_id,
            created_at=ts,
            total_tasks=len(plan.tasks),
            succeeded=succeeded,
            partial=partial,
            failed=failed,
            skipped=skipped,
            blocked=blocked,
            manual_review=manual_review,
            dry_run=not allow_write,
            results=results,
        )

    def _execute_task(self, task: CoverageRepairTask, allow_write: bool) -> RepairResult:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result_id = f"result_{task.task_id}"

        def make_result(status, rows_before=0, rows_after=0, rows_removed=0,
                        blocked_reason=None, warnings=None, errors=None):
            return RepairResult(
                result_id=result_id,
                task_id=task.task_id,
                plan_id="",
                symbol=task.symbol,
                dataset=task.dataset,
                issue_type=task.issue_type,
                action=task.action,
                status=status,
                rows_before=rows_before,
                rows_after=rows_after,
                rows_removed=rows_removed,
                dry_run=not allow_write,
                blocked_reason=blocked_reason,
                warnings=warnings or [],
                errors=errors or [],
                executed_at=ts,
            )

        # Safety: BLOCKED always stays BLOCKED
        if task.action == ACTION_BLOCKED or task.issue_type == ISSUE_INVALID:
            return make_result(
                REPAIR_STATUS_BLOCKED,
                rows_before=task.before_row_count,
                rows_after=task.before_row_count,
                blocked_reason=task.blocked_reason or "Invalid OHLC data must not be auto-modified.",
            )

        # CONFLICT → always MANUAL_REVIEW
        if task.action == ACTION_MANUAL_REVIEW or task.issue_type == ISSUE_CONFLICT:
            return make_result(
                REPAIR_STATUS_MANUAL,
                rows_before=task.before_row_count,
                rows_after=task.before_row_count,
                warnings=["Conflict requires manual review. No auto-overwrite."],
            )

        # SOURCE_REQUIRED → always SKIPPED (no external downloads)
        if task.action == ACTION_SOURCE_REQUIRED:
            return make_result(
                REPAIR_STATUS_SKIPPED,
                rows_before=task.before_row_count,
                rows_after=task.before_row_count,
                warnings=["Source data required. No external download. Import data manually."],
            )

        # AUTO_SAFE: dry-run if allow_write=False
        if not allow_write:
            return make_result(
                REPAIR_STATUS_DRY_RUN,
                rows_before=task.before_row_count,
                rows_after=task.estimated_after_row_count,
                warnings=["Dry run. No data modified. Re-run with allow_write=True to apply."],
            )

        # AUTO_SAFE + allow_write=True: execute the safe repair
        return self._execute_auto_safe(task, ts)

    def _execute_auto_safe(self, task: CoverageRepairTask, ts: str) -> RepairResult:
        """Execute an AUTO_SAFE repair task (identical duplicate deduplication only)."""
        result_id = f"result_{task.task_id}"

        if task.issue_type != ISSUE_DUPLICATE:
            # Only deduplicate is AUTO_SAFE; anything else unexpected → BLOCKED
            return RepairResult(
                result_id=result_id,
                task_id=task.task_id,
                plan_id="",
                symbol=task.symbol,
                dataset=task.dataset,
                issue_type=task.issue_type,
                action=task.action,
                status=REPAIR_STATUS_BLOCKED,
                rows_before=task.before_row_count,
                rows_after=task.before_row_count,
                rows_removed=0,
                dry_run=False,
                blocked_reason="Unexpected AUTO_SAFE action for non-duplicate issue.",
                executed_at=ts,
            )

        # Safe deduplication: remove identical duplicate rows
        try:
            data_path = os.path.join(
                BASE_DIR, "data", "import", task.dataset, f"{task.symbol}.csv"
            )
            if not os.path.isfile(data_path):
                return RepairResult(
                    result_id=result_id, task_id=task.task_id, plan_id="",
                    symbol=task.symbol, dataset=task.dataset,
                    issue_type=task.issue_type, action=task.action,
                    status=REPAIR_STATUS_FAILED,
                    rows_before=task.before_row_count, rows_after=task.before_row_count,
                    rows_removed=0, dry_run=False,
                    errors=["Data file not found."], executed_at=ts,
                )

            import pandas as pd
            df = None
            for enc in ("utf-8-sig", "utf-8", "big5", "cp950"):
                try:
                    df = pd.read_csv(data_path, encoding=enc)
                    break
                except Exception:
                    continue

            if df is None:
                return RepairResult(
                    result_id=result_id, task_id=task.task_id, plan_id="",
                    symbol=task.symbol, dataset=task.dataset,
                    issue_type=task.issue_type, action=task.action,
                    status=REPAIR_STATUS_FAILED,
                    rows_before=task.before_row_count, rows_after=task.before_row_count,
                    rows_removed=0, dry_run=False,
                    errors=["Could not read data file."], executed_at=ts,
                )

            rows_before = len(df)

            # Identify date column
            DATE_CANDIDATES = ["date", "時間", "日期", "datetime"]
            date_col = None
            for c in DATE_CANDIDATES:
                if c in df.columns:
                    date_col = c
                    break

            if date_col:
                # Drop exact duplicates (all columns identical), keep first
                df_dedup = df.drop_duplicates(keep="first")
            else:
                df_dedup = df.drop_duplicates(keep="first")

            rows_after = len(df_dedup)
            rows_removed = rows_before - rows_after

            if rows_removed == 0:
                return RepairResult(
                    result_id=result_id, task_id=task.task_id, plan_id="",
                    symbol=task.symbol, dataset=task.dataset,
                    issue_type=task.issue_type, action=task.action,
                    status=REPAIR_STATUS_OK,
                    rows_before=rows_before, rows_after=rows_after,
                    rows_removed=0, dry_run=False,
                    warnings=["No identical duplicates found to remove."], executed_at=ts,
                )

            # Before/after validation: ensure no new data introduced
            assert len(df_dedup) <= len(df), "Deduplication must not add rows"

            # Write back
            df_dedup.to_csv(data_path, index=False, encoding="utf-8-sig")

            return RepairResult(
                result_id=result_id, task_id=task.task_id, plan_id="",
                symbol=task.symbol, dataset=task.dataset,
                issue_type=task.issue_type, action=task.action,
                status=REPAIR_STATUS_OK,
                rows_before=rows_before, rows_after=rows_after,
                rows_removed=rows_removed, dry_run=False,
                executed_at=ts,
            )

        except Exception as exc:
            logger.error("_execute_auto_safe %s/%s: %s", task.symbol, task.dataset, exc)
            return RepairResult(
                result_id=result_id, task_id=task.task_id, plan_id="",
                symbol=task.symbol, dataset=task.dataset,
                issue_type=task.issue_type, action=task.action,
                status=REPAIR_STATUS_FAILED,
                rows_before=task.before_row_count, rows_after=task.before_row_count,
                rows_removed=0, dry_run=False,
                errors=[str(exc)], executed_at=ts,
            )

    def _refresh_universe_coverage(self, symbols: List[str]) -> None:
        try:
            from universe.universe_coverage_analyzer import UniverseCoverageAnalyzer
            analyzer = UniverseCoverageAnalyzer()
            analyzer.analyze(symbols=symbols if symbols else None)
            logger.info("Universe coverage refreshed for %d symbol(s) after repair.", len(symbols))
        except Exception as exc:
            logger.warning("Coverage refresh after repair unavailable: %s", exc)
