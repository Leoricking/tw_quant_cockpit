"""tests/test_small_capital_abc_buy_points_v170.py — A/B/C buy point tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.buy_point_rules_v170 import (
    check_a_buy_point, check_b_buy_point, check_c_buy_point, evaluate_buy_point,
)
from paper_trading.small_capital_strategy.abc_buy_point_v170 import (
    evaluate_abc_signal, evaluate_all_abc, get_best_buy_point,
)
from paper_trading.small_capital_strategy.enums_v170 import BuyPointType, ThemeStrength


def _a_signal(**kwargs):
    defaults = {
        "theme_strength": ThemeStrength.STRONG,
        "close_gt_ma20": True,
        "close_gt_ma60": True,
        "low_lte_ma10": True,
        "close_gte_ma10": True,
        "volume_contracting": True,
        "kd_not_dead_cross": True,
        "institutional_not_net_selling": True,
        "financing_not_overheated": True,
    }
    defaults.update(kwargs)
    return defaults


def _b_signal(**kwargs):
    defaults = {
        "consolidation_weeks": 3,
        "close_gt_platform_high": True,
        "volume_ratio": 2.0,
        "not_third_ext_red_candle": True,
        "financing_not_overheated": True,
        "regime_not_bear": True,
    }
    defaults.update(kwargs)
    return defaults


def _c_signal(**kwargs):
    defaults = {
        "had_first_wave": True,
        "pullback_completed": True,
        "close_reclaims_ma20": True,
        "volume_dry_up_before_reclaim": True,
        "kd_golden_cross_or_improving": True,
        "institutional_reaccumulation": True,
    }
    defaults.update(kwargs)
    return defaults


def test_check_a_valid():
    result = check_a_buy_point(_a_signal())
    assert result["passed"] is True


def test_check_a_has_buy_point_type():
    result = check_a_buy_point(_a_signal())
    assert result["buy_point_type"] == BuyPointType.A_10MA_PULLBACK.value


def test_check_a_theme_not_strong_fails():
    result = check_a_buy_point(_a_signal(theme_strength=ThemeStrength.WEAK))
    assert result["passed"] is False


def test_check_a_not_above_ma20_fails():
    result = check_a_buy_point(_a_signal(close_gt_ma20=False))
    assert result["passed"] is False


def test_check_b_valid():
    result = check_b_buy_point(_b_signal())
    assert result["passed"] is True


def test_check_b_has_buy_point_type():
    result = check_b_buy_point(_b_signal())
    assert result["buy_point_type"] == BuyPointType.B_PLATFORM_BREAKOUT.value


def test_check_b_volume_insufficient_fails():
    result = check_b_buy_point(_b_signal(volume_ratio=1.0))
    assert result["passed"] is False


def test_check_b_consolidation_too_short_fails():
    result = check_b_buy_point(_b_signal(consolidation_weeks=1))
    assert result["passed"] is False


def test_check_b_consolidation_too_long_fails():
    result = check_b_buy_point(_b_signal(consolidation_weeks=8))
    assert result["passed"] is False


def test_check_c_valid():
    result = check_c_buy_point(_c_signal())
    assert result["passed"] is True


def test_check_c_has_buy_point_type():
    result = check_c_buy_point(_c_signal())
    assert result["buy_point_type"] == BuyPointType.C_20MA_RECLAIM.value


def test_check_c_no_first_wave_fails():
    result = check_c_buy_point(_c_signal(had_first_wave=False))
    assert result["passed"] is False


def test_check_c_no_reclaim_ma20_fails():
    result = check_c_buy_point(_c_signal(close_reclaims_ma20=False))
    assert result["passed"] is False


def test_check_c_no_volume_dry_up_fails():
    result = check_c_buy_point(_c_signal(volume_dry_up_before_reclaim=False))
    assert result["passed"] is False


def test_evaluate_buy_point_a():
    result = evaluate_buy_point(BuyPointType.A_10MA_PULLBACK, _a_signal())
    assert result["buy_point_type"] == BuyPointType.A_10MA_PULLBACK.value


def test_evaluate_buy_point_b():
    result = evaluate_buy_point(BuyPointType.B_PLATFORM_BREAKOUT, _b_signal())
    assert result["buy_point_type"] == BuyPointType.B_PLATFORM_BREAKOUT.value


def test_evaluate_buy_point_c():
    result = evaluate_buy_point(BuyPointType.C_20MA_RECLAIM, _c_signal())
    assert result["buy_point_type"] == BuyPointType.C_20MA_RECLAIM.value


def test_evaluate_abc_signal_returns_result():
    combined = {**_a_signal(), **_b_signal(), **_c_signal()}
    result = evaluate_abc_signal("2330", BuyPointType.A_10MA_PULLBACK, combined)
    assert result is not None


def test_evaluate_all_abc_returns_list():
    combined = {**_a_signal(), **_b_signal(), **_c_signal()}
    results = evaluate_all_abc("2330", combined)
    assert isinstance(results, list)
    assert len(results) == 3


def test_get_best_buy_point_returns_result():
    combined = {**_a_signal(), **_b_signal(), **_c_signal()}
    results = evaluate_all_abc("2330", combined)
    best = get_best_buy_point(results)
    assert best is not None
