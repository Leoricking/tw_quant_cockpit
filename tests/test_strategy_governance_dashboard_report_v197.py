"""
tests/test_strategy_governance_dashboard_report_v197.py
Tests for strategy_governance_dashboard_report_v197.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_governance_dashboard_report_v197 import (
    REPORT_SECTIONS, get_report_section_names,
    export_quality_overview_report, export_evidence_coverage_report,
    export_decision_outcome_report, export_approval_quality_report,
    export_rejection_quality_report, export_monitoring_quality_report,
    export_rollback_frequency_report, export_violations_report,
    export_scorecard_report, export_audit_summary_report,
    export_full_dashboard_pack,
)


# ── REPORT_SECTIONS ───────────────────────────────────────────────────────────
def test_report_sections_is_list(): assert isinstance(REPORT_SECTIONS, list)
def test_report_sections_count_12(): assert len(REPORT_SECTIONS) == 12
def test_report_sections_has_quality_overview(): assert "quality_overview_report" in REPORT_SECTIONS
def test_report_sections_has_scorecard(): assert "scorecard_report" in REPORT_SECTIONS
def test_report_sections_has_audit_summary(): assert "audit_summary_report" in REPORT_SECTIONS

def test_get_report_section_names_returns_list(): assert isinstance(get_report_section_names(), list)
def test_get_report_section_names_count_12(): assert len(get_report_section_names()) == 12

# ── export_quality_overview_report ────────────────────────────────────────────
def test_overview_valid(): assert export_quality_overview_report("REG-001")["valid"] is True
def test_overview_paper_only(): assert export_quality_overview_report("REG-001")["paper_only"] is True
def test_overview_no_real_orders(): assert export_quality_overview_report("REG-001")["no_real_orders"] is True
def test_overview_section_name(): assert export_quality_overview_report("REG-001")["section"] == "quality_overview_report"
def test_overview_missing_source_blocked(): assert export_quality_overview_report("")["blocked"] is True
def test_overview_missing_source_not_valid(): assert export_quality_overview_report("")["valid"] is False

# ── export_evidence_coverage_report ──────────────────────────────────────────
def test_evidence_valid(): assert export_evidence_coverage_report("REG-001")["valid"] is True
def test_evidence_paper_only(): assert export_evidence_coverage_report("REG-001")["paper_only"] is True
def test_evidence_section_name(): assert export_evidence_coverage_report("REG-001")["section"] == "evidence_coverage_report"
def test_evidence_missing_source_blocked(): assert export_evidence_coverage_report("")["blocked"] is True

# ── export_decision_outcome_report ────────────────────────────────────────────
def test_outcome_valid(): assert export_decision_outcome_report("REG-001")["valid"] is True
def test_outcome_paper_only(): assert export_decision_outcome_report("REG-001")["paper_only"] is True
def test_outcome_section_name(): assert export_decision_outcome_report("REG-001")["section"] == "decision_outcome_report"
def test_outcome_missing_source_blocked(): assert export_decision_outcome_report("")["blocked"] is True

# ── export_approval_quality_report ────────────────────────────────────────────
def test_approval_valid(): assert export_approval_quality_report("REG-001")["valid"] is True
def test_approval_no_auto_approval(): assert export_approval_quality_report("REG-001")["auto_approval"] is False
def test_approval_no_production_mutation(): assert export_approval_quality_report("REG-001")["no_production_mutation"] is True
def test_approval_missing_source_blocked(): assert export_approval_quality_report("")["blocked"] is True

# ── export_rejection_quality_report ───────────────────────────────────────────
def test_rejection_valid(): assert export_rejection_quality_report("REG-001")["valid"] is True
def test_rejection_paper_only(): assert export_rejection_quality_report("REG-001")["paper_only"] is True
def test_rejection_missing_source_blocked(): assert export_rejection_quality_report("")["blocked"] is True

# ── export_rollback_frequency_report ──────────────────────────────────────────
def test_rollback_freq_valid(): assert export_rollback_frequency_report("REG-001")["valid"] is True
def test_rollback_freq_auto_rollback_false(): assert export_rollback_frequency_report("REG-001")["auto_rollback"] is False
def test_rollback_freq_requires_human_review(): assert export_rollback_frequency_report("REG-001")["requires_human_review"] is True
def test_rollback_freq_missing_source_blocked(): assert export_rollback_frequency_report("")["blocked"] is True

# ── export_violations_report ───────────────────────────────────────────────────
def test_violations_valid(): assert export_violations_report("REG-001")["valid"] is True
def test_violations_paper_only(): assert export_violations_report("REG-001")["paper_only"] is True
def test_violations_missing_source_blocked(): assert export_violations_report("")["blocked"] is True

# ── export_scorecard_report ───────────────────────────────────────────────────
def test_scorecard_valid(): assert export_scorecard_report("REG-001")["valid"] is True
def test_scorecard_metrics_12(): assert export_scorecard_report("REG-001")["scorecard_metrics"] == 12
def test_scorecard_paper_only(): assert export_scorecard_report("REG-001")["paper_only"] is True
def test_scorecard_missing_source_blocked(): assert export_scorecard_report("")["blocked"] is True

# ── export_full_dashboard_pack ────────────────────────────────────────────────
def test_full_pack_valid(): assert export_full_dashboard_pack("REG-001")["valid"] is True
def test_full_pack_paper_only(): assert export_full_dashboard_pack("REG-001")["paper_only"] is True
def test_full_pack_analytics_not_execute(): assert export_full_dashboard_pack("REG-001")["analytics_executes_decision"] is False
def test_full_pack_dashboard_not_mutate(): assert export_full_dashboard_pack("REG-001")["dashboard_mutates_strategy"] is False
def test_full_pack_auto_rollback_false(): assert export_full_dashboard_pack("REG-001")["auto_rollback"] is False
def test_full_pack_auto_approval_false(): assert export_full_dashboard_pack("REG-001")["auto_approval"] is False
def test_full_pack_immutable(): assert export_full_dashboard_pack("REG-001")["immutable"] is True
def test_full_pack_production_mutation_blocked(): assert export_full_dashboard_pack("REG-001")["production_mutation_blocked"] is True
def test_full_pack_live_activation_blocked(): assert export_full_dashboard_pack("REG-001")["live_activation_blocked"] is True
def test_full_pack_sections_included_12(): assert len(export_full_dashboard_pack("REG-001")["sections_included"]) == 12
def test_full_pack_missing_source_blocked(): assert export_full_dashboard_pack("")["blocked"] is True
