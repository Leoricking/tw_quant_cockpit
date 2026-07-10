"""
tests/test_integrated_strategy_models_v178.py
Tests for integrated_strategy_models_v178.py — v1.7.8 Small Capital Strategy Integration.
14 data models, paper/research only.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.

Safety invariants:
    paper_only=True, no_real_orders=True, no_broker=True, not_investment_advice=True
"""
import pytest
from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
    IntegratedStrategyInput,
    IntegratedStrategyContext,
    IntegratedStrategyDecision,
    IntegratedWatchlistDecision,
    IntegratedThemeDecision,
    IntegratedABCDecision,
    IntegratedRiskDecision,
    IntegratedBehaviorDecision,
    IntegratedPaperPlan,
    IntegratedNoTradeReason,
    IntegratedScorecard,
    IntegratedDashboard,
    IntegratedStrategyReport,
    IntegratedHealthSummary,
    get_all_model_names,
)
from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedDecisionAction,
    IntegratedNoTradeReasonCode,
    IntegratedScoreGrade,
    IntegratedBlockReason,
    IntegratedWatchlistStatus,
    IntegratedABCStatus,
    IntegratedThemeStatus,
    IntegratedRiskLevel,
    IntegratedBehaviorStatus,
)

# ---------------------------------------------------------------------------
# Safety invariants (module-level constants)
# ---------------------------------------------------------------------------
paper_only = True
no_real_orders = True
no_broker = True
not_investment_advice = True

_SCHEMA = "178"
_POLICY = "1.7.8-small-capital-strategy-integration"


# ---------------------------------------------------------------------------
# get_all_model_names
# ---------------------------------------------------------------------------

def test_get_all_model_names_returns_list():
    assert isinstance(get_all_model_names(), list)


def test_get_all_model_names_has_exactly_14_items():
    assert len(get_all_model_names()) == 14


def test_get_all_model_names_contains_integrated_strategy_input():
    assert "IntegratedStrategyInput" in get_all_model_names()


def test_get_all_model_names_contains_integrated_strategy_context():
    assert "IntegratedStrategyContext" in get_all_model_names()


def test_get_all_model_names_contains_integrated_strategy_decision():
    assert "IntegratedStrategyDecision" in get_all_model_names()


def test_get_all_model_names_contains_integrated_watchlist_decision():
    assert "IntegratedWatchlistDecision" in get_all_model_names()


def test_get_all_model_names_contains_integrated_theme_decision():
    assert "IntegratedThemeDecision" in get_all_model_names()


def test_get_all_model_names_contains_integrated_abc_decision():
    assert "IntegratedABCDecision" in get_all_model_names()


def test_get_all_model_names_contains_integrated_risk_decision():
    assert "IntegratedRiskDecision" in get_all_model_names()


def test_get_all_model_names_contains_integrated_behavior_decision():
    assert "IntegratedBehaviorDecision" in get_all_model_names()


def test_get_all_model_names_contains_integrated_paper_plan():
    assert "IntegratedPaperPlan" in get_all_model_names()


def test_get_all_model_names_contains_integrated_no_trade_reason():
    assert "IntegratedNoTradeReason" in get_all_model_names()


def test_get_all_model_names_contains_integrated_scorecard():
    assert "IntegratedScorecard" in get_all_model_names()


def test_get_all_model_names_contains_integrated_dashboard():
    assert "IntegratedDashboard" in get_all_model_names()


def test_get_all_model_names_contains_integrated_strategy_report():
    assert "IntegratedStrategyReport" in get_all_model_names()


def test_get_all_model_names_contains_integrated_health_summary():
    assert "IntegratedHealthSummary" in get_all_model_names()


# ---------------------------------------------------------------------------
# Model 1 — IntegratedStrategyInput
# ---------------------------------------------------------------------------

def test_strategy_input_default_paper_only_is_true():
    m = IntegratedStrategyInput()
    assert m.paper_only is True


def test_strategy_input_default_no_real_orders_is_true():
    m = IntegratedStrategyInput()
    assert m.no_real_orders is True


def test_strategy_input_default_no_broker_is_true():
    m = IntegratedStrategyInput()
    assert m.no_broker is True


def test_strategy_input_default_not_investment_advice_is_true():
    m = IntegratedStrategyInput()
    assert m.not_investment_advice is True


def test_strategy_input_default_demo_only_is_true():
    m = IntegratedStrategyInput()
    assert m.demo_only is True


def test_strategy_input_default_not_for_production_is_true():
    m = IntegratedStrategyInput()
    assert m.not_for_production is True


def test_strategy_input_source_lineage_is_set():
    m = IntegratedStrategyInput()
    assert m.source_lineage != ""
    assert "integrated_strategy_models_v178" in m.source_lineage


def test_strategy_input_default_real_order_requested_is_false():
    m = IntegratedStrategyInput()
    assert m.real_order_requested is False


def test_strategy_input_default_broker_requested_is_false():
    m = IntegratedStrategyInput()
    assert m.broker_requested is False


def test_strategy_input_default_margin_requested_is_false():
    m = IntegratedStrategyInput()
    assert m.margin_requested is False


def test_strategy_input_schema_version_is_178():
    m = IntegratedStrategyInput()
    assert m.schema_version == _SCHEMA


def test_strategy_input_policy_version_is_correct():
    m = IntegratedStrategyInput()
    assert m.policy_version == _POLICY


def test_strategy_input_symbol_can_be_overridden():
    m = IntegratedStrategyInput(symbol="AAPL")
    assert m.symbol == "AAPL"


def test_strategy_input_capital_twd_default():
    m = IntegratedStrategyInput()
    assert m.capital_twd == 300_000.0


def test_strategy_input_has_stop_loss_default_false():
    m = IntegratedStrategyInput()
    assert m.has_stop_loss is False


# ---------------------------------------------------------------------------
# Model 2 — IntegratedStrategyContext
# ---------------------------------------------------------------------------

def test_strategy_context_default_paper_only_is_true():
    m = IntegratedStrategyContext()
    assert m.paper_only is True


def test_strategy_context_block_reasons_is_empty_list_by_default():
    m = IntegratedStrategyContext()
    assert m.block_reasons == []


def test_strategy_context_block_reasons_is_list():
    m = IntegratedStrategyContext()
    assert isinstance(m.block_reasons, list)


def test_strategy_context_regime_allows_trade_default_false():
    m = IntegratedStrategyContext()
    assert m.regime_allows_trade is False


def test_strategy_context_schema_version_is_178():
    m = IntegratedStrategyContext()
    assert m.schema_version == _SCHEMA


def test_strategy_context_no_real_orders_is_true():
    m = IntegratedStrategyContext()
    assert m.no_real_orders is True


# ---------------------------------------------------------------------------
# Model 3 — IntegratedStrategyDecision
# ---------------------------------------------------------------------------

def test_strategy_decision_default_paper_only_is_true():
    m = IntegratedStrategyDecision()
    assert m.paper_only is True


def test_strategy_decision_default_no_real_orders_is_true():
    m = IntegratedStrategyDecision()
    assert m.no_real_orders is True


def test_strategy_decision_default_no_broker_is_true():
    m = IntegratedStrategyDecision()
    assert m.no_broker is True


def test_strategy_decision_default_action_is_observe():
    m = IntegratedStrategyDecision()
    assert m.action == IntegratedDecisionAction.OBSERVE


def test_strategy_decision_no_trade_reasons_is_empty_list_by_default():
    m = IntegratedStrategyDecision()
    assert m.no_trade_reasons == []


def test_strategy_decision_no_trade_reasons_is_list():
    m = IntegratedStrategyDecision()
    assert isinstance(m.no_trade_reasons, list)


def test_strategy_decision_block_reasons_is_empty_list_by_default():
    m = IntegratedStrategyDecision()
    assert m.block_reasons == []


def test_strategy_decision_schema_version_is_178():
    m = IntegratedStrategyDecision()
    assert m.schema_version == _SCHEMA


def test_strategy_decision_policy_version_is_correct():
    m = IntegratedStrategyDecision()
    assert m.policy_version == _POLICY


# ---------------------------------------------------------------------------
# Model 4 — IntegratedWatchlistDecision
# ---------------------------------------------------------------------------

def test_watchlist_decision_default_paper_only_is_true():
    m = IntegratedWatchlistDecision()
    assert m.paper_only is True


def test_watchlist_decision_default_status_is_unknown():
    m = IntegratedWatchlistDecision()
    assert m.status == IntegratedWatchlistStatus.UNKNOWN


def test_watchlist_decision_schema_version_is_178():
    m = IntegratedWatchlistDecision()
    assert m.schema_version == _SCHEMA


def test_watchlist_decision_no_real_orders_is_true():
    m = IntegratedWatchlistDecision()
    assert m.no_real_orders is True


# ---------------------------------------------------------------------------
# Model 5 — IntegratedThemeDecision
# ---------------------------------------------------------------------------

def test_theme_decision_default_paper_only_is_true():
    m = IntegratedThemeDecision()
    assert m.paper_only is True


def test_theme_decision_default_theme_status_is_unknown():
    m = IntegratedThemeDecision()
    assert m.theme_status == IntegratedThemeStatus.UNKNOWN


def test_theme_decision_schema_version_is_178():
    m = IntegratedThemeDecision()
    assert m.schema_version == _SCHEMA


def test_theme_decision_no_broker_is_true():
    m = IntegratedThemeDecision()
    assert m.no_broker is True


# ---------------------------------------------------------------------------
# Model 6 — IntegratedABCDecision
# ---------------------------------------------------------------------------

def test_abc_decision_default_paper_only_is_true():
    m = IntegratedABCDecision()
    assert m.paper_only is True


def test_abc_decision_default_abc_status_is_not_ready():
    m = IntegratedABCDecision()
    assert m.abc_status == IntegratedABCStatus.NOT_READY


def test_abc_decision_schema_version_is_178():
    m = IntegratedABCDecision()
    assert m.schema_version == _SCHEMA


def test_abc_decision_no_real_orders_is_true():
    m = IntegratedABCDecision()
    assert m.no_real_orders is True


# ---------------------------------------------------------------------------
# Model 7 — IntegratedRiskDecision
# ---------------------------------------------------------------------------

def test_risk_decision_default_paper_only_is_true():
    m = IntegratedRiskDecision()
    assert m.paper_only is True


def test_risk_decision_default_risk_level_is_safe():
    m = IntegratedRiskDecision()
    assert m.risk_level == IntegratedRiskLevel.SAFE


def test_risk_decision_schema_version_is_178():
    m = IntegratedRiskDecision()
    assert m.schema_version == _SCHEMA


def test_risk_decision_no_broker_is_true():
    m = IntegratedRiskDecision()
    assert m.no_broker is True


# ---------------------------------------------------------------------------
# Model 8 — IntegratedBehaviorDecision
# ---------------------------------------------------------------------------

def test_behavior_decision_default_paper_only_is_true():
    m = IntegratedBehaviorDecision()
    assert m.paper_only is True


def test_behavior_decision_default_behavior_status_is_clean():
    m = IntegratedBehaviorDecision()
    assert m.behavior_status == IntegratedBehaviorStatus.CLEAN


def test_behavior_decision_default_mistake_repeat_detected_is_false():
    m = IntegratedBehaviorDecision()
    assert m.mistake_repeat_detected is False


def test_behavior_decision_schema_version_is_178():
    m = IntegratedBehaviorDecision()
    assert m.schema_version == _SCHEMA


def test_behavior_decision_not_investment_advice_is_true():
    m = IntegratedBehaviorDecision()
    assert m.not_investment_advice is True


# ---------------------------------------------------------------------------
# Model 9 — IntegratedPaperPlan
# ---------------------------------------------------------------------------

def test_paper_plan_default_paper_only_is_true():
    m = IntegratedPaperPlan()
    assert m.paper_only is True


def test_paper_plan_default_no_real_orders_is_true():
    m = IntegratedPaperPlan()
    assert m.no_real_orders is True


def test_paper_plan_default_no_broker_is_true():
    m = IntegratedPaperPlan()
    assert m.no_broker is True


def test_paper_plan_broker_execution_enabled_is_false():
    m = IntegratedPaperPlan()
    assert m.broker_execution_enabled is False


def test_paper_plan_broker_execution_enabled_hardcoded_false():
    """broker_execution_enabled must be False even when instantiated explicitly."""
    m = IntegratedPaperPlan(broker_execution_enabled=False)
    assert m.broker_execution_enabled is False


def test_paper_plan_demo_only_is_true():
    m = IntegratedPaperPlan()
    assert m.demo_only is True


def test_paper_plan_not_for_production_is_true():
    m = IntegratedPaperPlan()
    assert m.not_for_production is True


def test_paper_plan_schema_version_is_178():
    m = IntegratedPaperPlan()
    assert m.schema_version == _SCHEMA


def test_paper_plan_policy_version_is_correct():
    m = IntegratedPaperPlan()
    assert m.policy_version == _POLICY


# ---------------------------------------------------------------------------
# Model 10 — IntegratedNoTradeReason
# ---------------------------------------------------------------------------

def test_no_trade_reason_default_paper_only_is_true():
    m = IntegratedNoTradeReason()
    assert m.paper_only is True


def test_no_trade_reason_default_code_is_data_incomplete():
    m = IntegratedNoTradeReason()
    assert m.code == IntegratedNoTradeReasonCode.DATA_INCOMPLETE


def test_no_trade_reason_schema_version_is_178():
    m = IntegratedNoTradeReason()
    assert m.schema_version == _SCHEMA


def test_no_trade_reason_no_real_orders_is_true():
    m = IntegratedNoTradeReason()
    assert m.no_real_orders is True


def test_no_trade_reason_code_can_be_set():
    m = IntegratedNoTradeReason(code=IntegratedNoTradeReasonCode.STOP_LOSS_MISSING)
    assert m.code == IntegratedNoTradeReasonCode.STOP_LOSS_MISSING


# ---------------------------------------------------------------------------
# Model 11 — IntegratedScorecard
# ---------------------------------------------------------------------------

def test_scorecard_default_paper_only_is_true():
    m = IntegratedScorecard()
    assert m.paper_only is True


def test_scorecard_default_theme_score_is_zero():
    m = IntegratedScorecard()
    assert m.theme_score == 0.0


def test_scorecard_default_watchlist_score_is_zero():
    m = IntegratedScorecard()
    assert m.watchlist_score == 0.0


def test_scorecard_default_abc_score_is_zero():
    m = IntegratedScorecard()
    assert m.abc_score == 0.0


def test_scorecard_default_regime_score_is_zero():
    m = IntegratedScorecard()
    assert m.regime_score == 0.0


def test_scorecard_default_risk_score_is_zero():
    m = IntegratedScorecard()
    assert m.risk_score == 0.0


def test_scorecard_default_behavior_score_is_zero():
    m = IntegratedScorecard()
    assert m.behavior_score == 0.0


def test_scorecard_default_final_score_is_zero():
    m = IntegratedScorecard()
    assert m.final_score == 0.0


def test_scorecard_default_grade_is_blocked():
    m = IntegratedScorecard()
    assert m.grade == IntegratedScoreGrade.BLOCKED


def test_scorecard_schema_version_is_178():
    m = IntegratedScorecard()
    assert m.schema_version == _SCHEMA


# ---------------------------------------------------------------------------
# Model 12 — IntegratedDashboard
# ---------------------------------------------------------------------------

def test_dashboard_default_paper_only_is_true():
    m = IntegratedDashboard()
    assert m.paper_only is True


def test_dashboard_default_no_real_orders_is_true():
    m = IntegratedDashboard()
    assert m.no_real_orders is True


def test_dashboard_default_no_broker_is_true():
    m = IntegratedDashboard()
    assert m.no_broker is True


def test_dashboard_sections_is_empty_list_by_default():
    m = IntegratedDashboard()
    assert m.sections == []


def test_dashboard_sections_is_list():
    m = IntegratedDashboard()
    assert isinstance(m.sections, list)


def test_dashboard_no_trade_reasons_is_empty_list_by_default():
    m = IntegratedDashboard()
    assert m.no_trade_reasons == []


def test_dashboard_no_trade_reasons_is_list():
    m = IntegratedDashboard()
    assert isinstance(m.no_trade_reasons, list)


def test_dashboard_schema_version_is_178():
    m = IntegratedDashboard()
    assert m.schema_version == _SCHEMA


def test_dashboard_demo_only_is_true():
    m = IntegratedDashboard()
    assert m.demo_only is True


def test_dashboard_not_for_production_is_true():
    m = IntegratedDashboard()
    assert m.not_for_production is True


def test_dashboard_sections_are_independent_between_instances():
    m1 = IntegratedDashboard()
    m2 = IntegratedDashboard()
    m1.sections.append({"key": "val"})
    assert m2.sections == []


# ---------------------------------------------------------------------------
# Model 13 — IntegratedStrategyReport
# ---------------------------------------------------------------------------

def test_strategy_report_default_paper_only_is_true():
    m = IntegratedStrategyReport()
    assert m.paper_only is True


def test_strategy_report_sections_is_empty_list_by_default():
    m = IntegratedStrategyReport()
    assert m.sections == []


def test_strategy_report_sections_is_list():
    m = IntegratedStrategyReport()
    assert isinstance(m.sections, list)


def test_strategy_report_default_action_is_observe():
    m = IntegratedStrategyReport()
    assert m.action == IntegratedDecisionAction.OBSERVE


def test_strategy_report_schema_version_is_178():
    m = IntegratedStrategyReport()
    assert m.schema_version == _SCHEMA


def test_strategy_report_no_real_orders_is_true():
    m = IntegratedStrategyReport()
    assert m.no_real_orders is True


def test_strategy_report_demo_only_is_true():
    m = IntegratedStrategyReport()
    assert m.demo_only is True


def test_strategy_report_not_for_production_is_true():
    m = IntegratedStrategyReport()
    assert m.not_for_production is True


# ---------------------------------------------------------------------------
# Model 14 — IntegratedHealthSummary
# ---------------------------------------------------------------------------

def test_health_summary_default_paper_only_is_true():
    m = IntegratedHealthSummary()
    assert m.paper_only is True


def test_health_summary_default_all_passed_is_true():
    m = IntegratedHealthSummary()
    assert m.all_passed is True


def test_health_summary_default_status_is_pass():
    m = IntegratedHealthSummary()
    assert m.status == "PASS"


def test_health_summary_schema_version_is_178():
    m = IntegratedHealthSummary()
    assert m.schema_version == _SCHEMA


def test_health_summary_no_real_orders_is_true():
    m = IntegratedHealthSummary()
    assert m.no_real_orders is True


def test_health_summary_not_investment_advice_is_true():
    m = IntegratedHealthSummary()
    assert m.not_investment_advice is True


# ---------------------------------------------------------------------------
# schema_version and policy_version on all models
# ---------------------------------------------------------------------------

def test_all_models_have_schema_version_178():
    models = [
        IntegratedStrategyInput(),
        IntegratedStrategyContext(),
        IntegratedStrategyDecision(),
        IntegratedWatchlistDecision(),
        IntegratedThemeDecision(),
        IntegratedABCDecision(),
        IntegratedRiskDecision(),
        IntegratedBehaviorDecision(),
        IntegratedPaperPlan(),
        IntegratedNoTradeReason(),
        IntegratedScorecard(),
        IntegratedDashboard(),
        IntegratedStrategyReport(),
        IntegratedHealthSummary(),
    ]
    for m in models:
        assert m.schema_version == _SCHEMA, f"{type(m).__name__} schema_version mismatch"


def test_all_models_have_correct_policy_version():
    models_with_policy = [
        IntegratedStrategyInput(),
        IntegratedStrategyContext(),
        IntegratedStrategyDecision(),
        IntegratedWatchlistDecision(),
        IntegratedThemeDecision(),
        IntegratedABCDecision(),
        IntegratedRiskDecision(),
        IntegratedBehaviorDecision(),
        IntegratedPaperPlan(),
        IntegratedNoTradeReason(),
        IntegratedScorecard(),
        IntegratedDashboard(),
        IntegratedStrategyReport(),
        IntegratedHealthSummary(),
    ]
    for m in models_with_policy:
        assert m.policy_version == _POLICY, f"{type(m).__name__} policy_version mismatch"


# ---------------------------------------------------------------------------
# Mutable default isolation checks
# ---------------------------------------------------------------------------

def test_strategy_decision_no_trade_reasons_lists_are_independent():
    m1 = IntegratedStrategyDecision()
    m2 = IntegratedStrategyDecision()
    m1.no_trade_reasons.append(IntegratedNoTradeReasonCode.STOP_LOSS_MISSING)
    assert m2.no_trade_reasons == []


def test_strategy_decision_block_reasons_lists_are_independent():
    m1 = IntegratedStrategyDecision()
    m2 = IntegratedStrategyDecision()
    m1.block_reasons.append(IntegratedBlockReason.NO_STOP_LOSS)
    assert m2.block_reasons == []


def test_strategy_context_block_reasons_lists_are_independent():
    m1 = IntegratedStrategyContext()
    m2 = IntegratedStrategyContext()
    m1.block_reasons.append(IntegratedBlockReason.LINEAGE_MISSING)
    assert m2.block_reasons == []


def test_strategy_input_override_symbol_and_date():
    m = IntegratedStrategyInput(symbol="TSMC", date="2026-07-10")
    assert m.symbol == "TSMC"
    assert m.date == "2026-07-10"
    assert m.paper_only is True
