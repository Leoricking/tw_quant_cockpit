"""
tests/test_decision_cockpit_models_v186.py
Tests for decision_cockpit_models_v186 module.
[!] Research Only. Paper Only. Decision Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import (
    DecisionCockpitInput, DecisionCockpitResult,
    DailyDecisionContext, WeeklyDecisionContext,
    MarketDecisionState, CandidateDecisionInput, CandidateDecisionResult,
    BuyPointDecision, RiskDecision, PositionSizingDecision,
    PortfolioDecision, MonteCarloDecision, ThemeDecision, RegimeDecision,
    EntryReadinessScore, AddReadinessScore, ReduceRiskDecision,
    BlockReason, DecisionChecklist, DecisionDashboard,
    DecisionReport, DecisionHealthSummary,
    get_all_model_names,
)


# ── DecisionCockpitInput ──────────────────────────────────────────────────────
def test_cockpit_input_paper_only():
    assert DecisionCockpitInput().paper_only is True

def test_cockpit_input_decision_only():
    assert DecisionCockpitInput().decision_only is True

def test_cockpit_input_no_real_orders():
    assert DecisionCockpitInput().no_real_orders is True

def test_cockpit_input_default_capital():
    assert DecisionCockpitInput().capital == 300000.0

def test_cockpit_input_default_regime():
    assert DecisionCockpitInput().market_regime == "BULL"

def test_cockpit_input_schema_version():
    assert DecisionCockpitInput().schema_version == "186"

def test_cockpit_input_no_broker():
    assert DecisionCockpitInput().no_broker is True

def test_cockpit_input_production_trading_blocked():
    assert DecisionCockpitInput().production_trading_blocked is True

def test_cockpit_input_custom_capital():
    assert DecisionCockpitInput(capital=500000.0).capital == 500000.0

# ── DecisionCockpitResult ─────────────────────────────────────────────────────
def test_cockpit_result_paper_only():
    assert DecisionCockpitResult().paper_only is True

def test_cockpit_result_decision_only():
    assert DecisionCockpitResult().decision_only is True

def test_cockpit_result_no_real_orders():
    assert DecisionCockpitResult().no_real_orders is True

def test_cockpit_result_cockpit_version():
    assert DecisionCockpitResult().cockpit_version == "1.8.6"

def test_cockpit_result_default_grade():
    assert DecisionCockpitResult().final_cockpit_grade == "WAIT"

def test_cockpit_result_schema_version():
    assert DecisionCockpitResult().schema_version == "186"

def test_cockpit_result_production_trading_blocked():
    assert DecisionCockpitResult().production_trading_blocked is True

# ── DailyDecisionContext ──────────────────────────────────────────────────────
def test_daily_context_paper_only():
    assert DailyDecisionContext().paper_only is True

def test_daily_context_decision_only():
    assert DailyDecisionContext().decision_only is True

def test_daily_context_no_real_orders():
    assert DailyDecisionContext().no_real_orders is True

def test_daily_context_default_action():
    assert DailyDecisionContext().daily_action == "DECISION_ONLY"

# ── WeeklyDecisionContext ─────────────────────────────────────────────────────
def test_weekly_context_paper_only():
    assert WeeklyDecisionContext().paper_only is True

def test_weekly_context_decision_only():
    assert WeeklyDecisionContext().decision_only is True

def test_weekly_context_default_action():
    assert WeeklyDecisionContext().weekly_action == "DECISION_ONLY"

# ── MarketDecisionState ───────────────────────────────────────────────────────
def test_market_state_paper_only():
    assert MarketDecisionState().paper_only is True

def test_market_state_decision_only():
    assert MarketDecisionState().decision_only is True

def test_market_state_default_regime():
    assert MarketDecisionState().market_regime == "BULL"

def test_market_state_default_action():
    assert MarketDecisionState().action == "DECISION_ONLY"

# ── CandidateDecisionInput ────────────────────────────────────────────────────
def test_candidate_input_paper_only():
    assert CandidateDecisionInput().paper_only is True

def test_candidate_input_decision_only():
    assert CandidateDecisionInput().decision_only is True

def test_candidate_input_default_regime():
    assert CandidateDecisionInput().market_regime == "BULL"

def test_candidate_input_default_buy_point():
    assert CandidateDecisionInput().abc_buy_point == "A_10MA_PULLBACK"

def test_candidate_input_custom_ticker():
    assert CandidateDecisionInput(ticker="2330").ticker == "2330"

# ── CandidateDecisionResult ───────────────────────────────────────────────────
def test_candidate_result_paper_only():
    assert CandidateDecisionResult().paper_only is True

def test_candidate_result_decision_only():
    assert CandidateDecisionResult().decision_only is True

def test_candidate_result_default_action():
    assert CandidateDecisionResult().final_action == "WAIT"

# ── BuyPointDecision ─────────────────────────────────────────────────────────
def test_buy_point_decision_paper_only():
    assert BuyPointDecision().paper_only is True

def test_buy_point_decision_no_real_orders():
    assert BuyPointDecision().no_real_orders is True

def test_buy_point_decision_default_action():
    assert BuyPointDecision().action == "WAIT"

# ── RiskDecision ─────────────────────────────────────────────────────────────
def test_risk_decision_paper_only():
    assert RiskDecision().paper_only is True

def test_risk_decision_default_action():
    assert RiskDecision().action == "DECISION_ONLY"

def test_risk_decision_default_cash():
    assert RiskDecision().cash_reserve_pct == 100.0

# ── PositionSizingDecision ────────────────────────────────────────────────────
def test_position_sizing_paper_only():
    assert PositionSizingDecision().paper_only is True

def test_position_sizing_decision_only():
    assert PositionSizingDecision().decision_only is True

def test_position_sizing_default_action():
    assert PositionSizingDecision().action == "DECISION_ONLY"

# ── PortfolioDecision ─────────────────────────────────────────────────────────
def test_portfolio_decision_paper_only():
    assert PortfolioDecision().paper_only is True

def test_portfolio_decision_default_action():
    assert PortfolioDecision().action == "DECISION_ONLY"

# ── MonteCarloDecision ────────────────────────────────────────────────────────
def test_monte_carlo_decision_paper_only():
    assert MonteCarloDecision().paper_only is True

def test_monte_carlo_default_level():
    assert MonteCarloDecision().ruin_risk_level == "LOW"

def test_monte_carlo_default_entry():
    assert MonteCarloDecision().entry_allowed is True

# ── ThemeDecision ─────────────────────────────────────────────────────────────
def test_theme_decision_paper_only():
    assert ThemeDecision().paper_only is True

def test_theme_decision_default_action():
    assert ThemeDecision().action == "DECISION_ONLY"

# ── RegimeDecision ────────────────────────────────────────────────────────────
def test_regime_decision_paper_only():
    assert RegimeDecision().paper_only is True

def test_regime_decision_default_regime():
    assert RegimeDecision().market_regime == "BULL"

def test_regime_decision_default_entry():
    assert RegimeDecision().entry_permitted is True

# ── EntryReadinessScore ───────────────────────────────────────────────────────
def test_entry_readiness_paper_only():
    assert EntryReadinessScore().paper_only is True

def test_entry_readiness_default_action():
    assert EntryReadinessScore().action == "WAIT"

# ── AddReadinessScore ─────────────────────────────────────────────────────────
def test_add_readiness_paper_only():
    assert AddReadinessScore().paper_only is True

def test_add_readiness_default_action():
    assert AddReadinessScore().action == "WAIT"

# ── ReduceRiskDecision ────────────────────────────────────────────────────────
def test_reduce_risk_paper_only():
    assert ReduceRiskDecision().paper_only is True

def test_reduce_risk_default_action():
    assert ReduceRiskDecision().action == "OBSERVE"

def test_reduce_risk_default_not_required():
    assert ReduceRiskDecision().reduce_required is False

# ── BlockReason ───────────────────────────────────────────────────────────────
def test_block_reason_paper_only():
    assert BlockReason().paper_only is True

def test_block_reason_default_severity():
    assert BlockReason().severity == "HIGH"

# ── DecisionChecklist ─────────────────────────────────────────────────────────
def test_checklist_paper_only():
    assert DecisionChecklist().paper_only is True

def test_checklist_all_false_default():
    assert DecisionChecklist().all_checked is False

# ── DecisionDashboard ─────────────────────────────────────────────────────────
def test_dashboard_paper_only():
    assert DecisionDashboard().paper_only is True

def test_dashboard_decision_only():
    assert DecisionDashboard().decision_only is True

def test_dashboard_no_broker():
    assert DecisionDashboard().no_broker is True

def test_dashboard_default_grade():
    assert DecisionDashboard().final_cockpit_grade == "WAIT"

# ── DecisionReport ────────────────────────────────────────────────────────────
def test_report_paper_only():
    assert DecisionReport().paper_only is True

def test_report_decision_only():
    assert DecisionReport().decision_only is True

def test_report_no_margin():
    assert DecisionReport().no_margin is True

def test_report_production_trading_blocked():
    assert DecisionReport().production_trading_blocked is True

def test_report_version():
    assert DecisionReport().version == "1.8.6"

# ── DecisionHealthSummary ─────────────────────────────────────────────────────
def test_health_summary_paper_only():
    assert DecisionHealthSummary().paper_only is True

def test_health_summary_decision_only():
    assert DecisionHealthSummary().decision_only is True

def test_health_summary_default_status():
    assert DecisionHealthSummary().status == "FAIL"

# ── get_all_model_names ───────────────────────────────────────────────────────
def test_all_model_names_count():
    assert len(get_all_model_names()) == 22

def test_all_model_names_has_cockpit_input():
    assert "DecisionCockpitInput" in get_all_model_names()

def test_all_model_names_has_cockpit_result():
    assert "DecisionCockpitResult" in get_all_model_names()

def test_all_model_names_has_block_reason():
    assert "BlockReason" in get_all_model_names()

def test_all_model_names_has_decision_dashboard():
    assert "DecisionDashboard" in get_all_model_names()

def test_all_model_names_returns_list():
    assert isinstance(get_all_model_names(), list)
