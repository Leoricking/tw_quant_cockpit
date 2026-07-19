"""
paper_trading/small_capital_strategy/portfolio_governance_gui_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — GUI Panel
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
PANEL_VERSION = "1.9.8"
PANEL_TITLE = "Paper Portfolio Governance & Risk Overlay Lab v1.9.8"
PANEL_SCHEMA_VERSION = "198"

_GOVERNANCE_TAB_NAMES = [
    "portfolio_governance",
    "risk_overlay",
    "exposure_dashboard",
]

_PAPER_HEADER = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "portfolio_governance_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "not_investment_advice": True,
    "dashboard_mutates_strategy": False,
    "overlay_places_real_order": False,
    "report_triggers_rebalance": False,
}

# Tab count includes all tabs from v1.0 through v1.9.8
_TOTAL_TAB_COUNT = 166


def get_panel_info() -> dict:
    return {
        "panel_version": PANEL_VERSION,
        "panel_title": PANEL_TITLE,
        "panel_schema_version": PANEL_SCHEMA_VERSION,
        "tab_count": _TOTAL_TAB_COUNT,
        "governance_tab_names": _GOVERNANCE_TAB_NAMES,
        "governance_tab_count": len(_GOVERNANCE_TAB_NAMES),
        **_PAPER_HEADER,
    }


def render_portfolio_governance_tab(portfolio: dict = None, grade: str = "LOW", recs: list = None) -> dict:
    return {
        "tab": "portfolio_governance",
        "portfolio": portfolio or {},
        "grade": grade,
        "recommendations": recs or [],
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "portfolio_governance_only": True,
        "dashboard_mutates_strategy": False,
        "not_investment_advice": True,
        "schema_version": PANEL_SCHEMA_VERSION,
    }


def render_risk_overlay_tab(candidate: str = "", overlay_result: dict = None) -> dict:
    return {
        "tab": "risk_overlay",
        "candidate": candidate,
        "overlay_result": overlay_result or {},
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "risk_overlay_only": True,
        "dashboard_mutates_strategy": False,
        "overlay_places_real_order": False,
        "not_investment_advice": True,
        "schema_version": PANEL_SCHEMA_VERSION,
    }


def render_exposure_dashboard_tab(exposure: dict = None, concentration: dict = None) -> dict:
    return {
        "tab": "exposure_dashboard",
        "exposure": exposure or {},
        "concentration": concentration or {},
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "exposure_dashboard_only": True,
        "dashboard_mutates_strategy": False,
        "not_investment_advice": True,
        "schema_version": PANEL_SCHEMA_VERSION,
    }


def get_governance_portfolio_tab_names() -> list:
    return list(_GOVERNANCE_TAB_NAMES)


def render_all_tabs(portfolio: dict = None, candidate: str = "", exposure: dict = None) -> dict:
    return {
        "portfolio_governance": render_portfolio_governance_tab(portfolio),
        "risk_overlay": render_risk_overlay_tab(candidate),
        "exposure_dashboard": render_exposure_dashboard_tab(exposure),
        "tab_count": _TOTAL_TAB_COUNT,
        **_PAPER_HEADER,
    }
