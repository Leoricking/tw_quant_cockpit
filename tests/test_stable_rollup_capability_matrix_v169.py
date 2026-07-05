"""
tests/test_stable_rollup_capability_matrix_v169.py
Tests for capability_matrix_v169 module.
"""
import pytest
from paper_trading.stable_rollup.capability_matrix_v169 import (
    CAPABILITY_MATRIX, get_matrix, get_capability, validate_matrix,
)


def test_matrix_is_list():
    assert isinstance(CAPABILITY_MATRIX, list)


def test_matrix_count_ge_19():
    assert len(CAPABILITY_MATRIX) >= 19


def test_get_matrix_returns_list():
    m = get_matrix()
    assert isinstance(m, list)


def test_get_matrix_returns_copy():
    m1 = get_matrix()
    m2 = get_matrix()
    assert m1 is not m2


def test_no_production_ready():
    for cap in get_matrix():
        assert cap.get("production_ready") is False, f"{cap['capability']} has production_ready=True"


def test_all_paper_only():
    for cap in get_matrix():
        assert cap.get("paper_only") is True, f"{cap['capability']} has paper_only=False"


def test_paper_trading_present():
    cap = get_capability("paper_trading")
    assert cap is not None


def test_stable_rollup_present():
    cap = get_capability("stable_rollup")
    assert cap is not None


def test_cli_present():
    cap = get_capability("cli")
    assert cap is not None


def test_gui_present():
    cap = get_capability("gui")
    assert cap is not None


def test_health_present():
    cap = get_capability("health")
    assert cap is not None


def test_gate_present():
    cap = get_capability("gate")
    assert cap is not None


def test_unique_capabilities():
    names = [c["capability"] for c in get_matrix()]
    assert len(set(names)) == len(names)


def test_get_capability_returns_dict():
    cap = get_capability("paper_trading")
    assert isinstance(cap, dict)
    assert "capability" in cap
    assert "introduced_in" in cap


def test_get_capability_nonexistent():
    cap = get_capability("nonexistent_capability_xyz")
    assert cap is None


def test_validate_matrix_pass():
    result = validate_matrix()
    assert result["status"] == "PASS"
    assert result["issues"] == []


def test_validate_matrix_total():
    result = validate_matrix()
    assert result["total"] >= 19


def test_each_cap_has_enhanced_in_list():
    for cap in get_matrix():
        assert isinstance(cap.get("enhanced_in"), list), f"{cap['capability']} enhanced_in not list"


def test_each_cap_has_dependencies_list():
    for cap in get_matrix():
        assert isinstance(cap.get("dependencies"), list), f"{cap['capability']} dependencies not list"


def test_deterministic_order():
    m1 = [c["capability"] for c in get_matrix()]
    m2 = [c["capability"] for c in get_matrix()]
    assert m1 == m2
