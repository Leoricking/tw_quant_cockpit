"""
gui/gui_navigation_adapter.py — GUINavigationAdapter for TW Quant Cockpit v0.5.2.

Adapter bridging the GUI navigation panel and the underlying registry/report modules.

[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import glob
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GUINavigationAdapter:
    """Adapter for GUI Navigation data — used by CLI commands and GUI panel.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        report_dir: str = "reports",
        output_dir: str = "data/backtest_results/gui_navigation",
    ) -> None:
        self.report_dir = os.path.join(BASE_DIR, report_dir) if not os.path.isabs(report_dir) else report_dir
        self.output_dir = os.path.join(BASE_DIR, output_dir) if not os.path.isabs(output_dir) else output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_registry(self) -> dict:
        """Return registry summary dict from GUINavigationReportData.build_summary()."""
        try:
            from gui.navigation.tab_registry import GUITabRegistry
            from gui.navigation.navigation_report_data import GUINavigationReportData
            reg  = GUITabRegistry()
            data = GUINavigationReportData(registry=reg)
            return data.build_summary()
        except Exception as exc:
            logger.error("GUINavigationAdapter.build_registry: %s", exc)
            return {
                "total_tabs":    0,
                "groups_count":  0,
                "safety_status": "ERROR",
                "error":         str(exc),
            }

    def search_tabs(self, query: str) -> List[dict]:
        """Return list of matching tabs from GUITabSearch.search(query)."""
        try:
            from gui.navigation.tab_search import GUITabSearch
            return GUITabSearch().search(query)
        except Exception as exc:
            logger.error("GUINavigationAdapter.search_tabs: %s", exc)
            return []

    def generate_report(self, mode: str = "real") -> str:
        """Generate GUI navigation report. Returns path to generated file."""
        try:
            from reports.gui_navigation_report import GUINavigationReport
            rpt  = GUINavigationReport(report_dir=self.report_dir, mode=mode)
            path = rpt.generate(mode=mode)
            return path
        except Exception as exc:
            logger.error("GUINavigationAdapter.generate_report: %s", exc)
            return ""

    def load_latest_summary(self) -> Optional[dict]:
        """Return the latest registry summary dict or None."""
        try:
            return self.build_registry()
        except Exception as exc:
            logger.warning("GUINavigationAdapter.load_latest_summary: %s", exc)
            return None

    def load_latest_report_path(self) -> str:
        """Return path to the latest gui_navigation_report_*.md or empty string."""
        try:
            pattern = os.path.join(self.report_dir, "gui_navigation_report_*.md")
            matches = sorted(glob.glob(pattern))
            return matches[-1] if matches else ""
        except Exception as exc:
            logger.warning("GUINavigationAdapter.load_latest_report_path: %s", exc)
            return ""
