"""
paper_trading/small_capital_strategy/cash_control_v170.py
Cash control for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.enums_v170 import MarketRegime, CashControlMode
from paper_trading.small_capital_strategy.models_v170 import CashControlPlan
from paper_trading.small_capital_strategy.market_regime_filter_v170 import REGIME_CONTROL


def get_cash_control_plan(regime: MarketRegime, capital_twd: float = 300000.0) -> CashControlPlan:
    """Return a CashControlPlan for the given regime."""
    ctrl = REGIME_CONTROL.get(regime, REGIME_CONTROL[MarketRegime.UNKNOWN])
    mode = CashControlMode(regime.value)

    return CashControlPlan(
        regime=regime,
        mode=mode,
        target_cash_pct=ctrl["cash_min_pct"],
        min_cash_pct=ctrl["cash_min_pct"],
        max_invested_pct=ctrl["max_invested_pct"],
    )


def validate_cash_control(plan: CashControlPlan, current_cash_pct: float) -> Dict[str, Any]:
    """
    Validate that current_cash_pct meets the plan requirements.
    Returns {valid, issues, cash_ok}.
    """
    issues = []
    cash_ok = current_cash_pct >= plan.min_cash_pct

    if not cash_ok:
        issues.append(
            f"current_cash_pct {current_cash_pct:.2%} < required min {plan.min_cash_pct:.2%}"
        )

    if current_cash_pct < 0:
        issues.append(f"current_cash_pct {current_cash_pct:.2%} must be >= 0")

    if not plan.paper_only:
        issues.append("paper_only must be True")

    return {
        "valid": len(issues) == 0,
        "cash_ok": cash_ok,
        "issues": issues,
        "current_cash_pct": current_cash_pct,
        "min_cash_pct": plan.min_cash_pct,
        "max_invested_pct": plan.max_invested_pct,
    }


def get_cash_control_summary() -> Dict[str, Any]:
    """Return cash control rules for all regimes."""
    return {
        regime.value: {
            "cash_min_pct": ctrl["cash_min_pct"],
            "max_invested_pct": ctrl["max_invested_pct"],
            "short_term_training_allowed": ctrl["short_term_training_allowed"],
        }
        for regime, ctrl in REGIME_CONTROL.items()
    }
