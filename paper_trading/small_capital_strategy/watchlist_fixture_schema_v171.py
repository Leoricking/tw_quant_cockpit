"""
paper_trading/small_capital_strategy/watchlist_fixture_schema_v171.py
Fixture schema for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

SCHEMA_VERSION = "171"

REQUIRED_MARKERS: Dict[str, bool] = {
    "test_fixture":           True,
    "demo_only":              True,
    "paper_only":             True,
    "research_only":          True,
    "not_live":               True,
    "no_broker":              True,
    "no_real_account":        True,
    "no_real_orders":         True,
    "not_for_production":     True,
    "not_investment_advice":  True,
    "watchlist_strategy_only": True,
}

REQUIRED_FIELDS: List[str] = [
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
    "expected_score_range",
    "expected_tier",
    "expected_exclusion_reasons",
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
    "watchlist_strategy_only",
]


def validate_watchlist_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a watchlist fixture dict. Returns {valid, issues}."""
    issues = []

    for field in REQUIRED_FIELDS:
        if field not in fixture:
            issues.append(f"missing required field: {field}")

    for marker, expected in REQUIRED_MARKERS.items():
        if fixture.get(marker) != expected:
            issues.append(
                f"marker '{marker}' must be {expected}, got {fixture.get(marker)!r}"
            )

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
