"""
data_onboarding/onboarding_store.py — OnboardingStore for TW Quant Cockpit v1.1.1.

Saves/loads onboarding results to data/import_reports/.
No git commit of runtime data.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

from data_onboarding.onboarding_schema import (
    ImportPlan, BatchImportSummary, RetryManifest, FileValidationResult,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class OnboardingStore:
    """
    Saves/loads onboarding results to data/import_reports/.
    No git commit of runtime data.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def __init__(self, output_dir: str = "data/import_reports") -> None:
        if not os.path.isabs(output_dir):
            self._dir = os.path.join(BASE_DIR, output_dir)
        else:
            self._dir = output_dir
        os.makedirs(self._dir, exist_ok=True)

    def _ts(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _latest(self, prefix: str) -> Optional[str]:
        """Return latest file path matching prefix in output dir."""
        try:
            files = sorted(
                [f for f in os.listdir(self._dir) if f.startswith(prefix) and f.endswith(".json")],
                reverse=True,
            )
            return os.path.join(self._dir, files[0]) if files else None
        except Exception:
            return None

    def _save_json(self, data: dict, prefix: str) -> str:
        path = os.path.join(self._dir, f"{prefix}_{self._ts()}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def _load_json(self, path: Optional[str]) -> Optional[dict]:
        if not path or not os.path.isfile(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("OnboardingStore._load_json %s: %s", path, exc)
            return None

    # ------------------------------------------------------------------
    # Plan
    # ------------------------------------------------------------------

    def save_plan(self, plan: ImportPlan) -> str:
        return self._save_json(plan.to_dict(), "import_plan")

    def load_latest_plan(self) -> Optional[ImportPlan]:
        data = self._load_json(self._latest("import_plan"))
        return ImportPlan.from_dict(data) if data else None

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def save_summary(self, summary: BatchImportSummary) -> str:
        return self._save_json(summary.to_dict(), "batch_summary")

    def load_latest_summary(self) -> Optional[BatchImportSummary]:
        data = self._load_json(self._latest("batch_summary"))
        return BatchImportSummary.from_dict(data) if data else None

    # ------------------------------------------------------------------
    # Retry manifest
    # ------------------------------------------------------------------

    def save_retry_manifest(self, manifest: RetryManifest) -> str:
        return self._save_json(manifest.to_dict(), "retry_manifest")

    def load_retry_manifest(self, manifest_id: str = "latest") -> Optional[RetryManifest]:
        if manifest_id == "latest":
            data = self._load_json(self._latest("retry_manifest"))
        else:
            path = os.path.join(self._dir, f"retry_manifest_{manifest_id}.json")
            data = self._load_json(path)
        return RetryManifest.from_dict(data) if data else None

    # ------------------------------------------------------------------
    # Validation results
    # ------------------------------------------------------------------

    def save_validation_results(self, results: List[FileValidationResult]) -> str:
        data = [r.to_dict() for r in results]
        return self._save_json({"validation_results": data}, "validation_results")
