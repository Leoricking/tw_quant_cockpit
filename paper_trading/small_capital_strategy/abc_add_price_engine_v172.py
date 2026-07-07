"""
paper_trading/small_capital_strategy/abc_add_price_engine_v172.py
Add price engine for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCAddMode, ABCExecutionStatus, ABCExecutionBlockReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCSignalInput, ABCNormalizedSignal, ABCAddPricePlan,
)


def build_a_add_plan(
    signal: ABCSignalInput,
    normalized: ABCNormalizedSignal,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCAddPricePlan:
    """Build add plan for A (10MA Pullback)."""
    if block_reasons:
        return ABCAddPricePlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
            add_mode=ABCAddMode.BLOCKED,
            add_price=0.0,
            status=ABCExecutionStatus.BLOCKED,
        )
    # Add on MA5 reclaim or prior high breakout
    add_price = signal.ma5 if signal.ma5 > 0 else signal.close * 1.02
    add_note = f"Add on MA5 reclaim ref={add_price:.2f} or prior high breakout"
    return ABCAddPricePlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        add_mode=ABCAddMode.MA5_RECLAIM,
        add_price=add_price,
        add_price_note=add_note,
        max_add_units=1,
        status=ABCExecutionStatus.WAITING_CONFIRMATION,
    )


def build_b_add_plan(
    signal: ABCSignalInput,
    normalized: ABCNormalizedSignal,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCAddPricePlan:
    """Build add plan for B (Platform Breakout)."""
    if block_reasons:
        return ABCAddPricePlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
            add_mode=ABCAddMode.BLOCKED,
            add_price=0.0,
            status=ABCExecutionStatus.BLOCKED,
        )
    # Add on second-day hold or retest hold
    add_price = signal.close * 1.01
    add_note = f"Add on second-day hold or retest hold near={add_price:.2f}"
    return ABCAddPricePlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
        add_mode=ABCAddMode.SECOND_DAY_HOLD,
        add_price=add_price,
        add_price_note=add_note,
        max_add_units=1,
        status=ABCExecutionStatus.WAITING_CONFIRMATION,
    )


def build_c_add_plan(
    signal: ABCSignalInput,
    normalized: ABCNormalizedSignal,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCAddPricePlan:
    """Build add plan for C (20MA Reclaim)."""
    if block_reasons:
        return ABCAddPricePlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
            add_mode=ABCAddMode.BLOCKED,
            add_price=0.0,
            status=ABCExecutionStatus.BLOCKED,
        )
    # Add on reaction high breakout
    add_price = signal.close * 1.03
    add_note = f"Add on reaction high breakout ref={add_price:.2f}"
    return ABCAddPricePlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
        add_mode=ABCAddMode.REACTION_HIGH,
        add_price=add_price,
        add_price_note=add_note,
        max_add_units=1,
        status=ABCExecutionStatus.WAITING_CONFIRMATION,
    )


def build_add_plan(
    signal: ABCSignalInput,
    normalized: ABCNormalizedSignal,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCAddPricePlan:
    """Dispatch add plan building by buy point type."""
    bpt = signal.buy_point_type
    if bpt == ABCBuyPointType.A_10MA_PULLBACK:
        return build_a_add_plan(signal, normalized, block_reasons)
    if bpt == ABCBuyPointType.B_PLATFORM_BREAKOUT:
        return build_b_add_plan(signal, normalized, block_reasons)
    if bpt == ABCBuyPointType.C_20MA_RECLAIM:
        return build_c_add_plan(signal, normalized, block_reasons)
    return ABCAddPricePlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.UNSUPPORTED,
        add_mode=ABCAddMode.BLOCKED,
        add_price=0.0,
        add_price_note="Unsupported buy point type",
        status=ABCExecutionStatus.BLOCKED,
    )
