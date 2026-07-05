"""
paper_trading/stable_rollup/fixture_aggregator_v169.py
Fixture aggregator for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any, Dict, Optional

VERSION = "1.6.9"

DEFAULT_FIXTURE_ROOT = "tests/fixtures/stable_rollup"


def run(fixture_root: Optional[str] = None) -> Dict[str, Any]:
    """Scan fixture directory and validate all JSON files."""
    from paper_trading.stable_rollup.fixture_schema_v169 import load_and_validate_fixture

    root = fixture_root or DEFAULT_FIXTURE_ROOT

    # Try to resolve relative to repo root
    base_candidates = [
        root,
        os.path.join(os.path.dirname(__file__), "..", "..", "..", root),
    ]

    fixture_path = None
    for candidate in base_candidates:
        p = Path(candidate)
        if p.is_dir():
            fixture_path = p
            break

    if fixture_path is None:
        return {
            "name": "fixture_aggregator_v169",
            "version": VERSION,
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "missing_markers": 0,
            "orphans": 0,
            "status": "DEGRADED",
            "error": f"fixture_root not found: {root!r}",
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    json_files = sorted(fixture_path.glob("*.json"))
    total = len(json_files)
    valid = 0
    invalid = 0
    missing_markers = 0
    ids_seen = set()
    orphans = 0

    for jf in json_files:
        result = load_and_validate_fixture(str(jf))
        if result["valid"]:
            valid += 1
        else:
            invalid += 1
            # Check if it's specifically missing markers
            marker_issues = [i for i in result["issues"] if "Marker" in i or "Missing required field" in i]
            if marker_issues:
                missing_markers += 1

        fid = result.get("fixture_id", "")
        if fid:
            if fid in ids_seen:
                orphans += 1
            ids_seen.add(fid)

    from paper_trading.stable_rollup.fixture_registry_v169 import get_registry
    registry = get_registry()
    # Orphans: fixture files not in registry
    for jf in json_files:
        stem = jf.stem
        if stem not in registry:
            orphans += 1

    status = "PASS" if (total >= 80 and valid >= 80 and invalid == 0) else "DEGRADED"

    return {
        "name": "fixture_aggregator_v169",
        "version": VERSION,
        "total": total,
        "valid": valid,
        "invalid": invalid,
        "missing_markers": missing_markers,
        "orphans": orphans,
        "status": status,
        "fixture_root": str(fixture_path),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
    }
