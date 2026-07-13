"""
tests/test_decision_cockpit_fixtures_v186.py
Tests for decision_cockpit_fixtures_v186 module.
[!] Research Only. Paper Only. Decision Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_cockpit_fixtures_v186 import (
    get_fixture_dir, get_fixture_count, get_fixture_info,
    _EXPECTED_COUNT,
)


def test_get_fixture_count_ge_75():
    assert get_fixture_count() >= 75

def test_get_fixture_count_exact():
    assert get_fixture_count() == 75

def test_expected_count_ge_75():
    assert _EXPECTED_COUNT >= 75

def test_get_fixture_dir_returns_str():
    assert isinstance(get_fixture_dir(), str)

def test_get_fixture_dir_nonempty():
    assert len(get_fixture_dir()) > 0

def test_get_fixture_dir_contains_decision_cockpit():
    assert "decision_cockpit" in get_fixture_dir()

def test_get_fixture_info_returns_dict():
    assert isinstance(get_fixture_info(), dict)

def test_get_fixture_info_paper_only():
    assert get_fixture_info()["paper_only"] is True

def test_get_fixture_info_research_only():
    assert get_fixture_info()["research_only"] is True

def test_get_fixture_info_decision_only():
    assert get_fixture_info()["decision_only"] is True

def test_get_fixture_info_no_real_orders():
    assert get_fixture_info()["no_real_orders"] is True

def test_get_fixture_info_no_broker():
    assert get_fixture_info()["no_broker"] is True

def test_get_fixture_info_no_margin():
    assert get_fixture_info()["no_margin"] is True

def test_get_fixture_info_no_leverage():
    assert get_fixture_info()["no_leverage"] is True

def test_get_fixture_info_not_investment_advice():
    assert get_fixture_info()["not_investment_advice"] is True

def test_get_fixture_info_demo_only():
    assert get_fixture_info()["demo_only"] is True

def test_get_fixture_info_not_for_production():
    assert get_fixture_info()["not_for_production"] is True

def test_get_fixture_info_production_trading_blocked():
    assert get_fixture_info()["production_trading_blocked"] is True

def test_get_fixture_info_expected_count():
    assert get_fixture_info()["expected_count"] == 75

def test_get_fixture_info_schema_version():
    assert get_fixture_info()["schema_version"] == "186"
