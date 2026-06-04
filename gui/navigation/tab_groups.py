"""
gui/navigation/tab_groups.py — GUITabGroupConfig for TW Quant Cockpit v0.5.2.

Hardcoded group definitions: 8 tab groups with display name, order, description.

[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


_GROUPS = [
    {
        "group_id":    "daily_research",
        "display_name": "Daily Research",
        "order":       1,
        "description": "Daily research workflow, reports, coaching, review",
    },
    {
        "group_id":    "data_providers",
        "display_name": "Data & Providers",
        "order":       2,
        "description": "API fetch, provider health, data quality, universe",
    },
    {
        "group_id":    "strategy_rules",
        "display_name": "Strategy & Rules",
        "order":       3,
        "description": "Strategy filter, rule governance, signal quality, strategy knowledge, ML",
    },
    {
        "group_id":    "backtest_simulation",
        "display_name": "Backtest & Simulation",
        "order":       4,
        "description": "Hardened backtest, portfolio cockpit, intraday replay",
    },
    {
        "group_id":    "ml_monitoring",
        "display_name": "ML & Monitoring",
        "order":       5,
        "description": "ML feature store, model monitoring",
    },
    {
        "group_id":    "journal_review",
        "display_name": "Journal & Review",
        "order":       6,
        "description": "Portfolio journal, experiment registry",
    },
    {
        "group_id":    "research_os",
        "display_name": "Research OS",
        "order":       7,
        "description": "OS planning, CLI UX, GUI navigation",
    },
    {
        "group_id":    "release_qa",
        "display_name": "Release & QA",
        "order":       8,
        "description": "Release status, usability QA",
    },
]


class GUITabGroupConfig:
    """Hardcoded tab group definitions for TW Quant Cockpit v0.5.2.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def list_groups(self) -> List[dict]:
        """Return all group definitions as a list of dicts."""
        return list(_GROUPS)

    def get_group(self, group_id: str) -> Optional[dict]:
        """Return a single group definition by group_id or None."""
        for g in _GROUPS:
            if g["group_id"] == group_id:
                return dict(g)
        return None

    def get_ordered_groups(self) -> List[dict]:
        """Return groups sorted by order field."""
        return sorted(_GROUPS, key=lambda g: g["order"])
