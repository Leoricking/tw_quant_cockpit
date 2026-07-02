"""
paper_trading/performance_attribution/safety_v167.py
Safety enforcement for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Real/live/production mode must not fallback to fixture/mock/offline.
[!] Must explicitly refuse or return unsupported/blocked.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

# ── Safety flag declarations ──────────────────────────────────────────────────
PAPER_ATTRIBUTION_AVAILABLE              = True
PAPER_ATTRIBUTION_RESEARCH_ONLY         = True
PAPER_ATTRIBUTION_PAPER_ONLY            = True
PAPER_ATTRIBUTION_DETERMINISTIC         = True
PAPER_ATTRIBUTION_READ_ONLY             = True

REAL_PERFORMANCE_ATTRIBUTION_ENABLED    = False
BROKER_ATTRIBUTION_ENABLED              = False
REAL_ACCOUNT_ATTRIBUTION_ENABLED        = False
REAL_ORDER_ATTRIBUTION_ENABLED          = False
PRODUCTION_LEDGER_ATTRIBUTION_ENABLED   = False
LIVE_EXECUTION_ATTRIBUTION_ENABLED      = False
PRODUCTION_PORTFOLIO_ATTRIBUTION_ENABLED = False
AUTO_CAPITAL_REALLOCATION_ENABLED       = False
AUTO_RISK_OVERRIDE_ENABLED              = False
AUTO_SESSION_CONTROL_ENABLED            = False
EXTERNAL_ATTRIBUTION_SERVICE_ENABLED    = False
EXTERNAL_ATTRIBUTION_DB_ENABLED         = False
NETWORK_ATTRIBUTION_ENABLED             = False

NO_REAL_ORDERS_CONST                    = True
BROKER_EXECUTION_ENABLED                = False
PRODUCTION_TRADING_BLOCKED              = True

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


def validate_attribution_safety(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that an attribution input/config dict contains no forbidden fields,
    real/live markers, or production flags.
    Returns {"safe": bool, "violations": List[str], "blocked": bool}.
    If violations found, return blocked=True.
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


def assert_paper_only() -> None:
    """Raise ValueError if any real/production flag is enabled. Called at module-level."""
    assert REAL_PERFORMANCE_ATTRIBUTION_ENABLED is False, "BLOCKED: real attribution"
    assert BROKER_ATTRIBUTION_ENABLED is False, "BLOCKED: broker attribution"
    assert REAL_ACCOUNT_ATTRIBUTION_ENABLED is False, "BLOCKED: real account"
    assert LIVE_EXECUTION_ATTRIBUTION_ENABLED is False, "BLOCKED: live execution"
    assert PRODUCTION_LEDGER_ATTRIBUTION_ENABLED is False, "BLOCKED: production ledger"
    assert PRODUCTION_TRADING_BLOCKED is True, "BLOCKED: production trading"


def get_safety_flags() -> Dict[str, Any]:
    """Return all safety flag values as a dict. Deterministic."""
    return {
        "PAPER_ATTRIBUTION_AVAILABLE": PAPER_ATTRIBUTION_AVAILABLE,
        "PAPER_ATTRIBUTION_RESEARCH_ONLY": PAPER_ATTRIBUTION_RESEARCH_ONLY,
        "PAPER_ATTRIBUTION_PAPER_ONLY": PAPER_ATTRIBUTION_PAPER_ONLY,
        "PAPER_ATTRIBUTION_DETERMINISTIC": PAPER_ATTRIBUTION_DETERMINISTIC,
        "PAPER_ATTRIBUTION_READ_ONLY": PAPER_ATTRIBUTION_READ_ONLY,
        "REAL_PERFORMANCE_ATTRIBUTION_ENABLED": REAL_PERFORMANCE_ATTRIBUTION_ENABLED,
        "BROKER_ATTRIBUTION_ENABLED": BROKER_ATTRIBUTION_ENABLED,
        "REAL_ACCOUNT_ATTRIBUTION_ENABLED": REAL_ACCOUNT_ATTRIBUTION_ENABLED,
        "REAL_ORDER_ATTRIBUTION_ENABLED": REAL_ORDER_ATTRIBUTION_ENABLED,
        "PRODUCTION_LEDGER_ATTRIBUTION_ENABLED": PRODUCTION_LEDGER_ATTRIBUTION_ENABLED,
        "LIVE_EXECUTION_ATTRIBUTION_ENABLED": LIVE_EXECUTION_ATTRIBUTION_ENABLED,
        "PRODUCTION_PORTFOLIO_ATTRIBUTION_ENABLED": PRODUCTION_PORTFOLIO_ATTRIBUTION_ENABLED,
        "AUTO_CAPITAL_REALLOCATION_ENABLED": AUTO_CAPITAL_REALLOCATION_ENABLED,
        "AUTO_RISK_OVERRIDE_ENABLED": AUTO_RISK_OVERRIDE_ENABLED,
        "AUTO_SESSION_CONTROL_ENABLED": AUTO_SESSION_CONTROL_ENABLED,
        "EXTERNAL_ATTRIBUTION_SERVICE_ENABLED": EXTERNAL_ATTRIBUTION_SERVICE_ENABLED,
        "EXTERNAL_ATTRIBUTION_DB_ENABLED": EXTERNAL_ATTRIBUTION_DB_ENABLED,
        "NETWORK_ATTRIBUTION_ENABLED": NETWORK_ATTRIBUTION_ENABLED,
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
    blocked_correct = [
        not flags["REAL_PERFORMANCE_ATTRIBUTION_ENABLED"],
        not flags["BROKER_ATTRIBUTION_ENABLED"],
        not flags["REAL_ACCOUNT_ATTRIBUTION_ENABLED"],
        not flags["REAL_ORDER_ATTRIBUTION_ENABLED"],
        not flags["PRODUCTION_LEDGER_ATTRIBUTION_ENABLED"],
        not flags["LIVE_EXECUTION_ATTRIBUTION_ENABLED"],
        not flags["PRODUCTION_PORTFOLIO_ATTRIBUTION_ENABLED"],
        not flags["AUTO_CAPITAL_REALLOCATION_ENABLED"],
        not flags["AUTO_RISK_OVERRIDE_ENABLED"],
        not flags["AUTO_SESSION_CONTROL_ENABLED"],
        not flags["EXTERNAL_ATTRIBUTION_SERVICE_ENABLED"],
        not flags["EXTERNAL_ATTRIBUTION_DB_ENABLED"],
        not flags["NETWORK_ATTRIBUTION_ENABLED"],
        not flags["BROKER_EXECUTION_ENABLED"],
        flags["PRODUCTION_TRADING_BLOCKED"],
        flags["PAPER_ATTRIBUTION_AVAILABLE"],
        flags["PAPER_ATTRIBUTION_RESEARCH_ONLY"],
        flags["PAPER_ATTRIBUTION_PAPER_ONLY"],
        flags["PAPER_ATTRIBUTION_DETERMINISTIC"],
        flags["PAPER_ATTRIBUTION_READ_ONLY"],
        flags["NO_REAL_ORDERS"],
    ]
    safety_capabilities = sum(1 for v in [
        flags["REAL_PERFORMANCE_ATTRIBUTION_ENABLED"],
        flags["BROKER_ATTRIBUTION_ENABLED"],
        flags["REAL_ACCOUNT_ATTRIBUTION_ENABLED"],
        flags["REAL_ORDER_ATTRIBUTION_ENABLED"],
        flags["PRODUCTION_LEDGER_ATTRIBUTION_ENABLED"],
        flags["LIVE_EXECUTION_ATTRIBUTION_ENABLED"],
        flags["PRODUCTION_PORTFOLIO_ATTRIBUTION_ENABLED"],
        flags["AUTO_CAPITAL_REALLOCATION_ENABLED"],
        flags["AUTO_RISK_OVERRIDE_ENABLED"],
        flags["AUTO_SESSION_CONTROL_ENABLED"],
        flags["EXTERNAL_ATTRIBUTION_SERVICE_ENABLED"],
        flags["EXTERNAL_ATTRIBUTION_DB_ENABLED"],
        flags["NETWORK_ATTRIBUTION_ENABLED"],
        flags["BROKER_EXECUTION_ENABLED"],
    ] if v is True)
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
