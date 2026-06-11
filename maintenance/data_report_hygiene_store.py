"""
maintenance/data_report_hygiene_store.py — DataReportHygieneStore for v1.0.2.

Saves and loads hygiene scan outputs as CSV files. Never deletes files.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Data Cleanup is Review Only. Archive Suggestions Only.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import List, Optional

from maintenance.data_report_hygiene_schema import (
    HygieneInventoryItem,
    HygieneReportManifest,
    HygieneSummary,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataReportHygieneStore:
    """Saves and loads Data & Report Hygiene scan outputs as CSV.

    [!] Research Only. No Real Orders. Review Only.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    review_only        = True

    def __init__(self, output_dir: str = "data/backtest_results/maintenance") -> None:
        if os.path.isabs(output_dir):
            self._output_dir = output_dir
        else:
            self._output_dir = os.path.join(BASE_DIR, output_dir)

    def save_inventory(self, items: List[HygieneInventoryItem]) -> str:
        """Save inventory CSV. Returns file path."""
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self._output_dir, f"data_report_hygiene_inventory_{ts}.csv")
        self._ensure_dir()
        if not items:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write("")
            return path
        rows = [i.to_dict() for i in items]
        self._write_csv(path, rows)
        logger.info("Saved inventory: %s (%d rows)", path, len(rows))
        return path

    def save_report_manifest(self, manifests: List[HygieneReportManifest]) -> str:
        """Save report manifest CSV. Returns file path."""
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self._output_dir, f"data_report_hygiene_report_manifest_{ts}.csv")
        self._ensure_dir()
        if not manifests:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write("")
            return path
        rows = [m.to_dict() for m in manifests]
        self._write_csv(path, rows)
        logger.info("Saved report manifest: %s (%d rows)", path, len(rows))
        return path

    def save_summary(self, summary: HygieneSummary) -> str:
        """Save summary CSV. Returns file path."""
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self._output_dir, f"data_report_hygiene_summary_{ts}.csv")
        self._ensure_dir()
        self._write_csv(path, [summary.to_dict()])
        logger.info("Saved summary: %s", path)
        return path

    def load_latest_inventory(self) -> List[HygieneInventoryItem]:
        """Load the most recent inventory CSV."""
        path = self._latest_file("data_report_hygiene_inventory_")
        if not path:
            return []
        rows = self._read_csv(path)
        return [HygieneInventoryItem.from_dict(r) for r in rows]

    def load_latest_report_manifest(self) -> List[HygieneReportManifest]:
        """Load the most recent report manifest CSV."""
        path = self._latest_file("data_report_hygiene_report_manifest_")
        if not path:
            return []
        rows = self._read_csv(path)
        return [HygieneReportManifest.from_dict(r) for r in rows]

    def load_latest_summary(self) -> Optional[HygieneSummary]:
        """Load the most recent summary CSV."""
        path = self._latest_file("data_report_hygiene_summary_")
        if not path:
            return None
        rows = self._read_csv(path)
        if not rows:
            return None
        return HygieneSummary.from_dict(rows[0])

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _ensure_dir(self) -> None:
        os.makedirs(self._output_dir, exist_ok=True)

    def _write_csv(self, path: str, rows: List[dict]) -> None:
        if not rows:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write("")
            return
        fieldnames = list(rows[0].keys())
        with open(path, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _read_csv(self, path: str) -> List[dict]:
        rows = []
        try:
            with open(path, "r", encoding="utf-8", newline="") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    rows.append(dict(row))
        except Exception as exc:
            logger.warning("Could not read CSV %s: %s", path, exc)
        return rows

    def _latest_file(self, prefix: str) -> Optional[str]:
        if not os.path.isdir(self._output_dir):
            return None
        matches = [
            f for f in os.listdir(self._output_dir)
            if f.startswith(prefix) and f.endswith(".csv")
        ]
        if not matches:
            return None
        matches.sort(reverse=True)
        return os.path.join(self._output_dir, matches[0])
