"""
paper_trading/small_capital_strategy/strategy_registry_fixtures_v196.py
JSON fixtures for Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_BASE_FLAGS = {
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


def _f(fid: str, name: str, **kwargs) -> Dict[str, Any]:
    return {**_BASE_FLAGS, "id": fid, "fixture_id": fid, "name": name, **kwargs}


_FIXTURES: List[Dict[str, Any]] = [
    # ── Version / schema fixtures (1-5) ──────────────────────────────────────
    _f("SMF196-001", "version_196_fixture",
       version="1.9.6", schema_version="196", verify_version=True),
    _f("SMF196-002", "release_name_fixture",
       release_name="Paper Strategy Decision Registry & Governance Lab"),
    _f("SMF196-003", "policy_version_fixture",
       policy_version="1.9.6-small-capital-strategy-paper-strategy-decision-registry-governance-lab"),
    _f("SMF196-004", "included_releases_fixture",
       included_release_count=26, includes_v195=True, includes_v190=True),
    _f("SMF196-005", "schema_196_paper_only_fixture",
       schema_version="196", paper_only=True, governance_only=True),

    # ── Decision source fixtures (6-15) ──────────────────────────────────────
    _f("SMF196-006", "decision_source_tuning_proposal",
       source_type="TUNING_PROPOSAL", valid=True, paper_only=True),
    _f("SMF196-007", "decision_source_sandbox_validation",
       source_type="SANDBOX_VALIDATION", valid=True, paper_only=True),
    _f("SMF196-008", "decision_source_shadow_comparison",
       source_type="SHADOW_COMPARISON", valid=True, paper_only=True),
    _f("SMF196-009", "decision_source_promotion_package",
       source_type="PROMOTION_PACKAGE", valid=True, paper_only=True),
    _f("SMF196-010", "decision_source_rollback_plan",
       source_type="ROLLBACK_PLAN", valid=True, paper_only=True),
    _f("SMF196-011", "decision_source_monitoring_alert",
       source_type="MONITORING_ALERT", valid=True, paper_only=True),
    _f("SMF196-012", "decision_source_drift_detection",
       source_type="DRIFT_DETECTION", valid=True, paper_only=True),
    _f("SMF196-013", "decision_source_human_approval_request",
       source_type="HUMAN_APPROVAL_REQUEST", valid=True, paper_only=True),
    _f("SMF196-014", "decision_source_rollback_review_ticket",
       source_type="ROLLBACK_REVIEW_TICKET", valid=True, paper_only=True),
    _f("SMF196-015", "decision_source_manual_review_note",
       source_type="MANUAL_REVIEW_NOTE", valid=True, paper_only=True),

    # ── Decision type fixtures (16-25) ───────────────────────────────────────
    _f("SMF196-016", "decision_type_approve_for_paper_only",
       decision_type="APPROVE_FOR_PAPER_ONLY", no_production_mutation=True, auto_approval=False),
    _f("SMF196-017", "decision_type_reject_candidate",
       decision_type="REJECT_CANDIDATE", paper_only=True, no_real_orders=True),
    _f("SMF196-018", "decision_type_keep_monitoring",
       decision_type="KEEP_MONITORING", paper_only=True),
    _f("SMF196-019", "decision_type_keep_shadow_only",
       decision_type="KEEP_SHADOW_ONLY", shadow_mode=True, paper_only=True),
    _f("SMF196-020", "decision_type_open_rollback_review",
       decision_type="OPEN_ROLLBACK_REVIEW", auto_rollback=False, requires_human_review=True),
    _f("SMF196-021", "decision_type_suspend_candidate_rule",
       decision_type="SUSPEND_CANDIDATE_RULE", paper_only=True, no_live_activation=True),
    _f("SMF196-022", "decision_type_require_more_evidence",
       decision_type="REQUIRE_MORE_EVIDENCE", paper_only=True, research_only=True),
    _f("SMF196-023", "decision_type_require_longer_monitoring",
       decision_type="REQUIRE_LONGER_MONITORING", paper_only=True),
    _f("SMF196-024", "decision_type_escalate_to_manual_review",
       decision_type="ESCALATE_TO_MANUAL_REVIEW", requires_human_review=True, auto_escalation=False),
    _f("SMF196-025", "decision_type_no_change",
       decision_type="NO_CHANGE", paper_only=True, governance_only=True),

    # ── Decision state fixtures (26-37) ──────────────────────────────────────
    _f("SMF196-026", "decision_state_draft", state="DRAFT", paper_only=True),
    _f("SMF196-027", "decision_state_pending_review",
       state="PENDING_REVIEW", requires_human_review=True),
    _f("SMF196-028", "decision_state_recorded",
       state="RECORDED", immutable=True, paper_only=True),
    _f("SMF196-029", "decision_state_approved_for_paper_only",
       state="APPROVED_FOR_PAPER_ONLY", no_production_mutation=True, auto_approval=False),
    _f("SMF196-030", "decision_state_rejected",
       state="REJECTED", paper_only=True, immutable=True),
    _f("SMF196-031", "decision_state_keep_monitoring",
       state="KEEP_MONITORING", paper_only=True),
    _f("SMF196-032", "decision_state_keep_shadow_only",
       state="KEEP_SHADOW_ONLY", shadow_mode=True, paper_only=True),
    _f("SMF196-033", "decision_state_rollback_review_required",
       state="ROLLBACK_REVIEW_REQUIRED", auto_rollback=False, requires_human_review=True),
    _f("SMF196-034", "decision_state_suspended_for_paper",
       state="SUSPENDED_FOR_PAPER", paper_only=True, no_live_activation=True),
    _f("SMF196-035", "decision_state_need_more_evidence",
       state="NEED_MORE_EVIDENCE", paper_only=True, research_only=True),
    _f("SMF196-036", "decision_state_invalid",
       state="INVALID", blocked=True, paper_only=True),
    _f("SMF196-037", "decision_state_archived",
       state="ARCHIVED", immutable=True, paper_only=True),

    # ── Governance check fixtures (38-47) ────────────────────────────────────
    _f("SMF196-038", "governance_check_count_19",
       governance_check_count=19, all_checks_defined=True),
    _f("SMF196-039", "governance_decision_id_present",
       check="decision_id_present", required=True, paper_only=True),
    _f("SMF196-040", "governance_source_present",
       check="source_present", required=True, paper_only=True),
    _f("SMF196-041", "governance_lineage_present",
       check="lineage_present", required=True, paper_only=True),
    _f("SMF196-042", "governance_evidence_present",
       check="evidence_present", required=True, paper_only=True),
    _f("SMF196-043", "governance_rationale_present",
       check="rationale_present", required=True, paper_only=True),
    _f("SMF196-044", "governance_checklist_present",
       check="checklist_present", required=True, paper_only=True),
    _f("SMF196-045", "governance_paper_only_flags",
       check="paper_only_flags_present", required=True, paper_only=True),
    _f("SMF196-046", "governance_immutable_record_policy",
       check="immutable_record_policy_present", required=True, immutable=True),
    _f("SMF196-047", "governance_audit_trail_present",
       check="audit_trail_present", required=True, audit_only=True),

    # ── Safety flag fixtures (48-55) ──────────────────────────────────────────
    _f("SMF196-048", "safety_flags_all_set",
       all_safety_flags_set=True, paper_only=True, no_real_orders=True,
       no_broker=True, governance_only=True, registry_only=True),
    _f("SMF196-049", "safety_no_production_mutation",
       no_production_strategy_mutation=True, production_mutation_blocked=True),
    _f("SMF196-050", "safety_no_automatic_rollback",
       no_automatic_rollback=True, auto_rollback=False, requires_human_review=True),
    _f("SMF196-051", "safety_no_live_activation",
       no_live_strategy_activation=True, live_activation_blocked=True),
    _f("SMF196-052", "safety_forbidden_actions_count_9",
       forbidden_action_count=9, no_real_orders=True),
    _f("SMF196-053", "safety_allowed_actions_count_18",
       allowed_action_count=18, paper_only=True, governance_only=True),
    _f("SMF196-054", "safety_hard_block_conditions_count_20",
       hard_block_count=20, all_blocks_defined=True),
    _f("SMF196-055", "safety_audit_all_safe",
       all_safe=True, violation_count=0, paper_only=True),

    # ── Hard block condition fixtures (56-65) ────────────────────────────────
    _f("SMF196-056", "hard_block_real_order_requested",
       block_condition="real_order_requested", blocked=True, paper_only=True),
    _f("SMF196-057", "hard_block_broker_requested",
       block_condition="broker_requested", blocked=True, no_broker=True),
    _f("SMF196-058", "hard_block_margin_or_leverage_requested",
       block_condition="margin_or_leverage_requested", blocked=True, no_margin=True),
    _f("SMF196-059", "hard_block_production_db_write",
       block_condition="production_db_write_attempted", blocked=True, no_production_writes=True),
    _f("SMF196-060", "hard_block_production_mutation",
       block_condition="production_strategy_mutation_attempted", blocked=True),
    _f("SMF196-061", "hard_block_automatic_rollback",
       block_condition="automatic_rollback_attempted", blocked=True, auto_rollback=False),
    _f("SMF196-062", "hard_block_live_activation",
       block_condition="live_strategy_activation_attempted", blocked=True),
    _f("SMF196-063", "hard_block_missing_decision_id",
       block_condition="missing_decision_id", blocked=True, decision_id=""),
    _f("SMF196-064", "hard_block_duplicate_decision_id",
       block_condition="duplicate_decision_id", blocked=True, is_duplicate=True),
    _f("SMF196-065", "hard_block_unsafe_export_path",
       block_condition="unsafe_export_path", blocked=True,
       export_path="C:/production/db.json"),

    # ── Engine function fixtures (66-70) ──────────────────────────────────────
    _f("SMF196-066", "engine_build_decision_record_valid",
       decision_id="DEC-ENG-001", source="TUNING_PROPOSAL",
       decision_type="APPROVE_FOR_PAPER_ONLY", rationale="test",
       expected_valid=True, expected_blocked=False),
    _f("SMF196-067", "engine_build_governance_check_valid",
       decision_id="DEC-GOV-001", evidence=["ev1", "ev2"], rationale="test rationale",
       expected_governance_passed=True),
    _f("SMF196-068", "engine_build_evidence_pack_valid",
       decision_id="DEC-EVP-001", evidence_links=["link1"],
       expected_valid=True, expected_blocked=False),
    _f("SMF196-069", "engine_build_audit_trail_valid",
       decision_id="DEC-AUD-001", event="RECORD_CREATED",
       expected_valid=True, immutable=True),
    _f("SMF196-070", "engine_build_export_manifest_valid",
       decision_id="DEC-EXP-001", export_path="output/registry_export.json",
       expected_valid=True, safe_path_only=True),

    # ── Report function fixtures (71-75) ──────────────────────────────────────
    _f("SMF196-071", "report_sections_count_10",
       report_section_count=10, all_sections_paper_only=True),
    _f("SMF196-072", "report_export_decision_record",
       decision_id="DEC-RPT-001", section="decision_record",
       expected_valid=True, paper_only=True),
    _f("SMF196-073", "report_export_governance_report",
       decision_id="DEC-RPT-002", section="governance_report",
       expected_valid=True, auto_approval=False),
    _f("SMF196-074", "report_export_full_registry_pack",
       decision_id="DEC-RPT-003", section="full_registry_pack",
       expected_valid=True, auto_rollback=False, auto_approval=False,
       all_sections_included=True),
    _f("SMF196-075", "report_export_audit_trail",
       decision_id="DEC-RPT-004", section="audit_trail_report",
       expected_valid=True, immutable=True, audit_only=True),
]

assert len(_FIXTURES) == 75, f"Expected 75 fixtures, got {len(_FIXTURES)}"


def get_all_fixtures() -> List[Dict[str, Any]]:
    """Return all 75 strategy registry fixtures."""
    return list(_FIXTURES)


def get_fixture_count() -> int:
    """Return total fixture count."""
    return len(_FIXTURES)


def get_fixture_by_id(fixture_id: str) -> Optional[Dict[str, Any]]:
    """Return a fixture by ID, or None if not found."""
    for f in _FIXTURES:
        if f.get("fixture_id") == fixture_id:
            return dict(f)
    return None
