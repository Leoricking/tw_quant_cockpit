"""
tests/test_decision_cockpit_version_v186.py
Tests for decision_cockpit_version_v186 module.
[!] Research Only. Paper Only. Decision Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_cockpit_version_v186 import (
    VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
    INCLUDED_RELEASES, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI,
    MIN_HEALTH_CHECKS, KNOWN_RELEASE_NAMES,
    get_version_info, verify_version, is_known_release, check_minimum_version,
)


def test_version_is_186():
    assert VERSION == "1.8.6"

def test_release_name():
    assert RELEASE_NAME == "End-to-End Small Capital Decision Cockpit"

def test_schema_version():
    assert SCHEMA_VERSION == "186"

def test_policy_version_contains_186():
    assert "1.8.6" in POLICY_VERSION

def test_policy_version_contains_decision_cockpit():
    assert "decision-cockpit" in POLICY_VERSION

def test_included_releases_count():
    assert len(INCLUDED_RELEASES) == 16

def test_included_releases_has_v170():
    assert "Small Capital Strategy v1.7.0" in INCLUDED_RELEASES

def test_included_releases_has_v185():
    assert "Portfolio Construction & Rebalancing Lab v1.8.5" in INCLUDED_RELEASES

def test_included_releases_has_v186():
    assert "End-to-End Small Capital Decision Cockpit v1.8.6" in INCLUDED_RELEASES

def test_min_scenarios_ge_75():
    assert MIN_SCENARIOS >= 75

def test_min_fixtures_ge_75():
    assert MIN_FIXTURES >= 75

def test_min_cli_ge_22():
    assert MIN_CLI >= 22

def test_min_health_checks_ge_60():
    assert MIN_HEALTH_CHECKS >= 60

def test_known_release_names_nonempty():
    assert len(KNOWN_RELEASE_NAMES) > 0

def test_get_version_info_returns_dict():
    assert isinstance(get_version_info(), dict)

def test_get_version_info_version():
    assert get_version_info()["version"] == "1.8.6"

def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True

def test_get_version_info_research_only():
    assert get_version_info()["research_only"] is True

def test_get_version_info_decision_only():
    assert get_version_info()["decision_only"] is True

def test_get_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True

def test_get_version_info_no_broker():
    assert get_version_info()["no_broker"] is True

def test_get_version_info_no_margin():
    assert get_version_info()["no_margin"] is True

def test_get_version_info_no_leverage():
    assert get_version_info()["no_leverage"] is True

def test_get_version_info_not_investment_advice():
    assert get_version_info()["not_investment_advice"] is True

def test_verify_version_true():
    assert verify_version() is True

def test_is_known_release_v170():
    assert is_known_release("Small Capital Strategy v1.7.0") is True

def test_is_known_release_v185():
    assert is_known_release("Portfolio Construction & Rebalancing Lab v1.8.5") is True

def test_is_known_release_v186():
    assert is_known_release("End-to-End Small Capital Decision Cockpit v1.8.6") is True

def test_is_known_release_unknown():
    assert is_known_release("Unknown Release v99.9") is False

def test_check_minimum_version_self():
    assert check_minimum_version("1.8.6") is True

def test_check_minimum_version_older():
    assert check_minimum_version("1.8.5") is True

def test_check_minimum_version_newer():
    assert check_minimum_version("1.9.0") is False

def test_schema_version_string():
    assert isinstance(SCHEMA_VERSION, str)

def test_version_string():
    assert isinstance(VERSION, str)
