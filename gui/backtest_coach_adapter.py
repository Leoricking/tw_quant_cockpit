"""
gui/backtest_coach_adapter.py — BacktestCoachAdapter v0.7.3

Bridge between GUI and backtest_coach package.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BacktestCoachAdapter:
    """
    GUI adapter for backtest_coach package.

    All methods catch exceptions and return safe defaults.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        output_dir:  str = "data/backtest_results/backtest_coach",
        report_dir:  str = "reports",
    ):
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(_BASE_DIR, output_dir)
        if not os.path.isabs(report_dir):
            report_dir = os.path.join(_BASE_DIR, report_dir)
        self._output_dir = output_dir
        self._report_dir = report_dir

    def run_loop(self, mode: str = "real", period: str = "daily") -> dict:
        """Run full backtest coach loop. Returns result dict."""
        try:
            from backtest_coach.backtest_coach_engine import BacktestCoachEngine
            engine = BacktestCoachEngine(
                project_root=_BASE_DIR,
                output_dir=self._output_dir,
            )
            result  = engine.run(mode=mode, period=period)
            summary = result.get("summary")
            signals = result.get("signals", [])
            tasks   = result.get("tasks", [])
            daily   = result.get("daily_tasks", [])
            weekly  = result.get("weekly_tasks", [])
            summary_dict = summary.to_dict() if summary else {}
            return {
                "ok":              True,
                "summary":         summary_dict,
                "signal_count":    len(signals),
                "task_count":      len(tasks),
                "daily_count":     len(daily),
                "weekly_count":    len(weekly),
                "no_real_orders":  True,
                "production_blocked": True,
            }
        except Exception as exc:
            logger.warning("BacktestCoachAdapter.run_loop error: %s", exc)
            return {"ok": False, "error": str(exc), "no_real_orders": True, "production_blocked": True}

    def generate_report(self, mode: str = "real") -> dict:
        """Generate backtest coach Markdown report. Returns path dict."""
        try:
            from reports.backtest_coach_report import BacktestCoachReportBuilder
            builder = BacktestCoachReportBuilder()
            path = builder.build(
                mode=mode,
                output_dir=self._report_dir,
                coach_output_dir=self._output_dir,
            )
            return {
                "ok":   True,
                "path": path,
                "no_real_orders": True,
                "production_blocked": True,
            }
        except Exception as exc:
            logger.warning("BacktestCoachAdapter.generate_report error: %s", exc)
            return {"ok": False, "error": str(exc), "path": "", "no_real_orders": True}

    def load_latest_summary(self) -> dict:
        """Load latest summary as dict."""
        try:
            from backtest_coach.backtest_coach_store import BacktestCoachStore
            store   = BacktestCoachStore(output_dir=self._output_dir)
            summary = store.load_latest_summary()
            return summary.to_dict() if summary else {}
        except Exception as exc:
            logger.warning("BacktestCoachAdapter.load_latest_summary error: %s", exc)
            return {}

    def load_latest_signals(self) -> list:
        """Load latest signals as list of dicts."""
        try:
            from backtest_coach.backtest_coach_store import BacktestCoachStore
            store = BacktestCoachStore(output_dir=self._output_dir)
            return [s.to_dict() for s in store.load_signals()]
        except Exception as exc:
            logger.warning("BacktestCoachAdapter.load_latest_signals error: %s", exc)
            return []

    def load_latest_tasks(self) -> list:
        """Load latest tasks as list of dicts."""
        try:
            from backtest_coach.backtest_coach_store import BacktestCoachStore
            store = BacktestCoachStore(output_dir=self._output_dir)
            return [t.to_dict() for t in store.load_tasks()]
        except Exception as exc:
            logger.warning("BacktestCoachAdapter.load_latest_tasks error: %s", exc)
            return []

    def load_latest_daily_tasks(self) -> list:
        """Load latest daily tasks as list of dicts."""
        try:
            from backtest_coach.backtest_coach_store import BacktestCoachStore
            store = BacktestCoachStore(output_dir=self._output_dir)
            return [t.to_dict() for t in store.load_daily_tasks()]
        except Exception as exc:
            logger.warning("BacktestCoachAdapter.load_latest_daily_tasks error: %s", exc)
            return []

    def load_latest_weekly_tasks(self) -> list:
        """Load latest weekly tasks as list of dicts."""
        try:
            from backtest_coach.backtest_coach_store import BacktestCoachStore
            store = BacktestCoachStore(output_dir=self._output_dir)
            return [t.to_dict() for t in store.load_weekly_tasks()]
        except Exception as exc:
            logger.warning("BacktestCoachAdapter.load_latest_weekly_tasks error: %s", exc)
            return []

    def load_latest_report_path(self) -> str:
        """Find path to latest backtest coach report."""
        try:
            import glob
            pattern = os.path.join(self._report_dir, "backtest_coach_report_*.md")
            files = sorted(glob.glob(pattern))
            return files[-1] if files else ""
        except Exception as exc:
            logger.warning("BacktestCoachAdapter.load_latest_report_path error: %s", exc)
            return ""
