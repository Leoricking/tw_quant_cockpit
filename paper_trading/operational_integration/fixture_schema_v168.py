"""
paper_trading/operational_integration/fixture_schema_v168.py
Fixture Schema for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

SCHEMA_VERSION = "1.6.8"
POLICY_VERSION = "1.6.8"
PAPER_ONLY     = True
RESEARCH_ONLY  = True
NO_REAL_ORDERS = True

REQUIRED_FIXTURE_MARKERS = [
    "test_fixture", "demo_only", "paper_only", "research_only", "not_live",
    "no_broker", "no_real_account", "no_real_orders", "not_for_production",
    "operational_integration_only",
]

FORBIDDEN_FIXTURE_FIELDS = frozenset({
    "broker_session", "real_account_token", "api_secret", "password",
    "credential", "real_order_handle", "production_db_connection",
    "bank_account", "real_capital_control", "live_execution",
    "shioaji_login", "broker_api_key", "production_ledger",
})


def validate_fixture_markers(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that fixture has all required safety markers.
    Accepts both lowercase and UPPERCASE marker keys (case-insensitive).
    Returns {valid, errors, warnings, paper_only}.
    """
    errors = []
    warnings = []
    # Build case-insensitive lookup: lowercase key -> value
    lower_fixture = {k.lower(): v for k, v in fixture.items()}
    for marker in REQUIRED_FIXTURE_MARKERS:
        if not lower_fixture.get(marker):
            errors.append(f"missing_marker: {marker}")
    valid = len(errors) == 0
    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "paper_only": True,
        "research_only": True,
    }


def validate_fixture_forbidden_fields(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check that fixture does not contain forbidden fields.
    Returns {clean, blocked, violations, paper_only}.
    """
    violations = []
    for field in FORBIDDEN_FIXTURE_FIELDS:
        if field in fixture:
            violations.append(field)
    clean = len(violations) == 0
    return {
        "clean": clean,
        "blocked": not clean,
        "violations": violations,
        "paper_only": True,
    }


def validate_fixture_full(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """Run full fixture validation (markers + forbidden fields)."""
    marker_result = validate_fixture_markers(fixture)
    forbidden_result = validate_fixture_forbidden_fields(fixture)
    valid = marker_result["valid"] and forbidden_result["clean"]
    errors = marker_result["errors"] + [f"forbidden_field: {v}" for v in forbidden_result["violations"]]
    return {
        "valid": valid,
        "errors": errors,
        "marker_check": marker_result,
        "forbidden_check": forbidden_result,
        "paper_only": True,
    }


def build_fixture_template(
    fixture_id: str,
    purpose: str,
    category: str,
    scenario_id: str = "",
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build a fixture template with all required markers."""
    template = {
        "fixture_id": fixture_id,
        "purpose": purpose,
        "category": category,
        "scenario_id": scenario_id,
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "source_lineage": f"fixture_template:{fixture_id}",
        "usage_type": "INTEGRATION",
        "referenced_by": [],
        "deterministic_seed": 42,
        "expected_status": "PASS",
        "expected_score_range": [60, 100],
        "expected_reconciliation": "RECONCILED",
        # Required markers
        "test_fixture": True,
        "demo_only": True,
        "paper_only": True,
        "research_only": True,
        "not_live": True,
        "no_broker": True,
        "no_real_account": True,
        "no_real_orders": True,
        "not_for_production": True,
        "operational_integration_only": True,
        "input": {},
        "expected": {},
    }
    if extra:
        template.update(extra)
    return template
