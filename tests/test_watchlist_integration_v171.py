"""tests/test_watchlist_integration_v171.py — integration tests for v1.7.1 watchlist pipeline."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, ThemeStrength, ThemeCategory,
)
from paper_trading.small_capital_strategy.watchlist_candidate_v171 import make_sample_candidate
from paper_trading.small_capital_strategy.candidate_pool_builder_v171 import (
    build_candidate_pool, score_and_classify_candidates,
)
from paper_trading.small_capital_strategy.overdiversification_detector_v171 import (
    detect_overdiversification,
)
from paper_trading.small_capital_strategy.top_candidate_selector_v171 import (
    recommend_top_candidates,
)
from paper_trading.small_capital_strategy.watchlist_ranking_v171 import rank_candidates
from paper_trading.small_capital_strategy.small_capital_watchlist_bridge_v171 import (
    map_tier_to_allocation_bucket, get_v170_bridge_summary,
)


def _make_full_pool(n=20):
    return [make_sample_candidate(str(i)) for i in range(n)]


def test_pool_build_and_count():
    candidates = _make_full_pool(20)
    pool = build_candidate_pool(candidates)
    assert pool.total_count == 20


def test_overdiversification_on_optimal_pool():
    candidates = _make_full_pool(20)
    pool = build_candidate_pool(candidates)
    result = detect_overdiversification(pool.candidates)
    from paper_trading.small_capital_strategy.watchlist_enums_v171 import OverdiversificationStatus
    assert result.status == OverdiversificationStatus.OPTIMAL


def test_rank_pipeline_returns_ranked_candidates():
    candidates = _make_full_pool(5)
    ranked = rank_candidates(candidates)
    assert len(ranked) == 5


def test_top_selection_pipeline():
    candidates = _make_full_pool(20)
    selection = recommend_top_candidates(candidates, regime="BULL")
    assert selection.paper_only is True


def test_top_selection_focus_le_10():
    candidates = _make_full_pool(20)
    selection = recommend_top_candidates(candidates, regime="BULL")
    assert len(selection.focus_candidates) <= 10


def test_score_and_classify_then_rank():
    raw_inputs = [
        {
            "symbol": str(i), "theme_strength": "STRONG",
            "above_20ma": True, "above_60ma": True,
            "liquidity_avg_vol": 15_000_000, "revenue_growth_pct": 0.12,
            "inst_net_buy_days": 8, "financing_ratio": 0.12,
            "atr_pct": 0.05, "theme_concentration_count": 0,
            "is_core_eligible": True,
        }
        for i in range(5)
    ]
    candidates = score_and_classify_candidates(raw_inputs)
    ranked = rank_candidates(candidates)
    assert len(ranked) == 5
    assert all(r.candidate.paper_only is True for r in ranked)


def test_bridge_integration_core_maps_correctly():
    bucket = map_tier_to_allocation_bucket(WatchlistTier.CORE)
    assert bucket == "CORE"


def test_bridge_integration_excluded_is_none():
    bucket = map_tier_to_allocation_bucket(WatchlistTier.EXCLUDED)
    assert bucket is None


def test_full_pipeline_safety_chain():
    # End-to-end: build pool → rank → select → bridge summary
    candidates = _make_full_pool(15)
    pool = build_candidate_pool(candidates)
    ranked = rank_candidates(pool.candidates)
    selection = recommend_top_candidates(pool.candidates, regime="UNKNOWN")
    summary = get_v170_bridge_summary()

    assert pool.paper_only is True
    assert all(r.candidate.paper_only is True for r in ranked)
    assert selection.paper_only is True
    assert summary["paper_only"] is True
    assert summary["not_investment_advice"] is True


def test_score_classify_overheated_excluded():
    raw = [{
        "symbol": "X",
        "theme_strength": "STRONG",
        "above_20ma": True, "above_60ma": True,
        "liquidity_avg_vol": 15_000_000,
        "revenue_growth_pct": 0.10,
        "inst_net_buy_days": 8,
        "financing_ratio": 0.45,  # > 30% overheated
        "atr_pct": 0.05,
        "theme_concentration_count": 0,
        "is_core_eligible": False,
    }]
    result = score_and_classify_candidates(raw)
    assert result[0].watchlist_tier == WatchlistTier.EXCLUDED


def test_score_classify_weak_theme_excluded():
    raw = [{
        "symbol": "Y",
        "theme_strength": "WEAK",
        "above_20ma": True, "above_60ma": True,
        "liquidity_avg_vol": 15_000_000,
        "revenue_growth_pct": 0.10,
        "inst_net_buy_days": 8,
        "financing_ratio": 0.10,
        "atr_pct": 0.05,
        "theme_concentration_count": 0,
        "is_core_eligible": False,
    }]
    result = score_and_classify_candidates(raw)
    assert result[0].watchlist_tier == WatchlistTier.EXCLUDED
