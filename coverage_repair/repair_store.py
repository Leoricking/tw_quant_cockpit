"""
coverage_repair/repair_store.py — RepairStore for TW Quant Cockpit v1.1.2.

Saves/loads repair plans, summaries, and retry manifests to data/coverage_repair_results/.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Output directory is gitignored.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "data", "coverage_repair_results")


class RepairStore:
    """Saves and loads repair workflow data.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def __init__(self, output_dir: str = DEFAULT_OUTPUT_DIR) -> None:
        self._output_dir = output_dir
        os.makedirs(self._output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Plan
    # ------------------------------------------------------------------

    def save_plan(self, plan) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self._output_dir, f"repair_plan_{ts}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(plan.to_dict(), f, ensure_ascii=False, indent=2)
        logger.info("Saved repair plan to %s", path)
        return path

    def load_latest_plan(self):
        from coverage_repair.coverage_repair_schema import RepairPlan
        return self._load_latest("repair_plan_", RepairPlan.from_dict)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def save_summary(self, summary) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self._output_dir, f"repair_summary_{ts}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary.to_dict(), f, ensure_ascii=False, indent=2)
        logger.info("Saved repair summary to %s", path)
        return path

    def load_latest_summary(self):
        from coverage_repair.coverage_repair_schema import RepairSummary
        return self._load_latest("repair_summary_", RepairSummary.from_dict)

    # ------------------------------------------------------------------
    # Retry Manifest
    # ------------------------------------------------------------------

    def save_retry_manifest(self, manifest) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self._output_dir, f"repair_retry_manifest_{ts}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(manifest.to_dict(), f, ensure_ascii=False, indent=2)
        logger.info("Saved repair retry manifest to %s", path)
        return path

    def load_latest_retry_manifest(self):
        from coverage_repair.coverage_repair_schema import RepairRetryManifest
        return self._load_latest("repair_retry_manifest_", RepairRetryManifest.from_dict)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_latest(self, prefix: str, from_dict_fn):
        files = [
            f for f in os.listdir(self._output_dir)
            if f.startswith(prefix) and f.endswith(".json")
        ]
        if not files:
            return None
        files.sort(reverse=True)
        path = os.path.join(self._output_dir, files[0])
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return from_dict_fn(data)
        except Exception as exc:
            logger.warning("RepairStore._load_latest %s: %s", path, exc)
            return None
