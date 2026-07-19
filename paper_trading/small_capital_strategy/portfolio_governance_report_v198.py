"""
paper_trading/small_capital_strategy/portfolio_governance_report_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Report
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
REPORT_SECTIONS = [
    "portfolio_snapshot",
    "exposure_summary",
    "theme_risk_analysis",
    "industry_risk_analysis",
    "strategy_risk_analysis",
    "concentration_risk",
    "correlation_risk",
    "risk_limits_evaluation",
    "risk_score_and_grade",
    "governance_recommendations",
    "risk_overlay_decisions",
    "audit_trail",
]

_PAPER_HEADER = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "portfolio_governance_only": True,
    "risk_overlay_only": True,
    "dashboard_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "not_investment_advice": True,
    "report_triggers_rebalance": False,
    "dashboard_mutates_strategy": False,
}


def export_portfolio_snapshot(snapshot: dict) -> dict:
    return {"section": "portfolio_snapshot", "data": snapshot, **_PAPER_HEADER}


def export_exposure_summary(exposure: dict) -> dict:
    return {"section": "exposure_summary", "data": exposure, **_PAPER_HEADER}


def export_theme_risk(theme_exposures: list) -> dict:
    return {"section": "theme_risk_analysis", "data": theme_exposures, **_PAPER_HEADER}


def export_industry_risk(industry_exposures: list) -> dict:
    return {"section": "industry_risk_analysis", "data": industry_exposures, **_PAPER_HEADER}


def export_concentration_risk(concentration: dict) -> dict:
    return {"section": "concentration_risk", "data": concentration, **_PAPER_HEADER}


def export_correlation_risk(correlation: dict) -> dict:
    return {"section": "correlation_risk", "data": correlation, **_PAPER_HEADER}


def export_risk_limits(limits_result: dict) -> dict:
    return {"section": "risk_limits_evaluation", "data": limits_result, **_PAPER_HEADER}


def export_risk_score_and_grade(score: float, grade: str) -> dict:
    return {"section": "risk_score_and_grade", "score": score, "grade": grade, **_PAPER_HEADER}


def export_recommendations(recs: list) -> dict:
    return {"section": "governance_recommendations", "recommendations": recs, **_PAPER_HEADER}


def export_risk_overlay_decisions(decisions: list) -> dict:
    return {"section": "risk_overlay_decisions", "decisions": decisions, **_PAPER_HEADER}


def export_audit_trail(entries: list) -> dict:
    return {"section": "audit_trail", "entries": entries, "immutable": True, **_PAPER_HEADER}


def export_full_governance_pack(
    snapshot: dict = None,
    exposure: dict = None,
    theme_exposures: list = None,
    industry_exposures: list = None,
    concentration: dict = None,
    correlation: dict = None,
    limits_result: dict = None,
    score: float = 0.0,
    grade: str = "LOW",
    recs: list = None,
    decisions: list = None,
    audit_entries: list = None,
) -> dict:
    return {
        "sections": REPORT_SECTIONS,
        "section_count": len(REPORT_SECTIONS),
        "portfolio_snapshot": export_portfolio_snapshot(snapshot or {}),
        "exposure_summary": export_exposure_summary(exposure or {}),
        "theme_risk": export_theme_risk(theme_exposures or []),
        "industry_risk": export_industry_risk(industry_exposures or []),
        "concentration_risk": export_concentration_risk(concentration or {}),
        "correlation_risk": export_correlation_risk(correlation or {}),
        "risk_limits": export_risk_limits(limits_result or {}),
        "risk_score_and_grade": export_risk_score_and_grade(score, grade),
        "recommendations": export_recommendations(recs or []),
        "risk_overlay_decisions": export_risk_overlay_decisions(decisions or []),
        "audit_trail": export_audit_trail(audit_entries or []),
        **_PAPER_HEADER,
    }
