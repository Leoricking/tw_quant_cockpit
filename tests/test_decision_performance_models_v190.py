"""tests/test_decision_performance_models_v190.py
Tests for decision performance models v1.9.0.
[!] Research Only. Paper Only.
"""
import pytest
from paper_trading.small_capital_strategy.decision_performance_models_v190 import (
    PerformanceReviewInput,
    PerformanceReviewResult,
    StrategyPerformanceSummary,
    SetupPerformanceSummary,
    ActionPerformanceSummary,
    MistakePerformanceSummary,
    RMultipleSummary,
    DrawdownReviewSummary,
    WinLossSummary,
    ExpectancySummary,
    RiskRewardSummary,
    StrategyRuleFinding,
    StrategyImprovementSuggestion,
    StrategyAdjustmentPlan,
    PerformanceReviewDashboard,
    PerformanceReviewExportManifest,
    PerformanceReviewEvidencePack,
    PerformanceReviewAuditTrail,
    PerformanceHealthSummary,
    PerformanceValidationResult,
    get_all_model_names,
)


def test_get_all_model_names_length():
    assert len(get_all_model_names()) == 20


def test_all_model_names_are_strings():
    assert all(isinstance(n, str) for n in get_all_model_names())


def test_model_names_contains_performance_review_input():
    assert "PerformanceReviewInput" in get_all_model_names()


def test_model_names_contains_performance_review_result():
    assert "PerformanceReviewResult" in get_all_model_names()


def test_model_names_contains_performance_health_summary():
    assert "PerformanceHealthSummary" in get_all_model_names()


def test_performance_review_input_paper_only():
    assert PerformanceReviewInput().paper_only is True


def test_performance_review_input_no_real_orders():
    assert PerformanceReviewInput().no_real_orders is True


def test_performance_review_input_performance_review_only():
    assert PerformanceReviewInput().performance_review_only is True


def test_performance_review_input_strategy_improvement_only():
    assert PerformanceReviewInput().strategy_improvement_only is True


def test_performance_review_input_schema_version():
    assert PerformanceReviewInput().schema_version == "190"


def test_performance_review_result_no_real_orders():
    assert PerformanceReviewResult().no_real_orders is True


def test_performance_review_result_paper_only():
    assert PerformanceReviewResult().paper_only is True


def test_performance_review_result_performance_review_only():
    assert PerformanceReviewResult().performance_review_only is True


def test_strategy_performance_summary_performance_review_only():
    assert StrategyPerformanceSummary().performance_review_only is True


def test_strategy_performance_summary_paper_only():
    assert StrategyPerformanceSummary().paper_only is True


def test_setup_performance_summary_schema_version():
    assert SetupPerformanceSummary().schema_version == "190"


def test_setup_performance_summary_paper_only():
    assert SetupPerformanceSummary().paper_only is True


def test_action_performance_summary_not_investment_advice():
    assert ActionPerformanceSummary().not_investment_advice is True


def test_action_performance_summary_paper_only():
    assert ActionPerformanceSummary().paper_only is True


def test_mistake_performance_summary_audit_only():
    assert MistakePerformanceSummary().audit_only is True


def test_mistake_performance_summary_paper_only():
    assert MistakePerformanceSummary().paper_only is True


def test_r_multiple_summary_no_broker():
    assert RMultipleSummary().no_broker is True


def test_r_multiple_summary_paper_only():
    assert RMultipleSummary().paper_only is True


def test_r_multiple_summary_performance_review_only():
    assert RMultipleSummary().performance_review_only is True


def test_drawdown_review_summary_production_trading_blocked():
    assert DrawdownReviewSummary().production_trading_blocked is True


def test_drawdown_review_summary_paper_only():
    assert DrawdownReviewSummary().paper_only is True


def test_win_loss_summary_strategy_improvement_only():
    assert WinLossSummary().strategy_improvement_only is True


def test_win_loss_summary_paper_only():
    assert WinLossSummary().paper_only is True


def test_expectancy_summary_review_only():
    assert ExpectancySummary().review_only is True


def test_expectancy_summary_paper_only():
    assert ExpectancySummary().paper_only is True


def test_risk_reward_summary_report_only():
    assert RiskRewardSummary().report_only is True


def test_risk_reward_summary_paper_only():
    assert RiskRewardSummary().paper_only is True


def test_strategy_rule_finding_demo_only():
    assert StrategyRuleFinding().demo_only is True


def test_strategy_rule_finding_paper_only():
    assert StrategyRuleFinding().paper_only is True


def test_strategy_improvement_suggestion_not_for_production():
    assert StrategyImprovementSuggestion().not_for_production is True


def test_strategy_improvement_suggestion_strategy_improvement_only():
    assert StrategyImprovementSuggestion().strategy_improvement_only is True


def test_strategy_adjustment_plan_no_leverage():
    assert StrategyAdjustmentPlan().no_leverage is True


def test_strategy_adjustment_plan_no_margin():
    assert StrategyAdjustmentPlan().no_margin is True


def test_performance_review_dashboard_no_leverage():
    assert PerformanceReviewDashboard().no_leverage is True


def test_performance_review_dashboard_paper_only():
    assert PerformanceReviewDashboard().paper_only is True


def test_performance_review_export_manifest_simulate_only():
    assert PerformanceReviewExportManifest().simulate_only is True


def test_performance_review_export_manifest_paper_only():
    assert PerformanceReviewExportManifest().paper_only is True


def test_performance_review_evidence_pack_validation_only():
    assert PerformanceReviewEvidencePack().validation_only is True


def test_performance_review_evidence_pack_paper_only():
    assert PerformanceReviewEvidencePack().paper_only is True


def test_performance_review_audit_trail_paper_only():
    assert PerformanceReviewAuditTrail().paper_only is True


def test_performance_review_audit_trail_audit_only():
    assert PerformanceReviewAuditTrail().audit_only is True


def test_performance_health_summary_research_only():
    assert PerformanceHealthSummary().research_only is True


def test_performance_health_summary_paper_only():
    assert PerformanceHealthSummary().paper_only is True


def test_performance_validation_result_performance_review_only():
    assert PerformanceValidationResult().performance_review_only is True


def test_performance_validation_result_paper_only():
    assert PerformanceValidationResult().paper_only is True


def test_performance_review_input_isinstance_object():
    assert isinstance(PerformanceReviewInput(), object)


def test_get_all_model_names_returns_list():
    assert isinstance(get_all_model_names(), list)


def test_performance_review_input_no_broker():
    assert PerformanceReviewInput().no_broker is True


def test_performance_review_input_not_investment_advice():
    assert PerformanceReviewInput().not_investment_advice is True


def test_performance_review_input_research_only():
    assert PerformanceReviewInput().research_only is True


def test_performance_review_input_production_trading_blocked():
    assert PerformanceReviewInput().production_trading_blocked is True


def test_performance_review_result_strategy_improvement_only():
    assert PerformanceReviewResult().strategy_improvement_only is True


def test_setup_performance_summary_performance_review_only():
    assert SetupPerformanceSummary().performance_review_only is True


def test_mistake_performance_summary_performance_review_only():
    assert MistakePerformanceSummary().performance_review_only is True


def test_r_multiple_summary_strategy_improvement_only():
    assert RMultipleSummary().strategy_improvement_only is True


def test_drawdown_review_summary_strategy_improvement_only():
    assert DrawdownReviewSummary().strategy_improvement_only is True


def test_win_loss_summary_performance_review_only():
    assert WinLossSummary().performance_review_only is True


def test_expectancy_summary_strategy_improvement_only():
    assert ExpectancySummary().strategy_improvement_only is True


def test_strategy_rule_finding_not_for_production():
    assert StrategyRuleFinding().not_for_production is True


def test_performance_review_dashboard_no_margin():
    assert PerformanceReviewDashboard().no_margin is True


def test_performance_review_evidence_pack_performance_review_only():
    assert PerformanceReviewEvidencePack().performance_review_only is True


def test_performance_review_audit_trail_no_real_orders():
    assert PerformanceReviewAuditTrail().no_real_orders is True


def test_performance_health_summary_no_real_orders():
    assert PerformanceHealthSummary().no_real_orders is True


def test_performance_validation_result_no_real_orders():
    assert PerformanceValidationResult().no_real_orders is True


def test_get_all_model_names_length_gte_18():
    assert len(get_all_model_names()) >= 18
