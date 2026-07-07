"""
paper_trading/small_capital_strategy/abc_condition_checker_v172.py
Condition checker for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Tuple

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCConditionStatus, ABCExecutionBlockReason,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCConditionCheck, ABCNormalizedSignal,
)
from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, ThemeStrength,
)

_BEAR_REGIME     = "BEAR"
_RISK_OFF_REGIME = "RISK_OFF"
_UNKNOWN_REGIME  = "UNKNOWN"


def _make_check(
    name: str,
    bpt: ABCBuyPointType,
    met: bool,
    detail: str = "",
    block_reason: ABCExecutionBlockReason = None,
) -> ABCConditionCheck:
    status = ABCConditionStatus.MET if met else ABCConditionStatus.NOT_MET
    is_blocking = (not met) and (block_reason is not None)
    return ABCConditionCheck(
        condition_name=name,
        buy_point_type=bpt,
        status=status,
        detail=detail,
        is_blocking=is_blocking,
        block_reason=block_reason if not met else None,
    )


def check_a_conditions(
    signal: ABCNormalizedSignal,
    tier: str,
    market_regime: str,
) -> List[ABCConditionCheck]:
    """Check all A (10MA Pullback) entry conditions."""
    bpt = ABCBuyPointType.A_10MA_PULLBACK
    checks = []
    raw = signal.raw

    checks.append(_make_check("tier_not_excluded", bpt,
        tier != WatchlistTier.EXCLUDED.value,
        f"tier={tier}",
        ABCExecutionBlockReason.WATCHLIST_EXCLUDED))

    theme_ok = raw.theme_strength in (
        ThemeStrength.STRONG.value, ThemeStrength.LEADING.value
    ) if raw else False
    checks.append(_make_check("theme_strength_strong_or_leading", bpt,
        theme_ok,
        f"theme={getattr(raw, 'theme_strength', 'N/A')}",
        ABCExecutionBlockReason.WEAK_THEME))

    checks.append(_make_check("close_above_ma20", bpt,
        signal.above_ma20,
        f"above_ma20={signal.above_ma20}",
        ABCExecutionBlockReason.BELOW_20MA))

    checks.append(_make_check("close_above_ma60", bpt,
        signal.above_ma60,
        f"above_ma60={signal.above_ma60}",
        ABCExecutionBlockReason.BELOW_60MA))

    checks.append(_make_check("low_touched_ma10", bpt,
        signal.low_touched_ma10,
        f"low_touched_ma10={signal.low_touched_ma10}",
        None))

    checks.append(_make_check("above_ma10", bpt,
        signal.above_ma10,
        f"above_ma10={signal.above_ma10}",
        None))

    checks.append(_make_check("volume_contracting", bpt,
        signal.volume_contracting,
        f"volume_contracting={signal.volume_contracting}",
        None))

    checks.append(_make_check("kd_not_dead_cross", bpt,
        signal.kd_not_dead_cross,
        f"kd_not_dead_cross={signal.kd_not_dead_cross}",
        None))

    checks.append(_make_check("institutional_not_selling", bpt,
        signal.institutional_not_selling,
        f"inst_ok={signal.institutional_not_selling}",
        ABCExecutionBlockReason.INSTITUTIONAL_HEAVY_SELLING))

    checks.append(_make_check("financing_not_overheated", bpt,
        signal.financing_safe,
        f"financing_safe={signal.financing_safe}",
        ABCExecutionBlockReason.FINANCING_OVERHEATED))

    # Bear regime: only CORE allowed
    if market_regime == _BEAR_REGIME:
        bear_ok = tier == WatchlistTier.CORE.value
        checks.append(_make_check("bear_regime_core_only", bpt,
            bear_ok,
            f"regime=BEAR tier={tier}",
            ABCExecutionBlockReason.BEAR_REGIME_NON_CORE))
    else:
        checks.append(_make_check("regime_not_bear_blocked", bpt,
            True, f"regime={market_regime}"))

    return checks


def check_b_conditions(
    signal: ABCNormalizedSignal,
    tier: str,
    market_regime: str,
) -> List[ABCConditionCheck]:
    """Check all B (Platform Breakout) entry conditions."""
    bpt = ABCBuyPointType.B_PLATFORM_BREAKOUT
    checks = []
    raw = signal.raw

    allowed_tiers = {
        WatchlistTier.MAIN_THEME.value,
        WatchlistTier.SECOND_WAVE.value,
        WatchlistTier.TRAINING.value,
    }
    checks.append(_make_check("tier_allowed_for_b", bpt,
        tier in allowed_tiers,
        f"tier={tier}",
        ABCExecutionBlockReason.WATCHLIST_EXCLUDED))

    checks.append(_make_check("consolidation_valid", bpt,
        signal.consolidation_valid,
        f"consolidation_valid={signal.consolidation_valid}",
        None))

    # close > prior platform high → use volume_confirmed as proxy
    breakout_above = signal.volume_confirmed
    if raw and raw.prior_platform_high > 0:
        breakout_above = raw.close > raw.prior_platform_high
    checks.append(_make_check("close_above_prior_platform_high", bpt,
        breakout_above,
        f"breakout={breakout_above}",
        ABCExecutionBlockReason.BREAKOUT_FAILED))

    checks.append(_make_check("volume_confirmed", bpt,
        signal.volume_confirmed,
        f"volume_confirmed={signal.volume_confirmed}",
        ABCExecutionBlockReason.VOLUME_NOT_CONFIRMED))

    checks.append(_make_check("financing_not_overheated", bpt,
        signal.financing_safe,
        f"financing_safe={signal.financing_safe}",
        ABCExecutionBlockReason.FINANCING_OVERHEATED))

    # B is blocked in BEAR regime
    bear_blocked = market_regime == _BEAR_REGIME
    checks.append(_make_check("regime_not_bear", bpt,
        not bear_blocked,
        f"regime={market_regime}",
        ABCExecutionBlockReason.MARKET_REGIME_BLOCKED))

    return checks


def check_c_conditions(
    signal: ABCNormalizedSignal,
    tier: str,
    market_regime: str,
) -> List[ABCConditionCheck]:
    """Check all C (20MA Reclaim) entry conditions."""
    bpt = ABCBuyPointType.C_20MA_RECLAIM
    checks = []

    allowed_tiers = {WatchlistTier.SECOND_WAVE.value, WatchlistTier.MAIN_THEME.value}
    checks.append(_make_check("tier_second_wave_or_main", bpt,
        tier in allowed_tiers,
        f"tier={tier}",
        ABCExecutionBlockReason.WATCHLIST_EXCLUDED))

    checks.append(_make_check("had_first_wave", bpt,
        signal.first_wave_present,
        f"first_wave={signal.first_wave_present}",
        ABCExecutionBlockReason.NO_FIRST_WAVE))

    checks.append(_make_check("pullback_completed", bpt,
        signal.pullback_complete,
        f"pullback_complete={signal.pullback_complete}",
        None))

    checks.append(_make_check("close_above_ma20", bpt,
        signal.ma20_reclaim_valid,
        f"ma20_reclaim={signal.ma20_reclaim_valid}",
        ABCExecutionBlockReason.BELOW_20MA))

    checks.append(_make_check("volume_dry_up_before_reclaim", bpt,
        signal.volume_contracting,
        f"vol_dry_up={signal.volume_contracting}",
        None))

    checks.append(_make_check("kd_improving", bpt,
        signal.kd_improving,
        f"kd_improving={signal.kd_improving}",
        None))

    checks.append(_make_check("institutional_reaccumulation", bpt,
        signal.institutional_not_selling,
        f"inst_reaccumulation={signal.institutional_not_selling}",
        None))

    checks.append(_make_check("financing_not_overheated", bpt,
        signal.financing_safe,
        f"financing_safe={signal.financing_safe}",
        ABCExecutionBlockReason.FINANCING_OVERHEATED))

    # C is blocked in RISK_OFF
    risk_off_blocked = market_regime == _RISK_OFF_REGIME
    checks.append(_make_check("regime_not_risk_off", bpt,
        not risk_off_blocked,
        f"regime={market_regime}",
        ABCExecutionBlockReason.RISK_OFF_REGIME))

    return checks


def check_conditions(
    signal: ABCNormalizedSignal,
    tier: str,
    market_regime: str,
) -> Tuple[List[ABCConditionCheck], List[ABCExecutionBlockReason]]:
    """Dispatch condition checking by buy point type."""
    bpt = signal.buy_point_type
    if bpt == ABCBuyPointType.A_10MA_PULLBACK:
        checks = check_a_conditions(signal, tier, market_regime)
    elif bpt == ABCBuyPointType.B_PLATFORM_BREAKOUT:
        checks = check_b_conditions(signal, tier, market_regime)
    elif bpt == ABCBuyPointType.C_20MA_RECLAIM:
        checks = check_c_conditions(signal, tier, market_regime)
    else:
        checks = [_make_check("unsupported_buy_point", bpt,
            False, f"buy_point_type={bpt}",
            ABCExecutionBlockReason.UNSUPPORTED_BUY_POINT)]

    block_reasons = [
        c.block_reason for c in checks
        if c.is_blocking and c.block_reason is not None
    ]
    return checks, block_reasons


def get_condition_names(bpt: ABCBuyPointType) -> List[str]:
    """Return expected condition names for a buy point type."""
    if bpt == ABCBuyPointType.A_10MA_PULLBACK:
        return [
            "tier_not_excluded", "theme_strength_strong_or_leading",
            "close_above_ma20", "close_above_ma60", "low_touched_ma10",
            "above_ma10", "volume_contracting", "kd_not_dead_cross",
            "institutional_not_selling", "financing_not_overheated",
            "bear_regime_core_only",
        ]
    if bpt == ABCBuyPointType.B_PLATFORM_BREAKOUT:
        return [
            "tier_allowed_for_b", "consolidation_valid",
            "close_above_prior_platform_high", "volume_confirmed",
            "financing_not_overheated", "regime_not_bear",
        ]
    if bpt == ABCBuyPointType.C_20MA_RECLAIM:
        return [
            "tier_second_wave_or_main", "had_first_wave",
            "pullback_completed", "close_above_ma20",
            "volume_dry_up_before_reclaim", "kd_improving",
            "institutional_reaccumulation", "financing_not_overheated",
            "regime_not_risk_off",
        ]
    return []
