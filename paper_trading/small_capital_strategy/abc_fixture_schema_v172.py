"""
paper_trading/small_capital_strategy/abc_fixture_schema_v172.py
Fixture schema for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SCHEMA_VERSION  = "172"
_POLICY_VERSION  = "1.7.2-abc-buy-point-execution-plan"
_SOURCE_LINEAGE  = "paper_trading.small_capital_strategy.abc_fixture_schema_v172"

# Required marker keys for every fixture
REQUIRED_MARKERS: List[str] = [
    "test_fixture",
    "demo_only",
    "paper_only",
    "research_only",
    "not_live",
    "no_broker",
    "no_real_account",
    "no_real_orders",
    "not_for_production",
    "not_investment_advice",
    "abc_execution_only",
]

# Required metadata keys
REQUIRED_METADATA: List[str] = [
    "fixture_id",
    "scenario_id",
    "purpose",
    "usage_type",
    "referenced_by",
    "deterministic_seed",
    "schema_version",
    "policy_version",
    "source_lineage",
    "expected_status",
    "expected_buy_point_type",
    "expected_score_range",
    "expected_action",
    "expected_block_reasons",
]


def make_fixture(
    fixture_id: str,
    scenario_id: str,
    purpose: str,
    usage_type: str,
    referenced_by: str,
    deterministic_seed: int,
    expected_status: str,
    expected_buy_point_type: str,
    expected_score_range: List[float],
    expected_action: str,
    expected_block_reasons: List[str],
    signal_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create a validated fixture dict."""
    fixture = {
        # Safety markers
        "test_fixture": True,
        "demo_only": True,
        "paper_only": True,
        "research_only": True,
        "not_live": True,
        "no_broker": True,
        "no_real_account": True,
        "no_real_orders": True,
        "not_for_production": True,
        "not_investment_advice": True,
        "abc_execution_only": True,
        # Metadata
        "fixture_id": fixture_id,
        "scenario_id": scenario_id,
        "purpose": purpose,
        "usage_type": usage_type,
        "referenced_by": referenced_by,
        "deterministic_seed": deterministic_seed,
        "schema_version": _SCHEMA_VERSION,
        "policy_version": _POLICY_VERSION,
        "source_lineage": _SOURCE_LINEAGE,
        "expected_status": expected_status,
        "expected_buy_point_type": expected_buy_point_type,
        "expected_score_range": expected_score_range,
        "expected_action": expected_action,
        "expected_block_reasons": expected_block_reasons,
    }
    if signal_data:
        fixture["signal_data"] = signal_data
    return fixture


def validate_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a fixture dict. Returns {valid, errors}."""
    errors = []
    for key in REQUIRED_MARKERS:
        if fixture.get(key) is not True:
            errors.append(f"Missing or invalid marker: {key}={fixture.get(key)!r}")
    for key in REQUIRED_METADATA:
        if key not in fixture:
            errors.append(f"Missing metadata key: {key}")
    if fixture.get("schema_version") != _SCHEMA_VERSION:
        errors.append(f"schema_version must be {_SCHEMA_VERSION!r}")
    return {"valid": len(errors) == 0, "errors": errors}


def validate_all_fixtures(fixtures: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate a list of fixtures. Returns aggregate result."""
    all_errors = []
    ids_seen = set()
    for f in fixtures:
        result = validate_fixture(f)
        if not result["valid"]:
            all_errors.extend(result["errors"])
        fid = f.get("fixture_id")
        if fid in ids_seen:
            all_errors.append(f"Duplicate fixture_id: {fid}")
        if fid:
            ids_seen.add(fid)
    return {
        "valid": len(all_errors) == 0,
        "total": len(fixtures),
        "errors": all_errors,
    }
