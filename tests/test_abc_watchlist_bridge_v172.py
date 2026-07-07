"""tests/test_abc_watchlist_bridge_v172.py — Watchlist bridge tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_watchlist_bridge_v172 import (
    check_watchlist_compatibility, get_tier_allowed_buy_points,
    get_tier_preferred_buy_points,
)
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCWatchlistCompatibility, ABCExecutionBlockReason,
)


def test_core_a_fully_compatible():
    result = check_watchlist_compatibility("2330", "CORE", ABCBuyPointType.A_10MA_PULLBACK)
    assert result.compatibility == ABCWatchlistCompatibility.FULLY_COMPATIBLE


def test_core_b_blocked():
    result = check_watchlist_compatibility("2330", "CORE", ABCBuyPointType.B_PLATFORM_BREAKOUT)
    assert result.compatibility == ABCWatchlistCompatibility.BLOCKED


def test_main_theme_a_compatible():
    result = check_watchlist_compatibility("2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK)
    assert result.compatibility == ABCWatchlistCompatibility.FULLY_COMPATIBLE


def test_main_theme_b_compatible():
    result = check_watchlist_compatibility("2330", "MAIN_THEME", ABCBuyPointType.B_PLATFORM_BREAKOUT)
    assert result.compatibility == ABCWatchlistCompatibility.FULLY_COMPATIBLE


def test_main_theme_c_compatible():
    result = check_watchlist_compatibility("2330", "MAIN_THEME", ABCBuyPointType.C_20MA_RECLAIM)
    assert result.compatibility == ABCWatchlistCompatibility.FULLY_COMPATIBLE


def test_second_wave_c_compatible():
    result = check_watchlist_compatibility("2330", "SECOND_WAVE", ABCBuyPointType.C_20MA_RECLAIM)
    assert result.compatibility == ABCWatchlistCompatibility.FULLY_COMPATIBLE


def test_second_wave_b_blocked():
    result = check_watchlist_compatibility("2330", "SECOND_WAVE", ABCBuyPointType.B_PLATFORM_BREAKOUT)
    assert result.compatibility == ABCWatchlistCompatibility.BLOCKED


def test_training_b_compatible():
    result = check_watchlist_compatibility("2330", "TRAINING", ABCBuyPointType.B_PLATFORM_BREAKOUT)
    assert result.compatibility in (
        ABCWatchlistCompatibility.FULLY_COMPATIBLE,
        ABCWatchlistCompatibility.COMPATIBLE,
    )


def test_training_has_cap():
    result = check_watchlist_compatibility("2330", "TRAINING", ABCBuyPointType.B_PLATFORM_BREAKOUT)
    assert result.training_cap == 15_000.0


def test_excluded_blocked():
    result = check_watchlist_compatibility("2330", "EXCLUDED", ABCBuyPointType.A_10MA_PULLBACK)
    assert result.compatibility == ABCWatchlistCompatibility.BLOCKED
    assert ABCExecutionBlockReason.WATCHLIST_EXCLUDED in result.block_reasons


def test_get_tier_allowed_core():
    allowed = get_tier_allowed_buy_points("CORE")
    assert ABCBuyPointType.A_10MA_PULLBACK in allowed
    assert ABCBuyPointType.B_PLATFORM_BREAKOUT not in allowed


def test_get_tier_allowed_main_theme():
    allowed = get_tier_allowed_buy_points("MAIN_THEME")
    assert len(allowed) == 3


def test_get_tier_preferred_second_wave():
    preferred = get_tier_preferred_buy_points("SECOND_WAVE")
    assert ABCBuyPointType.C_20MA_RECLAIM in preferred


def test_get_tier_allowed_excluded_empty():
    assert get_tier_allowed_buy_points("EXCLUDED") == []


def test_watchlist_result_paper_only():
    result = check_watchlist_compatibility("2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK)
    assert result.paper_only is True


def test_watchlist_result_no_real_orders():
    result = check_watchlist_compatibility("2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK)
    assert result.no_real_orders is True


def test_core_allowed_list_a_only():
    allowed = get_tier_allowed_buy_points("CORE")
    assert len(allowed) == 1
    assert ABCBuyPointType.A_10MA_PULLBACK in allowed


def test_second_wave_allowed_two():
    allowed = get_tier_allowed_buy_points("SECOND_WAVE")
    assert ABCBuyPointType.C_20MA_RECLAIM in allowed
    assert ABCBuyPointType.A_10MA_PULLBACK in allowed


def test_training_allowed_b_only():
    allowed = get_tier_allowed_buy_points("TRAINING")
    assert ABCBuyPointType.B_PLATFORM_BREAKOUT in allowed
    assert ABCBuyPointType.A_10MA_PULLBACK not in allowed


def test_core_c_blocked():
    result = check_watchlist_compatibility("2330", "CORE", ABCBuyPointType.C_20MA_RECLAIM)
    assert result.compatibility == ABCWatchlistCompatibility.BLOCKED


def test_training_a_blocked():
    result = check_watchlist_compatibility("2330", "TRAINING", ABCBuyPointType.A_10MA_PULLBACK)
    assert result.compatibility == ABCWatchlistCompatibility.BLOCKED


def test_training_c_blocked():
    result = check_watchlist_compatibility("2330", "TRAINING", ABCBuyPointType.C_20MA_RECLAIM)
    assert result.compatibility == ABCWatchlistCompatibility.BLOCKED


def test_main_theme_allowed_buy_points_count():
    allowed = get_tier_allowed_buy_points("MAIN_THEME")
    assert ABCBuyPointType.A_10MA_PULLBACK in allowed
    assert ABCBuyPointType.B_PLATFORM_BREAKOUT in allowed
    assert ABCBuyPointType.C_20MA_RECLAIM in allowed


def test_watchlist_not_investment_advice():
    result = check_watchlist_compatibility("2330", "MAIN_THEME", ABCBuyPointType.A_10MA_PULLBACK)
    assert result.not_investment_advice is True
