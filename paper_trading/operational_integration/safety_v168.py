"""
paper_trading/operational_integration/safety_v168.py
Safety enforcement for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

# ── Safety flag declarations ──────────────────────────────────────────────────
OPERATIONAL_INTEGRATION_AVAILABLE          = True
OPERATIONAL_INTEGRATION_RESEARCH_ONLY      = True
OPERATIONAL_INTEGRATION_PAPER_ONLY         = True
OPERATIONAL_INTEGRATION_READ_ONLY          = True
OPERATIONAL_INTEGRATION_DETERMINISTIC      = True

REAL_OPERATIONAL_INTEGRATION_ENABLED       = False
BROKER_INTEGRATION_ENABLED                 = False
REAL_ACCOUNT_INTEGRATION_ENABLED           = False
REAL_ORDER_INTEGRATION_ENABLED             = False
PRODUCTION_LEDGER_INTEGRATION_ENABLED      = False
LIVE_EXECUTION_INTEGRATION_ENABLED         = False
AUTO_PROCESS_CONTROL_ENABLED               = False
AUTO_SERVICE_CONTROL_ENABLED               = False
AUTO_SESSION_CONTROL_ENABLED               = False
AUTO_CAPITAL_REALLOCATION_ENABLED          = False
AUTO_RISK_OVERRIDE_ENABLED                 = False
EXTERNAL_COORDINATION_ENABLED              = False
EXTERNAL_MESSAGE_BROKER_ENABLED            = False
EXTERNAL_LOCK_SERVICE_ENABLED              = False
NETWORK_INTEGRATION_ENABLED                = False

NO_REAL_ORDERS_CONST                       = True
BROKER_EXECUTION_ENABLED                   = False
PRODUCTION_TRADING_BLOCKED                 = True

# ── Forbidden field names ─────────────────────────────────────────────────────
_FORBIDDEN_INPUT_FIELDS: frozenset = frozenset({
    "broker_session", "real_account_token", "api_secret", "password",
    "credential", "real_order_handle", "production_db_connection",
    "bank_account", "real_capital_control", "live_execution",
    "shioaji_login", "broker_api_key", "production_ledger",
    "cookie", "token", "api_key",
})

_REAL_LIVE_MARKERS = frozenset({
    "is_live", "is_real", "is_production", "live_mode", "real_mode",
    "production_mode", "broker_mode", "formal_ledger_mode",
})

_PRODUCTION_FLAGS = frozenset({
    "production_trading_enabled", "broker_execution_enabled",
    "real_order_creation_enabled", "real_order_execution_enabled",
    "live_account_sync_enabled", "real_portfolio_ledger_write_enabled",
})


def check_forbidden_fields(data: Dict[str, Any]) -> List[str]:
    """Return list of forbidden field names found in data dict."""
    found = []
    for key in _FORBIDDEN_INPUT_FIELDS:
        if key in data:
            found.append(key)
    return found


def check_real_live_markers(data: Dict[str, Any]) -> List[str]:
    """Return list of real/live marker fields that are True in data."""
    found = []
    for key in _REAL_LIVE_MARKERS:
        if data.get(key) is True:
            found.append(key)
    return found


def check_production_flags(data: Dict[str, Any]) -> List[str]:
    """Return list of production flags that are True in data."""
    found = []
    for key in _PRODUCTION_FLAGS:
        if data.get(key) is True:
            found.append(key)
    return found


def validate_integration_safety(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that an integration input/config dict contains no forbidden fields,
    real/live markers, or production flags.
    Returns {safe, violations, blocked, paper_only, ...}.
    """
    violations: List[str] = []
    forbidden = check_forbidden_fields(data)
    if forbidden:
        violations.extend(f"forbidden_field: {f}" for f in forbidden)
    real_markers = check_real_live_markers(data)
    if real_markers:
        violations.extend(f"real_live_marker: {m}" for m in real_markers)
    prod_flags = check_production_flags(data)
    if prod_flags:
        violations.extend(f"production_flag: {f}" for f in prod_flags)
    safe = len(violations) == 0
    return {
        "safe": safe,
        "blocked": not safe,
        "violations": violations,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_for_production": True,
    }


def assert_integration_paper_only() -> None:
    """Raise AssertionError if any real/production flag is enabled."""
    assert REAL_OPERATIONAL_INTEGRATION_ENABLED is False, "BLOCKED: real integration"
    assert BROKER_INTEGRATION_ENABLED is False, "BLOCKED: broker integration"
    assert REAL_ACCOUNT_INTEGRATION_ENABLED is False, "BLOCKED: real account"
    assert LIVE_EXECUTION_INTEGRATION_ENABLED is False, "BLOCKED: live execution"
    assert PRODUCTION_LEDGER_INTEGRATION_ENABLED is False, "BLOCKED: production ledger"
    assert PRODUCTION_TRADING_BLOCKED is True, "BLOCKED: production trading"
    assert NETWORK_INTEGRATION_ENABLED is False, "BLOCKED: network integration"


def get_safety_flags() -> Dict[str, Any]:
    """Return all safety flag values as a dict. Deterministic."""
    return {
        "OPERATIONAL_INTEGRATION_AVAILABLE": OPERATIONAL_INTEGRATION_AVAILABLE,
        "OPERATIONAL_INTEGRATION_RESEARCH_ONLY": OPERATIONAL_INTEGRATION_RESEARCH_ONLY,
        "OPERATIONAL_INTEGRATION_PAPER_ONLY": OPERATIONAL_INTEGRATION_PAPER_ONLY,
        "OPERATIONAL_INTEGRATION_READ_ONLY": OPERATIONAL_INTEGRATION_READ_ONLY,
        "OPERATIONAL_INTEGRATION_DETERMINISTIC": OPERATIONAL_INTEGRATION_DETERMINISTIC,
        "REAL_OPERATIONAL_INTEGRATION_ENABLED": REAL_OPERATIONAL_INTEGRATION_ENABLED,
        "BROKER_INTEGRATION_ENABLED": BROKER_INTEGRATION_ENABLED,
        "REAL_ACCOUNT_INTEGRATION_ENABLED": REAL_ACCOUNT_INTEGRATION_ENABLED,
        "REAL_ORDER_INTEGRATION_ENABLED": REAL_ORDER_INTEGRATION_ENABLED,
        "PRODUCTION_LEDGER_INTEGRATION_ENABLED": PRODUCTION_LEDGER_INTEGRATION_ENABLED,
        "LIVE_EXECUTION_INTEGRATION_ENABLED": LIVE_EXECUTION_INTEGRATION_ENABLED,
        "AUTO_PROCESS_CONTROL_ENABLED": AUTO_PROCESS_CONTROL_ENABLED,
        "AUTO_SERVICE_CONTROL_ENABLED": AUTO_SERVICE_CONTROL_ENABLED,
        "AUTO_SESSION_CONTROL_ENABLED": AUTO_SESSION_CONTROL_ENABLED,
        "AUTO_CAPITAL_REALLOCATION_ENABLED": AUTO_CAPITAL_REALLOCATION_ENABLED,
        "AUTO_RISK_OVERRIDE_ENABLED": AUTO_RISK_OVERRIDE_ENABLED,
        "EXTERNAL_COORDINATION_ENABLED": EXTERNAL_COORDINATION_ENABLED,
        "EXTERNAL_MESSAGE_BROKER_ENABLED": EXTERNAL_MESSAGE_BROKER_ENABLED,
        "EXTERNAL_LOCK_SERVICE_ENABLED": EXTERNAL_LOCK_SERVICE_ENABLED,
        "NETWORK_INTEGRATION_ENABLED": NETWORK_INTEGRATION_ENABLED,
        "NO_REAL_ORDERS": NO_REAL_ORDERS_CONST,
        "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
        "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
    }


def audit_safety() -> Dict[str, Any]:
    """
    Full safety audit: check all flags, return summary.
    All actual capabilities must be 0 / False.
    """
    flags = get_safety_flags()
    blocked_flags = [
        "REAL_OPERATIONAL_INTEGRATION_ENABLED",
        "BROKER_INTEGRATION_ENABLED",
        "REAL_ACCOUNT_INTEGRATION_ENABLED",
        "REAL_ORDER_INTEGRATION_ENABLED",
        "PRODUCTION_LEDGER_INTEGRATION_ENABLED",
        "LIVE_EXECUTION_INTEGRATION_ENABLED",
        "AUTO_PROCESS_CONTROL_ENABLED",
        "AUTO_SERVICE_CONTROL_ENABLED",
        "AUTO_SESSION_CONTROL_ENABLED",
        "AUTO_CAPITAL_REALLOCATION_ENABLED",
        "AUTO_RISK_OVERRIDE_ENABLED",
        "EXTERNAL_COORDINATION_ENABLED",
        "EXTERNAL_MESSAGE_BROKER_ENABLED",
        "EXTERNAL_LOCK_SERVICE_ENABLED",
        "NETWORK_INTEGRATION_ENABLED",
        "BROKER_EXECUTION_ENABLED",
    ]
    blocked_correct = [not flags[k] for k in blocked_flags]
    blocked_correct += [
        flags["PRODUCTION_TRADING_BLOCKED"],
        flags["OPERATIONAL_INTEGRATION_AVAILABLE"],
        flags["OPERATIONAL_INTEGRATION_RESEARCH_ONLY"],
        flags["OPERATIONAL_INTEGRATION_PAPER_ONLY"],
        flags["OPERATIONAL_INTEGRATION_READ_ONLY"],
        flags["OPERATIONAL_INTEGRATION_DETERMINISTIC"],
        flags["NO_REAL_ORDERS"],
    ]
    safety_capabilities = sum(1 for k in blocked_flags if flags[k] is True)
    all_safe = all(blocked_correct)
    return {
        "all_safe": all_safe,
        "safety_capabilities": safety_capabilities,
        "flags": flags,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_for_production": True,
    }
