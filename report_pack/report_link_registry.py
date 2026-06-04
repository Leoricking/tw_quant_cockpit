"""report_pack/report_link_registry.py — ReportLinkRegistry for TW Quant Cockpit v0.5.4.

Maps each report type to its CLI command, GUI tab, and documentation links.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from report_pack.report_pack_schema import (
    REPORT_DAILY_MARKET, REPORT_AUTO_REPORT, REPORT_DATA_QUALITY,
    REPORT_PROVIDER, REPORT_STRATEGY_FILTER, REPORT_SIGNAL_QUALITY,
    REPORT_RULE_GOVERNANCE, REPORT_PORTFOLIO_JOURNAL, REPORT_RESEARCH_REVIEW,
    REPORT_RESEARCH_COACH, REPORT_RESEARCH_WORKFLOW, REPORT_RESEARCH_OS,
    REPORT_REGRESSION, REPORT_CLI_UX, REPORT_GUI_NAVIGATION,
    REPORT_NOTIFICATION, REPORT_INTRADAY_REPLAY, REPORT_EXPERIMENT,
    REPORT_RELEASE, REPORT_SAFETY, REPORT_DATA_STABILIZATION,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Link definitions per report type
# ---------------------------------------------------------------------------
_LINK_MAP: Dict[str, dict] = {
    REPORT_DAILY_MARKET: {
        "cli_commands":  ["auto-report --profile daily"],
        "gui_tab":       "daily_workflow",
        "doc_path":      "docs/auto_report_center.md",
        "description":   "Daily market summary and executive overview",
    },
    REPORT_AUTO_REPORT: {
        "cli_commands":  ["auto-report", "auto-report --profile full"],
        "gui_tab":       "daily_workflow",
        "doc_path":      "docs/auto_report_center.md",
        "description":   "Comprehensive auto report center output",
    },
    REPORT_DATA_QUALITY: {
        "cli_commands":  ["data-quality-gate"],
        "gui_tab":       "data_quality",
        "doc_path":      "docs/data_quality.md",
        "description":   "Data quality gate report",
    },
    REPORT_PROVIDER: {
        "cli_commands":  ["provider-reliability"],
        "gui_tab":       "provider",
        "doc_path":      "docs/provider_reliability.md",
        "description":   "Data provider reliability report",
    },
    REPORT_STRATEGY_FILTER: {
        "cli_commands":  ["strategy-filter-pack", "strategy-filter --report"],
        "gui_tab":       "strategy_filter",
        "doc_path":      "docs/strategy_filter.md",
        "description":   "Strategy filter and signal pack report",
    },
    REPORT_SIGNAL_QUALITY: {
        "cli_commands":  ["signal-quality-report"],
        "gui_tab":       "signal_quality",
        "doc_path":      "docs/signal_quality.md",
        "description":   "Signal quality and factor analysis report",
    },
    REPORT_RULE_GOVERNANCE: {
        "cli_commands":  ["rule-governance-report"],
        "gui_tab":       "rule_governance",
        "doc_path":      "docs/rule_governance.md",
        "description":   "Rule governance and compliance report",
    },
    REPORT_PORTFOLIO_JOURNAL: {
        "cli_commands":  ["journal-summary", "journal-report"],
        "gui_tab":       "portfolio_journal",
        "doc_path":      "docs/portfolio_journal.md",
        "description":   "Portfolio journal and trade review report",
    },
    REPORT_RESEARCH_REVIEW: {
        "cli_commands":  ["research-review-summary", "research-review-report"],
        "gui_tab":       "research_review",
        "doc_path":      "docs/research_review.md",
        "description":   "Research review dashboard report",
    },
    REPORT_RESEARCH_COACH: {
        "cli_commands":  ["research-coach-summary", "research-coach-report"],
        "gui_tab":       "research_coach",
        "doc_path":      "docs/research_coach.md",
        "description":   "Research coach and feedback report",
    },
    REPORT_RESEARCH_WORKFLOW: {
        "cli_commands":  ["research-workflow-summary", "research-workflow-report"],
        "gui_tab":       "research_workflow",
        "doc_path":      "docs/research_workflow.md",
        "description":   "Research workflow automation report",
    },
    REPORT_RESEARCH_OS: {
        "cli_commands":  ["research-os-summary", "research-os-report"],
        "gui_tab":       "research_os",
        "doc_path":      "docs/research_os.md",
        "description":   "Research OS planning report",
    },
    REPORT_REGRESSION: {
        "cli_commands":  ["regression-run", "regression-report"],
        "gui_tab":       "regression_suite",
        "doc_path":      "docs/regression_suite_consolidation.md",
        "description":   "Regression suite consolidation report",
    },
    REPORT_CLI_UX: {
        "cli_commands":  ["cli-ux-report", "cli-list"],
        "gui_tab":       "cli_ux",
        "doc_path":      "docs/cli_ux.md",
        "description":   "CLI UX and command registry report",
    },
    REPORT_GUI_NAVIGATION: {
        "cli_commands":  ["gui-nav-report", "gui-nav-summary"],
        "gui_tab":       "gui_navigation",
        "doc_path":      "docs/gui_tab_grouping_navigation.md",
        "description":   "GUI navigation and tab registry report",
    },
    REPORT_NOTIFICATION: {
        "cli_commands":  ["notification-list", "notification-report"],
        "gui_tab":       "notification",
        "doc_path":      "docs/notification_center.md",
        "description":   "Notification center report",
    },
    REPORT_INTRADAY_REPLAY: {
        "cli_commands":  ["intraday-replay-report"],
        "gui_tab":       "intraday_replay",
        "doc_path":      "docs/intraday_replay.md",
        "description":   "Intraday replay and simulation report",
    },
    REPORT_EXPERIMENT: {
        "cli_commands":  ["experiment-registry"],
        "gui_tab":       "experiment_registry",
        "doc_path":      "docs/experiment_registry.md",
        "description":   "Experiment registry and hypothesis tracking",
    },
    REPORT_RELEASE: {
        "cli_commands":  ["stable-release-check"],
        "gui_tab":       "release_status",
        "doc_path":      "docs/release_notes_v0.5.md",
        "description":   "Stable release checklist report",
    },
    REPORT_SAFETY: {
        "cli_commands":  ["stable-release-check", "regression-run --suite safety"],
        "gui_tab":       "release_status",
        "doc_path":      "docs/release_notes_v0.5.md",
        "description":   "Safety checks and no-real-orders verification",
    },
    REPORT_DATA_STABILIZATION: {
        "cli_commands":  [
            "data-stabilization --mode real",
            "data-stabilization-report --mode real",
            "data-stabilization-summary",
            "data-lineage",
            "feature-readiness",
            "feature-store-health",
            "leakage-guard",
        ],
        "gui_tab":       "data_stabilization",
        "doc_path":      "docs/data_feature_store_stabilization.md",
        "description":   "Data / Feature Store Stabilization — schema, lineage, readiness, health, leakage",
    },
}


class ReportLinkRegistry:
    """Maps report types to CLI commands, GUI tabs, and documentation.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def get_links(self, report_type: str) -> dict:
        """Return link dict for a report type, or empty dict."""
        return dict(_LINK_MAP.get(report_type, {}))

    def get_cli_commands(self, report_type: str) -> List[str]:
        return list(_LINK_MAP.get(report_type, {}).get("cli_commands", []))

    def get_gui_tab(self, report_type: str) -> str:
        return _LINK_MAP.get(report_type, {}).get("gui_tab", "")

    def get_doc_path(self, report_type: str) -> str:
        return _LINK_MAP.get(report_type, {}).get("doc_path", "")

    def all_report_types(self) -> List[str]:
        return list(_LINK_MAP.keys())

    def build_link_index(self) -> List[dict]:
        """Return full link index as list of dicts."""
        return [
            {
                "report_type":   rt,
                "cli_commands":  info.get("cli_commands", []),
                "gui_tab":       info.get("gui_tab", ""),
                "doc_path":      info.get("doc_path", ""),
                "description":   info.get("description", ""),
            }
            for rt, info in _LINK_MAP.items()
        ]
