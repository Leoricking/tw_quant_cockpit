"""
tests/test_strategy_registry_engine_v196.py
Tests for strategy_registry_engine_v196 — Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_registry_engine_v196 import (
    validate_registry_action,
    validate_decision_source,
    validate_decision_type,
    validate_decision_state,
    build_decision_record,
    build_governance_check,
    build_decision_queue,
    build_evidence_pack,
    build_audit_trail,
    build_registry_dashboard,
    build_export_manifest,
    build_decision_lineage,
    build_registry_report,
    build_violation_report,
    get_engine_info,
)


# ── validate_registry_action ──────────────────────────────────────────────────

def test_validate_action_buy_blocked():
    assert validate_registry_action("BUY")["blocked"] is True

def test_validate_action_sell_blocked():
    assert validate_registry_action("SELL")["blocked"] is True

def test_validate_action_register_valid():
    assert validate_registry_action("REGISTER_DECISION")["valid"] is True

def test_validate_action_blocked_has_reason():
    result = validate_registry_action("BUY")
    assert "reason" in result


# ── validate_decision_source ──────────────────────────────────────────────────

def test_validate_source_manual_valid():
    assert validate_decision_source("MANUAL_REVIEW")["valid"] is True

def test_validate_source_unknown_invalid():
    result = validate_decision_source("UNKNOWN_SOURCE_XYZ")
    assert result["valid"] is False


# ── validate_decision_type ────────────────────────────────────────────────────

def test_validate_type_valid():
    from paper_trading.small_capital_strategy.strategy_registry_version_v196 import get_decision_types
    types = get_decision_types()
    assert validate_decision_type(types[0])["valid"] is True

def test_validate_type_unknown_invalid():
    result = validate_decision_type("UNKNOWN_TYPE_XYZ")
    assert result["valid"] is False


# ── validate_decision_state ───────────────────────────────────────────────────

def test_validate_state_valid():
    from paper_trading.small_capital_strategy.strategy_registry_version_v196 import get_decision_states
    states = get_decision_states()
    assert validate_decision_state(states[0])["valid"] is True

def test_validate_state_unknown_invalid():
    result = validate_decision_state("UNKNOWN_STATE_XYZ")
    assert result["valid"] is False


# ── build_decision_record ─────────────────────────────────────────────────────

def test_build_decision_record_missing_id_blocked():
    assert build_decision_record("", "MANUAL_REVIEW", "APPROVE_FOR_PAPER", "test rationale")["blocked"] is True

def test_build_decision_record_missing_source_blocked():
    assert build_decision_record("DEC-001", "", "APPROVE_FOR_PAPER", "test rationale")["blocked"] is True

def test_build_decision_record_missing_type_blocked():
    assert build_decision_record("DEC-001", "MANUAL_REVIEW", "", "test rationale")["blocked"] is True

def test_build_decision_record_missing_rationale_blocked():
    assert build_decision_record("DEC-001", "MANUAL_REVIEW", "APPROVE_FOR_PAPER", "")["blocked"] is True

def test_build_decision_record_valid():
    result = build_decision_record("DEC-001", "MANUAL_REVIEW", "APPROVE_FOR_PAPER", "test rationale")
    assert result["blocked"] is False

def test_build_decision_record_paper_only():
    result = build_decision_record("DEC-001", "MANUAL_REVIEW", "APPROVE_FOR_PAPER", "test rationale")
    assert result["paper_only"] is True

def test_build_decision_record_no_real_orders():
    result = build_decision_record("DEC-001", "MANUAL_REVIEW", "APPROVE_FOR_PAPER", "test rationale")
    assert result["no_real_orders"] is True

def test_build_decision_record_immutable():
    result = build_decision_record("DEC-001", "MANUAL_REVIEW", "APPROVE_FOR_PAPER", "test rationale")
    assert result["immutable"] is True


# ── build_governance_check ────────────────────────────────────────────────────

def test_build_governance_check_missing_id_blocked():
    assert build_governance_check("", "evidence123", "rationale123")["blocked"] is True

def test_build_governance_check_missing_evidence_blocked():
    assert build_governance_check("DEC-001", "", "rationale123")["blocked"] is True

def test_build_governance_check_missing_rationale_blocked():
    assert build_governance_check("DEC-001", "evidence123", "")["blocked"] is True

def test_build_governance_check_valid():
    result = build_governance_check("DEC-001", "evidence123", "rationale123")
    assert result["blocked"] is False

def test_build_governance_check_paper_only():
    result = build_governance_check("DEC-001", "evidence123", "rationale123")
    assert result["paper_only"] is True


# ── build_decision_queue ──────────────────────────────────────────────────────

def test_build_decision_queue_missing_registry_id_blocked():
    assert build_decision_queue("")["blocked"] is True

def test_build_decision_queue_valid():
    assert build_decision_queue("REG-001")["blocked"] is False

def test_build_decision_queue_auto_processing_false():
    result = build_decision_queue("REG-001")
    assert result["auto_processing"] is False

def test_build_decision_queue_requires_human_review():
    result = build_decision_queue("REG-001")
    assert result["requires_human_review"] is True


# ── build_evidence_pack ───────────────────────────────────────────────────────

def test_build_evidence_pack_missing_id_blocked():
    assert build_evidence_pack("")["blocked"] is True

def test_build_evidence_pack_valid():
    assert build_evidence_pack("DEC-001")["blocked"] is False

def test_build_evidence_pack_paper_only():
    assert build_evidence_pack("DEC-001")["paper_only"] is True


# ── build_audit_trail ─────────────────────────────────────────────────────────

def test_build_audit_trail_missing_id_blocked():
    assert build_audit_trail("")["blocked"] is True

def test_build_audit_trail_valid():
    assert build_audit_trail("DEC-001")["blocked"] is False

def test_build_audit_trail_immutable():
    assert build_audit_trail("DEC-001")["immutable"] is True


# ── build_registry_dashboard ──────────────────────────────────────────────────

def test_build_registry_dashboard_missing_registry_id_blocked():
    assert build_registry_dashboard("", "DEC-001")["blocked"] is True

def test_build_registry_dashboard_valid():
    assert build_registry_dashboard("REG-001", "DEC-001")["blocked"] is False

def test_build_registry_dashboard_paper_only():
    assert build_registry_dashboard("REG-001", "DEC-001")["paper_only"] is True


# ── build_export_manifest ─────────────────────────────────────────────────────

def test_build_export_manifest_unsafe_path_blocked():
    assert build_export_manifest("/etc/passwd", "DEC-001")["blocked"] is True

def test_build_export_manifest_safe_path_valid():
    assert build_export_manifest("reports/", "DEC-001")["blocked"] is False


# ── build_decision_lineage ────────────────────────────────────────────────────

def test_build_decision_lineage_missing_id_blocked():
    assert build_decision_lineage("")["blocked"] is True

def test_build_decision_lineage_valid():
    assert build_decision_lineage("DEC-001")["blocked"] is False

def test_build_decision_lineage_paper_only():
    assert build_decision_lineage("DEC-001")["paper_only"] is True


# ── build_registry_report ─────────────────────────────────────────────────────

def test_build_registry_report_paper_only():
    assert build_registry_report("DEC-001")["paper_only"] is True


# ── build_violation_report ────────────────────────────────────────────────────

def test_build_violation_report_paper_only():
    assert build_violation_report("DEC-001")["paper_only"] is True


# ── get_engine_info ───────────────────────────────────────────────────────────

def test_get_engine_info_returns_dict():
    assert isinstance(get_engine_info(), dict)

def test_get_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True

def test_get_engine_info_schema_version():
    assert get_engine_info()["schema_version"] == "196"
