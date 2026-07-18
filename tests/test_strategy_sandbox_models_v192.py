"""tests/test_strategy_sandbox_models_v192.py
Tests for strategy sandbox data models v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_sandbox_models_v192 import (
    StrategySandboxInput, StrategySandboxResult,
    ShadowValidationInput, ShadowValidationResult,
    SandboxRuleSet, SandboxRuleChange, SandboxGuardrailSet,
    ShadowComparisonResult, BaselineStrategySnapshot, CandidateStrategySnapshot,
    SandboxPerformanceDelta, SandboxRiskDelta, SandboxSignalDelta,
    SandboxApprovalState, SandboxBlockReason, SandboxValidationFinding,
    SandboxRecommendation, SandboxExportManifest, SandboxEvidencePack,
    SandboxAuditTrail, SandboxDashboard, SandboxHealthSummary,
    SandboxValidationResult, get_all_model_names,
)


# ── get_all_model_names ───────────────────────────────────────────────────────

def test_get_all_model_names_count_23():
    assert len(get_all_model_names()) == 23

def test_all_model_names_are_strings():
    assert all(isinstance(n, str) for n in get_all_model_names())

def test_model_names_contains_sandbox_input():
    assert "StrategySandboxInput" in get_all_model_names()

def test_model_names_contains_sandbox_result():
    assert "StrategySandboxResult" in get_all_model_names()

def test_model_names_contains_shadow_validation_input():
    assert "ShadowValidationInput" in get_all_model_names()

def test_model_names_contains_health_summary():
    assert "SandboxHealthSummary" in get_all_model_names()

def test_model_names_contains_validation_result():
    assert "SandboxValidationResult" in get_all_model_names()

def test_model_names_contains_sandbox_dashboard():
    assert "SandboxDashboard" in get_all_model_names()

def test_model_names_contains_sandbox_audit_trail():
    assert "SandboxAuditTrail" in get_all_model_names()


# ── StrategySandboxInput ──────────────────────────────────────────────────────

def test_sandbox_input_paper_only():
    assert StrategySandboxInput().paper_only is True

def test_sandbox_input_sandbox_only():
    assert StrategySandboxInput().sandbox_only is True

def test_sandbox_input_shadow_only():
    assert StrategySandboxInput().shadow_only is True

def test_sandbox_input_no_real_orders():
    assert StrategySandboxInput().no_real_orders is True

def test_sandbox_input_no_broker():
    assert StrategySandboxInput().no_broker is True

def test_sandbox_input_no_production_strategy_mutation():
    assert StrategySandboxInput().no_production_strategy_mutation is True

def test_sandbox_input_no_live_strategy_activation():
    assert StrategySandboxInput().no_live_strategy_activation is True

def test_sandbox_input_not_investment_advice():
    assert StrategySandboxInput().not_investment_advice is True

def test_sandbox_input_production_trading_blocked():
    assert StrategySandboxInput().production_trading_blocked is True

def test_sandbox_input_schema_version_192():
    assert StrategySandboxInput().schema_version == "192"


# ── StrategySandboxResult ─────────────────────────────────────────────────────

def test_sandbox_result_paper_only():
    assert StrategySandboxResult().paper_only is True

def test_sandbox_result_sandbox_only():
    assert StrategySandboxResult().sandbox_only is True

def test_sandbox_result_shadow_only():
    assert StrategySandboxResult().shadow_only is True

def test_sandbox_result_no_real_orders():
    assert StrategySandboxResult().no_real_orders is True

def test_sandbox_result_no_broker():
    assert StrategySandboxResult().no_broker is True

def test_sandbox_result_no_production_strategy_mutation():
    assert StrategySandboxResult().no_production_strategy_mutation is True

def test_sandbox_result_no_live_strategy_activation():
    assert StrategySandboxResult().no_live_strategy_activation is True

def test_sandbox_result_not_investment_advice():
    assert StrategySandboxResult().not_investment_advice is True

def test_sandbox_result_production_trading_blocked():
    assert StrategySandboxResult().production_trading_blocked is True

def test_sandbox_result_default_approval_state():
    assert StrategySandboxResult().approval_state == "SHADOW_ONLY"

def test_sandbox_result_schema_version_192():
    assert StrategySandboxResult().schema_version == "192"


# ── ShadowValidationInput ─────────────────────────────────────────────────────

def test_shadow_validation_input_paper_only():
    assert ShadowValidationInput().paper_only is True

def test_shadow_validation_input_sandbox_only():
    assert ShadowValidationInput().sandbox_only is True

def test_shadow_validation_input_shadow_only():
    assert ShadowValidationInput().shadow_only is True

def test_shadow_validation_input_no_real_orders():
    assert ShadowValidationInput().no_real_orders is True

def test_shadow_validation_input_no_broker():
    assert ShadowValidationInput().no_broker is True

def test_shadow_validation_input_no_production_strategy_mutation():
    assert ShadowValidationInput().no_production_strategy_mutation is True

def test_shadow_validation_input_no_live_strategy_activation():
    assert ShadowValidationInput().no_live_strategy_activation is True

def test_shadow_validation_input_not_investment_advice():
    assert ShadowValidationInput().not_investment_advice is True

def test_shadow_validation_input_production_trading_blocked():
    assert ShadowValidationInput().production_trading_blocked is True


# ── ShadowValidationResult ────────────────────────────────────────────────────

def test_shadow_validation_result_paper_only():
    assert ShadowValidationResult().paper_only is True

def test_shadow_validation_result_sandbox_only():
    assert ShadowValidationResult().sandbox_only is True

def test_shadow_validation_result_shadow_only():
    assert ShadowValidationResult().shadow_only is True

def test_shadow_validation_result_no_real_orders():
    assert ShadowValidationResult().no_real_orders is True

def test_shadow_validation_result_no_broker():
    assert ShadowValidationResult().no_broker is True

def test_shadow_validation_result_no_production_strategy_mutation():
    assert ShadowValidationResult().no_production_strategy_mutation is True

def test_shadow_validation_result_no_live_strategy_activation():
    assert ShadowValidationResult().no_live_strategy_activation is True

def test_shadow_validation_result_not_investment_advice():
    assert ShadowValidationResult().not_investment_advice is True

def test_shadow_validation_result_production_trading_blocked():
    assert ShadowValidationResult().production_trading_blocked is True


# ── SandboxRuleSet ────────────────────────────────────────────────────────────

def test_sandbox_ruleset_paper_only():
    assert SandboxRuleSet().paper_only is True

def test_sandbox_ruleset_sandbox_only():
    assert SandboxRuleSet().sandbox_only is True

def test_sandbox_ruleset_shadow_only():
    assert SandboxRuleSet().shadow_only is True

def test_sandbox_ruleset_no_real_orders():
    assert SandboxRuleSet().no_real_orders is True

def test_sandbox_ruleset_no_broker():
    assert SandboxRuleSet().no_broker is True

def test_sandbox_ruleset_no_production_strategy_mutation():
    assert SandboxRuleSet().no_production_strategy_mutation is True

def test_sandbox_ruleset_no_live_strategy_activation():
    assert SandboxRuleSet().no_live_strategy_activation is True

def test_sandbox_ruleset_not_investment_advice():
    assert SandboxRuleSet().not_investment_advice is True

def test_sandbox_ruleset_production_trading_blocked():
    assert SandboxRuleSet().production_trading_blocked is True


# ── SandboxRuleChange ─────────────────────────────────────────────────────────

def test_sandbox_rule_change_paper_only():
    assert SandboxRuleChange().paper_only is True

def test_sandbox_rule_change_sandbox_only():
    assert SandboxRuleChange().sandbox_only is True

def test_sandbox_rule_change_no_production_strategy_mutation():
    assert SandboxRuleChange().no_production_strategy_mutation is True

def test_sandbox_rule_change_no_live_strategy_activation():
    assert SandboxRuleChange().no_live_strategy_activation is True

def test_sandbox_rule_change_production_trading_blocked():
    assert SandboxRuleChange().production_trading_blocked is True


# ── SandboxGuardrailSet ───────────────────────────────────────────────────────

def test_sandbox_guardrail_set_paper_only():
    assert SandboxGuardrailSet().paper_only is True

def test_sandbox_guardrail_set_no_margin():
    assert SandboxGuardrailSet().no_margin is True

def test_sandbox_guardrail_set_no_leverage():
    assert SandboxGuardrailSet().no_leverage is True

def test_sandbox_guardrail_set_no_production_strategy_mutation():
    assert SandboxGuardrailSet().no_production_strategy_mutation is True


# ── ShadowComparisonResult ────────────────────────────────────────────────────

def test_shadow_comparison_result_paper_only():
    assert ShadowComparisonResult().paper_only is True

def test_shadow_comparison_result_no_leverage():
    assert ShadowComparisonResult().no_leverage is True

def test_shadow_comparison_result_improvement_detected_default():
    assert ShadowComparisonResult().improvement_detected is False

def test_shadow_comparison_result_regression_detected_default():
    assert ShadowComparisonResult().regression_detected is False


# ── BaselineStrategySnapshot ──────────────────────────────────────────────────

def test_baseline_snapshot_paper_only():
    assert BaselineStrategySnapshot().paper_only is True

def test_baseline_snapshot_no_production_strategy_mutation():
    assert BaselineStrategySnapshot().no_production_strategy_mutation is True

def test_baseline_snapshot_no_live_strategy_activation():
    assert BaselineStrategySnapshot().no_live_strategy_activation is True


# ── CandidateStrategySnapshot ─────────────────────────────────────────────────

def test_candidate_snapshot_paper_only():
    assert CandidateStrategySnapshot().paper_only is True

def test_candidate_snapshot_no_live_strategy_activation():
    assert CandidateStrategySnapshot().no_live_strategy_activation is True

def test_candidate_snapshot_no_production_strategy_mutation():
    assert CandidateStrategySnapshot().no_production_strategy_mutation is True


# ── SandboxPerformanceDelta ───────────────────────────────────────────────────

def test_performance_delta_paper_only():
    assert SandboxPerformanceDelta().paper_only is True

def test_performance_delta_not_investment_advice():
    assert SandboxPerformanceDelta().not_investment_advice is True

def test_performance_delta_improvement_detected_default():
    assert SandboxPerformanceDelta().improvement_detected is False


# ── SandboxRiskDelta ──────────────────────────────────────────────────────────

def test_risk_delta_paper_only():
    assert SandboxRiskDelta().paper_only is True

def test_risk_delta_demo_only():
    assert SandboxRiskDelta().demo_only is True

def test_risk_delta_risk_reduction_score_default():
    assert SandboxRiskDelta().risk_reduction_score == 0.0


# ── SandboxSignalDelta ────────────────────────────────────────────────────────

def test_signal_delta_paper_only():
    assert SandboxSignalDelta().paper_only is True

def test_signal_delta_not_for_production():
    assert SandboxSignalDelta().not_for_production is True

def test_signal_delta_count_default():
    assert SandboxSignalDelta().signal_count_delta == 0


# ── SandboxApprovalState ──────────────────────────────────────────────────────

def test_approval_state_paper_only():
    assert SandboxApprovalState().paper_only is True

def test_approval_state_production_trading_blocked():
    assert SandboxApprovalState().production_trading_blocked is True

def test_approval_state_requires_manual_review():
    assert SandboxApprovalState().requires_manual_review is True

def test_approval_state_auto_approve_blocked():
    assert SandboxApprovalState().auto_approve_blocked is True

def test_approval_state_default_state():
    assert SandboxApprovalState().state == "SHADOW_ONLY"


# ── SandboxBlockReason ────────────────────────────────────────────────────────

def test_block_reason_paper_only():
    assert SandboxBlockReason().paper_only is True

def test_block_reason_research_only():
    assert SandboxBlockReason().research_only is True

def test_block_reason_no_production_strategy_mutation():
    assert SandboxBlockReason().no_production_strategy_mutation is True


# ── SandboxValidationFinding ──────────────────────────────────────────────────

def test_validation_finding_paper_only():
    assert SandboxValidationFinding().paper_only is True

def test_validation_finding_simulate_only():
    assert SandboxValidationFinding().simulate_only is True

def test_validation_finding_production_trading_blocked():
    assert SandboxValidationFinding().production_trading_blocked is True


# ── SandboxRecommendation ─────────────────────────────────────────────────────

def test_recommendation_paper_only():
    assert SandboxRecommendation().paper_only is True

def test_recommendation_validation_only():
    assert SandboxRecommendation().validation_only is True

def test_recommendation_default_type():
    assert SandboxRecommendation().recommendation_type == "NO_CHANGE"


# ── SandboxExportManifest ─────────────────────────────────────────────────────

def test_export_manifest_paper_only():
    assert SandboxExportManifest().paper_only is True

def test_export_manifest_review_only():
    assert SandboxExportManifest().review_only is True

def test_export_manifest_safe_path_default():
    assert SandboxExportManifest().safe_path is True

def test_export_manifest_default_export_path():
    assert SandboxExportManifest().export_path == "reports/"


# ── SandboxEvidencePack ───────────────────────────────────────────────────────

def test_evidence_pack_paper_only():
    assert SandboxEvidencePack().paper_only is True

def test_evidence_pack_report_only():
    assert SandboxEvidencePack().report_only is True

def test_evidence_pack_all_evidence_present_default():
    assert SandboxEvidencePack().all_evidence_present is False


# ── SandboxAuditTrail ─────────────────────────────────────────────────────────

def test_audit_trail_paper_only():
    assert SandboxAuditTrail().paper_only is True

def test_audit_trail_audit_only():
    assert SandboxAuditTrail().audit_only is True

def test_audit_trail_audit_complete_default():
    assert SandboxAuditTrail().audit_complete is False


# ── SandboxDashboard ──────────────────────────────────────────────────────────

def test_dashboard_paper_only():
    assert SandboxDashboard().paper_only is True

def test_dashboard_sandbox_only():
    assert SandboxDashboard().sandbox_only is True

def test_dashboard_default_approval_state():
    assert SandboxDashboard().approval_state == "SHADOW_ONLY"

def test_dashboard_regression_detected_default():
    assert SandboxDashboard().regression_detected is False


# ── SandboxHealthSummary ──────────────────────────────────────────────────────

def test_health_summary_paper_only():
    assert SandboxHealthSummary().paper_only is True

def test_health_summary_shadow_only():
    assert SandboxHealthSummary().shadow_only is True

def test_health_summary_default_status():
    assert SandboxHealthSummary().status == "PASS"

def test_health_summary_schema_192():
    assert SandboxHealthSummary().schema_version == "192"


# ── SandboxValidationResult ───────────────────────────────────────────────────

def test_validation_result_paper_only():
    assert SandboxValidationResult().paper_only is True

def test_validation_result_sandbox_only():
    assert SandboxValidationResult().sandbox_only is True

def test_validation_result_production_trading_blocked():
    assert SandboxValidationResult().production_trading_blocked is True

def test_validation_result_schema_192():
    assert SandboxValidationResult().schema_version == "192"
