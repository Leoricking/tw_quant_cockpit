"""
paper_trading/small_capital_strategy/optimization_scenarios_v182.py
75 optimization scenarios (OP182-001 to OP182-075) for v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations


def _s(sid, cat, action, regime, theme_rank, wf_type, overfitting_level, stability_grade,
       final_grade, capital, ps_id, desc):
    return {
        "id": sid,
        "category": cat,
        "expected_action": action,
        "market_regime": regime,
        "theme_rank": theme_rank,
        "walkforward_type": wf_type,
        "overfitting_risk_level": overfitting_level,
        "stability_grade": stability_grade,
        "final_grade": final_grade,
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "validation_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "initial_capital": capital,
        "parameter_set_id": ps_id,
        "description": desc,
        "stress_test_only": True,
    }


_SCENARIOS = [
    # parameter_valid (10): OP182-001 to OP182-010
    _s("OP182-001", "parameter_valid", "PAPER_ENTRY_ALLOWED", "BULL", 1, "ROLLING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0001", "Bull market, good params, low overfitting"),
    _s("OP182-002", "parameter_valid", "PAPER_ENTRY_ALLOWED", "BULL", 2, "EXPANDING", "LOW", "STABLE", "ROBUST", 500000.0, "PS182-0002", "Bull market, medium capital, stable"),
    _s("OP182-003", "parameter_valid", "PAPER_ENTRY_ALLOWED", "BULL", 3, "ROLLING", "LOW", "ACCEPTABLE", "ACCEPTABLE", 1000000.0, "PS182-0003", "Bull market, large capital, acceptable"),
    _s("OP182-004", "parameter_valid", "PAPER_ENTRY_ALLOWED", "RANGE", 1, "REGIME_BASED", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0004", "Range market, robust params"),
    _s("OP182-005", "parameter_valid", "PAPER_ENTRY_ALLOWED", "BULL", 2, "THEME_CYCLE", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0005", "Bull market, theme cycle WF"),
    _s("OP182-006", "parameter_valid", "PAPER_ENTRY_ALLOWED", "BULL", 1, "ROLLING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0006", "Bull market, conservative risk"),
    _s("OP182-007", "parameter_valid", "PAPER_ENTRY_ALLOWED", "BULL", 3, "EXPANDING", "LOW", "ACCEPTABLE", "ACCEPTABLE", 500000.0, "PS182-0007", "Bull market, moderate positions"),
    _s("OP182-008", "parameter_valid", "PAPER_ENTRY_ALLOWED", "RANGE", 2, "ROLLING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0008", "Range market, tight stop"),
    _s("OP182-009", "parameter_valid", "PAPER_ENTRY_ALLOWED", "BULL", 1, "ROLLING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0009", "Bull market, high selectivity"),
    _s("OP182-010", "parameter_valid", "PAPER_ENTRY_ALLOWED", "BULL", 2, "EXPANDING", "LOW", "STABLE", "ROBUST", 500000.0, "PS182-0010", "Bull market, balanced portfolio"),
    # parameter_blocked (12): OP182-011 to OP182-022
    _s("OP182-011", "parameter_blocked", "BLOCKED", "BULL", 1, "ROLLING", "LOW", "BLOCKED", "BLOCKED", 300000.0, "PS182-0011", "Behavior risk BLOCKED"),
    _s("OP182-012", "parameter_blocked", "BLOCKED", "BULL", 2, "ROLLING", "LOW", "BLOCKED", "BLOCKED", 300000.0, "PS182-0012", "Risk dashboard BLOCKED"),
    _s("OP182-013", "parameter_blocked", "BLOCKED", "BEAR", 3, "ROLLING", "HIGH", "BLOCKED", "BLOCKED", 300000.0, "PS182-0013", "Missing stop loss"),
    _s("OP182-014", "parameter_blocked", "BLOCKED", "RISK_OFF", 1, "ROLLING", "HIGH", "BLOCKED", "BLOCKED", 300000.0, "PS182-0014", "Max drawdown exceeded"),
    _s("OP182-015", "parameter_blocked", "BLOCKED", "BEAR", 2, "ROLLING", "HIGH", "BLOCKED", "BLOCKED", 300000.0, "PS182-0015", "Zero stop loss pct"),
    _s("OP182-016", "parameter_blocked", "BLOCKED", "RISK_OFF", 3, "ROLLING", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0016", "Both risk limits BLOCKED"),
    _s("OP182-017", "parameter_blocked", "BLOCKED", "BEAR", 1, "ROLLING", "HIGH", "BLOCKED", "BLOCKED", 300000.0, "PS182-0017", "Negative stop loss"),
    _s("OP182-018", "parameter_blocked", "BLOCKED", "RISK_OFF", 2, "ROLLING", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0018", "Excessive drawdown limit"),
    _s("OP182-019", "parameter_blocked", "BLOCKED", "BEAR", 3, "ROLLING", "HIGH", "BLOCKED", "BLOCKED", 300000.0, "PS182-0019", "No capital allocated"),
    _s("OP182-020", "parameter_blocked", "BLOCKED", "RISK_OFF", 1, "ROLLING", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0020", "All thresholds zero"),
    _s("OP182-021", "parameter_blocked", "BLOCKED", "BEAR", 2, "ROLLING", "HIGH", "BLOCKED", "BLOCKED", 300000.0, "PS182-0021", "Risk pct too high"),
    _s("OP182-022", "parameter_blocked", "BLOCKED", "RISK_OFF", 3, "ROLLING", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0022", "Max positions zero"),
    # walk_forward_pass (8): OP182-023 to OP182-030
    _s("OP182-023", "walk_forward_pass", "VALIDATION_ONLY", "BULL", 1, "ROLLING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0023", "WF rolling pass rate 80%"),
    _s("OP182-024", "walk_forward_pass", "VALIDATION_ONLY", "BULL", 2, "EXPANDING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0024", "WF expanding pass rate 100%"),
    _s("OP182-025", "walk_forward_pass", "VALIDATION_ONLY", "RANGE", 1, "REGIME_BASED", "LOW", "ACCEPTABLE", "ACCEPTABLE", 300000.0, "PS182-0025", "WF regime-based pass"),
    _s("OP182-026", "walk_forward_pass", "VALIDATION_ONLY", "BULL", 3, "THEME_CYCLE", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0026", "WF theme cycle pass"),
    _s("OP182-027", "walk_forward_pass", "VALIDATION_ONLY", "BULL", 1, "BULLISH", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0027", "WF bullish pass"),
    _s("OP182-028", "walk_forward_pass", "VALIDATION_ONLY", "RANGE", 2, "RANGE", "LOW", "ACCEPTABLE", "ACCEPTABLE", 300000.0, "PS182-0028", "WF range pass"),
    _s("OP182-029", "walk_forward_pass", "VALIDATION_ONLY", "BULL", 1, "PARAMETER_STABILITY", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0029", "WF parameter stability pass"),
    _s("OP182-030", "walk_forward_pass", "VALIDATION_ONLY", "BULL", 2, "OVERFITTING_CHECK", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0030", "WF overfitting check pass"),
    # walk_forward_fail (8): OP182-031 to OP182-038
    _s("OP182-031", "walk_forward_fail", "BLOCKED", "BEAR", 3, "ROLLING", "HIGH", "UNSTABLE", "OVERFITTED", 300000.0, "PS182-0031", "WF rolling fail rate 20%"),
    _s("OP182-032", "walk_forward_fail", "BLOCKED", "RISK_OFF", 1, "EXPANDING", "HIGH", "UNSTABLE", "OVERFITTED", 300000.0, "PS182-0032", "WF expanding fail rate 0%"),
    _s("OP182-033", "walk_forward_fail", "BLOCKED", "BEAR", 2, "REGIME_BASED", "HIGH", "BLOCKED", "BLOCKED", 300000.0, "PS182-0033", "WF regime-based fail"),
    _s("OP182-034", "walk_forward_fail", "BLOCKED", "RISK_OFF", 3, "THEME_CYCLE", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0034", "WF theme cycle fail"),
    _s("OP182-035", "walk_forward_fail", "BLOCKED", "BEAR", 1, "BEARISH", "HIGH", "UNSTABLE", "OVERFITTED", 300000.0, "PS182-0035", "WF bearish fail"),
    _s("OP182-036", "walk_forward_fail", "BLOCKED", "RISK_OFF", 2, "RISK_OFF", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0036", "WF risk-off fail"),
    _s("OP182-037", "walk_forward_fail", "BLOCKED", "BEAR", 3, "PARAMETER_STABILITY", "HIGH", "UNSTABLE", "OVERFITTED", 300000.0, "PS182-0037", "WF param stability fail"),
    _s("OP182-038", "walk_forward_fail", "BLOCKED", "RISK_OFF", 1, "OVERFITTING_CHECK", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0038", "WF overfitting check fail"),
    # overfitting_low (7): OP182-039 to OP182-045
    _s("OP182-039", "overfitting_low", "PAPER_PLAN_READY", "BULL", 1, "ROLLING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0039", "Low overfitting, bull stable"),
    _s("OP182-040", "overfitting_low", "PAPER_PLAN_READY", "BULL", 2, "EXPANDING", "LOW", "STABLE", "ROBUST", 500000.0, "PS182-0040", "Low overfitting, expanding WF"),
    _s("OP182-041", "overfitting_low", "PAPER_PLAN_READY", "RANGE", 1, "REGIME_BASED", "LOW", "ACCEPTABLE", "ACCEPTABLE", 300000.0, "PS182-0041", "Low overfitting, range market"),
    _s("OP182-042", "overfitting_low", "PAPER_PLAN_READY", "BULL", 3, "THEME_CYCLE", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0042", "Low overfitting, theme cycle"),
    _s("OP182-043", "overfitting_low", "PAPER_PLAN_READY", "BULL", 1, "ROLLING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0043", "Low overfitting, conservative"),
    _s("OP182-044", "overfitting_low", "PAPER_PLAN_READY", "BULL", 2, "ROLLING", "LOW", "ACCEPTABLE", "ACCEPTABLE", 300000.0, "PS182-0044", "Low overfitting, moderate risk"),
    _s("OP182-045", "overfitting_low", "PAPER_PLAN_READY", "RANGE", 1, "EXPANDING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0045", "Low overfitting, range stable"),
    # overfitting_high (7): OP182-046 to OP182-052
    _s("OP182-046", "overfitting_high", "BLOCKED", "BULL", 3, "ROLLING", "HIGH", "UNSTABLE", "OVERFITTED", 300000.0, "PS182-0046", "High overfitting, curve fitted"),
    _s("OP182-047", "overfitting_high", "BLOCKED", "BEAR", 1, "EXPANDING", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0047", "Critical overfitting, bear fail"),
    _s("OP182-048", "overfitting_high", "BLOCKED", "RISK_OFF", 2, "REGIME_BASED", "HIGH", "UNSTABLE", "OVERFITTED", 300000.0, "PS182-0048", "High overfitting, risk-off"),
    _s("OP182-049", "overfitting_high", "BLOCKED", "BEAR", 3, "ROLLING", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0049", "Critical overfitting, no OOS"),
    _s("OP182-050", "overfitting_high", "BLOCKED", "RISK_OFF", 1, "EXPANDING", "HIGH", "UNSTABLE", "OVERFITTED", 300000.0, "PS182-0050", "High overfitting, degraded"),
    _s("OP182-051", "overfitting_high", "BLOCKED", "BEAR", 2, "ROLLING", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0051", "Critical overfitting, extreme gap"),
    _s("OP182-052", "overfitting_high", "BLOCKED", "RISK_OFF", 3, "ROLLING", "HIGH", "UNSTABLE", "OVERFITTED", 300000.0, "PS182-0052", "High overfitting, unstable"),
    # stability_check (8): OP182-053 to OP182-060
    _s("OP182-053", "stability_check", "PAPER_PLAN_READY", "BULL", 1, "ROLLING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0053", "Stable params, bull market"),
    _s("OP182-054", "stability_check", "PAPER_PLAN_READY", "RANGE", 2, "EXPANDING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0054", "Stable params, range market"),
    _s("OP182-055", "stability_check", "PAPER_PLAN_READY", "BULL", 1, "REGIME_BASED", "LOW", "ACCEPTABLE", "ACCEPTABLE", 300000.0, "PS182-0055", "Acceptable stability"),
    _s("OP182-056", "stability_check", "PAPER_PLAN_READY", "BULL", 3, "THEME_CYCLE", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0056", "Stable in theme cycle"),
    _s("OP182-057", "stability_check", "PAPER_PLAN_READY", "RANGE", 1, "ROLLING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0057", "Stable range, low sensitivity"),
    _s("OP182-058", "stability_check", "PAPER_PLAN_READY", "BULL", 2, "EXPANDING", "LOW", "ACCEPTABLE", "ACCEPTABLE", 500000.0, "PS182-0058", "Acceptable stability, medium cap"),
    _s("OP182-059", "stability_check", "PAPER_PLAN_READY", "BULL", 1, "ROLLING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0059", "Stable, conservative risk"),
    _s("OP182-060", "stability_check", "PAPER_PLAN_READY", "RANGE", 2, "EXPANDING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0060", "Stable, balanced params"),
    # sensitivity_high (7): OP182-061 to OP182-067
    _s("OP182-061", "sensitivity_high", "REVIEW_REQUIRED", "BULL", 1, "ROLLING", "MEDIUM", "ACCEPTABLE", "UNSTABLE", 300000.0, "PS182-0061", "High stop_loss sensitivity"),
    _s("OP182-062", "sensitivity_high", "REVIEW_REQUIRED", "BULL", 2, "EXPANDING", "MEDIUM", "ACCEPTABLE", "UNSTABLE", 300000.0, "PS182-0062", "High take_profit sensitivity"),
    _s("OP182-063", "sensitivity_high", "REVIEW_REQUIRED", "RANGE", 1, "ROLLING", "MEDIUM", "ACCEPTABLE", "UNSTABLE", 300000.0, "PS182-0063", "High risk_pct sensitivity"),
    _s("OP182-064", "sensitivity_high", "REVIEW_REQUIRED", "BULL", 3, "REGIME_BASED", "MEDIUM", "ACCEPTABLE", "UNSTABLE", 300000.0, "PS182-0064", "High max_positions sensitivity"),
    _s("OP182-065", "sensitivity_high", "REVIEW_REQUIRED", "BULL", 1, "ROLLING", "MEDIUM", "ACCEPTABLE", "UNSTABLE", 300000.0, "PS182-0065", "High theme threshold sensitivity"),
    _s("OP182-066", "sensitivity_high", "REVIEW_REQUIRED", "RANGE", 2, "EXPANDING", "MEDIUM", "ACCEPTABLE", "UNSTABLE", 300000.0, "PS182-0066", "High watchlist sensitivity"),
    _s("OP182-067", "sensitivity_high", "REVIEW_REQUIRED", "BULL", 1, "ROLLING", "MEDIUM", "ACCEPTABLE", "UNSTABLE", 300000.0, "PS182-0067", "High abc threshold sensitivity"),
    # regime_dependency (5): OP182-068 to OP182-072
    _s("OP182-068", "regime_dependency", "BLOCKED", "BEAR", 3, "BEARISH", "HIGH", "UNSTABLE", "BLOCKED", 300000.0, "PS182-0068", "Fails in bear market"),
    _s("OP182-069", "regime_dependency", "BLOCKED", "RISK_OFF", 1, "RISK_OFF", "HIGH", "BLOCKED", "BLOCKED", 300000.0, "PS182-0069", "Fails in risk-off market"),
    _s("OP182-070", "regime_dependency", "BLOCKED", "BEAR", 2, "BEARISH", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0070", "Severe bear dependency"),
    _s("OP182-071", "regime_dependency", "BLOCKED", "RISK_OFF", 3, "RISK_OFF", "CRITICAL", "BLOCKED", "BLOCKED", 300000.0, "PS182-0071", "Severe risk-off dependency"),
    _s("OP182-072", "regime_dependency", "BLOCKED", "BEAR", 1, "REGIME_BASED", "HIGH", "UNSTABLE", "BLOCKED", 300000.0, "PS182-0072", "Regime-dependent params"),
    # robustness_ranking (3): OP182-073 to OP182-075
    _s("OP182-073", "robustness_ranking", "VALIDATION_ONLY", "BULL", 1, "ROLLING", "LOW", "STABLE", "ROBUST", 300000.0, "PS182-0073", "Top rank, robust grade"),
    _s("OP182-074", "robustness_ranking", "VALIDATION_ONLY", "BULL", 2, "EXPANDING", "LOW", "STABLE", "ROBUST", 500000.0, "PS182-0074", "Second rank, robust grade"),
    _s("OP182-075", "robustness_ranking", "VALIDATION_ONLY", "RANGE", 1, "REGIME_BASED", "LOW", "ACCEPTABLE", "ACCEPTABLE", 300000.0, "PS182-0075", "Third rank, acceptable grade"),
]


def get_scenario_count() -> int:
    """Return total scenario count."""
    return len(_SCENARIOS)


def get_all_scenarios() -> list:
    """Return list of all scenarios."""
    return list(_SCENARIOS)


def get_scenario_by_id(sid: str):
    """Return scenario dict by id, or None."""
    return next((s for s in _SCENARIOS if s["id"] == sid), None)


def get_scenarios_by_category(cat: str) -> list:
    """Return list of scenarios matching category."""
    return [s for s in _SCENARIOS if s["category"] == cat]


def get_scenario_categories() -> list:
    """Return sorted list of unique categories."""
    return sorted(set(s["category"] for s in _SCENARIOS))


def get_scenario_ids() -> list:
    """Return list of all scenario IDs."""
    return [s["id"] for s in _SCENARIOS]


def get_scenarios_info() -> dict:
    """Return scenario metadata dict."""
    return {
        "count": len(_SCENARIOS),
        "paper_only": True,
        "validation_only": True,
        "no_real_orders": True,
    }
