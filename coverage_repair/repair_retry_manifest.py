"""
coverage_repair/repair_retry_manifest.py — RepairRetryManifestBuilder for TW Quant Cockpit v1.1.2.

Manages retry workflow for failed coverage repair tasks.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True by default on retry.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

from coverage_repair.coverage_repair_schema import (
    RepairSummary, RepairRetryManifest, RepairPlan,
    REPAIR_STATUS_FAILED,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RepairRetryManifestBuilder:
    """Manages retry manifests for failed coverage repair tasks.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def build(self, summary: RepairSummary) -> RepairRetryManifest:
        """Build a RepairRetryManifest from a RepairSummary's failed results."""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        manifest_id = f"repair_retry_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        failed_results = [r for r in summary.results if r.status == REPAIR_STATUS_FAILED]
        failed_tasks  = [r.task_id for r in failed_results]
        failed_symbols = list({r.symbol for r in failed_results})

        return RepairRetryManifest(
            manifest_id=manifest_id,
            created_at=ts,
            plan_id=summary.plan_id,
            failed_tasks=failed_tasks,
            failed_symbols=failed_symbols,
            retry_count=0,
        )

    def save(self, manifest: RepairRetryManifest, output_dir: Optional[str] = None) -> str:
        """Save manifest JSON. Returns path."""
        from coverage_repair.repair_store import RepairStore, DEFAULT_OUTPUT_DIR
        store = RepairStore(output_dir=output_dir or DEFAULT_OUTPUT_DIR)
        return store.save_retry_manifest(manifest)

    def load_latest(self, output_dir: Optional[str] = None) -> Optional[RepairRetryManifest]:
        """Load most recent manifest."""
        from coverage_repair.repair_store import RepairStore, DEFAULT_OUTPUT_DIR
        store = RepairStore(output_dir=output_dir or DEFAULT_OUTPUT_DIR)
        return store.load_latest_retry_manifest()

    def retry_from_manifest(
        self,
        manifest: RepairRetryManifest,
        dry_run: bool = True,
    ) -> Optional[RepairPlan]:
        """Rebuild a RepairPlan targeting the symbols in the manifest."""
        if not manifest.failed_symbols:
            logger.info("No failed symbols in retry manifest.")
            return None
        from coverage_repair.repair_planner import CoverageRepairPlanner
        planner = CoverageRepairPlanner()
        plan = planner.build_plan(symbols=manifest.failed_symbols, dry_run=dry_run)
        return plan
