"""
tests/test_strategy_governance_dashboard_engine_v197.py
Tests for strategy_governance_dashboard_engine_v197.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_governance_dashboard_engine_v197 import (
    validate_dashboard_action, validate_analytics_window, validate_quality_grade,
    validate_dashboard_panel, build_dashboard_input, build_quality_score,
    build_quality_grade, build_quality_summary, build_evidence_coverage_summary,
    build_outcome_summary, build_violation_summary, build_rollback_review_frequency,
    build_approval_quality_summary, build_rejection_quality_summary,
    build_monitoring_quality_summary, build_consistency_summary,
    build_decision_trend, build_dashboard_panel, build_dashboard_export,
    build_quality_report, build_quality_audit_trail,
    build_quality_health_summary, build_validation_result, get_engine_info,
)


# ── get_engine_info ───────────────────────────────────────────────────────────
def test_engine_info_returns_dict(): assert isinstance(get_engine_info(), dict)
def test_engine_info_paper_only(): assert get_engine_info()["paper_only"] is True
def test_engine_info_governance_analytics_only(): assert get_engine_info()["governance_analytics_only"] is True
def test_engine_info_no_real_orders(): assert get_engine_info()["no_real_orders"] is True
def test_engine_info_not_blocked(): assert get_engine_info()["blocked"] is False
def test_engine_info_has_version(): assert "version" in get_engine_info()
def test_engine_info_dashboard_not_mutate(): assert get_engine_info()["dashboard_mutates_strategy"] is False
def test_engine_info_analytics_not_execute(): assert get_engine_info()["analytics_executes_decision"] is False

# ── validate_dashboard_action ─────────────────────────────────────────────────
def test_validate_buy_blocked(): assert validate_dashboard_action("BUY")["blocked"] is True
def test_validate_buy_not_valid(): assert validate_dashboard_action("BUY")["valid"] is False
def test_validate_sell_blocked(): assert validate_dashboard_action("SELL")["blocked"] is True
def test_validate_broker_order_blocked(): assert validate_dashboard_action("BROKER_ORDER")["blocked"] is True
def test_validate_health_valid(): assert validate_dashboard_action("GOVERNANCE_DASHBOARD_HEALTH")["valid"] is True
def test_validate_health_not_blocked(): assert validate_dashboard_action("GOVERNANCE_DASHBOARD_HEALTH")["blocked"] is False
def test_validate_quality_analytics_valid(): assert validate_dashboard_action("QUALITY_ANALYTICS")["valid"] is True
def test_validate_unknown_not_blocked(): assert validate_dashboard_action("UNKNOWN_ACTION")["blocked"] is False
def test_validate_unknown_not_valid(): assert validate_dashboard_action("UNKNOWN_ACTION")["valid"] is False
def test_validate_empty_not_blocked(): r = validate_dashboard_action(""); assert r["blocked"] is False

# ── validate_analytics_window ─────────────────────────────────────────────────
def test_validate_window_daily_valid(): assert validate_analytics_window("DAILY")["valid"] is True
def test_validate_window_weekly_valid(): assert validate_analytics_window("WEEKLY")["valid"] is True
def test_validate_window_monthly_valid(): assert validate_analytics_window("MONTHLY")["valid"] is True
def test_validate_window_quarterly_valid(): assert validate_analytics_window("QUARTERLY")["valid"] is True
def test_validate_window_full_history_valid(): assert validate_analytics_window("FULL_HISTORY")["valid"] is True
def test_validate_window_empty_blocked(): assert validate_analytics_window("")["blocked"] is True
def test_validate_window_invalid_not_blocked(): r = validate_analytics_window("INVALID"); assert r["blocked"] is False
def test_validate_window_invalid_not_valid(): r = validate_analytics_window("INVALID"); assert r["valid"] is False

# ── validate_quality_grade ────────────────────────────────────────────────────
def test_validate_grade_excellent_valid(): assert validate_quality_grade("EXCELLENT")["valid"] is True
def test_validate_grade_good_valid(): assert validate_quality_grade("GOOD")["valid"] is True
def test_validate_grade_watch_valid(): assert validate_quality_grade("WATCH")["valid"] is True
def test_validate_grade_weak_valid(): assert validate_quality_grade("WEAK")["valid"] is True
def test_validate_grade_invalid_valid(): assert validate_quality_grade("INVALID")["valid"] is True
def test_validate_grade_empty_blocked(): assert validate_quality_grade("")["blocked"] is True
def test_validate_grade_unknown_not_valid(): assert validate_quality_grade("UNKNOWN")["valid"] is False

# ── validate_dashboard_panel ──────────────────────────────────────────────────
def test_validate_panel_quality_overview_valid(): assert validate_dashboard_panel("quality_overview")["valid"] is True
def test_validate_panel_evidence_coverage_valid(): assert validate_dashboard_panel("evidence_coverage")["valid"] is True
def test_validate_panel_export_manifest_valid(): assert validate_dashboard_panel("export_manifest")["valid"] is True
def test_validate_panel_empty_blocked(): assert validate_dashboard_panel("")["blocked"] is True
def test_validate_panel_unknown_not_valid(): assert validate_dashboard_panel("UNKNOWN_PANEL")["valid"] is False

# ── build_dashboard_input ─────────────────────────────────────────────────────
def test_build_input_valid(): r = build_dashboard_input("REG-001"); assert r["valid"] is True
def test_build_input_paper_only(): r = build_dashboard_input("REG-001"); assert r["paper_only"] is True
def test_build_input_no_real_orders(): r = build_dashboard_input("REG-001"); assert r["no_real_orders"] is True
def test_build_input_missing_source_blocked(): assert build_dashboard_input("")["blocked"] is True
def test_build_input_invalid_window_blocked(): assert build_dashboard_input("REG-001", "INVALID_WINDOW")["blocked"] is True
def test_build_input_full_history_valid(): r = build_dashboard_input("REG-001", "FULL_HISTORY"); assert r["valid"] is True
def test_build_input_weekly_valid(): r = build_dashboard_input("REG-001", "WEEKLY"); assert r["valid"] is True

# ── build_quality_score ───────────────────────────────────────────────────────
def test_build_quality_score_valid(): r = build_quality_score("DEC-001"); assert r["valid"] is True
def test_build_quality_score_paper_only(): r = build_quality_score("DEC-001"); assert r["paper_only"] is True
def test_build_quality_score_missing_id_blocked(): assert build_quality_score("")["blocked"] is True
def test_build_quality_score_composite_zero_empty_metrics(): r = build_quality_score("DEC-001"); assert r["composite_score"] == 0.0
def test_build_quality_score_with_metrics():
    m = {"evidence_coverage_score": 0.9, "rationale_completeness_score": 0.8}
    r = build_quality_score("DEC-001", m)
    assert r["composite_score"] > 0.0

# ── build_quality_grade ───────────────────────────────────────────────────────
def test_build_grade_excellent(): r = build_quality_grade("DEC-001", 0.90); assert r["grade"] == "EXCELLENT"
def test_build_grade_good(): r = build_quality_grade("DEC-001", 0.75); assert r["grade"] == "GOOD"
def test_build_grade_watch(): r = build_quality_grade("DEC-001", 0.55); assert r["grade"] == "WATCH"
def test_build_grade_weak(): r = build_quality_grade("DEC-001", 0.30); assert r["grade"] == "WEAK"
def test_build_grade_invalid(): r = build_quality_grade("DEC-001", 0.0); assert r["grade"] == "INVALID"
def test_build_grade_missing_id_blocked(): assert build_quality_grade("")["blocked"] is True
def test_build_grade_paper_only(): assert build_quality_grade("DEC-001", 0.80)["paper_only"] is True

# ── build_quality_summary ─────────────────────────────────────────────────────
def test_build_quality_summary_valid(): r = build_quality_summary("REG-001"); assert r["valid"] is True
def test_build_quality_summary_paper_only(): assert build_quality_summary("REG-001")["paper_only"] is True
def test_build_quality_summary_missing_source_blocked(): assert build_quality_summary("")["blocked"] is True
def test_build_quality_summary_total_zero_no_scores(): r = build_quality_summary("REG-001"); assert r["total_decisions"] == 0

# ── build_evidence_coverage_summary ──────────────────────────────────────────
def test_build_evidence_valid(): r = build_evidence_coverage_summary("REG-001"); assert r["valid"] is True
def test_build_evidence_paper_only(): assert build_evidence_coverage_summary("REG-001")["paper_only"] is True
def test_build_evidence_missing_source_blocked(): assert build_evidence_coverage_summary("")["blocked"] is True

# ── build_outcome_summary ─────────────────────────────────────────────────────
def test_build_outcome_valid(): r = build_outcome_summary("REG-001"); assert r["valid"] is True
def test_build_outcome_paper_only(): assert build_outcome_summary("REG-001")["paper_only"] is True
def test_build_outcome_missing_source_blocked(): assert build_outcome_summary("")["blocked"] is True
def test_build_outcome_approved_zero(): assert build_outcome_summary("REG-001")["approved_count"] == 0

# ── build_violation_summary ───────────────────────────────────────────────────
def test_build_violation_valid(): r = build_violation_summary("REG-001"); assert r["valid"] is True
def test_build_violation_paper_only(): assert build_violation_summary("REG-001")["paper_only"] is True
def test_build_violation_missing_source_blocked(): assert build_violation_summary("")["blocked"] is True

# ── build_rollback_review_frequency ──────────────────────────────────────────
def test_build_rollback_freq_valid(): r = build_rollback_review_frequency("REG-001"); assert r["valid"] is True
def test_build_rollback_freq_auto_rollback_false(): assert build_rollback_review_frequency("REG-001")["auto_rollback"] is False
def test_build_rollback_freq_requires_human_review(): assert build_rollback_review_frequency("REG-001")["requires_human_review"] is True
def test_build_rollback_freq_missing_source_blocked(): assert build_rollback_review_frequency("")["blocked"] is True

# ── build_approval_quality_summary ────────────────────────────────────────────
def test_build_approval_valid(): r = build_approval_quality_summary("REG-001"); assert r["valid"] is True
def test_build_approval_no_auto_approval(): assert build_approval_quality_summary("REG-001")["auto_approval"] is False
def test_build_approval_no_production_mutation(): assert build_approval_quality_summary("REG-001")["no_production_mutation"] is True
def test_build_approval_missing_source_blocked(): assert build_approval_quality_summary("")["blocked"] is True

# ── build_rejection_quality_summary ───────────────────────────────────────────
def test_build_rejection_valid(): r = build_rejection_quality_summary("REG-001"); assert r["valid"] is True
def test_build_rejection_paper_only(): assert build_rejection_quality_summary("REG-001")["paper_only"] is True
def test_build_rejection_missing_source_blocked(): assert build_rejection_quality_summary("")["blocked"] is True

# ── build_monitoring_quality_summary ─────────────────────────────────────────
def test_build_monitoring_valid(): r = build_monitoring_quality_summary("REG-001"); assert r["valid"] is True
def test_build_monitoring_paper_only(): assert build_monitoring_quality_summary("REG-001")["paper_only"] is True
def test_build_monitoring_missing_source_blocked(): assert build_monitoring_quality_summary("")["blocked"] is True

# ── build_consistency_summary ─────────────────────────────────────────────────
def test_build_consistency_valid(): r = build_consistency_summary("REG-001"); assert r["valid"] is True
def test_build_consistency_paper_only(): assert build_consistency_summary("REG-001")["paper_only"] is True
def test_build_consistency_missing_source_blocked(): assert build_consistency_summary("")["blocked"] is True

# ── build_decision_trend ──────────────────────────────────────────────────────
def test_build_trend_valid(): r = build_decision_trend("REG-001"); assert r["valid"] is True
def test_build_trend_stable_default(): assert build_decision_trend("REG-001")["trend_direction"] == "STABLE"
def test_build_trend_missing_source_blocked(): assert build_decision_trend("")["blocked"] is True

# ── build_dashboard_panel ─────────────────────────────────────────────────────
def test_build_panel_quality_overview_valid(): r = build_dashboard_panel("quality_overview"); assert r["valid"] is True
def test_build_panel_evidence_coverage_valid(): r = build_dashboard_panel("evidence_coverage"); assert r["valid"] is True
def test_build_panel_empty_blocked(): assert build_dashboard_panel("")["blocked"] is True
def test_build_panel_unknown_blocked(): assert build_dashboard_panel("UNKNOWN_PANEL")["blocked"] is True
def test_build_panel_paper_only(): assert build_dashboard_panel("quality_overview")["paper_only"] is True

# ── build_dashboard_export ────────────────────────────────────────────────────
def test_build_export_valid_path(): r = build_dashboard_export("output/report.json"); assert r["valid"] is True
def test_build_export_safe_path_only(): assert build_dashboard_export("output/report.json")["safe_path_only"] is True
def test_build_export_paper_only(): assert build_dashboard_export("output/report.json")["paper_only"] is True
def test_build_export_unsafe_path_blocked(): assert build_dashboard_export("C:/prod_db/data.json")["blocked"] is True
def test_build_export_empty_path_blocked(): assert build_dashboard_export("")["blocked"] is True

# ── build_quality_report ──────────────────────────────────────────────────────
def test_build_quality_report_valid(): r = build_quality_report("REG-001"); assert r["valid"] is True
def test_build_quality_report_paper_only(): assert build_quality_report("REG-001")["paper_only"] is True
def test_build_quality_report_missing_source_blocked(): assert build_quality_report("")["blocked"] is True
def test_build_quality_report_has_sections(): assert len(build_quality_report("REG-001")["report_sections"]) > 0

# ── build_quality_audit_trail ─────────────────────────────────────────────────
def test_build_audit_valid(): r = build_quality_audit_trail("RUN-001"); assert r["valid"] is True
def test_build_audit_immutable(): assert build_quality_audit_trail("RUN-001")["immutable"] is True
def test_build_audit_paper_only(): assert build_quality_audit_trail("RUN-001")["paper_only"] is True
def test_build_audit_missing_id_blocked(): assert build_quality_audit_trail("")["blocked"] is True

# ── build_validation_result ───────────────────────────────────────────────────
def test_build_validation_valid(): r = build_validation_result("REG-001"); assert r["valid"] is True
def test_build_validation_paper_only(): assert build_validation_result("REG-001")["paper_only"] is True
def test_build_validation_missing_source_blocked(): assert build_validation_result("")["blocked"] is True
def test_build_validation_passes_full_history(): r = build_validation_result("REG-001", "FULL_HISTORY"); assert r["governance_passed"] is True
