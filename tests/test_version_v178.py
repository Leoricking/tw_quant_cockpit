"""
tests/test_version_v178.py
Tests for version_v178.py — v1.7.8 Small Capital Strategy Integration.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.

Safety invariants:
    paper_only=True, no_real_orders=True, no_broker=True, not_investment_advice=True
"""
import pytest
from paper_trading.small_capital_strategy.version_v178 import (
    VERSION,
    RELEASE_NAME,
    SCHEMA_VERSION,
    POLICY_VERSION,
    BASE_RELEASE,
    COMPONENT_COUNT,
    MIN_SCENARIOS,
    MIN_FIXTURES,
    MIN_CLI,
    MIN_HEALTH,
    MIN_GATE,
    get_version_info,
    verify_version,
    is_known_release,
    check_minimum_version,
)

# ---------------------------------------------------------------------------
# Safety invariants (module-level constants)
# ---------------------------------------------------------------------------
paper_only = True
no_real_orders = True
no_broker = True
not_investment_advice = True


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

def test_version_is_1_7_8():
    assert VERSION == "1.7.8"


def test_release_name_is_small_capital_strategy_integration():
    assert RELEASE_NAME == "Small Capital Strategy Integration"


def test_schema_version_is_178():
    assert SCHEMA_VERSION == "178"


def test_policy_version_is_correct_string():
    assert POLICY_VERSION == "1.7.8-small-capital-strategy-integration"


def test_base_release_is_theme_rotation_scanner():
    assert BASE_RELEASE == "1.7.7 Theme Rotation Scanner"


def test_component_count_is_at_least_10():
    assert COMPONENT_COUNT >= 10


def test_min_scenarios_is_at_least_70():
    assert MIN_SCENARIOS >= 70


def test_min_fixtures_is_at_least_70():
    assert MIN_FIXTURES >= 70


def test_min_cli_is_at_least_17():
    assert MIN_CLI >= 17


def test_min_health_is_at_least_70():
    assert MIN_HEALTH >= 70


def test_min_gate_is_at_least_70():
    assert MIN_GATE >= 70


# ---------------------------------------------------------------------------
# get_version_info
# ---------------------------------------------------------------------------

def test_get_version_info_returns_dict():
    result = get_version_info()
    assert isinstance(result, dict)


def test_get_version_info_version_is_1_7_8():
    assert get_version_info()["version"] == "1.7.8"


def test_get_version_info_paper_only_is_true():
    assert get_version_info()["paper_only"] is True


def test_get_version_info_research_only_is_true():
    assert get_version_info()["research_only"] is True


def test_get_version_info_no_real_orders_is_true():
    assert get_version_info()["no_real_orders"] is True


def test_get_version_info_not_investment_advice_is_true():
    assert get_version_info()["not_investment_advice"] is True


def test_get_version_info_demo_only_is_true():
    assert get_version_info()["demo_only"] is True


def test_get_version_info_not_for_production_is_true():
    assert get_version_info()["not_for_production"] is True


def test_get_version_info_release_name_matches_constant():
    assert get_version_info()["release_name"] == RELEASE_NAME


def test_get_version_info_base_release_matches_constant():
    assert get_version_info()["base_release"] == BASE_RELEASE


def test_get_version_info_schema_version_matches_constant():
    assert get_version_info()["schema_version"] == SCHEMA_VERSION


def test_get_version_info_policy_version_matches_constant():
    assert get_version_info()["policy_version"] == POLICY_VERSION


def test_get_version_info_component_count_matches_constant():
    assert get_version_info()["component_count"] == COMPONENT_COUNT


def test_get_version_info_min_scenarios_matches_constant():
    assert get_version_info()["min_scenarios"] == MIN_SCENARIOS


# ---------------------------------------------------------------------------
# verify_version
# ---------------------------------------------------------------------------

def test_verify_version_returns_true():
    assert verify_version() is True


def test_verify_version_returns_bool():
    assert isinstance(verify_version(), bool)


# ---------------------------------------------------------------------------
# is_known_release
# ---------------------------------------------------------------------------

def test_is_known_release_small_capital_strategy_integration():
    assert is_known_release("Small Capital Strategy Integration") is True


def test_is_known_release_theme_rotation_scanner():
    assert is_known_release("Theme Rotation Scanner") is True


def test_is_known_release_mistake_taxonomy_and_weekly_review():
    assert is_known_release("Mistake Taxonomy & Weekly Review Dashboard") is True


def test_is_known_release_small_account_trade_journal():
    assert is_known_release("Small Account Trade Journal") is True


def test_is_known_release_market_regime_position_control():
    assert is_known_release("Market Regime Position Control") is True


def test_is_known_release_abc_buy_point_execution_plan():
    assert is_known_release("A/B/C Buy Point Execution Plan") is True


def test_is_known_release_watchlist_strategy_layer():
    assert is_known_release("Watchlist Strategy Layer") is True


def test_is_known_release_nonexistent_returns_false():
    assert is_known_release("NonExistent Release") is False


def test_is_known_release_empty_string_returns_false():
    assert is_known_release("") is False


def test_is_known_release_case_sensitive_wrong_case_returns_false():
    assert is_known_release("theme rotation scanner") is False


# ---------------------------------------------------------------------------
# check_minimum_version
# ---------------------------------------------------------------------------

def test_check_minimum_version_same_version_is_true():
    assert check_minimum_version("1.7.8") is True


def test_check_minimum_version_higher_major_is_true():
    assert check_minimum_version("2.0.0") is True


def test_check_minimum_version_lower_patch_is_false():
    assert check_minimum_version("1.7.7") is False


def test_check_minimum_version_much_lower_is_false():
    assert check_minimum_version("1.0.0") is False


def test_check_minimum_version_higher_minor_is_true():
    assert check_minimum_version("1.8.0") is True


def test_check_minimum_version_higher_patch_is_true():
    assert check_minimum_version("1.7.9") is True


def test_check_minimum_version_returns_bool():
    assert isinstance(check_minimum_version("1.7.8"), bool)


def test_check_minimum_version_lower_major_is_false():
    assert check_minimum_version("0.9.9") is False
