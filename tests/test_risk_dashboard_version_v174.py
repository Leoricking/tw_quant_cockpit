"""
tests/test_risk_dashboard_version_v174.py
Tests for Small Account Risk Dashboard version v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.version_v174 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    KNOWN_RELEASE_NAMES, get_version_info, verify_version, is_known_release,
    check_minimum_version,
)


class TestVersionConstants:
    def test_version_is_174(self):
        assert VERSION == "1.7.4"

    def test_release_name(self):
        assert RELEASE_NAME == "Small Account Risk Dashboard"

    def test_base_release(self):
        assert BASE_RELEASE == "1.7.3 Market Regime Position Control"

    def test_schema_version(self):
        assert SCHEMA_VERSION == "174"

    def test_policy_version_contains_174(self):
        assert "1.7.4" in POLICY_VERSION

    def test_component_count_24(self):
        assert COMPONENT_COUNT == 24

    def test_min_scenarios_65(self):
        assert MIN_SCENARIOS >= 65

    def test_min_fixtures_65(self):
        assert MIN_FIXTURES >= 65

    def test_min_cli_19(self):
        assert MIN_CLI >= 19

    def test_min_health_70(self):
        assert MIN_HEALTH >= 70

    def test_min_gate_65(self):
        assert MIN_GATE >= 65


class TestKnownReleaseNames:
    def test_includes_174(self):
        assert "Small Account Risk Dashboard" in KNOWN_RELEASE_NAMES

    def test_includes_173(self):
        assert "Market Regime Position Control" in KNOWN_RELEASE_NAMES

    def test_includes_172(self):
        assert "A/B/C Buy Point Execution Plan" in KNOWN_RELEASE_NAMES

    def test_includes_171(self):
        assert "Watchlist Strategy Layer" in KNOWN_RELEASE_NAMES

    def test_is_frozenset(self):
        assert isinstance(KNOWN_RELEASE_NAMES, frozenset)

    def test_at_least_6_releases(self):
        assert len(KNOWN_RELEASE_NAMES) >= 6


class TestVersionFunctions:
    def test_verify_version_true(self):
        assert verify_version() is True

    def test_is_known_release_self(self):
        assert is_known_release("Small Account Risk Dashboard") is True

    def test_is_known_release_unknown_false(self):
        assert is_known_release("Nonexistent Release XYZ") is False

    def test_get_version_info_dict(self):
        info = get_version_info()
        assert isinstance(info, dict)

    def test_get_version_info_version_key(self):
        assert get_version_info()["version"] == "1.7.4"

    def test_get_version_info_paper_only(self):
        assert get_version_info()["paper_only"] is True

    def test_get_version_info_research_only(self):
        assert get_version_info()["research_only"] is True

    def test_get_version_info_no_real_orders(self):
        assert get_version_info()["no_real_orders"] is True

    def test_get_version_info_not_investment_advice(self):
        assert get_version_info()["not_investment_advice"] is True

    def test_check_minimum_version_self(self):
        assert check_minimum_version("1.7.4") is True

    def test_check_minimum_version_higher(self):
        assert check_minimum_version("1.7.5") is True

    def test_check_minimum_version_lower(self):
        assert check_minimum_version("1.7.3") is False

    def test_check_minimum_version_invalid(self):
        assert check_minimum_version("not_a_version") is False
