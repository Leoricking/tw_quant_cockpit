"""
tests/test_strategy_registry_report_v196.py
Tests for strategy_registry_report_v196 — Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_registry_report_v196 import (
    REPORT_SECTIONS,
    get_report_section_names,
    export_decision_record_report,
    export_governance_report,
    export_lineage_report,
    export_evidence_pack_report,
    export_audit_trail_report,
    export_dashboard_report,
    export_registry_summary,
    export_violation_report,
    export_retention_policy_report,
    export_full_registry_pack,
)


# ── report sections ───────────────────────────────────────────────────────────

def test_report_sections_count_10():
    assert len(REPORT_SECTIONS) == 10

def test_get_report_section_names_count():
    assert len(get_report_section_names()) >= 10

def test_get_report_section_names_is_list():
    assert isinstance(get_report_section_names(), list)


# ── export_decision_record_report ─────────────────────────────────────────────

def test_decision_record_report_missing_id_blocked():
    assert export_decision_record_report("")["blocked"] is True

def test_decision_record_report_valid():
    assert export_decision_record_report("DEC-001")["valid"] is True

def test_decision_record_report_paper_only():
    assert export_decision_record_report("DEC-001")["paper_only"] is True

def test_decision_record_report_no_real_orders():
    assert export_decision_record_report("DEC-001")["no_real_orders"] is True


# ── export_governance_report ──────────────────────────────────────────────────

def test_governance_report_missing_id_blocked():
    assert export_governance_report("")["blocked"] is True

def test_governance_report_valid():
    assert export_governance_report("DEC-001")["valid"] is True

def test_governance_report_paper_only():
    assert export_governance_report("DEC-001")["paper_only"] is True


# ── export_lineage_report ─────────────────────────────────────────────────────

def test_lineage_report_missing_id_blocked():
    assert export_lineage_report("")["blocked"] is True

def test_lineage_report_valid():
    assert export_lineage_report("DEC-001")["valid"] is True

def test_lineage_report_paper_only():
    assert export_lineage_report("DEC-001")["paper_only"] is True


# ── export_evidence_pack_report ───────────────────────────────────────────────

def test_evidence_pack_report_missing_id_blocked():
    assert export_evidence_pack_report("")["blocked"] is True

def test_evidence_pack_report_valid():
    assert export_evidence_pack_report("DEC-001")["valid"] is True

def test_evidence_pack_report_paper_only():
    assert export_evidence_pack_report("DEC-001")["paper_only"] is True


# ── export_audit_trail_report ─────────────────────────────────────────────────

def test_audit_trail_report_missing_id_blocked():
    assert export_audit_trail_report("")["blocked"] is True

def test_audit_trail_report_valid():
    assert export_audit_trail_report("DEC-001")["valid"] is True

def test_audit_trail_report_immutable():
    assert export_audit_trail_report("DEC-001")["immutable"] is True


# ── export_dashboard_report ───────────────────────────────────────────────────

def test_dashboard_report_missing_id_blocked():
    assert export_dashboard_report("")["blocked"] is True

def test_dashboard_report_valid():
    assert export_dashboard_report("DEC-001")["valid"] is True

def test_dashboard_report_paper_only():
    assert export_dashboard_report("DEC-001")["paper_only"] is True


# ── export_registry_summary ───────────────────────────────────────────────────

def test_registry_summary_missing_id_blocked():
    assert export_registry_summary("")["blocked"] is True

def test_registry_summary_valid():
    assert export_registry_summary("DEC-001")["valid"] is True

def test_registry_summary_paper_only():
    assert export_registry_summary("DEC-001")["paper_only"] is True


# ── export_violation_report ───────────────────────────────────────────────────

def test_violation_report_missing_id_blocked():
    assert export_violation_report("")["blocked"] is True

def test_violation_report_valid():
    assert export_violation_report("DEC-001")["valid"] is True

def test_violation_report_paper_only():
    assert export_violation_report("DEC-001")["paper_only"] is True


# ── export_retention_policy_report ───────────────────────────────────────────

def test_retention_policy_report_missing_id_blocked():
    assert export_retention_policy_report("")["blocked"] is True

def test_retention_policy_report_valid():
    assert export_retention_policy_report("DEC-001")["valid"] is True

def test_retention_policy_report_no_auto_deletion():
    assert export_retention_policy_report("DEC-001")["auto_deletion"] is False


# ── export_full_registry_pack ─────────────────────────────────────────────────

def test_full_registry_pack_missing_id_blocked():
    assert export_full_registry_pack("")["blocked"] is True

def test_full_registry_pack_valid():
    assert export_full_registry_pack("DEC-001")["valid"] is True

def test_full_registry_pack_paper_only():
    assert export_full_registry_pack("DEC-001")["paper_only"] is True

def test_full_registry_pack_no_real_orders():
    assert export_full_registry_pack("DEC-001")["no_real_orders"] is True

def test_full_registry_pack_auto_rollback_false():
    assert export_full_registry_pack("DEC-001")["auto_rollback"] is False

def test_full_registry_pack_auto_approval_false():
    assert export_full_registry_pack("DEC-001")["auto_approval"] is False

def test_full_registry_pack_governance_only():
    assert export_full_registry_pack("DEC-001")["governance_only"] is True
