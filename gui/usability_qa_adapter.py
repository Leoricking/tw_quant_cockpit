"""
gui/usability_qa_adapter.py - Usability QA GUI adapter (v0.3.22).

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from datetime import date
from typing import Optional

logger = logging.getLogger(__name__)


class UsabilityQAAdapter:
    """
    Adapter between the GUI panel and the UsabilitySmokeTest / report builders.

    All methods are safe to call from a QThread worker.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        base_dir:    Optional[str] = None,
        results_dir: Optional[str] = None,
        report_dir:  Optional[str] = None,
    ):
        self._base_dir    = base_dir    or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._results_dir = results_dir or os.path.join(self._base_dir, "data", "backtest_results")
        self._report_dir  = report_dir  or os.path.join(self._base_dir, "reports")

    def run_smoke_test(self) -> dict:
        """Run the full usability smoke test suite. Returns result dict."""
        from qa.usability_smoke_test import UsabilitySmokeTest
        test = UsabilitySmokeTest(
            base_dir    = self._base_dir,
            results_dir = self._results_dir,
            report_dir  = self._report_dir,
        )
        return test.run()

    def generate_report(self, smoke_result: Optional[dict] = None) -> str:
        """Build a Markdown QA report. Returns the report file path."""
        from reports.usability_qa_report import UsabilityQAReportBuilder
        builder = UsabilityQAReportBuilder(
            smoke_result = smoke_result or {},
            report_dir   = self._report_dir,
        )
        return builder.build()

    def load_latest_report_path(self) -> Optional[str]:
        """Return the path of the most recent usability_smoke_test_report_*.md, or None."""
        import glob as _glob
        pattern  = os.path.join(self._report_dir, "usability_smoke_test_report_*.md")
        matches  = sorted(_glob.glob(pattern), reverse=True)
        return matches[0] if matches else None

    def load_latest_summary(self) -> Optional[dict]:
        """Load the latest smoke test CSV summary as a list of dicts, or None."""
        csv_path = os.path.join(self._results_dir, "usability_smoke_test_summary.csv")
        if not os.path.isfile(csv_path):
            return None
        try:
            import pandas as pd
            df = pd.read_csv(csv_path, encoding="utf-8-sig")
            return {
                "rows":   df.to_dict(orient="records"),
                "passed": int((df["status"] == "PASS").sum())   if "status" in df.columns else 0,
                "failed": int((df["status"] == "FAIL").sum())   if "status" in df.columns else 0,
                "warnings": int((df["status"] == "WARNING").sum()) if "status" in df.columns else 0,
                "total":  len(df),
            }
        except Exception as exc:
            logger.warning("[UsabilityQAAdapter] Failed to load CSV: %s", exc)
            return None
