"""
paper_trading/small_capital_strategy/theme_rotation_fixture_schema_v177.py
Fixture schema definition for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"

FIXTURE_REQUIRED_FIELDS = [
    "id",
    "symbol",
    "theme",
    "grade",
    "breadth_score",
    "paper_only",
    "research_only",
    "no_real_orders",
    "no_broker",
    "not_investment_advice",
    "demo_only",
    "not_for_production",
    "schema_version",
    "policy_version",
]

FIXTURE_BOOLEAN_FIELDS = [
    "paper_only",
    "research_only",
    "no_real_orders",
    "no_broker",
    "not_investment_advice",
    "demo_only",
    "not_for_production",
]


def validate_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a single fixture dict. Returns {valid, errors}."""
    errors: List[str] = []

    for field in FIXTURE_REQUIRED_FIELDS:
        if field not in fixture:
            errors.append(f"Missing required field: {field}")

    for field in FIXTURE_BOOLEAN_FIELDS:
        if field in fixture and fixture[field] is not True:
            errors.append(f"Boolean safety field must be True: {field}")

    if "schema_version" in fixture and fixture["schema_version"] != _SCHEMA:
        errors.append(f"schema_version mismatch: expected {_SCHEMA}, got {fixture['schema_version']}")

    return {"valid": len(errors) == 0, "errors": errors}


def validate_all_fixtures(fixtures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate all fixtures. Returns list of validation results."""
    return [validate_fixture(f) for f in fixtures]


def get_schema_version() -> str:
    """Return schema version."""
    return _SCHEMA


def get_required_fields() -> List[str]:
    """Return list of required fixture fields."""
    return list(FIXTURE_REQUIRED_FIELDS)
