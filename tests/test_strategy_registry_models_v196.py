"""
tests/test_strategy_registry_models_v196.py
Tests for strategy_registry_models_v196 — Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_registry_models_v196 import (
    StrategyDecisionId,
    StrategyDecisionSource,
    StrategyDecisionType,
    StrategyDecisionState,
    StrategyDecisionOwner,
    StrategyDecisionRationale,
    StrategyDecisionEvidenceLink,
    StrategyDecisionEvidencePack,
    StrategyDecisionLineage,
    StrategyDecisionGovernancePolicy,
    StrategyDecisionGovernanceResult,
    StrategyDecisionChecklist,
    StrategyDecisionViolation,
    StrategyDecisionRiskSummary,
    StrategyDecisionImpactSummary,
    StrategyDecisionExportManifest,
    StrategyDecisionAuditTrail,
    StrategyDecisionDashboard,
    StrategyDecisionQueue,
    StrategyDecisionQueueSummary,
    StrategyDecisionHealthSummary,
    StrategyDecisionValidationResult,
    StrategyDecisionRetentionPolicy,
    StrategyDecisionRecord,
    StrategyDecisionRegistryInput,
    StrategyDecisionRegistryResult,
    get_all_model_names,
)


# ── model count ───────────────────────────────────────────────────────────────

def test_model_count_26():
    assert len(get_all_model_names()) == 26

def test_model_names_is_list():
    assert isinstance(get_all_model_names(), list)

def test_model_names_contains_decision_record():
    assert "StrategyDecisionRecord" in get_all_model_names()


# ── StrategyDecisionRecord ────────────────────────────────────────────────────

def test_decision_record_paper_only():
    assert StrategyDecisionRecord().paper_only is True

def test_decision_record_no_real_orders():
    assert StrategyDecisionRecord().no_real_orders is True

def test_decision_record_no_broker():
    assert StrategyDecisionRecord().no_broker is True

def test_decision_record_immutable():
    assert StrategyDecisionRecord().immutable is True

def test_decision_record_governance_only():
    assert StrategyDecisionRecord().governance_only is True

def test_decision_record_registry_only():
    assert StrategyDecisionRecord().registry_only is True

def test_decision_record_not_investment_advice():
    assert StrategyDecisionRecord().not_investment_advice is True

def test_decision_record_no_auto_approval():
    assert StrategyDecisionRecord().auto_approval is False

def test_decision_record_schema_version():
    assert StrategyDecisionRecord().schema_version == "196"


# ── StrategyDecisionRegistryInput ────────────────────────────────────────────

def test_registry_input_paper_only():
    assert StrategyDecisionRegistryInput().paper_only is True

def test_registry_input_no_real_orders():
    assert StrategyDecisionRegistryInput().no_real_orders is True

def test_registry_input_schema_version():
    assert StrategyDecisionRegistryInput().schema_version == "196"


# ── StrategyDecisionRegistryResult ───────────────────────────────────────────

def test_registry_result_paper_only():
    assert StrategyDecisionRegistryResult().paper_only is True

def test_registry_result_no_real_orders():
    assert StrategyDecisionRegistryResult().no_real_orders is True

def test_registry_result_governance_only():
    assert StrategyDecisionRegistryResult().governance_only is True


# ── StrategyDecisionQueue ─────────────────────────────────────────────────────

def test_decision_queue_auto_processing_false():
    assert StrategyDecisionQueue().auto_processing is False

def test_decision_queue_requires_human_review():
    assert StrategyDecisionQueue().requires_human_review is True


# ── StrategyDecisionHealthSummary ─────────────────────────────────────────────

def test_health_summary_schema_version():
    assert StrategyDecisionHealthSummary().schema_version == "196"


# ── StrategyDecisionRetentionPolicy ──────────────────────────────────────────

def test_retention_policy_no_auto_deletion():
    assert StrategyDecisionRetentionPolicy().auto_deletion is False


# ── StrategyDecisionGovernanceResult ─────────────────────────────────────────

def test_governance_result_paper_only():
    assert StrategyDecisionGovernanceResult().paper_only is True


# ── StrategyDecisionAuditTrail ────────────────────────────────────────────────

def test_audit_trail_paper_only():
    assert StrategyDecisionAuditTrail().paper_only is True

def test_audit_trail_immutable():
    assert StrategyDecisionAuditTrail().immutable is True


# ── StrategyDecisionEvidencePack ─────────────────────────────────────────────

def test_evidence_pack_paper_only():
    assert StrategyDecisionEvidencePack().paper_only is True


# ── StrategyDecisionLineage ───────────────────────────────────────────────────

def test_lineage_paper_only():
    assert StrategyDecisionLineage().paper_only is True


# ── StrategyDecisionDashboard ─────────────────────────────────────────────────

def test_dashboard_paper_only():
    assert StrategyDecisionDashboard().paper_only is True

def test_dashboard_not_investment_advice():
    assert StrategyDecisionDashboard().not_investment_advice is True


# ── StrategyDecisionGovernancePolicy ─────────────────────────────────────────

def test_governance_policy_paper_only():
    assert StrategyDecisionGovernancePolicy().paper_only is True


# ── StrategyDecisionChecklist ─────────────────────────────────────────────────

def test_checklist_paper_only():
    assert StrategyDecisionChecklist().paper_only is True


# ── StrategyDecisionViolation ─────────────────────────────────────────────────

def test_violation_paper_only():
    assert StrategyDecisionViolation().paper_only is True
