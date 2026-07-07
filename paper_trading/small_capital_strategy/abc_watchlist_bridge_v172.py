"""
paper_trading/small_capital_strategy/abc_watchlist_bridge_v172.py
Watchlist tier compatibility bridge for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCWatchlistCompatibility, ABCExecutionBlockReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCWatchlistBridgeResult,
)
from paper_trading.small_capital_strategy.watchlist_enums_v171 import WatchlistTier
from paper_trading.small_capital_strategy.abc_position_sizing_bridge_v172 import (
    TRAINING_MAX_AMOUNT,
)

# Tier → allowed buy points
_TIER_ALLOWED: dict = {
    WatchlistTier.CORE.value:        [ABCBuyPointType.A_10MA_PULLBACK],
    WatchlistTier.MAIN_THEME.value:  [
        ABCBuyPointType.A_10MA_PULLBACK,
        ABCBuyPointType.B_PLATFORM_BREAKOUT,
        ABCBuyPointType.C_20MA_RECLAIM,
    ],
    WatchlistTier.SECOND_WAVE.value: [
        ABCBuyPointType.C_20MA_RECLAIM,
        ABCBuyPointType.A_10MA_PULLBACK,
    ],
    WatchlistTier.TRAINING.value:    [
        ABCBuyPointType.B_PLATFORM_BREAKOUT,
    ],
    WatchlistTier.EXCLUDED.value:    [],
}

# Tier → preferred buy points
_TIER_PREFERRED: dict = {
    WatchlistTier.CORE.value:        [ABCBuyPointType.A_10MA_PULLBACK],
    WatchlistTier.MAIN_THEME.value:  [
        ABCBuyPointType.A_10MA_PULLBACK,
        ABCBuyPointType.B_PLATFORM_BREAKOUT,
        ABCBuyPointType.C_20MA_RECLAIM,
    ],
    WatchlistTier.SECOND_WAVE.value: [
        ABCBuyPointType.C_20MA_RECLAIM,
        ABCBuyPointType.A_10MA_PULLBACK,
    ],
    WatchlistTier.TRAINING.value:    [ABCBuyPointType.B_PLATFORM_BREAKOUT],
    WatchlistTier.EXCLUDED.value:    [],
}


def check_watchlist_compatibility(
    symbol: str,
    tier: str,
    buy_point_type: ABCBuyPointType,
) -> ABCWatchlistBridgeResult:
    """Check watchlist tier compatibility for a buy point type."""
    block_reasons: List[ABCExecutionBlockReason] = []
    training_cap = 0.0

    if tier == WatchlistTier.EXCLUDED.value:
        block_reasons.append(ABCExecutionBlockReason.WATCHLIST_EXCLUDED)
        return ABCWatchlistBridgeResult(
            symbol=symbol,
            tier=tier,
            compatibility=ABCWatchlistCompatibility.BLOCKED,
            allowed_buy_points=[],
            preferred_buy_points=[],
            block_reasons=block_reasons,
            training_cap=0.0,
        )

    allowed = _TIER_ALLOWED.get(tier, [])
    preferred = _TIER_PREFERRED.get(tier, [])

    if buy_point_type not in allowed:
        block_reasons.append(ABCExecutionBlockReason.WATCHLIST_EXCLUDED)
        compat = ABCWatchlistCompatibility.BLOCKED
    elif buy_point_type in preferred:
        compat = ABCWatchlistCompatibility.FULLY_COMPATIBLE
    else:
        compat = ABCWatchlistCompatibility.COMPATIBLE

    if tier == WatchlistTier.TRAINING.value:
        training_cap = TRAINING_MAX_AMOUNT

    if block_reasons:
        compat = ABCWatchlistCompatibility.BLOCKED

    return ABCWatchlistBridgeResult(
        symbol=symbol,
        tier=tier,
        compatibility=compat,
        allowed_buy_points=list(allowed),
        preferred_buy_points=list(preferred),
        block_reasons=block_reasons,
        training_cap=training_cap,
    )


def get_tier_allowed_buy_points(tier: str) -> List[ABCBuyPointType]:
    """Return allowed buy point types for a given tier."""
    return list(_TIER_ALLOWED.get(tier, []))


def get_tier_preferred_buy_points(tier: str) -> List[ABCBuyPointType]:
    """Return preferred buy point types for a given tier."""
    return list(_TIER_PREFERRED.get(tier, []))
