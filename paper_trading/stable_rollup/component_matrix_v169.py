"""
paper_trading/stable_rollup/component_matrix_v169.py
Component registry and status matrix for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import List, Optional

COMPONENT_MATRIX: List[dict] = [
    {"component_name": "__init__", "module": "paper_trading.stable_rollup", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "version_v169", "module": "paper_trading.stable_rollup.version_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "enums_v169", "module": "paper_trading.stable_rollup.enums_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "models_v169", "module": "paper_trading.stable_rollup.models_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["enums_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "safety_v169", "module": "paper_trading.stable_rollup.safety_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "release_manifest_v169", "module": "paper_trading.stable_rollup.release_manifest_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "release_registry_v169", "module": "paper_trading.stable_rollup.release_registry_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["release_manifest_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "capability_matrix_v169", "module": "paper_trading.stable_rollup.capability_matrix_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "safety_matrix_v169", "module": "paper_trading.stable_rollup.safety_matrix_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "compatibility_matrix_v169", "module": "paper_trading.stable_rollup.compatibility_matrix_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "component_matrix_v169", "module": "paper_trading.stable_rollup.component_matrix_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "stable_contract_v169", "module": "paper_trading.stable_rollup.stable_contract_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["version_v169", "safety_v169", "release_manifest_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "stable_snapshot_v169", "module": "paper_trading.stable_rollup.stable_snapshot_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["models_v169", "enums_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "stable_validator_v169", "module": "paper_trading.stable_rollup.stable_validator_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["version_v169", "safety_v169", "release_manifest_v169", "release_registry_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "stable_reconciler_v169", "module": "paper_trading.stable_rollup.stable_reconciler_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["models_v169", "release_manifest_v169", "capability_matrix_v169", "safety_matrix_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "stable_scorecard_v169", "module": "paper_trading.stable_rollup.stable_scorecard_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["models_v169", "enums_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "stable_query_v169", "module": "paper_trading.stable_rollup.stable_query_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["models_v169", "release_registry_v169", "capability_matrix_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "stable_report_v169", "module": "paper_trading.stable_rollup.stable_report_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["models_v169", "stable_scorecard_v169", "stable_snapshot_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "migration_readiness_v169", "module": "paper_trading.stable_rollup.migration_readiness_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["models_v169", "enums_v169", "release_registry_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "regression_matrix_v169", "module": "paper_trading.stable_rollup.regression_matrix_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["models_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "scenario_registry_v169", "module": "paper_trading.stable_rollup.scenario_registry_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "fixture_schema_v169", "module": "paper_trading.stable_rollup.fixture_schema_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "fixture_registry_v169", "module": "paper_trading.stable_rollup.fixture_registry_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["fixture_schema_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "health_aggregator_v169", "module": "paper_trading.stable_rollup.health_aggregator_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "gate_aggregator_v169", "module": "paper_trading.stable_rollup.gate_aggregator_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "cli_aggregator_v169", "module": "paper_trading.stable_rollup.cli_aggregator_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "gui_aggregator_v169", "module": "paper_trading.stable_rollup.gui_aggregator_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": [], "health_coverage": True, "gate_coverage": True},
    {"component_name": "fixture_aggregator_v169", "module": "paper_trading.stable_rollup.fixture_aggregator_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["fixture_schema_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "scenario_aggregator_v169", "module": "paper_trading.stable_rollup.scenario_aggregator_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["scenario_registry_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "lineage_aggregator_v169", "module": "paper_trading.stable_rollup.lineage_aggregator_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["release_registry_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "contract_aggregator_v169", "module": "paper_trading.stable_rollup.contract_aggregator_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["stable_contract_v169"], "health_coverage": True, "gate_coverage": True},
    {"component_name": "health_v169", "module": "paper_trading.stable_rollup.health_v169", "version": "1.6.9", "status": "ACTIVE", "dependencies": ["version_v169", "enums_v169", "models_v169", "safety_v169"], "health_coverage": True, "gate_coverage": True},
]


def get_matrix() -> List[dict]:
    """Return the full component matrix."""
    return list(COMPONENT_MATRIX)


def get_component(name: str) -> Optional[dict]:
    """Return component entry by name, or None."""
    for comp in COMPONENT_MATRIX:
        if comp["component_name"] == name:
            return dict(comp)
    return None


def validate_matrix() -> dict:
    """Validate the component matrix."""
    issues = []
    names_seen = set()

    for comp in COMPONENT_MATRIX:
        name = comp.get("component_name", "")
        if not name:
            issues.append("Entry missing 'component_name'")
            continue
        if name in names_seen:
            issues.append(f"Duplicate component: {name!r}")
        names_seen.add(name)

        if not comp.get("module"):
            issues.append(f"Component {name!r}: missing 'module'")
        if comp.get("version") != "1.6.9":
            issues.append(f"Component {name!r}: version must be '1.6.9'")
        if comp.get("status") not in ("ACTIVE", "INACTIVE", "DEGRADED", "MISSING"):
            issues.append(f"Component {name!r}: invalid status {comp.get('status')!r}")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "total": len(COMPONENT_MATRIX),
        "unique": len(names_seen),
    }
