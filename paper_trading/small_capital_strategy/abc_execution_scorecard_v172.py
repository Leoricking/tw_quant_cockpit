"""
paper_trading/small_capital_strategy/abc_execution_scorecard_v172.py
Execution scorecard for A/B/C Buy Point Execution Plan v1.7.2.
Score 0-100. No A+. Weights sum = 100.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCConditionStatus, ABCExecutionGrade,
    ABCRiskPermission, ABCWatchlistCompatibility, ABCMarketCompatibility,
    ABCExecutionBlockReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCConditionCheck, ABCStopLossExecutionPlan, ABCTakeProfitExecutionPlan,
    ABCPositionSizingBridgeResult, ABCWatchlistBridgeResult,
    ABCMarketRegimeBridgeResult, ABCExecutionScorecard,
)

# Weights (must sum to 100)
_W_BUY_POINT_CONDITION = 25
_W_RISK_SIZING         = 25
_W_WATCHLIST_TIER      = 15
_W_MARKET_REGIME       = 15
_W_STOP_LOSS           = 10
_W_TAKE_PROFIT         = 5
_W_SAFETY              = 5
_WEIGHTS_SUM           = 100


def _score_conditions(
    checks: List[ABCConditionCheck],
) -> float:
    """Score buy point condition quality (0-100)."""
    if not checks:
        return 0.0
    met = sum(1 for c in checks if c.status == ABCConditionStatus.MET)
    return round(met / len(checks) * 100, 2)


def _score_risk_sizing(ps: ABCPositionSizingBridgeResult) -> float:
    """Score risk / position sizing compliance (0-100)."""
    if ps is None:
        return 0.0
    if ps.risk_permission == ABCRiskPermission.BLOCKED:
        return 0.0
    if ps.training_cap_applied:
        return 60.0
    if ps.risk_permission == ABCRiskPermission.DEGRADED:
        return 70.0
    return 100.0


def _score_watchlist_tier(wb: ABCWatchlistBridgeResult) -> float:
    """Score watchlist tier compatibility (0-100)."""
    if wb is None:
        return 0.0
    compat_scores = {
        ABCWatchlistCompatibility.FULLY_COMPATIBLE: 100.0,
        ABCWatchlistCompatibility.COMPATIBLE:        80.0,
        ABCWatchlistCompatibility.DEGRADED:          50.0,
        ABCWatchlistCompatibility.BLOCKED:            0.0,
    }
    return compat_scores.get(wb.compatibility, 0.0)


def _score_market_regime(rb: ABCMarketRegimeBridgeResult) -> float:
    """Score market regime compatibility (0-100)."""
    if rb is None:
        return 0.0
    compat_scores = {
        ABCMarketCompatibility.COMPATIBLE:       100.0,
        ABCMarketCompatibility.COMPATIBLE_CORE:   80.0,
        ABCMarketCompatibility.DEGRADED:          50.0,
        ABCMarketCompatibility.BLOCKED:            0.0,
        ABCMarketCompatibility.UNKNOWN:           40.0,
    }
    return compat_scores.get(rb.compatibility, 0.0)


def _score_stop_loss(sl: ABCStopLossExecutionPlan) -> float:
    """Score stop loss quality (0-100)."""
    if sl is None:
        return 0.0
    if sl.stop_loss_price <= 0:
        return 0.0
    # Penalize if stop is too close (< 1%) or too wide (> 8%)
    pct = sl.stop_loss_pct_from_entry
    if pct <= 0:
        return 20.0
    if pct > 0.10:
        return 30.0
    if pct > 0.08:
        return 60.0
    if pct < 0.01:
        return 50.0
    return 100.0


def _score_take_profit(tp: ABCTakeProfitExecutionPlan) -> float:
    """Score take profit completeness (0-100)."""
    if tp is None:
        return 0.0
    if not tp.take_profit_references:
        return 0.0
    if len(tp.take_profit_references) >= 2:
        return 100.0
    return 70.0


def _score_safety(block_reasons: List[ABCExecutionBlockReason]) -> float:
    """Score safety compliance. Any safety block = 0."""
    safety_blocks = {
        ABCExecutionBlockReason.REAL_ORDER_REQUESTED,
        ABCExecutionBlockReason.BROKER_REQUESTED,
        ABCExecutionBlockReason.SAFETY_VIOLATION,
        ABCExecutionBlockReason.MARGIN_NOT_ALLOWED,
    }
    for reason in block_reasons:
        if reason in safety_blocks:
            return 0.0
    return 100.0


def _score_to_grade(score: float, has_safety_block: bool) -> ABCExecutionGrade:
    """Convert numeric score to grade. No A+."""
    if has_safety_block:
        return ABCExecutionGrade.BLOCKED
    if score >= 85:
        return ABCExecutionGrade.A
    if score >= 70:
        return ABCExecutionGrade.B
    if score >= 55:
        return ABCExecutionGrade.C
    if score >= 40:
        return ABCExecutionGrade.D
    return ABCExecutionGrade.F


def compute_scorecard(
    symbol: str,
    buy_point_type: ABCBuyPointType,
    condition_checks: List[ABCConditionCheck],
    stop_loss_plan: ABCStopLossExecutionPlan,
    take_profit_plan: ABCTakeProfitExecutionPlan,
    position_sizing: ABCPositionSizingBridgeResult,
    watchlist_bridge: ABCWatchlistBridgeResult,
    regime_bridge: ABCMarketRegimeBridgeResult,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCExecutionScorecard:
    """Compute ABC execution scorecard."""
    safety_score      = _score_safety(block_reasons)
    has_safety_block  = safety_score == 0.0

    if has_safety_block:
        return ABCExecutionScorecard(
            symbol=symbol,
            buy_point_type=buy_point_type,
            total_score=0.0,
            buy_point_condition_score=0.0,
            risk_sizing_score=0.0,
            watchlist_tier_score=0.0,
            market_regime_score=0.0,
            stop_loss_score=0.0,
            take_profit_score=0.0,
            safety_score=0.0,
            grade=ABCExecutionGrade.BLOCKED,
            weights_sum=_WEIGHTS_SUM,
        )

    bp_score   = _score_conditions(condition_checks)
    risk_score = _score_risk_sizing(position_sizing)
    wl_score   = _score_watchlist_tier(watchlist_bridge)
    re_score   = _score_market_regime(regime_bridge)
    sl_score   = _score_stop_loss(stop_loss_plan)
    tp_score   = _score_take_profit(take_profit_plan)

    total = (
        bp_score   * _W_BUY_POINT_CONDITION / 100
        + risk_score * _W_RISK_SIZING         / 100
        + wl_score   * _W_WATCHLIST_TIER      / 100
        + re_score   * _W_MARKET_REGIME       / 100
        + sl_score   * _W_STOP_LOSS           / 100
        + tp_score   * _W_TAKE_PROFIT         / 100
        + safety_score * _W_SAFETY            / 100
    )
    total = round(min(100.0, total), 2)

    # Hard block if any blocking condition
    if any(
        c.is_blocking for c in (condition_checks or [])
    ) or (position_sizing and position_sizing.risk_permission == ABCRiskPermission.BLOCKED):
        grade = ABCExecutionGrade.BLOCKED
    else:
        grade = _score_to_grade(total, has_safety_block)

    return ABCExecutionScorecard(
        symbol=symbol,
        buy_point_type=buy_point_type,
        total_score=total,
        buy_point_condition_score=round(bp_score, 2),
        risk_sizing_score=round(risk_score, 2),
        watchlist_tier_score=round(wl_score, 2),
        market_regime_score=round(re_score, 2),
        stop_loss_score=round(sl_score, 2),
        take_profit_score=round(tp_score, 2),
        safety_score=safety_score,
        grade=grade,
        weights_sum=_WEIGHTS_SUM,
    )


def get_scorecard_weights() -> dict:
    """Return scorecard weights. Must sum to 100."""
    return {
        "buy_point_condition": _W_BUY_POINT_CONDITION,
        "risk_sizing":         _W_RISK_SIZING,
        "watchlist_tier":      _W_WATCHLIST_TIER,
        "market_regime":       _W_MARKET_REGIME,
        "stop_loss":           _W_STOP_LOSS,
        "take_profit":         _W_TAKE_PROFIT,
        "safety":              _W_SAFETY,
        "sum":                 _WEIGHTS_SUM,
    }
