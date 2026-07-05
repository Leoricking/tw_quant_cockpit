"""
paper_trading/stable_rollup/scenario_registry_v169.py
Scenario registry for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
80+ scenarios. No skip. No xfail.
"""
from __future__ import annotations
from typing import List, Optional, Dict

SCENARIO_REGISTRY: List[dict] = [
    # ── Release Identity (8) ──────────────────────────────────────────────────
    {"scenario_id": "sr_ri_001", "category": "release_identity", "name": "exact_version", "description": "Package VERSION must equal 1.6.9", "expected_status": "PASS", "fixture_id": "sr_001", "deterministic_seed": 42},
    {"scenario_id": "sr_ri_002", "category": "release_identity", "name": "exact_release_name", "description": "RELEASE_NAME must be Live Paper Trading Stable Rollup", "expected_status": "PASS", "fixture_id": "sr_002", "deterministic_seed": 42},
    {"scenario_id": "sr_ri_003", "category": "release_identity", "name": "base_release", "description": "BASE_RELEASE must reference v1.6.8", "expected_status": "PASS", "fixture_id": "sr_003", "deterministic_seed": 42},
    {"scenario_id": "sr_ri_004", "category": "release_identity", "name": "schema_version", "description": "SCHEMA_VERSION must be 169", "expected_status": "PASS", "fixture_id": "sr_004", "deterministic_seed": 42},
    {"scenario_id": "sr_ri_005", "category": "release_identity", "name": "policy_version", "description": "POLICY_VERSION must be 1.6.9-live-paper-stable-rollup", "expected_status": "PASS", "fixture_id": "sr_005", "deterministic_seed": 42},
    {"scenario_id": "sr_ri_006", "category": "release_identity", "name": "known_release_name", "description": "Release name must be in KNOWN_RELEASE_NAMES", "expected_status": "PASS", "fixture_id": "sr_006", "deterministic_seed": 42},
    {"scenario_id": "sr_ri_007", "category": "release_identity", "name": "minimum_version_met", "description": "check_minimum_version(1.6.9) must return True", "expected_status": "PASS", "fixture_id": "sr_007", "deterministic_seed": 42},
    {"scenario_id": "sr_ri_008", "category": "release_identity", "name": "version_info_dict", "description": "get_version_info() returns expected keys", "expected_status": "PASS", "fixture_id": "sr_008", "deterministic_seed": 42},
    # ── Capability (8) ───────────────────────────────────────────────────────
    {"scenario_id": "sr_cap_001", "category": "capability", "name": "matrix_count", "description": "Capability matrix has >= 19 entries", "expected_status": "PASS", "fixture_id": "sr_009", "deterministic_seed": 42},
    {"scenario_id": "sr_cap_002", "category": "capability", "name": "no_production_ready", "description": "No capability is production_ready=True", "expected_status": "PASS", "fixture_id": "sr_010", "deterministic_seed": 42},
    {"scenario_id": "sr_cap_003", "category": "capability", "name": "all_paper_only", "description": "All capabilities have paper_only=True", "expected_status": "PASS", "fixture_id": "sr_011", "deterministic_seed": 42},
    {"scenario_id": "sr_cap_004", "category": "capability", "name": "paper_trading_present", "description": "paper_trading capability exists in matrix", "expected_status": "PASS", "fixture_id": "sr_012", "deterministic_seed": 42},
    {"scenario_id": "sr_cap_005", "category": "capability", "name": "stable_rollup_present", "description": "stable_rollup capability exists in matrix", "expected_status": "PASS", "fixture_id": "sr_013", "deterministic_seed": 42},
    {"scenario_id": "sr_cap_006", "category": "capability", "name": "unique_capabilities", "description": "All capability names are unique", "expected_status": "PASS", "fixture_id": "sr_014", "deterministic_seed": 42},
    {"scenario_id": "sr_cap_007", "category": "capability", "name": "capability_validate_pass", "description": "validate_matrix() returns PASS", "expected_status": "PASS", "fixture_id": "sr_015", "deterministic_seed": 42},
    {"scenario_id": "sr_cap_008", "category": "capability", "name": "get_capability_returns_dict", "description": "get_capability() returns a dict for known name", "expected_status": "PASS", "fixture_id": "sr_016", "deterministic_seed": 42},
    # ── Safety (8) ───────────────────────────────────────────────────────────
    {"scenario_id": "sr_saf_001", "category": "safety", "name": "no_real_orders_flag", "description": "NO_REAL_ORDERS=True in package init", "expected_status": "PASS", "fixture_id": "sr_017", "deterministic_seed": 42},
    {"scenario_id": "sr_saf_002", "category": "safety", "name": "broker_disabled", "description": "BROKER_EXECUTION_ENABLED=False", "expected_status": "PASS", "fixture_id": "sr_018", "deterministic_seed": 42},
    {"scenario_id": "sr_saf_003", "category": "safety", "name": "production_blocked", "description": "PRODUCTION_TRADING_BLOCKED=True", "expected_status": "PASS", "fixture_id": "sr_019", "deterministic_seed": 42},
    {"scenario_id": "sr_saf_004", "category": "safety", "name": "is_safe_true", "description": "is_safe() returns True", "expected_status": "PASS", "fixture_id": "sr_020", "deterministic_seed": 42},
    {"scenario_id": "sr_saf_005", "category": "safety", "name": "safety_matrix_count", "description": "Safety matrix has >= 20 entries", "expected_status": "PASS", "fixture_id": "sr_021", "deterministic_seed": 42},
    {"scenario_id": "sr_saf_006", "category": "safety", "name": "no_dangerous_capabilities", "description": "count_dangerous_capabilities() == 0", "expected_status": "PASS", "fixture_id": "sr_022", "deterministic_seed": 42},
    {"scenario_id": "sr_saf_007", "category": "safety", "name": "validate_safety_pass", "description": "validate_safety() status == PASS", "expected_status": "PASS", "fixture_id": "sr_023", "deterministic_seed": 42},
    {"scenario_id": "sr_saf_008", "category": "safety", "name": "safety_matrix_validate_pass", "description": "safety_matrix_v169.validate_matrix() returns PASS", "expected_status": "PASS", "fixture_id": "sr_024", "deterministic_seed": 42},
    # ── Compatibility (8) ────────────────────────────────────────────────────
    {"scenario_id": "sr_cmp_001", "category": "compatibility", "name": "edge_count_11", "description": "Compatibility matrix has exactly 11 edges", "expected_status": "PASS", "fixture_id": "sr_025", "deterministic_seed": 42},
    {"scenario_id": "sr_cmp_002", "category": "compatibility", "name": "all_edges_compatible", "description": "All edges have overall_status=COMPATIBLE", "expected_status": "PASS", "fixture_id": "sr_026", "deterministic_seed": 42},
    {"scenario_id": "sr_cmp_003", "category": "compatibility", "name": "edge_168_to_169", "description": "Edge v1.6.8 -> v1.6.9 exists and is COMPATIBLE", "expected_status": "PASS", "fixture_id": "sr_027", "deterministic_seed": 42},
    {"scenario_id": "sr_cmp_004", "category": "compatibility", "name": "edge_160_to_161", "description": "Edge v1.6.0 -> v1.6.1 exists", "expected_status": "PASS", "fixture_id": "sr_028", "deterministic_seed": 42},
    {"scenario_id": "sr_cmp_005", "category": "compatibility", "name": "validate_matrix_pass", "description": "validate_matrix() returns PASS", "expected_status": "PASS", "fixture_id": "sr_029", "deterministic_seed": 42},
    {"scenario_id": "sr_cmp_006", "category": "compatibility", "name": "get_edge_returns_dict", "description": "get_edge() returns a dict for valid edge", "expected_status": "PASS", "fixture_id": "sr_030", "deterministic_seed": 42},
    {"scenario_id": "sr_cmp_007", "category": "compatibility", "name": "no_duplicate_edges", "description": "No duplicate from/to version pairs", "expected_status": "PASS", "fixture_id": "sr_031", "deterministic_seed": 42},
    {"scenario_id": "sr_cmp_008", "category": "compatibility", "name": "safety_compat_all_compatible", "description": "All edges have safety_compatibility=COMPATIBLE", "expected_status": "PASS", "fixture_id": "sr_032", "deterministic_seed": 42},
    # ── Aggregation (8) ──────────────────────────────────────────────────────
    {"scenario_id": "sr_agg_001", "category": "aggregation", "name": "health_aggregator_runs", "description": "health_aggregator_v169.run() returns dict with status", "expected_status": "PASS", "fixture_id": "sr_033", "deterministic_seed": 42},
    {"scenario_id": "sr_agg_002", "category": "aggregation", "name": "gate_aggregator_runs", "description": "gate_aggregator_v169.run() returns dict with status", "expected_status": "PASS", "fixture_id": "sr_034", "deterministic_seed": 42},
    {"scenario_id": "sr_agg_003", "category": "aggregation", "name": "cli_aggregator_runs", "description": "cli_aggregator_v169.run() returns dict", "expected_status": "PASS", "fixture_id": "sr_035", "deterministic_seed": 42},
    {"scenario_id": "sr_agg_004", "category": "aggregation", "name": "gui_aggregator_runs", "description": "gui_aggregator_v169.run() returns dict", "expected_status": "PASS", "fixture_id": "sr_036", "deterministic_seed": 42},
    {"scenario_id": "sr_agg_005", "category": "aggregation", "name": "fixture_aggregator_runs", "description": "fixture_aggregator_v169.run() returns dict", "expected_status": "PASS", "fixture_id": "sr_037", "deterministic_seed": 42},
    {"scenario_id": "sr_agg_006", "category": "aggregation", "name": "scenario_aggregator_runs", "description": "scenario_aggregator_v169.run() returns dict", "expected_status": "PASS", "fixture_id": "sr_038", "deterministic_seed": 42},
    {"scenario_id": "sr_agg_007", "category": "aggregation", "name": "lineage_aggregator_runs", "description": "lineage_aggregator_v169.run() returns dict", "expected_status": "PASS", "fixture_id": "sr_039", "deterministic_seed": 42},
    {"scenario_id": "sr_agg_008", "category": "aggregation", "name": "contract_aggregator_runs", "description": "contract_aggregator_v169.run() returns dict", "expected_status": "PASS", "fixture_id": "sr_040", "deterministic_seed": 42},
    # ── Reconciliation (8) ───────────────────────────────────────────────────
    {"scenario_id": "sr_rec_001", "category": "reconciliation", "name": "releases_reconcile", "description": "releases reconciliation expected=13", "expected_status": "PASS", "fixture_id": "sr_041", "deterministic_seed": 42},
    {"scenario_id": "sr_rec_002", "category": "reconciliation", "name": "capabilities_reconcile", "description": "capabilities reconciliation expected>=20", "expected_status": "PASS", "fixture_id": "sr_042", "deterministic_seed": 42},
    {"scenario_id": "sr_rec_003", "category": "reconciliation", "name": "safety_items_reconcile", "description": "safety_items reconciliation expected=20", "expected_status": "PASS", "fixture_id": "sr_043", "deterministic_seed": 42},
    {"scenario_id": "sr_rec_004", "category": "reconciliation", "name": "test_baseline_reconcile", "description": "test baseline expected=11465", "expected_status": "PASS", "fixture_id": "sr_044", "deterministic_seed": 42},
    {"scenario_id": "sr_rec_005", "category": "reconciliation", "name": "cli_reconcile", "description": "CLI commands reconciliation expected>=26", "expected_status": "PASS", "fixture_id": "sr_045", "deterministic_seed": 42},
    {"scenario_id": "sr_rec_006", "category": "reconciliation", "name": "reconcile_all_pass", "description": "reconcile_all() all entries have READY status", "expected_status": "PASS", "fixture_id": "sr_046", "deterministic_seed": 42},
    {"scenario_id": "sr_rec_007", "category": "reconciliation", "name": "reconcile_no_residual", "description": "reconcile_releases residual == 0", "expected_status": "PASS", "fixture_id": "sr_047", "deterministic_seed": 42},
    {"scenario_id": "sr_rec_008", "category": "reconciliation", "name": "reconcile_confidence_high", "description": "releases reconcile confidence == HIGH", "expected_status": "PASS", "fixture_id": "sr_048", "deterministic_seed": 42},
    # ── Migration (8) ────────────────────────────────────────────────────────
    {"scenario_id": "sr_mig_001", "category": "migration", "name": "safety_boundary_check", "description": "safety_boundaries check passes", "expected_status": "PASS", "fixture_id": "sr_049", "deterministic_seed": 42},
    {"scenario_id": "sr_mig_002", "category": "migration", "name": "stable_identity_check", "description": "stable_identity check passes", "expected_status": "PASS", "fixture_id": "sr_050", "deterministic_seed": 42},
    {"scenario_id": "sr_mig_003", "category": "migration", "name": "api_stability_check", "description": "api_stability check passes", "expected_status": "PASS", "fixture_id": "sr_051", "deterministic_seed": 42},
    {"scenario_id": "sr_mig_004", "category": "migration", "name": "rollback_traceability_check", "description": "rollback_traceability check passes", "expected_status": "PASS", "fixture_id": "sr_052", "deterministic_seed": 42},
    {"scenario_id": "sr_mig_005", "category": "migration", "name": "deterministic_replay_check", "description": "deterministic_replay check passes", "expected_status": "PASS", "fixture_id": "sr_053", "deterministic_seed": 42},
    {"scenario_id": "sr_mig_006", "category": "migration", "name": "get_readiness_not_blocked", "description": "get_readiness() != BLOCKED", "expected_status": "PASS", "fixture_id": "sr_054", "deterministic_seed": 42},
    {"scenario_id": "sr_mig_007", "category": "migration", "name": "compatibility_check_passes", "description": "compatibility check passes in assessment", "expected_status": "PASS", "fixture_id": "sr_055", "deterministic_seed": 42},
    {"scenario_id": "sr_mig_008", "category": "migration", "name": "assess_returns_summary", "description": "assess() returns MigrationReadinessSummary", "expected_status": "PASS", "fixture_id": "sr_056", "deterministic_seed": 42},
    # ── Contract (8) ─────────────────────────────────────────────────────────
    {"scenario_id": "sr_con_001", "category": "contract", "name": "contract_run_pass", "description": "StableContract.run() returns all_pass=True", "expected_status": "PASS", "fixture_id": "sr_057", "deterministic_seed": 42},
    {"scenario_id": "sr_con_002", "category": "contract", "name": "no_real_orders_contract", "description": "validate_no_real_orders() passes", "expected_status": "PASS", "fixture_id": "sr_058", "deterministic_seed": 42},
    {"scenario_id": "sr_con_003", "category": "contract", "name": "safety_contract_pass", "description": "validate_safety() contract passes", "expected_status": "PASS", "fixture_id": "sr_059", "deterministic_seed": 42},
    {"scenario_id": "sr_con_004", "category": "contract", "name": "read_only_contract_pass", "description": "validate_read_only() passes", "expected_status": "PASS", "fixture_id": "sr_060", "deterministic_seed": 42},
    {"scenario_id": "sr_con_005", "category": "contract", "name": "release_identity_contract_pass", "description": "validate_release_identity() passes", "expected_status": "PASS", "fixture_id": "sr_061", "deterministic_seed": 42},
    {"scenario_id": "sr_con_006", "category": "contract", "name": "backward_compat_contract_pass", "description": "validate_backward_compatibility() passes", "expected_status": "PASS", "fixture_id": "sr_062", "deterministic_seed": 42},
    {"scenario_id": "sr_con_007", "category": "contract", "name": "determinism_contract_pass", "description": "validate_determinism() passes", "expected_status": "PASS", "fixture_id": "sr_063", "deterministic_seed": 42},
    {"scenario_id": "sr_con_008", "category": "contract", "name": "capability_contract_pass", "description": "validate_capability() passes", "expected_status": "PASS", "fixture_id": "sr_064", "deterministic_seed": 42},
    # ── Manifest (8) ─────────────────────────────────────────────────────────
    {"scenario_id": "sr_man_001", "category": "manifest", "name": "manifest_count_13", "description": "Manifest has exactly 13 releases", "expected_status": "PASS", "fixture_id": "sr_065", "deterministic_seed": 42},
    {"scenario_id": "sr_man_002", "category": "manifest", "name": "manifest_v160_present", "description": "v1.6.0 is in manifest", "expected_status": "PASS", "fixture_id": "sr_066", "deterministic_seed": 42},
    {"scenario_id": "sr_man_003", "category": "manifest", "name": "manifest_v169_present", "description": "v1.6.9 is in manifest", "expected_status": "PASS", "fixture_id": "sr_067", "deterministic_seed": 42},
    {"scenario_id": "sr_man_004", "category": "manifest", "name": "manifest_validate_pass", "description": "validate_manifest() status=PASS", "expected_status": "PASS", "fixture_id": "sr_068", "deterministic_seed": 42},
    {"scenario_id": "sr_man_005", "category": "manifest", "name": "manifest_unique_versions", "description": "All versions in manifest are unique", "expected_status": "PASS", "fixture_id": "sr_069", "deterministic_seed": 42},
    {"scenario_id": "sr_man_006", "category": "manifest", "name": "manifest_parent_chain", "description": "Parent chain from v1.6.9 back to v1.6.0 is intact", "expected_status": "PASS", "fixture_id": "sr_070", "deterministic_seed": 42},
    {"scenario_id": "sr_man_007", "category": "manifest", "name": "manifest_hotfixes_sealed", "description": "All hotfix releases have sealed_status=SEALED", "expected_status": "PASS", "fixture_id": "sr_071", "deterministic_seed": 42},
    {"scenario_id": "sr_man_008", "category": "manifest", "name": "manifest_get_release", "description": "get_release(1.6.9) returns entry with correct name", "expected_status": "PASS", "fixture_id": "sr_072", "deterministic_seed": 42},
    # ── Scorecard (8) ────────────────────────────────────────────────────────
    {"scenario_id": "sr_sco_001", "category": "scorecard", "name": "weights_sum_100", "description": "SCORE_WEIGHTS sum to 100", "expected_status": "PASS", "fixture_id": "sr_073", "deterministic_seed": 42},
    {"scenario_id": "sr_sco_002", "category": "scorecard", "name": "safety_failure_blocked", "description": "Safety failure → BLOCKED grade", "expected_status": "PASS", "fixture_id": "sr_074", "deterministic_seed": 42},
    {"scenario_id": "sr_sco_003", "category": "scorecard", "name": "compute_returns_score", "description": "compute() returns StableRollupScore", "expected_status": "PASS", "fixture_id": "sr_075", "deterministic_seed": 42},
    {"scenario_id": "sr_sco_004", "category": "scorecard", "name": "score_not_for_real_trading", "description": "score.not_for_real_trading=True", "expected_status": "PASS", "fixture_id": "sr_076", "deterministic_seed": 42},
    {"scenario_id": "sr_sco_005", "category": "scorecard", "name": "compute_scorecard_runs", "description": "compute_scorecard() returns a StableRollupScore", "expected_status": "PASS", "fixture_id": "sr_077", "deterministic_seed": 42},
    {"scenario_id": "sr_sco_006", "category": "scorecard", "name": "safety_weight_is_20", "description": "safety weight is the largest weight", "expected_status": "PASS", "fixture_id": "sr_078", "deterministic_seed": 42},
    {"scenario_id": "sr_sco_007", "category": "scorecard", "name": "score_grade_exists", "description": "score.grade is a non-empty string", "expected_status": "PASS", "fixture_id": "sr_079", "deterministic_seed": 42},
    {"scenario_id": "sr_sco_008", "category": "scorecard", "name": "component_scores_dict", "description": "score.component_scores is a dict", "expected_status": "PASS", "fixture_id": "sr_080", "deterministic_seed": 42},
]

assert len(SCENARIO_REGISTRY) >= 80, f"Need >= 80 scenarios, got {len(SCENARIO_REGISTRY)}"


def get_registry() -> List[dict]:
    """Return all scenarios."""
    return list(SCENARIO_REGISTRY)


def get_scenario(scenario_id: str) -> Optional[dict]:
    """Return scenario by ID, or None."""
    for s in SCENARIO_REGISTRY:
        if s["scenario_id"] == scenario_id:
            return dict(s)
    return None


def get_by_category(category: str) -> List[dict]:
    """Return all scenarios in a category."""
    return [dict(s) for s in SCENARIO_REGISTRY if s["category"] == category]


def validate_registry() -> Dict[str, object]:
    """Validate scenario registry."""
    issues = []
    ids_seen = set()
    fixture_ids_seen = set()

    for s in SCENARIO_REGISTRY:
        sid = s.get("scenario_id", "")
        if not sid:
            issues.append("scenario missing scenario_id")
            continue
        if sid in ids_seen:
            issues.append(f"Duplicate scenario_id: {sid!r}")
        ids_seen.add(sid)

        fid = s.get("fixture_id", "")
        if fid and fid in fixture_ids_seen:
            # Fixtures can be shared, not an error
            pass
        fixture_ids_seen.add(fid)

        if s.get("expected_status") not in ("PASS", "FAIL"):
            issues.append(f"Scenario {sid!r}: invalid expected_status {s.get('expected_status')!r}")

        if not s.get("category"):
            issues.append(f"Scenario {sid!r}: missing category")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "total": len(SCENARIO_REGISTRY),
        "unique_ids": len(ids_seen),
    }
