"""tests/test_top_candidate_selector_v171.py — top candidate selector tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import WatchlistTier
from paper_trading.small_capital_strategy.watchlist_candidate_v171 import make_sample_candidate
from paper_trading.small_capital_strategy.watchlist_ranking_v171 import rank_candidates
from paper_trading.small_capital_strategy.top_candidate_selector_v171 import (
    select_focus_candidates, select_tradable_candidates, select_training_candidates,
    recommend_top_candidates, get_selection_limits,
)
from paper_trading.small_capital_strategy.overdiversification_detector_v171 import (
    FOCUS_CANDIDATES, TRADABLE_CANDIDATES, TRAINING_MAX,
)


def _make_core(symbol, score=85.0):
    c = make_sample_candidate(symbol, WatchlistTier.CORE, total_score=score)
    c = c.__class__(**{**c.__dict__, "tradable": True})
    return c


def _make_training(symbol, score=45.0):
    c = make_sample_candidate(symbol, WatchlistTier.TRAINING, total_score=score)
    c = c.__class__(**{**c.__dict__, "tradable": False})
    return c


def _make_excluded(symbol):
    c = make_sample_candidate(symbol, WatchlistTier.EXCLUDED, total_score=20.0)
    c = c.__class__(**{**c.__dict__, "tradable": False})
    return c


def test_selection_limits_max_focus():
    limits = get_selection_limits()
    assert limits["max_focus"] == FOCUS_CANDIDATES


def test_selection_limits_max_tradable():
    limits = get_selection_limits()
    assert limits["max_tradable"] == TRADABLE_CANDIDATES


def test_selection_limits_paper_only():
    limits = get_selection_limits()
    assert limits["paper_only"] is True


def test_select_focus_excludes_excluded_tier():
    candidates = [_make_core("A"), _make_excluded("B")]
    ranked = rank_candidates(candidates)
    focus = select_focus_candidates(ranked)
    symbols = [r.candidate.symbol for r in focus]
    assert "B" not in symbols


def test_select_focus_max_10():
    candidates = [_make_core(str(i), 80.0 - i) for i in range(15)]
    ranked = rank_candidates(candidates)
    focus = select_focus_candidates(ranked)
    assert len(focus) <= FOCUS_CANDIDATES


def test_select_focus_empty():
    focus = select_focus_candidates([])
    assert focus == []


def test_select_tradable_excludes_excluded():
    candidates = [_make_core("A"), _make_excluded("B")]
    ranked = rank_candidates(candidates)
    tradable = select_tradable_candidates(ranked, regime="BULL")
    symbols = [r.candidate.symbol for r in tradable]
    assert "B" not in symbols


def test_select_tradable_max_5():
    candidates = [_make_core(str(i), 85.0 - i) for i in range(10)]
    ranked = rank_candidates(candidates)
    tradable = select_tradable_candidates(ranked, regime="BULL")
    assert len(tradable) <= TRADABLE_CANDIDATES


def test_select_training_bear_regime_empty():
    candidates = [_make_training("T1"), _make_training("T2")]
    ranked = rank_candidates(candidates)
    result = select_training_candidates(ranked, regime="BEAR")
    assert result == []


def test_select_training_risk_off_empty():
    candidates = [_make_training("T1")]
    ranked = rank_candidates(candidates)
    result = select_training_candidates(ranked, regime="RISK_OFF")
    assert result == []


def test_select_training_bull_returns_training():
    candidates = [_make_training("T1"), _make_training("T2")]
    ranked = rank_candidates(candidates)
    result = select_training_candidates(ranked, regime="BULL")
    assert len(result) > 0


def test_recommend_returns_top_candidate_selection():
    candidates = [_make_core("A"), _make_core("B")]
    result = recommend_top_candidates(candidates)
    from paper_trading.small_capital_strategy.watchlist_models_v171 import TopCandidateSelection
    assert isinstance(result, TopCandidateSelection)


def test_recommend_paper_only():
    result = recommend_top_candidates([_make_core("A")])
    assert result.paper_only is True


def test_recommend_not_investment_advice():
    result = recommend_top_candidates([_make_core("A")])
    assert result.not_investment_advice is True


def test_recommend_regime_stored():
    result = recommend_top_candidates([_make_core("A")], regime="BULL")
    assert result.regime == "BULL"


def test_recommend_to_dict():
    result = recommend_top_candidates([_make_core("A")])
    d = result.to_dict()
    assert isinstance(d, dict)
    assert d["paper_only"] is True
