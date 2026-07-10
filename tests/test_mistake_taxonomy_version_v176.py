"""tests/test_mistake_taxonomy_version_v176.py — v1.7.6 version metadata tests."""
import pytest
from paper_trading.small_capital_strategy.version_v176 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    KNOWN_RELEASE_NAMES, get_version_info, verify_version, is_known_release,
    check_minimum_version,
)


class TestVersionConstants:
    def test_version_is_176(self):
        assert VERSION == "1.7.6"

    def test_release_name_correct(self):
        assert RELEASE_NAME == "Mistake Taxonomy & Weekly Review Dashboard"

    def test_base_release_correct(self):
        assert BASE_RELEASE == "1.7.5 Small Account Trade Journal"

    def test_schema_version_176(self):
        assert SCHEMA_VERSION == "176"

    def test_policy_version_correct(self):
        assert POLICY_VERSION == "1.7.6-mistake-taxonomy-weekly-review"

    def test_component_count_14(self):
        assert COMPONENT_COUNT == 14

    def test_min_scenarios_60(self):
        assert MIN_SCENARIOS >= 60

    def test_min_fixtures_60(self):
        assert MIN_FIXTURES >= 60

    def test_min_cli_14(self):
        assert MIN_CLI >= 14

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
        assert get_version_info()["version"] == "1.7.6"

    def test_get_version_info_paper_only(self):
        assert get_version_info()["paper_only"] is True

    def test_get_version_info_research_only(self):
        assert get_version_info()["research_only"] is True

    def test_get_version_info_no_real_orders(self):
        assert get_version_info()["no_real_orders"] is True

    def test_get_version_info_not_investment_advice(self):
        assert get_version_info()["not_investment_advice"] is True

    def test_check_minimum_version_self(self):
        assert check_minimum_version("1.7.6") is True

    def test_check_minimum_version_above(self):
        assert check_minimum_version("1.7.7") is True

    def test_check_minimum_version_below(self):
        assert check_minimum_version("1.7.5") is False


class TestKnownReleases:
    def test_known_release_v176(self):
        assert is_known_release("Mistake Taxonomy & Weekly Review Dashboard")

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

    def test_unknown_release_false(self):
        assert not is_known_release("Nonexistent Release")

    def test_known_release_names_is_frozenset(self):
        assert isinstance(KNOWN_RELEASE_NAMES, frozenset)
