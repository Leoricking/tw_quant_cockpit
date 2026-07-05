"""
tests/test_stable_rollup_safety_v169.py
Tests for safety_v169 module.
"""
import pytest
from paper_trading.stable_rollup.safety_v169 import (
    get_safety_flags, validate_safety, is_safe,
    LIVE_PAPER_STABLE_ROLLUP_AVAILABLE, LIVE_PAPER_STABLE_ROLLUP_RESEARCH_ONLY,
    LIVE_PAPER_STABLE_ROLLUP_PAPER_ONLY, LIVE_PAPER_STABLE_ROLLUP_READ_ONLY,
    NO_REAL_ORDERS, PRODUCTION_TRADING_BLOCKED,
    REAL_TRADING_ENABLED, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_ENABLED,
    LIVE_EXECUTION_ENABLED, AUTO_CAPITAL_REALLOCATION_ENABLED,
    NETWORK_TRADING_ENABLED, SHIOAJI_ENABLED, EXTERNAL_DB_ENABLED,
    CREDENTIAL_ACCESS_ENABLED, SECRET_ACCESS_ENABLED, LIVE_FALLBACK_ENABLED,
    SAFETY_CAPABILITY_NAMES,
)


def test_available_true():
    assert LIVE_PAPER_STABLE_ROLLUP_AVAILABLE is True


def test_research_only_true():
    assert LIVE_PAPER_STABLE_ROLLUP_RESEARCH_ONLY is True


def test_paper_only_true():
    assert LIVE_PAPER_STABLE_ROLLUP_PAPER_ONLY is True


def test_read_only_true():
    assert LIVE_PAPER_STABLE_ROLLUP_READ_ONLY is True


def test_no_real_orders_true():
    assert NO_REAL_ORDERS is True


def test_production_trading_blocked_true():
    assert PRODUCTION_TRADING_BLOCKED is True


def test_real_trading_disabled():
    assert REAL_TRADING_ENABLED is False


def test_broker_disabled():
    assert BROKER_EXECUTION_ENABLED is False


def test_production_trading_enabled_false():
    assert PRODUCTION_TRADING_ENABLED is False


def test_live_execution_disabled():
    assert LIVE_EXECUTION_ENABLED is False


def test_auto_capital_reallocation_disabled():
    assert AUTO_CAPITAL_REALLOCATION_ENABLED is False


def test_network_trading_disabled():
    assert NETWORK_TRADING_ENABLED is False


def test_shioaji_disabled():
    assert SHIOAJI_ENABLED is False


def test_external_db_disabled():
    assert EXTERNAL_DB_ENABLED is False


def test_credential_access_disabled():
    assert CREDENTIAL_ACCESS_ENABLED is False


def test_secret_access_disabled():
    assert SECRET_ACCESS_ENABLED is False


def test_live_fallback_disabled():
    assert LIVE_FALLBACK_ENABLED is False


def test_safety_capability_names_is_list():
    assert isinstance(SAFETY_CAPABILITY_NAMES, list)
    assert len(SAFETY_CAPABILITY_NAMES) > 0


def test_get_safety_flags_returns_dict():
    flags = get_safety_flags()
    assert isinstance(flags, dict)
    assert len(flags) > 0


def test_get_safety_flags_contains_no_real_orders():
    flags = get_safety_flags()
    assert "NO_REAL_ORDERS" in flags
    assert flags["NO_REAL_ORDERS"] is True


def test_get_safety_flags_contains_broker():
    flags = get_safety_flags()
    assert "BROKER_EXECUTION_ENABLED" in flags
    assert flags["BROKER_EXECUTION_ENABLED"] is False


def test_validate_safety_returns_dict():
    result = validate_safety()
    assert isinstance(result, dict)
    assert "status" in result
    assert "passed" in result
    assert "failed" in result
    assert "checks" in result


def test_validate_safety_passes():
    result = validate_safety()
    assert result["status"] == "PASS"
    assert result["failed"] == 0


def test_validate_safety_checks_is_list():
    result = validate_safety()
    assert isinstance(result["checks"], list)
    assert len(result["checks"]) > 0


def test_is_safe_returns_true():
    assert is_safe() is True
