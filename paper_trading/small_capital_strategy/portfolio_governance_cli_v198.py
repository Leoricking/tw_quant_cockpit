"""
paper_trading/small_capital_strategy/portfolio_governance_cli_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — CLI
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.portfolio_governance_version_v198 import get_version_info
from paper_trading.small_capital_strategy.portfolio_governance_safety_v198 import run_safety_audit
from paper_trading.small_capital_strategy.portfolio_governance_engine_v198 import (
    validate_portfolio_input, compute_risk_score, compute_risk_grade,
    evaluate_risk_limits, detect_concentration_risk, detect_correlation_risk,
    run_risk_overlay, generate_recommendations, build_exposure_summary,
    build_portfolio_dashboard, build_governance_report, export_governance_pack,
)
from paper_trading.small_capital_strategy.portfolio_governance_report_v198 import export_full_governance_pack
from paper_trading.small_capital_strategy.portfolio_governance_scenarios_v198 import get_scenarios
from paper_trading.small_capital_strategy.portfolio_governance_fixtures_v198 import get_fixtures

_PAPER_HEADER = {
    "paper_only": True,
    "no_real_orders": True,
    "not_investment_advice": True,
    "safety_classification": "RESEARCH_ONLY",
}

CLI_COMMANDS = [
    {
        "name": "portfolio-governance-version",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Show portfolio governance version info",
    },
    {
        "name": "portfolio-governance-run",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Run portfolio governance pipeline",
    },
    {
        "name": "portfolio-governance-snapshot",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Show portfolio snapshot",
    },
    {
        "name": "portfolio-governance-exposure",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Compute portfolio exposure summary",
    },
    {
        "name": "portfolio-governance-theme-risk",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Analyze theme risk in portfolio",
    },
    {
        "name": "portfolio-governance-industry-risk",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Analyze industry risk in portfolio",
    },
    {
        "name": "portfolio-governance-correlation-risk",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Detect correlation cluster risk",
    },
    {
        "name": "portfolio-governance-risk-limits",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Evaluate all risk limits against portfolio",
    },
    {
        "name": "portfolio-governance-risk-overlay",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Run risk overlay for new candidate",
    },
    {
        "name": "portfolio-governance-risk-score",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Compute portfolio risk score and grade",
    },
    {
        "name": "portfolio-governance-recommendations",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Generate governance recommendations",
    },
    {
        "name": "portfolio-governance-dashboard",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Render portfolio governance dashboard",
    },
    {
        "name": "portfolio-governance-report",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Build full governance report",
    },
    {
        "name": "portfolio-governance-export",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Export governance pack to file",
    },
    {
        "name": "portfolio-governance-health",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Run portfolio governance health check",
    },
    {
        "name": "portfolio-governance-gate",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Run portfolio governance release gate",
    },
    {
        "name": "portfolio-governance-scenarios",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "List portfolio governance scenarios",
    },
    {
        "name": "portfolio-governance-fixtures",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "List portfolio governance fixtures",
    },
    {
        "name": "portfolio-governance-safety-audit",
        "group": "portfolio_governance",
        "introduced_in": "1.9.8",
        "safety_classification": "RESEARCH_ONLY",
        "description": "Run portfolio governance safety audit",
    },
]

assert len(CLI_COMMANDS) == 19


def _cmd_version():
    return get_version_info()


def _cmd_run(inp: dict = None):
    if inp is None:
        inp = {}
    result = validate_portfolio_input(inp)
    return {**result, **_PAPER_HEADER}


def _cmd_snapshot(snapshot: dict = None):
    return {"snapshot": snapshot or {}, **_PAPER_HEADER}


def _cmd_exposure(positions: list = None):
    return build_exposure_summary(positions or [])


def _cmd_theme_risk(theme_exposures: list = None):
    return {"theme_exposures": theme_exposures or [], **_PAPER_HEADER}


def _cmd_industry_risk(industry_exposures: list = None):
    return {"industry_exposures": industry_exposures or [], **_PAPER_HEADER}


def _cmd_correlation_risk(clusters: list = None):
    return detect_correlation_risk(clusters or [])


def _cmd_risk_limits(portfolio: dict = None, limits: dict = None):
    return evaluate_risk_limits(portfolio or {}, limits or {})


def _cmd_risk_overlay(candidate: str = "", portfolio: dict = None):
    return run_risk_overlay(candidate, portfolio or {"paper_only": True})


def _cmd_risk_score(exposure_summary: dict = None):
    score_result = compute_risk_score(exposure_summary or {"raw_score": 0.0})
    grade_result = compute_risk_grade(score_result.get("score", 0.0))
    return {**score_result, "grade": grade_result.get("grade", "LOW"), **_PAPER_HEADER}


def _cmd_recommendations(grade: str = "LOW", breaches: list = None):
    return generate_recommendations(grade, breaches or [])


def _cmd_dashboard(snapshot: dict = None, exposure: dict = None, grade: str = "LOW", recs: list = None):
    return build_portfolio_dashboard(snapshot or {}, exposure or {}, grade, recs or [])


def _cmd_report(dashboard: dict = None, audit_trail: list = None):
    return build_governance_report(dashboard or {}, audit_trail or [])


def _cmd_export(report: dict = None, export_path: str = ""):
    return export_governance_pack(report or {}, export_path)


def _cmd_health():
    from paper_trading.small_capital_strategy.portfolio_governance_health_v198 import run_health_check
    return run_health_check()


def _cmd_gate():
    from release.portfolio_governance_release_gate_v198 import run_release_gate
    return run_release_gate()


def _cmd_scenarios():
    return {"scenarios": get_scenarios(), "count": 75, **_PAPER_HEADER}


def _cmd_fixtures():
    return {"fixtures": get_fixtures(), "count": 75, **_PAPER_HEADER}


def _cmd_safety_audit():
    return run_safety_audit()


COMMAND_MAP = {
    "portfolio-governance-version": _cmd_version,
    "portfolio-governance-run": _cmd_run,
    "portfolio-governance-snapshot": _cmd_snapshot,
    "portfolio-governance-exposure": _cmd_exposure,
    "portfolio-governance-theme-risk": _cmd_theme_risk,
    "portfolio-governance-industry-risk": _cmd_industry_risk,
    "portfolio-governance-correlation-risk": _cmd_correlation_risk,
    "portfolio-governance-risk-limits": _cmd_risk_limits,
    "portfolio-governance-risk-overlay": _cmd_risk_overlay,
    "portfolio-governance-risk-score": _cmd_risk_score,
    "portfolio-governance-recommendations": _cmd_recommendations,
    "portfolio-governance-dashboard": _cmd_dashboard,
    "portfolio-governance-report": _cmd_report,
    "portfolio-governance-export": _cmd_export,
    "portfolio-governance-health": _cmd_health,
    "portfolio-governance-gate": _cmd_gate,
    "portfolio-governance-scenarios": _cmd_scenarios,
    "portfolio-governance-fixtures": _cmd_fixtures,
    "portfolio-governance-safety-audit": _cmd_safety_audit,
}

assert len(COMMAND_MAP) == 19


def get_cli_commands() -> list:
    return list(CLI_COMMANDS)


def get_command_map() -> dict:
    return dict(COMMAND_MAP)
