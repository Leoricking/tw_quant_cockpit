"""
tests/test_decision_journal_models_v189.py
Tests for decision_journal_models_v189 — Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_journal_models_v189 import (
    DecisionJournalEntry, DecisionJournalBook, DecisionReviewInput, DecisionReviewResult,
    DecisionOutcomeSnapshot, PaperDecisionLifecycle, PaperDecisionEvidenceLink,
    DecisionMistakeTag, DecisionQualityScore, DailyReviewSummary, WeeklyReviewSummary,
    MonthlyReviewSummary, ReviewChecklist, ReviewFinding, ReviewActionItem,
    ReviewBlockReason, JournalExportManifest, JournalEvidencePack, JournalAuditTrail,
    JournalHealthSummary, JournalDashboard, JournalValidationResult,
    get_all_model_names,
)


def test_model_count_22():
    assert len(get_all_model_names()) == 22


def test_get_all_model_names_returns_list():
    assert isinstance(get_all_model_names(), list)


# ── DecisionJournalEntry ──────────────────────────────────────────────────────

def test_journal_entry_paper_only():
    assert DecisionJournalEntry().paper_only is True


def test_journal_entry_no_real_orders():
    assert DecisionJournalEntry().no_real_orders is True


def test_journal_entry_no_broker():
    assert DecisionJournalEntry().no_broker is True


def test_journal_entry_not_investment_advice():
    assert DecisionJournalEntry().not_investment_advice is True


def test_journal_entry_journal_only():
    assert DecisionJournalEntry().journal_only is True


def test_journal_entry_review_only():
    assert DecisionJournalEntry().review_only is True


def test_journal_entry_audit_only():
    assert DecisionJournalEntry().audit_only is True


def test_journal_entry_production_trading_blocked():
    assert DecisionJournalEntry().production_trading_blocked is True


def test_journal_entry_default_state():
    assert DecisionJournalEntry().state == "OBSERVE"


def test_journal_entry_default_schema():
    assert DecisionJournalEntry().schema_version == "189"


def test_journal_entry_timestamp_policy():
    assert DecisionJournalEntry().deterministic_timestamp_policy == "date_label_only_no_wall_clock"


def test_journal_entry_custom_fields():
    e = DecisionJournalEntry(entry_id="E1", symbol="TSMC", state="PAPER_PLAN_READY",
                              rationale="A-point confirmed", planned_size_pct=10.0)
    assert e.entry_id == "E1"
    assert e.symbol == "TSMC"
    assert e.state == "PAPER_PLAN_READY"
    assert e.rationale == "A-point confirmed"
    assert e.planned_size_pct == 10.0


def test_journal_entry_evidence_refs_default_empty():
    assert DecisionJournalEntry().evidence_refs == []


# ── DecisionJournalBook ───────────────────────────────────────────────────────

def test_journal_book_paper_only():
    assert DecisionJournalBook().paper_only is True


def test_journal_book_journal_only():
    assert DecisionJournalBook().journal_only is True


def test_journal_book_no_real_orders():
    assert DecisionJournalBook().no_real_orders is True


def test_journal_book_production_trading_blocked():
    assert DecisionJournalBook().production_trading_blocked is True


def test_journal_book_default_schema():
    assert DecisionJournalBook().schema_version == "189"


def test_journal_book_entries_default_empty():
    assert DecisionJournalBook().entries == []


# ── DecisionReviewInput ───────────────────────────────────────────────────────

def test_review_input_paper_only():
    assert DecisionReviewInput().paper_only is True


def test_review_input_journal_only():
    assert DecisionReviewInput().journal_only is True


def test_review_input_review_only():
    assert DecisionReviewInput().review_only is True


def test_review_input_default_review_type():
    assert DecisionReviewInput().review_type == "daily_review"


def test_review_input_no_broker():
    assert DecisionReviewInput().no_broker is True


def test_review_input_schema_189():
    assert DecisionReviewInput().schema_version == "189"


# ── DecisionReviewResult ──────────────────────────────────────────────────────

def test_review_result_paper_only():
    assert DecisionReviewResult().paper_only is True


def test_review_result_journal_only():
    assert DecisionReviewResult().journal_only is True


def test_review_result_not_blocked_by_default():
    assert DecisionReviewResult().blocked is False


def test_review_result_default_grade():
    assert DecisionReviewResult().review_grade == "ACCEPTABLE"


# ── DecisionOutcomeSnapshot ───────────────────────────────────────────────────

def test_outcome_snapshot_paper_only():
    assert DecisionOutcomeSnapshot().paper_only is True


def test_outcome_snapshot_no_real_orders():
    assert DecisionOutcomeSnapshot().no_real_orders is True


def test_outcome_snapshot_schema_189():
    assert DecisionOutcomeSnapshot().schema_version == "189"


# ── PaperDecisionLifecycle ────────────────────────────────────────────────────

def test_lifecycle_paper_only():
    assert PaperDecisionLifecycle().paper_only is True


def test_lifecycle_journal_only():
    assert PaperDecisionLifecycle().journal_only is True


def test_lifecycle_not_closed_by_default():
    assert PaperDecisionLifecycle().is_closed is False


# ── PaperDecisionEvidenceLink ─────────────────────────────────────────────────

def test_evidence_link_paper_only():
    assert PaperDecisionEvidenceLink().paper_only is True


def test_evidence_link_journal_only():
    assert PaperDecisionEvidenceLink().journal_only is True


def test_evidence_link_audit_only():
    assert PaperDecisionEvidenceLink().audit_only is True


# ── DecisionMistakeTag ────────────────────────────────────────────────────────

def test_mistake_tag_paper_only():
    assert DecisionMistakeTag().paper_only is True


def test_mistake_tag_default_tag():
    assert DecisionMistakeTag().tag == "NO_MISTAKE_FOUND"


def test_mistake_tag_review_only():
    assert DecisionMistakeTag().review_only is True


# ── DecisionQualityScore ──────────────────────────────────────────────────────

def test_quality_score_paper_only():
    assert DecisionQualityScore().paper_only is True


def test_quality_score_default_grade():
    assert DecisionQualityScore().grade == "ACCEPTABLE"


def test_quality_score_default_score():
    assert DecisionQualityScore().score == 0.0


# ── DailyReviewSummary ────────────────────────────────────────────────────────

def test_daily_review_paper_only():
    assert DailyReviewSummary().paper_only is True


def test_daily_review_journal_only():
    assert DailyReviewSummary().journal_only is True


def test_daily_review_review_only():
    assert DailyReviewSummary().review_only is True


def test_daily_review_default_grade():
    assert DailyReviewSummary().grade == "ACCEPTABLE"


def test_daily_review_no_broker():
    assert DailyReviewSummary().no_broker is True


# ── WeeklyReviewSummary ───────────────────────────────────────────────────────

def test_weekly_review_paper_only():
    assert WeeklyReviewSummary().paper_only is True


def test_weekly_review_journal_only():
    assert WeeklyReviewSummary().journal_only is True


def test_weekly_review_default_grade():
    assert WeeklyReviewSummary().weekly_grade == "ACCEPTABLE"


def test_weekly_review_risk_budget_exceeded_false():
    assert WeeklyReviewSummary().risk_budget_exceeded is False


def test_weekly_review_over_concentration_false():
    assert WeeklyReviewSummary().over_concentration_detected is False


# ── MonthlyReviewSummary ──────────────────────────────────────────────────────

def test_monthly_review_paper_only():
    assert MonthlyReviewSummary().paper_only is True


def test_monthly_review_journal_only():
    assert MonthlyReviewSummary().journal_only is True


def test_monthly_review_default_grade():
    assert MonthlyReviewSummary().monthly_grade == "ACCEPTABLE"


# ── ReviewChecklist ───────────────────────────────────────────────────────────

def test_review_checklist_paper_only():
    assert ReviewChecklist().paper_only is True


def test_review_checklist_review_only():
    assert ReviewChecklist().review_only is True


def test_review_checklist_default_not_complete():
    assert ReviewChecklist().all_complete is False


# ── ReviewFinding ─────────────────────────────────────────────────────────────

def test_review_finding_paper_only():
    assert ReviewFinding().paper_only is True


def test_review_finding_review_only():
    assert ReviewFinding().review_only is True


def test_review_finding_default_severity():
    assert ReviewFinding().severity == "LOW"


# ── ReviewActionItem ──────────────────────────────────────────────────────────

def test_review_action_item_paper_only():
    assert ReviewActionItem().paper_only is True


def test_review_action_item_not_complete_by_default():
    assert ReviewActionItem().is_complete is False


def test_review_action_item_default_priority():
    assert ReviewActionItem().priority == "MEDIUM"


# ── ReviewBlockReason ─────────────────────────────────────────────────────────

def test_review_block_reason_paper_only():
    assert ReviewBlockReason().paper_only is True


def test_review_block_reason_review_only():
    assert ReviewBlockReason().review_only is True


# ── JournalExportManifest ─────────────────────────────────────────────────────

def test_export_manifest_paper_only():
    assert JournalExportManifest().paper_only is True


def test_export_manifest_audit_only():
    assert JournalExportManifest().audit_only is True


def test_export_manifest_default_format():
    assert JournalExportManifest().format == "json"


# ── JournalEvidencePack ───────────────────────────────────────────────────────

def test_evidence_pack_paper_only():
    assert JournalEvidencePack().paper_only is True


def test_evidence_pack_journal_only():
    assert JournalEvidencePack().journal_only is True


def test_evidence_pack_evidence_links_default():
    assert JournalEvidencePack().evidence_links == []


# ── JournalAuditTrail ─────────────────────────────────────────────────────────

def test_audit_trail_paper_only():
    assert JournalAuditTrail().paper_only is True


def test_audit_trail_audit_only():
    assert JournalAuditTrail().audit_only is True


def test_audit_trail_is_complete_by_default():
    assert JournalAuditTrail().is_complete is True


# ── JournalHealthSummary ──────────────────────────────────────────────────────

def test_health_summary_paper_only():
    assert JournalHealthSummary().paper_only is True


def test_health_summary_default_status():
    assert JournalHealthSummary().status == "FAIL"


def test_health_summary_all_passed_false_by_default():
    assert JournalHealthSummary().all_passed is False


# ── JournalDashboard ──────────────────────────────────────────────────────────

def test_dashboard_paper_only():
    assert JournalDashboard().paper_only is True


def test_dashboard_journal_only():
    assert JournalDashboard().journal_only is True


def test_dashboard_review_only():
    assert JournalDashboard().review_only is True


def test_dashboard_report_only():
    assert JournalDashboard().report_only is True


def test_dashboard_audit_only():
    assert JournalDashboard().audit_only is True


def test_dashboard_default_grade():
    assert JournalDashboard().overall_grade == "ACCEPTABLE"


# ── JournalValidationResult ───────────────────────────────────────────────────

def test_validation_result_paper_only():
    assert JournalValidationResult().paper_only is True


def test_validation_result_valid_by_default():
    assert JournalValidationResult().is_valid is True


def test_validation_result_not_blocked_by_default():
    assert JournalValidationResult().blocked is False


def test_validation_result_errors_empty_by_default():
    assert JournalValidationResult().errors == []
