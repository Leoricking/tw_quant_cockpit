"""tests/test_strategy_promotion_models_v193.py — v1.9.3 model tests."""
import pytest
from paper_trading.small_capital_strategy.strategy_promotion_models_v193 import (
    StrategyPromotionInput, StrategyPromotionResult, PromotionPackage,
    PromotionCandidateRule, PromotionEvidenceLink, PromotionValidationSummary,
    PromotionRiskSummary, PromotionImpactSummary, PromotionApprovalChecklist,
    PromotionApprovalState, RollbackPlan, RollbackTrigger, RollbackStep,
    RollbackValidationResult, PromotionBlockReason, PromotionFinding,
    PromotionRecommendation, PromotionExportManifest, PromotionEvidencePack,
    PromotionAuditTrail, PromotionDashboard, PromotionHealthSummary,
    get_all_model_names,
)


# ── StrategyPromotionInput ────────────────────────────────────────────────────
def test_promotion_input_paper_only(): assert StrategyPromotionInput().paper_only is True
def test_promotion_input_research_only(): assert StrategyPromotionInput().research_only is True
def test_promotion_input_promote_package_only(): assert StrategyPromotionInput().promotion_package_only is True
def test_promotion_input_rollback_plan_only(): assert StrategyPromotionInput().rollback_plan_only is True
def test_promotion_input_no_real_orders(): assert StrategyPromotionInput().no_real_orders is True
def test_promotion_input_no_broker(): assert StrategyPromotionInput().no_broker is True
def test_promotion_input_no_margin(): assert StrategyPromotionInput().no_margin is True
def test_promotion_input_no_leverage(): assert StrategyPromotionInput().no_leverage is True
def test_promotion_input_no_production_mutation(): assert StrategyPromotionInput().no_production_strategy_mutation is True
def test_promotion_input_no_live_activation(): assert StrategyPromotionInput().no_live_strategy_activation is True
def test_promotion_input_not_investment_advice(): assert StrategyPromotionInput().not_investment_advice is True
def test_promotion_input_demo_only(): assert StrategyPromotionInput().demo_only is True
def test_promotion_input_not_for_production(): assert StrategyPromotionInput().not_for_production is True
def test_promotion_input_production_blocked(): assert StrategyPromotionInput().production_trading_blocked is True
def test_promotion_input_schema_193(): assert StrategyPromotionInput().schema_version == "193"
def test_promotion_input_default_promotion_id(): assert StrategyPromotionInput().promotion_id == ""

# ── StrategyPromotionResult ───────────────────────────────────────────────────
def test_promotion_result_paper_only(): assert StrategyPromotionResult().paper_only is True
def test_promotion_result_no_real_orders(): assert StrategyPromotionResult().no_real_orders is True
def test_promotion_result_promotion_package_only(): assert StrategyPromotionResult().promotion_package_only is True
def test_promotion_result_default_approval_state(): assert StrategyPromotionResult().approval_state == "DRAFT"
def test_promotion_result_default_blocked_false(): assert StrategyPromotionResult().blocked is False
def test_promotion_result_schema_193(): assert StrategyPromotionResult().schema_version == "193"

# ── PromotionPackage ──────────────────────────────────────────────────────────
def test_promotion_package_paper_only(): assert PromotionPackage().paper_only is True
def test_promotion_package_promotion_package_only(): assert PromotionPackage().promotion_package_only is True
def test_promotion_package_rollback_plan_only(): assert PromotionPackage().rollback_plan_only is True
def test_promotion_package_no_broker(): assert PromotionPackage().no_broker is True
def test_promotion_package_default_approval_state(): assert PromotionPackage().approval_state == "DRAFT"
def test_promotion_package_schema_193(): assert PromotionPackage().schema_version == "193"

# ── PromotionCandidateRule ────────────────────────────────────────────────────
def test_candidate_rule_paper_only(): assert PromotionCandidateRule().paper_only is True
def test_candidate_rule_rollback_plan_only(): assert PromotionCandidateRule().rollback_plan_only is True
def test_candidate_rule_default_approval_state(): assert PromotionCandidateRule().approval_state == "DRAFT"
def test_candidate_rule_schema_193(): assert PromotionCandidateRule().schema_version == "193"

# ── PromotionEvidenceLink ─────────────────────────────────────────────────────
def test_evidence_link_paper_only(): assert PromotionEvidenceLink().paper_only is True
def test_evidence_link_no_broker(): assert PromotionEvidenceLink().no_broker is True
def test_evidence_link_schema_193(): assert PromotionEvidenceLink().schema_version == "193"

# ── PromotionValidationSummary ────────────────────────────────────────────────
def test_validation_summary_paper_only(): assert PromotionValidationSummary().paper_only is True
def test_validation_summary_no_margin(): assert PromotionValidationSummary().no_margin is True
def test_validation_summary_default_passed_false(): assert PromotionValidationSummary().sandbox_validation_passed is False
def test_validation_summary_schema_193(): assert PromotionValidationSummary().schema_version == "193"

# ── PromotionRiskSummary ──────────────────────────────────────────────────────
def test_risk_summary_paper_only(): assert PromotionRiskSummary().paper_only is True
def test_risk_summary_no_leverage(): assert PromotionRiskSummary().no_leverage is True
def test_risk_summary_schema_193(): assert PromotionRiskSummary().schema_version == "193"

# ── PromotionImpactSummary ────────────────────────────────────────────────────
def test_impact_summary_paper_only(): assert PromotionImpactSummary().paper_only is True
def test_impact_summary_not_investment_advice(): assert PromotionImpactSummary().not_investment_advice is True
def test_impact_summary_schema_193(): assert PromotionImpactSummary().schema_version == "193"

# ── PromotionApprovalChecklist ────────────────────────────────────────────────
def test_approval_checklist_paper_only(): assert PromotionApprovalChecklist().paper_only is True
def test_approval_checklist_demo_only(): assert PromotionApprovalChecklist().demo_only is True
def test_approval_checklist_default_false(): assert PromotionApprovalChecklist().all_items_checked is False
def test_approval_checklist_schema_193(): assert PromotionApprovalChecklist().schema_version == "193"

# ── PromotionApprovalState ────────────────────────────────────────────────────
def test_approval_state_paper_only(): assert PromotionApprovalState().paper_only is True
def test_approval_state_not_for_production(): assert PromotionApprovalState().not_for_production is True
def test_approval_state_requires_manual_review(): assert PromotionApprovalState().requires_manual_review is True
def test_approval_state_auto_approve_blocked(): assert PromotionApprovalState().auto_approve_blocked is True
def test_approval_state_schema_193(): assert PromotionApprovalState().schema_version == "193"

# ── RollbackPlan ──────────────────────────────────────────────────────────────
def test_rollback_plan_paper_only(): assert RollbackPlan().paper_only is True
def test_rollback_plan_rollback_plan_only(): assert RollbackPlan().rollback_plan_only is True
def test_rollback_plan_production_blocked(): assert RollbackPlan().production_trading_blocked is True
def test_rollback_plan_default_checklist_false(): assert RollbackPlan().rollback_checklist_complete is False
def test_rollback_plan_schema_193(): assert RollbackPlan().schema_version == "193"

# ── RollbackTrigger ───────────────────────────────────────────────────────────
def test_rollback_trigger_paper_only(): assert RollbackTrigger().paper_only is True
def test_rollback_trigger_no_real_orders(): assert RollbackTrigger().no_real_orders is True
def test_rollback_trigger_auto_rollback_blocked(): assert RollbackTrigger().auto_rollback_blocked is True
def test_rollback_trigger_schema_193(): assert RollbackTrigger().schema_version == "193"

# ── RollbackStep ──────────────────────────────────────────────────────────────
def test_rollback_step_paper_only(): assert RollbackStep().paper_only is True
def test_rollback_step_rollback_plan_only(): assert RollbackStep().rollback_plan_only is True
def test_rollback_step_schema_193(): assert RollbackStep().schema_version == "193"

# ── RollbackValidationResult ──────────────────────────────────────────────────
def test_rollback_validation_paper_only(): assert RollbackValidationResult().paper_only is True
def test_rollback_validation_research_only(): assert RollbackValidationResult().research_only is True
def test_rollback_validation_default_invalid(): assert RollbackValidationResult().valid is False
def test_rollback_validation_schema_193(): assert RollbackValidationResult().schema_version == "193"

# ── PromotionBlockReason ──────────────────────────────────────────────────────
def test_block_reason_paper_only(): assert PromotionBlockReason().paper_only is True
def test_block_reason_simulate_only(): assert PromotionBlockReason().simulate_only is True
def test_block_reason_default_hard_block(): assert PromotionBlockReason().severity == "HARD_BLOCK"
def test_block_reason_schema_193(): assert PromotionBlockReason().schema_version == "193"

# ── PromotionFinding ──────────────────────────────────────────────────────────
def test_finding_paper_only(): assert PromotionFinding().paper_only is True
def test_finding_validation_only(): assert PromotionFinding().validation_only is True
def test_finding_schema_193(): assert PromotionFinding().schema_version == "193"

# ── PromotionRecommendation ───────────────────────────────────────────────────
def test_recommendation_paper_only(): assert PromotionRecommendation().paper_only is True
def test_recommendation_review_only(): assert PromotionRecommendation().review_only is True
def test_recommendation_default_no_change(): assert PromotionRecommendation().recommendation_type == "NO_CHANGE"
def test_recommendation_schema_193(): assert PromotionRecommendation().schema_version == "193"

# ── PromotionExportManifest ───────────────────────────────────────────────────
def test_export_manifest_paper_only(): assert PromotionExportManifest().paper_only is True
def test_export_manifest_report_only(): assert PromotionExportManifest().report_only is True
def test_export_manifest_default_path(): assert PromotionExportManifest().export_path == "reports/"
def test_export_manifest_schema_193(): assert PromotionExportManifest().schema_version == "193"

# ── PromotionEvidencePack ─────────────────────────────────────────────────────
def test_evidence_pack_paper_only(): assert PromotionEvidencePack().paper_only is True
def test_evidence_pack_audit_only(): assert PromotionEvidencePack().audit_only is True
def test_evidence_pack_default_empty(): assert PromotionEvidencePack().evidence_count == 0
def test_evidence_pack_schema_193(): assert PromotionEvidencePack().schema_version == "193"

# ── PromotionAuditTrail ───────────────────────────────────────────────────────
def test_audit_trail_paper_only(): assert PromotionAuditTrail().paper_only is True
def test_audit_trail_promotion_package_only(): assert PromotionAuditTrail().promotion_package_only is True
def test_audit_trail_deterministic_ts(): assert PromotionAuditTrail().deterministic_timestamp_policy == "date_label_only_no_wall_clock"
def test_audit_trail_schema_193(): assert PromotionAuditTrail().schema_version == "193"

# ── PromotionDashboard ────────────────────────────────────────────────────────
def test_dashboard_paper_only(): assert PromotionDashboard().paper_only is True
def test_dashboard_rollback_plan_only(): assert PromotionDashboard().rollback_plan_only is True
def test_dashboard_default_state(): assert PromotionDashboard().approval_state == "DRAFT"
def test_dashboard_schema_193(): assert PromotionDashboard().schema_version == "193"

# ── PromotionHealthSummary ────────────────────────────────────────────────────
def test_health_summary_paper_only(): assert PromotionHealthSummary().paper_only is True
def test_health_summary_no_production_mutation(): assert PromotionHealthSummary().no_production_strategy_mutation is True
def test_health_summary_schema_193(): assert PromotionHealthSummary().schema_version == "193"

# ── get_all_model_names ───────────────────────────────────────────────────────
def test_model_names_count(): assert len(get_all_model_names()) == 22
def test_model_names_has_promotion_input(): assert "StrategyPromotionInput" in get_all_model_names()
def test_model_names_has_rollback_plan(): assert "RollbackPlan" in get_all_model_names()
def test_model_names_has_promotion_health(): assert "PromotionHealthSummary" in get_all_model_names()
def test_model_names_returns_list(): assert isinstance(get_all_model_names(), list)
