"""
paper_trading/stable_rollup/fixture_schema_v169.py
JSON fixture schema for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, List

REQUIRED_MARKERS: Dict[str, bool] = {
    "test_fixture": True,
    "demo_only": True,
    "paper_only": True,
    "research_only": True,
    "not_live": True,
    "no_broker": True,
    "no_real_account": True,
    "no_real_orders": True,
    "not_for_production": True,
    "stable_rollup_only": True,
}

REQUIRED_FIELDS: List[str] = [
    "test_fixture",
    "demo_only",
    "paper_only",
    "research_only",
    "not_live",
    "no_broker",
    "no_real_account",
    "no_real_orders",
    "not_for_production",
    "stable_rollup_only",
    "fixture_id",
    "scenario_id",
    "purpose",
    "usage_type",
    "deterministic_seed",
    "schema_version",
    "policy_version",
    "source_lineage",
    "expected_status",
]


def validate_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a fixture dict against the schema. Returns {valid, issues}."""
    issues = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in fixture:
            issues.append(f"Missing required field: {field!r}")

    # Check markers are all True
    for marker, expected_value in REQUIRED_MARKERS.items():
        actual = fixture.get(marker)
        if actual is not True:
            issues.append(f"Marker {marker!r} must be True, got {actual!r}")

    # Check fixture_id is non-empty
    if not fixture.get("fixture_id"):
        issues.append("fixture_id must be non-empty")

    # Check scenario_id is non-empty
    if not fixture.get("scenario_id"):
        issues.append("scenario_id must be non-empty")

    # Check schema_version
    if fixture.get("schema_version") != "169":
        issues.append(f"schema_version must be '169', got {fixture.get('schema_version')!r}")

    # Check policy_version
    if fixture.get("policy_version") != "1.6.9-live-paper-stable-rollup":
        issues.append(f"policy_version must be '1.6.9-live-paper-stable-rollup', got {fixture.get('policy_version')!r}")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
    }


def load_and_validate_fixture(path: str) -> Dict[str, Any]:
    """Load a JSON fixture file and validate it."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            fixture = json.load(f)
        result = validate_fixture(fixture)
        result["path"] = path
        result["fixture_id"] = fixture.get("fixture_id", "")
        return result
    except json.JSONDecodeError as exc:
        return {"valid": False, "issues": [f"JSON parse error: {exc}"], "path": path, "fixture_id": ""}
    except FileNotFoundError:
        return {"valid": False, "issues": [f"File not found: {path}"], "path": path, "fixture_id": ""}
    except Exception as exc:
        return {"valid": False, "issues": [str(exc)], "path": path, "fixture_id": ""}
