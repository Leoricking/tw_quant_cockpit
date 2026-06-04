"""gui/regression_suite_adapter.py — RegressionSuiteAdapter for TW Quant Cockpit v0.5.3.
[!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RegressionSuiteAdapter:
    """Non-GUI adapter for the Regression Suite Consolidation feature.

    No PySide6 dependency. Safe for use from CLI or non-GUI contexts.

    [!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        output_dir: str = "data/backtest_results/regression",
        report_dir: str = "reports",
    ) -> None:
        self.output_dir = os.path.join(BASE_DIR, output_dir)
        self.report_dir = os.path.join(BASE_DIR, report_dir)

        self._registry = None
        self._runner   = None
        self._store    = None

        try:
            from regression.suite_registry import RegressionSuiteRegistry
            self._registry = RegressionSuiteRegistry()
        except Exception as exc:
            logger.warning("RegressionSuiteAdapter: registry unavailable: %s", exc)

        try:
            from regression.regression_runner import RegressionRunner
            self._runner = RegressionRunner(registry=self._registry)
        except Exception as exc:
            logger.warning("RegressionSuiteAdapter: runner unavailable: %s", exc)

        try:
            from regression.regression_store import RegressionStore
            self._store = RegressionStore(output_dir=output_dir)
        except Exception as exc:
            logger.warning("RegressionSuiteAdapter: store unavailable: %s", exc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_suite(self, suite: str = "quick", mode: str = "real") -> dict:
        """Run a named regression suite. Returns summary dict."""
        try:
            if self._runner is None:
                return {
                    "suite":          suite,
                    "status":         "FAIL",
                    "error":          "RegressionRunner not available",
                    "no_real_orders": True,
                }
            return self._runner.run_suite(suite_name=suite, mode=mode)
        except Exception as exc:
            logger.warning("RegressionSuiteAdapter.run_suite() failed: %s", exc)
            return {
                "suite":          suite,
                "status":         "FAIL",
                "error":          str(exc),
                "no_real_orders": True,
            }

    def generate_report(self, mode: str = "real") -> str:
        """Generate regression consolidation report. Returns path."""
        try:
            from reports.regression_consolidation_report import RegressionConsolidationReport
            rpt = RegressionConsolidationReport(
                registry=self._registry,
                runner=self._runner,
                store=self._store,
                report_dir=self.report_dir,
                output_dir=self.output_dir,
                mode=mode,
            )
            return rpt.generate(suite_name="quick", mode=mode)
        except Exception as exc:
            logger.warning("RegressionSuiteAdapter.generate_report() failed: %s", exc)
            return ""

    def load_latest_summary(self) -> dict:
        """Load latest regression summary from store."""
        try:
            if self._store:
                return self._store.load_latest_summary()
        except Exception as exc:
            logger.warning("RegressionSuiteAdapter.load_latest_summary() failed: %s", exc)
        return {}

    def load_latest_results(self) -> list:
        """Load latest regression results from store."""
        try:
            if self._store:
                return self._store.load_latest_results()
        except Exception as exc:
            logger.warning("RegressionSuiteAdapter.load_latest_results() failed: %s", exc)
        return []

    def load_latest_coverage_matrix(self) -> list:
        """Load latest coverage matrix from store."""
        try:
            if self._store:
                return self._store.load_latest_coverage_matrix()
        except Exception as exc:
            logger.warning("RegressionSuiteAdapter.load_latest_coverage_matrix() failed: %s", exc)
        return []

    def load_latest_report_path(self) -> Optional[str]:
        """Find latest regression report Markdown file."""
        try:
            if self._store:
                return self._store.load_latest_report_path()
        except Exception as exc:
            logger.warning("RegressionSuiteAdapter.load_latest_report_path() failed: %s", exc)
        return None

    def list_suites(self) -> List[str]:
        """Return list of available suite names."""
        try:
            if self._registry:
                return self._registry.list_suites()
        except Exception as exc:
            logger.warning("RegressionSuiteAdapter.list_suites() failed: %s", exc)
        return []

    def get_coverage_score(self) -> float:
        """Return average coverage score."""
        try:
            from regression.coverage_matrix import RegressionCoverageMatrix
            matrix = RegressionCoverageMatrix(registry=self._registry)
            return matrix.summary_score()
        except Exception as exc:
            logger.warning("RegressionSuiteAdapter.get_coverage_score() failed: %s", exc)
        return 0.0
