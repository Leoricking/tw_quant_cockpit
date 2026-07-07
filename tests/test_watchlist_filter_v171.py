"""tests/test_watchlist_filter_v171.py — filter tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, WatchlistDecision, WatchlistExclusionReason,
)
from paper_trading.small_capital_strategy.watchlist_candidate_v171 import make_sample_candidate
from paper_trading.small_capital_strategy.watchlist_filter_v171 import (
    filter_for_small_capital, exclude_untradable, apply_regime_filter,
)


def test_clean_candidate_passes():
    c = make_sample_candidate()
    result = filter_for_small_capital(c)
    assert result.passed is True


def test_clean_candidate_include_decision():
    c = make_sample_candidate()
    result = filter_for_small_capital(c)
    assert result.decision == WatchlistDecision.INCLUDE


def test_excluded_tier_blocked():
    c = make_sample_candidate("X", WatchlistTier.EXCLUDED)
    result = filter_for_small_capital(c)
    assert result.passed is False


def test_hard_block_weak_theme():
    from paper_trading.small_capital_strategy.watchlist_enums_v171 import ThemeStrength
    c = make_sample_candidate("X", WatchlistTier.MAIN_THEME, theme_strength=ThemeStrength.WEAK)
    c.exclusion_reasons = [WatchlistExclusionReason.WEAK_THEME]
    result = filter_for_small_capital(c)
    assert result.passed is False
    assert result.decision == WatchlistDecision.EXCLUDE


def test_soft_reason_degrade():
    c = make_sample_candidate()
    c.exclusion_reasons = [WatchlistExclusionReason.BELOW_20MA]
    result = filter_for_small_capital(c)
    assert result.passed is True
    assert result.decision == WatchlistDecision.DEGRADE


def test_paper_only():
    c = make_sample_candidate()
    result = filter_for_small_capital(c)
    assert result.paper_only is True


def test_no_real_orders():
    c = make_sample_candidate()
    result = filter_for_small_capital(c)
    assert result.no_real_orders is True


def test_exclude_untradable_returns_only_passed():
    c_good = make_sample_candidate("G", WatchlistTier.CORE)
    c_bad = make_sample_candidate("B", WatchlistTier.EXCLUDED)
    result = exclude_untradable([c_good, c_bad])
    assert len(result) == 1
    assert result[0].symbol == "G"


def test_exclude_untradable_empty():
    assert exclude_untradable([]) == []


def test_regime_filter_bull_all_eligible():
    c1 = make_sample_candidate("A", WatchlistTier.CORE)
    c2 = make_sample_candidate("B", WatchlistTier.TRAINING)
    result = apply_regime_filter([c1, c2], "BULL")
    assert len(result) == 2


def test_regime_filter_bear_only_core():
    from paper_trading.small_capital_strategy.watchlist_enums_v171 import ThemeStrength
    c_core = make_sample_candidate("CORE", WatchlistTier.CORE)
    c_train = make_sample_candidate("TRAIN", WatchlistTier.TRAINING)
    result = apply_regime_filter([c_core, c_train], "BEAR")
    assert any(c.symbol == "CORE" for c in result)
    assert not any(c.symbol == "TRAIN" for c in result)


def test_regime_filter_risk_off_only_core():
    c_core = make_sample_candidate("CORE", WatchlistTier.CORE)
    c_second = make_sample_candidate("SW", WatchlistTier.SECOND_WAVE)
    result = apply_regime_filter([c_core, c_second], "RISK_OFF")
    assert all(c.watchlist_tier == WatchlistTier.CORE for c in result)


def test_regime_filter_unknown_conservative():
    c_core = make_sample_candidate("CORE", WatchlistTier.CORE, total_score=80.0)
    c_train = make_sample_candidate("TRAIN", WatchlistTier.TRAINING, total_score=45.0)
    result = apply_regime_filter([c_core, c_train], "UNKNOWN")
    assert any(c.symbol == "CORE" for c in result)
    assert not any(c.symbol == "TRAIN" for c in result)
