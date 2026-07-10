"""
tests/test_stable_rollup_version_v179.py
Tests for stable_rollup_version_v179 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_version_v179 import (
    VERSION,
    RELEASE_NAME,
    BASE_RELEASE,
    SCHEMA_VERSION,
    POLICY_VERSION,
    INCLUDED_RELEASES,
    MIN_SCENARIOS,
    MIN_FIXTURES,
    MIN_CLI,
    MIN_HEALTH,
    MIN_GATE,
    KNOWN_RELEASE_NAMES,
    get_version_info,
    verify_version,
    is_known_release,
    check_minimum_version,
)


def test_version_is_179():
    assert VERSION == "1.7.9"


def test_release_name_is_stable_rollup():
    assert RELEASE_NAME == "Small Capital Strategy Stable Rollup"


def test_base_release_is_178():
    assert BASE_RELEASE == "1.7.8 Small Capital Strategy Integration"


def test_schema_version_is_179():
    assert SCHEMA_VERSION == "179"


def test_policy_version_contains_179():
    assert "1.7.9" in POLICY_VERSION
    assert "stable-rollup" in POLICY_VERSION


def test_included_releases_count():
    assert len(INCLUDED_RELEASES) == 9


def test_included_releases_starts_v170():
    assert INCLUDED_RELEASES[0] == "v1.7.0"


def test_included_releases_ends_v178():
    assert INCLUDED_RELEASES[-1] == "v1.7.8"


def test_min_scenarios_ge_50():
    assert MIN_SCENARIOS >= 50


def test_min_fixtures_ge_50():
    assert MIN_FIXTURES >= 50


def test_min_cli_is_12():
    assert MIN_CLI == 12


def test_min_health_ge_50():
    assert MIN_HEALTH >= 50


def test_min_gate_ge_50():
    assert MIN_GATE >= 50


def test_known_release_names_is_frozenset():
    assert isinstance(KNOWN_RELEASE_NAMES, frozenset)


def test_known_release_names_contains_self():
    assert "Small Capital Strategy Stable Rollup" in KNOWN_RELEASE_NAMES


def test_known_release_names_contains_178():
    assert "Small Capital Strategy Integration" in KNOWN_RELEASE_NAMES


def test_get_version_info_returns_dict():
    info = get_version_info()
    assert isinstance(info, dict)


def test_get_version_info_version_field():
    info = get_version_info()
    assert info["version"] == "1.7.9"


def test_get_version_info_paper_only():
    info = get_version_info()
    assert info["paper_only"] is True


def test_get_version_info_no_real_orders():
    info = get_version_info()
    assert info["no_real_orders"] is True


def test_get_version_info_not_investment_advice():
    info = get_version_info()
    assert info["not_investment_advice"] is True


def test_get_version_info_research_only():
    info = get_version_info()
    assert info["research_only"] is True


def test_verify_version_returns_true():
    assert verify_version() is True


def test_is_known_release_self():
    assert is_known_release("Small Capital Strategy Stable Rollup") is True


def test_is_known_release_unknown_returns_false():
    assert is_known_release("Totally Unknown Release XYZ") is False


def test_check_minimum_version_self():
    assert check_minimum_version("1.7.9") is True


def test_check_minimum_version_higher():
    assert check_minimum_version("2.0.0") is True


def test_check_minimum_version_lower_returns_false():
    assert check_minimum_version("1.7.8") is False


def test_check_minimum_version_invalid_returns_false():
    assert check_minimum_version("not_a_version") is False
