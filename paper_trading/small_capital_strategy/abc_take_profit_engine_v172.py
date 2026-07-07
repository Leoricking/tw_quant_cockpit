"""
paper_trading/small_capital_strategy/abc_take_profit_engine_v172.py
Take profit engine for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCTakeProfitMode, ABCExecutionBlockReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCSignalInput, ABCTakeProfitExecutionPlan,
)
from paper_trading.small_capital_strategy.watchlist_enums_v171 import WatchlistTier

_PARTIAL_PCT_LOW  = 0.10
_PARTIAL_PCT_HIGH = 0.15
_SWING_PCT_LOW    = 0.25
_SWING_PCT_HIGH   = 0.40


def _calc_references(entry: float, pcts: List[float]) -> List[float]:
    return [round(entry * (1 + p), 2) for p in pcts]


def build_a_take_profit_plan(
    signal: ABCSignalInput,
    tier: str,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCTakeProfitExecutionPlan:
    """Build take profit plan for A (10MA Pullback)."""
    if block_reasons:
        return ABCTakeProfitExecutionPlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
            take_profit_mode=ABCTakeProfitMode.NO_PLAN,
        )
    entry = signal.close
    tier_supports_swing = tier in (
        WatchlistTier.CORE.value,
        WatchlistTier.MAIN_THEME.value,
    )
    if tier_supports_swing:
        refs = _calc_references(entry, [_PARTIAL_PCT_LOW, _SWING_PCT_LOW, _SWING_PCT_HIGH])
        mode = ABCTakeProfitMode.SWING_25_40_PCT
        partial = _PARTIAL_PCT_LOW
        swing = _SWING_PCT_LOW
        note = f"Partial {_PARTIAL_PCT_LOW*100:.0f}%, swing {_SWING_PCT_LOW*100:.0f}%-{_SWING_PCT_HIGH*100:.0f}%"
    else:
        refs = _calc_references(entry, [_PARTIAL_PCT_LOW, _PARTIAL_PCT_HIGH])
        mode = ABCTakeProfitMode.PARTIAL_10_15_PCT
        partial = _PARTIAL_PCT_LOW
        swing = 0.0
        note = f"Partial {_PARTIAL_PCT_LOW*100:.0f}%-{_PARTIAL_PCT_HIGH*100:.0f}%"
    return ABCTakeProfitExecutionPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        take_profit_mode=mode,
        take_profit_references=refs,
        partial_pct_first=partial,
        swing_pct_target=swing,
        take_profit_note=note,
    )


def build_b_take_profit_plan(
    signal: ABCSignalInput,
    tier: str,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCTakeProfitExecutionPlan:
    """Build take profit plan for B (Platform Breakout)."""
    if block_reasons:
        return ABCTakeProfitExecutionPlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
            take_profit_mode=ABCTakeProfitMode.NO_PLAN,
        )
    entry = signal.close
    refs = _calc_references(entry, [_PARTIAL_PCT_LOW, _PARTIAL_PCT_HIGH, _SWING_PCT_LOW])
    note = f"Partial {_PARTIAL_PCT_LOW*100:.0f}% first, then staged"
    return ABCTakeProfitExecutionPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.B_PLATFORM_BREAKOUT,
        take_profit_mode=ABCTakeProfitMode.STAGED,
        take_profit_references=refs,
        partial_pct_first=_PARTIAL_PCT_LOW,
        swing_pct_target=_SWING_PCT_LOW,
        take_profit_note=note,
    )


def build_c_take_profit_plan(
    signal: ABCSignalInput,
    tier: str,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCTakeProfitExecutionPlan:
    """Build take profit plan for C (20MA Reclaim)."""
    if block_reasons:
        return ABCTakeProfitExecutionPlan(
            symbol=signal.symbol,
            buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
            take_profit_mode=ABCTakeProfitMode.NO_PLAN,
        )
    entry = signal.close
    refs = _calc_references(entry, [_SWING_PCT_LOW, _SWING_PCT_HIGH])
    note = f"Prior high / staged {_SWING_PCT_LOW*100:.0f}%-{_SWING_PCT_HIGH*100:.0f}%"
    return ABCTakeProfitExecutionPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.C_20MA_RECLAIM,
        take_profit_mode=ABCTakeProfitMode.SWING_25_40_PCT,
        take_profit_references=refs,
        partial_pct_first=_PARTIAL_PCT_LOW,
        swing_pct_target=_SWING_PCT_LOW,
        take_profit_note=note,
    )


def build_take_profit_plan(
    signal: ABCSignalInput,
    tier: str,
    block_reasons: List[ABCExecutionBlockReason],
) -> ABCTakeProfitExecutionPlan:
    """Dispatch take profit plan building by buy point type."""
    bpt = signal.buy_point_type
    if bpt == ABCBuyPointType.A_10MA_PULLBACK:
        return build_a_take_profit_plan(signal, tier, block_reasons)
    if bpt == ABCBuyPointType.B_PLATFORM_BREAKOUT:
        return build_b_take_profit_plan(signal, tier, block_reasons)
    if bpt == ABCBuyPointType.C_20MA_RECLAIM:
        return build_c_take_profit_plan(signal, tier, block_reasons)
    return ABCTakeProfitExecutionPlan(
        symbol=signal.symbol,
        buy_point_type=ABCBuyPointType.UNSUPPORTED,
        take_profit_mode=ABCTakeProfitMode.NO_PLAN,
        take_profit_note="Unsupported buy point type",
    )


def get_take_profit_constants() -> dict:
    """Return take profit engine constants."""
    return {
        "partial_pct_low": _PARTIAL_PCT_LOW,
        "partial_pct_high": _PARTIAL_PCT_HIGH,
        "swing_pct_low": _SWING_PCT_LOW,
        "swing_pct_high": _SWING_PCT_HIGH,
    }
