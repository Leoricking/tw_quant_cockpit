"""
gui/intraday_pipeline_adapter.py — GUI bridge for Intraday Pipeline (v0.3.27).
No subprocess. Direct Python call.
[!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class IntradayPipelineAdapter:
    """
    Thin bridge between the GUI and the intraday pipeline modules.

    Calls IntradayDataPipeline, IntradayQualityChecker, and
    IntradayPipelineReportBuilder directly (no subprocess).

    [!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.

    Safety flags
    ------------
    read_only           : True
    no_real_orders      : True
    production_blocked  : True
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(
        self,
        standard_root: str = "data/import/intraday_standard",
        report_dir: str = "reports",
        results_dir: str = "data/backtest_results",
    ):
        self.standard_root = (
            standard_root if os.path.isabs(standard_root)
            else os.path.join(BASE_DIR, standard_root)
        )
        self.report_dir = (
            report_dir if os.path.isabs(report_dir)
            else os.path.join(BASE_DIR, report_dir)
        )
        self.results_dir = (
            results_dir if os.path.isabs(results_dir)
            else os.path.join(BASE_DIR, results_dir)
        )

    # ------------------------------------------------------------------
    # Pipeline
    # ------------------------------------------------------------------

    def run_pipeline(
        self,
        mode: str = "real",
        freq: str = "1min",
        dry_run: bool = True,
    ) -> dict:
        """
        Instantiate IntradayDataPipeline and run it.

        Parameters
        ----------
        mode    : "real" only in v0.3.27 (no mock fallback)
        freq    : "1min" or "5min"
        dry_run : if True, skip file writes

        Returns
        -------
        dict — pipeline result or {"status": "ERROR", "error": str}
        """
        try:
            from intraday.intraday_pipeline import IntradayDataPipeline
            pipeline = IntradayDataPipeline(
                mode=mode,
                freq=freq,
                dry_run=dry_run,
                output_root=self.standard_root,
                results_dir=self.results_dir,
                report_dir=self.report_dir,
            )
            result = pipeline.run()
            result["mode"] = mode
            result["freq"] = freq
            result["dry_run"] = dry_run
            return result
        except Exception as exc:
            logger.exception("run_pipeline error: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    # ------------------------------------------------------------------
    # Quality check
    # ------------------------------------------------------------------

    def check_quality(self, freq: str = "1min") -> dict:
        """
        Instantiate IntradayQualityChecker and run it.

        Returns
        -------
        dict — quality result or {"status": "ERROR", "error": str}
        """
        try:
            from intraday.intraday_quality import IntradayQualityChecker
            checker = IntradayQualityChecker(standard_root=self.standard_root)
            return checker.run()
        except Exception as exc:
            logger.exception("check_quality error: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_report(
        self,
        mode: str = "real",
        pipeline_result: Optional[dict] = None,
        quality_result: Optional[dict] = None,
    ) -> str:
        """
        Instantiate IntradayPipelineReportBuilder and build the report.

        Returns
        -------
        str path to the written report, or an error string
        """
        try:
            from reports.intraday_pipeline_report import IntradayPipelineReportBuilder
            builder = IntradayPipelineReportBuilder(
                pipeline_result=pipeline_result,
                quality_result=quality_result,
                mode=mode,
            )
            return builder.build(output_dir=self.report_dir)
        except Exception as exc:
            logger.exception("generate_report error: %s", exc)
            return f"ERROR: {exc}"

    # ------------------------------------------------------------------
    # Summary / latest report
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """
        Read intraday_pipeline_summary.csv from results_dir.

        Returns
        -------
        dict with summary fields, or empty dict if not found
        """
        csv_path = os.path.join(self.results_dir, "intraday_pipeline_summary.csv")
        if not os.path.isfile(csv_path):
            return {}
        try:
            import pandas as pd
            df = pd.read_csv(csv_path, dtype=str)
            if df.empty:
                return {}
            # Return last row as dict
            return df.iloc[-1].to_dict()
        except Exception as exc:
            logger.warning("load_latest_summary: %s", exc)
            return {}

    def load_latest_report_path(self) -> Optional[str]:
        """
        Find the latest intraday_pipeline_report_*.md in report_dir.

        Returns
        -------
        str absolute path, or None if not found
        """
        if not os.path.isdir(self.report_dir):
            return None
        try:
            candidates = [
                f for f in os.listdir(self.report_dir)
                if f.startswith("intraday_pipeline_report_") and f.endswith(".md")
            ]
            if not candidates:
                return None
            candidates.sort(reverse=True)
            return os.path.join(self.report_dir, candidates[0])
        except Exception as exc:
            logger.warning("load_latest_report_path: %s", exc)
            return None
