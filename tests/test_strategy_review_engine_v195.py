"""
tests/test_strategy_review_engine_v195.py
Tests for strategy review engine v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_review_engine_v195 import (
    validate_review_action, validate_review_decision_state,
    validate_review_alert_category, validate_review_severity,
    build_review_alert, build_human_approval_request,
    build_rollback_review_ticket, build_review_evidence_pack,
    build_review_dashboard, build_review_export_manifest,
    build_review_audit_trail, build_review_recommendation,
    get_engine_info,
)


# ── validate_review_action ────────────────────────────────────────────────────

def test_validate_allowed_action_review():
    result = validate_review_action("REVIEW")
    assert result["valid"] is True
    assert result["blocked"] is False


def test_validate_forbidden_action_buy():
    result = validate_review_action("BUY")
    assert result["blocked"] is True
    assert result["valid"] is False


def test_validate_allowed_action_human_approval():
    result = validate_review_action("HUMAN_APPROVAL")
    assert result["valid"] is True


def test_validate_allowed_action_monitor():
    result = validate_review_action("MONITOR")
    assert result["valid"] is True


# ── validate_review_decision_state ────────────────────────────────────────────

def test_validate_decision_state_approved():
    result = validate_review_decision_state("APPROVED_FOR_PAPER_ONLY")
    assert result["valid"] is True


def test_validate_decision_state_rejected():
    result = validate_review_decision_state("REJECTED")
    assert result["valid"] is True


def test_validate_decision_state_invalid():
    result = validate_review_decision_state("UNKNOWN_STATE")
    assert result["valid"] is False


# ── validate_review_alert_category ───────────────────────────────────────────

def test_validate_alert_category_win_rate():
    result = validate_review_alert_category("WIN_RATE_DRIFT_REVIEW")
    assert result["valid"] is True


def test_validate_alert_category_invalid():
    result = validate_review_alert_category("UNKNOWN_CATEGORY")
    assert result["valid"] is False


# ── validate_review_severity ──────────────────────────────────────────────────

def test_validate_severity_critical():
    result = validate_review_severity("CRITICAL")
    assert result["valid"] is True


def test_validate_severity_info():
    result = validate_review_severity("INFO")
    assert result["valid"] is True


def test_validate_severity_invalid():
    result = validate_review_severity("UNKNOWN")
    assert result["valid"] is False


# ── build_review_alert ────────────────────────────────────────────────────────

def test_build_review_alert_blocked_missing_id():
    result = build_review_alert("", "WIN_RATE_DRIFT_REVIEW", "HIGH")
    assert result["blocked"] is True


def test_build_review_alert_valid():
    result = build_review_alert("RA-001", "WIN_RATE_DRIFT_REVIEW", "HIGH")
    assert result["valid"] is True
    assert result["blocked"] is False


def test_build_review_alert_paper_only():
    result = build_review_alert("RA-001", "WIN_RATE_DRIFT_REVIEW", "HIGH")
    assert result["paper_only"] is True


def test_build_review_alert_no_real_orders():
    result = build_review_alert("RA-001", "WIN_RATE_DRIFT_REVIEW", "HIGH")
    assert result["no_real_orders"] is True


# ── build_human_approval_request ──────────────────────────────────────────────

def test_build_human_approval_request_blocked_missing_id():
    result = build_human_approval_request("", "alert-001", "checklist-001")
    assert result["blocked"] is True


def test_build_human_approval_request_blocked_missing_alert():
    result = build_human_approval_request("req-001", "", "checklist-001")
    assert result["blocked"] is True


def test_build_human_approval_request_valid():
    result = build_human_approval_request("req-001", "alert-001", "checklist-001")
    assert result["valid"] is True
    assert result["blocked"] is False


def test_build_human_approval_request_auto_approval_false():
    result = build_human_approval_request("req-001", "alert-001", "checklist-001")
    assert result["auto_approval"] is False


def test_build_human_approval_request_requires_manual_review():
    result = build_human_approval_request("req-001", "alert-001", "checklist-001")
    assert result["requires_manual_review"] is True


# ── build_rollback_review_ticket ──────────────────────────────────────────────

def test_build_rollback_review_ticket_blocked_missing_id():
    result = build_rollback_review_ticket("", "trigger-001")
    assert result["blocked"] is True


def test_build_rollback_review_ticket_valid_with_empty_trigger():
    result = build_rollback_review_ticket("rr-001", "")
    assert result["valid"] is True


def test_build_rollback_review_ticket_valid():
    result = build_rollback_review_ticket("rr-001", "trigger-001")
    assert result["valid"] is True


def test_build_rollback_review_ticket_auto_rollback_false():
    result = build_rollback_review_ticket("rr-001", "trigger-001")
    assert result["auto_rollback"] is False


def test_build_rollback_review_ticket_requires_manual_review():
    result = build_rollback_review_ticket("rr-001", "trigger-001")
    assert result["requires_manual_review"] is True


# ── build_review_evidence_pack ────────────────────────────────────────────────

def test_build_review_evidence_pack_blocked_missing_id():
    result = build_review_evidence_pack("", ["e1"])
    assert result["blocked"] is True


def test_build_review_evidence_pack_valid_with_empty_evidence():
    result = build_review_evidence_pack("ep-001", [])
    assert result["valid"] is True


def test_build_review_evidence_pack_valid():
    result = build_review_evidence_pack("ep-001", ["e1", "e2"])
    assert result["valid"] is True


def test_build_review_evidence_pack_paper_only():
    result = build_review_evidence_pack("ep-001", ["e1"])
    assert result["paper_only"] is True


# ── build_review_dashboard ────────────────────────────────────────────────────

def test_build_review_dashboard_blocked_missing_dashboard_id():
    result = build_review_dashboard("", "review-001")
    assert result["blocked"] is True


def test_build_review_dashboard_valid():
    result = build_review_dashboard("dash-001", "review-001")
    assert result["valid"] is True


def test_build_review_dashboard_paper_only():
    result = build_review_dashboard("dash-001", "review-001")
    assert result["paper_only"] is True


# ── build_review_recommendation ───────────────────────────────────────────────

def test_build_review_recommendation_blocked_missing_id():
    result = build_review_recommendation("", "APPROVE_FOR_PAPER_ONLY")
    assert result["blocked"] is True


def test_build_review_recommendation_valid():
    result = build_review_recommendation("rec-001", "APPROVE_FOR_PAPER_ONLY")
    assert result["valid"] is True


def test_build_review_recommendation_paper_only():
    result = build_review_recommendation("rec-001", "APPROVE_FOR_PAPER_ONLY")
    assert result["paper_only"] is True


def test_build_review_recommendation_production_blocked():
    result = build_review_recommendation("rec-001", "APPROVE_FOR_PAPER_ONLY")
    assert result["production_trading_blocked"] is True


# ── get_engine_info ───────────────────────────────────────────────────────────

def test_engine_info_is_dict():
    assert isinstance(get_engine_info(), dict)


def test_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True


def test_engine_info_schema_version():
    assert get_engine_info()["schema_version"] == "195"


def test_engine_info_review_only():
    assert get_engine_info()["review_only"] is True
