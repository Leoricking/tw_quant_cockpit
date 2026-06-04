"""report_pack/report_registry.py — ReportRegistry for TW Quant Cockpit v0.5.4.

Defines which report types are included in each pack type (daily/weekly/full).

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Dict, List

from report_pack.report_pack_schema import (
    PACK_DAILY, PACK_WEEKLY, PACK_FULL, PACK_CUSTOM,
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
# Pack definitions: which report types are included per pack type
# ---------------------------------------------------------------------------

_PACK_DEFINITIONS: Dict[str, List[str]] = {
    PACK_DAILY: [
        REPORT_DAILY_MARKET,
        REPORT_AUTO_REPORT,
        REPORT_DATA_QUALITY,
        REPORT_PROVIDER,
        REPORT_SIGNAL_QUALITY,
        REPORT_PORTFOLIO_JOURNAL,
        REPORT_NOTIFICATION,
        REPORT_RESEARCH_COACH,
        REPORT_STRATEGY_FILTER,
        REPORT_DATA_STABILIZATION,
    ],
    PACK_WEEKLY: [
        REPORT_DAILY_MARKET,
        REPORT_AUTO_REPORT,
        REPORT_DATA_QUALITY,
        REPORT_PROVIDER,
        REPORT_SIGNAL_QUALITY,
        REPORT_PORTFOLIO_JOURNAL,
        REPORT_NOTIFICATION,
        REPORT_RESEARCH_COACH,
        REPORT_STRATEGY_FILTER,
        REPORT_RULE_GOVERNANCE,
        REPORT_RESEARCH_REVIEW,
        REPORT_RESEARCH_WORKFLOW,
        REPORT_RESEARCH_OS,
        REPORT_CLI_UX,
        REPORT_GUI_NAVIGATION,
        REPORT_EXPERIMENT,
        REPORT_DATA_STABILIZATION,
    ],
    PACK_FULL: [
        REPORT_DAILY_MARKET,
        REPORT_AUTO_REPORT,
        REPORT_DATA_QUALITY,
        REPORT_PROVIDER,
        REPORT_SIGNAL_QUALITY,
        REPORT_PORTFOLIO_JOURNAL,
        REPORT_NOTIFICATION,
        REPORT_RESEARCH_COACH,
        REPORT_STRATEGY_FILTER,
        REPORT_RULE_GOVERNANCE,
        REPORT_RESEARCH_REVIEW,
        REPORT_RESEARCH_WORKFLOW,
        REPORT_RESEARCH_OS,
        REPORT_CLI_UX,
        REPORT_GUI_NAVIGATION,
        REPORT_EXPERIMENT,
        REPORT_REGRESSION,
        REPORT_INTRADAY_REPLAY,
        REPORT_RELEASE,
        REPORT_SAFETY,
        REPORT_DATA_STABILIZATION,
    ],
}

# Display metadata per pack type
_PACK_META: Dict[str, dict] = {
    PACK_DAILY: {
        "display_name": "Daily Research Pack",
        "description":  "Core daily research reports: market, signals, data quality, portfolio",
        "report_count": len(_PACK_DEFINITIONS[PACK_DAILY]),
    },
    PACK_WEEKLY: {
        "display_name": "Weekly Research Pack",
        "description":  "Weekly review + daily pack: strategy, governance, workflow, OS, CLI/GUI",
        "report_count": len(_PACK_DEFINITIONS[PACK_WEEKLY]),
    },
    PACK_FULL: {
        "display_name": "Full Research Pack",
        "description":  "All 20 report types: weekly + regression, replay, release, safety",
        "report_count": len(_PACK_DEFINITIONS[PACK_FULL]),
    },
}


class ReportRegistry:
    """Registry of report pack definitions.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def get_report_types(self, pack_type: str) -> List[str]:
        """Return ordered list of report types for a pack type."""
        return list(_PACK_DEFINITIONS.get(pack_type, []))

    def get_pack_meta(self, pack_type: str) -> dict:
        """Return display metadata for a pack type."""
        return dict(_PACK_META.get(pack_type, {}))

    def list_pack_types(self) -> List[str]:
        """Return all supported pack types."""
        return [PACK_DAILY, PACK_WEEKLY, PACK_FULL, PACK_CUSTOM]

    def pack_type_display(self, pack_type: str) -> str:
        meta = _PACK_META.get(pack_type, {})
        return meta.get("display_name", pack_type.title())
