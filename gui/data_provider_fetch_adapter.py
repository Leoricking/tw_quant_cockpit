"""
gui/data_provider_fetch_adapter.py - Data adapter for Provider Fetch GUI (v0.3.19).

Bridges DataProviderAutoFetcher / DataFreshnessChecker to the GUI.
No subprocess. No real token display. No order placement.

[!] Read Only. No Real Orders.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataProviderFetchAdapter:
    """
    GUI adapter for the Data Provider Auto Fetch panel.

    Parameters
    ----------
    import_root : Root folder for data/import (default: project root)
    report_dir  : Report output directory (default: reports/)
    """

    def __init__(
        self,
        import_root: Optional[str] = None,
        report_dir:  Optional[str] = None,
    ):
        self._import_root = import_root or _BASE_DIR
        self._report_dir  = report_dir  or os.path.join(_BASE_DIR, "reports")
        self._last_fetch_summary: Optional[dict] = None

    # ------------------------------------------------------------------
    # Auto fetch
    # ------------------------------------------------------------------

    def run_auto_fetch(
        self,
        mode:     str = "real",
        dry_run:  bool = False,
        datasets: Optional[list] = None,
        months:   int = 24,
    ) -> dict:
        """
        Run the auto fetch pipeline.
        Returns the full fetch summary dict.
        Never raises — errors are captured in the result.
        """
        try:
            from data.providers.auto_fetcher import DataProviderAutoFetcher
            fetcher = DataProviderAutoFetcher(
                mode=mode,
                output_root=self._import_root,
                report_dir=self._report_dir,
                months=months,
                dry_run=dry_run,
            )
            result = fetcher.run(datasets=datasets)
            result["error"] = None
            self._last_fetch_summary = result
            return result
        except Exception as exc:
            logger.error("DataProviderFetchAdapter.run_auto_fetch: %s", exc)
            return {
                "status":        "FAILED",
                "mode":          mode,
                "read_only":     True,
                "no_real_orders":True,
                "dry_run":       dry_run,
                "datasets":      {},
                "providers_used":[],
                "rows_fetched":  0,
                "rows_written":  0,
                "warnings":      [],
                "errors":        [str(exc)],
                "error":         str(exc),
            }

    # ------------------------------------------------------------------
    # Freshness check
    # ------------------------------------------------------------------

    def run_freshness_check(self) -> dict:
        """
        Run the data freshness check.
        Returns the freshness summary dict.
        """
        try:
            from data.providers.data_freshness import DataFreshnessChecker
            checker = DataFreshnessChecker(import_root=self._import_root)
            result  = checker.run_all()
            result["error"] = None
            return result
        except Exception as exc:
            logger.error("DataProviderFetchAdapter.run_freshness_check: %s", exc)
            return {
                "checked_at":   datetime.now().isoformat(),
                "datasets":     {},
                "summary":      {},
                "read_only":    True,
                "no_real_orders":True,
                "error":        str(exc),
            }

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_report(self, mode: str = "real") -> dict:
        """
        Run fetch + freshness, then generate a Markdown report.
        Returns {"path": str, "error": str or None}.
        """
        try:
            fetch_result = self.run_auto_fetch(mode=mode, dry_run=True)
            freshness    = self.run_freshness_check()

            from reports.data_provider_fetch_report import DataProviderFetchReportBuilder
            builder = DataProviderFetchReportBuilder(
                report_date=datetime.now().strftime("%Y-%m-%d"),
                mode=mode,
                fetch_result=fetch_result,
                freshness=freshness,
            )
            path = builder.build(output_dir=self._report_dir)
            return {"path": path, "error": None}
        except Exception as exc:
            logger.error("DataProviderFetchAdapter.generate_report: %s", exc)
            return {"path": None, "error": str(exc)}

    # ------------------------------------------------------------------
    # Last fetch summary
    # ------------------------------------------------------------------

    def load_latest_fetch_summary(self) -> Optional[dict]:
        """Return the last fetch summary, or None."""
        return self._last_fetch_summary

    # ------------------------------------------------------------------
    # Latest report path
    # ------------------------------------------------------------------

    def load_latest_report_path(self) -> Optional[str]:
        """Return path of the most recent fetch report, or None."""
        try:
            import glob
            pattern = os.path.join(self._report_dir, "data_provider_fetch_report_*.md")
            files   = sorted(glob.glob(pattern))
            return files[-1] if files else None
        except Exception:
            return None
