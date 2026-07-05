"""
tests/test_stable_rollup_safety_matrix_v169.py
Tests for safety_matrix_v169 module.
"""
import pytest
from paper_trading.stable_rollup.safety_matrix_v169 import (
    SAFETY_MATRIX, get_matrix, get_safety_item, validate_matrix, count_dangerous_capabilities,
)


def test_matrix_is_list():
    assert isinstance(SAFETY_MATRIX, list)


def test_matrix_count_ge_20():
    assert len(SAFETY_MATRIX) >= 20


def test_get_matrix_returns_list():
    m = get_matrix()
    assert isinstance(m, list)


def test_get_matrix_returns_copy():
    m1 = get_matrix()
    m2 = get_matrix()
    assert m1 is not m2


def test_all_actual_states_disabled_or_blocked():
    for item in get_matrix():
        assert item["actual_state"] in ("DISABLED", "BLOCKED"), \
            f"{item['capability']} actual_state={item['actual_state']}"


def test_all_executable_capability_found_false():
    for item in get_matrix():
        assert item["executable_capability_found"] is False, \
            f"{item['capability']} executable_capability_found=True"


def test_all_status_safe():
    for item in get_matrix():
        assert item["status"] == "SAFE", f"{item['capability']} status={item['status']}"


def test_real_trading_present():
    item = get_safety_item("real_trading")
    assert item is not None
    assert item["actual_state"] == "DISABLED"


def test_broker_present():
    item = get_safety_item("broker")
    assert item is not None
    assert item["actual_state"] == "DISABLED"


def test_shioaji_present():
    item = get_safety_item("shioaji")
    assert item is not None
    assert item["actual_state"] == "BLOCKED"


def test_credential_access_present():
    item = get_safety_item("credential_access")
    assert item is not None
    assert item["actual_state"] == "BLOCKED"


def test_get_safety_item_nonexistent():
    item = get_safety_item("nonexistent_xyz")
    assert item is None


def test_validate_matrix_pass():
    result = validate_matrix()
    assert result["status"] == "PASS"
    assert result["issues"] == []


def test_validate_matrix_total():
    result = validate_matrix()
    assert result["total"] >= 20


def test_count_dangerous_capabilities_zero():
    n = count_dangerous_capabilities()
    assert n == 0


def test_unique_capabilities():
    names = [item["capability"] for item in get_matrix()]
    assert len(set(names)) == len(names)


def test_deterministic_order():
    m1 = [item["capability"] for item in get_matrix()]
    m2 = [item["capability"] for item in get_matrix()]
    assert m1 == m2
