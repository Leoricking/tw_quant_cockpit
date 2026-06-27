"""
paper_trading/failure_validation/fixtures_validator_v165.py — Fixture safety marker validation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Validates that all fixtures contain 10 required safety markers.
"""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional, Tuple

PAPER_ONLY = True
RESEARCH_ONLY = True

REQUIRED_SAFETY_MARKERS = [
    "TEST_FIXTURE",
    "DEMO_ONLY",
    "PAPER_ONLY",
    "RESEARCH_ONLY",
    "NOT_LIVE",
    "NO_BROKER",
    "NO_REAL_ACCOUNT",
    "NO_REAL_ORDER",
    "NOT_FOR_PRODUCTION",
    "FAILURE_INJECTION_ONLY",
]


def validate_fixture_safety_markers(fixture_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate that a fixture dict contains all 10 required safety markers set to True."""
    missing = []
    for marker in REQUIRED_SAFETY_MARKERS:
        if not fixture_data.get(marker, False):
            missing.append(marker)
    return len(missing) == 0, missing


def validate_fixture_file(filepath: str) -> Tuple[bool, List[str]]:
    """Load and validate a JSON fixture file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return validate_fixture_safety_markers(data)
    except Exception as e:
        return False, [f"ERROR loading fixture: {e}"]


def validate_fixture_directory(directory: str) -> Dict[str, Any]:
    """Validate all JSON fixtures in a directory."""
    results = {}
    total = 0
    passed = 0
    for fname in os.listdir(directory):
        if fname.endswith(".json"):
            fpath = os.path.join(directory, fname)
            ok, missing = validate_fixture_file(fpath)
            results[fname] = {"passed": ok, "missing_markers": missing}
            total += 1
            if ok:
                passed += 1
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "files": results,
    }
