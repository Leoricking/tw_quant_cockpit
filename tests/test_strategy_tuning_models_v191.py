"""tests/test_strategy_tuning_models_v191.py
Tests for strategy tuning models v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_tuning_models_v191 import (
    StrategyRuleTuningInput, StrategyRuleTuningResult,
    StrategyRuleCandidate, StrategyRuleAdjustment,
    StrategyGuardrail, GuardrailTrigger, GuardrailSeverity, GuardrailAction,
    RuleTuningEvidence, RuleTuningFinding, RuleTuningRecommendation,
    RuleTuningBacktestSnapshot, RuleTuningReviewChecklist,
    RuleTuningApprovalState, RuleTuningExportManifest,
    RuleTuningEvidencePack, RuleTuningAuditTrail, RuleTuningDashboard,
    RuleTuningHealthSummary, RuleTuningValidationResult,
    get_all_model_names,
)


def test_get_all_model_names_length():
    assert len(get_all_model_names()) == 20

def test_all_model_names_are_strings():
    assert all(isinstance(n, str) for n in get_all_model_names())

def test_model_names_contains_tuning_input():
    assert "StrategyRuleTuningInput" in get_all_model_names()

def test_model_names_contains_tuning_result():
    assert "StrategyRuleTuningResult" in get_all_model_names()

def test_model_names_contains_guardrail():
    assert "StrategyGuardrail" in get_all_model_names()

def test_model_names_contains_health_summary():
    assert "RuleTuningHealthSummary" in get_all_model_names()

def test_model_names_contains_validation_result():
    assert "RuleTuningValidationResult" in get_all_model_names()


# ── StrategyRuleTuningInput ───────────────────────────────────────────────────

def test_tuning_input_paper_only():
    assert StrategyRuleTuningInput().paper_only is True

def test_tuning_input_research_only():
    assert StrategyRuleTuningInput().research_only is True

def test_tuning_input_tuning_only():
    assert StrategyRuleTuningInput().tuning_only is True

def test_tuning_input_guardrail_only():
    assert StrategyRuleTuningInput().guardrail_only is True

def test_tuning_input_no_real_orders():
    assert StrategyRuleTuningInput().no_real_orders is True

def test_tuning_input_no_broker():
    assert StrategyRuleTuningInput().no_broker is True

def test_tuning_input_no_production_mutation():
    assert StrategyRuleTuningInput().no_production_strategy_mutation is True

def test_tuning_input_not_investment_advice():
    assert StrategyRuleTuningInput().not_investment_advice is True

def test_tuning_input_schema_version():
    assert StrategyRuleTuningInput().schema_version == "191"

def test_tuning_input_production_blocked():
    assert StrategyRuleTuningInput().production_trading_blocked is True


# ── StrategyRuleTuningResult ──────────────────────────────────────────────────

def test_tuning_result_paper_only():
    assert StrategyRuleTuningResult().paper_only is True

def test_tuning_result_no_real_orders():
    assert StrategyRuleTuningResult().no_real_orders is True

def test_tuning_result_tuning_only():
    assert StrategyRuleTuningResult().tuning_only is True

def test_tuning_result_no_production_mutation():
    assert StrategyRuleTuningResult().no_production_strategy_mutation is True

def test_tuning_result_default_approval_state():
    assert StrategyRuleTuningResult().approval_state == "PROPOSED"

def test_tuning_result_schema_191():
    assert StrategyRuleTuningResult().schema_version == "191"


# ── StrategyRuleCandidate ─────────────────────────────────────────────────────

def test_rule_candidate_paper_only():
    assert StrategyRuleCandidate().paper_only is True

def test_rule_candidate_tuning_only():
    assert StrategyRuleCandidate().tuning_only is True

def test_rule_candidate_no_production_mutation():
    assert StrategyRuleCandidate().no_production_strategy_mutation is True

def test_rule_candidate_default_category():
    assert StrategyRuleCandidate().rule_category == "ABC_BUY_POINT"

def test_rule_candidate_default_recommendation():
    assert StrategyRuleCandidate().recommendation == "NO_CHANGE"

def test_rule_candidate_schema_191():
    assert StrategyRuleCandidate().schema_version == "191"


# ── StrategyRuleAdjustment ────────────────────────────────────────────────────

def test_rule_adjustment_paper_only():
    assert StrategyRuleAdjustment().paper_only is True

def test_rule_adjustment_guardrail_only():
    assert StrategyRuleAdjustment().guardrail_only is True

def test_rule_adjustment_no_production_mutation():
    assert StrategyRuleAdjustment().no_production_strategy_mutation is True

def test_rule_adjustment_review_only():
    assert StrategyRuleAdjustment().review_only is True

def test_rule_adjustment_default_state():
    assert StrategyRuleAdjustment().approval_state == "PROPOSED"

def test_rule_adjustment_schema_191():
    assert StrategyRuleAdjustment().schema_version == "191"


# ── StrategyGuardrail ─────────────────────────────────────────────────────────

def test_guardrail_paper_only():
    assert StrategyGuardrail().paper_only is True

def test_guardrail_guardrail_only():
    assert StrategyGuardrail().guardrail_only is True

def test_guardrail_no_production_mutation():
    assert StrategyGuardrail().no_production_strategy_mutation is True

def test_guardrail_production_blocked():
    assert StrategyGuardrail().production_trading_blocked is True

def test_guardrail_default_trigger():
    assert StrategyGuardrail().trigger == "EXPECTANCY_NEGATIVE"

def test_guardrail_schema_191():
    assert StrategyGuardrail().schema_version == "191"


# ── GuardrailTrigger ──────────────────────────────────────────────────────────

def test_guardrail_trigger_paper_only():
    assert GuardrailTrigger().paper_only is True

def test_guardrail_trigger_guardrail_only():
    assert GuardrailTrigger().guardrail_only is True

def test_guardrail_trigger_no_broker():
    assert GuardrailTrigger().no_broker is True

def test_guardrail_trigger_no_production_mutation():
    assert GuardrailTrigger().no_production_strategy_mutation is True

def test_guardrail_trigger_default_type():
    assert GuardrailTrigger().trigger_type == "EXPECTANCY_NEGATIVE"

def test_guardrail_trigger_schema_191():
    assert GuardrailTrigger().schema_version == "191"


# ── GuardrailSeverity ─────────────────────────────────────────────────────────

def test_guardrail_severity_paper_only():
    assert GuardrailSeverity().paper_only is True

def test_guardrail_severity_no_broker():
    assert GuardrailSeverity().no_broker is True

def test_guardrail_severity_not_investment_advice():
    assert GuardrailSeverity().not_investment_advice is True

def test_guardrail_severity_default_level():
    assert GuardrailSeverity().severity_level == "WARNING"

def test_guardrail_severity_schema_191():
    assert GuardrailSeverity().schema_version == "191"


# ── GuardrailAction ───────────────────────────────────────────────────────────

def test_guardrail_action_paper_only():
    assert GuardrailAction().paper_only is True

def test_guardrail_action_not_investment_advice():
    assert GuardrailAction().not_investment_advice is True

def test_guardrail_action_no_real_orders():
    assert GuardrailAction().no_real_orders is True

def test_guardrail_action_default_type():
    assert GuardrailAction().action_type == "LOG_ONLY"

def test_guardrail_action_schema_191():
    assert GuardrailAction().schema_version == "191"


# ── RuleTuningEvidence ────────────────────────────────────────────────────────

def test_evidence_paper_only():
    assert RuleTuningEvidence().paper_only is True

def test_evidence_production_blocked():
    assert RuleTuningEvidence().production_trading_blocked is True

def test_evidence_no_production_mutation():
    assert RuleTuningEvidence().no_production_strategy_mutation is True

def test_evidence_schema_191():
    assert RuleTuningEvidence().schema_version == "191"


# ── RuleTuningFinding ─────────────────────────────────────────────────────────

def test_finding_paper_only():
    assert RuleTuningFinding().paper_only is True

def test_finding_demo_only():
    assert RuleTuningFinding().demo_only is True

def test_finding_default_category():
    assert RuleTuningFinding().rule_category == "ABC_BUY_POINT"

def test_finding_default_recommendation():
    assert RuleTuningFinding().recommendation == "NO_CHANGE"

def test_finding_schema_191():
    assert RuleTuningFinding().schema_version == "191"


# ── RuleTuningRecommendation ──────────────────────────────────────────────────

def test_recommendation_paper_only():
    assert RuleTuningRecommendation().paper_only is True

def test_recommendation_not_for_production():
    assert RuleTuningRecommendation().not_for_production is True

def test_recommendation_no_production_mutation():
    assert RuleTuningRecommendation().no_production_strategy_mutation is True

def test_recommendation_default_type():
    assert RuleTuningRecommendation().recommendation_type == "NO_CHANGE"

def test_recommendation_default_state():
    assert RuleTuningRecommendation().approval_state == "PROPOSED"

def test_recommendation_schema_191():
    assert RuleTuningRecommendation().schema_version == "191"


# ── RuleTuningBacktestSnapshot ────────────────────────────────────────────────

def test_backtest_snapshot_paper_only():
    assert RuleTuningBacktestSnapshot().paper_only is True

def test_backtest_snapshot_no_margin():
    assert RuleTuningBacktestSnapshot().no_margin is True

def test_backtest_snapshot_simulate_only():
    assert RuleTuningBacktestSnapshot().simulate_only is True

def test_backtest_snapshot_schema_191():
    assert RuleTuningBacktestSnapshot().schema_version == "191"


# ── RuleTuningReviewChecklist ─────────────────────────────────────────────────

def test_review_checklist_paper_only():
    assert RuleTuningReviewChecklist().paper_only is True

def test_review_checklist_no_leverage():
    assert RuleTuningReviewChecklist().no_leverage is True

def test_review_checklist_schema_191():
    assert RuleTuningReviewChecklist().schema_version == "191"


# ── RuleTuningApprovalState ───────────────────────────────────────────────────

def test_approval_state_paper_only():
    assert RuleTuningApprovalState().paper_only is True

def test_approval_state_simulate_only():
    assert RuleTuningApprovalState().simulate_only is True

def test_approval_state_auto_approve_blocked():
    assert RuleTuningApprovalState().auto_approve_blocked is True

def test_approval_state_requires_manual_review():
    assert RuleTuningApprovalState().requires_manual_review is True

def test_approval_state_default_state():
    assert RuleTuningApprovalState().state == "PROPOSED"

def test_approval_state_schema_191():
    assert RuleTuningApprovalState().schema_version == "191"


# ── RuleTuningExportManifest ──────────────────────────────────────────────────

def test_export_manifest_paper_only():
    assert RuleTuningExportManifest().paper_only is True

def test_export_manifest_report_only():
    assert RuleTuningExportManifest().report_only is True

def test_export_manifest_safe_path_default():
    assert RuleTuningExportManifest().safe_path is True

def test_export_manifest_default_path():
    assert RuleTuningExportManifest().export_path == "reports/"

def test_export_manifest_schema_191():
    assert RuleTuningExportManifest().schema_version == "191"


# ── RuleTuningEvidencePack ────────────────────────────────────────────────────

def test_evidence_pack_paper_only():
    assert RuleTuningEvidencePack().paper_only is True

def test_evidence_pack_audit_only():
    assert RuleTuningEvidencePack().audit_only is True

def test_evidence_pack_no_production_mutation():
    assert RuleTuningEvidencePack().no_production_strategy_mutation is True

def test_evidence_pack_schema_191():
    assert RuleTuningEvidencePack().schema_version == "191"


# ── RuleTuningAuditTrail ──────────────────────────────────────────────────────

def test_audit_trail_paper_only():
    assert RuleTuningAuditTrail().paper_only is True

def test_audit_trail_audit_only():
    assert RuleTuningAuditTrail().audit_only is True

def test_audit_trail_review_only():
    assert RuleTuningAuditTrail().review_only is True

def test_audit_trail_timestamp_policy():
    assert "date_label" in RuleTuningAuditTrail().deterministic_timestamp_policy

def test_audit_trail_schema_191():
    assert RuleTuningAuditTrail().schema_version == "191"


# ── RuleTuningDashboard ───────────────────────────────────────────────────────

def test_dashboard_paper_only():
    assert RuleTuningDashboard().paper_only is True

def test_dashboard_review_only():
    assert RuleTuningDashboard().review_only is True

def test_dashboard_validation_only():
    assert RuleTuningDashboard().validation_only is True

def test_dashboard_no_production_mutation():
    assert RuleTuningDashboard().no_production_strategy_mutation is True

def test_dashboard_default_approval_state():
    assert RuleTuningDashboard().overall_approval_state == "PROPOSED"

def test_dashboard_schema_191():
    assert RuleTuningDashboard().schema_version == "191"


# ── RuleTuningHealthSummary ───────────────────────────────────────────────────

def test_health_summary_paper_only():
    assert RuleTuningHealthSummary().paper_only is True

def test_health_summary_research_only():
    assert RuleTuningHealthSummary().research_only is True

def test_health_summary_default_status():
    assert RuleTuningHealthSummary().status == "PASS"

def test_health_summary_schema_191():
    assert RuleTuningHealthSummary().schema_version == "191"


# ── RuleTuningValidationResult ────────────────────────────────────────────────

def test_validation_result_paper_only():
    assert RuleTuningValidationResult().paper_only is True

def test_validation_result_tuning_only():
    assert RuleTuningValidationResult().tuning_only is True

def test_validation_result_production_blocked():
    assert RuleTuningValidationResult().production_trading_blocked is True

def test_validation_result_schema_191():
    assert RuleTuningValidationResult().schema_version == "191"
