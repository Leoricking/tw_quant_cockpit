"""
data_coverage/data_coverage_engine.py — DataCoverageEngine for TW Quant Cockpit v0.6.2.

Orchestrates registry, scanner, and summary building for data coverage.

[!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Tuple

from data_coverage.data_coverage_registry import DataCoverageRegistry
from data_coverage.data_coverage_scanner import DataCoverageScanner
from data_coverage.data_coverage_schema import (
    DataCoverageItem, DataCoverageSummary,
    STATUS_READY, STATUS_PARTIAL, STATUS_MISSING_REQUIRED,
    STATUS_MISSING_OPTIONAL, STATUS_ENV_LIMITED, STATUS_NOT_GENERATED,
    STATUS_STALE, STATUS_FAILED, STATUS_UNKNOWN,
)

logger = logging.getLogger(__name__)


class DataCoverageEngine:
    """Orchestrates data coverage scan and summary.

    [!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        project_root: str = ".",
        output_dir: str = "data/backtest_results/data_coverage",
    ) -> None:
        self.project_root = project_root
        self.output_dir   = output_dir

    def run(self, mode: str = "real") -> Tuple[List[DataCoverageItem], DataCoverageSummary]:
        """Run a full coverage scan and return (items, summary)."""
        registry = DataCoverageRegistry()
        scanner  = DataCoverageScanner(
            registry=registry,
            project_root=self.project_root,
            output_dir=self.output_dir,
        )
        items   = scanner.scan(mode=mode)
        summary = self.build_summary(items, mode=mode)
        return items, summary

    def build_summary(
        self,
        items: List[DataCoverageItem],
        mode: str = "real",
    ) -> DataCoverageSummary:
        """Build DataCoverageSummary from scanned items."""
        total  = len(items)
        ready  = sum(1 for i in items if i.status == STATUS_READY)
        partial = sum(1 for i in items if i.status == STATUS_PARTIAL)
        env_lim = sum(1 for i in items if i.status == STATUS_ENV_LIMITED)
        not_gen = sum(1 for i in items if i.status == STATUS_NOT_GENERATED)
        miss_req = sum(1 for i in items if i.status == STATUS_MISSING_REQUIRED)
        miss_opt = sum(1 for i in items if i.status == STATUS_MISSING_OPTIONAL)
        stale   = sum(1 for i in items if i.status == STATUS_STALE)
        failed  = sum(1 for i in items if i.status == STATUS_FAILED)

        score = self.calculate_score(items)

        # Determine overall status
        if miss_req > 0 or failed > 0:
            overall_status = "DEGRADED"
        elif miss_opt > 2 or env_lim > 0:
            overall_status = "PARTIAL"
        elif ready >= total * 0.8:
            overall_status = "GOOD"
        else:
            overall_status = "PARTIAL"

        blockers = [
            f"{i.item_id} [{i.domain}]: {i.missing_reason or 'MISSING REQUIRED'}"
            for i in items if i.status == STATUS_MISSING_REQUIRED
        ]
        warnings = [
            f"{i.item_id} [{i.domain}]: {i.missing_reason or i.status}"
            for i in items
            if i.status in (STATUS_ENV_LIMITED, STATUS_FAILED, STATUS_MISSING_OPTIONAL)
        ]

        return DataCoverageSummary(
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            mode=mode,
            total_items=total,
            ready_count=ready,
            partial_count=partial,
            env_limited_count=env_lim,
            not_generated_count=not_gen,
            missing_required_count=miss_req,
            missing_optional_count=miss_opt,
            stale_count=stale,
            failed_count=failed,
            coverage_score=score,
            overall_status=overall_status,
            blockers=blockers,
            warnings=warnings,
        )

    def calculate_score(self, items: List[DataCoverageItem]) -> float:
        """Calculate a 0-100 coverage score.

        Scoring weights:
        - required READY   → +3.0 points
        - optional READY   → +1.0 point
        - ENV_LIMITED      → -0.5 penalty (not zero — limited by env, not missing)
        - MISSING_OPTIONAL → -0.2 penalty
        - FAILED           → -2.0 heavy penalty
        - MISSING_REQUIRED → -3.0 heavy penalty
        """
        if not items:
            return 0.0

        max_score = 0.0
        actual_score = 0.0

        for item in items:
            if item.required:
                max_score += 3.0
                if item.status == STATUS_READY:
                    actual_score += 3.0
                elif item.status == STATUS_PARTIAL:
                    actual_score += 1.5
                elif item.status == STATUS_ENV_LIMITED:
                    actual_score += 2.5  # env-limited is not item's fault
                    actual_score -= 0.5
                elif item.status == STATUS_NOT_GENERATED:
                    actual_score += 1.0
                elif item.status == STATUS_FAILED:
                    actual_score -= 2.0
                # MISSING_REQUIRED: 0 points
            else:
                max_score += 1.0
                if item.status == STATUS_READY:
                    actual_score += 1.0
                elif item.status == STATUS_PARTIAL:
                    actual_score += 0.5
                elif item.status == STATUS_ENV_LIMITED:
                    actual_score += 0.5  # env-limited, small penalty
                    actual_score -= 0.5
                elif item.status in (STATUS_MISSING_OPTIONAL, STATUS_NOT_GENERATED):
                    actual_score -= 0.2
                elif item.status == STATUS_FAILED:
                    actual_score -= 2.0

        if max_score <= 0:
            return 0.0

        raw = (actual_score / max_score) * 100.0
        return max(0.0, min(100.0, round(raw, 1)))
