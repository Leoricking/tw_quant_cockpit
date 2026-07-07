"""
paper_trading/small_capital_strategy/exposure_control_engine_v173.py
Exposure control engine for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict

from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimeBlockReason,
)
from paper_trading.small_capital_strategy.market_regime_models_v173 import ExposureControlPlan

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.exposure_control_engine_v173"

# Per-regime exposure limits
_REGIME_EXPOSURE: Dict[MarketRegime, Dict[str, object]] = {
    MarketRegime.BULL: {
        "max_total_exposure_pct": 95,
        "max_single_position_pct": 40,
        "margin_allowed": False,
        "leverage_allowed": False,
    },
    MarketRegime.RANGE: {
        "max_total_exposure_pct": 75,
        "max_single_position_pct": 30,
        "margin_allowed": False,
        "leverage_allowed": False,
    },
    MarketRegime.BEAR: {
        "max_total_exposure_pct": 50,
        "max_single_position_pct": 20,
        "margin_allowed": False,
        "leverage_allowed": False,
    },
    MarketRegime.RISK_OFF: {
        "max_total_exposure_pct": 40,
        "max_single_position_pct": 15,
        "margin_allowed": False,
        "leverage_allowed": False,
    },
    MarketRegime.UNKNOWN: {
        "max_total_exposure_pct": 60,
        "max_single_position_pct": 25,
        "margin_allowed": False,
        "leverage_allowed": False,
    },
}


def build_exposure_control_plan(regime: MarketRegime) -> ExposureControlPlan:
    """Build exposure control plan for a given market regime. Paper only."""
    limits = _REGIME_EXPOSURE.get(regime)
    if limits is None:
        return ExposureControlPlan(
            regime=regime,
            block_reasons=[RegimeBlockReason.INSUFFICIENT_DATA],
            note="regime_not_found",
            schema_version=_SCHEMA,
            policy_version=_POLICY,
            source_lineage=_LINEAGE,
        )

    return ExposureControlPlan(
        regime=regime,
        max_total_exposure_pct=int(limits["max_total_exposure_pct"]),
        max_single_position_pct=int(limits["max_single_position_pct"]),
        margin_allowed=bool(limits["margin_allowed"]),
        leverage_allowed=bool(limits["leverage_allowed"]),
        block_reasons=[],
        note=f"regime={regime.value} no_margin no_leverage",
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )


def check_exposure_within_limits(
    regime: MarketRegime,
    total_exposure_pct: float,
    single_position_pct: float,
) -> Dict[str, object]:
    """
    Check if given exposure values are within limits for regime.
    Returns {within_limits, violations}.
    """
    plan = build_exposure_control_plan(regime)
    violations = []
    if total_exposure_pct > plan.max_total_exposure_pct:
        violations.append(
            f"total_exposure {total_exposure_pct:.1f}% > limit {plan.max_total_exposure_pct}%"
        )
    if single_position_pct > plan.max_single_position_pct:
        violations.append(
            f"single_position {single_position_pct:.1f}% > limit {plan.max_single_position_pct}%"
        )
    return {
        "within_limits": len(violations) == 0,
        "violations": violations,
        "plan": plan,
    }
