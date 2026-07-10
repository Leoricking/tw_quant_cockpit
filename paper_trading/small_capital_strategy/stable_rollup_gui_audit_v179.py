"""
paper_trading/small_capital_strategy/stable_rollup_gui_audit_v179.py
GUI audit for Small Capital Strategy Stable Rollup v1.7.9.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "179"
_POLICY  = "1.7.9-small-capital-strategy-stable-rollup"

_REQUIRED_STABLE_TABS: List[str] = [
    "stable_rollup",
    "stable_health",
    "stable_report",
]


def run_gui_audit() -> Dict[str, Any]:
    """Audit GUI panel for stable rollup tabs and no error strings."""
    from gui.small_capital_strategy_panel import _TABS, render_all_tabs, PANEL_VERSION
    missing_tabs = [t for t in _REQUIRED_STABLE_TABS if t not in _TABS]
    tabs_present = [t for t in _REQUIRED_STABLE_TABS if t in _TABS]
    all_tabs_present = len(missing_tabs) == 0

    # Check render_all_tabs has no error strings
    rendered = render_all_tabs()
    error_tabs = [
        k for k, v in rendered.items()
        if isinstance(v, dict) and v.get("error") is not None
    ]
    render_clean = len(error_tabs) == 0

    return {
        "all_tabs_present": all_tabs_present,
        "render_clean": render_clean,
        "panel_version": PANEL_VERSION,
        "total_tabs": len(_TABS),
        "stable_tabs_present": tabs_present,
        "missing_tabs": missing_tabs,
        "error_tabs": error_tabs,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def get_required_stable_tabs() -> List[str]:
    return list(_REQUIRED_STABLE_TABS)
