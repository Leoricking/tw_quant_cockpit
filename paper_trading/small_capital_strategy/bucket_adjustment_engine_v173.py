"""
paper_trading/small_capital_strategy/bucket_adjustment_engine_v173.py
Bucket adjustment engine for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict

from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimeBlockReason,
)
from paper_trading.small_capital_strategy.market_regime_models_v173 import BucketAdjustmentPlan
from paper_trading.small_capital_strategy.cash_ratio_engine_v173 import build_cash_ratio_plan

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.bucket_adjustment_engine_v173"

DEFAULT_CAPITAL_TWD = 300_000.0


def build_bucket_adjustment_plan(
    regime: MarketRegime,
    capital_twd: float = DEFAULT_CAPITAL_TWD,
) -> BucketAdjustmentPlan:
    """
    Build bucket adjustment plan for a given regime and capital amount.
    Derives TWD amounts from cash_ratio_engine allocations. Paper only.
    """
    cash_plan = build_cash_ratio_plan(regime)
    block_reasons = list(cash_plan.block_reasons)

    if not cash_plan.allocation_valid:
        return BucketAdjustmentPlan(
            regime=regime,
            capital_twd=capital_twd,
            block_reasons=block_reasons,
            schema_version=_SCHEMA,
            policy_version=_POLICY,
            source_lineage=_LINEAGE,
        )

    core_amt     = capital_twd * cash_plan.core_pct / 100
    swing_amt    = capital_twd * cash_plan.main_theme_swing_pct / 100
    second_amt   = capital_twd * cash_plan.second_wave_setup_pct / 100
    training_amt = capital_twd * cash_plan.short_term_training_pct / 100
    cash_amt     = capital_twd * cash_plan.cash_pct / 100
    total_amt    = core_amt + swing_amt + second_amt + training_amt + cash_amt

    bucket_pcts: Dict[str, int] = {
        "CORE": cash_plan.core_pct,
        "MAIN_THEME_SWING": cash_plan.main_theme_swing_pct,
        "SECOND_WAVE_SETUP": cash_plan.second_wave_setup_pct,
        "SHORT_TERM_TRAINING": cash_plan.short_term_training_pct,
        "CASH": cash_plan.cash_pct,
    }

    return BucketAdjustmentPlan(
        regime=regime,
        capital_twd=capital_twd,
        core_amount=round(core_amt, 2),
        main_theme_swing_amount=round(swing_amt, 2),
        second_wave_setup_amount=round(second_amt, 2),
        short_term_training_amount=round(training_amt, 2),
        cash_amount=round(cash_amt, 2),
        total_amount=round(total_amt, 2),
        bucket_pcts=bucket_pcts,
        block_reasons=block_reasons,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )


def get_training_amount(regime: MarketRegime, capital_twd: float = DEFAULT_CAPITAL_TWD) -> float:
    """Return short_term_training_amount for regime. Zero in BEAR/RISK_OFF/UNKNOWN."""
    plan = build_bucket_adjustment_plan(regime, capital_twd)
    return plan.short_term_training_amount
