"""tests/test_revenue_growth_filter_v171.py — revenue growth filter tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import RevenueGrowthGrade
from paper_trading.small_capital_strategy.revenue_growth_filter_v171 import (
    apply_revenue_growth_filter, grade_revenue_growth, score_revenue_grade,
    get_revenue_thresholds,
)


def test_grade_strong():
    assert grade_revenue_growth(0.20) == RevenueGrowthGrade.STRONG


def test_grade_moderate():
    assert grade_revenue_growth(0.10) == RevenueGrowthGrade.MODERATE


def test_grade_weak():
    assert grade_revenue_growth(0.02) == RevenueGrowthGrade.WEAK


def test_grade_negative():
    assert grade_revenue_growth(-0.05) == RevenueGrowthGrade.NEGATIVE


def test_score_strong():
    assert score_revenue_grade(RevenueGrowthGrade.STRONG) == 90.0


def test_score_negative():
    assert score_revenue_grade(RevenueGrowthGrade.NEGATIVE) == 15.0


def test_filter_strong_passes():
    result = apply_revenue_growth_filter("X", 0.20)
    assert result.passed is True


def test_filter_negative_fails():
    result = apply_revenue_growth_filter("X", -0.05)
    assert result.passed is False


def test_filter_reason_on_fail():
    result = apply_revenue_growth_filter("X", -0.05)
    assert "negative" in result.reason.lower()


def test_filter_paper_only():
    result = apply_revenue_growth_filter("X", 0.20)
    assert result.paper_only is True


def test_get_thresholds_dict():
    t = get_revenue_thresholds()
    assert isinstance(t, dict)
