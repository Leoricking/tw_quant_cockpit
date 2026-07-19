"""
paper_trading/small_capital_strategy/strategy_governance_dashboard_scenarios_v197.py
Scenarios for Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only. Quality Analytics Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_BASE = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "governance_analytics_only": True,
    "dashboard_only": True,
    "quality_analytics_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_strategy_mutation": True,
    "no_automatic_rollback": True,
    "no_live_strategy_activation": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
    "schema_version": "197",
}


def _s(sid: str, name: str, category: str, **kwargs) -> Dict[str, Any]:
    return {**_BASE, "id": sid, "scenario_id": sid, "name": name, "category": category, **kwargs}


_SCENARIOS: List[Dict[str, Any]] = [
    # ── Complete governance dashboard (1-5) ──────────────────────────────────
    _s("SP197-001", "complete_governance_dashboard_full_history", "complete_governance_dashboard",
       registry_source="REG-001", analytics_window="FULL_HISTORY",
       panels_count=12, all_panels_rendered=True, quality_analytics_complete=True),
    _s("SP197-002", "complete_governance_dashboard_weekly", "complete_governance_dashboard",
       registry_source="REG-001", analytics_window="WEEKLY",
       panels_count=12, evidence_coverage_panel=True),
    _s("SP197-003", "complete_governance_dashboard_monthly", "complete_governance_dashboard",
       registry_source="REG-001", analytics_window="MONTHLY",
       panels_count=12, decision_outcome_panel=True),
    _s("SP197-004", "complete_governance_dashboard_quarterly", "complete_governance_dashboard",
       registry_source="REG-002", analytics_window="QUARTERLY",
       panels_count=12, governance_violations_panel=True),
    _s("SP197-005", "complete_governance_dashboard_daily", "complete_governance_dashboard",
       registry_source="REG-002", analytics_window="DAILY",
       panels_count=12, audit_trail_health_panel=True),

    # ── Excellent decision quality (6-10) ────────────────────────────────────
    _s("SP197-006", "excellent_quality_high_evidence_coverage", "excellent_decision_quality",
       decision_id="DEC-001", composite_score=0.92, grade="EXCELLENT",
       evidence_coverage_score=0.95, rationale_completeness_score=0.90),
    _s("SP197-007", "excellent_quality_complete_audit_trail", "excellent_decision_quality",
       decision_id="DEC-002", composite_score=0.88, grade="EXCELLENT",
       audit_trail_completeness_score=0.99, lineage_completeness_score=0.95),
    _s("SP197-008", "excellent_quality_full_governance_pass", "excellent_decision_quality",
       decision_id="DEC-003", composite_score=0.90, grade="EXCELLENT",
       governance_violation_score=1.0, checklist_completeness_score=0.95),
    _s("SP197-009", "excellent_quality_paper_only_safety_max", "excellent_decision_quality",
       decision_id="DEC-004", composite_score=0.87, grade="EXCELLENT",
       paper_only_safety_score=1.0, registry_integrity_score=0.95),
    _s("SP197-010", "excellent_quality_low_latency_high_review", "excellent_decision_quality",
       decision_id="DEC-005", composite_score=0.91, grade="EXCELLENT",
       decision_latency_score=0.90, review_quality_score=0.95),

    # ── Weak evidence coverage (11-15) ───────────────────────────────────────
    _s("SP197-011", "weak_evidence_no_evidence_links", "weak_evidence_coverage",
       decision_id="DEC-011", evidence_coverage_score=0.0, grade="WEAK",
       evidence_gap_severity="HIGH", missing_evidence_types=["paper_simulation", "shadow_comparison"]),
    _s("SP197-012", "weak_evidence_partial_only", "weak_evidence_coverage",
       decision_id="DEC-012", evidence_coverage_score=0.25, grade="WEAK",
       partial_evidence=True, decisions_with_partial_evidence=True),
    _s("SP197-013", "weak_evidence_missing_backtest_ref", "weak_evidence_coverage",
       decision_id="DEC-013", evidence_coverage_score=0.30, grade="WATCH",
       missing_evidence_types=["backtest_result"]),
    _s("SP197-014", "weak_evidence_sandbox_only", "weak_evidence_coverage",
       decision_id="DEC-014", evidence_coverage_score=0.40, grade="WATCH",
       evidence_source_count=1, requires_more_evidence=True),
    _s("SP197-015", "weak_evidence_gap_detected_multi_source", "weak_evidence_coverage",
       decision_id="DEC-015", evidence_coverage_score=0.20, grade="WEAK",
       evidence_gap_count=3, evidence_gap_severity="CRITICAL"),

    # ── Missing rationale quality penalty (16-19) ────────────────────────────
    _s("SP197-016", "missing_rationale_score_penalized", "missing_rationale_quality_penalty",
       decision_id="DEC-016", rationale_completeness_score=0.0, composite_score=0.35, grade="WEAK",
       rationale_penalty_applied=True),
    _s("SP197-017", "incomplete_rationale_low_score", "missing_rationale_quality_penalty",
       decision_id="DEC-017", rationale_completeness_score=0.20, composite_score=0.42, grade="WEAK",
       rationale_text_length=15),
    _s("SP197-018", "null_rationale_quality_blocked", "missing_rationale_quality_penalty",
       decision_id="DEC-018", rationale_completeness_score=0.0, blocked_by_rationale=True, grade="INVALID"),
    _s("SP197-019", "rationale_only_boilerplate_penalty", "missing_rationale_quality_penalty",
       decision_id="DEC-019", rationale_completeness_score=0.15, grade="WEAK",
       boilerplate_detected=True),

    # ── Missing lineage quality penalty (20-23) ──────────────────────────────
    _s("SP197-020", "missing_lineage_score_penalized", "missing_lineage_quality_penalty",
       decision_id="DEC-020", lineage_completeness_score=0.0, composite_score=0.30, grade="WEAK",
       lineage_penalty_applied=True),
    _s("SP197-021", "incomplete_lineage_no_parents", "missing_lineage_quality_penalty",
       decision_id="DEC-021", lineage_completeness_score=0.10, parent_count=0, grade="WEAK"),
    _s("SP197-022", "lineage_missing_source_ref", "missing_lineage_quality_penalty",
       decision_id="DEC-022", lineage_completeness_score=0.25, missing_source_refs=True, grade="WATCH"),
    _s("SP197-023", "lineage_broken_chain_penalty", "missing_lineage_quality_penalty",
       decision_id="DEC-023", lineage_completeness_score=0.05, broken_lineage_chain=True, grade="WEAK"),

    # ── Rollback review frequency high (24-27) ───────────────────────────────
    _s("SP197-024", "rollback_review_frequency_high_weekly", "rollback_review_frequency_high",
       registry_source="REG-001", analytics_window="WEEKLY",
       total_rollback_reviews=8, rollback_review_rate=0.40, auto_rollback=False),
    _s("SP197-025", "rollback_review_frequency_high_monthly", "rollback_review_frequency_high",
       registry_source="REG-001", analytics_window="MONTHLY",
       total_rollback_reviews=15, rollback_review_rate=0.35, requires_human_review=True),
    _s("SP197-026", "rollback_review_frequency_critical_quarter", "rollback_review_frequency_high",
       registry_source="REG-002", analytics_window="QUARTERLY",
       total_rollback_reviews=22, rollback_review_rate=0.45, severity="HIGH"),
    _s("SP197-027", "rollback_review_triggers_most_common", "rollback_review_frequency_high",
       registry_source="REG-002", analytics_window="FULL_HISTORY",
       most_common_trigger="DRIFT_DETECTION", rollback_review_rate=0.38),

    # ── Approval quality good (28-31) ────────────────────────────────────────
    _s("SP197-028", "approval_quality_good_average_score_high", "approval_quality_good",
       registry_source="REG-001", analytics_window="FULL_HISTORY",
       total_approved=20, average_quality_score=0.78, grade="GOOD",
       auto_approval=False, no_production_mutation=True),
    _s("SP197-029", "approval_quality_good_with_evidence", "approval_quality_good",
       registry_source="REG-001", analytics_window="MONTHLY",
       total_approved=8, average_quality_score=0.80, high_quality_count=6),
    _s("SP197-030", "approval_quality_good_complete_checklist", "approval_quality_good",
       registry_source="REG-002", analytics_window="QUARTERLY",
       total_approved=12, average_quality_score=0.75, checklist_complete=True),
    _s("SP197-031", "approval_quality_good_paper_only_confirmed", "approval_quality_good",
       registry_source="REG-002", analytics_window="WEEKLY",
       total_approved=4, average_quality_score=0.82, paper_only=True, grade="GOOD"),

    # ── Rejection quality good (32-35) ───────────────────────────────────────
    _s("SP197-032", "rejection_quality_good_strong_rationale", "rejection_quality_good",
       registry_source="REG-001", analytics_window="FULL_HISTORY",
       total_rejected=10, average_quality_score=0.77, most_common_rejection_reason="poor_evidence"),
    _s("SP197-033", "rejection_quality_good_with_audit_trail", "rejection_quality_good",
       registry_source="REG-001", analytics_window="MONTHLY",
       total_rejected=5, average_quality_score=0.75, has_audit_trail=True),
    _s("SP197-034", "rejection_quality_good_governance_pass", "rejection_quality_good",
       registry_source="REG-002", analytics_window="QUARTERLY",
       total_rejected=7, average_quality_score=0.73, governance_passed=True),
    _s("SP197-035", "rejection_quality_good_lineage_complete", "rejection_quality_good",
       registry_source="REG-002", analytics_window="WEEKLY",
       total_rejected=3, average_quality_score=0.79, lineage_complete=True),

    # ── Keep monitoring quality weak (36-39) ─────────────────────────────────
    _s("SP197-036", "keep_monitoring_quality_weak_no_followup", "keep_monitoring_quality_weak",
       registry_source="REG-001", analytics_window="FULL_HISTORY",
       total_keep_monitoring=15, average_quality_score=0.35, grade="WEAK",
       decisions_needing_followup=["DEC-031", "DEC-032"]),
    _s("SP197-037", "keep_monitoring_quality_weak_stale_records", "keep_monitoring_quality_weak",
       registry_source="REG-001", analytics_window="MONTHLY",
       total_keep_monitoring=8, average_quality_score=0.30, stale_records=True),
    _s("SP197-038", "keep_monitoring_quality_weak_missing_evidence", "keep_monitoring_quality_weak",
       registry_source="REG-002", analytics_window="QUARTERLY",
       total_keep_monitoring=6, average_quality_score=0.25, missing_evidence=True),
    _s("SP197-039", "keep_monitoring_quality_weak_no_trend_data", "keep_monitoring_quality_weak",
       registry_source="REG-002", analytics_window="WEEKLY",
       total_keep_monitoring=4, average_quality_score=0.28, no_trend_data=True),

    # ── Governance violation detected (40-43) ────────────────────────────────
    _s("SP197-040", "governance_violation_missing_paper_flags", "governance_violation_detected",
       registry_source="REG-001", violation_type="missing_paper_only_flags",
       violation_count=3, severity="HIGH", blocked=True),
    _s("SP197-041", "governance_violation_forbidden_action_word", "governance_violation_detected",
       registry_source="REG-001", violation_type="forbidden_action_words",
       violation_count=1, severity="CRITICAL", blocked=True),
    _s("SP197-042", "governance_violation_unsafe_export_path", "governance_violation_detected",
       registry_source="REG-002", violation_type="unsafe_export_path",
       violation_count=2, severity="HIGH", blocked=True),
    _s("SP197-043", "governance_violation_missing_investment_advice_flag", "governance_violation_detected",
       registry_source="REG-002", violation_type="missing_not_investment_advice_flags",
       violation_count=1, severity="CRITICAL", blocked=True),

    # ── Audit trail incomplete (44-47) ───────────────────────────────────────
    _s("SP197-044", "audit_trail_incomplete_no_entries", "audit_trail_incomplete",
       decision_id="DEC-044", audit_trail_completeness_score=0.0, entry_count=0,
       audit_trail_incomplete=True, grade="WEAK"),
    _s("SP197-045", "audit_trail_incomplete_partial_entries", "audit_trail_incomplete",
       decision_id="DEC-045", audit_trail_completeness_score=0.25, entry_count=1,
       missing_audit_events=["RECORD_CREATED", "GOVERNANCE_CHECK"]),
    _s("SP197-046", "audit_trail_incomplete_non_immutable", "audit_trail_incomplete",
       decision_id="DEC-046", audit_trail_completeness_score=0.40, immutable=False,
       immutability_violation=True, grade="WATCH"),
    _s("SP197-047", "audit_trail_incomplete_missing_timestamps", "audit_trail_incomplete",
       decision_id="DEC-047", audit_trail_completeness_score=0.15, missing_timestamps=True, grade="WEAK"),

    # ── Unsafe export blocked (48-50) ────────────────────────────────────────
    _s("SP197-048", "unsafe_export_path_production_db", "unsafe_export_blocked",
       export_path="C:/prod_db/analytics.json", blocked=True, block_reason="unsafe_export_path"),
    _s("SP197-049", "unsafe_export_path_live_db", "unsafe_export_blocked",
       export_path="/live_db/governance_report.json", blocked=True, block_reason="unsafe_export_path"),
    _s("SP197-050", "unsafe_export_path_broker_dir", "unsafe_export_blocked",
       export_path="C:/broker_data/dashboard.json", blocked=True, block_reason="unsafe_export_path"),

    # ── Malformed analytics input blocked (51-53) ────────────────────────────
    _s("SP197-051", "malformed_analytics_input_empty_source", "malformed_analytics_input_blocked",
       registry_source="", blocked=True, block_reason="missing_registry_source"),
    _s("SP197-052", "malformed_analytics_input_invalid_window", "malformed_analytics_input_blocked",
       registry_source="REG-001", analytics_window="INVALID_WINDOW",
       blocked=True, block_reason="unknown_analytics_window"),
    _s("SP197-053", "malformed_analytics_input_none_source", "malformed_analytics_input_blocked",
       registry_source=None, blocked=True, block_reason="missing_registry_source"),

    # ── Production mutation blocked (54-56) ──────────────────────────────────
    _s("SP197-054", "production_mutation_blocked_strategy_change", "production_mutation_blocked",
       registry_source="REG-001", blocked=True,
       block_reason="production_strategy_mutation_attempted",
       attempted_action="MUTATE_PRODUCTION_STRATEGY"),
    _s("SP197-055", "production_mutation_blocked_db_write", "production_mutation_blocked",
       registry_source="REG-001", blocked=True,
       block_reason="production_db_write_attempted"),
    _s("SP197-056", "production_mutation_blocked_dashboard_tries", "production_mutation_blocked",
       registry_source="REG-002", blocked=True,
       block_reason="dashboard_tries_to_mutate_strategy",
       dashboard_mutates_strategy=False),

    # ── Automatic rollback blocked (57-59) ───────────────────────────────────
    _s("SP197-057", "automatic_rollback_blocked_drift", "automatic_rollback_blocked",
       registry_source="REG-001", blocked=True,
       block_reason="automatic_rollback_attempted", auto_rollback=False),
    _s("SP197-058", "automatic_rollback_blocked_analytics", "automatic_rollback_blocked",
       registry_source="REG-001", blocked=True,
       block_reason="automatic_rollback_attempted", requires_human_review=True),
    _s("SP197-059", "automatic_rollback_blocked_quality_trigger", "automatic_rollback_blocked",
       registry_source="REG-002", blocked=True,
       block_reason="automatic_rollback_attempted", no_automatic_rollback=True),

    # ── Live activation blocked (60-62) ─────────────────────────────────────
    _s("SP197-060", "live_activation_blocked_from_dashboard", "live_activation_blocked",
       registry_source="REG-001", blocked=True,
       block_reason="live_strategy_activation_attempted"),
    _s("SP197-061", "live_activation_blocked_quality_gate", "live_activation_blocked",
       registry_source="REG-001", blocked=True,
       block_reason="live_strategy_activation_attempted", no_live_strategy_activation=True),
    _s("SP197-062", "live_activation_blocked_analytics_output", "live_activation_blocked",
       registry_source="REG-002", blocked=True,
       block_reason="live_strategy_activation_attempted", paper_only=True),

    # ── Broker request blocked (63-65) ──────────────────────────────────────
    _s("SP197-063", "broker_request_blocked_real_order", "broker_request_blocked",
       registry_source="REG-001", blocked=True,
       block_reason="real_order_requested", no_real_orders=True),
    _s("SP197-064", "broker_request_blocked_margin", "broker_request_blocked",
       registry_source="REG-001", blocked=True,
       block_reason="margin_or_leverage_requested", no_margin=True),
    _s("SP197-065", "broker_request_blocked_broker_execution", "broker_request_blocked",
       registry_source="REG-002", blocked=True,
       block_reason="broker_requested", no_broker=True),

    # ── Dashboard empty state (66-68) ────────────────────────────────────────
    _s("SP197-066", "dashboard_empty_state_no_decisions", "dashboard_empty_state",
       registry_source="REG-EMPTY", decision_count=0, empty_state=True,
       panels_rendered=12, all_panels_empty=True),
    _s("SP197-067", "dashboard_empty_state_new_registry", "dashboard_empty_state",
       registry_source="REG-NEW", decision_count=0, empty_state=True,
       analytics_window="DAILY"),
    _s("SP197-068", "dashboard_empty_state_filter_no_match", "dashboard_empty_state",
       registry_source="REG-001", decision_count=0, empty_state=True,
       analytics_window="WEEKLY", filter_applied=True),

    # ── Full history analytics (69-71) ──────────────────────────────────────
    _s("SP197-069", "full_history_analytics_all_decisions", "full_history_analytics",
       registry_source="REG-001", analytics_window="FULL_HISTORY",
       total_decisions=100, quality_summary_complete=True),
    _s("SP197-070", "full_history_analytics_trend_computed", "full_history_analytics",
       registry_source="REG-001", analytics_window="FULL_HISTORY",
       trend_direction="IMPROVING", quality_delta=0.12),
    _s("SP197-071", "full_history_analytics_all_panels", "full_history_analytics",
       registry_source="REG-002", analytics_window="FULL_HISTORY",
       panels_count=12, all_panels_complete=True),

    # ── Complete quality report (72-75) ──────────────────────────────────────
    _s("SP197-072", "complete_quality_report_all_sections", "complete_quality_report",
       registry_source="REG-001", analytics_window="FULL_HISTORY",
       report_section_count=12, all_sections_paper_only=True),
    _s("SP197-073", "complete_quality_report_scorecard", "complete_quality_report",
       registry_source="REG-001", analytics_window="MONTHLY",
       scorecard_metrics=12, quality_grades_computed=True),
    _s("SP197-074", "complete_quality_report_audit_summary", "complete_quality_report",
       registry_source="REG-002", analytics_window="QUARTERLY",
       audit_summary_included=True, immutable=True, audit_only=True),
    _s("SP197-075", "complete_quality_report_export_pack", "complete_quality_report",
       registry_source="REG-002", analytics_window="FULL_HISTORY",
       export_path="output/quality_report.json", all_sections_included=True,
       production_mutation_blocked=True, live_activation_blocked=True),
]

assert len(_SCENARIOS) == 75, f"Expected 75 scenarios, got {len(_SCENARIOS)}"


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Return all 75 governance dashboard scenarios."""
    return list(_SCENARIOS)


def get_scenario_count() -> int:
    """Return total scenario count."""
    return len(_SCENARIOS)


def get_scenario_by_id(scenario_id: str) -> Dict[str, Any]:
    """Return a scenario by ID, or {} if not found."""
    for s in _SCENARIOS:
        if s.get("scenario_id") == scenario_id:
            return dict(s)
    return {}


def get_scenarios_by_category(category: str) -> List[Dict[str, Any]]:
    """Return all scenarios matching the given category."""
    return [s for s in _SCENARIOS if s.get("category") == category]


def get_scenario_categories() -> List[str]:
    """Return list of unique scenario categories."""
    seen = []
    for s in _SCENARIOS:
        c = s.get("category", "")
        if c not in seen:
            seen.append(c)
    return seen
