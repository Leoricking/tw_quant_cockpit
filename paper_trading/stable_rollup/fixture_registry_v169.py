"""
paper_trading/stable_rollup/fixture_registry_v169.py
Fixture registry for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import Dict, Any, Optional


def _make_fixture_entry(fixture_id: str, scenario_id: str, purpose: str) -> dict:
    return {
        "fixture_id": fixture_id,
        "scenario_id": scenario_id,
        "purpose": purpose,
        "path": f"tests/fixtures/stable_rollup/{fixture_id}.json",
        "schema_version": "169",
        "policy_version": "1.6.9-live-paper-stable-rollup",
        "source_lineage": "v1.6.9",
        "paper_only": True,
        "no_real_orders": True,
    }


FIXTURE_REGISTRY: Dict[str, dict] = {
    f"sr_{str(i).zfill(3)}": _make_fixture_entry(
        f"sr_{str(i).zfill(3)}",
        f"scenario_{str(i).zfill(3)}",
        f"Stable rollup test fixture {i}",
    )
    for i in range(1, 81)
}


def get_registry() -> Dict[str, dict]:
    """Return the fixture registry."""
    return dict(FIXTURE_REGISTRY)


def get_fixture(fixture_id: str) -> Optional[dict]:
    """Return fixture metadata by ID, or None."""
    entry = FIXTURE_REGISTRY.get(fixture_id)
    return dict(entry) if entry else None


def validate_registry() -> Dict[str, Any]:
    """Validate the fixture registry."""
    issues = []
    for fid, entry in FIXTURE_REGISTRY.items():
        if entry.get("fixture_id") != fid:
            issues.append(f"fixture_id mismatch: key={fid!r}, entry={entry.get('fixture_id')!r}")
        if not entry.get("path"):
            issues.append(f"{fid}: missing path")
        if not entry.get("paper_only", False):
            issues.append(f"{fid}: paper_only must be True")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "total": len(FIXTURE_REGISTRY),
    }


def count_fixtures() -> int:
    """Return total number of registered fixtures."""
    return len(FIXTURE_REGISTRY)
