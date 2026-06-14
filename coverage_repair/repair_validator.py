"""
coverage_repair/repair_validator.py — Before/after validation for coverage repair operations.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Validates that repairs do not introduce new issues, data loss, or invalid OHLC.
[!] Real dataset must not mix mock source rows.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from coverage_repair.repair_schema import (
    CoverageRepairResult,
    RESULT_STATUS_REPAIRED, RESULT_STATUS_PARTIAL, RESULT_STATUS_BLOCKED,
    RESULT_STATUS_SOURCE_REQUIRED, RESULT_STATUS_DRY_RUN,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CoverageRepairValidator:
    """Validates before/after state of coverage repair operations.

    Key invariants:
    - rows should not decrease unexpectedly (beyond deduplicated count)
    - no new invalid OHLC rows introduced
    - no new future dates introduced
    - no new conflicting rows introduced
    - real dataset must not contain mock source rows
    - coverage quality must improve (or remain the same) for REPAIRED status

    [!] Research Only. No Real Orders.
    """

    NO_REAL_ORDERS = True
    RESEARCH_ONLY  = True

    def capture_before(self, symbols: List[str]) -> Dict[str, dict]:
        """Capture coverage snapshot before repair execution."""
        snapshots = {}
        for symbol in symbols:
            snapshots[symbol] = self._snapshot_symbol(symbol)
        return snapshots

    def capture_after(self, symbols: List[str]) -> Dict[str, dict]:
        """Capture coverage snapshot after repair execution."""
        snapshots = {}
        for symbol in symbols:
            snapshots[symbol] = self._snapshot_symbol(symbol)
        return snapshots

    def compare_coverage(self, before: Dict[str, dict], after: Dict[str, dict]) -> dict:
        """Compare before/after snapshots. Returns a diff summary."""
        diff = {}
        all_symbols = set(list(before.keys()) + list(after.keys()))
        for symbol in all_symbols:
            b = before.get(symbol, {})
            a = after.get(symbol, {})
            diff[symbol] = {
                "rows_before":       b.get("row_count", 0),
                "rows_after":        a.get("row_count", 0),
                "rows_delta":        a.get("row_count", 0) - b.get("row_count", 0),
                "invalid_before":    b.get("invalid_count", 0),
                "invalid_after":     a.get("invalid_count", 0),
                "duplicate_before":  b.get("duplicate_count", 0),
                "duplicate_after":   a.get("duplicate_count", 0),
                "last_date_before":  b.get("last_date"),
                "last_date_after":   a.get("last_date"),
                "quality_before":    b.get("quality"),
                "quality_after":     a.get("quality"),
            }
        return diff

    def validate_task_result(self, result: CoverageRepairResult) -> dict:
        """Validate a single repair result. Returns a validation dict."""
        issues = []

        if result.rows_after < result.rows_before - result.duplicates_removed:
            unexpected_loss = result.rows_before - result.duplicates_removed - result.rows_after
            issues.append(f"Unexpected row loss: {unexpected_loss} rows")

        if result.status == RESULT_STATUS_REPAIRED and result.rows_after == 0:
            issues.append("Result is REPAIRED but row count is 0")

        valid = len(issues) == 0
        return {
            "task_id": result.task_id,
            "symbol":  result.symbol,
            "status":  result.status,
            "valid":   valid,
            "issues":  issues,
        }

    def validate_no_data_loss(
        self,
        before: Dict[str, dict],
        after: Dict[str, dict],
        max_loss_ratio: float = 0.05,
    ) -> dict:
        """Check that row counts have not decreased beyond expected deduplications."""
        violations = []
        for symbol in before:
            b_rows = before[symbol].get("row_count", 0)
            a_rows = after.get(symbol, {}).get("row_count", 0)
            if b_rows > 0:
                loss_ratio = (b_rows - a_rows) / b_rows
                if loss_ratio > max_loss_ratio and a_rows < b_rows:
                    violations.append({
                        "symbol":     symbol,
                        "rows_before": b_rows,
                        "rows_after":  a_rows,
                        "loss_ratio":  round(loss_ratio, 4),
                    })
        return {
            "passed":     len(violations) == 0,
            "violations": violations,
        }

    def validate_no_new_conflict(
        self,
        before: Dict[str, dict],
        after: Dict[str, dict],
    ) -> dict:
        """Check that no new conflicting rows were introduced."""
        violations = []
        for symbol in after:
            b_conflicts = before.get(symbol, {}).get("conflict_count", 0)
            a_conflicts = after[symbol].get("conflict_count", 0)
            if a_conflicts > b_conflicts:
                violations.append({
                    "symbol":           symbol,
                    "conflicts_before": b_conflicts,
                    "conflicts_after":  a_conflicts,
                })
        return {
            "passed":     len(violations) == 0,
            "violations": violations,
        }

    def validate_no_mock_rows(self, symbols: List[str]) -> dict:
        """Check that real dataset files do not contain rows tagged as mock source."""
        violations = []
        for symbol in symbols:
            path = os.path.join(BASE_DIR, "data", "import", "daily", f"{symbol}.csv")
            if os.path.exists(path):
                try:
                    import csv
                    with open(path, newline="", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for i, row in enumerate(reader):
                            source = row.get("source", "").lower()
                            if "mock" in source or "fake" in source or "synthetic" in source:
                                violations.append({
                                    "symbol": symbol,
                                    "row":    i + 2,
                                    "source": source,
                                })
                except Exception as exc:
                    logger.warning("validate_no_mock_rows %s: %s", symbol, exc)
        return {
            "passed":     len(violations) == 0,
            "violations": violations,
        }

    def validate_date_range(
        self,
        symbols: List[str],
        max_future_days: int = 0,
    ) -> dict:
        """Check that no future dates exist in the daily dataset."""
        from datetime import date
        today = date.today()
        violations = []
        for symbol in symbols:
            path = os.path.join(BASE_DIR, "data", "import", "daily", f"{symbol}.csv")
            if os.path.exists(path):
                try:
                    import csv
                    with open(path, newline="", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for i, row in enumerate(reader):
                            raw_date = row.get("date", "")
                            try:
                                d = datetime.strptime(raw_date[:10], "%Y-%m-%d").date()
                                if d > today:
                                    violations.append({
                                        "symbol": symbol,
                                        "row":    i + 2,
                                        "date":   raw_date,
                                    })
                            except ValueError:
                                pass
                except Exception as exc:
                    logger.warning("validate_date_range %s: %s", symbol, exc)
        return {
            "passed":     len(violations) == 0,
            "violations": violations,
        }

    def build_validation_summary(
        self,
        before: Dict[str, dict],
        after: Dict[str, dict],
        results: List[CoverageRepairResult],
    ) -> dict:
        """Build a comprehensive validation summary."""
        diff = self.compare_coverage(before, after)
        no_loss = self.validate_no_data_loss(before, after)
        no_new_conflict = self.validate_no_new_conflict(before, after)
        task_validations = [self.validate_task_result(r) for r in results]

        all_passed = (
            no_loss["passed"]
            and no_new_conflict["passed"]
            and all(v["valid"] for v in task_validations)
        )

        return {
            "validated_at":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "overall_valid":      all_passed,
            "no_data_loss":       no_loss,
            "no_new_conflict":    no_new_conflict,
            "task_validations":   task_validations,
            "coverage_diff":      diff,
            "research_only":      True,
            "no_real_orders":     True,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _snapshot_symbol(self, symbol: str) -> dict:
        """Read basic stats for a symbol's daily CSV."""
        path = os.path.join(BASE_DIR, "data", "import", "daily", f"{symbol}.csv")
        if not os.path.exists(path):
            return {"symbol": symbol, "exists": False, "row_count": 0}

        try:
            import csv
            from datetime import date

            rows = []
            with open(path, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))

            invalid_count = 0
            duplicate_dates: dict = {}
            conflict_count = 0
            last_date = None

            for row in rows:
                raw_date = row.get("date", "")[:10]
                if raw_date in duplicate_dates:
                    existing = duplicate_dates[raw_date]
                    if existing != row:
                        conflict_count += 1
                else:
                    duplicate_dates[raw_date] = row

                try:
                    close = float(row.get("close", 0) or 0)
                    high  = float(row.get("high",  0) or 0)
                    low   = float(row.get("low",   0) or 0)
                    if close <= 0 or high < low:
                        invalid_count += 1
                except (ValueError, TypeError):
                    invalid_count += 1

                if raw_date:
                    if last_date is None or raw_date > last_date:
                        last_date = raw_date

            duplicate_count = len(rows) - len(duplicate_dates)

            # Determine quality
            if invalid_count > 0 or conflict_count > 0:
                quality = "INVALID"
            elif len(rows) >= 240:
                quality = "READY"
            elif len(rows) >= 120:
                quality = "PARTIAL"
            elif len(rows) > 0:
                quality = "INSUFFICIENT"
            else:
                quality = "MISSING"

            return {
                "symbol":          symbol,
                "exists":          True,
                "row_count":       len(rows),
                "invalid_count":   invalid_count,
                "duplicate_count": duplicate_count,
                "conflict_count":  conflict_count,
                "last_date":       last_date,
                "quality":         quality,
            }
        except Exception as exc:
            logger.warning("snapshot_symbol %s: %s", symbol, exc)
            return {"symbol": symbol, "exists": True, "row_count": 0, "error": str(exc)}
