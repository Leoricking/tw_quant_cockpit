"""report_pack/report_collector.py — ReportCollector for TW Quant Cockpit v0.5.4.

Scans known output locations to determine status of each report type.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import glob
import logging
import os
from datetime import datetime
from typing import List, Optional

from report_pack.report_pack_schema import (
    ReportPackItem,
    STATUS_READY, STATUS_MISSING, STATUS_FAILED,
    REPORT_DAILY_MARKET, REPORT_AUTO_REPORT, REPORT_DATA_QUALITY,
    REPORT_PROVIDER, REPORT_STRATEGY_FILTER, REPORT_SIGNAL_QUALITY,
    REPORT_RULE_GOVERNANCE, REPORT_PORTFOLIO_JOURNAL, REPORT_RESEARCH_REVIEW,
    REPORT_RESEARCH_COACH, REPORT_RESEARCH_WORKFLOW, REPORT_RESEARCH_OS,
    REPORT_REGRESSION, REPORT_CLI_UX, REPORT_GUI_NAVIGATION,
    REPORT_NOTIFICATION, REPORT_INTRADAY_REPLAY, REPORT_EXPERIMENT,
    REPORT_RELEASE, REPORT_SAFETY,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Pattern map: report_type -> list of glob patterns (relative to BASE_DIR)
# ---------------------------------------------------------------------------
_REPORT_PATTERNS = {
    REPORT_DAILY_MARKET:      ["reports/auto_report_center/*/daily_market_summary*.md",
                                "reports/auto_report_center/*/executive_summary.md"],
    REPORT_AUTO_REPORT:       ["reports/auto_report_center/*/index.md"],
    REPORT_DATA_QUALITY:      ["reports/data_quality_gate_report*.md",
                                "data/backtest_results/data_quality_gate*.csv"],
    REPORT_PROVIDER:          ["reports/provider_reliability_report*.md",
                                "data/backtest_results/provider_reliability*.csv"],
    REPORT_STRATEGY_FILTER:   ["reports/strategy_filter_report*.md",
                                "data/backtest_results/strategy_filter_pack*.csv"],
    REPORT_SIGNAL_QUALITY:    ["reports/signal_quality_report*.md",
                                "data/backtest_results/signal_quality*.csv"],
    REPORT_RULE_GOVERNANCE:   ["reports/rule_governance_report*.md",
                                "data/backtest_results/governance*.csv"],
    REPORT_PORTFOLIO_JOURNAL: ["reports/portfolio_journal_report*.md",
                                "data/backtest_results/portfolio_journal_summary.csv"],
    REPORT_RESEARCH_REVIEW:   ["reports/research_review_report*.md",
                                "data/backtest_results/research_review*.csv"],
    REPORT_RESEARCH_COACH:    ["reports/research_coach_report*.md",
                                "data/backtest_results/research_coach*.csv"],
    REPORT_RESEARCH_WORKFLOW: ["reports/research_workflow_report*.md",
                                "data/backtest_results/research_workflow*.csv"],
    REPORT_RESEARCH_OS:       ["reports/research_os_report*.md",
                                "data/backtest_results/research_os*.csv"],
    REPORT_REGRESSION:        ["data/backtest_results/regression/regression_summary*.csv",
                                "data/backtest_results/regression/regression_results*.csv"],
    REPORT_CLI_UX:            ["reports/cli_ux_report*.md",
                                "data/backtest_results/cli_ux*.csv"],
    REPORT_GUI_NAVIGATION:    ["reports/gui_navigation_report*.md",
                                "data/backtest_results/gui_navigation*.csv"],
    REPORT_NOTIFICATION:      ["reports/notification_center_report*.md",
                                "data/backtest_results/notification*.csv"],
    REPORT_INTRADAY_REPLAY:   ["reports/intraday_replay_report*.md",
                                "data/backtest_results/intraday_replay*.csv"],
    REPORT_EXPERIMENT:        ["reports/experiment_registry_report*.md",
                                "data/backtest_results/experiment*.csv"],
    REPORT_RELEASE:           ["reports/stable_release_checklist_report*.md",
                                "data/backtest_results/stable_release_checklist*.csv"],
    REPORT_SAFETY:            ["reports/stable_release_checklist_report*.md"],
}


class ReportCollector:
    """Scans output directories to collect report status for each report type.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, base_dir: Optional[str] = None) -> None:
        self.base_dir = base_dir or BASE_DIR

    def collect(self, report_types: List[str], report_date: Optional[str] = None) -> List[ReportPackItem]:
        """Collect status for each report_type. Returns list of ReportPackItem."""
        today = report_date or datetime.now().strftime("%Y-%m-%d")
        items: List[ReportPackItem] = []
        for rt in report_types:
            item = self._collect_one(rt, today)
            items.append(item)
        return items

    def _collect_one(self, report_type: str, report_date: str) -> ReportPackItem:
        """Check file system for a given report type."""
        try:
            patterns = _REPORT_PATTERNS.get(report_type, [])
            found_path = ""
            found_size = 0

            for pattern in patterns:
                full_pattern = os.path.join(self.base_dir, pattern)
                matches = sorted(glob.glob(full_pattern))
                if matches:
                    found_path = matches[-1]
                    try:
                        found_size = os.path.getsize(found_path)
                    except Exception:
                        found_size = 0
                    break

            if found_path and found_size > 0:
                return ReportPackItem(
                    report_type=report_type,
                    status=STATUS_READY,
                    path=found_path,
                    report_date=report_date,
                    size_bytes=found_size,
                    generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            return ReportPackItem(
                report_type=report_type,
                status=STATUS_MISSING,
                report_date=report_date,
                notes=f"No output found for {report_type}",
            )
        except Exception as exc:
            logger.warning("ReportCollector._collect_one(%s) failed: %s", report_type, exc)
            return ReportPackItem(
                report_type=report_type,
                status=STATUS_FAILED,
                report_date=report_date,
                error=str(exc),
            )
