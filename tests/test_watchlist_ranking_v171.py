"""tests/test_watchlist_ranking_v171.py — ranking tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, WatchlistSortKey,
)
from paper_trading.small_capital_strategy.watchlist_candidate_v171 import make_sample_candidate
from paper_trading.small_capital_strategy.watchlist_ranking_v171 import (
    rank_candidates, get_ranking_rules,
)


def _core(score=80.0): return make_sample_candidate("CORE", WatchlistTier.CORE, total_score=score)
def _main(score=78.0): return make_sample_candidate("MAIN", WatchlistTier.MAIN_THEME, total_score=score)
def _excl(score=20.0): return make_sample_candidate("EXCL", WatchlistTier.EXCLUDED, total_score=score)
def _train(score=45.0): return make_sample_candidate("TRAIN", WatchlistTier.TRAINING, total_score=score)


def test_rank_candidates_returns_list():
    ranked = rank_candidates([_core(), _main()])
    assert isinstance(ranked, list)


def test_rank_candidates_length_preserved():
    candidates = [_core(), _main(), _excl()]
    ranked = rank_candidates(candidates)
    assert len(ranked) == 3


def test_rank_candidates_one_indexed():
    ranked = rank_candidates([_core()])
    assert ranked[0].rank == 1


def test_core_ranks_above_main_theme():
    ranked = rank_candidates([_main(80.0), _core(80.0)])
    assert ranked[0].candidate.watchlist_tier == WatchlistTier.CORE


def test_excluded_ranks_last():
    ranked = rank_candidates([_excl(), _core(), _main()])
    last = ranked[-1]
    assert last.candidate.watchlist_tier == WatchlistTier.EXCLUDED


def test_rank_descending_by_score():
    c1 = make_sample_candidate("A", WatchlistTier.MAIN_THEME, total_score=90.0)
    c2 = make_sample_candidate("B", WatchlistTier.MAIN_THEME, total_score=70.0)
    ranked = rank_candidates([c2, c1])
    assert ranked[0].candidate.symbol == "A"
    assert ranked[1].candidate.symbol == "B"


def test_rank_reason_contains_tier():
    ranked = rank_candidates([_core()])
    assert "CORE" in ranked[0].rank_reason


def test_ranked_candidate_paper_only():
    ranked = rank_candidates([_core()])
    assert ranked[0].paper_only is True


def test_get_ranking_rules_is_dict():
    assert isinstance(get_ranking_rules(), dict)


def test_get_ranking_rules_paper_only():
    rules = get_ranking_rules()
    assert rules["paper_only"] is True


def test_get_ranking_rules_not_investment_advice():
    rules = get_ranking_rules()
    assert rules["not_investment_advice"] is True


def test_rank_empty_list():
    assert rank_candidates([]) == []


def test_rank_by_technical_score():
    import dataclasses
    c1_base = make_sample_candidate("A", WatchlistTier.MAIN_THEME, total_score=70.0)
    c2_base = make_sample_candidate("B", WatchlistTier.MAIN_THEME, total_score=60.0)
    c1 = dataclasses.replace(c1_base, technical_score=90.0)
    c2 = dataclasses.replace(c2_base, technical_score=50.0)
    ranked = rank_candidates([c2, c1], sort_key=WatchlistSortKey.TECHNICAL_SCORE)
    assert ranked[0].candidate.symbol == "A"


def test_training_ranks_below_main_theme():
    ranked = rank_candidates([_train(), _main()])
    tiers = [r.candidate.watchlist_tier for r in ranked]
    assert tiers.index(WatchlistTier.MAIN_THEME) < tiers.index(WatchlistTier.TRAINING)
