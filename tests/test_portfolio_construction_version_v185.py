"""
tests/test_portfolio_construction_version_v185.py
Tests for portfolio_construction_version_v185 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_construction_version_v185 import (
    VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
    BASE_RELEASE, INCLUDED_RELEASES, KNOWN_RELEASE_NAMES,
    MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH_CHECKS,
    get_version_info, verify_version, is_known_release, check_minimum_version,
)


def test_version_is_185():
    assert VERSION == "1.8.5"

def test_release_name():
    assert RELEASE_NAME == "Portfolio Construction & Rebalancing Lab"

def test_schema_version():
    assert SCHEMA_VERSION == "185"

def test_policy_version_contains_185():
    assert "1.8.5" in POLICY_VERSION

def test_base_release_contains_184():
    assert "1.8.4" in BASE_RELEASE

def test_included_releases_count():
    assert len(INCLUDED_RELEASES) == 15

def test_known_release_names_count():
    assert len(KNOWN_RELEASE_NAMES) == 15

def test_min_scenarios_75():
    assert MIN_SCENARIOS == 75

def test_min_fixtures_75():
    assert MIN_FIXTURES == 75

def test_min_cli_22():
    assert MIN_CLI == 22

def test_min_health_checks_60():
    assert MIN_HEALTH_CHECKS == 60

def test_get_version_info_dict():
    info = get_version_info()
    assert isinstance(info, dict)

def test_get_version_info_version():
    assert get_version_info()["version"] == "1.8.5"

def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True

def test_get_version_info_research_only():
    assert get_version_info()["research_only"] is True

def test_get_version_info_portfolio_only():
    assert get_version_info()["portfolio_only"] is True

def test_get_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True

def test_get_version_info_no_broker():
    assert get_version_info()["no_broker"] is True

def test_get_version_info_no_margin():
    assert get_version_info()["no_margin"] is True

def test_get_version_info_no_leverage():
    assert get_version_info()["no_leverage"] is True

def test_verify_version_true():
    assert verify_version() is True

def test_is_known_release_v170():
    assert is_known_release("Small Capital Strategy v1.7.0") is True

def test_is_known_release_v184():
    assert is_known_release("Position Sizing & Capital Allocation Lab v1.8.4") is True

def test_is_known_release_v185():
    assert is_known_release("Portfolio Construction & Rebalancing Lab v1.8.5") is True

def test_is_known_release_unknown():
    assert is_known_release("Unknown Release v9.9.9") is False

def test_check_minimum_version_equal():
    assert check_minimum_version("1.8.5") is True

def test_check_minimum_version_lower():
    assert check_minimum_version("1.8.4") is True

def test_check_minimum_version_higher():
    assert check_minimum_version("1.9.0") is False
