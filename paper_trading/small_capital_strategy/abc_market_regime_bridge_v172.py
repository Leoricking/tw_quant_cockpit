"""
paper_trading/small_capital_strategy/abc_market_regime_bridge_v172.py
Market regime compatibility bridge for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCMarketCompatibility,
    ABCExecutionBlockReason, ABCExecutionWarningReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCMarketRegimeBridgeResult,
)
from paper_trading.small_capital_strategy.watchlist_enums_v171 import WatchlistTier

_BULL     = "BULL"
_BEAR     = "BEAR"
_RISK_OFF = "RISK_OFF"
_NEUTRAL  = "NEUTRAL"
_UNKNOWN  = "UNKNOWN"

# regime → blocked buy points (non-CORE)
_REGIME_BLOCK_NON_CORE = {
    _BEAR: [
        ABCBuyPointType.B_PLATFORM_BREAKOUT,
        ABCBuyPointType.C_20MA_RECLAIM,
    ],
    _RISK_OFF: [ABCBuyPointType.B_PLATFORM_BREAKOUT],
}

# regime → fully blocked (all tiers)
_REGIME_FULL_BLOCK: dict = {}


def check_market_regime_compatibility(
    market_regime: str,
    buy_point_type: ABCBuyPointType,
    tier: str,
) -> ABCMarketRegimeBridgeResult:
    """Check market regime compatibility for a buy point and tier."""
    block_reasons: List[ABCExecutionBlockReason] = []
    warnings: List[ABCExecutionWarningReason] = []

    is_core = tier == WatchlistTier.CORE.value

    # Bear regime: only CORE A allowed
    if market_regime == _BEAR:
        if buy_point_type == ABCBuyPointType.B_PLATFORM_BREAKOUT:
            block_reasons.append(ABCExecutionBlockReason.MARKET_REGIME_BLOCKED)
        elif buy_point_type == ABCBuyPointType.C_20MA_RECLAIM:
            block_reasons.append(ABCExecutionBlockReason.MARKET_REGIME_BLOCKED)
        elif buy_point_type == ABCBuyPointType.A_10MA_PULLBACK and not is_core:
            block_reasons.append(ABCExecutionBlockReason.BEAR_REGIME_NON_CORE)

    # Risk-off: B is blocked
    elif market_regime == _RISK_OFF:
        if buy_point_type == ABCBuyPointType.B_PLATFORM_BREAKOUT:
            block_reasons.append(ABCExecutionBlockReason.RISK_OFF_REGIME)
        elif buy_point_type == ABCBuyPointType.C_20MA_RECLAIM:
            block_reasons.append(ABCExecutionBlockReason.RISK_OFF_REGIME)

    # Unknown: all non-CORE degraded
    elif market_regime == _UNKNOWN:
        if not is_core:
            warnings.append(ABCExecutionWarningReason.REGIME_DEGRADED)

    if block_reasons:
        compat = ABCMarketCompatibility.BLOCKED
    elif warnings:
        compat = ABCMarketCompatibility.DEGRADED
    elif market_regime == _BEAR and is_core:
        compat = ABCMarketCompatibility.COMPATIBLE_CORE
    else:
        compat = ABCMarketCompatibility.COMPATIBLE

    return ABCMarketRegimeBridgeResult(
        market_regime=market_regime,
        buy_point_type=buy_point_type,
        tier=tier,
        compatibility=compat,
        block_reasons=block_reasons,
        warnings=warnings,
    )


def get_compatible_regimes(buy_point_type: ABCBuyPointType) -> List[str]:
    """Return regimes that are compatible with a buy point type."""
    if buy_point_type == ABCBuyPointType.A_10MA_PULLBACK:
        return [_BULL, _NEUTRAL, _BEAR]  # BEAR only for CORE
    if buy_point_type == ABCBuyPointType.B_PLATFORM_BREAKOUT:
        return [_BULL, _NEUTRAL]
    if buy_point_type == ABCBuyPointType.C_20MA_RECLAIM:
        return [_BULL, _NEUTRAL]
    return []
