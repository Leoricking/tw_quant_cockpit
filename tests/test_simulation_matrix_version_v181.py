"""
tests/test_simulation_matrix_version_v181.py
Tests for simulation_matrix_version_v181 — Simulation Scenario Matrix & Stress Test Lab v1.8.1.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.simulation_matrix_version_v181 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    INCLUDED_RELEASES, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    KNOWN_RELEASE_NAMES,
    get_version_info, verify_version, is_known_release, check_minimum_version,
)


# ── Version constants ──────────────────────────────────────────────────────────

def test_version_is_181():
    assert VERSION == "1.8.1"

def test_version_has_three_parts():
    assert len(VERSION.split(".")) == 3

def test_version_parts_are_digits():
    assert all(p.isdigit() for p in VERSION.split("."))

def test_release_name():
    assert RELEASE_NAME == "Simulation Scenario Matrix & Stress Test Lab"

def test_base_release():
    assert BASE_RELEASE == "1.8.0 Paper Simulation & Performance Lab"

def test_schema_version():
    assert SCHEMA_VERSION == "181"

def test_policy_version():
    assert POLICY_VERSION == "1.8.1-simulation-scenario-matrix-stress-test"

def test_policy_version_starts_with_181():
    assert POLICY_VERSION.startswith("1.8.1")

def test_policy_version_contains_simulation():
    assert "simulation" in POLICY_VERSION

def test_policy_version_contains_matrix():
    assert "matrix" in POLICY_VERSION

def test_policy_version_contains_stress():
    assert "stress" in POLICY_VERSION


# ── Minimums ───────────────────────────────────────────────────────────────────

def test_min_scenarios_ge_75():
    assert MIN_SCENARIOS >= 75

def test_min_fixtures_ge_75():
    assert MIN_FIXTURES >= 75

def test_min_cli_ge_20():
    assert MIN_CLI >= 20

def test_min_health_ge_55():
    assert MIN_HEALTH >= 55

def test_min_gate_ge_55():
    assert MIN_GATE >= 55

def test_min_scenarios_equals_75():
    assert MIN_SCENARIOS == 75

def test_min_fixtures_equals_75():
    assert MIN_FIXTURES == 75

def test_min_cli_equals_20():
    assert MIN_CLI == 20


# ── Included releases ──────────────────────────────────────────────────────────

def test_included_releases_is_list():
    assert isinstance(INCLUDED_RELEASES, list)

def test_included_releases_contains_v170():
    assert "v1.7.0" in INCLUDED_RELEASES

def test_included_releases_contains_v179():
    assert "v1.7.9" in INCLUDED_RELEASES

def test_included_releases_contains_v180():
    assert "v1.8.0" in INCLUDED_RELEASES

def test_included_releases_ge_11():
    assert len(INCLUDED_RELEASES) >= 11

def test_included_releases_v171():
    assert "v1.7.1" in INCLUDED_RELEASES

def test_included_releases_v172():
    assert "v1.7.2" in INCLUDED_RELEASES

def test_included_releases_v173():
    assert "v1.7.3" in INCLUDED_RELEASES

def test_included_releases_v174():
    assert "v1.7.4" in INCLUDED_RELEASES

def test_included_releases_v175():
    assert "v1.7.5" in INCLUDED_RELEASES

def test_included_releases_v176():
    assert "v1.7.6" in INCLUDED_RELEASES

def test_included_releases_v177():
    assert "v1.7.7" in INCLUDED_RELEASES

def test_included_releases_v178():
    assert "v1.7.8" in INCLUDED_RELEASES


# ── Known release names ────────────────────────────────────────────────────────

def test_known_releases_is_frozenset():
    assert isinstance(KNOWN_RELEASE_NAMES, frozenset)

def test_known_releases_contains_current():
    assert "Simulation Scenario Matrix & Stress Test Lab" in KNOWN_RELEASE_NAMES

def test_known_releases_contains_paper_sim():
    assert "Paper Simulation & Performance Lab" in KNOWN_RELEASE_NAMES

def test_known_releases_ge_10():
    assert len(KNOWN_RELEASE_NAMES) >= 10


# ── get_version_info() ─────────────────────────────────────────────────────────

def test_get_version_info_is_dict():
    assert isinstance(get_version_info(), dict)

def test_get_version_info_version():
    assert get_version_info()["version"] == "1.8.1"

def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True

def test_get_version_info_research_only():
    assert get_version_info()["research_only"] is True

def test_get_version_info_simulate_only():
    assert get_version_info()["simulate_only"] is True

def test_get_version_info_stress_test_only():
    assert get_version_info()["stress_test_only"] is True

def test_get_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True

def test_get_version_info_not_investment_advice():
    assert get_version_info()["not_investment_advice"] is True

def test_get_version_info_demo_only():
    assert get_version_info()["demo_only"] is True

def test_get_version_info_not_for_production():
    assert get_version_info()["not_for_production"] is True

def test_get_version_info_min_scenarios():
    assert get_version_info()["min_scenarios"] >= 75

def test_get_version_info_min_fixtures():
    assert get_version_info()["min_fixtures"] >= 75

def test_get_version_info_min_cli():
    assert get_version_info()["min_cli"] >= 20

def test_get_version_info_schema_version():
    assert get_version_info()["schema_version"] == "181"

def test_get_version_info_policy_version():
    assert "stress-test" in get_version_info()["policy_version"]

def test_get_version_info_included_releases():
    info = get_version_info()
    assert "v1.8.0" in info["included_releases"]


# ── verify_version() ───────────────────────────────────────────────────────────

def test_verify_version_returns_true():
    assert verify_version() is True

def test_verify_version_type_is_bool():
    assert isinstance(verify_version(), bool)


# ── is_known_release() ─────────────────────────────────────────────────────────

def test_is_known_release_current():
    assert is_known_release("Simulation Scenario Matrix & Stress Test Lab") is True

def test_is_known_release_paper_sim():
    assert is_known_release("Paper Simulation & Performance Lab") is True

def test_is_known_release_unknown():
    assert is_known_release("Unknown Release XYZ") is False

def test_is_known_release_empty():
    assert is_known_release("") is False


# ── check_minimum_version() ────────────────────────────────────────────────────

def test_check_minimum_version_same():
    assert check_minimum_version("1.8.1") is True

def test_check_minimum_version_higher():
    assert check_minimum_version("2.0.0") is True

def test_check_minimum_version_lower():
    assert check_minimum_version("1.7.9") is False

def test_check_minimum_version_lower_minor():
    assert check_minimum_version("1.8.0") is False

def test_check_minimum_version_invalid():
    assert check_minimum_version("not-a-version") is False
