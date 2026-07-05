"""
paper_trading/stable_rollup/release_manifest_v169.py
v1.6.x Release Manifest for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from typing import List, Optional

RELEASE_MANIFEST: List[dict] = [
    {
        "version": "1.6.0",
        "release_name": "Live Paper Trading Foundation",
        "parent_version": None,
        "parent_commit": None,
        "commit": "SEALED",
        "release_category": "foundation",
        "capability_groups": ["paper_trading", "execution_simulator", "paper_ledger", "paper_risk_gate"],
        "safety_boundaries": ["NO_REAL_ORDERS", "BROKER_EXECUTION_ENABLED=False"],
        "health_module": "paper_trading.health_v160",
        "gate_module": "release.live_paper_trading_release_gate_v160",
        "cli_prefix": "paper",
        "gui_panel": "gui.live_paper_trading_panel",
        "fixture_roots": ["tests/fixtures/live_paper_trading/"],
        "scenario_roots": ["tests/scenarios/live_paper_trading/"],
        "known_limitations": ["Simulation only", "No broker connectivity"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.1",
        "release_name": "Market Data Session Adapter",
        "parent_version": "1.6.0",
        "parent_commit": "SEALED",
        "commit": "SEALED",
        "release_category": "adapter",
        "capability_groups": ["market_data_session", "session_adapter", "data_replay"],
        "safety_boundaries": ["NO_REAL_ORDERS", "BROKER_EXECUTION_ENABLED=False"],
        "health_module": "paper_trading.market_data.health_v161",
        "gate_module": "release.market_data_session_release_gate_v161",
        "cli_prefix": "market-data",
        "gui_panel": "gui.market_data_session_panel",
        "fixture_roots": ["tests/fixtures/market_data_session/"],
        "scenario_roots": ["tests/scenarios/market_data_session/"],
        "known_limitations": ["Simulated market data only"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.1.1",
        "release_name": "Warning Clean Hotfix",
        "parent_version": "1.6.1",
        "parent_commit": "SEALED",
        "commit": "SEALED",
        "release_category": "hotfix",
        "capability_groups": ["warning_cleanup"],
        "safety_boundaries": ["NO_REAL_ORDERS"],
        "health_module": None,
        "gate_module": None,
        "cli_prefix": None,
        "gui_panel": None,
        "fixture_roots": [],
        "scenario_roots": [],
        "known_limitations": ["Hotfix only, no new features"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.2",
        "release_name": "Paper Strategy Orchestration",
        "parent_version": "1.6.1.1",
        "parent_commit": "SEALED",
        "commit": "SEALED",
        "release_category": "feature",
        "capability_groups": ["strategy_orchestration", "signal_evaluation", "decision_pipeline"],
        "safety_boundaries": ["NO_REAL_ORDERS", "REAL_STRATEGY_EXECUTION_ENABLED=False"],
        "health_module": "paper_trading.strategy.health_v162",
        "gate_module": "release.paper_strategy_orchestration_release_gate_v162",
        "cli_prefix": "paper-strategy",
        "gui_panel": "gui.paper_strategy_panel",
        "fixture_roots": ["tests/fixtures/paper_strategy/"],
        "scenario_roots": ["tests/scenarios/paper_strategy/"],
        "known_limitations": ["Paper orders only, no live execution"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.3",
        "release_name": "Session Operations Observability",
        "parent_version": "1.6.2",
        "parent_commit": "SEALED",
        "commit": "SEALED",
        "release_category": "observability",
        "capability_groups": ["session_operations", "observability", "metrics"],
        "safety_boundaries": ["NO_REAL_ORDERS", "PRODUCTION_OPERATIONS_ENABLED=False"],
        "health_module": "paper_trading.operations.health_v163",
        "gate_module": "release.session_operations_observability_release_gate_v163",
        "cli_prefix": "session-ops",
        "gui_panel": "gui.session_operations_panel",
        "fixture_roots": ["tests/fixtures/session_operations/"],
        "scenario_roots": ["tests/scenarios/session_operations/"],
        "known_limitations": ["Read-only metrics"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.4",
        "release_name": "Operational Analytics and Review",
        "parent_version": "1.6.3",
        "parent_commit": "SEALED",
        "commit": "SEALED",
        "release_category": "analytics",
        "capability_groups": ["analytics", "review", "reporting"],
        "safety_boundaries": ["NO_REAL_ORDERS", "OPERATIONAL_ANALYTICS_AUTO_LIVE_ACTION_ENABLED=False"],
        "health_module": "paper_trading.analytics.health_v164",
        "gate_module": "release.operational_analytics_review_release_gate_v164",
        "cli_prefix": "analytics",
        "gui_panel": "gui.operational_analytics_panel",
        "fixture_roots": ["tests/fixtures/analytics/"],
        "scenario_roots": ["tests/scenarios/analytics/"],
        "known_limitations": ["Analytics only, no automated actions"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.5",
        "release_name": "Failure Injection and Recovery Validation",
        "parent_version": "1.6.4",
        "parent_commit": "SEALED",
        "commit": "SEALED",
        "release_category": "validation",
        "capability_groups": ["failure_injection", "recovery_validation", "chaos"],
        "safety_boundaries": ["NO_REAL_ORDERS", "REAL_FAILURE_INJECTION_ENABLED=False"],
        "health_module": "paper_trading.failure_validation.health_v165",
        "gate_module": "release.failure_injection_recovery_release_gate_v165",
        "cli_prefix": "failure",
        "gui_panel": "gui.failure_injection_panel",
        "fixture_roots": ["tests/fixtures/failure_injection/"],
        "scenario_roots": ["tests/scenarios/failure_injection/"],
        "known_limitations": ["Simulated failures only"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.6",
        "release_name": "Multi-session Coordination",
        "parent_version": "1.6.5",
        "parent_commit": "SEALED",
        "commit": "SEALED",
        "release_category": "coordination",
        "capability_groups": ["multi_session_coordination", "session_registry", "cross_session"],
        "safety_boundaries": ["NO_REAL_ORDERS", "CROSS_SESSION_BROKER_ENABLED=False"],
        "health_module": "paper_trading.multi_session.health_v166",
        "gate_module": "release.multi_session_coordination_release_gate_v166",
        "cli_prefix": "multi-session",
        "gui_panel": "gui.multi_session_panel",
        "fixture_roots": ["tests/fixtures/multi_session/"],
        "scenario_roots": ["tests/scenarios/multi_session/"],
        "known_limitations": ["Paper sessions only"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.6.1",
        "release_name": "Fixture Governance & Safety Marker Hotfix",
        "parent_version": "1.6.6",
        "parent_commit": "SEALED",
        "commit": "SEALED",
        "release_category": "hotfix",
        "capability_groups": ["fixture_governance", "safety_markers"],
        "safety_boundaries": ["NO_REAL_ORDERS"],
        "health_module": None,
        "gate_module": "release.multi_session_fixture_governance_release_gate_v1661",
        "cli_prefix": None,
        "gui_panel": None,
        "fixture_roots": [],
        "scenario_roots": [],
        "known_limitations": ["Governance hotfix only"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.6.2",
        "release_name": "Replay Session Lineage Handler Integrity Hotfix",
        "parent_version": "1.6.6.1",
        "parent_commit": "SEALED",
        "commit": "SEALED",
        "release_category": "hotfix",
        "capability_groups": ["replay_lineage", "session_lineage"],
        "safety_boundaries": ["NO_REAL_ORDERS"],
        "health_module": None,
        "gate_module": None,
        "cli_prefix": None,
        "gui_panel": None,
        "fixture_roots": [],
        "scenario_roots": [],
        "known_limitations": ["Lineage hotfix only"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.7",
        "release_name": "Paper Performance Attribution",
        "parent_version": "1.6.6.2",
        "parent_commit": "SEALED",
        "commit": "SEALED",
        "release_category": "feature",
        "capability_groups": ["performance_attribution", "attribution_engine", "pnl_decomposition"],
        "safety_boundaries": ["NO_REAL_ORDERS", "REAL_PERFORMANCE_ATTRIBUTION_ENABLED=False"],
        "health_module": "paper_trading.performance_attribution.health_v167",
        "gate_module": "release.paper_performance_attribution_release_gate_v167",
        "cli_prefix": "paper-attribution",
        "gui_panel": "gui.paper_attribution_panel",
        "fixture_roots": ["tests/fixtures/paper_attribution/"],
        "scenario_roots": ["tests/scenarios/paper_attribution/"],
        "known_limitations": ["Paper performance only"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.8",
        "release_name": "Operational Integration Hardening",
        "parent_version": "1.6.7",
        "parent_commit": "SEALED",
        "commit": "SEALED",
        "release_category": "hardening",
        "capability_groups": ["operational_integration", "integration_hardening", "bridge_layer"],
        "safety_boundaries": ["NO_REAL_ORDERS", "BROKER_INTEGRATION_ENABLED=False"],
        "health_module": "paper_trading.operational_integration.health_v168",
        "gate_module": "release.operational_integration_hardening_release_gate_v168",
        "cli_prefix": "integration",
        "gui_panel": "gui.operational_integration_panel",
        "fixture_roots": ["tests/fixtures/operational_integration/"],
        "scenario_roots": ["tests/scenarios/operational_integration/"],
        "known_limitations": ["Integration simulation only"],
        "sealed_status": "SEALED",
    },
    {
        "version": "1.6.9",
        "release_name": "Live Paper Trading Stable Rollup",
        "parent_version": "1.6.8",
        "parent_commit": "SEALED",
        "commit": "BASE_RELEASE_1.6.8",
        "release_category": "stable_rollup",
        "capability_groups": ["stable_rollup", "version_matrix", "capability_matrix", "migration_readiness"],
        "safety_boundaries": [
            "NO_REAL_ORDERS=True",
            "PRODUCTION_TRADING_BLOCKED=True",
            "BROKER_EXECUTION_ENABLED=False",
            "LIVE_EXECUTION_ENABLED=False",
        ],
        "health_module": "paper_trading.stable_rollup.health_v169",
        "gate_module": "release.live_paper_trading_stable_rollup_release_gate_v169",
        "cli_prefix": "stable-rollup",
        "gui_panel": "gui.live_paper_trading_stable_rollup_panel",
        "fixture_roots": ["tests/fixtures/stable_rollup/"],
        "scenario_roots": ["tests/scenarios/stable_rollup/"],
        "known_limitations": [
            "Rollup consolidation only",
            "No new trading features",
            "Read-only analysis",
        ],
        "sealed_status": "NOT_SEALED",
    },
]


def get_manifest() -> List[dict]:
    """Return the canonical release manifest."""
    return list(RELEASE_MANIFEST)


def get_release(version: str) -> Optional[dict]:
    """Return the manifest entry for a given version, or None."""
    for r in RELEASE_MANIFEST:
        if r["version"] == version:
            return dict(r)
    return None


def get_all_versions() -> List[str]:
    """Return list of all release versions in manifest order."""
    return [r["version"] for r in RELEASE_MANIFEST]


def validate_manifest() -> dict:
    """Validate manifest uniqueness, parent chain, etc."""
    issues = []
    versions_seen = set()
    names_seen = set()

    for entry in RELEASE_MANIFEST:
        v = entry["version"]
        n = entry["release_name"]
        parent = entry.get("parent_version")

        if v in versions_seen:
            issues.append(f"Duplicate version: {v}")
        versions_seen.add(v)

        if n in names_seen:
            issues.append(f"Duplicate release name: {n}")
        names_seen.add(n)

        if parent is not None and parent not in versions_seen:
            # Parent must already appear before this entry
            issues.append(f"Parent {parent!r} not defined before {v!r}")

    # Check parent chain from v1.6.9 back to v1.6.0
    expected_chain = [
        ("1.6.9", "1.6.8"),
        ("1.6.8", "1.6.7"),
        ("1.6.7", "1.6.6.2"),
        ("1.6.6.2", "1.6.6.1"),
        ("1.6.6.1", "1.6.6"),
        ("1.6.6", "1.6.5"),
        ("1.6.5", "1.6.4"),
        ("1.6.4", "1.6.3"),
        ("1.6.3", "1.6.2"),
        ("1.6.2", "1.6.1.1"),
        ("1.6.1.1", "1.6.1"),
        ("1.6.1", "1.6.0"),
    ]
    version_map = {r["version"]: r for r in RELEASE_MANIFEST}
    for child, parent_v in expected_chain:
        if child in version_map:
            actual_parent = version_map[child].get("parent_version")
            if actual_parent != parent_v:
                issues.append(f"Chain broken: {child} expected parent {parent_v!r}, got {actual_parent!r}")

    total = len(RELEASE_MANIFEST)
    valid = total - len(issues)
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "total": total,
        "valid": valid,
    }
