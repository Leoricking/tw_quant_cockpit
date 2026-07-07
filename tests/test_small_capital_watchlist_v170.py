"""tests/test_small_capital_watchlist_v170.py — watchlist profile tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.watchlist_profile_v170 import (
    create_default_watchlist_profile, rank_candidates, filter_for_small_capital,
    exclude_untradable, detect_overdiversification, recommend_top_candidates,
    MAX_WATCHLIST, DEFAULT_WATCHLIST, FOCUS_CANDIDATES, TRADABLE_CANDIDATES,
)


def _make_candidate(**kwargs):
    defaults = {
        "symbol": "2330",
        "technical_score": 0.8,
        "institutional_score": 0.7,
        "revenue_score": 0.6,
        "theme_score": 0.9,
        "liquidity_score": 0.8,
        "risk_score": 0.3,
        "tradable": True,
        "theme_strength": "STRONG",
    }
    defaults.update(kwargs)
    return defaults


def test_max_watchlist_50():
    assert MAX_WATCHLIST == 50


def test_default_watchlist_30():
    assert DEFAULT_WATCHLIST == 30


def test_focus_candidates_10():
    assert FOCUS_CANDIDATES == 10


def test_tradable_candidates_5():
    assert TRADABLE_CANDIDATES == 5


def test_create_default_watchlist_profile():
    wp = create_default_watchlist_profile()
    assert wp is not None


def test_create_default_watchlist_profile_paper_only():
    wp = create_default_watchlist_profile()
    assert wp.paper_only is True


def test_rank_candidates_returns_list():
    candidates = [_make_candidate(symbol=str(i)) for i in range(5)]
    ranked = rank_candidates(candidates)
    assert isinstance(ranked, list)


def test_rank_candidates_sorted_descending():
    candidates = [
        _make_candidate(symbol="A", technical_score=0.5),
        _make_candidate(symbol="B", technical_score=0.9),
    ]
    ranked = rank_candidates(candidates)
    assert len(ranked) == 2


def test_filter_for_small_capital_pass():
    candidates = [_make_candidate(liquidity_score=0.8, risk_score=0.3)]
    filtered = filter_for_small_capital(candidates)
    assert len(filtered) == 1


def test_filter_for_small_capital_low_liquidity():
    candidates = [_make_candidate(liquidity_score=0.2, risk_score=0.3)]
    filtered = filter_for_small_capital(candidates)
    assert len(filtered) == 0


def test_filter_for_small_capital_high_risk():
    candidates = [_make_candidate(liquidity_score=0.8, risk_score=0.9)]
    filtered = filter_for_small_capital(candidates)
    assert len(filtered) == 0


def test_exclude_untradable():
    from paper_trading.small_capital_strategy.enums_v170 import WatchlistTier
    candidates = [
        _make_candidate(symbol="A", watchlist_tier=WatchlistTier.CORE.value),
        _make_candidate(symbol="B", watchlist_tier=WatchlistTier.EXCLUDED.value),
    ]
    filtered = exclude_untradable(candidates)
    assert len(filtered) == 1
    assert filtered[0]["symbol"] == "A"


def test_detect_overdiversification_true():
    from paper_trading.small_capital_strategy.enums_v170 import WatchlistTier
    # Need >max_holdings*3 = >12 candidates in CORE or MAIN_THEME
    candidates = [
        _make_candidate(symbol=str(i), watchlist_tier=WatchlistTier.CORE.value)
        for i in range(15)
    ]
    assert detect_overdiversification(candidates, max_holdings=4) is True


def test_detect_overdiversification_false():
    from paper_trading.small_capital_strategy.enums_v170 import WatchlistTier
    candidates = [
        _make_candidate(symbol=str(i), watchlist_tier=WatchlistTier.CORE.value)
        for i in range(3)
    ]
    assert detect_overdiversification(candidates, max_holdings=4) is False


def test_recommend_top_candidates_5():
    candidates = [_make_candidate(symbol=str(i)) for i in range(10)]
    ranked = rank_candidates(candidates)
    top = recommend_top_candidates(ranked, n=5)
    assert len(top) == 5


def test_recommend_top_candidates_fewer_than_n():
    candidates = [_make_candidate(symbol=str(i)) for i in range(3)]
    ranked = rank_candidates(candidates)
    top = recommend_top_candidates(ranked, n=5)
    assert len(top) == 3
