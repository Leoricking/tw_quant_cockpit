"""
paper_trading/performance_attribution/fixture_registry_v167.py
Fixture Registry for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Register, list, get, validate fixtures. No production DB. No network.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .fixture_schema_v167 import (
    validate_fixture_full,
    build_fixture_template,
    REQUIRED_FIXTURE_MARKERS,
)

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class FixtureRegistry:
    """
    In-memory registry of paper attribution fixtures.
    Validates all fixtures on registration.
    Never stores fixtures with forbidden fields.
    """

    def __init__(self) -> None:
        self._fixtures: Dict[str, Dict[str, Any]] = {}

    def register(self, fixture: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a fixture. Validates all markers + forbidden fields.
        Returns {"registered": bool, "fixture_id": str, "errors": list}.
        """
        result = validate_fixture_full(fixture)
        if not result["valid"] or result["blocked"]:
            return {
                "registered": False,
                "fixture_id":  fixture.get("fixture_id", ""),
                "errors":      result["errors"],
                "blocked":     result["blocked"],
            }
        fid = fixture["fixture_id"]
        self._fixtures[fid] = dict(fixture)
        return {
            "registered": True,
            "fixture_id":  fid,
            "errors":      [],
            "blocked":     False,
        }

    def get(self, fixture_id: str) -> Optional[Dict[str, Any]]:
        """Get fixture by ID. Returns None if not found."""
        return self._fixtures.get(fixture_id)

    def list_ids(self) -> List[str]:
        """Sorted list of registered fixture IDs."""
        return sorted(self._fixtures.keys())

    def list_by_category(self, category: str) -> List[Dict[str, Any]]:
        """List all fixtures in a category."""
        return [f for f in self._fixtures.values() if f.get("category") == category]

    def count(self) -> int:
        """Total number of registered fixtures."""
        return len(self._fixtures)

    def validate(self, fixture_id: str) -> Dict[str, Any]:
        """Re-validate a registered fixture by ID."""
        fixture = self._fixtures.get(fixture_id)
        if fixture is None:
            return {"valid": False, "errors": [f"not_found: {fixture_id}"]}
        return validate_fixture_full(fixture)

    def validate_all(self) -> Dict[str, Any]:
        """Validate all registered fixtures. Returns summary."""
        results = {}
        failures = 0
        for fid, fixture in self._fixtures.items():
            r = validate_fixture_full(fixture)
            results[fid] = r
            if not r["valid"]:
                failures += 1
        return {
            "total":    len(self._fixtures),
            "failures": failures,
            "all_valid": failures == 0,
            "results":  results,
            "paper_only": True,
        }

    def delete(self, fixture_id: str) -> Dict[str, Any]:
        """Delete a fixture by ID (test cleanup only)."""
        if fixture_id in self._fixtures:
            del self._fixtures[fixture_id]
            return {"deleted": True, "fixture_id": fixture_id}
        return {"deleted": False, "fixture_id": fixture_id, "error": "not_found"}

    def summarize(self) -> Dict[str, Any]:
        """Return registry summary statistics."""
        categories: Dict[str, int] = {}
        for f in self._fixtures.values():
            cat = f.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        return {
            "total":        len(self._fixtures),
            "categories":   categories,
            "fixture_ids":  self.list_ids(),
            "paper_only":   True,
            "research_only": True,
        }

    def export_manifest(self) -> List[Dict[str, Any]]:
        """Return a list of fixture summaries (id, purpose, category)."""
        return [
            {
                "fixture_id": f.get("fixture_id", ""),
                "purpose":    f.get("purpose", ""),
                "category":   f.get("category", ""),
                "paper_only": True,
            }
            for f in sorted(self._fixtures.values(), key=lambda x: x.get("fixture_id", ""))
        ]
