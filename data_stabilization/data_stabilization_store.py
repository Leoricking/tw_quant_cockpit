"""data_stabilization/data_stabilization_store.py — DataStabilizationStore v0.5.5.

Persists Data Stabilization outputs to CSV files.
Output dir: data/backtest_results/data_stabilization/

[!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import glob
import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_DIR = os.path.join(
    BASE_DIR, "data", "backtest_results", "data_stabilization"
)


class DataStabilizationStore:
    """Persists Data Stabilization outputs.

    [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
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
            logger.warning("DataStabilizationStore: cannot create output_dir: %s", exc)

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save_summary(self, summary: dict) -> Optional[str]:
        """Save flat summary to data_stabilization_summary_YYYY-MM-DD.csv."""
        return self._save_flat(
            summary, f"data_stabilization_summary_{self._today()}.csv"
        )

    def save_schema_status(self, rows: List[dict]) -> Optional[str]:
        """Save schema status rows to dataset_schema_status_YYYY-MM-DD.csv."""
        return self._save_rows(rows, f"dataset_schema_status_{self._today()}.csv")

    def save_lineage(self, rows: List[dict]) -> Optional[str]:
        """Save lineage records to data_lineage_YYYY-MM-DD.csv."""
        return self._save_rows(rows, f"data_lineage_{self._today()}.csv")

    def save_feature_readiness(self, rows: List[dict]) -> Optional[str]:
        """Save feature readiness rows to feature_readiness_YYYY-MM-DD.csv."""
        return self._save_rows(rows, f"feature_readiness_{self._today()}.csv")

    def save_health(self, health: dict) -> Optional[str]:
        """Save feature store health to feature_store_health_YYYY-MM-DD.csv."""
        flat = {k: v for k, v in health.items() if not isinstance(v, list)}
        return self._save_flat(flat, f"feature_store_health_{self._today()}.csv")

    def save_leakage_summary(self, rows: List[dict]) -> Optional[str]:
        """Save leakage findings to leakage_guard_summary_YYYY-MM-DD.csv."""
        return self._save_rows(rows, f"leakage_guard_summary_{self._today()}.csv")

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """Load most recent data_stabilization_summary_*.csv."""
        return self._load_flat("data_stabilization_summary_*.csv")

    def load_schema_status(self) -> List[dict]:
        """Load most recent dataset_schema_status_*.csv."""
        return self._load_rows("dataset_schema_status_*.csv")

    def load_lineage(self) -> List[dict]:
        """Load most recent data_lineage_*.csv."""
        return self._load_rows("data_lineage_*.csv")

    def load_feature_readiness(self) -> List[dict]:
        """Load most recent feature_readiness_*.csv."""
        return self._load_rows("feature_readiness_*.csv")

    def load_health(self) -> dict:
        """Load most recent feature_store_health_*.csv."""
        return self._load_flat("feature_store_health_*.csv")

    def load_leakage_summary(self) -> List[dict]:
        """Load most recent leakage_guard_summary_*.csv."""
        return self._load_rows("leakage_guard_summary_*.csv")

    def load_latest_report_path(self) -> Optional[str]:
        """Find most recent data_stabilization_report_*.md."""
        try:
            pattern = os.path.join(
                BASE_DIR, "reports", "data_stabilization_report_*.md"
            )
            files = sorted(glob.glob(pattern))
            return files[-1] if files else None
        except Exception as exc:
            logger.warning("DataStabilizationStore.load_latest_report_path(): %s", exc)
            return None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _today(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def _save_flat(self, data: dict, filename: str) -> Optional[str]:
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            path = os.path.join(self.output_dir, filename)
            flat = {k: v for k, v in data.items() if not isinstance(v, (list, dict))}
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(flat.keys()), extrasaction="ignore")
                writer.writeheader()
                writer.writerow(flat)
            logger.info("DataStabilizationStore: saved → %s", path)
            return path
        except Exception as exc:
            logger.warning("DataStabilizationStore._save_flat(%s): %s", filename, exc)
            return None

    def _save_rows(self, rows: List[dict], filename: str) -> Optional[str]:
        try:
            if not rows:
                return None
            os.makedirs(self.output_dir, exist_ok=True)
            path = os.path.join(self.output_dir, filename)
            # Flatten list values to strings
            flat_rows = []
            for row in rows:
                flat = {k: (", ".join(str(v2) for v2 in v) if isinstance(v, list) else v)
                        for k, v in row.items()}
                flat_rows.append(flat)
            fieldnames = list(flat_rows[0].keys())
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(flat_rows)
            logger.info("DataStabilizationStore: saved → %s", path)
            return path
        except Exception as exc:
            logger.warning("DataStabilizationStore._save_rows(%s): %s", filename, exc)
            return None

    def _load_flat(self, pattern: str) -> dict:
        try:
            files = sorted(glob.glob(os.path.join(self.output_dir, pattern)))
            if not files:
                return {}
            with open(files[-1], "r", encoding="utf-8") as f:
                import csv as csv_mod
                reader = csv_mod.DictReader(f)
                for row in reader:
                    return dict(row)
            return {}
        except Exception as exc:
            logger.warning("DataStabilizationStore._load_flat(%s): %s", pattern, exc)
            return {}

    def _load_rows(self, pattern: str) -> List[dict]:
        try:
            files = sorted(glob.glob(os.path.join(self.output_dir, pattern)))
            if not files:
                return []
            with open(files[-1], "r", encoding="utf-8") as f:
                import csv as csv_mod
                reader = csv_mod.DictReader(f)
                return [dict(row) for row in reader]
        except Exception as exc:
            logger.warning("DataStabilizationStore._load_rows(%s): %s", pattern, exc)
            return []
