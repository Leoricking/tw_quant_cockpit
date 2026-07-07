"""tests/test_liquidity_filter_v171.py — liquidity filter tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import LiquidityGrade
from paper_trading.small_capital_strategy.liquidity_filter_v171 import (
    apply_liquidity_filter, grade_liquidity, score_liquidity_grade,
    get_liquidity_thresholds,
    LIQUIDITY_HIGH_THRESHOLD, LIQUIDITY_MEDIUM_THRESHOLD, LIQUIDITY_LOW_THRESHOLD,
)


def test_high_threshold_constant():
    assert LIQUIDITY_HIGH_THRESHOLD == 20_000_000


def test_low_threshold_constant():
    assert LIQUIDITY_LOW_THRESHOLD == 1_000_000


def test_grade_high():
    assert grade_liquidity(50_000_000) == LiquidityGrade.HIGH


def test_grade_medium():
    assert grade_liquidity(10_000_000) == LiquidityGrade.MEDIUM


def test_grade_low():
    assert grade_liquidity(2_000_000) == LiquidityGrade.LOW


def test_grade_blocked():
    assert grade_liquidity(500_000) == LiquidityGrade.BLOCKED


def test_score_high():
    assert score_liquidity_grade(LiquidityGrade.HIGH) == 90.0


def test_score_blocked():
    assert score_liquidity_grade(LiquidityGrade.BLOCKED) == 0.0


def test_filter_high_passes():
    result = apply_liquidity_filter("X", 30_000_000)
    assert result.passed is True


def test_filter_blocked_fails():
    result = apply_liquidity_filter("X", 500_000)
    assert result.passed is False


def test_filter_reason_empty_on_pass():
    result = apply_liquidity_filter("X", 30_000_000)
    assert result.reason == ""


def test_filter_reason_on_fail():
    result = apply_liquidity_filter("X", 500_000)
    assert "liquidity too low" in result.reason


def test_filter_paper_only():
    result = apply_liquidity_filter("X", 30_000_000)
    assert result.paper_only is True


def test_filter_not_investment_advice():
    result = apply_liquidity_filter("X", 30_000_000)
    assert result.not_investment_advice is True


def test_get_thresholds_dict():
    t = get_liquidity_thresholds()
    assert isinstance(t, dict)
    assert t["high"] == LIQUIDITY_HIGH_THRESHOLD
