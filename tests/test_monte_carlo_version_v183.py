"""
tests/test_monte_carlo_version_v183.py
Tests for Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3 version metadata.
[!] Research Only. Paper Only. Monte Carlo Only.
"""
from paper_trading.small_capital_strategy.monte_carlo_version_v183 import (
    VERSION,
    RELEASE_NAME,
    BASE_RELEASE,
    SCHEMA_VERSION,
    POLICY_VERSION,
    INCLUDED_RELEASES,
    KNOWN_RELEASE_NAMES,
    MIN_SCENARIOS,
    MIN_FIXTURES,
    MIN_CLI,
    MIN_HEALTH_CHECKS,
    get_version_info,
    verify_version,
    is_known_release,
    check_minimum_version,
)


# --- VERSION ---

def test_version_equals_183():
    assert VERSION == "1.8.3"


def test_version_is_str():
    assert isinstance(VERSION, str)


# --- RELEASE_NAME ---

def test_release_name_value():
    assert RELEASE_NAME == "Monte Carlo Risk-of-Ruin & Robustness Lab"


def test_release_name_contains_monte_carlo():
    assert "Monte Carlo" in RELEASE_NAME


def test_release_name_contains_risk_of_ruin():
    assert "Risk-of-Ruin" in RELEASE_NAME


# --- BASE_RELEASE ---

def test_base_release_value():
    assert BASE_RELEASE == "v1.8.2-parameter-optimization-walk-forward-validation-lab"


def test_base_release_contains_182():
    assert "1.8.2" in BASE_RELEASE


# --- SCHEMA_VERSION ---

def test_schema_version_equals_183():
    assert SCHEMA_VERSION == "183"


def test_schema_version_is_str():
    assert isinstance(SCHEMA_VERSION, str)


# --- POLICY_VERSION ---

def test_policy_version_contains_183():
    assert "1.8.3" in POLICY_VERSION


def test_policy_version_contains_monte_carlo():
    assert "monte-carlo" in POLICY_VERSION


# --- INCLUDED_RELEASES ---

def test_included_releases_has_13_entries():
    assert len(INCLUDED_RELEASES) == 13


def test_included_releases_is_list():
    assert isinstance(INCLUDED_RELEASES, list)


def test_included_releases_contains_small_capital_strategy_v170():
    assert "Small Capital Strategy v1.7.0" in INCLUDED_RELEASES


def test_included_releases_contains_monte_carlo_v183():
    assert "Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3" in INCLUDED_RELEASES


def test_included_releases_contains_parameter_optimization_v182():
    assert "Parameter Optimization & Walk-Forward Validation Lab v1.8.2" in INCLUDED_RELEASES


# --- MIN_ constants ---

def test_min_scenarios_equals_75():
    assert MIN_SCENARIOS == 75


def test_min_fixtures_equals_75():
    assert MIN_FIXTURES == 75


def test_min_cli_equals_18():
    assert MIN_CLI == 18


def test_min_health_checks_equals_60():
    assert MIN_HEALTH_CHECKS == 60


# --- KNOWN_RELEASE_NAMES ---

def test_known_release_names_has_13_entries():
    assert len(KNOWN_RELEASE_NAMES) == 13


def test_known_release_names_is_list():
    assert isinstance(KNOWN_RELEASE_NAMES, list)


def test_known_release_names_contains_small_capital_strategy_v170():
    assert "Small Capital Strategy v1.7.0" in KNOWN_RELEASE_NAMES


def test_known_release_names_contains_monte_carlo_v183():
    assert "Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3" in KNOWN_RELEASE_NAMES


def test_all_known_release_names_are_str():
    assert all(isinstance(name, str) for name in KNOWN_RELEASE_NAMES)


# --- get_version_info() ---

def test_get_version_info_returns_dict():
    result = get_version_info()
    assert isinstance(result, dict)


def test_get_version_info_version_equals_183():
    assert get_version_info()["version"] == "1.8.3"


def test_get_version_info_paper_only_is_true():
    assert get_version_info()["paper_only"] is True


def test_get_version_info_monte_carlo_only_is_true():
    assert get_version_info()["monte_carlo_only"] is True


def test_get_version_info_research_only_is_true():
    assert get_version_info()["research_only"] is True


def test_get_version_info_no_broker_is_true():
    assert get_version_info()["no_broker"] is True


def test_get_version_info_schema_version_equals_183():
    assert get_version_info()["schema_version"] == "183"


# --- verify_version() ---

def test_verify_version_is_true():
    assert verify_version() is True


def test_verify_version_returns_bool():
    assert isinstance(verify_version(), bool)


# --- is_known_release() ---

def test_is_known_release_monte_carlo_v183_is_true():
    assert is_known_release("Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3") is True


def test_is_known_release_small_capital_strategy_v170_is_true():
    assert is_known_release("Small Capital Strategy v1.7.0") is True


def test_is_known_release_unknown_is_false():
    assert is_known_release("Unknown Release v9.9.9") is False


def test_is_known_release_empty_string_is_false():
    assert is_known_release("") is False


# --- check_minimum_version() ---

def test_check_minimum_version_170_is_true():
    assert check_minimum_version("1.7.0") is True


def test_check_minimum_version_183_is_true():
    assert check_minimum_version("1.8.3") is True


def test_check_minimum_version_190_is_false():
    assert check_minimum_version("1.9.0") is False
