"""tests/test_theme_strength_v171.py — theme strength model tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import ThemeStrength
from paper_trading.small_capital_strategy.theme_strength_model_v171 import (
    assess_theme_strength, score_theme_for_strength, apply_theme_strength_filter,
    get_theme_strength_scores,
)


def test_assess_leading():
    result = assess_theme_strength("AI", 6, 0.80, 85.0)
    assert result == ThemeStrength.LEADING


def test_assess_strong():
    result = assess_theme_strength("AI", 3, 0.55, 65.0)
    assert result == ThemeStrength.STRONG


def test_assess_moderate():
    result = assess_theme_strength("EV", 2, 0.35, 45.0)
    assert result == ThemeStrength.MODERATE


def test_assess_weak_no_leaders():
    result = assess_theme_strength("BIO", 0, 0.30, 40.0)
    assert result == ThemeStrength.WEAK


def test_assess_weak_low_breadth():
    result = assess_theme_strength("BIO", 1, 0.10, 40.0)
    assert result == ThemeStrength.WEAK


def test_assess_weak_low_momentum():
    result = assess_theme_strength("BIO", 1, 0.35, 10.0)
    assert result == ThemeStrength.WEAK


def test_score_leading():
    assert score_theme_for_strength(ThemeStrength.LEADING) == 100.0


def test_score_strong():
    assert score_theme_for_strength(ThemeStrength.STRONG) == 85.0


def test_score_moderate():
    assert score_theme_for_strength(ThemeStrength.MODERATE) == 60.0


def test_score_weak():
    assert score_theme_for_strength(ThemeStrength.WEAK) == 0.0


def test_score_unknown():
    assert score_theme_for_strength(ThemeStrength.UNKNOWN) == 35.0


def test_filter_leading_passes():
    result = apply_theme_strength_filter("X", "AI", ThemeStrength.LEADING)
    assert result.passed is True


def test_filter_strong_passes():
    result = apply_theme_strength_filter("X", "AI", ThemeStrength.STRONG)
    assert result.passed is True


def test_filter_moderate_passes():
    result = apply_theme_strength_filter("X", "EV", ThemeStrength.MODERATE)
    assert result.passed is True


def test_filter_unknown_passes():
    result = apply_theme_strength_filter("X", "EV", ThemeStrength.UNKNOWN)
    assert result.passed is True


def test_filter_weak_fails():
    result = apply_theme_strength_filter("X", "BIO", ThemeStrength.WEAK)
    assert result.passed is False


def test_filter_reason_on_fail():
    result = apply_theme_strength_filter("X", "BIO", ThemeStrength.WEAK)
    assert "weak" in result.reason.lower()


def test_filter_reason_empty_on_pass():
    result = apply_theme_strength_filter("X", "AI", ThemeStrength.STRONG)
    assert result.reason == ""


def test_filter_paper_only():
    result = apply_theme_strength_filter("X", "AI", ThemeStrength.STRONG)
    assert result.paper_only is True


def test_filter_not_investment_advice():
    result = apply_theme_strength_filter("X", "AI", ThemeStrength.STRONG)
    assert result.not_investment_advice is True


def test_get_strength_scores_dict():
    scores = get_theme_strength_scores()
    assert isinstance(scores, dict)


def test_get_strength_scores_leading_is_highest():
    scores = get_theme_strength_scores()
    assert scores[ThemeStrength.LEADING.value] >= scores[ThemeStrength.STRONG.value]


def test_get_strength_scores_weak_is_zero():
    scores = get_theme_strength_scores()
    assert scores[ThemeStrength.WEAK.value] == 0.0
