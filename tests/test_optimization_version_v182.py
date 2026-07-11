"""
tests/test_optimization_version_v182.py
Tests for optimization version module v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.optimization_version_v182 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    INCLUDED_RELEASES, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH_CHECKS,
    KNOWN_RELEASE_NAMES, get_version_info, verify_version, is_known_release,
    check_minimum_version,
)


# --- VERSION ---
def test_version_is_182():
    assert VERSION == "1.8.2"

def test_version_type_str():
    assert isinstance(VERSION, str)

def test_version_not_empty():
    assert len(VERSION) > 0


# --- RELEASE_NAME ---
def test_release_name():
    assert RELEASE_NAME == "Parameter Optimization & Walk-Forward Validation Lab"

def test_release_name_contains_optimization():
    assert "Optimization" in RELEASE_NAME

def test_release_name_contains_walk_forward():
    assert "Walk-Forward" in RELEASE_NAME

def test_release_name_not_empty():
    assert len(RELEASE_NAME) > 0


# --- BASE_RELEASE ---
def test_base_release():
    assert BASE_RELEASE == "v1.8.1-simulation-scenario-matrix-stress-test-lab"

def test_base_release_contains_181():
    assert "1.8.1" in BASE_RELEASE


# --- SCHEMA_VERSION ---
def test_schema_version():
    assert SCHEMA_VERSION == "182"

def test_schema_version_str():
    assert isinstance(SCHEMA_VERSION, str)


# --- POLICY_VERSION ---
def test_policy_version():
    assert POLICY_VERSION == "1.8.2-small-capital-strategy-parameter-optimization"

def test_policy_version_contains_182():
    assert "1.8.2" in POLICY_VERSION

def test_policy_version_contains_optimization():
    assert "optimization" in POLICY_VERSION


# --- INCLUDED_RELEASES ---
def test_included_releases_count():
    assert len(INCLUDED_RELEASES) == 12

def test_included_releases_type():
    assert isinstance(INCLUDED_RELEASES, list)

def test_included_releases_v170():
    assert "Small Capital Strategy v1.7.0" in INCLUDED_RELEASES

def test_included_releases_v171():
    assert "Watchlist Strategy Layer v1.7.1" in INCLUDED_RELEASES

def test_included_releases_v172():
    assert "A/B/C Buy Point Execution Plan v1.7.2" in INCLUDED_RELEASES

def test_included_releases_v173():
    assert "Market Regime Position Control v1.7.3" in INCLUDED_RELEASES

def test_included_releases_v175():
    assert "Small Account Trade Journal v1.7.5" in INCLUDED_RELEASES

def test_included_releases_v176():
    assert "Mistake Taxonomy Review Dashboard v1.7.6" in INCLUDED_RELEASES

def test_included_releases_v177():
    assert "Theme Rotation Scanner v1.7.7" in INCLUDED_RELEASES

def test_included_releases_v178():
    assert "Small Capital Strategy Integration v1.7.8" in INCLUDED_RELEASES

def test_included_releases_v179():
    assert "Small Capital Strategy Stable Rollup v1.7.9" in INCLUDED_RELEASES

def test_included_releases_v180():
    assert "Paper Simulation & Performance Lab v1.8.0" in INCLUDED_RELEASES

def test_included_releases_v181():
    assert "Simulation Scenario Matrix & Stress Test Lab v1.8.1" in INCLUDED_RELEASES

def test_included_releases_v182():
    assert "Parameter Optimization & Walk-Forward Validation Lab v1.8.2" in INCLUDED_RELEASES


# --- MIN_* ---
def test_min_scenarios():
    assert MIN_SCENARIOS == 75

def test_min_fixtures():
    assert MIN_FIXTURES == 75

def test_min_cli():
    assert MIN_CLI == 17

def test_min_health_checks():
    assert MIN_HEALTH_CHECKS == 60


# --- KNOWN_RELEASE_NAMES ---
def test_known_release_names_count():
    assert len(KNOWN_RELEASE_NAMES) == 12

def test_known_release_names_type():
    assert isinstance(KNOWN_RELEASE_NAMES, list)

def test_known_release_v170():
    assert "Small Capital Strategy v1.7.0" in KNOWN_RELEASE_NAMES

def test_known_release_v182():
    assert "Parameter Optimization & Walk-Forward Validation Lab v1.8.2" in KNOWN_RELEASE_NAMES

def test_known_release_all_strings():
    assert all(isinstance(n, str) for n in KNOWN_RELEASE_NAMES)


# --- get_version_info() ---
def test_get_version_info_returns_dict():
    info = get_version_info()
    assert isinstance(info, dict)

def test_get_version_info_version():
    assert get_version_info()["version"] == "1.8.2"

def test_get_version_info_release_name():
    assert get_version_info()["release_name"] == RELEASE_NAME

def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True

def test_get_version_info_research_only():
    assert get_version_info()["research_only"] is True

def test_get_version_info_simulate_only():
    assert get_version_info()["simulate_only"] is True

def test_get_version_info_validation_only():
    assert get_version_info()["validation_only"] is True

def test_get_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True

def test_get_version_info_not_investment_advice():
    assert get_version_info()["not_investment_advice"] is True

def test_get_version_info_no_broker():
    assert get_version_info()["no_broker"] is True

def test_get_version_info_schema_version():
    assert get_version_info()["schema_version"] == "182"

def test_get_version_info_policy_version():
    assert get_version_info()["policy_version"] == POLICY_VERSION


# --- verify_version() ---
def test_verify_version_true():
    assert verify_version() is True

def test_verify_version_returns_bool():
    assert isinstance(verify_version(), bool)


# --- is_known_release() ---
def test_is_known_release_v182():
    assert is_known_release("Parameter Optimization & Walk-Forward Validation Lab v1.8.2") is True

def test_is_known_release_v170():
    assert is_known_release("Small Capital Strategy v1.7.0") is True

def test_is_known_release_unknown():
    assert is_known_release("Unknown Release v9.9.9") is False

def test_is_known_release_empty():
    assert is_known_release("") is False


# --- check_minimum_version() ---
def test_check_minimum_version_170():
    assert check_minimum_version("1.7.0") is True

def test_check_minimum_version_182():
    assert check_minimum_version("1.8.2") is True

def test_check_minimum_version_190():
    assert check_minimum_version("1.9.0") is False

def test_check_minimum_version_100():
    assert check_minimum_version("1.0.0") is True
