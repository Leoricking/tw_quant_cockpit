"""report_pack/report_pack_store.py — ReportPackStore for TW Quant Cockpit v0.5.4.

Persists ReportPack manifests and summaries to CSV / JSON.
Output directory: data/backtest_results/report_pack/

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import glob
import json
import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "data", "backtest_results", "report_pack")


class ReportPackStore:
    """Persists ReportPack data to disk.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, output_dir: Optional[str] = None) -> None:
        self.output_dir = output_dir or _DEFAULT_OUTPUT_DIR
        try:
            os.makedirs(self.output_dir, exist_ok=True)
        except Exception as exc:
            logger.warning("ReportPackStore: cannot create output_dir: %s", exc)

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save_pack_summary(self, pack_dict: dict) -> Optional[str]:
        """Save pack summary (flattened) to report_pack_summary_YYYY-MM-DD.csv."""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(self.output_dir, f"report_pack_summary_{today}.csv")
            os.makedirs(self.output_dir, exist_ok=True)

            flat = {k: v for k, v in pack_dict.items() if k != "items"}
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(flat.keys()), extrasaction="ignore")
                writer.writeheader()
                writer.writerow(flat)
            logger.info("ReportPackStore: summary saved → %s", path)
            return path
        except Exception as exc:
            logger.warning("ReportPackStore.save_pack_summary() failed: %s", exc)
            return None

    def save_pack_items(self, items: List[dict], pack_type: str = "") -> Optional[str]:
        """Save pack items list to report_pack_items_YYYY-MM-DD.csv."""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            suffix = f"_{pack_type}" if pack_type else ""
            path = os.path.join(self.output_dir, f"report_pack_items{suffix}_{today}.csv")
            os.makedirs(self.output_dir, exist_ok=True)

            if not items:
                return None
            fieldnames = list(items[0].keys())
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(items)
            logger.info("ReportPackStore: items saved → %s", path)
            return path
        except Exception as exc:
            logger.warning("ReportPackStore.save_pack_items() failed: %s", exc)
            return None

    def save_health_report(self, health: dict) -> Optional[str]:
        """Save health check result to report_pack_health_YYYY-MM-DD.csv."""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(self.output_dir, f"report_pack_health_{today}.csv")
            os.makedirs(self.output_dir, exist_ok=True)

            flat = {k: v for k, v in health.items() if not isinstance(v, list)}
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(flat.keys()), extrasaction="ignore")
                writer.writeheader()
                writer.writerow(flat)
            logger.info("ReportPackStore: health saved → %s", path)
            return path
        except Exception as exc:
            logger.warning("ReportPackStore.save_health_report() failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """Load most recent report_pack_summary_*.csv. Returns {} on failure."""
        try:
            pattern = os.path.join(self.output_dir, "report_pack_summary_*.csv")
            files = sorted(glob.glob(pattern))
            if not files:
                return {}
            path = files[-1]
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    return dict(row)
            return {}
        except Exception as exc:
            logger.warning("ReportPackStore.load_latest_summary() failed: %s", exc)
            return {}

    def load_latest_items(self, pack_type: str = "") -> List[dict]:
        """Load most recent report_pack_items_*.csv. Returns [] on failure."""
        try:
            suffix = f"_{pack_type}" if pack_type else ""
            pattern = os.path.join(self.output_dir, f"report_pack_items{suffix}_*.csv")
            files = sorted(glob.glob(pattern))
            if not files:
                return []
            path = files[-1]
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return [dict(row) for row in reader]
        except Exception as exc:
            logger.warning("ReportPackStore.load_latest_items() failed: %s", exc)
            return []

    def load_latest_health(self) -> dict:
        """Load most recent report_pack_health_*.csv. Returns {} on failure."""
        try:
            pattern = os.path.join(self.output_dir, "report_pack_health_*.csv")
            files = sorted(glob.glob(pattern))
            if not files:
                return {}
            path = files[-1]
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    return dict(row)
            return {}
        except Exception as exc:
            logger.warning("ReportPackStore.load_latest_health() failed: %s", exc)
            return {}

    def load_latest_report_path(self) -> Optional[str]:
        """Find most recent report_pack_consolidation_report_*.md."""
        try:
            pattern = os.path.join(
                BASE_DIR, "reports", "report_pack_consolidation_report_*.md"
            )
            files = sorted(glob.glob(pattern))
            if not files:
                return None
            return files[-1]
        except Exception as exc:
            logger.warning("ReportPackStore.load_latest_report_path() failed: %s", exc)
            return None
