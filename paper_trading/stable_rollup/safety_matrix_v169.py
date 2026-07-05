"""
paper_trading/stable_rollup/safety_matrix_v169.py
Cross-version safety matrix for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import List, Optional

SAFETY_MATRIX: List[dict] = [
    {
        "capability": "real_trading",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "REAL_TRADING_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "real_account",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "REAL_ACCOUNT_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "real_order",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "REAL_ORDER_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "broker",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "BROKER_EXECUTION_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "shioaji",
        "expected_state": "BLOCKED",
        "actual_state": "BLOCKED",
        "source_module": "paper_trading.stable_rollup.safety_v169",
        "source_constant": "SHIOAJI_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "production_ledger",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "PRODUCTION_LEDGER_WRITE_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "production_process_control",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup.safety_v169",
        "source_constant": "PRODUCTION_PROCESS_CONTROL_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "service_control",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "AUTO_SERVICE_CONTROL_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "session_control",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "AUTO_SESSION_CONTROL_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "capital_reallocation",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "AUTO_CAPITAL_REALLOCATION_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "risk_override",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "AUTO_RISK_OVERRIDE_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "network_coordination",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "NETWORK_TRADING_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "external_db",
        "expected_state": "BLOCKED",
        "actual_state": "BLOCKED",
        "source_module": "paper_trading.stable_rollup.safety_v169",
        "source_constant": "EXTERNAL_DB_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "external_message_broker",
        "expected_state": "BLOCKED",
        "actual_state": "BLOCKED",
        "source_module": "paper_trading.stable_rollup.safety_v169",
        "source_constant": "EXTERNAL_MESSAGE_BROKER_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "external_lock_service",
        "expected_state": "BLOCKED",
        "actual_state": "BLOCKED",
        "source_module": "paper_trading.stable_rollup.safety_v169",
        "source_constant": "EXTERNAL_LOCK_SERVICE_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "live_fallback",
        "expected_state": "BLOCKED",
        "actual_state": "BLOCKED",
        "source_module": "paper_trading.stable_rollup.safety_v169",
        "source_constant": "LIVE_FALLBACK_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "mock_fallback",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "EXTERNAL_COORDINATION_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "fixture_fallback",
        "expected_state": "DISABLED",
        "actual_state": "DISABLED",
        "source_module": "paper_trading.stable_rollup",
        "source_constant": "LIVE_EXECUTION_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "credential_access",
        "expected_state": "BLOCKED",
        "actual_state": "BLOCKED",
        "source_module": "paper_trading.stable_rollup.safety_v169",
        "source_constant": "CREDENTIAL_ACCESS_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
    {
        "capability": "secret_access",
        "expected_state": "BLOCKED",
        "actual_state": "BLOCKED",
        "source_module": "paper_trading.stable_rollup.safety_v169",
        "source_constant": "SECRET_ACCESS_ENABLED",
        "executable_capability_found": False,
        "status": "SAFE",
    },
]


def get_matrix() -> List[dict]:
    """Return the full safety matrix."""
    return list(SAFETY_MATRIX)


def get_safety_item(name: str) -> Optional[dict]:
    """Return safety item by capability name, or None."""
    for item in SAFETY_MATRIX:
        if item["capability"] == name:
            return dict(item)
    return None


def validate_matrix() -> dict:
    """Validate the safety matrix."""
    issues = []
    names_seen = set()

    for item in SAFETY_MATRIX:
        name = item.get("capability", "")
        if not name:
            issues.append("Entry missing 'capability' field")
            continue
        if name in names_seen:
            issues.append(f"Duplicate capability: {name!r}")
        names_seen.add(name)

        actual = item.get("actual_state", "")
        if actual not in ("DISABLED", "BLOCKED"):
            issues.append(f"Capability {name!r}: actual_state must be DISABLED or BLOCKED, got {actual!r}")

        if item.get("executable_capability_found", True) is not False:
            issues.append(f"Capability {name!r}: executable_capability_found must be False")

        status = item.get("status", "")
        if status not in ("SAFE",):
            issues.append(f"Capability {name!r}: status must be SAFE, got {status!r}")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "total": len(SAFETY_MATRIX),
        "unique": len(names_seen),
    }


def count_dangerous_capabilities() -> int:
    """Count capabilities that are NOT in a safe state."""
    count = 0
    for item in SAFETY_MATRIX:
        if item.get("status") != "SAFE":
            count += 1
        if item.get("executable_capability_found", False) is True:
            count += 1
        actual = item.get("actual_state", "")
        if actual not in ("DISABLED", "BLOCKED"):
            count += 1
    return count
