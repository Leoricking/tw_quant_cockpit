"""
gui/release_status_adapter.py — ReleaseStatusAdapter: GUI bridge for Release Status panel (v0.4.0).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations
import logging
import os

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReleaseStatusAdapter:
    """GUI bridge for the Release Status panel.

    Wraps release.version_info, release.regression_suite,
    release.stable_release_checklist, and reports.stable_release_report.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, report_dir: str = "reports",
                 results_dir: str = "data/backtest_results") -> None:
        self.report_dir  = os.path.join(BASE_DIR, report_dir)
        self.results_dir = os.path.join(BASE_DIR, results_dir)

    # ------------------------------------------------------------------
    # Version info
    # ------------------------------------------------------------------

    def get_version_info(self) -> dict:
        """Return version info dict from release.version_info."""
        try:
            from release.version_info import get_version_info
            return get_version_info()
        except Exception as exc:
            logger.warning("get_version_info failed: %s", exc)
            return {
                "version":            "v0.4.0",
                "release_name":       "Research Platform Stable Release",
                "release_stage":      "stable_research",
                "read_only":          True,
                "no_real_orders":     True,
                "production_blocked": True,
                "real_order_ready":   False,
                "error":              str(exc),
            }

    # ------------------------------------------------------------------
    # Regression suite
    # ------------------------------------------------------------------

    def run_quick_regression(self, mode: str = "real") -> dict:
        """Create RegressionSuite(quick=True) and call run_quick()."""
        try:
            from release.regression_suite import RegressionSuite
            suite = RegressionSuite(mode=mode, quick=True,
                                    results_dir=os.path.relpath(self.results_dir, BASE_DIR))
            return suite.run_quick()
        except Exception as exc:
            logger.error("run_quick_regression failed: %s", exc)
            return {
                "suite":   "quick",
                "status":  "FAIL",
                "mode":    mode,
                "tests":   [],
                "passed":  0,
                "failed":  0,
                "warned":  0,
                "error":   str(exc),
            }

    def run_full_regression(self, mode: str = "real") -> dict:
        """Create RegressionSuite(quick=False) and call run_full()."""
        try:
            from release.regression_suite import RegressionSuite
            suite = RegressionSuite(mode=mode, quick=False,
                                    results_dir=os.path.relpath(self.results_dir, BASE_DIR))
            return suite.run_full()
        except Exception as exc:
            logger.error("run_full_regression failed: %s", exc)
            return {
                "suite":   "full",
                "status":  "FAIL",
                "mode":    mode,
                "tests":   [],
                "passed":  0,
                "failed":  0,
                "warned":  0,
                "error":   str(exc),
            }

    # ------------------------------------------------------------------
    # Checklist
    # ------------------------------------------------------------------

    def run_checklist(self, mode: str = "real") -> dict:
        """Create StableReleaseChecklist and call run()."""
        try:
            from release.stable_release_checklist import StableReleaseChecklist
            checklist = StableReleaseChecklist(
                mode=mode,
                results_dir=os.path.relpath(self.results_dir, BASE_DIR),
                report_dir=os.path.relpath(self.report_dir, BASE_DIR),
            )
            return checklist.run()
        except Exception as exc:
            logger.error("run_checklist failed: %s", exc)
            return {
                "status":             "FAIL",
                "mode":               mode,
                "version":            "v0.4.0",
                "items":              [],
                "passed":             0,
                "failed":             0,
                "warnings":           0,
                "read_only":          True,
                "no_real_orders":     True,
                "production_blocked": True,
                "real_order_ready":   False,
                "error":              str(exc),
            }

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_report(self, mode: str = "real",
                         regression_result: dict | None = None,
                         checklist_result: dict | None = None) -> dict:
        """Create StableReleaseReportBuilder and call build()."""
        try:
            from reports.stable_release_report import StableReleaseReportBuilder
            builder = StableReleaseReportBuilder(
                report_dir=os.path.relpath(self.report_dir, BASE_DIR),
                results_dir=os.path.relpath(self.results_dir, BASE_DIR),
                mode=mode,
            )
            path = builder.build(
                regression_result=regression_result,
                checklist_result=checklist_result,
            )
            return {"status": "OK", "path": path, "error": None}
        except Exception as exc:
            logger.error("generate_report failed: %s", exc)
            return {"status": "FAIL", "path": None, "error": str(exc)}

    # ------------------------------------------------------------------
    # Report discovery
    # ------------------------------------------------------------------

    def load_latest_report_path(self) -> str | None:
        """Scan report_dir for the most recent stable_release_report_*.md."""
        try:
            if not os.path.isdir(self.report_dir):
                return None
            candidates = [
                f for f in os.listdir(self.report_dir)
                if f.startswith("stable_release_report_") and f.endswith(".md")
            ]
            if not candidates:
                return None
            candidates.sort(reverse=True)
            return os.path.join(self.report_dir, candidates[0])
        except Exception as exc:
            logger.warning("load_latest_report_path failed: %s", exc)
            return None
