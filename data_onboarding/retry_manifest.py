"""
data_onboarding/retry_manifest.py — RetryManifestBuilder for TW Quant Cockpit v1.1.1.

Builds, saves, and loads retry manifests for failed imports.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

from data_onboarding.onboarding_schema import (
    BatchImportSummary, RetryManifest, ImportPlan,
    IMPORT_MODE_MERGE_SAFE,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RetryManifestBuilder:
    """
    Builds, saves, and loads retry manifests for failed imports.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def build(self, summary: BatchImportSummary) -> RetryManifest:
        """Build a RetryManifest from a BatchImportSummary."""
        failed_files   = [r.file_path for r in summary.results if r.status == "FAILED"]
        failed_symbols = list({r.symbol for r in summary.results
                               if r.status == "FAILED" and r.symbol})
        return RetryManifest(
            manifest_id=str(uuid.uuid4())[:8],
            created_at=datetime.now().isoformat(),
            source_path=summary.source_path,
            failed_files=failed_files,
            failed_symbols=failed_symbols,
            retry_count=0,
        )

    def save(self, manifest: RetryManifest, output_dir: str = "data/import_reports") -> str:
        """Save as JSON. Returns file path."""
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(output_dir, exist_ok=True)
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(output_dir, f"retry_manifest_{ts}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(manifest.to_dict(), f, ensure_ascii=False, indent=2)
        logger.info("Saved retry manifest to %s", path)
        return path

    def load_latest(self, output_dir: str = "data/import_reports") -> Optional[RetryManifest]:
        """Load the latest retry manifest JSON."""
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        if not os.path.isdir(output_dir):
            return None
        manifests = sorted(
            [f for f in os.listdir(output_dir) if f.startswith("retry_manifest_") and f.endswith(".json")],
            reverse=True,
        )
        if not manifests:
            return None
        path = os.path.join(output_dir, manifests[0])
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return RetryManifest.from_dict(data)
        except Exception as exc:
            logger.warning("Failed to load retry manifest %s: %s", path, exc)
            return None

    def retry_from_manifest(self, manifest: RetryManifest, dry_run: bool = True) -> ImportPlan:
        """Build a new ImportPlan from the failed files in the manifest."""
        from data_onboarding.import_planner import ImportPlanner
        from data_onboarding.onboarding_schema import ImportPlanItem, FILE_TYPE_UNKNOWN, PLAN_ACTION_MERGE_SAFE
        import uuid

        planner = ImportPlanner()
        # Build plan from failed files list
        # We'll discover each file individually
        items = []
        for file_path in manifest.failed_files:
            if not os.path.isfile(file_path):
                continue
            try:
                from data_onboarding.file_discovery import ImportFileDiscovery
                disc_result = ImportFileDiscovery()._process_file(file_path)
                if disc_result:
                    from data_onboarding.file_validator import ImportFileValidator
                    val = ImportFileValidator().validate(
                        file_path, disc_result.detected_symbol, disc_result.detected_dataset or 'daily'
                    )
                    item = planner.plan_file(disc_result, IMPORT_MODE_MERGE_SAFE, False, val, None)
                    items.append(item)
            except Exception as exc:
                logger.warning("retry_from_manifest: skipping %s: %s", file_path, exc)

        plan = ImportPlan(
            plan_id=str(uuid.uuid4())[:8],
            created_at=datetime.now().isoformat(),
            source_path=manifest.source_path,
            total_files=len(items),
            merge_safe_count=sum(1 for i in items if i.action == PLAN_ACTION_MERGE_SAFE),
            append_safe_count=0,
            replace_explicit_count=0,
            blocked_count=sum(1 for i in items if i.action == "BLOCKED"),
            review_count=sum(1 for i in items if i.action == "REVIEW"),
            skip_count=sum(1 for i in items if i.action == "SKIP"),
            items=items,
            dry_run=dry_run,
            destructive_disabled=True,
        )
        return plan
