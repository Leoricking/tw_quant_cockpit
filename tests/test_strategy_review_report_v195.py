"""
tests/test_strategy_review_report_v195.py
Tests for strategy review report module v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_review_report_v195 import (
    export_review_summary, export_review_alert_report,
    export_human_approval_report, export_rollback_review_report,
    export_review_evidence_pack, export_review_audit_trail,
    export_full_review_pack, export_review_dashboard,
    export_approval_checklist, export_review_findings,
    get_report_section_names,
)


# ── export_review_summary ─────────────────────────────────────────────────────

def test_export_review_summary_blocked_missing_id():
    assert export_review_summary("")["blocked"] is True


def test_export_review_summary_valid():
    assert export_review_summary("REV-001")["valid"] is True


def test_export_review_summary_paper_only():
    assert export_review_summary("REV-001")["paper_only"] is True


def test_export_review_summary_no_real_orders():
    assert export_review_summary("REV-001")["no_real_orders"] is True


def test_export_review_summary_schema_version():
    assert export_review_summary("REV-001")["schema_version"] == "195"


# ── export_review_alert_report ────────────────────────────────────────────────

def test_export_review_alert_report_blocked_missing_id():
    assert export_review_alert_report("")["blocked"] is True


def test_export_review_alert_report_valid():
    assert export_review_alert_report("REV-001")["valid"] is True


def test_export_review_alert_report_paper_only():
    assert export_review_alert_report("REV-001")["paper_only"] is True


# ── export_human_approval_report ──────────────────────────────────────────────

def test_export_human_approval_report_blocked_missing_id():
    assert export_human_approval_report("")["blocked"] is True


def test_export_human_approval_report_valid():
    assert export_human_approval_report("REV-001")["valid"] is True


def test_export_human_approval_report_auto_approval_false():
    assert export_human_approval_report("REV-001")["auto_approval"] is False


def test_export_human_approval_report_requires_manual_review():
    assert export_human_approval_report("REV-001")["requires_manual_review"] is True


def test_export_human_approval_report_paper_only():
    assert export_human_approval_report("REV-001")["paper_only"] is True


# ── export_rollback_review_report ─────────────────────────────────────────────

def test_export_rollback_review_report_blocked_missing_id():
    assert export_rollback_review_report("")["blocked"] is True


def test_export_rollback_review_report_valid():
    assert export_rollback_review_report("REV-001")["valid"] is True


def test_export_rollback_review_report_auto_rollback_false():
    assert export_rollback_review_report("REV-001")["auto_rollback"] is False


def test_export_rollback_review_report_requires_manual_review():
    assert export_rollback_review_report("REV-001")["requires_manual_review"] is True


# ── export_review_evidence_pack ───────────────────────────────────────────────

def test_export_review_evidence_pack_blocked_missing_id():
    assert export_review_evidence_pack("")["blocked"] is True


def test_export_review_evidence_pack_valid():
    assert export_review_evidence_pack("REV-001")["valid"] is True


def test_export_review_evidence_pack_paper_only():
    assert export_review_evidence_pack("REV-001")["paper_only"] is True


# ── export_review_audit_trail ─────────────────────────────────────────────────

def test_export_review_audit_trail_blocked_missing_id():
    assert export_review_audit_trail("")["blocked"] is True


def test_export_review_audit_trail_valid():
    assert export_review_audit_trail("REV-001")["valid"] is True


def test_export_review_audit_trail_audit_only():
    assert export_review_audit_trail("REV-001")["audit_only"] is True


# ── export_full_review_pack ───────────────────────────────────────────────────

def test_export_full_review_pack_blocked_missing_id():
    assert export_full_review_pack("")["blocked"] is True


def test_export_full_review_pack_valid():
    assert export_full_review_pack("REV-001")["valid"] is True


def test_export_full_review_pack_paper_only():
    assert export_full_review_pack("REV-001")["paper_only"] is True


def test_export_full_review_pack_no_real_orders():
    assert export_full_review_pack("REV-001")["no_real_orders"] is True


# ── export_review_dashboard ───────────────────────────────────────────────────

def test_export_review_dashboard_blocked_missing_id():
    assert export_review_dashboard("")["blocked"] is True


def test_export_review_dashboard_valid():
    assert export_review_dashboard("REV-001")["valid"] is True


def test_export_review_dashboard_paper_only():
    assert export_review_dashboard("REV-001")["paper_only"] is True


# ── export_approval_checklist ─────────────────────────────────────────────────

def test_export_approval_checklist_blocked_missing_id():
    assert export_approval_checklist("")["blocked"] is True


def test_export_approval_checklist_valid():
    assert export_approval_checklist("REV-001")["valid"] is True


def test_export_approval_checklist_requires_human_review():
    result = export_approval_checklist("REV-001")
    assert result.get("requires_manual_review", True) is True


# ── export_review_findings ────────────────────────────────────────────────────

def test_export_review_findings_blocked_missing_id():
    assert export_review_findings("")["blocked"] is True


def test_export_review_findings_valid():
    assert export_review_findings("REV-001")["valid"] is True


def test_export_review_findings_not_investment_advice():
    assert export_review_findings("REV-001")["not_investment_advice"] is True


# ── get_report_section_names ──────────────────────────────────────────────────

def test_get_report_section_names_count():
    assert len(get_report_section_names()) >= 10


def test_get_report_section_names_is_list():
    assert isinstance(get_report_section_names(), list)


def test_get_report_section_names_has_review_summary():
    sections = get_report_section_names()
    assert any("summary" in s.lower() or "review" in s.lower() for s in sections)
