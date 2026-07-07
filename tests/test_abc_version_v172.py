"""tests/test_abc_version_v172.py — Version identity tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.version_v172 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    ACCEPTED_MINIMUM_VERSION, KNOWN_RELEASE_NAMES,
    get_version_info, verify_version, is_known_release, check_minimum_version,
)


def test_version_is_172():
    assert VERSION == "1.7.2"


def test_release_name():
    assert RELEASE_NAME == "A/B/C Buy Point Execution Plan"


def test_base_release():
    assert BASE_RELEASE == "1.7.1 Watchlist Strategy Layer"


def test_schema_version():
    assert SCHEMA_VERSION == "172"


def test_policy_version_contains_172():
    assert "1.7.2" in POLICY_VERSION


def test_component_count_ge_24():
    assert COMPONENT_COUNT >= 24


def test_min_scenarios_70():
    assert MIN_SCENARIOS >= 70


def test_min_fixtures_70():
    assert MIN_FIXTURES >= 70


def test_min_cli_20():
    assert MIN_CLI >= 20


def test_min_health_75():
    assert MIN_HEALTH >= 75


def test_min_gate_70():
    assert MIN_GATE >= 70


def test_accepted_minimum_version():
    assert ACCEPTED_MINIMUM_VERSION == "1.7.1"


def test_known_release_names_is_frozenset():
    assert isinstance(KNOWN_RELEASE_NAMES, frozenset)


def test_known_release_names_includes_self():
    assert "A/B/C Buy Point Execution Plan" in KNOWN_RELEASE_NAMES


def test_known_release_names_includes_v171():
    assert "Watchlist Strategy Layer" in KNOWN_RELEASE_NAMES


def test_known_release_names_includes_v170():
    assert "Small Capital Growth Strategy Template" in KNOWN_RELEASE_NAMES


def test_get_version_info_returns_dict():
    info = get_version_info()
    assert isinstance(info, dict)


def test_get_version_info_version():
    assert get_version_info()["version"] == "1.7.2"


def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True


def test_get_version_info_not_investment_advice():
    assert get_version_info()["not_investment_advice"] is True


def test_verify_version_returns_dict():
    assert isinstance(verify_version(), dict)


def test_verify_version_matches_get_version_info():
    assert verify_version() == get_version_info()


def test_is_known_release_self():
    assert is_known_release("A/B/C Buy Point Execution Plan") is True


def test_is_known_release_v171():
    assert is_known_release("Watchlist Strategy Layer") is True


def test_is_known_release_unknown_false():
    assert is_known_release("Nonexistent Release") is False


def test_check_minimum_version_171():
    assert check_minimum_version("1.7.1") is True


def test_check_minimum_version_172():
    assert check_minimum_version("1.7.2") is True


def test_check_minimum_version_160_false():
    assert check_minimum_version("1.6.0") is False


def test_check_minimum_version_invalid_false():
    assert check_minimum_version("not_a_version") is False
