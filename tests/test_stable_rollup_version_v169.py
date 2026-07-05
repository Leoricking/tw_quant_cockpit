"""
tests/test_stable_rollup_version_v169.py
Tests for version_v169 module.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from paper_trading.stable_rollup.version_v169 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
    ACCEPTED_MINIMUM_VERSION, KNOWN_RELEASE_NAMES,
    get_version_info, is_known_release, check_minimum_version,
)


def test_version_is_169():
    assert VERSION == "1.6.9"


def test_release_name():
    assert RELEASE_NAME == "Live Paper Trading Stable Rollup"


def test_base_release():
    assert BASE_RELEASE == "1.6.8 Operational Integration Hardening"


def test_schema_version():
    assert SCHEMA_VERSION == "169"


def test_policy_version():
    assert POLICY_VERSION == "1.6.9-live-paper-stable-rollup"


def test_component_count():
    assert COMPONENT_COUNT == 32


def test_min_scenarios():
    assert MIN_SCENARIOS == 80


def test_min_fixtures():
    assert MIN_FIXTURES == 80


def test_min_cli():
    assert MIN_CLI == 26


def test_min_health():
    assert MIN_HEALTH == 80


def test_min_gate():
    assert MIN_GATE == 70


def test_accepted_minimum_version():
    assert ACCEPTED_MINIMUM_VERSION == "1.6.8"


def test_known_release_names_is_frozenset():
    assert isinstance(KNOWN_RELEASE_NAMES, frozenset)


def test_known_release_names_contains_169():
    assert "Live Paper Trading Stable Rollup" in KNOWN_RELEASE_NAMES


def test_known_release_names_contains_168():
    assert "Operational Integration Hardening" in KNOWN_RELEASE_NAMES


def test_known_release_names_min_count():
    assert len(KNOWN_RELEASE_NAMES) >= 10


def test_get_version_info_returns_dict():
    info = get_version_info()
    assert isinstance(info, dict)


def test_get_version_info_version_key():
    info = get_version_info()
    assert info["version"] == "1.6.9"


def test_get_version_info_paper_only():
    info = get_version_info()
    assert info["paper_only"] is True


def test_get_version_info_no_real_orders():
    info = get_version_info()
    assert info["no_real_orders"] is True


def test_is_known_release_true():
    assert is_known_release("Live Paper Trading Stable Rollup") is True


def test_is_known_release_false():
    assert is_known_release("Unknown Release XYZ") is False


def test_check_minimum_version_169():
    assert check_minimum_version("1.6.9") is True


def test_check_minimum_version_168():
    assert check_minimum_version("1.6.8") is True


def test_check_minimum_version_167_false():
    assert check_minimum_version("1.6.7") is False


def test_check_minimum_version_invalid():
    result = check_minimum_version("not.a.version")
    assert isinstance(result, bool)
