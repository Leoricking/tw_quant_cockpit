"""regression/regression_store.py — RegressionStore for TW Quant Cockpit v0.5.3.
[!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
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


class RegressionStore:
    """Persists regression run results, summaries, and coverage matrices.

    [!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, output_dir: str = "data/backtest_results/regression") -> None:
        self.output_dir = os.path.join(BASE_DIR, output_dir)
        try:
            os.makedirs(self.output_dir, exist_ok=True)
        except Exception as exc:
            logger.warning("RegressionStore: cannot create output_dir: %s", exc)

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save_results(self, results: list) -> Optional[str]:
        """Save list of RegressionTestResult dicts to CSV. Returns path or None."""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(self.output_dir, f"regression_results_{today}.csv")
            os.makedirs(self.output_dir, exist_ok=True)

            if not results:
                return None

            # Normalise — accept both RegressionTestResult objects and dicts
            rows = [r.to_dict() if hasattr(r, "to_dict") else r for r in results]
            if not rows:
                return None

            fieldnames = list(rows[0].keys())
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.info("RegressionStore: results saved → %s", path)
            return path
        except Exception as exc:
            logger.warning("RegressionStore.save_results() failed: %s", exc)
            return None

    def save_summary(self, summary: dict) -> Optional[str]:
        """Save summary dict to CSV. Returns path or None."""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(self.output_dir, f"regression_summary_{today}.csv")
            os.makedirs(self.output_dir, exist_ok=True)

            # Flatten to single-row CSV (exclude nested 'tests' list)
            flat = {k: v for k, v in summary.items() if k != "tests"}
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(flat.keys()), extrasaction="ignore")
                writer.writeheader()
                writer.writerow(flat)
            logger.info("RegressionStore: summary saved → %s", path)
            return path
        except Exception as exc:
            logger.warning("RegressionStore.save_summary() failed: %s", exc)
            return None

    def save_coverage_matrix(self, matrix: list) -> Optional[str]:
        """Save coverage matrix to CSV. Returns path or None."""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(self.output_dir, f"regression_coverage_matrix_{today}.csv")
            os.makedirs(self.output_dir, exist_ok=True)

            if not matrix:
                return None

            fieldnames = list(matrix[0].keys())
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(matrix)
            logger.info("RegressionStore: coverage matrix saved → %s", path)
            return path
        except Exception as exc:
            logger.warning("RegressionStore.save_coverage_matrix() failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """Load the most recent regression_summary_*.csv. Returns {} on failure."""
        try:
            pattern = os.path.join(self.output_dir, "regression_summary_*.csv")
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
            logger.warning("RegressionStore.load_latest_summary() failed: %s", exc)
            return {}

    def load_latest_results(self) -> list:
        """Load the most recent regression_results_*.csv. Returns [] on failure."""
        try:
            pattern = os.path.join(self.output_dir, "regression_results_*.csv")
            files = sorted(glob.glob(pattern))
            if not files:
                return []
            path = files[-1]
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return [dict(row) for row in reader]
        except Exception as exc:
            logger.warning("RegressionStore.load_latest_results() failed: %s", exc)
            return []

    def load_latest_coverage_matrix(self) -> list:
        """Load the most recent regression_coverage_matrix_*.csv. Returns [] on failure."""
        try:
            pattern = os.path.join(self.output_dir, "regression_coverage_matrix_*.csv")
            files = sorted(glob.glob(pattern))
            if not files:
                return []
            path = files[-1]
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return [dict(row) for row in reader]
        except Exception as exc:
            logger.warning("RegressionStore.load_latest_coverage_matrix() failed: %s", exc)
            return []

    def load_latest_report_path(self) -> Optional[str]:
        """Find the most recent regression consolidation report Markdown file."""
        try:
            pattern = os.path.join(BASE_DIR, "reports", "regression_consolidation_report_*.md")
            files = sorted(glob.glob(pattern))
            if not files:
                return None
            return files[-1]
        except Exception as exc:
            logger.warning("RegressionStore.load_latest_report_path() failed: %s", exc)
            return None
