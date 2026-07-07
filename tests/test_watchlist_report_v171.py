"""tests/test_watchlist_report_v171.py — watchlist report tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_report_v171 import (
    get_section_names, SECTION_NAMES,
)


def test_section_names_is_list():
    assert isinstance(get_section_names(), list)


def test_section_names_count():
    assert len(get_section_names()) == 14


def test_section_names_constant_length():
    assert len(SECTION_NAMES) == 14


def test_section_names_watchlist_profile():
    assert "watchlist_profile" in get_section_names()


def test_section_names_candidate_pool_summary():
    assert "candidate_pool_summary" in get_section_names()


def test_section_names_theme_rotation():
    assert "theme_rotation" in get_section_names()


def test_section_names_ranking_method():
    assert "ranking_method" in get_section_names()


def test_section_names_top_10_focus():
    assert "top_10_focus_candidates" in get_section_names()


def test_section_names_top_5_tradable():
    assert "top_5_tradable_candidates" in get_section_names()


def test_section_names_tier_classification():
    assert "tier_classification" in get_section_names()


def test_section_names_excluded_candidates():
    assert "excluded_candidates" in get_section_names()


def test_section_names_overdiversification():
    assert "overdiversification_check" in get_section_names()


def test_section_names_small_capital_fit():
    assert "small_capital_fit" in get_section_names()


def test_section_names_v170_allocation():
    assert "v170_allocation_mapping" in get_section_names()


def test_section_names_risk_notes():
    assert "risk_notes" in get_section_names()


def test_section_names_safety():
    assert "safety" in get_section_names()


def test_section_names_not_investment_advice():
    assert "not_investment_advice" in get_section_names()


def test_get_section_names_returns_copy():
    names = get_section_names()
    names.append("EXTRA")
    # Original should be unchanged
    assert "EXTRA" not in SECTION_NAMES


def test_section_names_no_duplicates():
    names = get_section_names()
    assert len(names) == len(set(names))
