"""
tests/test_position_sizing_version_v184.py
Tests for position_sizing_version_v184 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.position_sizing_version_v184 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    INCLUDED_RELEASES, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH_CHECKS,
    KNOWN_RELEASE_NAMES, get_version_info, verify_version, is_known_release,
    check_minimum_version,
)


def test_version_is_184():
    assert VERSION == "1.8.4"


def test_release_name_correct():
    assert RELEASE_NAME == "Position Sizing & Capital Allocation Lab"


def test_base_release_references_v183():
    assert "1.8.3" in BASE_RELEASE


def test_schema_version_is_184():
    assert SCHEMA_VERSION == "184"


def test_policy_version_contains_184():
    assert "1.8.4" in POLICY_VERSION


def test_policy_version_contains_position_sizing():
    assert "position-sizing" in POLICY_VERSION


def test_included_releases_is_list():
    assert isinstance(INCLUDED_RELEASES, list)


def test_included_releases_ge_14():
    assert len(INCLUDED_RELEASES) >= 14


def test_included_releases_contains_v170():
    assert any("1.7.0" in r for r in INCLUDED_RELEASES)


def test_included_releases_contains_v183():
    assert any("1.8.3" in r for r in INCLUDED_RELEASES)


def test_included_releases_contains_v184():
    assert any("1.8.4" in r for r in INCLUDED_RELEASES)


def test_min_scenarios_ge_75():
    assert MIN_SCENARIOS >= 75


def test_min_fixtures_ge_75():
    assert MIN_FIXTURES >= 75


def test_min_cli_ge_20():
    assert MIN_CLI >= 20


def test_min_health_checks_ge_60():
    assert MIN_HEALTH_CHECKS >= 60


def test_known_release_names_is_list():
    assert isinstance(KNOWN_RELEASE_NAMES, list)


def test_known_release_names_ge_14():
    assert len(KNOWN_RELEASE_NAMES) >= 14


def test_get_version_info_returns_dict():
    info = get_version_info()
    assert isinstance(info, dict)


def test_get_version_info_version():
    assert get_version_info()["version"] == "1.8.4"


def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True


def test_get_version_info_research_only():
    assert get_version_info()["research_only"] is True


def test_get_version_info_allocation_only():
    assert get_version_info()["allocation_only"] is True


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


def test_get_version_info_schema_version():
    assert get_version_info()["schema_version"] == "184"


def test_verify_version_true():
    assert verify_version() is True


def test_is_known_release_v170():
    assert is_known_release("Small Capital Strategy v1.7.0") is True


def test_is_known_release_v183():
    assert is_known_release("Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3") is True


def test_is_known_release_v184():
    assert is_known_release("Position Sizing & Capital Allocation Lab v1.8.4") is True


def test_is_known_release_unknown_false():
    assert is_known_release("Nonexistent Release vX.Y.Z") is False


def test_check_minimum_version_self():
    assert check_minimum_version("1.8.4") is True


def test_check_minimum_version_lower():
    assert check_minimum_version("1.8.3") is True


def test_check_minimum_version_higher_false():
    assert check_minimum_version("1.9.0") is False
