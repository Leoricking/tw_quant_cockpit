"""
paper_trading/small_capital_strategy/strategy_registry_scenarios_v196.py
Scenarios for Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_BASE = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "governance_only": True,
    "registry_only": True,
    "decision_record_only": True,
    "review_only": True,
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
    "schema_version": "196",
}


def _s(sid: str, name: str, category: str, **kwargs) -> Dict[str, Any]:
    return {**_BASE, "id": sid, "scenario_id": sid, "name": name, "category": category, **kwargs}


_SCENARIOS: List[Dict[str, Any]] = [
    # ── Complete decision registry record (1-5) ──────────────────────────────
    _s("SP196-001", "complete_decision_registry_record", "complete_registry",
       decision_id="DEC-001", source="TUNING_PROPOSAL", decision_type="APPROVE_FOR_PAPER_ONLY",
       decision_state="RECORDED", has_evidence=True, has_rationale=True,
       has_lineage=True, has_audit_trail=True, governance_passed=True),
    _s("SP196-002", "complete_record_from_sandbox_validation", "complete_registry",
       decision_id="DEC-002", source="SANDBOX_VALIDATION", decision_type="KEEP_MONITORING",
       decision_state="RECORDED", has_evidence=True, has_rationale=True, governance_passed=True),
    _s("SP196-003", "complete_record_from_promotion_package", "complete_registry",
       decision_id="DEC-003", source="PROMOTION_PACKAGE", decision_type="APPROVE_FOR_PAPER_ONLY",
       decision_state="APPROVED_FOR_PAPER_ONLY", has_evidence=True, governance_passed=True),
    _s("SP196-004", "complete_record_with_all_checks", "complete_registry",
       decision_id="DEC-004", source="MONITORING_ALERT", decision_type="ESCALATE_TO_MANUAL_REVIEW",
       decision_state="PENDING_REVIEW", all_governance_checks_passed=True),
    _s("SP196-005", "complete_governance_evidence_pack", "complete_registry",
       decision_id="DEC-005", source="DRIFT_DETECTION", decision_type="REQUIRE_MORE_EVIDENCE",
       decision_state="NEED_MORE_EVIDENCE", evidence_count=5, governance_passed=True),

    # ── Approved-for-paper-only decisions (6-10) ─────────────────────────────
    _s("SP196-006", "approved_for_paper_only_tuning", "approved_for_paper",
       decision_id="DEC-006", source="TUNING_PROPOSAL", decision_type="APPROVE_FOR_PAPER_ONLY",
       decision_state="APPROVED_FOR_PAPER_ONLY", auto_approval=False, requires_human_review=True),
    _s("SP196-007", "approved_for_paper_only_sandbox", "approved_for_paper",
       decision_id="DEC-007", source="SANDBOX_VALIDATION", decision_type="APPROVE_FOR_PAPER_ONLY",
       decision_state="APPROVED_FOR_PAPER_ONLY", no_production_mutation=True),
    _s("SP196-008", "approved_for_paper_only_shadow", "approved_for_paper",
       decision_id="DEC-008", source="SHADOW_COMPARISON", decision_type="APPROVE_FOR_PAPER_ONLY",
       decision_state="APPROVED_FOR_PAPER_ONLY", shadow_only=True),
    _s("SP196-009", "approved_for_paper_only_with_lineage", "approved_for_paper",
       decision_id="DEC-009", source="HUMAN_APPROVAL_REQUEST", decision_type="APPROVE_FOR_PAPER_ONLY",
       decision_state="APPROVED_FOR_PAPER_ONLY", has_lineage=True),
    _s("SP196-010", "approved_for_paper_only_with_evidence_pack", "approved_for_paper",
       decision_id="DEC-010", source="PROMOTION_PACKAGE", decision_type="APPROVE_FOR_PAPER_ONLY",
       decision_state="APPROVED_FOR_PAPER_ONLY", evidence_count=3, has_audit_trail=True),

    # ── Rejected candidate decisions (11-15) ─────────────────────────────────
    _s("SP196-011", "rejected_candidate_poor_evidence", "rejected",
       decision_id="DEC-011", source="SANDBOX_VALIDATION", decision_type="REJECT_CANDIDATE",
       decision_state="REJECTED", rejection_reason="poor_evidence"),
    _s("SP196-012", "rejected_candidate_governance_fail", "rejected",
       decision_id="DEC-012", source="TUNING_PROPOSAL", decision_type="REJECT_CANDIDATE",
       decision_state="REJECTED", rejection_reason="governance_check_failed"),
    _s("SP196-013", "rejected_candidate_missing_lineage", "rejected",
       decision_id="DEC-013", source="MONITORING_ALERT", decision_type="REJECT_CANDIDATE",
       decision_state="REJECTED", rejection_reason="missing_lineage"),
    _s("SP196-014", "rejected_candidate_drift_detected", "rejected",
       decision_id="DEC-014", source="DRIFT_DETECTION", decision_type="REJECT_CANDIDATE",
       decision_state="REJECTED", rejection_reason="critical_drift"),
    _s("SP196-015", "rejected_candidate_safety_violation", "rejected",
       decision_id="DEC-015", source="ROLLBACK_REVIEW_TICKET", decision_type="REJECT_CANDIDATE",
       decision_state="REJECTED", rejection_reason="safety_violation"),

    # ── Keep monitoring decisions (16-20) ────────────────────────────────────
    _s("SP196-016", "keep_monitoring_low_confidence", "keep_monitoring",
       decision_id="DEC-016", source="MONITORING_ALERT", decision_type="KEEP_MONITORING",
       decision_state="KEEP_MONITORING", monitoring_window="30d"),
    _s("SP196-017", "keep_monitoring_insufficient_data", "keep_monitoring",
       decision_id="DEC-017", source="TUNING_PROPOSAL", decision_type="KEEP_MONITORING",
       decision_state="KEEP_MONITORING", requires_more_data=True),
    _s("SP196-018", "keep_monitoring_after_review", "keep_monitoring",
       decision_id="DEC-018", source="HUMAN_APPROVAL_REQUEST", decision_type="KEEP_MONITORING",
       decision_state="KEEP_MONITORING", previous_state="PENDING_REVIEW"),
    _s("SP196-019", "keep_monitoring_drift_detected", "keep_monitoring",
       decision_id="DEC-019", source="DRIFT_DETECTION", decision_type="KEEP_MONITORING",
       decision_state="KEEP_MONITORING", drift_severity="LOW"),
    _s("SP196-020", "keep_monitoring_require_longer_window", "keep_monitoring",
       decision_id="DEC-020", source="SANDBOX_VALIDATION", decision_type="REQUIRE_LONGER_MONITORING",
       decision_state="KEEP_MONITORING", extended_window="60d"),

    # ── Keep shadow-only decisions (21-25) ───────────────────────────────────
    _s("SP196-021", "keep_shadow_only_sandbox", "keep_shadow",
       decision_id="DEC-021", source="SANDBOX_VALIDATION", decision_type="KEEP_SHADOW_ONLY",
       decision_state="KEEP_SHADOW_ONLY", shadow_mode=True),
    _s("SP196-022", "keep_shadow_only_not_ready", "keep_shadow",
       decision_id="DEC-022", source="SHADOW_COMPARISON", decision_type="KEEP_SHADOW_ONLY",
       decision_state="KEEP_SHADOW_ONLY", reason="not_ready_for_paper"),
    _s("SP196-023", "keep_shadow_only_more_evidence_needed", "keep_shadow",
       decision_id="DEC-023", source="MONITORING_ALERT", decision_type="KEEP_SHADOW_ONLY",
       decision_state="KEEP_SHADOW_ONLY", evidence_required=True),
    _s("SP196-024", "keep_shadow_only_high_risk", "keep_shadow",
       decision_id="DEC-024", source="TUNING_PROPOSAL", decision_type="KEEP_SHADOW_ONLY",
       decision_state="KEEP_SHADOW_ONLY", risk_level="HIGH"),
    _s("SP196-025", "keep_shadow_only_after_reject", "keep_shadow",
       decision_id="DEC-025", source="ROLLBACK_REVIEW_TICKET", decision_type="KEEP_SHADOW_ONLY",
       decision_state="KEEP_SHADOW_ONLY", previous_state="REJECTED"),

    # ── Rollback review required (26-30) ─────────────────────────────────────
    _s("SP196-026", "rollback_review_critical_drift", "rollback_review",
       decision_id="DEC-026", source="DRIFT_DETECTION", decision_type="OPEN_ROLLBACK_REVIEW",
       decision_state="ROLLBACK_REVIEW_REQUIRED", auto_rollback=False, requires_human_review=True),
    _s("SP196-027", "rollback_review_critical_alert", "rollback_review",
       decision_id="DEC-027", source="MONITORING_ALERT", decision_type="OPEN_ROLLBACK_REVIEW",
       decision_state="ROLLBACK_REVIEW_REQUIRED", severity="CRITICAL"),
    _s("SP196-028", "rollback_review_safety_flag", "rollback_review",
       decision_id="DEC-028", source="ROLLBACK_REVIEW_TICKET", decision_type="OPEN_ROLLBACK_REVIEW",
       decision_state="ROLLBACK_REVIEW_REQUIRED", no_automatic_rollback=True),
    _s("SP196-029", "rollback_review_performance_drop", "rollback_review",
       decision_id="DEC-029", source="HUMAN_APPROVAL_REQUEST", decision_type="OPEN_ROLLBACK_REVIEW",
       decision_state="ROLLBACK_REVIEW_REQUIRED", requires_manual_review=True),
    _s("SP196-030", "rollback_review_evidence_pack", "rollback_review",
       decision_id="DEC-030", source="PROMOTION_PACKAGE", decision_type="OPEN_ROLLBACK_REVIEW",
       decision_state="ROLLBACK_REVIEW_REQUIRED", has_rollback_plan=True),

    # ── Suspend candidate rule (31-35) ───────────────────────────────────────
    _s("SP196-031", "suspend_candidate_rule_high_loss", "suspend_candidate",
       decision_id="DEC-031", source="MONITORING_ALERT", decision_type="SUSPEND_CANDIDATE_RULE",
       decision_state="SUSPENDED_FOR_PAPER", suspension_reason="high_loss_rate"),
    _s("SP196-032", "suspend_candidate_rule_safety", "suspend_candidate",
       decision_id="DEC-032", source="DRIFT_DETECTION", decision_type="SUSPEND_CANDIDATE_RULE",
       decision_state="SUSPENDED_FOR_PAPER", suspension_reason="safety_flag"),
    _s("SP196-033", "suspend_candidate_rule_governance", "suspend_candidate",
       decision_id="DEC-033", source="MANUAL_REVIEW_NOTE", decision_type="SUSPEND_CANDIDATE_RULE",
       decision_state="SUSPENDED_FOR_PAPER", governance_violation=True),
    _s("SP196-034", "suspend_candidate_rule_paper_only", "suspend_candidate",
       decision_id="DEC-034", source="TUNING_PROPOSAL", decision_type="SUSPEND_CANDIDATE_RULE",
       decision_state="SUSPENDED_FOR_PAPER", paper_only=True),
    _s("SP196-035", "suspend_candidate_rule_pending_review", "suspend_candidate",
       decision_id="DEC-035", source="SANDBOX_VALIDATION", decision_type="SUSPEND_CANDIDATE_RULE",
       decision_state="SUSPENDED_FOR_PAPER", awaiting_human_review=True),

    # ── Require more evidence (36-40) ────────────────────────────────────────
    _s("SP196-036", "require_more_evidence_low_sample", "require_evidence",
       decision_id="DEC-036", source="SANDBOX_VALIDATION", decision_type="REQUIRE_MORE_EVIDENCE",
       decision_state="NEED_MORE_EVIDENCE", reason="low_sample_count"),
    _s("SP196-037", "require_more_evidence_incomplete_lineage", "require_evidence",
       decision_id="DEC-037", source="MONITORING_ALERT", decision_type="REQUIRE_MORE_EVIDENCE",
       decision_state="NEED_MORE_EVIDENCE", reason="incomplete_lineage"),
    _s("SP196-038", "require_more_evidence_missing_rationale", "require_evidence",
       decision_id="DEC-038", source="TUNING_PROPOSAL", decision_type="REQUIRE_MORE_EVIDENCE",
       decision_state="NEED_MORE_EVIDENCE", reason="missing_rationale"),
    _s("SP196-039", "require_more_evidence_shadow_only", "require_evidence",
       decision_id="DEC-039", source="SHADOW_COMPARISON", decision_type="REQUIRE_MORE_EVIDENCE",
       decision_state="NEED_MORE_EVIDENCE", reason="shadow_only_insufficient"),
    _s("SP196-040", "require_more_evidence_promotion_pending", "require_evidence",
       decision_id="DEC-040", source="PROMOTION_PACKAGE", decision_type="REQUIRE_MORE_EVIDENCE",
       decision_state="NEED_MORE_EVIDENCE", reason="pending_promotion_evidence"),

    # ── Block: missing decision id (41-43) ───────────────────────────────────
    _s("SP196-041", "blocked_missing_decision_id", "hard_block",
       decision_id="", source="TUNING_PROPOSAL", decision_type="APPROVE_FOR_PAPER_ONLY",
       blocked=True, block_reason="missing_decision_id"),
    _s("SP196-042", "blocked_empty_decision_id_record", "hard_block",
       decision_id="", source="SANDBOX_VALIDATION", decision_type="KEEP_MONITORING",
       blocked=True, block_reason="missing_decision_id"),
    _s("SP196-043", "blocked_whitespace_only_decision_id", "hard_block",
       decision_id="   ", source="MONITORING_ALERT", decision_type="NO_CHANGE",
       blocked=True, block_reason="missing_decision_id"),

    # ── Block: missing source (44-46) ────────────────────────────────────────
    _s("SP196-044", "blocked_missing_source", "hard_block",
       decision_id="DEC-044", source="", decision_type="APPROVE_FOR_PAPER_ONLY",
       blocked=True, block_reason="missing_decision_source"),
    _s("SP196-045", "blocked_null_source", "hard_block",
       decision_id="DEC-045", source=None, decision_type="KEEP_MONITORING",
       blocked=True, block_reason="missing_decision_source"),
    _s("SP196-046", "blocked_unknown_source", "hard_block",
       decision_id="DEC-046", source="INVALID_SOURCE", decision_type="NO_CHANGE",
       blocked=True, block_reason="unknown_decision_source"),

    # ── Block: missing lineage (47-48) ───────────────────────────────────────
    _s("SP196-047", "blocked_missing_lineage", "hard_block",
       decision_id="DEC-047", source="TUNING_PROPOSAL", decision_type="APPROVE_FOR_PAPER_ONLY",
       has_lineage=False, blocked=True, block_reason="missing_decision_lineage"),
    _s("SP196-048", "blocked_empty_lineage", "hard_block",
       decision_id="DEC-048", source="SANDBOX_VALIDATION", decision_type="KEEP_MONITORING",
       has_lineage=False, source_ids=[], blocked=True, block_reason="missing_decision_lineage"),

    # ── Block: missing evidence (49-51) ──────────────────────────────────────
    _s("SP196-049", "blocked_missing_evidence", "hard_block",
       decision_id="DEC-049", source="TUNING_PROPOSAL", decision_type="APPROVE_FOR_PAPER_ONLY",
       evidence_ids=[], blocked=True, block_reason="missing_decision_evidence"),
    _s("SP196-050", "blocked_null_evidence", "hard_block",
       decision_id="DEC-050", source="MONITORING_ALERT", decision_type="KEEP_MONITORING",
       evidence_ids=None, blocked=True, block_reason="missing_decision_evidence"),
    _s("SP196-051", "blocked_no_evidence_links", "hard_block",
       decision_id="DEC-051", source="DRIFT_DETECTION", decision_type="REQUIRE_MORE_EVIDENCE",
       evidence_count=0, blocked=True, block_reason="missing_decision_evidence"),

    # ── Block: missing rationale (52-53) ─────────────────────────────────────
    _s("SP196-052", "blocked_missing_rationale", "hard_block",
       decision_id="DEC-052", source="TUNING_PROPOSAL", decision_type="APPROVE_FOR_PAPER_ONLY",
       rationale="", blocked=True, block_reason="missing_decision_rationale"),
    _s("SP196-053", "blocked_null_rationale", "hard_block",
       decision_id="DEC-053", source="SANDBOX_VALIDATION", decision_type="KEEP_MONITORING",
       rationale=None, blocked=True, block_reason="missing_decision_rationale"),

    # ── Block: duplicate decision id (54-55) ─────────────────────────────────
    _s("SP196-054", "blocked_duplicate_decision_id", "hard_block",
       decision_id="DEC-001", source="TUNING_PROPOSAL", decision_type="APPROVE_FOR_PAPER_ONLY",
       blocked=True, block_reason="duplicate_decision_id", is_duplicate=True),
    _s("SP196-055", "blocked_duplicate_registry_entry", "hard_block",
       decision_id="DEC-002", source="MONITORING_ALERT", decision_type="NO_CHANGE",
       blocked=True, block_reason="duplicate_decision_id", existing_entry=True),

    # ── Block: malformed registry input (56-57) ──────────────────────────────
    _s("SP196-056", "blocked_malformed_registry_input", "hard_block",
       decision_id="MALFORMED$$", source="???", decision_type="INVALID",
       blocked=True, block_reason="malformed_registry_input"),
    _s("SP196-057", "blocked_invalid_json_structure", "hard_block",
       decision_id="DEC-057", source="TUNING_PROPOSAL", decision_type="APPROVE_FOR_PAPER_ONLY",
       malformed=True, blocked=True, block_reason="malformed_registry_input"),

    # ── Block: unsafe export path (58-59) ────────────────────────────────────
    _s("SP196-058", "blocked_unsafe_export_path", "hard_block",
       decision_id="DEC-058", export_path="C:/prod_db/decisions.json",
       blocked=True, block_reason="unsafe_export_path"),
    _s("SP196-059", "blocked_production_export_path", "hard_block",
       decision_id="DEC-059", export_path="/production/strategy/registry.db",
       blocked=True, block_reason="unsafe_export_path"),

    # ── Block: production mutation (60-61) ───────────────────────────────────
    _s("SP196-060", "blocked_production_mutation", "hard_block",
       decision_id="DEC-060", source="TUNING_PROPOSAL",
       blocked=True, block_reason="production_strategy_mutation_attempted",
       attempted_action="MUTATE_PRODUCTION_STRATEGY"),
    _s("SP196-061", "blocked_production_db_write", "hard_block",
       decision_id="DEC-061", source="MONITORING_ALERT",
       blocked=True, block_reason="production_db_write_attempted"),

    # ── Block: automatic rollback (62-63) ────────────────────────────────────
    _s("SP196-062", "blocked_automatic_rollback", "hard_block",
       decision_id="DEC-062", source="DRIFT_DETECTION",
       blocked=True, block_reason="automatic_rollback_attempted",
       auto_rollback=False),
    _s("SP196-063", "blocked_auto_rollback_trigger", "hard_block",
       decision_id="DEC-063", source="ROLLBACK_REVIEW_TICKET",
       blocked=True, block_reason="automatic_rollback_attempted",
       requires_human_review=True),

    # ── Block: live activation (64-65) ───────────────────────────────────────
    _s("SP196-064", "blocked_live_activation", "hard_block",
       decision_id="DEC-064", source="PROMOTION_PACKAGE",
       blocked=True, block_reason="live_strategy_activation_attempted"),
    _s("SP196-065", "blocked_live_broker_order", "hard_block",
       decision_id="DEC-065", source="HUMAN_APPROVAL_REQUEST",
       blocked=True, block_reason="real_order_requested"),

    # ── Complete governance evidence pack (66-70) ────────────────────────────
    _s("SP196-066", "complete_governance_evidence_pack_full", "governance_evidence",
       decision_id="DEC-066", source="PROMOTION_PACKAGE", decision_type="APPROVE_FOR_PAPER_ONLY",
       evidence_count=10, governance_checks_passed=19, all_checks_passed=True),
    _s("SP196-067", "governance_evidence_audit_trail_complete", "governance_evidence",
       decision_id="DEC-067", source="MONITORING_ALERT", decision_type="ESCALATE_TO_MANUAL_REVIEW",
       has_audit_trail=True, audit_entry_count=5, governance_passed=True),
    _s("SP196-068", "governance_evidence_lineage_complete", "governance_evidence",
       decision_id="DEC-068", source="SANDBOX_VALIDATION", decision_type="KEEP_MONITORING",
       has_lineage=True, parent_count=2, source_count=3),
    _s("SP196-069", "governance_evidence_all_flags_present", "governance_evidence",
       decision_id="DEC-069", source="TUNING_PROPOSAL", decision_type="KEEP_SHADOW_ONLY",
       paper_only=True, governance_only=True, registry_only=True, all_flags_checked=True),
    _s("SP196-070", "governance_evidence_checklist_complete", "governance_evidence",
       decision_id="DEC-070", source="DRIFT_DETECTION", decision_type="REQUIRE_MORE_EVIDENCE",
       checklist_item_count=19, all_checked=True, governance_passed=True),

    # ── Escalate to manual review (71-73) ────────────────────────────────────
    _s("SP196-071", "escalate_to_manual_review_high_risk", "escalation",
       decision_id="DEC-071", source="MONITORING_ALERT", decision_type="ESCALATE_TO_MANUAL_REVIEW",
       decision_state="PENDING_REVIEW", risk_level="HIGH", auto_escalation=False),
    _s("SP196-072", "escalate_to_manual_review_critical_drift", "escalation",
       decision_id="DEC-072", source="DRIFT_DETECTION", decision_type="ESCALATE_TO_MANUAL_REVIEW",
       decision_state="PENDING_REVIEW", drift_severity="CRITICAL"),
    _s("SP196-073", "escalate_to_manual_review_safety_concern", "escalation",
       decision_id="DEC-073", source="ROLLBACK_REVIEW_TICKET", decision_type="ESCALATE_TO_MANUAL_REVIEW",
       decision_state="PENDING_REVIEW", requires_human_review=True),

    # ── No change decisions (74-75) ──────────────────────────────────────────
    _s("SP196-074", "no_change_decision_healthy", "no_change",
       decision_id="DEC-074", source="MONITORING_ALERT", decision_type="NO_CHANGE",
       decision_state="RECORDED", reason="strategy_performing_within_bounds"),
    _s("SP196-075", "no_change_decision_paper_only_confirmed", "no_change",
       decision_id="DEC-075", source="MANUAL_REVIEW_NOTE", decision_type="NO_CHANGE",
       decision_state="RECORDED", paper_only=True, governance_passed=True,
       audit_trail_complete=True),
]

assert len(_SCENARIOS) == 75, f"Expected 75 scenarios, got {len(_SCENARIOS)}"


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Return all 75 strategy registry scenarios."""
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
