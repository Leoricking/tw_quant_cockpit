"""
paper_trading/small_capital_strategy/small_capital_allocation_adapter_v173.py
Small capital allocation adapter for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, Any

from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
from paper_trading.small_capital_strategy.market_regime_models_v173 import BucketAdjustmentPlan
from paper_trading.small_capital_strategy.bucket_adjustment_engine_v173 import (
    build_bucket_adjustment_plan, DEFAULT_CAPITAL_TWD,
)
from paper_trading.small_capital_strategy.exposure_control_engine_v173 import (
    build_exposure_control_plan,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.small_capital_allocation_adapter_v173"


def build_full_allocation(
    regime: MarketRegime,
    capital_twd: float = DEFAULT_CAPITAL_TWD,
) -> Dict[str, Any]:
    """
    Build full allocation plan combining bucket amounts and exposure limits.
    Paper only.
    """
    bucket_plan  = build_bucket_adjustment_plan(regime, capital_twd)
    exposure_plan = build_exposure_control_plan(regime)

    return {
        "regime": regime.value,
        "capital_twd": capital_twd,
        "bucket_plan": bucket_plan,
        "exposure_plan": exposure_plan,
        "core_amount": bucket_plan.core_amount,
        "main_theme_swing_amount": bucket_plan.main_theme_swing_amount,
        "second_wave_setup_amount": bucket_plan.second_wave_setup_amount,
        "short_term_training_amount": bucket_plan.short_term_training_amount,
        "cash_amount": bucket_plan.cash_amount,
        "total_amount": bucket_plan.total_amount,
        "max_total_exposure_pct": exposure_plan.max_total_exposure_pct,
        "max_single_position_pct": exposure_plan.max_single_position_pct,
        "margin_allowed": exposure_plan.margin_allowed,
        "leverage_allowed": exposure_plan.leverage_allowed,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def get_max_position_amount(
    regime: MarketRegime,
    capital_twd: float = DEFAULT_CAPITAL_TWD,
) -> float:
    """Return max single-position amount in TWD for regime. Paper only."""
    exposure_plan = build_exposure_control_plan(regime)
    return capital_twd * exposure_plan.max_single_position_pct / 100


def validate_allocation_sum(bucket_plan: BucketAdjustmentPlan) -> bool:
    """Return True if bucket amounts sum to capital_twd (within 1 TWD tolerance)."""
    computed = (
        bucket_plan.core_amount
        + bucket_plan.main_theme_swing_amount
        + bucket_plan.second_wave_setup_amount
        + bucket_plan.short_term_training_amount
        + bucket_plan.cash_amount
    )
    return abs(computed - bucket_plan.capital_twd) < 1.0
