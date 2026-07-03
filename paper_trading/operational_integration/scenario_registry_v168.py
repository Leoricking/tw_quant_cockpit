"""
paper_trading/operational_integration/scenario_registry_v168.py
Scenario Registry for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
[!] 100+ scenarios with unique IDs, categories, expected statuses.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

CAT_CONTRACT      = "contract"
CAT_DATA_FLOW     = "data_flow"
CAT_LINEAGE       = "lineage"
CAT_TIMESTAMP     = "timestamp"
CAT_IDENTITY      = "identity"
CAT_PIPELINE      = "pipeline"
CAT_RECONCILIATION = "reconciliation"
CAT_DETERMINISM   = "determinism"
CAT_SAFETY        = "safety"
CAT_CROSS_SYSTEM  = "cross_system"

STATUS_PASS    = "PASS"
STATUS_FAIL    = "FAIL"
STATUS_DEGRADED = "DEGRADED"
STATUS_BLOCKED = "BLOCKED"

_SCENARIOS: List[Dict[str, Any]] = [
    # ── Contract scenarios OI-C-001 to OI-C-010 ──────────────────────────────
    {"id": "OI-C-001", "category": CAT_CONTRACT, "name": "market_data_to_session_valid",
     "description": "Valid MarketDataToSession contract payload", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-C-002", "category": CAT_CONTRACT, "name": "market_data_to_session_missing_symbol",
     "description": "MarketDataToSession missing symbol field", "expected_status": STATUS_FAIL, "paper_only": True},
    {"id": "OI-C-003", "category": CAT_CONTRACT, "name": "session_to_strategy_valid",
     "description": "Valid SessionToStrategy contract", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-C-004", "category": CAT_CONTRACT, "name": "strategy_to_portfolio_valid",
     "description": "Valid StrategyToPortfolio contract", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-C-005", "category": CAT_CONTRACT, "name": "portfolio_to_execution_valid",
     "description": "Valid PortfolioToExecution contract", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-C-006", "category": CAT_CONTRACT, "name": "execution_to_analytics_valid",
     "description": "Valid ExecutionToAnalytics contract", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-C-007", "category": CAT_CONTRACT, "name": "contract_forbidden_field_blocked",
     "description": "Contract with forbidden field returns BLOCKED", "expected_status": STATUS_BLOCKED, "paper_only": True},
    {"id": "OI-C-008", "category": CAT_CONTRACT, "name": "analytics_to_attribution_valid",
     "description": "Valid AnalyticsToAttribution contract", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-C-009", "category": CAT_CONTRACT, "name": "attribution_to_coordination_valid",
     "description": "Valid AttributionToCoordination contract", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-C-010", "category": CAT_CONTRACT, "name": "health_to_report_valid",
     "description": "Valid HealthToReport contract", "expected_status": STATUS_PASS, "paper_only": True},
    # ── Data flow scenarios OI-D-001 to OI-D-010 ─────────────────────────────
    {"id": "OI-D-001", "category": CAT_DATA_FLOW, "name": "normal_flow_no_gaps",
     "description": "Normal data flow with no sequence gaps", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-D-002", "category": CAT_DATA_FLOW, "name": "sequence_gap_detected",
     "description": "Data flow with sequence gap", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-D-003", "category": CAT_DATA_FLOW, "name": "duplicate_payload_blocked",
     "description": "Duplicate payload hash detected", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-D-004", "category": CAT_DATA_FLOW, "name": "stale_data_flagged",
     "description": "Stale market data flagged as degraded", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-D-005", "category": CAT_DATA_FLOW, "name": "forbidden_field_leakage",
     "description": "Forbidden field leaked in payload", "expected_status": STATUS_BLOCKED, "paper_only": True},
    {"id": "OI-D-006", "category": CAT_DATA_FLOW, "name": "schema_drift_detected",
     "description": "Schema drift between expected and actual", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-D-007", "category": CAT_DATA_FLOW, "name": "reorder_detected",
     "description": "Out-of-order payload timestamps", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-D-008", "category": CAT_DATA_FLOW, "name": "flow_complete_no_issues",
     "description": "Complete flow with no issues", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-D-009", "category": CAT_DATA_FLOW, "name": "multi_component_flow_tracked",
     "description": "Flow tracked across multiple components", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-D-010", "category": CAT_DATA_FLOW, "name": "dropped_payload_flagged",
     "description": "Dropped payload flagged in tracking", "expected_status": STATUS_DEGRADED, "paper_only": True},
    # ── Lineage scenarios OI-L-001 to OI-L-010 ───────────────────────────────
    {"id": "OI-L-001", "category": CAT_LINEAGE, "name": "complete_lineage_chain",
     "description": "Complete lineage chain from root to leaf", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-L-002", "category": CAT_LINEAGE, "name": "broken_lineage_chain",
     "description": "Missing parent in lineage chain", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-L-003", "category": CAT_LINEAGE, "name": "fixture_contamination_detected",
     "description": "Fixture lineage leaked into production chain", "expected_status": STATUS_BLOCKED, "paper_only": True},
    {"id": "OI-L-004", "category": CAT_LINEAGE, "name": "duplicate_lineage_id",
     "description": "Duplicate lineage ID detected", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-L-005", "category": CAT_LINEAGE, "name": "stale_lineage_record",
     "description": "Lineage record older than max_age", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-L-006", "category": CAT_LINEAGE, "name": "mock_contamination_detected",
     "description": "Mock data lineage in real run chain", "expected_status": STATUS_BLOCKED, "paper_only": True},
    {"id": "OI-L-007", "category": CAT_LINEAGE, "name": "lineage_rebuild_succeeds",
     "description": "Lineage chain successfully rebuilt", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-L-008", "category": CAT_LINEAGE, "name": "paper_lineage_clean",
     "description": "Paper-only lineage with no contamination", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-L-009", "category": CAT_LINEAGE, "name": "lineage_version_mismatch",
     "description": "Lineage version mismatch across components", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-L-010", "category": CAT_LINEAGE, "name": "lineage_cycle_detected",
     "description": "Cyclic lineage reference detected", "expected_status": STATUS_FAIL, "paper_only": True},
    # ── Timestamp scenarios OI-T-001 to OI-T-010 ─────────────────────────────
    {"id": "OI-T-001", "category": CAT_TIMESTAMP, "name": "valid_aware_timestamps",
     "description": "All timestamps are timezone-aware and ordered", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-T-002", "category": CAT_TIMESTAMP, "name": "future_timestamp_rejected",
     "description": "Future timestamp flagged as invalid", "expected_status": STATUS_FAIL, "paper_only": True},
    {"id": "OI-T-003", "category": CAT_TIMESTAMP, "name": "naive_timestamp_flagged",
     "description": "Naive (no timezone) timestamp flagged", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-T-004", "category": CAT_TIMESTAMP, "name": "reversed_timestamps_rejected",
     "description": "Period start > end rejected", "expected_status": STATUS_FAIL, "paper_only": True},
    {"id": "OI-T-005", "category": CAT_TIMESTAMP, "name": "timezone_mismatch_detected",
     "description": "Timezone mismatch between components detected", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-T-006", "category": CAT_TIMESTAMP, "name": "out_of_order_timestamps",
     "description": "Out-of-order sequence of timestamps", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-T-007", "category": CAT_TIMESTAMP, "name": "period_boundary_violated",
     "description": "Event outside period boundary", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-T-008", "category": CAT_TIMESTAMP, "name": "stale_timestamp_flagged",
     "description": "Timestamp too old, flagged as stale", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-T-009", "category": CAT_TIMESTAMP, "name": "timezone_normalization",
     "description": "Timestamps normalized to Asia/Taipei", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-T-010", "category": CAT_TIMESTAMP, "name": "period_mismatch",
     "description": "Period mismatch across components", "expected_status": STATUS_DEGRADED, "paper_only": True},
    # ── Identity scenarios OI-I-001 to OI-I-010 ──────────────────────────────
    {"id": "OI-I-001", "category": CAT_IDENTITY, "name": "unique_identities_valid",
     "description": "All entity identities unique and valid", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-I-002", "category": CAT_IDENTITY, "name": "duplicate_run_id_detected",
     "description": "Duplicate run ID across sessions", "expected_status": STATUS_FAIL, "paper_only": True},
    {"id": "OI-I-003", "category": CAT_IDENTITY, "name": "session_collision_detected",
     "description": "Session collision between components", "expected_status": STATUS_FAIL, "paper_only": True},
    {"id": "OI-I-004", "category": CAT_IDENTITY, "name": "orphan_identity_flagged",
     "description": "Identity without valid session assignment", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-I-005", "category": CAT_IDENTITY, "name": "fixture_identity_leaked",
     "description": "Fixture identity leaked into real run", "expected_status": STATUS_BLOCKED, "paper_only": True},
    {"id": "OI-I-006", "category": CAT_IDENTITY, "name": "symbol_normalized",
     "description": "Symbol normalized to canonical form", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-I-007", "category": CAT_IDENTITY, "name": "conflicting_identities",
     "description": "Conflicting identity assignments detected", "expected_status": STATUS_FAIL, "paper_only": True},
    {"id": "OI-I-008", "category": CAT_IDENTITY, "name": "missing_strategy_id",
     "description": "Missing strategy ID in signal chain", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-I-009", "category": CAT_IDENTITY, "name": "stale_identity_record",
     "description": "Identity record not updated within threshold", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-I-010", "category": CAT_IDENTITY, "name": "portfolio_session_mismatch",
     "description": "Portfolio ID mismatch with session", "expected_status": STATUS_FAIL, "paper_only": True},
    # ── Pipeline scenarios OI-P-001 to OI-P-010 ──────────────────────────────
    {"id": "OI-P-001", "category": CAT_PIPELINE, "name": "all_stages_complete",
     "description": "All 14 pipeline stages complete successfully", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-P-002", "category": CAT_PIPELINE, "name": "context_load_failure",
     "description": "Context load stage fails", "expected_status": STATUS_FAIL, "paper_only": True},
    {"id": "OI-P-003", "category": CAT_PIPELINE, "name": "contract_validate_degraded",
     "description": "Contract validation returns degraded", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-P-004", "category": CAT_PIPELINE, "name": "registry_validate_missing",
     "description": "Component registry has missing dependencies", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-P-005", "category": CAT_PIPELINE, "name": "bridge_connect_fail",
     "description": "Bridge connection failure", "expected_status": STATUS_FAIL, "paper_only": True},
    {"id": "OI-P-006", "category": CAT_PIPELINE, "name": "scorecard_below_threshold",
     "description": "Scorecard falls below passing threshold", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-P-007", "category": CAT_PIPELINE, "name": "failure_isolation_blocks_cascade",
     "description": "Failure isolated to prevent cascade", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-P-008", "category": CAT_PIPELINE, "name": "degraded_propagation_correct",
     "description": "Degraded status propagated to downstream", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-P-009", "category": CAT_PIPELINE, "name": "report_generated_complete",
     "description": "Full report generated with all sections", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-P-010", "category": CAT_PIPELINE, "name": "pipeline_idempotent",
     "description": "Pipeline produces same result on re-run", "expected_status": STATUS_PASS, "paper_only": True},
    # ── Reconciliation scenarios OI-R-001 to OI-R-010 ────────────────────────
    {"id": "OI-R-001", "category": CAT_RECONCILIATION, "name": "market_data_session_reconcile",
     "description": "Market data rows match session input rows", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-R-002", "category": CAT_RECONCILIATION, "name": "execution_analytics_reconcile",
     "description": "Executions match analytics trades", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-R-003", "category": CAT_RECONCILIATION, "name": "pnl_attribution_reconcile",
     "description": "Analytics PnL matches attribution PnL", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-R-004", "category": CAT_RECONCILIATION, "name": "pnl_mismatch_degraded",
     "description": "PnL mismatch beyond tolerance returns DEGRADED", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-R-005", "category": CAT_RECONCILIATION, "name": "reconcile_rounding_tolerance",
     "description": "Reconciliation with rounding within tolerance", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-R-006", "category": CAT_RECONCILIATION, "name": "strategy_portfolio_reconcile",
     "description": "Strategy allocations match portfolio positions", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-R-007", "category": CAT_RECONCILIATION, "name": "health_aggregate_reconcile",
     "description": "Component health matches aggregate health", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-R-008", "category": CAT_RECONCILIATION, "name": "recovery_failure_reconcile",
     "description": "Failure events match recovery records", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-R-009", "category": CAT_RECONCILIATION, "name": "reconcile_insufficient_data",
     "description": "Reconciliation with insufficient data", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-R-010", "category": CAT_RECONCILIATION, "name": "report_status_aggregate",
     "description": "Aggregate health matches report status", "expected_status": STATUS_PASS, "paper_only": True},
    # ── Determinism scenarios OI-DET-001 to OI-DET-010 ───────────────────────
    {"id": "OI-DET-001", "category": CAT_DETERMINISM, "name": "same_seed_same_output",
     "description": "Same seed produces identical output", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-DET-002", "category": CAT_DETERMINISM, "name": "stage_order_stable",
     "description": "Stage ordering is stable across runs", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-DET-003", "category": CAT_DETERMINISM, "name": "score_stable_across_runs",
     "description": "Scorecard total stable across replays", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-DET-004", "category": CAT_DETERMINISM, "name": "hash_stable_same_input",
     "description": "Result hash stable for same input", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-DET-005", "category": CAT_DETERMINISM, "name": "no_current_time_dependency",
     "description": "Output does not depend on current time", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-DET-006", "category": CAT_DETERMINISM, "name": "no_network_dependency",
     "description": "No network calls in deterministic path", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-DET-007", "category": CAT_DETERMINISM, "name": "fixture_hash_stable",
     "description": "Fixture hash stable after reload", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-DET-008", "category": CAT_DETERMINISM, "name": "snapshot_stable",
     "description": "State snapshot stable for same state", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-DET-009", "category": CAT_DETERMINISM, "name": "report_stable_same_input",
     "description": "Report content stable for same input", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-DET-010", "category": CAT_DETERMINISM, "name": "non_deterministic_flagged",
     "description": "Non-deterministic output correctly flagged", "expected_status": STATUS_FAIL, "paper_only": True},
    # ── Safety scenarios OI-S-001 to OI-S-010 ────────────────────────────────
    {"id": "OI-S-001", "category": CAT_SAFETY, "name": "all_safety_flags_correct",
     "description": "All safety flags at expected values", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-S-002", "category": CAT_SAFETY, "name": "broker_disabled",
     "description": "Broker integration disabled", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-S-003", "category": CAT_SAFETY, "name": "no_real_orders",
     "description": "No real orders flag enabled", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-S-004", "category": CAT_SAFETY, "name": "forbidden_field_blocked",
     "description": "Forbidden field in input blocked", "expected_status": STATUS_BLOCKED, "paper_only": True},
    {"id": "OI-S-005", "category": CAT_SAFETY, "name": "production_trading_blocked",
     "description": "Production trading correctly blocked", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-S-006", "category": CAT_SAFETY, "name": "live_markers_rejected",
     "description": "Live/real mode markers rejected", "expected_status": STATUS_BLOCKED, "paper_only": True},
    {"id": "OI-S-007", "category": CAT_SAFETY, "name": "network_disabled",
     "description": "Network integration disabled", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-S-008", "category": CAT_SAFETY, "name": "auto_capital_disabled",
     "description": "Auto capital reallocation disabled", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-S-009", "category": CAT_SAFETY, "name": "process_control_disabled",
     "description": "Auto process control disabled", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-S-010", "category": CAT_SAFETY, "name": "safety_audit_passes",
     "description": "Full safety audit returns all_safe=True", "expected_status": STATUS_PASS, "paper_only": True},
    # ── Cross-system scenarios OI-X-001 to OI-X-010 ──────────────────────────
    {"id": "OI-X-001", "category": CAT_CROSS_SYSTEM, "name": "end_to_end_research_run",
     "description": "Full end-to-end integration run for research", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-X-002", "category": CAT_CROSS_SYSTEM, "name": "attribution_integration_valid",
     "description": "Attribution integrates with analytics correctly", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-X-003", "category": CAT_CROSS_SYSTEM, "name": "coordination_recovery_link",
     "description": "Coordination correctly links to recovery", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-X-004", "category": CAT_CROSS_SYSTEM, "name": "multi_session_integrity",
     "description": "Multi-session run maintains identity integrity", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-X-005", "category": CAT_CROSS_SYSTEM, "name": "failure_cascade_blocked",
     "description": "Failure cascade blocked by isolation", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-X-006", "category": CAT_CROSS_SYSTEM, "name": "cross_component_reconcile",
     "description": "Cross-component reconciliation passes", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-X-007", "category": CAT_CROSS_SYSTEM, "name": "replay_regression_stable",
     "description": "Regression replay produces same results", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-X-008", "category": CAT_CROSS_SYSTEM, "name": "degraded_propagation_end_to_end",
     "description": "Degraded status propagated end to end", "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "OI-X-009", "category": CAT_CROSS_SYSTEM, "name": "fixture_governance_clean",
     "description": "All fixtures pass governance checks", "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "OI-X-010", "category": CAT_CROSS_SYSTEM, "name": "scorecard_grade_a",
     "description": "Full integration achieves Grade A score", "expected_status": STATUS_PASS, "paper_only": True},
]

assert len(_SCENARIOS) >= 100, f"Need at least 100 scenarios, got {len(_SCENARIOS)}"


class ScenarioRegistry:
    """Registry for integration scenarios. Research only."""

    def all_scenarios(self) -> List[Dict[str, Any]]:
        """Return all scenarios."""
        return list(_SCENARIOS)

    def count(self) -> int:
        """Return total number of scenarios."""
        return len(_SCENARIOS)

    def list_categories(self) -> List[str]:
        """Return sorted list of unique categories."""
        return sorted(set(s["category"] for s in _SCENARIOS))

    def get_by_category(self, cat: str) -> List[Dict[str, Any]]:
        """Return scenarios filtered by category."""
        return [s for s in _SCENARIOS if s["category"] == cat]

    def summarize(self) -> Dict[str, Any]:
        """Return summary of scenario registry."""
        cats = self.list_categories()
        return {
            "total_scenarios": self.count(),
            "categories": cats,
            "category_counts": {c: len(self.get_by_category(c)) for c in cats},
            "paper_only": True,
            "research_only": True,
        }
