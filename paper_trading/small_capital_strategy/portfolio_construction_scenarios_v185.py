"""
paper_trading/small_capital_strategy/portfolio_construction_scenarios_v185.py
75 Portfolio Construction scenarios for Portfolio Construction & Rebalancing Lab v1.8.5.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Portfolio Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Dict, Any

_SAFETY_META = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "portfolio_only": True,
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
    # ── empty portfolio (5) ─────────────────────────────────────────────
    {"id": "PC185-001", "category": "empty_portfolio",
     "description": "300K, 0 holdings, 0 candidates → BALANCED empty", **_SAFETY_META},
    {"id": "PC185-002", "category": "empty_portfolio",
     "description": "500K, 0 holdings → BALANCED empty", **_SAFETY_META},
    {"id": "PC185-003", "category": "empty_portfolio",
     "description": "1M, 0 holdings → BALANCED empty", **_SAFETY_META},
    {"id": "PC185-004", "category": "empty_portfolio",
     "description": "3M, 0 holdings → BALANCED empty", **_SAFETY_META},
    {"id": "PC185-005", "category": "empty_portfolio",
     "description": "300K BULL, 0 holdings, max_positions=3 → BALANCED", **_SAFETY_META},

    # ── single holding (5) ─────────────────────────────────────────────
    {"id": "PC185-006", "category": "single_holding",
     "description": "300K, 1 holding AI theme, BULL → CONCENTRATED", **_SAFETY_META},
    {"id": "PC185-007", "category": "single_holding",
     "description": "500K, 1 holding semiconductor, BULL → CONCENTRATED", **_SAFETY_META},
    {"id": "PC185-008", "category": "single_holding",
     "description": "1M, 1 holding PCB, BULL → CONCENTRATED", **_SAFETY_META},
    {"id": "PC185-009", "category": "single_holding",
     "description": "300K, 1 holding above_10ma=False → REDUCE", **_SAFETY_META},
    {"id": "PC185-010", "category": "single_holding",
     "description": "300K, 1 holding above_20ma=False → REPLACE", **_SAFETY_META},

    # ── equal weight 2 holdings (5) ────────────────────────────────────
    {"id": "PC185-011", "category": "equal_weight_2",
     "description": "300K, 2 holdings equal weight, BULL → ACCEPTABLE", **_SAFETY_META},
    {"id": "PC185-012", "category": "equal_weight_2",
     "description": "500K, 2 holdings equal weight → ACCEPTABLE", **_SAFETY_META},
    {"id": "PC185-013", "category": "equal_weight_2",
     "description": "1M, 2 holdings equal weight different sectors → BALANCED", **_SAFETY_META},
    {"id": "PC185-014", "category": "equal_weight_2",
     "description": "300K, 2 holdings same sector → sector_exposure_check", **_SAFETY_META},
    {"id": "PC185-015", "category": "equal_weight_2",
     "description": "300K, 2 holdings same theme → theme_exposure_check", **_SAFETY_META},

    # ── equal weight 3 holdings (5) ────────────────────────────────────
    {"id": "PC185-016", "category": "equal_weight_3",
     "description": "300K, 3 holdings 3 sectors BULL → BALANCED", **_SAFETY_META},
    {"id": "PC185-017", "category": "equal_weight_3",
     "description": "300K, 3 holdings 2 sectors 3 themes → ACCEPTABLE", **_SAFETY_META},
    {"id": "PC185-018", "category": "equal_weight_3",
     "description": "500K, 3 holdings 3 sectors → BALANCED", **_SAFETY_META},
    {"id": "PC185-019", "category": "equal_weight_3",
     "description": "1M, 3 holdings 3 sectors 3 themes → BALANCED", **_SAFETY_META},
    {"id": "PC185-020", "category": "equal_weight_3",
     "description": "300K, 3 holdings, max_total_exposure=60% → exposure check", **_SAFETY_META},

    # ── 4–5 holdings (5) ──────────────────────────────────────────────
    {"id": "PC185-021", "category": "multi_holding_4",
     "description": "500K, 4 holdings 4 themes → BALANCED", **_SAFETY_META},
    {"id": "PC185-022", "category": "multi_holding_4",
     "description": "1M, 4 holdings mixed sectors → ACCEPTABLE", **_SAFETY_META},
    {"id": "PC185-023", "category": "multi_holding_5",
     "description": "1M, 5 holdings 5 sectors → BALANCED", **_SAFETY_META},
    {"id": "PC185-024", "category": "multi_holding_5",
     "description": "3M, 5 holdings 3 themes → ACCEPTABLE", **_SAFETY_META},
    {"id": "PC185-025", "category": "multi_holding_6",
     "description": "3M, 6 holdings max_positions=6 → BALANCED", **_SAFETY_META},

    # ── conviction weight (5) ──────────────────────────────────────────
    {"id": "PC185-026", "category": "conviction_weight",
     "description": "300K, 3 holdings conviction_weight → varied weights", **_SAFETY_META},
    {"id": "PC185-027", "category": "conviction_weight",
     "description": "500K, 3 holdings conviction=8/5/3 → weighted", **_SAFETY_META},
    {"id": "PC185-028", "category": "conviction_weight",
     "description": "1M, 4 holdings conviction_weight → ACCEPTABLE", **_SAFETY_META},
    {"id": "PC185-029", "category": "conviction_weight",
     "description": "300K, 2 holdings high conviction → concentration check", **_SAFETY_META},
    {"id": "PC185-030", "category": "conviction_weight",
     "description": "3M, 5 holdings conviction_weight → BALANCED", **_SAFETY_META},

    # ── volatility adjusted weight (5) ────────────────────────────────
    {"id": "PC185-031", "category": "volatility_adjusted",
     "description": "300K, 3 holdings vol_adjusted_weight → low vol gets more", **_SAFETY_META},
    {"id": "PC185-032", "category": "volatility_adjusted",
     "description": "500K, 3 holdings mixed volatility → ACCEPTABLE", **_SAFETY_META},
    {"id": "PC185-033", "category": "volatility_adjusted",
     "description": "1M, 4 holdings vol_adjusted → BALANCED", **_SAFETY_META},
    {"id": "PC185-034", "category": "volatility_adjusted",
     "description": "300K, high vol holding gets less weight → ACCEPTABLE", **_SAFETY_META},
    {"id": "PC185-035", "category": "volatility_adjusted",
     "description": "3M, 5 holdings vol_adjusted_weight → BALANCED", **_SAFETY_META},

    # ── sector exposure (5) ────────────────────────────────────────────
    {"id": "PC185-036", "category": "sector_exposure",
     "description": "300K, all holdings in AI sector → OVEREXPOSED", **_SAFETY_META},
    {"id": "PC185-037", "category": "sector_exposure",
     "description": "300K, max_sector_exposure=35%, 3 holdings 2 in same sector → check", **_SAFETY_META},
    {"id": "PC185-038", "category": "sector_exposure",
     "description": "500K, sector exposure 45% limit → OVEREXPOSED", **_SAFETY_META},
    {"id": "PC185-039", "category": "sector_exposure",
     "description": "1M, 3 sectors balanced → sector_ok=True", **_SAFETY_META},
    {"id": "PC185-040", "category": "sector_exposure",
     "description": "300K, 2 sectors < limit → sector_ok=True", **_SAFETY_META},

    # ── theme exposure (5) ─────────────────────────────────────────────
    {"id": "PC185-041", "category": "theme_exposure",
     "description": "300K, all AI theme → theme OVEREXPOSED", **_SAFETY_META},
    {"id": "PC185-042", "category": "theme_exposure",
     "description": "300K, max_theme_exposure=40%, 2 AI holdings → check", **_SAFETY_META},
    {"id": "PC185-043", "category": "theme_exposure",
     "description": "500K, semiconductor+PCB+AI → theme_ok", **_SAFETY_META},
    {"id": "PC185-044", "category": "theme_exposure",
     "description": "1M, 3 themes balanced → theme_ok=True", **_SAFETY_META},
    {"id": "PC185-045", "category": "theme_exposure",
     "description": "3M, 5 themes → theme_ok=True", **_SAFETY_META},

    # ── market regime (5) ─────────────────────────────────────────────
    {"id": "PC185-046", "category": "market_regime",
     "description": "300K BLOCKED regime → BLOCKED", **_SAFETY_META},
    {"id": "PC185-047", "category": "market_regime",
     "description": "300K WEAK regime → mc_adjustment reduced", **_SAFETY_META},
    {"id": "PC185-048", "category": "market_regime",
     "description": "300K RISK_OFF → exposure reduced", **_SAFETY_META},
    {"id": "PC185-049", "category": "market_regime",
     "description": "300K BULL regime → normal weights", **_SAFETY_META},
    {"id": "PC185-050", "category": "market_regime",
     "description": "300K BEAR regime → reduced exposure", **_SAFETY_META},

    # ── Monte Carlo ruin risk (5) ──────────────────────────────────────
    {"id": "PC185-051", "category": "monte_carlo_ruin",
     "description": "ruin_risk_pct=25% → BLOCKED", **_SAFETY_META},
    {"id": "PC185-052", "category": "monte_carlo_ruin",
     "description": "ruin_risk_pct=15% → mc_adjustment=0.5", **_SAFETY_META},
    {"id": "PC185-053", "category": "monte_carlo_ruin",
     "description": "ruin_risk_pct=8% → mc_adjustment=0.7", **_SAFETY_META},
    {"id": "PC185-054", "category": "monte_carlo_ruin",
     "description": "ruin_risk_pct=0% → mc_adjustment=1.0", **_SAFETY_META},
    {"id": "PC185-055", "category": "monte_carlo_ruin",
     "description": "ruin_risk=0%, BULL, balanced → BALANCED", **_SAFETY_META},

    # ── keep / reduce / replace (5) ───────────────────────────────────
    {"id": "PC185-056", "category": "keep_replace",
     "description": "holding above_10ma=True above_20ma=True → KEEP", **_SAFETY_META},
    {"id": "PC185-057", "category": "keep_replace",
     "description": "holding above_10ma=False above_20ma=True → REDUCE", **_SAFETY_META},
    {"id": "PC185-058", "category": "keep_replace",
     "description": "holding above_10ma=False above_20ma=False → REPLACE", **_SAFETY_META},
    {"id": "PC185-059", "category": "keep_replace",
     "description": "holding pnl=-9% → REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "PC185-060", "category": "keep_replace",
     "description": "mixed portfolio: 1 keep 1 replace → mixed decisions", **_SAFETY_META},

    # ── rebalance plan (5) ────────────────────────────────────────────
    {"id": "PC185-061", "category": "rebalance",
     "description": "3 holdings equal weight, no drift → rebalance_needed=False", **_SAFETY_META},
    {"id": "PC185-062", "category": "rebalance",
     "description": "3 holdings with drift > 10% → rebalance_needed=True", **_SAFETY_META},
    {"id": "PC185-063", "category": "rebalance",
     "description": "2 holdings threshold=5%, drift=7% → rebalance_needed", **_SAFETY_META},
    {"id": "PC185-064", "category": "rebalance",
     "description": "rebalance in WEAK regime → action REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "PC185-065", "category": "rebalance",
     "description": "rebalance in BULL, balanced → action OBSERVE", **_SAFETY_META},

    # ── diversification score (5) ─────────────────────────────────────
    {"id": "PC185-066", "category": "diversification",
     "description": "1 holding → low diversification score", **_SAFETY_META},
    {"id": "PC185-067", "category": "diversification",
     "description": "3 holdings equal → medium diversification", **_SAFETY_META},
    {"id": "PC185-068", "category": "diversification",
     "description": "5 holdings equal → high diversification", **_SAFETY_META},
    {"id": "PC185-069", "category": "diversification",
     "description": "6 holdings 1 dominant → concentrated", **_SAFETY_META},
    {"id": "PC185-070", "category": "diversification",
     "description": "4 holdings conviction_weight → check diversification", **_SAFETY_META},

    # ── capital stages (5) ────────────────────────────────────────────
    {"id": "PC185-071", "category": "capital_stage",
     "description": "300K max_positions=2 → max 2 holdings", **_SAFETY_META},
    {"id": "PC185-072", "category": "capital_stage",
     "description": "500K max_positions=3 → max 3 holdings", **_SAFETY_META},
    {"id": "PC185-073", "category": "capital_stage",
     "description": "1M max_positions=5 → max 5 holdings", **_SAFETY_META},
    {"id": "PC185-074", "category": "capital_stage",
     "description": "3M max_positions=6 → max 6 holdings", **_SAFETY_META},
    {"id": "PC185-075", "category": "capital_stage",
     "description": "3M 6 holdings 6 sectors → BALANCED", **_SAFETY_META},
]


def count_scenarios() -> int:
    """Return total scenario count."""
    return len(_SCENARIOS)


def get_scenarios() -> List[Dict[str, Any]]:
    """Return all scenarios."""
    return list(_SCENARIOS)


def get_scenarios_by_category(category: str) -> List[Dict[str, Any]]:
    """Return scenarios filtered by category."""
    return [s for s in _SCENARIOS if s.get("category") == category]
