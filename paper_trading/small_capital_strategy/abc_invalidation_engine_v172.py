"""
paper_trading/small_capital_strategy/abc_invalidation_engine_v172.py
Invalidation engine for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCInvalidationReason, ABCExecutionBlockReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCSignalInput, ABCInvalidationPlan,
)

_BARS_TO_CONFIRM_A = 3
_BARS_TO_CONFIRM_B = 2
_BARS_TO_CONFIRM_C = 3


def build_a_invalidation_plan(
    signal: ABCSignalInput,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCInvalidationPlan:
    """Build invalidation plan for A (10MA Pullback)."""
    reasons = [
        ABCInvalidationReason.CLOSE_BELOW_MA20,
        ABCInvalidationReason.MA10_RECLAIM_FAILS,
        ABCInvalidationReason.STOP_LOSS_HIT,
    ]
    notes = [
        f"Close below MA20={signal.ma20:.2f} invalidates plan",
        f"MA10 reclaim fails within {_BARS_TO_CONFIRM_A} bars",
        "Stop loss triggered",
    ]
    return ABCInvalidationPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        invalidation_reasons=reasons,
        invalidation_notes=notes,
        bars_to_confirm=_BARS_TO_CONFIRM_A,
    )


def build_b_invalidation_plan(
    signal: ABCSignalInput,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCInvalidationPlan:
    """Build invalidation plan for B (Platform Breakout)."""
    reasons = [
        ABCInvalidationReason.BREAKOUT_BACK_INTO_PLATFORM,
        ABCInvalidationReason.VOLUME_COLLAPSE,
        ABCInvalidationReason.STOP_LOSS_HIT,
    ]
    notes = [
        f"Close back into platform below={signal.prior_platform_high:.2f} with volume",
        "Volume collapses after breakout confirming failure",
        "Stop loss triggered",
    ]
    return ABCInvalidationPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
        invalidation_reasons=reasons,
        invalidation_notes=notes,
        bars_to_confirm=_BARS_TO_CONFIRM_B,
    )


def build_c_invalidation_plan(
    signal: ABCSignalInput,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCInvalidationPlan:
    """Build invalidation plan for C (20MA Reclaim)."""
    reasons = [
        ABCInvalidationReason.RECLAIM_FAILS_N_BARS,
        ABCInvalidationReason.CLOSE_BELOW_MA20,
        ABCInvalidationReason.STOP_LOSS_HIT,
    ]
    notes = [
        f"MA20 reclaim fails to hold within {_BARS_TO_CONFIRM_C} bars",
        f"Close below MA20={signal.ma20:.2f} invalidates second wave thesis",
        "Stop loss triggered",
    ]
    return ABCInvalidationPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
        invalidation_reasons=reasons,
        invalidation_notes=notes,
        bars_to_confirm=_BARS_TO_CONFIRM_C,
    )


def build_invalidation_plan(
    signal: ABCSignalInput,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCInvalidationPlan:
    """Dispatch invalidation plan building by buy point type."""
    bpt = signal.buy_point_type
    if bpt == ABCBuyPointType.A_10MA_PULLBACK:
        return build_a_invalidation_plan(signal, block_reasons)
    if bpt == ABCBuyPointType.B_PLATFORM_BREAKOUT:
        return build_b_invalidation_plan(signal, block_reasons)
    if bpt == ABCBuyPointType.C_20MA_RECLAIM:
        return build_c_invalidation_plan(signal, block_reasons)
    return ABCInvalidationPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.UNSUPPORTED,
        invalidation_reasons=[ABCInvalidationReason.NOT_SET],
        invalidation_notes=["Unsupported buy point type"],
    )


def get_invalidation_bars(bpt: ABCBuyPointType) -> int:
    """Return N bars to confirm invalidation for a buy point type."""
    if bpt == ABCBuyPointType.A_10MA_PULLBACK:
        return _BARS_TO_CONFIRM_A
    if bpt == ABCBuyPointType.B_PLATFORM_BREAKOUT:
        return _BARS_TO_CONFIRM_B
    if bpt == ABCBuyPointType.C_20MA_RECLAIM:
        return _BARS_TO_CONFIRM_C
    return 0
