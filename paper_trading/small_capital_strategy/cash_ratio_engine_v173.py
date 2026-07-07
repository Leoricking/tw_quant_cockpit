"""
paper_trading/small_capital_strategy/cash_ratio_engine_v173.py
Cash ratio engine for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict

from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimeBlockReason,
)
from paper_trading.small_capital_strategy.market_regime_models_v173 import CashRatioPlan

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.cash_ratio_engine_v173"

# Per-regime allocation table (sum to 100)
_REGIME_ALLOCATION: Dict[MarketRegime, Dict[str, int]] = {
    MarketRegime.BULL: {
        "max_invested_pct": 95,
        "min_cash_pct": 5,
        "core_pct": 40,
        "main_theme_swing_pct": 35,
        "second_wave_setup_pct": 15,
        "short_term_training_pct": 5,
        "cash_pct": 5,
    },
    MarketRegime.RANGE: {
        "max_invested_pct": 75,
        "min_cash_pct": 25,
        "core_pct": 35,
        "main_theme_swing_pct": 25,
        "second_wave_setup_pct": 10,
        "short_term_training_pct": 5,
        "cash_pct": 25,
    },
    MarketRegime.BEAR: {
        "max_invested_pct": 50,
        "min_cash_pct": 50,
        "core_pct": 30,
        "main_theme_swing_pct": 15,
        "second_wave_setup_pct": 5,
        "short_term_training_pct": 0,
        "cash_pct": 50,
    },
    MarketRegime.RISK_OFF: {
        "max_invested_pct": 40,
        "min_cash_pct": 60,
        "core_pct": 25,
        "main_theme_swing_pct": 10,
        "second_wave_setup_pct": 5,
        "short_term_training_pct": 0,
        "cash_pct": 60,
    },
    MarketRegime.UNKNOWN: {
        "max_invested_pct": 60,
        "min_cash_pct": 40,
        "core_pct": 35,
        "main_theme_swing_pct": 15,
        "second_wave_setup_pct": 10,
        "short_term_training_pct": 0,
        "cash_pct": 40,
    },
}


def build_cash_ratio_plan(regime: MarketRegime) -> CashRatioPlan:
    """Build cash ratio plan for a given market regime. Paper only."""
    alloc = _REGIME_ALLOCATION.get(regime)
    if alloc is None:
        return CashRatioPlan(
            regime=regime,
            allocation_valid=False,
            block_reasons=[RegimeBlockReason.INSUFFICIENT_DATA],
            plan_note="regime_not_found",
            schema_version=_SCHEMA,
            policy_version=_POLICY,
            source_lineage=_LINEAGE,
        )

    total = (
        alloc["core_pct"]
        + alloc["main_theme_swing_pct"]
        + alloc["second_wave_setup_pct"]
        + alloc["short_term_training_pct"]
        + alloc["cash_pct"]
    )
    valid = total == 100
    block_reasons = []
    if not valid:
        block_reasons.append(RegimeBlockReason.ALLOCATION_INVALID)
    if alloc["cash_pct"] < alloc["min_cash_pct"]:
        block_reasons.append(RegimeBlockReason.CASH_BELOW_MINIMUM)

    return CashRatioPlan(
        regime=regime,
        max_invested_pct=alloc["max_invested_pct"],
        min_cash_pct=alloc["min_cash_pct"],
        core_pct=alloc["core_pct"],
        main_theme_swing_pct=alloc["main_theme_swing_pct"],
        second_wave_setup_pct=alloc["second_wave_setup_pct"],
        short_term_training_pct=alloc["short_term_training_pct"],
        cash_pct=alloc["cash_pct"],
        total_pct=total,
        allocation_valid=valid and not block_reasons,
        block_reasons=block_reasons,
        plan_note=f"regime={regime.value} total={total}",
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )


def get_all_regime_allocations() -> Dict[str, Dict[str, int]]:
    """Return allocation table for all regimes."""
    return {r.value: v for r, v in _REGIME_ALLOCATION.items()}
