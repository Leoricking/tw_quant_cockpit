"""tests/test_small_capital_theme_filter_v170.py — theme filter tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.enums_v170 import ThemeStrength
from paper_trading.small_capital_strategy.theme_filter_v170 import (
    filter_by_theme, batch_filter, MINIMUM_THEME_STRENGTH,
)


def test_minimum_theme_strength_moderate():
    assert MINIMUM_THEME_STRENGTH == ThemeStrength.MODERATE


def test_filter_strong_passes():
    result = filter_by_theme("2330", "AI", ThemeStrength.STRONG)
    assert result.passed is True


def test_filter_moderate_passes():
    result = filter_by_theme("2330", "AI", ThemeStrength.MODERATE)
    assert result.passed is True


def test_filter_weak_fails():
    result = filter_by_theme("2330", "AI", ThemeStrength.WEAK)
    assert result.passed is False


def test_filter_none_fails():
    result = filter_by_theme("2330", "AI", ThemeStrength.NONE)
    assert result.passed is False


def test_filter_result_has_symbol():
    result = filter_by_theme("2330", "AI", ThemeStrength.STRONG)
    assert result.symbol == "2330"


def test_filter_result_has_theme():
    result = filter_by_theme("2330", "AI", ThemeStrength.STRONG)
    assert result.theme == "AI"


def test_filter_result_has_theme_strength():
    result = filter_by_theme("2330", "AI", ThemeStrength.STRONG)
    assert result.theme_strength == ThemeStrength.STRONG.value


def test_filter_result_paper_only():
    result = filter_by_theme("2330", "AI", ThemeStrength.STRONG)
    assert result.paper_only is True


def test_batch_filter_returns_list():
    candidates = [
        {"symbol": "2330", "theme": "AI", "theme_strength": ThemeStrength.STRONG},
        {"symbol": "2454", "theme": "EV", "theme_strength": ThemeStrength.WEAK},
    ]
    results = batch_filter(candidates)
    assert isinstance(results, list)
    assert len(results) == 2


def test_batch_filter_strong_passes():
    candidates = [{"symbol": "2330", "theme": "AI", "theme_strength": ThemeStrength.STRONG}]
    results = batch_filter(candidates)
    assert results[0].passed is True


def test_batch_filter_weak_fails():
    candidates = [{"symbol": "2454", "theme": "EV", "theme_strength": ThemeStrength.WEAK}]
    results = batch_filter(candidates)
    assert results[0].passed is False
