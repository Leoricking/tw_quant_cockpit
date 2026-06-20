"""
data/providers/finmind/capabilities_v144.py — FinMind capability registration v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SECONDARY_AGGREGATOR. All capabilities are research-only supplements.
"""
from __future__ import annotations

from typing import Any, Dict, List

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

FINMIND_CAPABILITIES: List[Dict[str, Any]] = [
    {
        "name": "finmind_adapter_hardening",
        "status": "STABLE",
        "version": "1.4.4",
        "description": "FinMind secondary aggregator with API v4, quota, schema drift, conflict detection",
        "research_only": True,
        "allows_formal_conclusion": False,
        "allows_primary_override": False,
        "allows_broker": False,
    },
    {
        "name": "finmind_api_v4",
        "status": "STABLE",
        "version": "1.4.4",
        "description": "API v4 client with injectable transport for offline tests",
        "research_only": True,
    },
    {
        "name": "finmind_token_security",
        "status": "STABLE",
        "version": "1.4.4",
        "description": "Secure token handling: env var only, fingerprint only, never log full token",
        "research_only": True,
    },
    {
        "name": "finmind_quota_manager",
        "status": "STABLE",
        "version": "1.4.4",
        "description": "Quota tracking: request counting, error recording, status reporting",
        "research_only": True,
    },
    {
        "name": "finmind_error_classifier",
        "status": "STABLE",
        "version": "1.4.4",
        "description": "Classifies HTTP/payload errors into structured FinMindErrorDetail",
        "research_only": True,
    },
    {
        "name": "finmind_schema_registry",
        "status": "STABLE",
        "version": "1.4.4",
        "description": "Schema definitions and registry for all supported FinMind datasets",
        "research_only": True,
    },
    {
        "name": "finmind_schema_drift",
        "status": "STABLE",
        "version": "1.4.4",
        "description": "Detects additive/breaking schema drift; blocking on required field missing",
        "research_only": True,
    },
    {
        "name": "finmind_conflict_detector",
        "status": "STABLE",
        "version": "1.4.4",
        "description": "Compares FinMind data vs primary source; primary always wins",
        "research_only": True,
    },
    {
        "name": "finmind_pit_guard",
        "status": "STABLE",
        "version": "1.4.4",
        "description": "Point-in-time classification; UNKNOWN blocks formal historical conclusion",
        "research_only": True,
    },
    {
        "name": "finmind_request_planner",
        "status": "STABLE",
        "version": "1.4.4",
        "description": "Dry-run fetch planner with allowlist, quota, schema, PIT checks",
        "research_only": True,
    },
]


def get_capabilities() -> List[Dict[str, Any]]:
    """Return all FinMind capabilities."""
    return list(FINMIND_CAPABILITIES)


def is_capability_available(name: str) -> bool:
    """Return True if capability is STABLE."""
    for cap in FINMIND_CAPABILITIES:
        if cap["name"] == name:
            return cap.get("status") == "STABLE"
    return False
