"""
paper_trading/small_capital_strategy/fixture_schema_v170.py
Fixture schema for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

SCHEMA_VERSION = "170"

REQUIRED_MARKERS: Dict[str, bool] = {
    "paper_only": True,
    "research_only": True,
    "no_real_orders": True,
    "not_investment_advice": True,
    "small_capital_strategy_only": True,
    "fixture_data_only": True,
    "no_live_data": True,
    "no_broker_connection": True,
    "simulation_safe": True,
    "schema_validated": True,
}

REQUIRED_FIELDS: List[str] = [
    "fixture_id",
    "scenario_id",
    "template_id",
    "schema_version",
    "paper_only",
    "research_only",
    "no_real_orders",
    "not_investment_advice",
    "small_capital_strategy_only",
    "fixture_data_only",
    "no_live_data",
    "no_broker_connection",
    "simulation_safe",
    "schema_validated",
    "input",
    "expected",
    "category",
    "description",
    "created_at",
]


def validate_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a fixture dict against the schema. Returns {valid, issues}."""
    issues = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in fixture:
            issues.append(f"missing required field: {field}")

    # Check required markers
    for marker, expected_value in REQUIRED_MARKERS.items():
        if fixture.get(marker) != expected_value:
            issues.append(
                f"marker '{marker}' must be {expected_value}, got {fixture.get(marker)!r}"
            )

    # Check schema_version
    if fixture.get("schema_version") != SCHEMA_VERSION:
        issues.append(
            f"schema_version must be '{SCHEMA_VERSION}', got {fixture.get('schema_version')!r}"
        )

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "fixture_id": fixture.get("fixture_id", "unknown"),
    }


def get_required_markers() -> Dict[str, bool]:
    """Return a copy of required markers."""
    return dict(REQUIRED_MARKERS)


def get_required_fields() -> List[str]:
    """Return a copy of required fields."""
    return list(REQUIRED_FIELDS)
