"""
data_onboarding/batch_executor.py — BatchImportExecutor for TW Quant Cockpit v1.1.1.

Executes an ImportPlan.
Wraps existing XQExportImporter and BatchImporter.

Rules:
- allow_write=False by default (dry_run only)
- destructive=False always
- Each file failure is isolated (does not abort others)
- REPLACE_EXPLICIT is BLOCKED unless explicitly enabled
- After successful import, triggers universe coverage refresh

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

from data_onboarding.onboarding_schema import (
    ImportPlan, ImportPlanItem, ImportResult, BatchImportSummary, RetryManifest,
    PLAN_ACTION_BLOCKED, PLAN_ACTION_REVIEW, PLAN_ACTION_SKIP,
    PLAN_ACTION_REPLACE_EXPLICIT,
    FILE_TYPE_XQ_EXCEL, FILE_TYPE_XQ_CSV, FILE_TYPE_STANDARD_CSV, FILE_TYPE_EXCEL,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BatchImportExecutor:
    """
    Executes an ImportPlan.
    Wraps existing XQExportImporter and BatchImporter.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] allow_write=False by default.
    """

    research_only  = True
    no_real_orders = True

    def execute(self, plan: ImportPlan, allow_write: bool = False) -> BatchImportSummary:
        """Execute all MERGE_SAFE / APPEND_SAFE tasks in the plan."""
        results: List[ImportResult] = []
        batch_id = str(uuid.uuid4())[:8]

        for item in plan.items:
            result = self.execute_item(item, allow_write=allow_write)
            results.append(result)

        succeeded = sum(1 for r in results if r.status in ("OK", "DRY_RUN"))
        partial   = sum(1 for r in results if r.status == "PARTIAL")
        failed    = sum(1 for r in results if r.status == "FAILED")
        skipped   = sum(1 for r in results if r.status == "SKIPPED")
        blocked   = sum(1 for r in results if r.status == "BLOCKED")

        summary = BatchImportSummary(
            batch_id=batch_id,
            created_at=datetime.now().isoformat(),
            source_path=plan.source_path,
            total_files=len(results),
            succeeded=succeeded,
            partial=partial,
            failed=failed,
            skipped=skipped,
            blocked=blocked,
            dry_run=not allow_write,
            results=results,
        )

        # Refresh coverage after write
        if allow_write and succeeded > 0:
            symbols = [r.symbol for r in results if r.symbol and r.status == "OK"]
            if symbols:
                try:
                    self.refresh_coverage(symbols)
                except Exception as exc:
                    logger.warning("Coverage refresh failed: %s", exc)

        return summary

    def execute_item(self, item: ImportPlanItem, allow_write: bool = False) -> ImportResult:
        """Execute a single plan item."""
        result_id = str(uuid.uuid4())[:8]
        base_kwargs = dict(
            result_id=result_id,
            plan_id="",
            file_path=item.file_path,
            symbol=item.symbol,
            dataset=item.dataset,
            dry_run=not allow_write,
        )

        # Blocked / skip / review
        if item.action == PLAN_ACTION_BLOCKED:
            return ImportResult(
                **base_kwargs,
                status="BLOCKED",
                rows_imported=0, rows_skipped=0, rows_failed=0,
                conflicts_detected=0, conflicts_kept=0,
                errors=[item.blocked_reason or "Blocked"],
            )
        if item.action == PLAN_ACTION_SKIP:
            return ImportResult(
                **base_kwargs,
                status="SKIPPED",
                rows_imported=0, rows_skipped=0, rows_failed=0,
                conflicts_detected=0, conflicts_kept=0,
            )
        if item.action == PLAN_ACTION_REVIEW:
            return ImportResult(
                **base_kwargs,
                status="SKIPPED",
                rows_imported=0, rows_skipped=0, rows_failed=0,
                conflicts_detected=item.expected_conflict_rows, conflicts_kept=0,
                warnings=["File requires manual review before import — conflicts detected"],
            )
        if item.action == PLAN_ACTION_REPLACE_EXPLICIT:
            return ImportResult(
                **base_kwargs,
                status="BLOCKED",
                rows_imported=0, rows_skipped=0, rows_failed=0,
                conflicts_detected=0, conflicts_kept=0,
                errors=["REPLACE_EXPLICIT is blocked — destructive import disabled by default"],
            )

        # Try actual import
        try:
            if item.file_type in (FILE_TYPE_XQ_EXCEL, FILE_TYPE_XQ_CSV):
                return self._execute_xq_file(item, allow_write)
            else:
                return self._execute_csv_file(item, allow_write)
        except Exception as exc:
            logger.warning("execute_item failed for %s: %s", item.file_path, exc)
            return ImportResult(
                **base_kwargs,
                status="FAILED",
                rows_imported=0, rows_skipped=0, rows_failed=0,
                conflicts_detected=0, conflicts_kept=0,
                errors=[str(exc)],
                executed_at=datetime.now().isoformat(),
            )

    def _execute_xq_file(self, item: ImportPlanItem, allow_write: bool) -> ImportResult:
        """Use existing XQExportImporter."""
        result_id = str(uuid.uuid4())[:8]
        try:
            from data.xq_export_importer import XQExportImporter
            importer = XQExportImporter()
            dry_run = not allow_write
            xq_result = importer.import_file(
                item.file_path,
                symbol=item.symbol or "",
                dry_run=dry_run,
            )
            rows_imported = xq_result.get("total_rows_imported", 0) if isinstance(xq_result, dict) else 0
            status = "DRY_RUN" if dry_run else "OK"
            return ImportResult(
                result_id=result_id,
                plan_id="",
                file_path=item.file_path,
                symbol=item.symbol,
                dataset=item.dataset,
                status=status,
                rows_imported=rows_imported,
                rows_skipped=0,
                rows_failed=0,
                conflicts_detected=0,
                conflicts_kept=0,
                dry_run=dry_run,
                executed_at=datetime.now().isoformat(),
            )
        except Exception as exc:
            return ImportResult(
                result_id=result_id,
                plan_id="",
                file_path=item.file_path,
                symbol=item.symbol,
                dataset=item.dataset,
                status="FAILED",
                rows_imported=0, rows_skipped=0, rows_failed=0,
                conflicts_detected=0, conflicts_kept=0,
                dry_run=not allow_write,
                errors=[str(exc)],
                executed_at=datetime.now().isoformat(),
            )

    def _execute_csv_file(self, item: ImportPlanItem, allow_write: bool) -> ImportResult:
        """Use existing BatchImporter / CSVImporter."""
        result_id = str(uuid.uuid4())[:8]
        dry_run = not allow_write
        try:
            from data.csv_importer import CSVImporter
            importer = CSVImporter()
            csv_result = importer.import_file(
                item.file_path,
                symbol=item.symbol or "",
                dataset=item.dataset,
                dry_run=dry_run,
            )
            rows_imported = csv_result.get("rows_imported", 0) if isinstance(csv_result, dict) else 0
            status = "DRY_RUN" if dry_run else "OK"
            return ImportResult(
                result_id=result_id,
                plan_id="",
                file_path=item.file_path,
                symbol=item.symbol,
                dataset=item.dataset,
                status=status,
                rows_imported=rows_imported,
                rows_skipped=0,
                rows_failed=0,
                conflicts_detected=0,
                conflicts_kept=0,
                dry_run=dry_run,
                executed_at=datetime.now().isoformat(),
            )
        except Exception as exc:
            # CSVImporter may not exist — that's OK, return DRY_RUN result
            status = "DRY_RUN" if dry_run else "FAILED"
            return ImportResult(
                result_id=result_id,
                plan_id="",
                file_path=item.file_path,
                symbol=item.symbol,
                dataset=item.dataset,
                status=status,
                rows_imported=0,
                rows_skipped=0,
                rows_failed=0,
                conflicts_detected=0,
                conflicts_kept=0,
                dry_run=dry_run,
                warnings=[f"CSV import: {exc}"] if dry_run else [],
                errors=[] if dry_run else [str(exc)],
                executed_at=datetime.now().isoformat(),
            )

    def refresh_coverage(self, symbols: List[str]) -> dict:
        """After import, call UniverseCoverageAnalyzer to refresh coverage."""
        try:
            from universe.universe_coverage_analyzer import UniverseCoverageAnalyzer
            analyzer = UniverseCoverageAnalyzer()
            result = analyzer.analyze(symbols=symbols)
            return result if isinstance(result, dict) else {"status": "refreshed", "symbols": symbols}
        except Exception as exc:
            logger.warning("refresh_coverage: %s", exc)
            return {"status": "unavailable", "error": str(exc), "symbols": symbols}

    def build_retry_manifest(self, summary: BatchImportSummary) -> RetryManifest:
        """Build retry manifest from failed results."""
        failed_files   = [r.file_path for r in summary.results if r.status == "FAILED"]
        failed_symbols = list({r.symbol for r in summary.results if r.status == "FAILED" and r.symbol})
        return RetryManifest(
            manifest_id=str(uuid.uuid4())[:8],
            created_at=datetime.now().isoformat(),
            source_path=summary.source_path,
            failed_files=failed_files,
            failed_symbols=failed_symbols,
        )
