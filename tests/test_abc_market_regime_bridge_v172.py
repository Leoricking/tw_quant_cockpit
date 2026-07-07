"""tests/test_abc_market_regime_bridge_v172.py — Market regime bridge tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_market_regime_bridge_v172 import (
    check_market_regime_compatibility, get_compatible_regimes,
)
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCMarketCompatibility, ABCExecutionBlockReason,
)


def test_bull_a_main_theme_compatible():
    result = check_market_regime_compatibility("BULL", ABCBuyPointType.A_10MA_PULLBACK, "MAIN_THEME")
    assert result.compatibility == ABCMarketCompatibility.COMPATIBLE


def test_bull_b_compatible():
    result = check_market_regime_compatibility("BULL", ABCBuyPointType.B_PLATFORM_BREAKOUT, "MAIN_THEME")
    assert result.compatibility == ABCMarketCompatibility.COMPATIBLE


def test_bull_c_compatible():
    result = check_market_regime_compatibility("BULL", ABCBuyPointType.C_20MA_RECLAIM, "SECOND_WAVE")
    assert result.compatibility == ABCMarketCompatibility.COMPATIBLE


def test_bear_a_core_compatible():
    result = check_market_regime_compatibility("BEAR", ABCBuyPointType.A_10MA_PULLBACK, "CORE")
    assert result.compatibility == ABCMarketCompatibility.COMPATIBLE_CORE


def test_bear_a_non_core_blocked():
    result = check_market_regime_compatibility("BEAR", ABCBuyPointType.A_10MA_PULLBACK, "MAIN_THEME")
    assert result.compatibility == ABCMarketCompatibility.BLOCKED
    assert ABCExecutionBlockReason.BEAR_REGIME_NON_CORE in result.block_reasons


def test_bear_b_blocked():
    result = check_market_regime_compatibility("BEAR", ABCBuyPointType.B_PLATFORM_BREAKOUT, "MAIN_THEME")
    assert result.compatibility == ABCMarketCompatibility.BLOCKED
    assert ABCExecutionBlockReason.MARKET_REGIME_BLOCKED in result.block_reasons


def test_bear_c_blocked():
    result = check_market_regime_compatibility("BEAR", ABCBuyPointType.C_20MA_RECLAIM, "SECOND_WAVE")
    assert result.compatibility == ABCMarketCompatibility.BLOCKED


def test_risk_off_b_blocked():
    result = check_market_regime_compatibility("RISK_OFF", ABCBuyPointType.B_PLATFORM_BREAKOUT, "MAIN_THEME")
    assert result.compatibility == ABCMarketCompatibility.BLOCKED
    assert ABCExecutionBlockReason.RISK_OFF_REGIME in result.block_reasons


def test_risk_off_c_blocked():
    result = check_market_regime_compatibility("RISK_OFF", ABCBuyPointType.C_20MA_RECLAIM, "SECOND_WAVE")
    assert result.compatibility == ABCMarketCompatibility.BLOCKED


def test_risk_off_a_compatible():
    result = check_market_regime_compatibility("RISK_OFF", ABCBuyPointType.A_10MA_PULLBACK, "CORE")
    assert result.compatibility != ABCMarketCompatibility.BLOCKED


def test_unknown_non_core_degraded():
    result = check_market_regime_compatibility("UNKNOWN", ABCBuyPointType.A_10MA_PULLBACK, "MAIN_THEME")
    assert result.compatibility == ABCMarketCompatibility.DEGRADED


def test_get_compatible_regimes_a():
    regimes = get_compatible_regimes(ABCBuyPointType.A_10MA_PULLBACK)
    assert "BULL" in regimes
    assert "BEAR" in regimes


def test_get_compatible_regimes_b():
    regimes = get_compatible_regimes(ABCBuyPointType.B_PLATFORM_BREAKOUT)
    assert "BULL" in regimes
    assert "BEAR" not in regimes


def test_get_compatible_regimes_unsupported_empty():
    regimes = get_compatible_regimes(ABCBuyPointType.UNSUPPORTED)
    assert regimes == []


def test_regime_result_paper_only():
    result = check_market_regime_compatibility("BULL", ABCBuyPointType.A_10MA_PULLBACK, "MAIN_THEME")
    assert result.paper_only is True


def test_neutral_a_compatible():
    result = check_market_regime_compatibility("NEUTRAL", ABCBuyPointType.A_10MA_PULLBACK, "MAIN_THEME")
    assert result.compatibility == ABCMarketCompatibility.COMPATIBLE


def test_neutral_b_compatible():
    result = check_market_regime_compatibility("NEUTRAL", ABCBuyPointType.B_PLATFORM_BREAKOUT, "MAIN_THEME")
    assert result.compatibility == ABCMarketCompatibility.COMPATIBLE


def test_unknown_core_compatible():
    result = check_market_regime_compatibility("UNKNOWN", ABCBuyPointType.A_10MA_PULLBACK, "CORE")
    assert result.compatibility != ABCMarketCompatibility.BLOCKED


def test_risk_off_a_core_not_blocked():
    result = check_market_regime_compatibility("RISK_OFF", ABCBuyPointType.A_10MA_PULLBACK, "CORE")
    assert result.compatibility != ABCMarketCompatibility.BLOCKED


def test_get_compatible_regimes_c():
    regimes = get_compatible_regimes(ABCBuyPointType.C_20MA_RECLAIM)
    assert "BULL" in regimes
    assert "BEAR" not in regimes


def test_bear_a_core_no_block_reasons():
    result = check_market_regime_compatibility("BEAR", ABCBuyPointType.A_10MA_PULLBACK, "CORE")
    assert result.block_reasons == []


def test_regime_result_no_real_orders():
    result = check_market_regime_compatibility("BULL", ABCBuyPointType.A_10MA_PULLBACK, "MAIN_THEME")
    assert result.no_real_orders is True


def test_bear_b_blocked_reason_market_regime():
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCExecutionBlockReason
    result = check_market_regime_compatibility("BEAR", ABCBuyPointType.B_PLATFORM_BREAKOUT, "MAIN_THEME")
    assert ABCExecutionBlockReason.MARKET_REGIME_BLOCKED in result.block_reasons


def test_unknown_a_main_theme_has_warning():
    result = check_market_regime_compatibility("UNKNOWN", ABCBuyPointType.A_10MA_PULLBACK, "MAIN_THEME")
    assert len(result.warnings) > 0
