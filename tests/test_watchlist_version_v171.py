"""tests/test_watchlist_version_v171.py — version identity tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.version_v171 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    ACCEPTED_MINIMUM_VERSION, KNOWN_RELEASE_NAMES,
    get_version_info, verify_version, is_known_release, check_minimum_version,
)


def test_version_string():
    assert VERSION == "1.7.1"


def test_release_name():
    assert RELEASE_NAME == "Watchlist Strategy Layer"


def test_base_release():
    assert BASE_RELEASE == "1.7.0 Small Capital Growth Strategy Template"


def test_schema_version():
    assert SCHEMA_VERSION == "171"


def test_policy_version_contains_version():
    assert "1.7.1" in POLICY_VERSION


def test_min_scenarios_gte_70():
    assert MIN_SCENARIOS >= 70


def test_min_fixtures_gte_70():
    assert MIN_FIXTURES >= 70


def test_min_cli_gte_22():
    assert MIN_CLI >= 22


def test_min_health_gte_70():
    assert MIN_HEALTH >= 70


def test_min_gate_gte_65():
    assert MIN_GATE >= 65


def test_accepted_minimum_version():
    assert ACCEPTED_MINIMUM_VERSION == "1.7.0"


def test_known_release_names_is_frozenset():
    assert isinstance(KNOWN_RELEASE_NAMES, frozenset)


def test_known_release_names_contains_self():
    assert "Watchlist Strategy Layer" in KNOWN_RELEASE_NAMES


def test_known_release_names_contains_v170():
    assert "Small Capital Growth Strategy Template" in KNOWN_RELEASE_NAMES


def test_get_version_info_returns_dict():
    assert isinstance(get_version_info(), dict)


def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True


def test_get_version_info_research_only():
    assert get_version_info()["research_only"] is True


def test_get_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True


def test_get_version_info_not_investment_advice():
    assert get_version_info()["not_investment_advice"] is True


def test_verify_version_returns_dict():
    assert isinstance(verify_version(), dict)


def test_is_known_release_self():
    assert is_known_release("Watchlist Strategy Layer") is True


def test_is_known_release_v170():
    assert is_known_release("Small Capital Growth Strategy Template") is True


def test_is_known_release_unknown():
    assert is_known_release("Nonexistent Release 9999") is False


def test_check_minimum_version_pass():
    assert check_minimum_version("1.7.0") is True


def test_check_minimum_version_equal():
    assert check_minimum_version("1.7.1") is True


def test_check_minimum_version_fail():
    assert check_minimum_version("1.6.0") is False


def test_check_minimum_version_old():
    assert check_minimum_version("1.5.0") is False
