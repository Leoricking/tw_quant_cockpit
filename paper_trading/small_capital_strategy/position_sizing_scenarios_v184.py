"""
paper_trading/small_capital_strategy/position_sizing_scenarios_v184.py
75 Position Sizing scenarios for Capital Allocation Lab v1.8.4.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Allocation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Dict, Any

_SAFETY_META = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "allocation_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
}

_SCENARIOS: List[Dict[str, Any]] = [
    # ── fixed risk sizing safe (10) ─────────────────────────────────────
    {"id": "PS184-001", "category": "fixed_risk_safe",
     "description": "300K capital, 1% risk, 7% stop, BULL, expected SAFE", **_SAFETY_META},
    {"id": "PS184-002", "category": "fixed_risk_safe",
     "description": "500K capital, 1% risk, 7% stop, BULL, expected SAFE", **_SAFETY_META},
    {"id": "PS184-003", "category": "fixed_risk_safe",
     "description": "1M capital, 1% risk, 7% stop, BULL, expected SAFE", **_SAFETY_META},
    {"id": "PS184-004", "category": "fixed_risk_safe",
     "description": "3M capital, 1% risk, 7% stop, BULL, expected SAFE", **_SAFETY_META},
    {"id": "PS184-005", "category": "fixed_risk_safe",
     "description": "300K capital, 0.5% risk, 5% stop, BULL, expected SAFE", **_SAFETY_META},
    {"id": "PS184-006", "category": "fixed_risk_safe",
     "description": "500K capital, 0.8% risk, 5% stop, BULL, expected SAFE", **_SAFETY_META},
    {"id": "PS184-007", "category": "fixed_risk_safe",
     "description": "1M capital, 0.5% risk, 3% stop, BULL, expected SAFE", **_SAFETY_META},
    {"id": "PS184-008", "category": "fixed_risk_safe",
     "description": "3M capital, 0.5% risk, 5% stop, BULL, expected SAFE", **_SAFETY_META},
    {"id": "PS184-009", "category": "fixed_risk_safe",
     "description": "300K capital, 1% risk, 10% stop, BULL, expected SAFE", **_SAFETY_META},
    {"id": "PS184-010", "category": "fixed_risk_safe",
     "description": "500K capital, 1.5% risk, 7% stop, BULL, expected ACCEPTABLE", **_SAFETY_META},
    # ── blocked scenarios (10) ──────────────────────────────────────────
    {"id": "PS184-011", "category": "blocked",
     "description": "No stop loss → BLOCKED", **_SAFETY_META},
    {"id": "PS184-012", "category": "blocked",
     "description": "Stop loss distance = 0 → BLOCKED", **_SAFETY_META},
    {"id": "PS184-013", "category": "blocked",
     "description": "per_trade_risk_pct > 5% → BLOCKED", **_SAFETY_META},
    {"id": "PS184-014", "category": "blocked",
     "description": "Drawdown budget exhausted → BLOCKED", **_SAFETY_META},
    {"id": "PS184-015", "category": "blocked",
     "description": "Ruin risk > 20% → BLOCKED", **_SAFETY_META},
    {"id": "PS184-016", "category": "blocked",
     "description": "Market regime BLOCKED → action BLOCKED", **_SAFETY_META},
    {"id": "PS184-017", "category": "blocked",
     "description": "Cash reserve < 5% → BLOCKED", **_SAFETY_META},
    {"id": "PS184-018", "category": "blocked",
     "description": "Single position > 50% → BLOCKED", **_SAFETY_META},
    {"id": "PS184-019", "category": "blocked",
     "description": "Total exposure > 95% → BLOCKED", **_SAFETY_META},
    {"id": "PS184-020", "category": "blocked",
     "description": "Both ruin risk high AND no stop loss → BLOCKED", **_SAFETY_META},
    # ── ABC buy point staged sizing (10) ────────────────────────────────
    {"id": "PS184-021", "category": "abc_staged",
     "description": "A_10MA_PULLBACK initial 40%, add1 30%, add2 30%", **_SAFETY_META},
    {"id": "PS184-022", "category": "abc_staged",
     "description": "B_BREAKOUT initial 50%, add1 25%, add2 25%", **_SAFETY_META},
    {"id": "PS184-023", "category": "abc_staged",
     "description": "C_20MA_RECLAIM initial 30%, add1 30%, add2 40%", **_SAFETY_META},
    {"id": "PS184-024", "category": "abc_staged",
     "description": "A point high volatility reduces sizing", **_SAFETY_META},
    {"id": "PS184-025", "category": "abc_staged",
     "description": "B point weak regime reduces sizing", **_SAFETY_META},
    {"id": "PS184-026", "category": "abc_staged",
     "description": "C point high ruin risk reduces sizing", **_SAFETY_META},
    {"id": "PS184-027", "category": "abc_staged",
     "description": "A point BULL regime, safe ruin, PAPER_ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "PS184-028", "category": "abc_staged",
     "description": "B point RISK_OFF regime, REDUCE_RISK action", **_SAFETY_META},
    {"id": "PS184-029", "category": "abc_staged",
     "description": "C point add plan generates PAPER_ADD_ALLOWED", **_SAFETY_META},
    {"id": "PS184-030", "category": "abc_staged",
     "description": "A point with drawdown 15% of 20% budget, CAUTION", **_SAFETY_META},
    # ── capital stage scenarios (8) ──────────────────────────────────────
    {"id": "PS184-031", "category": "capital_stage",
     "description": "300K stage: max 2-3 positions, 1% risk each", **_SAFETY_META},
    {"id": "PS184-032", "category": "capital_stage",
     "description": "500K stage: max 3-4 positions, 1% risk each", **_SAFETY_META},
    {"id": "PS184-033", "category": "capital_stage",
     "description": "1M stage: max 4-5 positions, 1% risk each", **_SAFETY_META},
    {"id": "PS184-034", "category": "capital_stage",
     "description": "3M stage: max 5-6 positions, 0.5% risk each", **_SAFETY_META},
    {"id": "PS184-035", "category": "capital_stage",
     "description": "300K with 3 concurrent positions, exposure check", **_SAFETY_META},
    {"id": "PS184-036", "category": "capital_stage",
     "description": "500K with 4 concurrent positions, exposure check", **_SAFETY_META},
    {"id": "PS184-037", "category": "capital_stage",
     "description": "1M with 5 concurrent positions, exposure check", **_SAFETY_META},
    {"id": "PS184-038", "category": "capital_stage",
     "description": "3M with 6 concurrent positions, within limits", **_SAFETY_META},
    # ── risk budget scenarios (8) ────────────────────────────────────────
    {"id": "PS184-039", "category": "risk_budget",
     "description": "Conservative: 0.5% per trade, 10% max position", **_SAFETY_META},
    {"id": "PS184-040", "category": "risk_budget",
     "description": "Moderate: 1.0% per trade, 20% max position", **_SAFETY_META},
    {"id": "PS184-041", "category": "risk_budget",
     "description": "Aggressive: 2.0% per trade, 25% max position", **_SAFETY_META},
    {"id": "PS184-042", "category": "risk_budget",
     "description": "Cash reserve 50%: half capital always reserved", **_SAFETY_META},
    {"id": "PS184-043", "category": "risk_budget",
     "description": "Max drawdown 10%: tight budget, early caution", **_SAFETY_META},
    {"id": "PS184-044", "category": "risk_budget",
     "description": "Max drawdown 25%: wider budget, more headroom", **_SAFETY_META},
    {"id": "PS184-045", "category": "risk_budget",
     "description": "Sector limit 25%: 3 stocks same sector near limit", **_SAFETY_META},
    {"id": "PS184-046", "category": "risk_budget",
     "description": "Theme limit 30%: 2 stocks same theme near limit", **_SAFETY_META},
    # ── drawdown budget scenarios (7) ────────────────────────────────────
    {"id": "PS184-047", "category": "drawdown_budget",
     "description": "0% current drawdown, full budget available", **_SAFETY_META},
    {"id": "PS184-048", "category": "drawdown_budget",
     "description": "5% drawdown vs 20% budget, 25% used", **_SAFETY_META},
    {"id": "PS184-049", "category": "drawdown_budget",
     "description": "10% drawdown vs 20% budget, 50% used, CAUTION", **_SAFETY_META},
    {"id": "PS184-050", "category": "drawdown_budget",
     "description": "15% drawdown vs 20% budget, 75% used, HIGH_RISK", **_SAFETY_META},
    {"id": "PS184-051", "category": "drawdown_budget",
     "description": "20% drawdown vs 20% budget, 100% used, BLOCKED", **_SAFETY_META},
    {"id": "PS184-052", "category": "drawdown_budget",
     "description": "8% drawdown vs 15% budget, size reduction", **_SAFETY_META},
    {"id": "PS184-053", "category": "drawdown_budget",
     "description": "12% drawdown vs 25% budget, 48% used, ACCEPTABLE", **_SAFETY_META},
    # ── concentration risk scenarios (5) ─────────────────────────────────
    {"id": "PS184-054", "category": "concentration_risk",
     "description": "Single stock 10% of capital, low concentration", **_SAFETY_META},
    {"id": "PS184-055", "category": "concentration_risk",
     "description": "Single stock 20% of capital, moderate concentration", **_SAFETY_META},
    {"id": "PS184-056", "category": "concentration_risk",
     "description": "Single stock 30% of capital, HIGH concentration", **_SAFETY_META},
    {"id": "PS184-057", "category": "concentration_risk",
     "description": "2 stocks same theme, 40% combined, near limit", **_SAFETY_META},
    {"id": "PS184-058", "category": "concentration_risk",
     "description": "3 stocks same sector, 45% combined, exceeds limit", **_SAFETY_META},
    # ── exposure limit scenarios (5) ─────────────────────────────────────
    {"id": "PS184-059", "category": "exposure_limit",
     "description": "40% total exposure, 60% limit, safe entry", **_SAFETY_META},
    {"id": "PS184-060", "category": "exposure_limit",
     "description": "55% total exposure, 60% limit, near limit", **_SAFETY_META},
    {"id": "PS184-061", "category": "exposure_limit",
     "description": "60% total exposure, 60% limit, no more entries", **_SAFETY_META},
    {"id": "PS184-062", "category": "exposure_limit",
     "description": "50% exposure, 80% limit, 3 more positions possible", **_SAFETY_META},
    {"id": "PS184-063", "category": "exposure_limit",
     "description": "Cash reserve 10%, 50% cash rule, size cut", **_SAFETY_META},
    # ── Monte Carlo adjusted scenarios (5) ───────────────────────────────
    {"id": "PS184-064", "category": "monte_carlo_adjusted",
     "description": "Ruin risk 1%, full sizing allowed", **_SAFETY_META},
    {"id": "PS184-065", "category": "monte_carlo_adjusted",
     "description": "Ruin risk 5%, sizing reduced to 70%", **_SAFETY_META},
    {"id": "PS184-066", "category": "monte_carlo_adjusted",
     "description": "Ruin risk 10%, sizing reduced to 50%", **_SAFETY_META},
    {"id": "PS184-067", "category": "monte_carlo_adjusted",
     "description": "Ruin risk 15%, CAUTION, review required", **_SAFETY_META},
    {"id": "PS184-068", "category": "monte_carlo_adjusted",
     "description": "Ruin risk 25%, BLOCKED, no entry allowed", **_SAFETY_META},
    # ── safety compliance scenarios (7) ──────────────────────────────────
    {"id": "PS184-069", "category": "safety_compliance",
     "description": "All safety flags True, system clean", **_SAFETY_META},
    {"id": "PS184-070", "category": "safety_compliance",
     "description": "No broker flag verified", **_SAFETY_META},
    {"id": "PS184-071", "category": "safety_compliance",
     "description": "No real orders verified", **_SAFETY_META},
    {"id": "PS184-072", "category": "safety_compliance",
     "description": "No margin / leverage verified", **_SAFETY_META},
    {"id": "PS184-073", "category": "safety_compliance",
     "description": "Production trading blocked verified", **_SAFETY_META},
    {"id": "PS184-074", "category": "safety_compliance",
     "description": "Allocation only flag verified", **_SAFETY_META},
    {"id": "PS184-075", "category": "safety_compliance",
     "description": "All output actions are paper/research/allocation only", **_SAFETY_META},
]


def get_scenarios() -> List[Dict[str, Any]]:
    """Return list of all position sizing scenarios."""
    return list(_SCENARIOS)


def count_scenarios() -> int:
    """Return count of scenarios."""
    return len(_SCENARIOS)


def get_scenarios_by_category(category: str) -> List[Dict[str, Any]]:
    """Return scenarios filtered by category."""
    return [s for s in _SCENARIOS if s.get("category") == category]


def get_scenario_categories() -> List[str]:
    """Return list of unique scenario categories."""
    seen = []
    for s in _SCENARIOS:
        c = s.get("category", "")
        if c not in seen:
            seen.append(c)
    return seen
