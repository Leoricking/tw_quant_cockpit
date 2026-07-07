"""tests/test_watchlist_profile_v171.py — watchlist profile / overdiversification tests."""
import pytest
from paper_trading.small_capital_strategy.overdiversification_detector_v171 import (
    detect_overdiversification, get_watchlist_size_rules,
    DEFAULT_WATCHLIST, MAX_WATCHLIST, FOCUS_CANDIDATES, TRADABLE_CANDIDATES, TRAINING_MAX,
    MIN_WATCHLIST,
)
from paper_trading.small_capital_strategy.watchlist_enums_v171 import OverdiversificationStatus
from paper_trading.small_capital_strategy.watchlist_candidate_v171 import make_sample_candidate


def _pool(n):
    return [make_sample_candidate(str(i)) for i in range(n)]


def test_default_watchlist_30():
    assert DEFAULT_WATCHLIST == 30


def test_max_watchlist_50():
    assert MAX_WATCHLIST == 50


def test_focus_candidates_10():
    assert FOCUS_CANDIDATES == 10


def test_tradable_candidates_5():
    assert TRADABLE_CANDIDATES == 5


def test_training_max_5():
    assert TRAINING_MAX == 5


def test_min_watchlist_10():
    assert MIN_WATCHLIST == 10


def test_optimal_20_candidates():
    ov = detect_overdiversification(_pool(20))
    assert ov.status == OverdiversificationStatus.OPTIMAL


def test_optimal_30_candidates():
    ov = detect_overdiversification(_pool(30))
    assert ov.status == OverdiversificationStatus.OPTIMAL


def test_insufficient_below_10():
    ov = detect_overdiversification(_pool(5))
    assert ov.status == OverdiversificationStatus.INSUFFICIENT_COVERAGE


def test_insufficient_zero():
    ov = detect_overdiversification([])
    assert ov.status == OverdiversificationStatus.INSUFFICIENT_COVERAGE


def test_overdiversified_above_50():
    ov = detect_overdiversification(_pool(55))
    assert ov.status == OverdiversificationStatus.OVERDIVERSIFIED


def test_acceptable_40_candidates():
    ov = detect_overdiversification(_pool(40))
    assert ov.status == OverdiversificationStatus.OPTIMAL


def test_total_count_correct():
    ov = detect_overdiversification(_pool(15))
    assert ov.total_candidates == 15


def test_result_paper_only():
    ov = detect_overdiversification(_pool(20))
    assert ov.paper_only is True


def test_result_to_dict():
    d = detect_overdiversification(_pool(20)).to_dict()
    assert isinstance(d, dict)
    assert d["paper_only"] is True


def test_get_rules_dict():
    rules = get_watchlist_size_rules()
    assert isinstance(rules, dict)
    assert rules["default_watchlist"] == DEFAULT_WATCHLIST
