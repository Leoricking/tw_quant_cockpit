"""
gui/hardened_backtest_adapter.py — GUI bridge for HardenedBacktester (v0.3.26).

No subprocess. Direct Python call.

[!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import json
import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class HardenedBacktestAdapter:
    """
    GUI bridge for the HardenedBacktester.

    Provides a clean interface between the GUI panel and the backtest engine.
    Uses direct Python calls (no subprocess).

    [!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only = True
    no_real_orders = True
    production_blocked = True

    def __init__(
        self,
        results_dir: str = "data/backtest_results",
        report_dir: str = "reports",
    ) -> None:
        self.results_dir = os.path.join(BASE_DIR, results_dir)
        self.report_dir = os.path.join(BASE_DIR, report_dir)

    # ------------------------------------------------------------------
    # Run backtest
    # ------------------------------------------------------------------

    def run_backtest(
        self,
        mode: str = "real",
        entry_model: str = "next_open",
        exit_model: str = "combined",
        cost_model: str = "taiwan_realistic",
        split_method: str = "walk_forward",
        max_holding_days: int = 20,
        zero_cost: bool = False,
    ) -> dict:
        """
        Instantiate HardenedBacktester and run it.

        Returns result dict; on exception returns error dict.
        """
        try:
            from backtest.hardened_backtester import HardenedBacktester
            backtester = HardenedBacktester(
                mode=mode,
                entry_model=entry_model,
                exit_model=exit_model,
                cost_model=cost_model,
                split_method=split_method,
                max_holding_days=max_holding_days,
                zero_cost=zero_cost,
                results_dir=os.path.relpath(self.results_dir, BASE_DIR),
                report_dir=os.path.relpath(self.report_dir, BASE_DIR),
            )
            result = backtester.run()
            return result
        except Exception as exc:
            logger.error("HardenedBacktestAdapter.run_backtest error: %s", exc, exc_info=True)
            return {
                "status": "ERROR",
                "error": str(exc),
                "note": "Research Only / Backtest Only / No Real Orders. Production Trading: BLOCKED.",
            }

    # ------------------------------------------------------------------
    # Generate report
    # ------------------------------------------------------------------

    def generate_report(
        self,
        mode: str = "real",
        backtest_result: dict | None = None,
    ) -> str:
        """
        Generate the hardened backtest report.

        If backtest_result is None, loads from latest metrics file.
        Returns path to report; on exception returns error string.
        """
        try:
            from reports.hardened_backtest_report import HardenedBacktestReportBuilder

            if backtest_result is None:
                backtest_result = self.load_latest_metrics()

            builder = HardenedBacktestReportBuilder(
                backtest_result=backtest_result,
                mode=mode,
            )
            path = builder.build(output_dir=self.report_dir)
            logger.info("HardenedBacktestAdapter.generate_report: %s", path)
            return path
        except Exception as exc:
            logger.error("HardenedBacktestAdapter.generate_report error: %s", exc, exc_info=True)
            return f"ERROR generating report: {exc}"

    # ------------------------------------------------------------------
    # Load latest data
    # ------------------------------------------------------------------

    def load_latest_metrics(self) -> dict:
        """
        Read hardened_backtest_metrics.csv from results_dir.

        Returns dict or {} if file missing.
        """
        metrics_path = os.path.join(self.results_dir, "hardened_backtest_metrics.csv")
        if not os.path.exists(metrics_path):
            logger.warning("load_latest_metrics: file not found at %s", metrics_path)
            return {}
        try:
            # Read without pandas dependency if possible
            try:
                import pandas as pd
                df = pd.read_csv(metrics_path)
                if df.empty:
                    return {}
                return df.iloc[0].to_dict()
            except ImportError:
                import csv
                with open(metrics_path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        return dict(row)
                return {}
        except Exception as exc:
            logger.error("load_latest_metrics error: %s", exc)
            return {}

    def load_latest_report_path(self) -> str | None:
        """
        Find the most recent hardened_backtest_report_*.md in report_dir.

        Returns path or None.
        """
        try:
            if not os.path.exists(self.report_dir):
                return None
            candidates = [
                f for f in os.listdir(self.report_dir)
                if f.startswith("hardened_backtest_report_") and f.endswith(".md")
            ]
            if not candidates:
                return None
            candidates.sort(reverse=True)
            return os.path.join(self.report_dir, candidates[0])
        except Exception as exc:
            logger.error("load_latest_report_path error: %s", exc)
            return None

    def load_latest_assumptions(self) -> dict:
        """
        Read hardened_backtest_assumptions.json from results_dir.

        Returns dict or {}.
        """
        assumptions_path = os.path.join(self.results_dir, "hardened_backtest_assumptions.json")
        if not os.path.exists(assumptions_path):
            logger.warning("load_latest_assumptions: file not found at %s", assumptions_path)
            return {}
        try:
            with open(assumptions_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.error("load_latest_assumptions error: %s", exc)
            return {}
