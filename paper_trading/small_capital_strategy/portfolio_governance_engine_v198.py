"""
paper_trading/small_capital_strategy/portfolio_governance_engine_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Engine
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.portfolio_governance_version_v198 import (
    RISK_GRADES, RISK_RECOMMENDATIONS, RISK_LIMIT_KEYS, FORBIDDEN_OUTPUT_WORDS,
    HARD_BLOCK_CONDITIONS,
)

_PAPER_HEADER = {
    "paper_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "not_investment_advice": True,
    "analytics_executes_decision": False,
    "dashboard_mutates_strategy": False,
}

GRADE_THRESHOLDS = {
    "LOW": (0.0, 0.2),
    "MODERATE": (0.2, 0.4),
    "ELEVATED": (0.4, 0.6),
    "HIGH": (0.6, 0.8),
    "CRITICAL": (0.8, 1.01),
}


def _blocked(reason: str) -> dict:
    return {"blocked": True, "reason": reason, **_PAPER_HEADER}


def _ok(**extra) -> dict:
    return {"blocked": False, **_PAPER_HEADER, **extra}


def validate_portfolio_input(inp: dict) -> dict:
    if not isinstance(inp, dict):
        return _blocked("malformed_portfolio_input")
    if not inp.get("paper_only"):
        return _blocked("missing_paper_only_flags")
    if not inp.get("no_real_orders"):
        return _blocked("missing_no_real_orders_flag")
    if not inp.get("no_broker"):
        return _blocked("missing_no_broker_flags")
    if "positions" not in inp:
        return _blocked("missing_position_list")
    if "snapshot" not in inp:
        return _blocked("missing_portfolio_snapshot")
    if "risk_limits" not in inp:
        return _blocked("missing_risk_limits")
    for word in FORBIDDEN_OUTPUT_WORDS:
        if word in str(inp):
            return _blocked("forbidden_action_words")
    return _ok(valid=True)


def validate_risk_grade(grade: str) -> dict:
    if grade not in RISK_GRADES:
        return _ok(valid=False, grade=grade)
    return _ok(valid=True, grade=grade)


def validate_risk_recommendation(rec: str) -> dict:
    if rec not in RISK_RECOMMENDATIONS:
        return _ok(valid=False, recommendation=rec)
    return _ok(valid=True, recommendation=rec)


def validate_risk_limit_key(key: str) -> dict:
    if key not in RISK_LIMIT_KEYS:
        return _ok(valid=False, key=key)
    return _ok(valid=True, key=key)


def compute_risk_score(exposure_summary: dict) -> dict:
    if not isinstance(exposure_summary, dict):
        return _blocked("malformed_exposure_summary")
    raw = exposure_summary.get("raw_score", 0.0)
    score = max(0.0, min(1.0, float(raw)))
    return _ok(score=score)


def compute_risk_grade(score: float) -> dict:
    if not isinstance(score, (int, float)) or score < 0 or score > 1:
        return _ok(grade="INVALID", score=score)
    for grade, (low, high) in GRADE_THRESHOLDS.items():
        if low <= score < high:
            return _ok(grade=grade, score=score)
    return _ok(grade="CRITICAL", score=score)


def evaluate_risk_limits(portfolio: dict, limits: dict) -> dict:
    if not isinstance(portfolio, dict) or not isinstance(limits, dict):
        return _blocked("malformed_risk_limit_input")
    results = []
    breached = []
    for key in RISK_LIMIT_KEYS:
        limit_val = limits.get(key, 1.0)
        current_val = portfolio.get(key, 0.0)
        breach = current_val > limit_val
        results.append({"limit": key, "limit_value": limit_val, "current_value": current_val, "breached": breach})
        if breach:
            breached.append(key)
    return _ok(results=results, breached=breached, any_breach=len(breached) > 0)


def detect_concentration_risk(weights: dict, max_weight: float = 0.3) -> dict:
    if not isinstance(weights, dict):
        return _blocked("malformed_weights")
    breaches = {k: v for k, v in weights.items() if v > max_weight}
    return _ok(breaches=breaches, any_breach=len(breaches) > 0)


def detect_correlation_risk(clusters: list, max_cluster_weight: float = 0.5) -> dict:
    if not isinstance(clusters, list):
        return _blocked("malformed_clusters")
    breaches = [c for c in clusters if c.get("weight", 0.0) > max_cluster_weight]
    return _ok(breaches=breaches, any_breach=len(breaches) > 0)


def run_risk_overlay(candidate: str, portfolio: dict) -> dict:
    if not isinstance(portfolio, dict):
        return _blocked("malformed_portfolio_input")
    if not portfolio.get("paper_only"):
        return _blocked("missing_paper_only_flags")
    for word in FORBIDDEN_OUTPUT_WORDS:
        if word in str(candidate):
            return _blocked("forbidden_action_words")
    if portfolio.get("overlay_tries_to_rebalance_real_portfolio"):
        return _blocked("overlay_tries_to_rebalance_real_portfolio")
    if portfolio.get("overlay_tries_to_mutate_strategy"):
        return _blocked("overlay_tries_to_mutate_strategy")
    risk_score = portfolio.get("risk_score", 0.0)
    overlay_passed = risk_score < 0.8
    return _ok(candidate=candidate, overlay_passed=overlay_passed, risk_score=risk_score)


def generate_recommendations(risk_grade: str, breaches: list) -> dict:
    recs = []
    if risk_grade in ("HIGH", "CRITICAL"):
        recs.append("RISK_OFF_MODE")
        recs.append("REQUIRE_HUMAN_REVIEW")
    elif risk_grade == "ELEVATED":
        recs.append("REDUCE_POSITION_SIZE")
        recs.append("KEEP_CASH_BUFFER")
    elif risk_grade == "MODERATE":
        recs.append("REQUIRE_MORE_EVIDENCE")
    else:
        recs.append("NO_CHANGE")
    if "max_single_theme_weight" in breaches:
        recs.append("REDUCE_THEME_EXPOSURE")
    if "max_single_industry_weight" in breaches:
        recs.append("REDUCE_INDUSTRY_EXPOSURE")
    if "max_open_candidates" in breaches:
        recs.append("BLOCK_NEW_CANDIDATE")
    valid_recs = [r for r in recs if r in RISK_RECOMMENDATIONS]
    return _ok(recommendations=valid_recs, count=len(valid_recs))


def build_exposure_summary(positions: list) -> dict:
    if not isinstance(positions, list):
        return _blocked("malformed_positions")
    symbols = set()
    themes = set()
    industries = set()
    strategies = set()
    for p in positions:
        if isinstance(p, dict):
            symbols.add(p.get("symbol", ""))
            themes.add(p.get("theme", ""))
            industries.add(p.get("industry", ""))
            strategies.add(p.get("strategy_id", ""))
    return _ok(
        symbol_count=len(symbols),
        theme_count=len(themes),
        industry_count=len(industries),
        strategy_count=len(strategies),
    )


def build_portfolio_dashboard(snapshot: dict, exposure: dict, grade: str, recs: list) -> dict:
    if not isinstance(snapshot, dict):
        return _blocked("malformed_snapshot")
    panels = {
        "portfolio_snapshot": snapshot,
        "exposure_summary": exposure,
        "risk_grade": grade,
        "recommendations": recs,
    }
    return _ok(
        panels=panels,
        panel_count=len(panels),
        dashboard_mutates_strategy=False,
        paper_only=True,
    )


def build_governance_report(dashboard: dict, audit_trail: list) -> dict:
    if not isinstance(dashboard, dict):
        return _blocked("malformed_dashboard")
    return _ok(
        sections=["summary", "exposure", "risk_assessment", "recommendations", "audit"],
        section_count=5,
        audit_entries=len(audit_trail) if isinstance(audit_trail, list) else 0,
        report_triggers_rebalance=False,
        paper_only=True,
    )


def build_audit_trail_entry(event_type: str, detail: str) -> dict:
    return _ok(event_type=event_type, detail=detail, immutable=True)


def export_governance_pack(report: dict, export_path: str = "") -> dict:
    if export_path and any(bad in export_path for bad in ["..", "//", "\\\\", "production", "live"]):
        return _blocked("unsafe_export_path")
    return _ok(exported=True, export_path=export_path or "paper_export/governance_pack.json", paper_only=True)
