"""
tests/test_strategy_monitoring_models_v194.py
Tests for strategy_monitoring_models_v194.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_monitoring_models_v194 import (
    StrategyMonitoringInput, StrategyMonitoringResult, MonitoringPackageSnapshot,
    MonitoringRuleSnapshot, MonitoringWindow, MonitoringMetricSnapshot,
    MonitoringBaselineSnapshot, MonitoringCurrentSnapshot, StrategyDriftSignal,
    DriftDetectionResult, DriftSeverity, DriftCategory, MonitoringRiskStatus,
    MonitoringPerformanceStatus, MonitoringSignalQualityStatus, MonitoringGuardrailStatus,
    MonitoringRollbackTrigger, MonitoringReviewAlert, MonitoringFinding,
    MonitoringRecommendation, MonitoringExportManifest, MonitoringEvidencePack,
    MonitoringAuditTrail, MonitoringDashboard, MonitoringHealthSummary,
    MonitoringValidationResult, get_all_model_names,
)


# ── model count ───────────────────────────────────────────────────────────────

def test_model_names_count():
    assert len(get_all_model_names()) == 26


def test_model_names_is_list():
    assert isinstance(get_all_model_names(), list)


def test_all_model_names_are_strings():
    assert all(isinstance(n, str) for n in get_all_model_names())


# ── StrategyMonitoringInput ───────────────────────────────────────────────────

def test_monitoring_input_paper_only():
    assert StrategyMonitoringInput().paper_only is True


def test_monitoring_input_no_real_orders():
    assert StrategyMonitoringInput().no_real_orders is True


def test_monitoring_input_monitoring_only():
    assert StrategyMonitoringInput().monitoring_only is True


def test_monitoring_input_drift_detection_only():
    assert StrategyMonitoringInput().drift_detection_only is True


def test_monitoring_input_not_investment_advice():
    assert StrategyMonitoringInput().not_investment_advice is True


def test_monitoring_input_schema_version():
    assert StrategyMonitoringInput().schema_version == "194"


def test_monitoring_input_no_broker():
    assert StrategyMonitoringInput().no_broker is True


def test_monitoring_input_production_trading_blocked():
    assert StrategyMonitoringInput().production_trading_blocked is True


# ── StrategyMonitoringResult ──────────────────────────────────────────────────

def test_monitoring_result_no_real_orders():
    assert StrategyMonitoringResult().no_real_orders is True


def test_monitoring_result_paper_only():
    assert StrategyMonitoringResult().paper_only is True


def test_monitoring_result_monitoring_only():
    assert StrategyMonitoringResult().monitoring_only is True


def test_monitoring_result_not_investment_advice():
    assert StrategyMonitoringResult().not_investment_advice is True


def test_monitoring_result_schema_version():
    assert StrategyMonitoringResult().schema_version == "194"


# ── MonitoringPackageSnapshot ─────────────────────────────────────────────────

def test_package_snapshot_paper_only():
    assert MonitoringPackageSnapshot().paper_only is True


def test_package_snapshot_monitoring_only():
    assert MonitoringPackageSnapshot().monitoring_only is True


def test_package_snapshot_no_real_orders():
    assert MonitoringPackageSnapshot().no_real_orders is True


# ── MonitoringRuleSnapshot ────────────────────────────────────────────────────

def test_rule_snapshot_paper_only():
    assert MonitoringRuleSnapshot().paper_only is True


def test_rule_snapshot_monitoring_only():
    assert MonitoringRuleSnapshot().monitoring_only is True


# ── MonitoringWindow ──────────────────────────────────────────────────────────

def test_monitoring_window_paper_only():
    assert MonitoringWindow().paper_only is True


def test_monitoring_window_monitoring_only():
    assert MonitoringWindow().monitoring_only is True


# ── MonitoringMetricSnapshot ──────────────────────────────────────────────────

def test_metric_snapshot_paper_only():
    assert MonitoringMetricSnapshot().paper_only is True


def test_metric_snapshot_monitoring_only():
    assert MonitoringMetricSnapshot().monitoring_only is True


# ── MonitoringBaselineSnapshot ────────────────────────────────────────────────

def test_baseline_snapshot_paper_only():
    assert MonitoringBaselineSnapshot().paper_only is True


def test_baseline_snapshot_no_real_orders():
    assert MonitoringBaselineSnapshot().no_real_orders is True


def test_baseline_snapshot_monitoring_only():
    assert MonitoringBaselineSnapshot().monitoring_only is True


# ── MonitoringCurrentSnapshot ─────────────────────────────────────────────────

def test_current_snapshot_paper_only():
    assert MonitoringCurrentSnapshot().paper_only is True


def test_current_snapshot_monitoring_only():
    assert MonitoringCurrentSnapshot().monitoring_only is True


def test_current_snapshot_drift_detection_only():
    assert MonitoringCurrentSnapshot().drift_detection_only is True


# ── StrategyDriftSignal ───────────────────────────────────────────────────────

def test_drift_signal_paper_only():
    assert StrategyDriftSignal().paper_only is True


def test_drift_signal_drift_detection_only():
    assert StrategyDriftSignal().drift_detection_only is True


def test_drift_signal_no_real_orders():
    assert StrategyDriftSignal().no_real_orders is True


def test_drift_signal_not_for_production():
    assert StrategyDriftSignal().not_for_production is True


# ── DriftDetectionResult ──────────────────────────────────────────────────────

def test_drift_detection_result_paper_only():
    assert DriftDetectionResult().paper_only is True


def test_drift_detection_result_drift_detection_only():
    assert DriftDetectionResult().drift_detection_only is True


def test_drift_detection_result_not_investment_advice():
    assert DriftDetectionResult().not_investment_advice is True


# ── DriftSeverity ─────────────────────────────────────────────────────────────

def test_drift_severity_paper_only():
    assert DriftSeverity().paper_only is True


def test_drift_severity_drift_detection_only():
    assert DriftSeverity().drift_detection_only is True


# ── DriftCategory ─────────────────────────────────────────────────────────────

def test_drift_category_paper_only():
    assert DriftCategory().paper_only is True


def test_drift_category_monitoring_only():
    assert DriftCategory().monitoring_only is True


# ── MonitoringRiskStatus ──────────────────────────────────────────────────────

def test_monitoring_risk_status_paper_only():
    assert MonitoringRiskStatus().paper_only is True


def test_monitoring_risk_status_monitoring_only():
    assert MonitoringRiskStatus().monitoring_only is True


# ── MonitoringPerformanceStatus ───────────────────────────────────────────────

def test_monitoring_performance_status_paper_only():
    assert MonitoringPerformanceStatus().paper_only is True


def test_monitoring_performance_status_monitoring_only():
    assert MonitoringPerformanceStatus().monitoring_only is True


# ── MonitoringSignalQualityStatus ─────────────────────────────────────────────

def test_monitoring_signal_quality_status_paper_only():
    assert MonitoringSignalQualityStatus().paper_only is True


def test_monitoring_signal_quality_status_drift_detection_only():
    assert MonitoringSignalQualityStatus().drift_detection_only is True


# ── MonitoringGuardrailStatus ─────────────────────────────────────────────────

def test_monitoring_guardrail_status_paper_only():
    assert MonitoringGuardrailStatus().paper_only is True


def test_monitoring_guardrail_status_monitoring_only():
    assert MonitoringGuardrailStatus().monitoring_only is True


# ── MonitoringRollbackTrigger ─────────────────────────────────────────────────

def test_rollback_trigger_paper_only():
    assert MonitoringRollbackTrigger().paper_only is True


def test_rollback_trigger_auto_rollback_false():
    assert MonitoringRollbackTrigger().auto_rollback is False


def test_rollback_trigger_requires_manual_review():
    assert MonitoringRollbackTrigger().requires_manual_review is True


def test_rollback_trigger_no_real_orders():
    assert MonitoringRollbackTrigger().no_real_orders is True


def test_rollback_trigger_rollback_trigger_only():
    assert MonitoringRollbackTrigger().rollback_trigger_only is True


# ── MonitoringReviewAlert ─────────────────────────────────────────────────────

def test_monitoring_review_alert_paper_only():
    assert MonitoringReviewAlert().paper_only is True


def test_monitoring_review_alert_monitoring_only():
    assert MonitoringReviewAlert().monitoring_only is True


def test_monitoring_review_alert_requires_manual_review():
    assert MonitoringReviewAlert().requires_manual_review is True


# ── MonitoringFinding ─────────────────────────────────────────────────────────

def test_monitoring_finding_paper_only():
    assert MonitoringFinding().paper_only is True


def test_monitoring_finding_monitoring_only():
    assert MonitoringFinding().monitoring_only is True


def test_monitoring_finding_drift_detection_only():
    assert MonitoringFinding().drift_detection_only is True


# ── MonitoringRecommendation ──────────────────────────────────────────────────

def test_monitoring_recommendation_paper_only():
    assert MonitoringRecommendation().paper_only is True


def test_monitoring_recommendation_monitoring_only():
    assert MonitoringRecommendation().monitoring_only is True


def test_monitoring_recommendation_not_investment_advice():
    assert MonitoringRecommendation().not_investment_advice is True


# ── MonitoringExportManifest ──────────────────────────────────────────────────

def test_monitoring_export_manifest_paper_only():
    assert MonitoringExportManifest().paper_only is True


def test_monitoring_export_manifest_monitoring_only():
    assert MonitoringExportManifest().monitoring_only is True


def test_monitoring_export_manifest_review_only():
    assert MonitoringExportManifest().review_only is True


# ── MonitoringEvidencePack ────────────────────────────────────────────────────

def test_monitoring_evidence_pack_paper_only():
    assert MonitoringEvidencePack().paper_only is True


def test_monitoring_evidence_pack_monitoring_only():
    assert MonitoringEvidencePack().monitoring_only is True


def test_monitoring_evidence_pack_report_only():
    assert MonitoringEvidencePack().report_only is True


# ── MonitoringAuditTrail ──────────────────────────────────────────────────────

def test_monitoring_audit_trail_paper_only():
    assert MonitoringAuditTrail().paper_only is True


def test_monitoring_audit_trail_monitoring_only():
    assert MonitoringAuditTrail().monitoring_only is True


def test_monitoring_audit_trail_audit_only():
    assert MonitoringAuditTrail().audit_only is True


# ── MonitoringDashboard ───────────────────────────────────────────────────────

def test_monitoring_dashboard_paper_only():
    assert MonitoringDashboard().paper_only is True


def test_monitoring_dashboard_monitoring_only():
    assert MonitoringDashboard().monitoring_only is True


def test_monitoring_dashboard_not_investment_advice():
    assert MonitoringDashboard().not_investment_advice is True


# ── MonitoringHealthSummary ───────────────────────────────────────────────────

def test_monitoring_health_summary_paper_only():
    assert MonitoringHealthSummary().paper_only is True


def test_monitoring_health_summary_monitoring_only():
    assert MonitoringHealthSummary().monitoring_only is True


# ── MonitoringValidationResult ────────────────────────────────────────────────

def test_monitoring_validation_result_paper_only():
    assert MonitoringValidationResult().paper_only is True


def test_monitoring_validation_result_monitoring_only():
    assert MonitoringValidationResult().monitoring_only is True


def test_monitoring_validation_result_drift_detection_only():
    assert MonitoringValidationResult().drift_detection_only is True
