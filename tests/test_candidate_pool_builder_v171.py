"""tests/test_candidate_pool_builder_v171.py — candidate pool builder tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import CandidatePoolType
from paper_trading.small_capital_strategy.watchlist_candidate_v171 import make_sample_candidate
from paper_trading.small_capital_strategy.candidate_pool_builder_v171 import (
    build_candidate_pool, score_and_classify_candidates, get_pool_profile_id,
    PROFILE_ID,
)


def _raw_input(symbol="1234"):
    return {
        "symbol": symbol,
        "name": f"Stock-{symbol}",
        "market": "TWSE",
        "sector": "Tech",
        "industry": "Semi",
        "theme": "AI",
        "theme_category": "AI_SEMICONDUCTOR",
        "theme_strength": "STRONG",
        "above_20ma": True,
        "above_60ma": True,
        "liquidity_avg_vol": 20_000_000,
        "revenue_growth_pct": 0.15,
        "inst_net_buy_days": 10,
        "financing_ratio": 0.10,
        "atr_pct": 0.05,
        "theme_concentration_count": 0,
        "is_core_eligible": True,
    }


def test_profile_id_constant():
    assert PROFILE_ID == "small_capital_watchlist_v171"


def test_get_pool_profile_id():
    assert get_pool_profile_id() == PROFILE_ID


def test_build_pool_total_count():
    candidates = [make_sample_candidate(str(i)) for i in range(5)]
    pool = build_candidate_pool(candidates)
    assert pool.total_count == 5


def test_build_pool_paper_only():
    pool = build_candidate_pool([make_sample_candidate("X")])
    assert pool.paper_only is True


def test_build_pool_not_investment_advice():
    pool = build_candidate_pool([make_sample_candidate("X")])
    assert pool.not_investment_advice is True


def test_build_pool_default_type():
    pool = build_candidate_pool([make_sample_candidate("X")])
    assert pool.pool_type == CandidatePoolType.FULL_WATCHLIST


def test_build_pool_custom_type():
    pool = build_candidate_pool(
        [make_sample_candidate("X")],
        pool_type=CandidatePoolType.FOCUS_CANDIDATES,
    )
    assert pool.pool_type == CandidatePoolType.FOCUS_CANDIDATES


def test_build_pool_profile_id():
    pool = build_candidate_pool([make_sample_candidate("X")])
    assert pool.profile_id == PROFILE_ID


def test_build_pool_empty():
    pool = build_candidate_pool([])
    assert pool.total_count == 0


def test_score_and_classify_returns_list():
    result = score_and_classify_candidates([_raw_input()])
    assert isinstance(result, list)
    assert len(result) == 1


def test_score_and_classify_paper_only():
    result = score_and_classify_candidates([_raw_input()])
    assert result[0].paper_only is True


def test_score_and_classify_symbol():
    result = score_and_classify_candidates([_raw_input("5566")])
    assert result[0].symbol == "5566"


def test_score_and_classify_has_total_score():
    result = score_and_classify_candidates([_raw_input()])
    assert 0.0 <= result[0].total_score <= 100.0


def test_score_and_classify_has_tier():
    result = score_and_classify_candidates([_raw_input()])
    from paper_trading.small_capital_strategy.watchlist_enums_v171 import WatchlistTier
    assert isinstance(result[0].watchlist_tier, WatchlistTier)


def test_score_and_classify_multiple():
    raws = [_raw_input(str(i)) for i in range(3)]
    result = score_and_classify_candidates(raws)
    assert len(result) == 3


def test_score_and_classify_unknown_theme():
    raw = _raw_input()
    raw["theme_strength"] = "INVALID_THEME"
    result = score_and_classify_candidates([raw])
    from paper_trading.small_capital_strategy.watchlist_enums_v171 import ThemeStrength
    assert result[0].theme_strength == ThemeStrength.UNKNOWN


def test_score_and_classify_empty():
    result = score_and_classify_candidates([])
    assert result == []
