"""
tests/test_strategy_review_models_v195.py
Tests for strategy review models v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_review_models_v195 import (
    StrategyReviewInput, StrategyReviewResult,
    ReviewAlert, ReviewAlertSource, ReviewAlertSeverity, ReviewAlertCategory,
    HumanApprovalRequest, HumanApprovalChecklist, HumanApprovalDecision,
    ReviewDecisionState, ReviewDecisionRationale,
    RollbackReviewTicket, ReviewEvidenceLink, ReviewEvidencePack,
    ReviewFinding, ReviewRecommendation,
    ReviewExportManifest, ReviewAuditTrail, ReviewDashboard,
    ReviewHealthSummary, ReviewValidationResult,
    ReviewQueue, ReviewQueueSummary, ReviewSlaStatus, ReviewEscalationRule,
    get_all_model_names,
)


# ── model names ───────────────────────────────────────────────────────────────

def test_model_names_count():
    assert len(get_all_model_names()) == 25


def test_model_names_includes_strategy_review_input():
    assert "StrategyReviewInput" in get_all_model_names()


def test_model_names_includes_human_approval_decision():
    assert "HumanApprovalDecision" in get_all_model_names()


def test_model_names_includes_rollback_review_ticket():
    assert "RollbackReviewTicket" in get_all_model_names()


# ── StrategyReviewInput ───────────────────────────────────────────────────────

def test_strategy_review_input_paper_only():
    assert StrategyReviewInput().paper_only is True


def test_strategy_review_input_no_real_orders():
    assert StrategyReviewInput().no_real_orders is True


def test_strategy_review_input_review_only():
    assert StrategyReviewInput().review_only is True


def test_strategy_review_input_schema_version():
    assert StrategyReviewInput().schema_version == "195"


def test_strategy_review_input_not_investment_advice():
    assert StrategyReviewInput().not_investment_advice is True


# ── StrategyReviewResult ──────────────────────────────────────────────────────

def test_strategy_review_result_no_real_orders():
    assert StrategyReviewResult().no_real_orders is True


def test_strategy_review_result_paper_only():
    assert StrategyReviewResult().paper_only is True


# ── ReviewAlert ───────────────────────────────────────────────────────────────

def test_review_alert_paper_only():
    assert ReviewAlert().paper_only is True


def test_review_alert_not_investment_advice():
    assert ReviewAlert().not_investment_advice is True


# ── ReviewAlertSource ─────────────────────────────────────────────────────────

def test_review_alert_source_paper_only():
    assert ReviewAlertSource().paper_only is True


# ── ReviewAlertSeverity ───────────────────────────────────────────────────────

def test_review_alert_severity_no_real_orders():
    assert ReviewAlertSeverity().no_real_orders is True


# ── ReviewAlertCategory ───────────────────────────────────────────────────────

def test_review_alert_category_not_investment_advice():
    assert ReviewAlertCategory().not_investment_advice is True


# ── HumanApprovalRequest ──────────────────────────────────────────────────────

def test_human_approval_request_paper_only():
    assert HumanApprovalRequest().paper_only is True


def test_human_approval_request_requires_manual_review():
    assert HumanApprovalRequest().requires_manual_review is True


def test_human_approval_request_no_auto_approval():
    assert HumanApprovalRequest().auto_approval is False


# ── HumanApprovalChecklist ────────────────────────────────────────────────────

def test_human_approval_checklist_human_approval_only():
    assert HumanApprovalChecklist().human_approval_only is True


def test_human_approval_checklist_no_real_orders():
    assert HumanApprovalChecklist().no_real_orders is True


# ── HumanApprovalDecision ─────────────────────────────────────────────────────

def test_human_approval_decision_auto_approval_false():
    assert HumanApprovalDecision().auto_approval is False


def test_human_approval_decision_requires_manual_review():
    assert HumanApprovalDecision().requires_manual_review is True


def test_human_approval_decision_paper_only():
    assert HumanApprovalDecision().paper_only is True


def test_human_approval_decision_not_investment_advice():
    assert HumanApprovalDecision().not_investment_advice is True


# ── ReviewDecisionState ───────────────────────────────────────────────────────

def test_review_decision_state_paper_only():
    assert ReviewDecisionState().paper_only is True


def test_review_decision_state_no_real_orders():
    assert ReviewDecisionState().no_real_orders is True


# ── ReviewDecisionRationale ───────────────────────────────────────────────────

def test_review_decision_rationale_not_investment_advice():
    assert ReviewDecisionRationale().not_investment_advice is True


# ── RollbackReviewTicket ──────────────────────────────────────────────────────

def test_rollback_review_ticket_auto_rollback_false():
    assert RollbackReviewTicket().auto_rollback is False


def test_rollback_review_ticket_requires_manual_review():
    assert RollbackReviewTicket().requires_manual_review is True


def test_rollback_review_ticket_paper_only():
    assert RollbackReviewTicket().paper_only is True


def test_rollback_review_ticket_rollback_review_only():
    assert RollbackReviewTicket().rollback_review_only is True


# ── ReviewEvidenceLink ────────────────────────────────────────────────────────

def test_review_evidence_link_paper_only():
    assert ReviewEvidenceLink().paper_only is True


# ── ReviewEvidencePack ────────────────────────────────────────────────────────

def test_review_evidence_pack_audit_only():
    assert ReviewEvidencePack().audit_only is True


# ── ReviewFinding ─────────────────────────────────────────────────────────────

def test_review_finding_not_investment_advice():
    assert ReviewFinding().not_investment_advice is True


# ── ReviewRecommendation ──────────────────────────────────────────────────────

def test_review_recommendation_production_trading_blocked():
    assert ReviewRecommendation().production_trading_blocked is True


# ── ReviewExportManifest ──────────────────────────────────────────────────────

def test_review_export_manifest_report_only():
    assert ReviewExportManifest().report_only is True


# ── ReviewAuditTrail ──────────────────────────────────────────────────────────

def test_review_audit_trail_audit_only():
    assert ReviewAuditTrail().audit_only is True


# ── ReviewDashboard ───────────────────────────────────────────────────────────

def test_review_dashboard_no_real_orders():
    assert ReviewDashboard().no_real_orders is True


# ── ReviewHealthSummary ───────────────────────────────────────────────────────

def test_review_health_summary_schema_version():
    assert ReviewHealthSummary().schema_version == "195"


# ── ReviewValidationResult ────────────────────────────────────────────────────

def test_review_validation_result_review_only():
    assert ReviewValidationResult().review_only is True


# ── ReviewQueue ───────────────────────────────────────────────────────────────

def test_review_queue_auto_processing_false():
    assert ReviewQueue().auto_processing is False


def test_review_queue_paper_only():
    assert ReviewQueue().paper_only is True


# ── ReviewQueueSummary ────────────────────────────────────────────────────────

def test_review_queue_summary_no_real_orders():
    assert ReviewQueueSummary().no_real_orders is True


# ── ReviewSlaStatus ───────────────────────────────────────────────────────────

def test_review_sla_status_paper_only():
    assert ReviewSlaStatus().paper_only is True


# ── ReviewEscalationRule ──────────────────────────────────────────────────────

def test_review_escalation_rule_auto_escalate_execution_false():
    assert ReviewEscalationRule().auto_escalate_execution is False


def test_review_escalation_rule_requires_manual_review():
    assert ReviewEscalationRule().escalate_to_manual is True
