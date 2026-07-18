"""
tests/test_strategy_monitoring_report_v194.py
Tests for strategy_monitoring_report_v194.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_monitoring_report_v194 import (
    export_monitoring_summary, export_drift_report, export_rollback_trigger_report,
    export_evidence_pack_report, export_audit_trail_report, export_dashboard_report,
    export_performance_comparison_report, export_signal_quality_report,
    export_guardrail_status_report, export_full_monitoring_pack,
    get_report_section_names,
)


# ── get_report_section_names ──────────────────────────────────────────────────

def test_report_section_names_count():
    assert len(get_report_section_names()) == 10


def test_report_section_names_is_list():
    assert isinstance(get_report_section_names(), list)


def test_report_section_names_monitoring_summary():
    assert "monitoring_summary" in get_report_section_names()


def test_report_section_names_drift_report():
    assert "drift_report" in get_report_section_names()


def test_report_section_names_rollback_trigger_report():
    assert "rollback_trigger_report" in get_report_section_names()


def test_report_section_names_evidence_pack_report():
    assert "evidence_pack_report" in get_report_section_names()


def test_report_section_names_audit_trail_report():
    assert "audit_trail_report" in get_report_section_names()


def test_report_section_names_dashboard_report():
    assert "dashboard_report" in get_report_section_names()


# ── export_monitoring_summary ─────────────────────────────────────────────────

def test_export_monitoring_summary_returns_dict():
    result = export_monitoring_summary("mon1")
    assert isinstance(result, dict)


def test_export_monitoring_summary_paper_only():
    assert export_monitoring_summary("mon1")["paper_only"] is True


def test_export_monitoring_summary_no_real_orders():
    assert export_monitoring_summary("mon1")["no_real_orders"] is True


def test_export_monitoring_summary_monitoring_only():
    assert export_monitoring_summary("mon1")["monitoring_only"] is True


def test_export_monitoring_summary_schema_version():
    assert export_monitoring_summary("mon1")["schema_version"] == "194"


def test_export_monitoring_summary_not_blocked():
    assert export_monitoring_summary("mon1")["blocked"] is False


def test_export_monitoring_summary_blocked_when_empty():
    assert export_monitoring_summary("")["blocked"] is True


# ── export_drift_report ───────────────────────────────────────────────────────

def test_export_drift_report_returns_dict():
    result = export_drift_report("mon1")
    assert isinstance(result, dict)


def test_export_drift_report_paper_only():
    assert export_drift_report("mon1")["paper_only"] is True


def test_export_drift_report_drift_detection_only():
    assert export_drift_report("mon1")["drift_detection_only"] is True


def test_export_drift_report_not_blocked():
    assert export_drift_report("mon1")["blocked"] is False


def test_export_drift_report_blocked_when_empty():
    assert export_drift_report("")["blocked"] is True


# ── export_rollback_trigger_report ────────────────────────────────────────────

def test_export_rollback_trigger_report_returns_dict():
    result = export_rollback_trigger_report("mon1")
    assert isinstance(result, dict)


def test_export_rollback_trigger_report_auto_rollback_false():
    assert export_rollback_trigger_report("mon1")["auto_rollback"] is False


def test_export_rollback_trigger_report_requires_manual_review():
    assert export_rollback_trigger_report("mon1")["requires_manual_review"] is True


def test_export_rollback_trigger_report_paper_only():
    assert export_rollback_trigger_report("mon1")["paper_only"] is True


def test_export_rollback_trigger_report_not_blocked():
    assert export_rollback_trigger_report("mon1")["blocked"] is False


def test_export_rollback_trigger_report_blocked_when_empty():
    assert export_rollback_trigger_report("")["blocked"] is True


# ── export_evidence_pack_report ───────────────────────────────────────────────

def test_export_evidence_pack_report_returns_dict():
    result = export_evidence_pack_report("mon1")
    assert isinstance(result, dict)


def test_export_evidence_pack_report_paper_only():
    assert export_evidence_pack_report("mon1")["paper_only"] is True


def test_export_evidence_pack_report_report_only():
    assert export_evidence_pack_report("mon1")["report_only"] is True


def test_export_evidence_pack_report_not_blocked():
    assert export_evidence_pack_report("mon1")["blocked"] is False


def test_export_evidence_pack_report_blocked_when_empty():
    assert export_evidence_pack_report("")["blocked"] is True


# ── export_audit_trail_report ─────────────────────────────────────────────────

def test_export_audit_trail_report_returns_dict():
    result = export_audit_trail_report("mon1")
    assert isinstance(result, dict)


def test_export_audit_trail_report_paper_only():
    assert export_audit_trail_report("mon1")["paper_only"] is True


def test_export_audit_trail_report_audit_only():
    assert export_audit_trail_report("mon1")["audit_only"] is True


def test_export_audit_trail_report_not_blocked():
    assert export_audit_trail_report("mon1")["blocked"] is False


def test_export_audit_trail_report_blocked_when_empty():
    assert export_audit_trail_report("")["blocked"] is True


# ── export_dashboard_report ───────────────────────────────────────────────────

def test_export_dashboard_report_returns_dict():
    result = export_dashboard_report("mon1")
    assert isinstance(result, dict)


def test_export_dashboard_report_paper_only():
    assert export_dashboard_report("mon1")["paper_only"] is True


def test_export_dashboard_report_monitoring_only():
    assert export_dashboard_report("mon1")["monitoring_only"] is True


def test_export_dashboard_report_not_blocked():
    assert export_dashboard_report("mon1")["blocked"] is False


def test_export_dashboard_report_blocked_when_empty():
    assert export_dashboard_report("")["blocked"] is True


# ── export_performance_comparison_report ──────────────────────────────────────

def test_export_performance_comparison_report_returns_dict():
    result = export_performance_comparison_report("mon1")
    assert isinstance(result, dict)


def test_export_performance_comparison_report_paper_only():
    assert export_performance_comparison_report("mon1")["paper_only"] is True


def test_export_performance_comparison_report_not_blocked():
    assert export_performance_comparison_report("mon1")["blocked"] is False


def test_export_performance_comparison_report_blocked_when_empty():
    assert export_performance_comparison_report("")["blocked"] is True


# ── export_signal_quality_report ──────────────────────────────────────────────

def test_export_signal_quality_report_returns_dict():
    result = export_signal_quality_report("mon1")
    assert isinstance(result, dict)


def test_export_signal_quality_report_paper_only():
    assert export_signal_quality_report("mon1")["paper_only"] is True


def test_export_signal_quality_report_drift_detection_only():
    assert export_signal_quality_report("mon1")["drift_detection_only"] is True


def test_export_signal_quality_report_not_blocked():
    assert export_signal_quality_report("mon1")["blocked"] is False


def test_export_signal_quality_report_blocked_when_empty():
    assert export_signal_quality_report("")["blocked"] is True


# ── export_guardrail_status_report ────────────────────────────────────────────

def test_export_guardrail_status_report_returns_dict():
    result = export_guardrail_status_report("mon1")
    assert isinstance(result, dict)


def test_export_guardrail_status_report_paper_only():
    assert export_guardrail_status_report("mon1")["paper_only"] is True


def test_export_guardrail_status_report_monitoring_only():
    assert export_guardrail_status_report("mon1")["monitoring_only"] is True


def test_export_guardrail_status_report_not_blocked():
    assert export_guardrail_status_report("mon1")["blocked"] is False


def test_export_guardrail_status_report_blocked_when_empty():
    assert export_guardrail_status_report("")["blocked"] is True


# ── export_full_monitoring_pack ───────────────────────────────────────────────

def test_export_full_monitoring_pack_returns_dict():
    result = export_full_monitoring_pack("mon1")
    assert isinstance(result, dict)


def test_export_full_monitoring_pack_paper_only():
    assert export_full_monitoring_pack("mon1")["paper_only"] is True


def test_export_full_monitoring_pack_schema_version():
    assert export_full_monitoring_pack("mon1")["schema_version"] == "194"


def test_export_full_monitoring_pack_not_blocked():
    assert export_full_monitoring_pack("mon1")["blocked"] is False


def test_export_full_monitoring_pack_blocked_when_empty():
    assert export_full_monitoring_pack("")["blocked"] is True
