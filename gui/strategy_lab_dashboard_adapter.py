# gui/strategy_lab_dashboard_adapter.py
# TW Quant Cockpit — Strategy Lab Dashboard GUI Adapter
# v0.9.3 — Research Only / No Real Orders / Production Trading BLOCKED
#
# DISCLAIMER: Research purposes ONLY. No real orders. Production trading BLOCKED.

from __future__ import annotations

import logging
import os
from typing import List

logger = logging.getLogger(__name__)

VERSION = "v0.9.3"

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _as_list(obj) -> list:
    if isinstance(obj, list):
        return obj
    if obj is None:
        return []
    return [obj]


def _to_dict(obj) -> dict:
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return {}


def _to_dicts(objs) -> list:
    return [_to_dict(o) for o in _as_list(objs)]


class StrategyLabDashboardAdapter:
    """
    GUI ↔ backend bridge for StrategyLabDashboard package.

    All methods catch exceptions and return safe defaults.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    _FORBIDDEN = frozenset([
        "BUY", "SELL", "ORDER", "EXECUTE",
        "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
    ])

    def __init__(
        self,
        output_dir: str = "data/backtest_results/strategy_lab_dashboard",
        report_dir: str = "reports",
    ) -> None:
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(_BASE_DIR, output_dir)
        self._output_dir = output_dir
        if not os.path.isabs(report_dir):
            report_dir = os.path.join(_BASE_DIR, report_dir)
        self._report_dir = report_dir

    # ------------------------------------------------------------------
    # Engine
    # ------------------------------------------------------------------

    def run_dashboard(self, mode: str = "real") -> dict:
        """Run StrategyLabDashboardEngine and return result dict."""
        try:
            from strategy_lab.strategy_lab_dashboard_engine import StrategyLabDashboardEngine
            engine = StrategyLabDashboardEngine(output_dir=self._output_dir)
            result = engine.run(mode=mode)
            if not isinstance(result, dict):
                result = {}
            return result
        except Exception as exc:
            logger.warning("StrategyLabDashboardAdapter.run_dashboard: %s", exc)
            return {"error": str(exc), "no_real_orders": True, "production_blocked": True}

    def generate_report(self, mode: str = "real") -> str:
        """Generate the Strategy Lab Dashboard report and return file path."""
        try:
            from reports.strategy_lab_dashboard_report import StrategyLabDashboardReportBuilder
            builder = StrategyLabDashboardReportBuilder(
                output_dir=self._output_dir,
                report_dir=self._report_dir,
            )
            return builder.build(mode=mode)
        except Exception as exc:
            logger.warning("StrategyLabDashboardAdapter.generate_report: %s", exc)
            return ""

    # ------------------------------------------------------------------
    # Store queries
    # ------------------------------------------------------------------

    def _get_store(self):
        try:
            from strategy_lab.strategy_lab_dashboard_store import StrategyLabDashboardStore
            return StrategyLabDashboardStore(output_dir=self._output_dir)
        except Exception:
            return None

    def load_latest_summary(self) -> dict:
        store = self._get_store()
        if store is None:
            return {}
        summary = store.load_latest_summary()
        return _to_dict(summary)

    def load_cards(self) -> list:
        store = self._get_store()
        if store is None:
            return []
        return _to_dicts(store.load_latest_cards())

    def load_rows(self) -> list:
        store = self._get_store()
        if store is None:
            return []
        return _to_dicts(store.load_latest_rows())

    def load_actions(self) -> list:
        store = self._get_store()
        if store is None:
            return []
        return _to_dicts(store.load_latest_actions())

    def top_priorities(self, limit: int = 10) -> list:
        try:
            from strategy_lab.strategy_lab_dashboard_query import StrategyLabDashboardQuery
            store = self._get_store()
            q = StrategyLabDashboardQuery(store=store)
            return _to_dicts(q.top_priorities(limit=limit))
        except Exception as exc:
            logger.warning("StrategyLabDashboardAdapter.top_priorities: %s", exc)
            return []
