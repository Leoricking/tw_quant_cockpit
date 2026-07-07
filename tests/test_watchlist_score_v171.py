"""tests/test_watchlist_score_v171.py — scoring engine tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    ThemeStrength, WatchlistExclusionReason, RankingGrade,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import WatchlistScoreInput
from paper_trading.small_capital_strategy.watchlist_score_v171 import (
    compute_watchlist_score, get_score_weights, SCORE_WEIGHTS,
    score_theme_strength, score_technical, score_revenue_growth,
    score_liquidity, score_institutional, score_financing, score_small_capital_fit,
)


def _make_inp(**kwargs):
    defaults = dict(
        symbol="TEST", theme_strength=ThemeStrength.STRONG,
        above_20ma=True, above_60ma=True,
        liquidity_avg_vol=30_000_000, revenue_growth_pct=0.20,
        inst_net_buy_days=12, financing_ratio=0.10,
        atr_pct=0.04, theme_concentration_count=0,
        paper_only=True, research_only=True, no_real_orders=True, not_investment_advice=True,
    )
    defaults.update(kwargs)
    return WatchlistScoreInput(**defaults)


def test_score_weights_sum_100():
    assert sum(SCORE_WEIGHTS.values()) == 100


def test_score_weights_has_7_components():
    assert len(SCORE_WEIGHTS) == 7


def test_get_score_weights_returns_dict():
    assert isinstance(get_score_weights(), dict)


def test_theme_strength_leading_100():
    assert score_theme_strength(ThemeStrength.LEADING) == 100.0


def test_theme_strength_strong_85():
    assert score_theme_strength(ThemeStrength.STRONG) == 85.0


def test_theme_strength_weak_0():
    assert score_theme_strength(ThemeStrength.WEAK) == 0.0


def test_technical_both_above_90():
    assert score_technical(True, True) == 90.0


def test_technical_below_20ma_55():
    assert score_technical(True, False) == 55.0


def test_technical_both_below_20():
    assert score_technical(False, False) == 20.0


def test_revenue_strong():
    assert score_revenue_growth(0.30) == 100.0


def test_revenue_negative():
    assert score_revenue_growth(-0.10) == 15.0


def test_liquidity_high():
    assert score_liquidity(50_000_000) == 100.0


def test_liquidity_blocked():
    assert score_liquidity(500_000) == 0.0


def test_institutional_accumulating():
    assert score_institutional(12) == 95.0


def test_institutional_heavy_sell():
    assert score_institutional(-1) == 0.0


def test_financing_healthy():
    assert score_financing(0.05) == 95.0


def test_financing_overheated():
    assert score_financing(0.45) == 0.0


def test_small_capital_fit_low_atr():
    assert score_small_capital_fit(0.02) == 95.0


def test_strong_theme_high_score():
    inp = _make_inp()
    result = compute_watchlist_score(inp)
    assert result.total_score >= 70.0
    assert result.grade in (RankingGrade.A, RankingGrade.B)


def test_weak_theme_blocked():
    inp = _make_inp(theme_strength=ThemeStrength.WEAK)
    result = compute_watchlist_score(inp)
    assert result.blocked is True
    assert result.total_score == 0.0
    assert WatchlistExclusionReason.WEAK_THEME in result.exclusion_reasons


def test_low_liquidity_blocked():
    inp = _make_inp(liquidity_avg_vol=500_000)
    result = compute_watchlist_score(inp)
    assert result.blocked is True
    assert WatchlistExclusionReason.LOW_LIQUIDITY in result.exclusion_reasons


def test_financing_overheated_blocked():
    inp = _make_inp(financing_ratio=0.45)
    result = compute_watchlist_score(inp)
    assert result.blocked is True
    assert WatchlistExclusionReason.FINANCING_OVERHEATED in result.exclusion_reasons


def test_institutional_heavy_sell_blocked():
    inp = _make_inp(inst_net_buy_days=-3)
    result = compute_watchlist_score(inp)
    assert result.blocked is True
    assert WatchlistExclusionReason.INSTITUTIONAL_HEAVY_SELLING in result.exclusion_reasons


def test_below_20ma_exclusion_reason():
    inp = _make_inp(above_20ma=False, above_60ma=True)
    result = compute_watchlist_score(inp)
    assert WatchlistExclusionReason.BELOW_20MA in result.exclusion_reasons
    assert result.blocked is False


def test_below_60ma_exclusion_reason():
    inp = _make_inp(above_20ma=True, above_60ma=False)
    result = compute_watchlist_score(inp)
    assert WatchlistExclusionReason.BELOW_60MA in result.exclusion_reasons


def test_high_volatility_exclusion():
    inp = _make_inp(atr_pct=0.15)
    result = compute_watchlist_score(inp)
    assert WatchlistExclusionReason.TOO_VOLATILE_FOR_SMALL_CAPITAL in result.exclusion_reasons


def test_duplicate_theme_overexposure():
    inp = _make_inp(theme_concentration_count=4)
    result = compute_watchlist_score(inp)
    assert WatchlistExclusionReason.DUPLICATE_THEME_OVEREXPOSURE in result.exclusion_reasons


def test_no_a_plus_grade():
    inp = _make_inp()
    result = compute_watchlist_score(inp)
    assert result.grade.value != "A+"


def test_result_paper_only():
    result = compute_watchlist_score(_make_inp())
    assert result.paper_only is True


def test_result_not_investment_advice():
    result = compute_watchlist_score(_make_inp())
    assert result.not_investment_advice is True


def test_result_schema_version():
    result = compute_watchlist_score(_make_inp())
    assert result.schema_version == "171"


def test_total_score_bounded():
    inp = _make_inp()
    result = compute_watchlist_score(inp)
    assert 0.0 <= result.total_score <= 100.0
