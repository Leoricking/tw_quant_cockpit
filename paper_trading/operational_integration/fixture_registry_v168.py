"""
paper_trading/operational_integration/fixture_registry_v168.py
Fixture Registry for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .fixture_schema_v168 import validate_fixture_full

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class FixtureRegistry:
    """Registry for integration test fixtures. Research only."""

    def __init__(self) -> None:
        self._fixtures: Dict[str, Dict[str, Any]] = {}

    def register(self, fixture: Dict[str, Any]) -> Dict[str, Any]:
        """Register a fixture after validation. Returns validation result."""
        validation = validate_fixture_full(fixture)
        if not validation["valid"]:
            return {"registered": False, "errors": validation["errors"], "paper_only": True}
        fid = fixture.get("fixture_id", "")
        if not fid:
            return {"registered": False, "errors": ["missing fixture_id"], "paper_only": True}
        self._fixtures[fid] = fixture
        return {"registered": True, "fixture_id": fid, "paper_only": True}

    def get(self, fixture_id: str) -> Optional[Dict[str, Any]]:
        """Return fixture by ID or None."""
        return self._fixtures.get(fixture_id)

    def list_ids(self) -> List[str]:
        """Return sorted list of all fixture IDs."""
        return sorted(self._fixtures.keys())

    def validate(self, fixture_id: str) -> Dict[str, Any]:
        """Validate a fixture by ID."""
        fixture = self._fixtures.get(fixture_id)
        if fixture is None:
            return {"valid": False, "errors": [f"fixture not found: {fixture_id}"], "paper_only": True}
        return validate_fixture_full(fixture)

    def validate_all(self) -> Dict[str, Any]:
        """Validate all registered fixtures."""
        results = {}
        errors_total = []
        for fid, fixture in self._fixtures.items():
            result = validate_fixture_full(fixture)
            results[fid] = result
            if not result["valid"]:
                errors_total.extend(result["errors"])
        all_valid = all(v["valid"] for v in results.values())
        return {
            "all_valid": all_valid,
            "total": len(self._fixtures),
            "valid_count": sum(1 for v in results.values() if v["valid"]),
            "error_count": len(errors_total),
            "details": results,
            "paper_only": True,
        }

    def count(self) -> int:
        """Return total number of registered fixtures."""
        return len(self._fixtures)

    def list_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Return fixtures filtered by category."""
        return [f for f in self._fixtures.values() if f.get("category") == category]

    def summarize(self) -> Dict[str, Any]:
        """Return summary of fixture registry."""
        categories = set(f.get("category", "") for f in self._fixtures.values())
        return {
            "total_fixtures": self.count(),
            "categories": sorted(categories),
            "category_counts": {
                cat: len(self.list_by_category(cat)) for cat in categories
            },
            "paper_only": True,
            "research_only": True,
        }

    def export_manifest(self) -> Dict[str, Any]:
        """Export manifest of all fixtures."""
        return {
            "version": "1.6.8",
            "total": self.count(),
            "fixtures": [
                {
                    "fixture_id": f.get("fixture_id", ""),
                    "category": f.get("category", ""),
                    "purpose": f.get("purpose", ""),
                    "scenario_id": f.get("scenario_id", ""),
                    "paper_only": True,
                }
                for f in self._fixtures.values()
            ],
            "paper_only": True,
        }
