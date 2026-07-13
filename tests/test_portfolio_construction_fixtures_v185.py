"""
tests/test_portfolio_construction_fixtures_v185.py
Tests for portfolio_construction_fixtures_v185 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_construction_fixtures_v185 import (
    get_fixture_count, get_fixture_dir, get_fixture_info, _EXPECTED_COUNT,
)


def test_fixture_count_ge_75():
    assert get_fixture_count() >= 75

def test_fixture_count_exact():
    assert get_fixture_count() == 75

def test_expected_count_75():
    assert _EXPECTED_COUNT == 75

def test_fixture_dir_is_str():
    assert isinstance(get_fixture_dir(), str)

def test_fixture_dir_nonempty():
    assert len(get_fixture_dir()) > 0

def test_fixture_dir_ends_portfolio_construction():
    assert get_fixture_dir().endswith("portfolio_construction")

def test_fixture_info_is_dict():
    assert isinstance(get_fixture_info(), dict)

def test_fixture_info_paper_only():
    assert get_fixture_info()["paper_only"] is True

def test_fixture_info_research_only():
    assert get_fixture_info()["research_only"] is True

def test_fixture_info_portfolio_only():
    assert get_fixture_info()["portfolio_only"] is True

def test_fixture_info_no_real_orders():
    assert get_fixture_info()["no_real_orders"] is True

def test_fixture_info_schema_version():
    assert get_fixture_info()["schema_version"] == "185"

def test_fixture_info_expected_count():
    assert get_fixture_info()["expected_count"] == 75

def test_fixture_info_fixture_dir_key():
    assert "fixture_dir" in get_fixture_info()
