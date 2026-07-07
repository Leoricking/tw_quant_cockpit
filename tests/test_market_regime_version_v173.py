"""
tests/test_market_regime_version_v173.py
Tests for Market Regime Position Control version_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.version_v173 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    KNOWN_RELEASE_NAMES, get_version_info, verify_version, is_known_release,
    check_minimum_version,
)


class TestVersionConstants:
    def test_version_is_173(self):
        assert VERSION == "1.7.3"

    def test_release_name(self):
        assert RELEASE_NAME == "Market Regime Position Control"

    def test_base_release(self):
        assert BASE_RELEASE == "1.7.2 A/B/C Buy Point Execution Plan"

    def test_schema_version(self):
        assert SCHEMA_VERSION == "173"

    def test_policy_version(self):
        assert POLICY_VERSION == "1.7.3-market-regime-position-control"

    def test_component_count_23(self):
        assert COMPONENT_COUNT == 23

    def test_min_scenarios_65(self):
        assert MIN_SCENARIOS >= 65

    def test_min_fixtures_65(self):
        assert MIN_FIXTURES >= 65

    def test_min_cli_18(self):
        assert MIN_CLI >= 18

    def test_min_health_70(self):
        assert MIN_HEALTH >= 70

    def test_min_gate_65(self):
        assert MIN_GATE >= 65


class TestKnownReleaseNames:
    def test_known_releases_frozenset(self):
        assert isinstance(KNOWN_RELEASE_NAMES, frozenset)

    def test_includes_173(self):
        assert "Market Regime Position Control" in KNOWN_RELEASE_NAMES

    def test_includes_172(self):
        assert "A/B/C Buy Point Execution Plan" in KNOWN_RELEASE_NAMES

    def test_includes_171(self):
        assert "Watchlist Strategy Layer" in KNOWN_RELEASE_NAMES

    def test_includes_169(self):
        assert "Live Paper Trading Stable Rollup" in KNOWN_RELEASE_NAMES

    def test_includes_small_capital(self):
        assert "Small Capital Growth Strategy" in KNOWN_RELEASE_NAMES


class TestGetVersionInfo:
    def test_returns_dict(self):
        info = get_version_info()
        assert isinstance(info, dict)

    def test_version_key(self):
        assert get_version_info()["version"] == "1.7.3"

    def test_paper_only_true(self):
        assert get_version_info()["paper_only"] is True

    def test_no_real_orders_true(self):
        assert get_version_info()["no_real_orders"] is True

    def test_research_only_true(self):
        assert get_version_info()["research_only"] is True

    def test_not_investment_advice_true(self):
        assert get_version_info()["not_investment_advice"] is True

    def test_all_required_keys(self):
        info = get_version_info()
        for key in ["version", "release_name", "schema_version", "policy_version"]:
            assert key in info


class TestVerifyVersion:
    def test_verify_returns_true(self):
        assert verify_version() is True


class TestIsKnownRelease:
    def test_self_is_known(self):
        assert is_known_release("Market Regime Position Control") is True

    def test_unknown_is_false(self):
        assert is_known_release("Fake Release v99") is False

    def test_172_is_known(self):
        assert is_known_release("A/B/C Buy Point Execution Plan") is True


class TestCheckMinimumVersion:
    def test_self_passes(self):
        assert check_minimum_version("1.7.3") is True

    def test_higher_passes(self):
        assert check_minimum_version("1.7.4") is True

    def test_lower_fails(self):
        assert check_minimum_version("1.7.2") is False

    def test_invalid_returns_false(self):
        assert check_minimum_version("not_a_version") is False
