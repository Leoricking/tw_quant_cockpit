"""
paper_trading/small_capital_strategy/mistake_taxonomy_fixture_schema_v176.py
Fixture schema validation for v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "176"
_POLICY  = "1.7.6-mistake-taxonomy-weekly-review"

REQUIRED_SAFETY_FIELDS = [
    "paper_only",
    "research_only",
    "no_real_orders",
    "no_broker",
    "not_investment_advice",
    "demo_only",
    "not_for_production",
]

REQUIRED_FIELDS = [
    "id",
    "symbol",
    "trade_date",
    "mistake_category",
    "severity",
    "cost_twd",
    "week_label",
    "schema_version",
    "policy_version",
] + REQUIRED_SAFETY_FIELDS


def validate_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a fixture dict. Returns {valid, errors}."""
    errors: List[str] = []
    for f in REQUIRED_FIELDS:
        if f not in fixture:
            errors.append(f"Missing required field: {f}")
    # Safety field values
    for f in REQUIRED_SAFETY_FIELDS:
        if fixture.get(f) is not True:
            errors.append(f"Safety field {f} must be True")
    return {"valid": len(errors) == 0, "errors": errors}


def validate_all_fixtures(fixtures: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate a list of fixtures. Returns {all_valid, invalid_count, errors}."""
    all_errors: List[str] = []
    invalid = 0
    for fx in fixtures:
        result = validate_fixture(fx)
        if not result["valid"]:
            invalid += 1
            all_errors.extend(result["errors"])
    return {"all_valid": invalid == 0, "invalid_count": invalid, "errors": all_errors}
