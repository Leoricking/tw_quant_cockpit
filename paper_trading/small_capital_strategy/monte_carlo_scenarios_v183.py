"""
paper_trading/small_capital_strategy/monte_carlo_scenarios_v183.py
75 Monte Carlo scenarios (MC183-001 to MC183-075) for v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations


def _s(sid, cat, action, regime, trial_count, win_rate, ruin_prob, survival_rate,
       ror_grade, final_grade, capital, seed, desc):
    return {
        "id": sid,
        "category": cat,
        "expected_action": action,
        "market_regime": regime,
        "trial_count": trial_count,
        "win_rate_pct": win_rate,
        "ruin_probability_pct": ruin_prob,
        "survival_rate_pct": survival_rate,
        "ror_grade": ror_grade,
        "final_grade": final_grade,
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "validation_only": True,
        "monte_carlo_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "production_trading_blocked": True,
        "initial_capital": capital,
        "random_seed": seed,
        "description": desc,
    }


_SCENARIOS = [
    # monte_carlo_robust (10): MC183-001 to MC183-010
    _s("MC183-001", "monte_carlo_robust", "MONTE_CARLO_ONLY", "BULL", 1000, 55.0, 0.4, 99.6, "LOW", "ROBUST", 300000.0, 42, "Bull market, low ruin, high win rate"),
    _s("MC183-002", "monte_carlo_robust", "MONTE_CARLO_ONLY", "BULL", 1000, 52.0, 0.8, 99.2, "LOW", "ROBUST", 500000.0, 42, "Bull market, moderate win rate, robust"),
    _s("MC183-003", "monte_carlo_robust", "MONTE_CARLO_ONLY", "BULL", 500, 56.0, 0.6, 99.4, "LOW", "ROBUST", 300000.0, 42, "Bull market, 500 trials, robust"),
    _s("MC183-004", "monte_carlo_robust", "MONTE_CARLO_ONLY", "RANGE", 1000, 53.0, 1.0, 99.0, "LOW", "ROBUST", 300000.0, 42, "Range market, good survival"),
    _s("MC183-005", "monte_carlo_robust", "MONTE_CARLO_ONLY", "BULL", 5000, 54.0, 0.5, 99.5, "LOW", "ROBUST", 300000.0, 42, "Bull market, 5000 trials, very robust"),
    _s("MC183-006", "monte_carlo_robust", "MONTE_CARLO_ONLY", "BULL", 1000, 58.0, 0.2, 99.8, "LOW", "ROBUST", 300000.0, 42, "Bull market, high win rate, very robust"),
    _s("MC183-007", "monte_carlo_robust", "MONTE_CARLO_ONLY", "RANGE", 1000, 51.0, 1.8, 98.2, "LOW", "ROBUST", 300000.0, 42, "Range market, borderline robust"),
    _s("MC183-008", "monte_carlo_robust", "MONTE_CARLO_ONLY", "BULL", 100, 55.0, 1.0, 99.0, "LOW", "ROBUST", 300000.0, 42, "Bull market, 100 trials, robust"),
    _s("MC183-009", "monte_carlo_robust", "MONTE_CARLO_ONLY", "BULL", 1000, 60.0, 0.1, 99.9, "VERY_LOW", "ROBUST", 500000.0, 42, "Bull market, high win rate, near-zero ruin"),
    _s("MC183-010", "monte_carlo_robust", "MONTE_CARLO_ONLY", "RANGE", 500, 53.0, 1.5, 98.5, "LOW", "ROBUST", 300000.0, 42, "Range market, 500 trials, conservative params"),
    # monte_carlo_blocked (10): MC183-011 to MC183-020
    _s("MC183-011", "monte_carlo_blocked", "BLOCKED", "BEAR", 1000, 35.0, 45.0, 55.0, "CRITICAL", "RUIN_RISK", 300000.0, 42, "Bear market, very low win rate, RUIN_RISK"),
    _s("MC183-012", "monte_carlo_blocked", "BLOCKED", "RISK_OFF", 1000, 30.0, 60.0, 40.0, "CRITICAL", "RUIN_RISK", 300000.0, 42, "Risk-off, extremely low win rate"),
    _s("MC183-013", "monte_carlo_blocked", "BLOCKED", "BEAR", 1000, 45.0, 25.0, 75.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Bear market, high ruin probability"),
    _s("MC183-014", "monte_carlo_blocked", "BLOCKED", "RISK_OFF", 1000, 40.0, 30.0, 70.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Risk-off, very high ruin probability"),
    _s("MC183-015", "monte_carlo_blocked", "BLOCKED", "BEAR", 500, 42.0, 22.0, 78.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Bear market, 500 trials, high risk"),
    _s("MC183-016", "monte_carlo_blocked", "BLOCKED", "RISK_OFF", 1000, 38.0, 35.0, 65.0, "CRITICAL", "RUIN_RISK", 300000.0, 42, "Risk-off market, ruin_risk grade"),
    _s("MC183-017", "monte_carlo_blocked", "BLOCKED", "BEAR", 1000, 33.0, 50.0, 50.0, "CRITICAL", "RUIN_RISK", 300000.0, 42, "Bear market, half ruined"),
    _s("MC183-018", "monte_carlo_blocked", "BLOCKED", "BEAR", 1000, 48.0, 12.0, 88.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Bear market, no stop loss, high risk"),
    _s("MC183-019", "monte_carlo_blocked", "BLOCKED", "RISK_OFF", 1000, 44.0, 18.0, 82.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Risk-off, no out-of-sample robustness"),
    _s("MC183-020", "monte_carlo_blocked", "BLOCKED", "BEAR", 1000, 36.0, 42.0, 58.0, "CRITICAL", "RUIN_RISK", 300000.0, 42, "Bear market, strategy fails under all shuffles"),
    # risk_of_ruin_low (8): MC183-021 to MC183-028
    _s("MC183-021", "risk_of_ruin_low", "PAPER_PLAN_READY", "BULL", 1000, 55.0, 0.6, 99.4, "LOW", "ROBUST", 300000.0, 42, "Low RoR, capital floor 70%, dd limit 20%"),
    _s("MC183-022", "risk_of_ruin_low", "PAPER_PLAN_READY", "BULL", 1000, 54.0, 0.8, 99.2, "LOW", "ROBUST", 300000.0, 42, "Low RoR, capital floor 60%, dd limit 25%"),
    _s("MC183-023", "risk_of_ruin_low", "PAPER_PLAN_READY", "RANGE", 1000, 52.0, 1.2, 98.8, "LOW", "ROBUST", 300000.0, 42, "Range market, low RoR, tight capital floor"),
    _s("MC183-024", "risk_of_ruin_low", "PAPER_PLAN_READY", "BULL", 500, 56.0, 0.4, 99.6, "LOW", "ROBUST", 300000.0, 42, "Bull market, very low RoR, 500 trials"),
    _s("MC183-025", "risk_of_ruin_low", "PAPER_PLAN_READY", "BULL", 1000, 53.0, 1.5, 98.5, "LOW", "ACCEPTABLE", 300000.0, 42, "Bull market, borderline low RoR"),
    _s("MC183-026", "risk_of_ruin_low", "PAPER_PLAN_READY", "RANGE", 1000, 55.0, 0.9, 99.1, "LOW", "ROBUST", 300000.0, 42, "Range market, low RoR, stable params"),
    _s("MC183-027", "risk_of_ruin_low", "PAPER_PLAN_READY", "BULL", 1000, 57.0, 0.3, 99.7, "VERY_LOW", "ROBUST", 500000.0, 42, "Large capital, very low RoR"),
    _s("MC183-028", "risk_of_ruin_low", "PAPER_PLAN_READY", "BULL", 1000, 51.0, 1.9, 98.1, "LOW", "ACCEPTABLE", 300000.0, 42, "Borderline RoR, still acceptable"),
    # risk_of_ruin_high (7): MC183-029 to MC183-035
    _s("MC183-029", "risk_of_ruin_high", "BLOCKED", "BEAR", 1000, 42.0, 22.0, 78.0, "HIGH", "HIGH_RISK", 300000.0, 42, "High RoR, capital floor 50%, bear market"),
    _s("MC183-030", "risk_of_ruin_high", "BLOCKED", "RISK_OFF", 1000, 38.0, 35.0, 65.0, "CRITICAL", "RUIN_RISK", 300000.0, 42, "Critical RoR, risk-off market"),
    _s("MC183-031", "risk_of_ruin_high", "BLOCKED", "BEAR", 1000, 44.0, 18.0, 82.0, "HIGH", "HIGH_RISK", 300000.0, 42, "High RoR, losing streak threshold exceeded"),
    _s("MC183-032", "risk_of_ruin_high", "BLOCKED", "BEAR", 500, 40.0, 28.0, 72.0, "HIGH", "HIGH_RISK", 300000.0, 42, "High RoR, 500 trials, bear market"),
    _s("MC183-033", "risk_of_ruin_high", "BLOCKED", "RISK_OFF", 1000, 36.0, 40.0, 60.0, "CRITICAL", "RUIN_RISK", 300000.0, 42, "Critical RoR, only survives lucky sequence"),
    _s("MC183-034", "risk_of_ruin_high", "BLOCKED", "BEAR", 1000, 45.0, 15.0, 85.0, "HIGH", "HIGH_RISK", 300000.0, 42, "High RoR, missing out-of-sample robust param"),
    _s("MC183-035", "risk_of_ruin_high", "BLOCKED", "RISK_OFF", 1000, 43.0, 20.0, 80.0, "HIGH", "HIGH_RISK", 300000.0, 42, "High RoR, worst-5pct drawdown exceeds limit"),
    # bootstrap_pass (8): MC183-036 to MC183-043
    _s("MC183-036", "bootstrap_pass", "VALIDATION_ONLY", "BULL", 1000, 55.0, 0.5, 99.5, "LOW", "ROBUST", 300000.0, 42, "Bootstrap pass, mean return positive"),
    _s("MC183-037", "bootstrap_pass", "VALIDATION_ONLY", "BULL", 500, 53.0, 1.0, 99.0, "LOW", "ROBUST", 300000.0, 42, "Bootstrap pass, 500 samples, CI positive"),
    _s("MC183-038", "bootstrap_pass", "VALIDATION_ONLY", "RANGE", 1000, 52.0, 1.2, 98.8, "LOW", "ACCEPTABLE", 300000.0, 42, "Range market, bootstrap pass"),
    _s("MC183-039", "bootstrap_pass", "VALIDATION_ONLY", "BULL", 1000, 58.0, 0.2, 99.8, "LOW", "ROBUST", 300000.0, 42, "Bootstrap pass, high win rate, wide CI"),
    _s("MC183-040", "bootstrap_pass", "VALIDATION_ONLY", "BULL", 1000, 54.0, 0.8, 99.2, "LOW", "ROBUST", 500000.0, 42, "Bootstrap pass, large capital, stable"),
    _s("MC183-041", "bootstrap_pass", "VALIDATION_ONLY", "RANGE", 500, 53.0, 1.4, 98.6, "LOW", "ACCEPTABLE", 300000.0, 42, "Range market, 500 samples, borderline pass"),
    _s("MC183-042", "bootstrap_pass", "VALIDATION_ONLY", "BULL", 1000, 56.0, 0.4, 99.6, "LOW", "ROBUST", 300000.0, 42, "Bootstrap pass, 1000 samples, robust"),
    _s("MC183-043", "bootstrap_pass", "VALIDATION_ONLY", "BULL", 5000, 55.0, 0.5, 99.5, "LOW", "ROBUST", 300000.0, 42, "Bootstrap pass, 5000 trials, very confident"),
    # bootstrap_fail (5): MC183-044 to MC183-048
    _s("MC183-044", "bootstrap_fail", "BLOCKED", "BEAR", 1000, 42.0, 22.0, 78.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Bootstrap fail, mean return negative"),
    _s("MC183-045", "bootstrap_fail", "BLOCKED", "RISK_OFF", 1000, 38.0, 35.0, 65.0, "CRITICAL", "RUIN_RISK", 300000.0, 42, "Bootstrap fail, CI entirely negative"),
    _s("MC183-046", "bootstrap_fail", "BLOCKED", "BEAR", 500, 44.0, 18.0, 82.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Bootstrap fail, worst-5pct drawdown too high"),
    _s("MC183-047", "bootstrap_fail", "BLOCKED", "RISK_OFF", 1000, 40.0, 28.0, 72.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Bootstrap fail, std too high, unreliable"),
    _s("MC183-048", "bootstrap_fail", "BLOCKED", "BEAR", 1000, 45.0, 15.0, 85.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Bootstrap fail, drawdown exceeds limit"),
    # sequence_risk_low (5): MC183-049 to MC183-053
    _s("MC183-049", "sequence_risk_low", "PAPER_PLAN_READY", "BULL", 1000, 55.0, 0.6, 99.4, "LOW", "ROBUST", 300000.0, 42, "Low sequence risk, few consecutive losses"),
    _s("MC183-050", "sequence_risk_low", "PAPER_PLAN_READY", "BULL", 1000, 58.0, 0.2, 99.8, "LOW", "ROBUST", 300000.0, 42, "Low sequence risk, high win rate limits streaks"),
    _s("MC183-051", "sequence_risk_low", "PAPER_PLAN_READY", "RANGE", 1000, 53.0, 1.0, 99.0, "LOW", "ACCEPTABLE", 300000.0, 42, "Range market, tolerable streak length"),
    _s("MC183-052", "sequence_risk_low", "PAPER_PLAN_READY", "BULL", 500, 55.0, 0.8, 99.2, "LOW", "ROBUST", 300000.0, 42, "500 trials, max streak within threshold"),
    _s("MC183-053", "sequence_risk_low", "PAPER_PLAN_READY", "BULL", 1000, 54.0, 0.9, 99.1, "LOW", "ROBUST", 300000.0, 42, "Consecutive loss distribution well controlled"),
    # sequence_risk_high (5): MC183-054 to MC183-058
    _s("MC183-054", "sequence_risk_high", "BLOCKED", "BEAR", 1000, 35.0, 45.0, 55.0, "CRITICAL", "RUIN_RISK", 300000.0, 42, "High sequence risk, extreme losing streaks"),
    _s("MC183-055", "sequence_risk_high", "BLOCKED", "RISK_OFF", 1000, 40.0, 28.0, 72.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Losing streak >8 common in risk-off"),
    _s("MC183-056", "sequence_risk_high", "BLOCKED", "BEAR", 1000, 42.0, 22.0, 78.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Bear market, streaks exceed threshold frequently"),
    _s("MC183-057", "sequence_risk_high", "BLOCKED", "RISK_OFF", 500, 38.0, 35.0, 65.0, "CRITICAL", "RUIN_RISK", 300000.0, 42, "500 trials, extreme streak risk"),
    _s("MC183-058", "sequence_risk_high", "BLOCKED", "BEAR", 1000, 44.0, 18.0, 82.0, "HIGH", "HIGH_RISK", 300000.0, 42, "Bear market, streak ruin probability high"),
    # tail_risk_pass (5): MC183-059 to MC183-063
    _s("MC183-059", "tail_risk_pass", "RESEARCH_ONLY", "BULL", 1000, 55.0, 0.5, 99.5, "LOW", "ROBUST", 300000.0, 42, "Tail risk acceptable, 5pct return not too negative"),
    _s("MC183-060", "tail_risk_pass", "RESEARCH_ONLY", "BULL", 1000, 56.0, 0.4, 99.6, "LOW", "ROBUST", 300000.0, 42, "Tail risk low, expected shortfall manageable"),
    _s("MC183-061", "tail_risk_pass", "RESEARCH_ONLY", "RANGE", 1000, 52.0, 1.5, 98.5, "LOW", "ACCEPTABLE", 300000.0, 42, "Range market, tail risk within tolerance"),
    _s("MC183-062", "tail_risk_pass", "RESEARCH_ONLY", "BULL", 500, 54.0, 0.8, 99.2, "LOW", "ROBUST", 300000.0, 42, "500 trials, tail risk grade ROBUST"),
    _s("MC183-063", "tail_risk_pass", "RESEARCH_ONLY", "BULL", 5000, 55.0, 0.5, 99.5, "LOW", "ROBUST", 300000.0, 42, "5000 trials, tail risk very stable"),
    # robustness_ranking (12): MC183-064 to MC183-075
    _s("MC183-064", "robustness_ranking", "MONTE_CARLO_ONLY", "BULL", 1000, 58.0, 0.2, 99.8, "VERY_LOW", "ROBUST", 300000.0, 42, "Rank 1, highest robustness probability"),
    _s("MC183-065", "robustness_ranking", "MONTE_CARLO_ONLY", "BULL", 1000, 56.0, 0.4, 99.6, "LOW", "ROBUST", 300000.0, 42, "Rank 2, high robustness"),
    _s("MC183-066", "robustness_ranking", "MONTE_CARLO_ONLY", "BULL", 1000, 55.0, 0.6, 99.4, "LOW", "ROBUST", 300000.0, 42, "Rank 3, good robustness"),
    _s("MC183-067", "robustness_ranking", "MONTE_CARLO_ONLY", "RANGE", 1000, 53.0, 1.0, 99.0, "LOW", "ACCEPTABLE", 300000.0, 42, "Rank 4, acceptable robustness"),
    _s("MC183-068", "robustness_ranking", "MONTE_CARLO_ONLY", "RANGE", 1000, 52.0, 1.5, 98.5, "LOW", "ACCEPTABLE", 300000.0, 42, "Rank 5, borderline acceptable"),
    _s("MC183-069", "robustness_ranking", "MONTE_CARLO_ONLY", "BULL", 5000, 57.0, 0.3, 99.7, "VERY_LOW", "ROBUST", 300000.0, 42, "Rank 1b, 5000 trials, very robust"),
    _s("MC183-070", "robustness_ranking", "MONTE_CARLO_ONLY", "RANGE", 500, 53.0, 1.2, 98.8, "LOW", "ROBUST", 300000.0, 42, "Rank 3b, range market, 500 trials"),
    _s("MC183-071", "robustness_ranking", "MONTE_CARLO_ONLY", "BULL", 1000, 54.0, 0.8, 99.2, "LOW", "ROBUST", 500000.0, 42, "Rank 2b, large capital, robust"),
    _s("MC183-072", "robustness_ranking", "MONTE_CARLO_ONLY", "BULL", 100, 55.0, 1.0, 99.0, "LOW", "ACCEPTABLE", 300000.0, 42, "Rank 4b, 100 trials, less confident"),
    _s("MC183-073", "robustness_ranking", "MONTE_CARLO_ONLY", "RANGE", 1000, 51.0, 1.8, 98.2, "LOW", "ACCEPTABLE", 300000.0, 42, "Rank 5b, range market, borderline"),
    _s("MC183-074", "robustness_ranking", "MONTE_CARLO_ONLY", "BULL", 1000, 60.0, 0.1, 99.9, "VERY_LOW", "ROBUST", 500000.0, 42, "Rank 1c, 60% win rate, top grade"),
    _s("MC183-075", "robustness_ranking", "MONTE_CARLO_ONLY", "BULL", 1000, 53.0, 1.6, 98.4, "LOW", "ACCEPTABLE", 300000.0, 42, "Rank 5c, conservative capital, acceptable"),
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
        "monte_carlo_only": True,
        "no_real_orders": True,
    }
