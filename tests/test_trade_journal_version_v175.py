"""
tests/test_trade_journal_version_v175.py
Tests for Trade Journal version metadata v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.version_v175 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    KNOWN_RELEASE_NAMES, get_version_info, verify_version, is_known_release,
    check_minimum_version,
)


class TestVersionConstants:
    def test_version_is_175(self):
        assert VERSION == "1.7.5"

    def test_release_name_correct(self):
        assert RELEASE_NAME == "Small Account Trade Journal"

    def test_base_release_correct(self):
        assert BASE_RELEASE == "1.7.4 Small Account Risk Dashboard"

    def test_schema_version_175(self):
        assert SCHEMA_VERSION == "175"

    def test_policy_version_correct(self):
        assert POLICY_VERSION == "1.7.5-small-account-trade-journal"

    def test_component_count_16(self):
        assert COMPONENT_COUNT == 16

    def test_min_scenarios_55(self):
        assert MIN_SCENARIOS >= 55

    def test_min_fixtures_55(self):
        assert MIN_FIXTURES >= 55

    def test_min_cli_15(self):
        assert MIN_CLI >= 15

    def test_min_health_70(self):
        assert MIN_HEALTH >= 70

    def test_min_gate_65(self):
        assert MIN_GATE >= 65


class TestVersionFunctions:
    def test_verify_version_true(self):
        assert verify_version() is True

    def test_get_version_info_returns_dict(self):
        assert isinstance(get_version_info(), dict)

    def test_get_version_info_version_key(self):
        assert get_version_info()["version"] == "1.7.5"

    def test_get_version_info_paper_only(self):
        assert get_version_info()["paper_only"] is True

    def test_get_version_info_research_only(self):
        assert get_version_info()["research_only"] is True

    def test_get_version_info_no_real_orders(self):
        assert get_version_info()["no_real_orders"] is True

    def test_get_version_info_not_investment_advice(self):
        assert get_version_info()["not_investment_advice"] is True


class TestKnownReleases:
    def test_known_release_v175(self):
        assert is_known_release("Small Account Trade Journal")

    def test_known_release_v174(self):
        assert is_known_release("Small Account Risk Dashboard")

    def test_known_release_v173(self):
        assert is_known_release("Market Regime Position Control")

    def test_known_release_v172(self):
        assert is_known_release("A/B/C Buy Point Execution Plan")

    def test_known_release_v171(self):
        assert is_known_release("Watchlist Strategy Layer")

    def test_known_release_v170(self):
        assert is_known_release("Small Capital Growth Strategy")

    def test_unknown_release_false(self):
        assert not is_known_release("Unknown Release Name XYZ")

    def test_known_release_names_is_frozenset(self):
        assert isinstance(KNOWN_RELEASE_NAMES, frozenset)

    def test_known_release_names_ge_7(self):
        assert len(KNOWN_RELEASE_NAMES) >= 7


class TestCheckMinimumVersion:
    def test_same_version_true(self):
        assert check_minimum_version("1.7.5") is True

    def test_higher_version_true(self):
        assert check_minimum_version("1.7.6") is True

    def test_lower_version_false(self):
        assert check_minimum_version("1.7.4") is False

    def test_invalid_version_false(self):
        assert check_minimum_version("not-a-version") is False
