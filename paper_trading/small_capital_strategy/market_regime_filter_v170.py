"""
paper_trading/small_capital_strategy/market_regime_filter_v170.py
Market regime position control for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.enums_v170 import MarketRegime
from paper_trading.small_capital_strategy.models_v170 import MarketRegimeResult

# Regime control table
REGIME_CONTROL = {
    MarketRegime.BULL: {
        "max_invested_pct": 0.95,
        "cash_min_pct": 0.05,
        "short_term_training_allowed": True,
    },
    MarketRegime.RANGE: {
        "max_invested_pct": 0.75,
        "cash_min_pct": 0.25,
        "short_term_training_allowed": True,
    },
    MarketRegime.BEAR: {
        "max_invested_pct": 0.50,
        "cash_min_pct": 0.50,
        "short_term_training_allowed": False,
    },
    MarketRegime.RISK_OFF: {
        "max_invested_pct": 0.50,
        "cash_min_pct": 0.50,
        "short_term_training_allowed": False,
    },
    MarketRegime.UNKNOWN: {
        "max_invested_pct": 0.60,
        "cash_min_pct": 0.40,
        "short_term_training_allowed": False,
    },
}


def get_regime_control(regime: MarketRegime) -> MarketRegimeResult:
    """Return MarketRegimeResult for the given regime."""
    ctrl = REGIME_CONTROL.get(regime, REGIME_CONTROL[MarketRegime.UNKNOWN])
    return MarketRegimeResult(
        regime=regime,
        max_invested_pct=ctrl["max_invested_pct"],
        cash_min_pct=ctrl["cash_min_pct"],
        short_term_training_allowed=ctrl["short_term_training_allowed"],
    )


def is_trade_allowed_in_regime(regime: MarketRegime, is_short_term: bool = False) -> bool:
    """Return True if trading is broadly allowed in this regime."""
    if regime in (MarketRegime.BEAR, MarketRegime.RISK_OFF) and is_short_term:
        return False
    return True


def validate_regime_result(result: MarketRegimeResult) -> Dict[str, Any]:
    """Validate a MarketRegimeResult. Returns {valid, issues}."""
    issues = []
    if result.max_invested_pct + result.cash_min_pct > 1.0 + 0.001:
        issues.append(
            f"max_invested_pct {result.max_invested_pct} + cash_min_pct {result.cash_min_pct} > 1.0"
        )
    if result.cash_min_pct < 0:
        issues.append(f"cash_min_pct must be >= 0, got {result.cash_min_pct}")
    if not result.paper_only:
        issues.append("paper_only must be True")
    if not result.no_real_orders:
        issues.append("no_real_orders must be True")
    return {"valid": len(issues) == 0, "issues": issues}
