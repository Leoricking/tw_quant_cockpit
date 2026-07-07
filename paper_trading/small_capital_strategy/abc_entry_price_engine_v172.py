"""
paper_trading/small_capital_strategy/abc_entry_price_engine_v172.py
Entry price engine for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCEntryMode, ABCExecutionStatus, ABCExecutionBlockReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCSignalInput, ABCNormalizedSignal, ABCEntryPricePlan,
)


def build_a_entry_plan(
    signal: ABCSignalInput,
    normalized: ABCNormalizedSignal,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCEntryPricePlan:
    """Build entry price plan for A (10MA Pullback)."""
    if block_reasons:
        return ABCEntryPricePlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
            entry_mode=ABCEntryMode.BLOCKED,
            entry_price=0.0,
            entry_price_note="Blocked: conditions not met",
            status=ABCExecutionStatus.BLOCKED,
            block_reasons=list(block_reasons),
        )

    # Entry: close if already above MA10, else MA10 reclaim reference
    if normalized.above_ma10 and normalized.low_touched_ma10:
        entry_price = signal.close
        entry_note = f"MA10 reclaim confirmed at close={signal.close:.2f}"
        status = ABCExecutionStatus.READY
    elif normalized.above_ma10:
        entry_price = signal.ma10
        entry_note = f"Waiting MA10 reclaim ref={signal.ma10:.2f}"
        status = ABCExecutionStatus.WAITING_CONFIRMATION
    else:
        entry_price = signal.ma10
        entry_note = f"MA10 reclaim not yet confirmed, ref={signal.ma10:.2f}"
        status = ABCExecutionStatus.WAITING_CONFIRMATION

    return ABCEntryPricePlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        entry_mode=ABCEntryMode.MA10_RECLAIM,
        entry_price=entry_price,
        entry_price_note=entry_note,
        status=status,
        block_reasons=[],
    )


def build_b_entry_plan(
    signal: ABCSignalInput,
    normalized: ABCNormalizedSignal,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCEntryPricePlan:
    """Build entry price plan for B (Platform Breakout)."""
    if block_reasons:
        return ABCEntryPricePlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
            entry_mode=ABCEntryMode.BLOCKED,
            entry_price=0.0,
            entry_price_note="Blocked: conditions not met",
            status=ABCExecutionStatus.BLOCKED,
            block_reasons=list(block_reasons),
        )

    pph = signal.prior_platform_high
    breakout_confirmed = normalized.volume_confirmed and signal.close > pph
    if breakout_confirmed:
        entry_price = signal.close
        entry_note = f"Breakout confirmed at close={signal.close:.2f} > platform={pph:.2f}"
        status = ABCExecutionStatus.READY
    else:
        entry_price = pph
        entry_note = f"Waiting breakout above platform={pph:.2f}"
        status = ABCExecutionStatus.WAITING_CONFIRMATION

    return ABCEntryPricePlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
        entry_mode=ABCEntryMode.BREAKOUT_CONFIRMATION,
        entry_price=entry_price,
        entry_price_note=entry_note,
        status=status,
        block_reasons=[],
    )


def build_c_entry_plan(
    signal: ABCSignalInput,
    normalized: ABCNormalizedSignal,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCEntryPricePlan:
    """Build entry price plan for C (20MA Reclaim)."""
    if block_reasons:
        return ABCEntryPricePlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
            entry_mode=ABCEntryMode.BLOCKED,
            entry_price=0.0,
            entry_price_note="Blocked: conditions not met",
            status=ABCExecutionStatus.BLOCKED,
            block_reasons=list(block_reasons),
        )

    if normalized.ma20_reclaim_valid and normalized.pullback_complete:
        entry_price = signal.close
        entry_note = f"MA20 reclaim confirmed at close={signal.close:.2f}"
        status = ABCExecutionStatus.READY
    else:
        entry_price = signal.ma20
        entry_note = f"Waiting MA20 reclaim, ref={signal.ma20:.2f}"
        status = ABCExecutionStatus.WAITING_CONFIRMATION

    return ABCEntryPricePlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
        entry_mode=ABCEntryMode.MA20_RECLAIM,
        entry_price=entry_price,
        entry_price_note=entry_note,
        status=status,
        block_reasons=[],
    )


def build_entry_plan(
    signal: ABCSignalInput,
    normalized: ABCNormalizedSignal,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCEntryPricePlan:
    """Dispatch entry plan building by buy point type."""
    bpt = signal.buy_point_type
    if bpt == ABCBuyPointType.A_10MA_PULLBACK:
        return build_a_entry_plan(signal, normalized, block_reasons)
    if bpt == ABCBuyPointType.B_PLATFORM_BREAKOUT:
        return build_b_entry_plan(signal, normalized, block_reasons)
    if bpt == ABCBuyPointType.C_20MA_RECLAIM:
        return build_c_entry_plan(signal, normalized, block_reasons)
    return ABCEntryPricePlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.UNSUPPORTED,
        entry_mode=ABCEntryMode.BLOCKED,
        entry_price=0.0,
        entry_price_note="Unsupported buy point type",
        status=ABCExecutionStatus.BLOCKED,
        block_reasons=[ABCExecutionBlockReason.UNSUPPORTED_BUY_POINT],
    )
