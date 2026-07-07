"""tests/test_small_capital_version_v170.py — version identity tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.version_v170 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    ACCEPTED_MINIMUM_VERSION, KNOWN_RELEASE_NAMES,
    get_version_info, verify_version, is_known_release, check_minimum_version,
)


def test_version_string():
    assert VERSION == "1.7.0"


def test_release_name():
    assert RELEASE_NAME == "Small Capital Growth Strategy Template"


def test_base_release():
    assert BASE_RELEASE == "1.6.9.1 Stable Rollup Compatibility Hotfix"


def test_schema_version():
    assert SCHEMA_VERSION == "170"


def test_policy_version_contains_version():
    assert "1.7.0" in POLICY_VERSION


def test_component_count():
    assert COMPONENT_COUNT == 28


def test_min_scenarios():
    assert MIN_SCENARIOS == 80


def test_min_fixtures():
    assert MIN_FIXTURES == 80


def test_min_cli():
    assert MIN_CLI == 25


def test_min_health():
    assert MIN_HEALTH == 80


def test_min_gate():
    assert MIN_GATE == 70


def test_accepted_minimum_version():
    assert ACCEPTED_MINIMUM_VERSION == "1.6.9.1"


def test_known_release_names_is_frozenset():
    assert isinstance(KNOWN_RELEASE_NAMES, frozenset)


def test_known_release_names_includes_self():
    assert "Small Capital Growth Strategy Template" in KNOWN_RELEASE_NAMES


def test_known_release_names_includes_v169():
    assert "Live Paper Trading Stable Rollup" in KNOWN_RELEASE_NAMES


def test_known_release_names_includes_v168():
    assert "Operational Integration Hardening" in KNOWN_RELEASE_NAMES


def test_known_release_names_includes_v167():
    assert "Paper Performance Attribution" in KNOWN_RELEASE_NAMES


def test_known_release_names_includes_stable_rollup_hotfix():
    assert "Stable Rollup Compatibility Hotfix" in KNOWN_RELEASE_NAMES


def test_get_version_info_returns_dict():
    info = get_version_info()
    assert isinstance(info, dict)


def test_get_version_info_has_version():
    info = get_version_info()
    assert info["version"] == "1.7.0"


def test_get_version_info_has_release_name():
    info = get_version_info()
    assert info["release_name"] == "Small Capital Growth Strategy Template"


def test_get_version_info_paper_only():
    info = get_version_info()
    assert info["paper_only"] is True


def test_get_version_info_no_real_orders():
    info = get_version_info()
    assert info["no_real_orders"] is True


def test_verify_version_returns_dict():
    info = verify_version()
    assert isinstance(info, dict)


def test_verify_version_has_version():
    info = verify_version()
    assert info["version"] == "1.7.0"


def test_is_known_release_self():
    assert is_known_release("Small Capital Growth Strategy Template") is True


def test_is_known_release_v169():
    assert is_known_release("Live Paper Trading Stable Rollup") is True


def test_is_known_release_unknown_returns_false():
    assert is_known_release("Unknown Release XYZ") is False


def test_check_minimum_version_equal():
    assert check_minimum_version("1.6.9.1") is True


def test_check_minimum_version_self():
    assert check_minimum_version("1.7.0") is True


def test_check_minimum_version_below_returns_false():
    assert check_minimum_version("1.5.0") is False


def test_check_minimum_version_below_169_returns_false():
    assert check_minimum_version("1.6.8") is False
