"""tests/test_watchlist_tier_classifier_v171.py — tier classifier tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, ThemeStrength, WatchlistExclusionReason, SmallCapitalTradability,
)
from paper_trading.small_capital_strategy.watchlist_tier_classifier_v171 import (
    classify_watchlist_tier, classify_candidate_tier, get_tier_thresholds,
)
from paper_trading.small_capital_strategy.watchlist_candidate_v171 import make_sample_candidate


def test_core_classification():
    result = classify_watchlist_tier(
        total_score=88.0, theme_strength=ThemeStrength.STRONG,
        liquidity_score=85.0, exclusion_reasons=[], is_core_eligible=True,
    )
    assert result.tier == WatchlistTier.CORE


def test_main_theme_classification():
    result = classify_watchlist_tier(
        total_score=75.0, theme_strength=ThemeStrength.STRONG,
        liquidity_score=60.0, exclusion_reasons=[], is_core_eligible=False,
    )
    assert result.tier == WatchlistTier.MAIN_THEME


def test_second_wave_classification():
    result = classify_watchlist_tier(
        total_score=55.0, theme_strength=ThemeStrength.MODERATE,
        liquidity_score=50.0, exclusion_reasons=[], is_core_eligible=False,
    )
    assert result.tier == WatchlistTier.SECOND_WAVE


def test_training_classification():
    result = classify_watchlist_tier(
        total_score=42.0, theme_strength=ThemeStrength.MODERATE,
        liquidity_score=40.0, exclusion_reasons=[], is_core_eligible=False,
    )
    assert result.tier == WatchlistTier.TRAINING


def test_excluded_weak_theme():
    result = classify_watchlist_tier(
        total_score=80.0, theme_strength=ThemeStrength.WEAK,
        liquidity_score=80.0,
        exclusion_reasons=[WatchlistExclusionReason.WEAK_THEME],
        is_core_eligible=True,
    )
    assert result.tier == WatchlistTier.EXCLUDED


def test_excluded_low_liquidity():
    result = classify_watchlist_tier(
        total_score=80.0, theme_strength=ThemeStrength.STRONG,
        liquidity_score=80.0,
        exclusion_reasons=[WatchlistExclusionReason.LOW_LIQUIDITY],
        is_core_eligible=False,
    )
    assert result.tier == WatchlistTier.EXCLUDED


def test_excluded_financing_overheated():
    result = classify_watchlist_tier(
        total_score=80.0, theme_strength=ThemeStrength.STRONG,
        liquidity_score=80.0,
        exclusion_reasons=[WatchlistExclusionReason.FINANCING_OVERHEATED],
        is_core_eligible=False,
    )
    assert result.tier == WatchlistTier.EXCLUDED


def test_excluded_score_too_low():
    result = classify_watchlist_tier(
        total_score=20.0, theme_strength=ThemeStrength.MODERATE,
        liquidity_score=30.0, exclusion_reasons=[], is_core_eligible=False,
    )
    assert result.tier == WatchlistTier.EXCLUDED


def test_core_tradable():
    result = classify_watchlist_tier(
        total_score=88.0, theme_strength=ThemeStrength.STRONG,
        liquidity_score=85.0, exclusion_reasons=[], is_core_eligible=True,
    )
    assert result.small_capital_tradability == SmallCapitalTradability.TRADABLE


def test_excluded_not_tradable():
    result = classify_watchlist_tier(
        total_score=80.0, theme_strength=ThemeStrength.STRONG,
        liquidity_score=80.0,
        exclusion_reasons=[WatchlistExclusionReason.WEAK_THEME],
        is_core_eligible=False,
    )
    assert result.small_capital_tradability == SmallCapitalTradability.EXCLUDED


def test_classify_candidate_tier():
    c = make_sample_candidate("X", WatchlistTier.CORE, total_score=88.0)
    result = classify_candidate_tier(c)
    assert result.symbol == "X"


def test_get_tier_thresholds_dict():
    thresholds = get_tier_thresholds()
    assert isinstance(thresholds, dict)
    assert "core_min_total" in thresholds
    assert "training_min_total" in thresholds


def test_tier_thresholds_values():
    t = get_tier_thresholds()
    assert t["training_min_total"] < t["second_wave_min_total"]
    assert t["second_wave_min_total"] < t["main_theme_min_total"]
