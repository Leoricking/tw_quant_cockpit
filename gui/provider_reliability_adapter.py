"""
gui/provider_reliability_adapter.py - GUI bridge for Provider Reliability (v0.3.24).

Calls ProviderReliabilityMatrix directly (no subprocess).

[!] Read Only. No Real Orders. No token modification. No weight change.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProviderReliabilityAdapter:
    """
    GUI bridge between the dashboard and ProviderReliabilityMatrix.

    Parameters
    ----------
    results_dir : data/backtest_results
    report_dir  : reports/
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        results_dir: str = "data/backtest_results",
        report_dir:  str = "reports",
    ):
        self._results_dir = os.path.join(_BASE_DIR, results_dir)
        self._report_dir  = os.path.join(_BASE_DIR, report_dir)

    def run_reliability_matrix(self, mode: str = "real") -> dict:
        """
        Run the reliability matrix and return result dict.
        Does NOT place orders. Does NOT change weights. Does NOT change provider config.
        """
        try:
            from data.providers.reliability_matrix import ProviderReliabilityMatrix
            matrix = ProviderReliabilityMatrix(
                results_dir=self._results_dir,
                report_dir=self._report_dir,
                mode=mode,
            )
            return matrix.run()
        except Exception as exc:
            logger.error("run_reliability_matrix: %s", exc)
            return {
                "error":           str(exc),
                "mode":            mode,
                "read_only":       True,
                "no_real_orders":  True,
                "production_blocked": True,
            }

    def generate_report(self, mode: str = "real") -> str:
        """
        Run the matrix and write a Markdown report.
        Returns the path to the generated report.
        """
        try:
            data = self.run_reliability_matrix(mode=mode)
            from reports.provider_reliability_report import ProviderReliabilityReportBuilder
            builder = ProviderReliabilityReportBuilder(
                report_date=datetime.now().strftime("%Y-%m-%d"),
                matrix_data=data,
            )
            return builder.build(output_dir=self._report_dir)
        except Exception as exc:
            logger.error("generate_report: %s", exc)
            return ""

    def load_latest_report_path(self) -> Optional[str]:
        """Return the path to the most recently generated report, or None."""
        try:
            candidates = [
                os.path.join(self._report_dir, f)
                for f in os.listdir(self._report_dir)
                if f.startswith("provider_reliability_report") and f.endswith(".md")
            ]
            if not candidates:
                return None
            return max(candidates, key=os.path.getmtime)
        except Exception:
            return None

    def load_latest_summary(self) -> dict:
        """Return the latest reliability summary dict, or empty dict."""
        try:
            data = self.run_reliability_matrix()
            return data.get("reliability_summary", {})
        except Exception:
            return {}
