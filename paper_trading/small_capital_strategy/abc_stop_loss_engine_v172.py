"""
paper_trading/small_capital_strategy/abc_stop_loss_engine_v172.py
Stop loss engine for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCStopLossMode, ABCExecutionStatus, ABCExecutionBlockReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCSignalInput, ABCStopLossExecutionPlan,
)

_MAX_STOP_LOSS_PCT = 0.10   # 10% maximum stop from entry


def _pct_from_entry(entry: float, stop: float) -> float:
    if entry <= 0:
        return 0.0
    return abs(entry - stop) / entry


def build_a_stop_loss_plan(
    signal: ABCSignalInput,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCStopLossExecutionPlan:
    """Build stop loss plan for A (10MA Pullback)."""
    if block_reasons:
        return ABCStopLossExecutionPlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
            stop_loss_mode=ABCStopLossMode.NOT_SET,
            stop_loss_price=0.0,
            status=ABCExecutionStatus.BLOCKED,
        )
    # Stop: min(MA10 break ref, recent swing low ≈ MA20 * 0.97)
    ma10_break_ref = signal.ma10 * 0.99
    swing_low = signal.ma20 * 0.97
    stop_price = min(ma10_break_ref, swing_low)
    pct = _pct_from_entry(signal.close, stop_price)
    note = f"stop=min(MA10_break={ma10_break_ref:.2f}, swing_low={swing_low:.2f})={stop_price:.2f}"
    return ABCStopLossExecutionPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        stop_loss_mode=ABCStopLossMode.MA10_BREAK_REF,
        stop_loss_price=stop_price,
        stop_loss_note=note,
        stop_loss_pct_from_entry=round(pct, 4),
        status=ABCExecutionStatus.READY,
    )


def build_b_stop_loss_plan(
    signal: ABCSignalInput,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCStopLossExecutionPlan:
    """Build stop loss plan for B (Platform Breakout)."""
    if block_reasons:
        return ABCStopLossExecutionPlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
            stop_loss_mode=ABCStopLossMode.NOT_SET,
            stop_loss_price=0.0,
            status=ABCExecutionStatus.BLOCKED,
        )
    # Stop: platform upper bound or breakout day low
    platform_upper = signal.prior_platform_high
    breakout_day_low = signal.close * 0.97
    stop_price = max(platform_upper * 0.99, breakout_day_low)
    pct = _pct_from_entry(signal.close, stop_price)
    note = (f"stop=max(platform_upper*0.99={platform_upper*0.99:.2f}, "
            f"breakout_day_low={breakout_day_low:.2f})={stop_price:.2f}")
    return ABCStopLossExecutionPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
        stop_loss_mode=ABCStopLossMode.PLATFORM_LOWER,
        stop_loss_price=stop_price,
        stop_loss_note=note,
        stop_loss_pct_from_entry=round(pct, 4),
        status=ABCExecutionStatus.READY,
    )


def build_c_stop_loss_plan(
    signal: ABCSignalInput,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCStopLossExecutionPlan:
    """Build stop loss plan for C (20MA Reclaim)."""
    if block_reasons:
        return ABCStopLossExecutionPlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
            stop_loss_mode=ABCStopLossMode.NOT_SET,
            stop_loss_price=0.0,
            status=ABCExecutionStatus.BLOCKED,
        )
    # Stop: below MA20 or pullback low ≈ MA60 * 0.97
    below_ma20 = signal.ma20 * 0.995
    pullback_low = signal.ma60 * 0.97
    stop_price = min(below_ma20, pullback_low)
    pct = _pct_from_entry(signal.close, stop_price)
    note = f"stop=min(below_MA20={below_ma20:.2f}, pullback_low={pullback_low:.2f})={stop_price:.2f}"
    return ABCStopLossExecutionPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
        stop_loss_mode=ABCStopLossMode.BELOW_MA20,
        stop_loss_price=stop_price,
        stop_loss_note=note,
        stop_loss_pct_from_entry=round(pct, 4),
        status=ABCExecutionStatus.READY,
    )


def build_stop_loss_plan(
    signal: ABCSignalInput,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCStopLossExecutionPlan:
    """Dispatch stop loss plan building by buy point type."""
    bpt = signal.buy_point_type
    if bpt == ABCBuyPointType.A_10MA_PULLBACK:
        return build_a_stop_loss_plan(signal, block_reasons)
    if bpt == ABCBuyPointType.B_PLATFORM_BREAKOUT:
        return build_b_stop_loss_plan(signal, block_reasons)
    if bpt == ABCBuyPointType.C_20MA_RECLAIM:
        return build_c_stop_loss_plan(signal, block_reasons)
    return ABCStopLossExecutionPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.UNSUPPORTED,
        stop_loss_mode=ABCStopLossMode.NOT_SET,
        stop_loss_price=0.0,
        stop_loss_note="Unsupported buy point type",
        status=ABCExecutionStatus.BLOCKED,
    )


def validate_stop_loss(stop_price: float, entry_price: float) -> bool:
    """Return True if stop loss is valid (below entry and within max pct)."""
    if entry_price <= 0 or stop_price <= 0:
        return False
    if stop_price >= entry_price:
        return False
    pct = _pct_from_entry(entry_price, stop_price)
    return pct <= _MAX_STOP_LOSS_PCT


def get_stop_loss_constants() -> dict:
    """Return stop loss engine constants."""
    return {"max_stop_loss_pct": _MAX_STOP_LOSS_PCT}
