"""
tests/test_position_sizing_models_v184.py
Tests for position_sizing_models_v184 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.position_sizing_models_v184 import (
    CapitalProfile, RiskBudget, PositionSizingInput, PositionSizingRule,
    PositionSizingResult, PortfolioAllocationInput, PortfolioAllocationResult,
    ScalingPlan, AddPositionPlan, ReducePositionPlan, StopLossBudget,
    DrawdownBudget, ConcentrationRiskReport, ExposureLimitReport,
    CashReservePlan, CapitalStagePlan, PositionSizingDashboard,
    PositionSizingReport, PositionSizingHealthSummary, get_all_model_names,
)


# ── CapitalProfile ────────────────────────────────────────────────────────────
def test_capital_profile_paper_only():
    assert CapitalProfile().paper_only is True

def test_capital_profile_allocation_only():
    assert CapitalProfile().allocation_only is True

def test_capital_profile_no_real_orders():
    assert CapitalProfile().no_real_orders is True

def test_capital_profile_default_capital():
    assert CapitalProfile().capital == 300000.0

def test_capital_profile_custom_capital():
    assert CapitalProfile(capital=500000.0).capital == 500000.0

def test_capital_profile_schema_version():
    assert CapitalProfile().schema_version == "184"


# ── RiskBudget ────────────────────────────────────────────────────────────────
def test_risk_budget_paper_only():
    assert RiskBudget().paper_only is True

def test_risk_budget_no_real_orders():
    assert RiskBudget().no_real_orders is True

def test_risk_budget_no_margin():
    assert RiskBudget().no_margin is True

def test_risk_budget_no_leverage():
    assert RiskBudget().no_leverage is True

def test_risk_budget_default_per_trade_risk():
    assert RiskBudget().per_trade_risk_pct == 1.0

def test_risk_budget_custom_per_trade_risk():
    assert RiskBudget(per_trade_risk_pct=0.5).per_trade_risk_pct == 0.5

def test_risk_budget_default_max_position():
    assert RiskBudget().max_single_position_pct == 20.0

def test_risk_budget_default_cash_reserve():
    assert RiskBudget().cash_reserve_pct == 20.0

def test_risk_budget_default_max_drawdown():
    assert RiskBudget().max_drawdown_budget_pct == 20.0

def test_risk_budget_default_max_positions():
    assert RiskBudget().max_concurrent_positions == 4


# ── PositionSizingInput ───────────────────────────────────────────────────────
def test_ps_input_paper_only():
    assert PositionSizingInput().paper_only is True

def test_ps_input_allocation_only():
    assert PositionSizingInput().allocation_only is True

def test_ps_input_no_real_orders():
    assert PositionSizingInput().no_real_orders is True

def test_ps_input_no_broker():
    assert PositionSizingInput().no_broker is True

def test_ps_input_no_margin():
    assert PositionSizingInput().no_margin is True

def test_ps_input_no_leverage():
    assert PositionSizingInput().no_leverage is True

def test_ps_input_default_capital():
    assert PositionSizingInput().capital == 300000.0

def test_ps_input_default_risk_pct():
    assert PositionSizingInput().per_trade_risk_pct == 1.0

def test_ps_input_default_stop_loss_pct():
    assert PositionSizingInput().stop_loss_distance_pct == 7.0

def test_ps_input_has_stop_loss():
    assert PositionSizingInput().has_stop_loss is True

def test_ps_input_default_abc():
    assert PositionSizingInput().abc_buy_point == "A_10MA_PULLBACK"

def test_ps_input_schema_184():
    assert PositionSizingInput().schema_version == "184"


# ── PositionSizingRule ────────────────────────────────────────────────────────
def test_ps_rule_paper_only():
    assert PositionSizingRule().paper_only is True

def test_ps_rule_no_real_orders():
    assert PositionSizingRule().no_real_orders is True

def test_ps_rule_default_name():
    assert PositionSizingRule().rule_name == "fixed_risk"

def test_ps_rule_enabled():
    assert PositionSizingRule().enabled is True


# ── PositionSizingResult ──────────────────────────────────────────────────────
def test_ps_result_paper_only():
    assert PositionSizingResult().paper_only is True

def test_ps_result_allocation_only():
    assert PositionSizingResult().allocation_only is True

def test_ps_result_no_real_orders():
    assert PositionSizingResult().no_real_orders is True

def test_ps_result_no_broker():
    assert PositionSizingResult().no_broker is True

def test_ps_result_no_margin():
    assert PositionSizingResult().no_margin is True

def test_ps_result_not_investment_advice():
    assert PositionSizingResult().not_investment_advice is True

def test_ps_result_default_capital():
    assert PositionSizingResult().capital == 300000.0

def test_ps_result_default_grade():
    assert PositionSizingResult().final_position_grade == "SAFE"

def test_ps_result_default_action():
    assert PositionSizingResult().action == "PAPER_PLAN_READY"

def test_ps_result_schema():
    assert PositionSizingResult().schema_version == "184"


# ── PortfolioAllocationInput ──────────────────────────────────────────────────
def test_portfolio_alloc_input_paper_only():
    assert PortfolioAllocationInput().paper_only is True

def test_portfolio_alloc_input_no_real_orders():
    assert PortfolioAllocationInput().no_real_orders is True

def test_portfolio_alloc_input_default_positions():
    assert PortfolioAllocationInput().max_concurrent_positions == 4


# ── PortfolioAllocationResult ─────────────────────────────────────────────────
def test_portfolio_alloc_result_paper_only():
    assert PortfolioAllocationResult().paper_only is True

def test_portfolio_alloc_result_no_real_orders():
    assert PortfolioAllocationResult().no_real_orders is True

def test_portfolio_alloc_result_action():
    assert PortfolioAllocationResult().action == "ALLOCATION_ONLY"


# ── ScalingPlan ───────────────────────────────────────────────────────────────
def test_scaling_plan_paper_only():
    assert ScalingPlan().paper_only is True

def test_scaling_plan_no_real_orders():
    assert ScalingPlan().no_real_orders is True

def test_scaling_plan_default_abc():
    assert ScalingPlan().abc_buy_point == "A_10MA_PULLBACK"

def test_scaling_plan_initial_40pct():
    assert ScalingPlan().initial_entry_pct == 40.0


# ── AddPositionPlan ───────────────────────────────────────────────────────────
def test_add_position_plan_paper_only():
    assert AddPositionPlan().paper_only is True

def test_add_position_plan_action():
    assert AddPositionPlan().action == "PAPER_ADD_ALLOWED"


# ── ReducePositionPlan ────────────────────────────────────────────────────────
def test_reduce_position_plan_paper_only():
    assert ReducePositionPlan().paper_only is True

def test_reduce_position_plan_action():
    assert ReducePositionPlan().action == "REDUCE_RISK"


# ── StopLossBudget ────────────────────────────────────────────────────────────
def test_stop_loss_budget_paper_only():
    assert StopLossBudget().paper_only is True

def test_stop_loss_budget_default_distance():
    assert StopLossBudget().stop_loss_distance_pct == 7.0


# ── DrawdownBudget ────────────────────────────────────────────────────────────
def test_drawdown_budget_paper_only():
    assert DrawdownBudget().paper_only is True

def test_drawdown_budget_default_max():
    assert DrawdownBudget().max_drawdown_budget_pct == 20.0

def test_drawdown_budget_not_exhausted():
    assert DrawdownBudget().budget_exhausted is False


# ── ConcentrationRiskReport ───────────────────────────────────────────────────
def test_concentration_report_paper_only():
    assert ConcentrationRiskReport().paper_only is True

def test_concentration_report_default_risk_level():
    assert ConcentrationRiskReport().risk_level == "SAFE"


# ── ExposureLimitReport ───────────────────────────────────────────────────────
def test_exposure_report_paper_only():
    assert ExposureLimitReport().paper_only is True

def test_exposure_report_default_ok():
    assert ExposureLimitReport().exposure_ok is True


# ── CashReservePlan ───────────────────────────────────────────────────────────
def test_cash_reserve_plan_paper_only():
    assert CashReservePlan().paper_only is True

def test_cash_reserve_plan_default_pct():
    assert CashReservePlan().cash_reserve_pct == 20.0


# ── CapitalStagePlan ──────────────────────────────────────────────────────────
def test_capital_stage_plan_paper_only():
    assert CapitalStagePlan().paper_only is True

def test_capital_stage_plan_default_label():
    assert CapitalStagePlan().stage_label == "300K"


# ── PositionSizingDashboard ───────────────────────────────────────────────────
def test_ps_dashboard_paper_only():
    assert PositionSizingDashboard().paper_only is True

def test_ps_dashboard_no_real_orders():
    assert PositionSizingDashboard().no_real_orders is True

def test_ps_dashboard_no_broker():
    assert PositionSizingDashboard().no_broker is True


# ── PositionSizingReport ──────────────────────────────────────────────────────
def test_ps_report_paper_only():
    assert PositionSizingReport().paper_only is True

def test_ps_report_allocation_only():
    assert PositionSizingReport().allocation_only is True

def test_ps_report_no_real_orders():
    assert PositionSizingReport().no_real_orders is True

def test_ps_report_version():
    assert PositionSizingReport().version == "1.8.4"


# ── PositionSizingHealthSummary ───────────────────────────────────────────────
def test_ps_health_summary_paper_only():
    assert PositionSizingHealthSummary().paper_only is True

def test_ps_health_summary_no_real_orders():
    assert PositionSizingHealthSummary().no_real_orders is True

def test_ps_health_summary_default_status():
    assert PositionSizingHealthSummary().status == "FAIL"


# ── get_all_model_names ───────────────────────────────────────────────────────
def test_get_all_model_names_returns_list():
    assert isinstance(get_all_model_names(), list)

def test_get_all_model_names_count_19():
    assert len(get_all_model_names()) == 19

def test_get_all_model_names_contains_capital_profile():
    assert "CapitalProfile" in get_all_model_names()

def test_get_all_model_names_contains_risk_budget():
    assert "RiskBudget" in get_all_model_names()

def test_get_all_model_names_contains_ps_result():
    assert "PositionSizingResult" in get_all_model_names()

def test_get_all_model_names_contains_drawdown_budget():
    assert "DrawdownBudget" in get_all_model_names()
