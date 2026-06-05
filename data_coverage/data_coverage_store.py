"""
data_coverage/data_coverage_store.py — DataCoverageStore for TW Quant Cockpit v0.6.2.

Saves and loads coverage scan results (CSV files).

[!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import glob
import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)


class DataCoverageStore:
    """Persists coverage scan results to CSV files.

    [!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, output_dir: str = "data/backtest_results/data_coverage") -> None:
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _today(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def save_items(self, items: list) -> str:
        """Save coverage items to a dated CSV. Returns file path."""
        path = os.path.join(self.output_dir, f"data_coverage_items_{self._today()}.csv")
        fieldnames = [
            "item_id", "domain", "dataset_name", "status", "required",
            "environment_limited", "not_generated", "actual_path",
            "last_updated", "missing_reason", "suggested_command",
            "coverage_score", "warning",
            "no_real_orders", "production_blocked",
        ]
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                for item in items:
                    d = item.to_dict() if hasattr(item, "to_dict") else item
                    writer.writerow({k: d.get(k, "") for k in fieldnames})
            logger.info("Saved coverage items to %s", path)
        except Exception as exc:
            logger.warning("save_items failed: %s", exc)
        return path

    def save_summary(self, summary) -> str:
        """Save coverage summary to a dated CSV. Returns file path."""
        path = os.path.join(self.output_dir, f"data_coverage_summary_{self._today()}.csv")
        d = summary.to_dict() if hasattr(summary, "to_dict") else summary
        fieldnames = list(d.keys())
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                # Flatten lists to string for CSV
                row = {}
                for k, v in d.items():
                    if isinstance(v, list):
                        row[k] = " | ".join(str(x) for x in v)
                    else:
                        row[k] = v
                writer.writerow(row)
            logger.info("Saved coverage summary to %s", path)
        except Exception as exc:
            logger.warning("save_summary failed: %s", exc)
        return path

    def save_matrix(self, items: list) -> str:
        """Save domain/item/status matrix to a dated CSV. Returns file path."""
        path = os.path.join(self.output_dir, f"data_coverage_matrix_{self._today()}.csv")
        fieldnames = ["domain", "item_id", "dataset_name", "status", "required", "suggested_command"]
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                for item in items:
                    d = item.to_dict() if hasattr(item, "to_dict") else item
                    writer.writerow({k: d.get(k, "") for k in fieldnames})
            logger.info("Saved coverage matrix to %s", path)
        except Exception as exc:
            logger.warning("save_matrix failed: %s", exc)
        return path

    def load_latest_items(self) -> List[dict]:
        """Load the most recent coverage items CSV. Returns list of dicts."""
        pattern = os.path.join(self.output_dir, "data_coverage_items_*.csv")
        files = sorted(glob.glob(pattern))
        if not files:
            return []
        latest = files[-1]
        try:
            with open(latest, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as exc:
            logger.warning("load_latest_items failed: %s", exc)
            return []

    def load_latest_summary(self) -> dict:
        """Load the most recent coverage summary CSV. Returns dict."""
        pattern = os.path.join(self.output_dir, "data_coverage_summary_*.csv")
        files = sorted(glob.glob(pattern))
        if not files:
            return {}
        latest = files[-1]
        try:
            with open(latest, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                return rows[0] if rows else {}
        except Exception as exc:
            logger.warning("load_latest_summary failed: %s", exc)
            return {}
