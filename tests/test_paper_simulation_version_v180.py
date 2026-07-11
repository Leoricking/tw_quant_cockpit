"""tests/test_paper_simulation_version_v180.py — v1.8.0 Paper Simulation version tests"""
from __future__ import annotations
import pytest
from paper_trading.small_capital_strategy.paper_simulation_version_v180 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    INCLUDED_RELEASES, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    KNOWN_RELEASE_NAMES, get_version_info, verify_version, is_known_release,
    check_minimum_version,
)


# ---------------------------------------------------------------------------
# VERSION constant
# ---------------------------------------------------------------------------

def test_version_equals_180():
    assert VERSION == "1.8.0"


def test_version_is_string():
    assert isinstance(VERSION, str)


def test_version_has_three_parts():
    parts = VERSION.split(".")
    assert len(parts) == 3


def test_version_parts_are_digits():
    parts = VERSION.split(".")
    assert all(p.isdigit() for p in parts)


# ---------------------------------------------------------------------------
# RELEASE_NAME constant
# ---------------------------------------------------------------------------

def test_release_name_value():
    assert RELEASE_NAME == "Paper Simulation & Performance Lab"


def test_release_name_is_string():
    assert isinstance(RELEASE_NAME, str)


def test_release_name_not_empty():
    assert len(RELEASE_NAME) > 0


# ---------------------------------------------------------------------------
# BASE_RELEASE constant
# ---------------------------------------------------------------------------

def test_base_release_value():
    assert BASE_RELEASE == "1.7.9 Small Capital Strategy Stable Rollup"


def test_base_release_is_string():
    assert isinstance(BASE_RELEASE, str)


def test_base_release_contains_179():
    assert "1.7.9" in BASE_RELEASE


# ---------------------------------------------------------------------------
# SCHEMA_VERSION constant
# ---------------------------------------------------------------------------

def test_schema_version_value():
    assert SCHEMA_VERSION == "180"


def test_schema_version_is_string():
    assert isinstance(SCHEMA_VERSION, str)


# ---------------------------------------------------------------------------
# POLICY_VERSION constant
# ---------------------------------------------------------------------------

def test_policy_version_contains_180():
    assert "1.8.0" in POLICY_VERSION


def test_policy_version_is_string():
    assert isinstance(POLICY_VERSION, str)


def test_policy_version_not_empty():
    assert len(POLICY_VERSION) > 0


# ---------------------------------------------------------------------------
# Minimum threshold constants
# ---------------------------------------------------------------------------

def test_min_scenarios_equals_70():
    assert MIN_SCENARIOS == 70


def test_min_fixtures_equals_70():
    assert MIN_FIXTURES == 70


def test_min_cli_equals_19():
    assert MIN_CLI == 19


def test_min_health_at_least_50():
    assert MIN_HEALTH >= 50


def test_min_gate_at_least_50():
    assert MIN_GATE >= 50


# ---------------------------------------------------------------------------
# INCLUDED_RELEASES
# ---------------------------------------------------------------------------

def test_included_releases_is_list():
    assert isinstance(INCLUDED_RELEASES, list)


def test_included_releases_has_v170():
    assert "v1.7.0" in INCLUDED_RELEASES


def test_included_releases_has_v179():
    assert "v1.7.9" in INCLUDED_RELEASES


def test_included_releases_has_all_v17x():
    for minor in range(10):
        assert f"v1.7.{minor}" in INCLUDED_RELEASES


def test_included_releases_length():
    assert len(INCLUDED_RELEASES) >= 10


# ---------------------------------------------------------------------------
# KNOWN_RELEASE_NAMES
# ---------------------------------------------------------------------------

def test_known_release_names_is_frozenset():
    assert isinstance(KNOWN_RELEASE_NAMES, frozenset)


def test_known_release_names_has_at_least_10():
    assert len(KNOWN_RELEASE_NAMES) >= 10


def test_known_release_names_contains_current():
    assert "Paper Simulation & Performance Lab" in KNOWN_RELEASE_NAMES


def test_known_release_names_contains_stable_rollup():
    assert "Small Capital Strategy Stable Rollup" in KNOWN_RELEASE_NAMES


def test_known_release_names_contains_theme_rotation():
    assert "Theme Rotation Scanner" in KNOWN_RELEASE_NAMES


# ---------------------------------------------------------------------------
# get_version_info()
# ---------------------------------------------------------------------------

def test_get_version_info_returns_dict():
    info = get_version_info()
    assert isinstance(info, dict)


def test_get_version_info_paper_only():
    info = get_version_info()
    assert info["paper_only"] is True


def test_get_version_info_research_only():
    info = get_version_info()
    assert info["research_only"] is True


def test_get_version_info_no_real_orders():
    info = get_version_info()
    assert info["no_real_orders"] is True


def test_get_version_info_version_key():
    info = get_version_info()
    assert info["version"] == "1.8.0"


def test_get_version_info_schema_version_key():
    info = get_version_info()
    assert info["schema_version"] == "180"


def test_get_version_info_min_scenarios_key():
    info = get_version_info()
    assert info["min_scenarios"] == MIN_SCENARIOS


def test_get_version_info_not_investment_advice():
    info = get_version_info()
    assert info["not_investment_advice"] is True


def test_get_version_info_demo_only():
    info = get_version_info()
    assert info["demo_only"] is True


def test_get_version_info_not_for_production():
    info = get_version_info()
    assert info["not_for_production"] is True


# ---------------------------------------------------------------------------
# verify_version()
# ---------------------------------------------------------------------------

def test_verify_version_returns_true():
    assert verify_version() is True


def test_verify_version_returns_bool():
    result = verify_version()
    assert isinstance(result, bool)


# ---------------------------------------------------------------------------
# is_known_release()
# ---------------------------------------------------------------------------

def test_is_known_release_current_name():
    assert is_known_release("Paper Simulation & Performance Lab") is True


def test_is_known_release_fake_returns_false():
    assert is_known_release("FAKE_RELEASE_XYZ") is False


def test_is_known_release_empty_string():
    assert is_known_release("") is False


def test_is_known_release_returns_bool():
    result = is_known_release("Paper Simulation & Performance Lab")
    assert isinstance(result, bool)


# ---------------------------------------------------------------------------
# check_minimum_version()
# ---------------------------------------------------------------------------

def test_check_minimum_version_same_version():
    # ver == VERSION: True (ver >= VERSION)
    assert check_minimum_version("1.8.0") is True


def test_check_minimum_version_higher_returns_true():
    # ver > VERSION: True (ver >= VERSION)
    assert check_minimum_version("1.9.0") is True


def test_check_minimum_version_lower_returns_false():
    # ver < VERSION: False (ver < VERSION)
    assert check_minimum_version("1.7.0") is False


def test_check_minimum_version_returns_bool():
    result = check_minimum_version("1.8.0")
    assert isinstance(result, bool)


def test_check_minimum_version_very_old_returns_false():
    # ver much lower than VERSION: False
    assert check_minimum_version("1.0.0") is False


def test_check_minimum_version_future_returns_true():
    # ver > VERSION: True
    assert check_minimum_version("2.0.0") is True
