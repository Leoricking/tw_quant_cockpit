"""
paper_trading/small_capital_strategy/risk_dashboard_fixture_schema_v174.py
Fixture schema for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"
_LINEAGE = "paper_trading.small_capital_strategy.risk_dashboard_fixture_schema_v174"

REQUIRED_FIXTURE_FIELDS = [
    "fixture_id",
    "name",
    "category",
    "scenario_id",
    "inputs",
    "expected",
    "deterministic_seed",
    "paper_only",
    "no_real_orders",
    "test_fixture",
    "demo_only",
    "not_live",
    "no_broker",
    "no_real_account",
    "not_for_production",
    "not_investment_advice",
    "small_account_risk_dashboard_only",
]

REQUIRED_SAFETY_MARKERS = [
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
    "small_account_risk_dashboard_only",
]


def validate_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a single fixture dict. Returns {valid, errors}."""
    errors = []
    for f in REQUIRED_FIXTURE_FIELDS:
        if f not in fixture:
            errors.append(f"missing_field:{f}")
    for marker in REQUIRED_SAFETY_MARKERS:
        if not fixture.get(marker):
            errors.append(f"safety_marker_false:{marker}")
    if fixture.get("deterministic_seed") != int(_SCHEMA):
        errors.append(f"wrong_seed:{fixture.get('deterministic_seed')}")
    return {"valid": len(errors) == 0, "errors": errors}


def make_fixture(
    fixture_id: str,
    name: str,
    category: str,
    scenario_id: str,
    inputs: Dict[str, Any],
    expected: Dict[str, Any],
    seed: int = int(_SCHEMA),
    purpose: str = "",
    usage_type: str = "test",
    referenced_by: str = "",
    expected_score_range: List[float] = None,
    expected_block_reasons: List[str] = None,
) -> Dict[str, Any]:
    """Create a well-formed fixture dict."""
    return {
        "fixture_id": fixture_id,
        "name": name,
        "category": category,
        "scenario_id": scenario_id,
        "inputs": inputs,
        "expected": expected,
        "deterministic_seed": seed,
        "purpose": purpose or name,
        "usage_type": usage_type,
        "referenced_by": referenced_by,
        "expected_status": expected.get("status", "PASS"),
        "expected_score_range": expected_score_range or [0.0, 100.0],
        "expected_block_reasons": expected_block_reasons or [],
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
        "source_lineage": _LINEAGE,
        # Safety markers — all True, set at definition time (not test-time)
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
        "small_account_risk_dashboard_only": True,
    }
