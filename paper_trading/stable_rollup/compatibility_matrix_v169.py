"""
paper_trading/stable_rollup/compatibility_matrix_v169.py
Version compatibility matrix for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import List, Optional

# All compatibility is explicitly defined, NOT based on version string comparison
COMPATIBILITY_EDGES: List[dict] = [
    {
        "from_version": "1.6.0",
        "to_version": "1.6.1",
        "version_identity": "COMPATIBLE",
        "schema_compatibility": "COMPATIBLE",
        "cli_compatibility": "COMPATIBLE",
        "gui_compatibility": "COMPATIBLE",
        "fixture_compatibility": "COMPATIBLE",
        "lineage_compatibility": "COMPATIBLE",
        "safety_compatibility": "COMPATIBLE",
        "health_compatibility": "COMPATIBLE",
        "gate_compatibility": "COMPATIBLE",
        "report_compatibility": "COMPATIBLE",
        "overall_status": "COMPATIBLE",
    },
    {
        "from_version": "1.6.1",
        "to_version": "1.6.2",
        "version_identity": "COMPATIBLE",
        "schema_compatibility": "COMPATIBLE",
        "cli_compatibility": "COMPATIBLE",
        "gui_compatibility": "COMPATIBLE",
        "fixture_compatibility": "COMPATIBLE",
        "lineage_compatibility": "COMPATIBLE",
        "safety_compatibility": "COMPATIBLE",
        "health_compatibility": "COMPATIBLE",
        "gate_compatibility": "COMPATIBLE",
        "report_compatibility": "COMPATIBLE",
        "overall_status": "COMPATIBLE",
    },
    {
        "from_version": "1.6.2",
        "to_version": "1.6.3",
        "version_identity": "COMPATIBLE",
        "schema_compatibility": "COMPATIBLE",
        "cli_compatibility": "COMPATIBLE",
        "gui_compatibility": "COMPATIBLE",
        "fixture_compatibility": "COMPATIBLE",
        "lineage_compatibility": "COMPATIBLE",
        "safety_compatibility": "COMPATIBLE",
        "health_compatibility": "COMPATIBLE",
        "gate_compatibility": "COMPATIBLE",
        "report_compatibility": "COMPATIBLE",
        "overall_status": "COMPATIBLE",
    },
    {
        "from_version": "1.6.3",
        "to_version": "1.6.4",
        "version_identity": "COMPATIBLE",
        "schema_compatibility": "COMPATIBLE",
        "cli_compatibility": "COMPATIBLE",
        "gui_compatibility": "COMPATIBLE",
        "fixture_compatibility": "COMPATIBLE",
        "lineage_compatibility": "COMPATIBLE",
        "safety_compatibility": "COMPATIBLE",
        "health_compatibility": "COMPATIBLE",
        "gate_compatibility": "COMPATIBLE",
        "report_compatibility": "COMPATIBLE",
        "overall_status": "COMPATIBLE",
    },
    {
        "from_version": "1.6.4",
        "to_version": "1.6.5",
        "version_identity": "COMPATIBLE",
        "schema_compatibility": "COMPATIBLE",
        "cli_compatibility": "COMPATIBLE",
        "gui_compatibility": "COMPATIBLE",
        "fixture_compatibility": "COMPATIBLE",
        "lineage_compatibility": "COMPATIBLE",
        "safety_compatibility": "COMPATIBLE",
        "health_compatibility": "COMPATIBLE",
        "gate_compatibility": "COMPATIBLE",
        "report_compatibility": "COMPATIBLE",
        "overall_status": "COMPATIBLE",
    },
    {
        "from_version": "1.6.5",
        "to_version": "1.6.6",
        "version_identity": "COMPATIBLE",
        "schema_compatibility": "COMPATIBLE",
        "cli_compatibility": "COMPATIBLE",
        "gui_compatibility": "COMPATIBLE",
        "fixture_compatibility": "COMPATIBLE",
        "lineage_compatibility": "COMPATIBLE",
        "safety_compatibility": "COMPATIBLE",
        "health_compatibility": "COMPATIBLE",
        "gate_compatibility": "COMPATIBLE",
        "report_compatibility": "COMPATIBLE",
        "overall_status": "COMPATIBLE",
    },
    {
        "from_version": "1.6.6",
        "to_version": "1.6.6.1",
        "version_identity": "COMPATIBLE",
        "schema_compatibility": "COMPATIBLE",
        "cli_compatibility": "COMPATIBLE",
        "gui_compatibility": "COMPATIBLE",
        "fixture_compatibility": "COMPATIBLE",
        "lineage_compatibility": "COMPATIBLE",
        "safety_compatibility": "COMPATIBLE",
        "health_compatibility": "COMPATIBLE",
        "gate_compatibility": "COMPATIBLE",
        "report_compatibility": "COMPATIBLE",
        "overall_status": "COMPATIBLE",
    },
    {
        "from_version": "1.6.6.1",
        "to_version": "1.6.6.2",
        "version_identity": "COMPATIBLE",
        "schema_compatibility": "COMPATIBLE",
        "cli_compatibility": "COMPATIBLE",
        "gui_compatibility": "COMPATIBLE",
        "fixture_compatibility": "COMPATIBLE",
        "lineage_compatibility": "COMPATIBLE",
        "safety_compatibility": "COMPATIBLE",
        "health_compatibility": "COMPATIBLE",
        "gate_compatibility": "COMPATIBLE",
        "report_compatibility": "COMPATIBLE",
        "overall_status": "COMPATIBLE",
    },
    {
        "from_version": "1.6.6.2",
        "to_version": "1.6.7",
        "version_identity": "COMPATIBLE",
        "schema_compatibility": "COMPATIBLE",
        "cli_compatibility": "COMPATIBLE",
        "gui_compatibility": "COMPATIBLE",
        "fixture_compatibility": "COMPATIBLE",
        "lineage_compatibility": "COMPATIBLE",
        "safety_compatibility": "COMPATIBLE",
        "health_compatibility": "COMPATIBLE",
        "gate_compatibility": "COMPATIBLE",
        "report_compatibility": "COMPATIBLE",
        "overall_status": "COMPATIBLE",
    },
    {
        "from_version": "1.6.7",
        "to_version": "1.6.8",
        "version_identity": "COMPATIBLE",
        "schema_compatibility": "COMPATIBLE",
        "cli_compatibility": "COMPATIBLE",
        "gui_compatibility": "COMPATIBLE",
        "fixture_compatibility": "COMPATIBLE",
        "lineage_compatibility": "COMPATIBLE",
        "safety_compatibility": "COMPATIBLE",
        "health_compatibility": "COMPATIBLE",
        "gate_compatibility": "COMPATIBLE",
        "report_compatibility": "COMPATIBLE",
        "overall_status": "COMPATIBLE",
    },
    {
        "from_version": "1.6.8",
        "to_version": "1.6.9",
        "version_identity": "COMPATIBLE",
        "schema_compatibility": "COMPATIBLE",
        "cli_compatibility": "COMPATIBLE",
        "gui_compatibility": "COMPATIBLE",
        "fixture_compatibility": "COMPATIBLE",
        "lineage_compatibility": "COMPATIBLE",
        "safety_compatibility": "COMPATIBLE",
        "health_compatibility": "COMPATIBLE",
        "gate_compatibility": "COMPATIBLE",
        "report_compatibility": "COMPATIBLE",
        "overall_status": "COMPATIBLE",
    },
]


def get_edges() -> List[dict]:
    """Return all compatibility edges."""
    return list(COMPATIBILITY_EDGES)


def get_edge(from_v: str, to_v: str) -> Optional[dict]:
    """Return compatibility edge between two versions, or None."""
    for edge in COMPATIBILITY_EDGES:
        if edge["from_version"] == from_v and edge["to_version"] == to_v:
            return dict(edge)
    return None


def validate_matrix() -> dict:
    """Validate the compatibility matrix."""
    issues = []
    edges_seen = set()

    for edge in COMPATIBILITY_EDGES:
        from_v = edge.get("from_version", "")
        to_v = edge.get("to_version", "")
        key = (from_v, to_v)

        if not from_v or not to_v:
            issues.append(f"Edge missing from/to version: {edge}")
            continue
        if key in edges_seen:
            issues.append(f"Duplicate edge: {from_v} -> {to_v}")
        edges_seen.add(key)

        overall = edge.get("overall_status", "")
        if overall not in ("COMPATIBLE", "INCOMPATIBLE", "PARTIAL", "UNKNOWN"):
            issues.append(f"Edge {from_v}->{to_v}: invalid overall_status {overall!r}")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "total": len(COMPATIBILITY_EDGES),
        "unique": len(edges_seen),
    }
