"""
tests/test_stable_rollup_compatibility_v179.py
Tests for stable_rollup_compatibility_v179 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_compatibility_v179 import (
    check_version_importable,
    run_compatibility_check,
    is_backward_compatible,
    get_compatible_versions,
)


def test_run_compatibility_check_returns_dict():
    result = run_compatibility_check()
    assert isinstance(result, dict)


def test_run_compatibility_check_all_compatible():
    result = run_compatibility_check()
    assert result["all_compatible"] is True


def test_run_compatibility_check_versions_checked_9():
    result = run_compatibility_check()
    assert result["versions_checked"] == 9


def test_run_compatibility_check_paper_only():
    result = run_compatibility_check()
    assert result["paper_only"] is True


def test_run_compatibility_check_no_real_orders():
    result = run_compatibility_check()
    assert result["no_real_orders"] is True


def test_run_compatibility_check_results_is_list():
    result = run_compatibility_check()
    assert isinstance(result["results"], list)


def test_is_backward_compatible_v170():
    assert is_backward_compatible("v1.7.0") is True


def test_is_backward_compatible_v171():
    assert is_backward_compatible("v1.7.1") is True


def test_is_backward_compatible_v172():
    assert is_backward_compatible("v1.7.2") is True


def test_is_backward_compatible_v173():
    assert is_backward_compatible("v1.7.3") is True


def test_is_backward_compatible_v174():
    assert is_backward_compatible("v1.7.4") is True


def test_is_backward_compatible_v175():
    assert is_backward_compatible("v1.7.5") is True


def test_is_backward_compatible_v176():
    assert is_backward_compatible("v1.7.6") is True


def test_is_backward_compatible_v177():
    assert is_backward_compatible("v1.7.7") is True


def test_is_backward_compatible_v178():
    assert is_backward_compatible("v1.7.8") is True


def test_check_version_importable_v170_returns_dict():
    result = check_version_importable("v1.7.0")
    assert isinstance(result, dict)


def test_check_version_importable_v170_importable():
    result = check_version_importable("v1.7.0")
    assert result["importable"] is True


def test_check_version_importable_v170_version_match():
    result = check_version_importable("v1.7.0")
    assert result["version_match"] is True


def test_check_version_importable_v170_safety_ok():
    result = check_version_importable("v1.7.0")
    assert result["safety_ok"] is True


def test_check_version_importable_v178_paper_only():
    result = check_version_importable("v1.7.8")
    assert result["paper_only"] is True


def test_get_compatible_versions_returns_list():
    versions = get_compatible_versions()
    assert isinstance(versions, list)


def test_get_compatible_versions_contains_all_9():
    versions = get_compatible_versions()
    assert len(versions) == 9


def test_get_compatible_versions_contains_v170():
    versions = get_compatible_versions()
    assert "v1.7.0" in versions
