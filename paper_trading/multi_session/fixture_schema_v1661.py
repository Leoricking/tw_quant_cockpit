"""
paper_trading/multi_session/fixture_schema_v1661.py
Fixture safety marker schema and validation for Multi-session Coordination v1.6.6.1.
[!] Research Only. Paper Only. No Real Orders. No Broker. No Production Capability.
[!] Deterministic. Side-effect free. No file mutation during validation. No network.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

VERSION = "1.6.6.1"
SCHEMA_VERSION = "1661"

# All 10 required safety markers with their required values
REQUIRED_FIXTURE_MARKERS: Dict[str, Any] = {
    "test_fixture": True,
    "demo_only": True,
    "paper_only": True,
    "research_only": True,
    "not_live": True,
    "no_broker": True,
    "no_real_account": True,
    "no_real_orders": True,
    "not_for_production": True,
    "multi_session_only": True,
}

MARKER_COUNT = len(REQUIRED_FIXTURE_MARKERS)  # 10


def validate_fixture_markers(fixture: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate that a fixture dict contains all 10 required safety markers
    with the correct boolean True values.

    Returns (is_valid, list_of_violations).
    Deterministic. No side effects.
    """
    violations: List[str] = []
    for key, expected in REQUIRED_FIXTURE_MARKERS.items():
        if key not in fixture:
            violations.append(f"missing marker: {key!r}")
        elif fixture[key] is not True:
            violations.append(
                f"invalid marker value: {key!r}={fixture[key]!r} (expected True)"
            )
    return (len(violations) == 0, violations)


def validate_fixture_schema(fixture: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate fixture has required structural fields in addition to markers.
    Returns (is_valid, list_of_violations).
    """
    violations: List[str] = []
    marker_valid, marker_violations = validate_fixture_markers(fixture)
    violations.extend(marker_violations)

    if "test_id" not in fixture:
        violations.append("missing required field: 'test_id'")
    elif not isinstance(fixture["test_id"], str) or not fixture["test_id"].strip():
        violations.append("invalid 'test_id': must be a non-empty string")

    if "version" not in fixture:
        violations.append("missing required field: 'version'")

    return (len(violations) == 0, violations)


def find_missing_markers(fixture: Dict[str, Any]) -> List[str]:
    """Return list of marker keys absent from the fixture."""
    return [k for k in REQUIRED_FIXTURE_MARKERS if k not in fixture]


def find_invalid_marker_values(fixture: Dict[str, Any]) -> List[Tuple[str, Any]]:
    """
    Return list of (key, actual_value) for markers present but not True.
    """
    return [
        (k, fixture[k])
        for k in REQUIRED_FIXTURE_MARKERS
        if k in fixture and fixture[k] is not True
    ]


def normalize_marker_report(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a structured marker report for a single fixture.
    Deterministic. No side effects.
    """
    missing = find_missing_markers(fixture)
    invalid = find_invalid_marker_values(fixture)
    present = [k for k in REQUIRED_FIXTURE_MARKERS if k in fixture and fixture[k] is True]
    return {
        "test_id": fixture.get("test_id", "<unknown>"),
        "total_required": MARKER_COUNT,
        "present_and_valid": len(present),
        "missing": missing,
        "invalid_values": invalid,
        "is_valid": len(missing) == 0 and len(invalid) == 0,
    }


def fixture_safety_summary(fixtures: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregate safety marker summary across a list of fixture dicts.
    Returns counts and per-marker missing stats.
    Deterministic. No side effects.
    """
    total = len(fixtures)
    valid_count = 0
    invalid_count = 0
    missing_by_marker: Dict[str, int] = {k: 0 for k in REQUIRED_FIXTURE_MARKERS}
    invalid_by_marker: Dict[str, int] = {k: 0 for k in REQUIRED_FIXTURE_MARKERS}

    for fx in fixtures:
        is_valid, _ = validate_fixture_markers(fx)
        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1
        for k in REQUIRED_FIXTURE_MARKERS:
            if k not in fx:
                missing_by_marker[k] += 1
            elif fx[k] is not True:
                invalid_by_marker[k] += 1

    return {
        "total": total,
        "valid": valid_count,
        "invalid": invalid_count,
        "missing_by_marker": missing_by_marker,
        "invalid_values_by_marker": invalid_by_marker,
        "marker_count": MARKER_COUNT,
        "schema_version": SCHEMA_VERSION,
        "all_valid": valid_count == total,
    }
