"""
training_metrics/training_metrics_store.py — TrainingMetricsStore v0.8.2

CSV-based persistence for training metrics data.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import List, Optional

from training_metrics.training_metrics_schema import (
    TrainingMetric, TrainingMetricsSummary,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_METRICS_FILE  = "training_metrics_{date}.csv"
_HISTORY_FILE  = "training_metrics_history.csv"
_SUMMARY_FILE  = "training_metrics_summary_{date}.csv"


class TrainingMetricsStore:
    """Saves and loads training metrics from CSV files.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, output_dir: str = "data/backtest_results/training_metrics") -> None:
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        self.output_dir = output_dir

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save_metrics(self, metrics: List[TrainingMetric]) -> str:
        """Save metrics to date-stamped CSV. Returns path."""
        os.makedirs(self.output_dir, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        path  = os.path.join(self.output_dir, _METRICS_FILE.format(date=today))
        try:
            fieldnames = [
                "metric_id", "metric_type", "source_module", "label",
                "value", "unit", "trend", "status", "description",
                "period", "baseline", "delta", "note", "generated_at",
            ]
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                for m in metrics:
                    writer.writerow(m.to_dict())
            logger.info("TrainingMetricsStore: saved %d metrics -> %s", len(metrics), path)
        except Exception as exc:
            logger.warning("TrainingMetricsStore.save_metrics: %s", exc)
        return path

    def save_summary(self, summary: TrainingMetricsSummary) -> str:
        """Save summary to date-stamped CSV. Returns path."""
        os.makedirs(self.output_dir, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        path  = os.path.join(self.output_dir, _SUMMARY_FILE.format(date=today))
        try:
            d = summary.to_dict()
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(d.keys()), extrasaction="ignore")
                writer.writeheader()
                writer.writerow(d)
            logger.info("TrainingMetricsStore: saved summary -> %s", path)
        except Exception as exc:
            logger.warning("TrainingMetricsStore.save_summary: %s", exc)
        return path

    def append_to_history(self, metrics: List[TrainingMetric]) -> str:
        """Append metrics to the rolling history CSV. Returns path."""
        os.makedirs(self.output_dir, exist_ok=True)
        path = os.path.join(self.output_dir, _HISTORY_FILE)
        try:
            fieldnames = [
                "metric_id", "metric_type", "source_module", "label",
                "value", "unit", "trend", "status", "description",
                "period", "baseline", "delta", "note", "generated_at",
            ]
            file_exists = os.path.exists(path)
            with open(path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                if not file_exists:
                    writer.writeheader()
                for m in metrics:
                    writer.writerow(m.to_dict())
            logger.info("TrainingMetricsStore: appended %d rows to history", len(metrics))
        except Exception as exc:
            logger.warning("TrainingMetricsStore.append_to_history: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_latest_metrics(self) -> List[TrainingMetric]:
        """Load most recent metrics CSV. Returns list of TrainingMetric."""
        # Use explicit pattern to avoid matching summary files
        import glob
        pattern = os.path.join(self.output_dir, "training_metrics_[0-9]*.csv")
        files   = sorted(glob.glob(pattern))
        if not files:
            return []
        try:
            items = []
            with open(files[-1], encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        items.append(TrainingMetric.from_dict(row))
                    except Exception as row_exc:
                        logger.warning("TrainingMetricsStore row parse error: %s", row_exc)
            return items
        except Exception as exc:
            logger.warning("TrainingMetricsStore.load_latest_metrics: %s", exc)
            return []

    def load_latest_summary(self) -> Optional[TrainingMetricsSummary]:
        """Load most recent summary CSV. Returns TrainingMetricsSummary or None."""
        import glob
        pattern = os.path.join(self.output_dir, "training_metrics_summary_*.csv")
        files   = sorted(glob.glob(pattern))
        if not files:
            return None
        try:
            with open(files[-1], encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    return TrainingMetricsSummary.from_dict(row)
        except Exception as exc:
            logger.warning("TrainingMetricsStore.load_latest_summary: %s", exc)
        return None

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _load_latest_typed(self, pattern: str, cls) -> list:
        """Load items from the most recent CSV matching pattern."""
        import glob
        files = sorted(glob.glob(os.path.join(self.output_dir, pattern)))
        if not files:
            return []
        try:
            items = []
            with open(files[-1], encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        items.append(cls.from_dict(row))
                    except Exception as row_exc:
                        logger.warning("TrainingMetricsStore row parse error: %s", row_exc)
            return items
        except Exception as exc:
            logger.warning("TrainingMetricsStore._load_latest_typed: %s", exc)
            return []
