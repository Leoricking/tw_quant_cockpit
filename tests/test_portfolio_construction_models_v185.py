"""
tests/test_portfolio_construction_models_v185.py
Tests for portfolio_construction_models_v185 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_construction_models_v185 import (
    PortfolioProfile, PortfolioHolding, PortfolioCandidate,
    PortfolioConstructionInput, PortfolioConstructionResult,
    RebalanceInput, RebalancePlan, RebalanceAction,
    PortfolioExposureReport, SectorExposureReport, ThemeExposureReport,
    CorrelationRiskReport, ConcentrationLimit, DiversificationScore,
    RotationCandidate, KeepOrReplaceDecision, PortfolioRiskBudget,
    PortfolioDashboard, PortfolioRebalanceReport, PortfolioHealthSummary,
    get_all_model_names,
)


# ── PortfolioProfile ──────────────────────────────────────────────────────────
def test_portfolio_profile_paper_only():
    assert PortfolioProfile().paper_only is True

def test_portfolio_profile_portfolio_only():
    assert PortfolioProfile().portfolio_only is True

def test_portfolio_profile_no_real_orders():
    assert PortfolioProfile().no_real_orders is True

def test_portfolio_profile_default_capital():
    assert PortfolioProfile().capital == 300000.0

def test_portfolio_profile_custom_capital():
    assert PortfolioProfile(capital=500000.0).capital == 500000.0

def test_portfolio_profile_schema_version():
    assert PortfolioProfile().schema_version == "185"

def test_portfolio_profile_default_max_positions():
    assert PortfolioProfile().max_positions == 3

def test_portfolio_profile_no_margin():
    assert PortfolioProfile().no_margin is True

def test_portfolio_profile_no_leverage():
    assert PortfolioProfile().no_leverage is True


# ── PortfolioHolding ──────────────────────────────────────────────────────────
def test_portfolio_holding_paper_only():
    assert PortfolioHolding().paper_only is True

def test_portfolio_holding_no_real_orders():
    assert PortfolioHolding().no_real_orders is True

def test_portfolio_holding_default_ticker():
    assert PortfolioHolding().ticker == ""

def test_portfolio_holding_custom_ticker():
    assert PortfolioHolding(ticker="2330").ticker == "2330"

def test_portfolio_holding_schema_version():
    assert PortfolioHolding().schema_version == "185"

def test_portfolio_holding_above_10ma_default():
    assert PortfolioHolding().above_10ma is True

def test_portfolio_holding_above_20ma_default():
    assert PortfolioHolding().above_20ma is True

def test_portfolio_holding_conviction_score_default():
    assert PortfolioHolding().conviction_score == 5.0


# ── PortfolioCandidate ────────────────────────────────────────────────────────
def test_portfolio_candidate_paper_only():
    assert PortfolioCandidate().paper_only is True

def test_portfolio_candidate_no_real_orders():
    assert PortfolioCandidate().no_real_orders is True

def test_portfolio_candidate_schema_version():
    assert PortfolioCandidate().schema_version == "185"

def test_portfolio_candidate_market_regime_compatible_default():
    assert PortfolioCandidate().market_regime_compatible is True


# ── PortfolioConstructionInput ────────────────────────────────────────────────
def test_construction_input_paper_only():
    assert PortfolioConstructionInput().paper_only is True

def test_construction_input_portfolio_only():
    assert PortfolioConstructionInput().portfolio_only is True

def test_construction_input_no_real_orders():
    assert PortfolioConstructionInput().no_real_orders is True

def test_construction_input_default_capital():
    assert PortfolioConstructionInput().capital == 300000.0

def test_construction_input_default_regime():
    assert PortfolioConstructionInput().market_regime == "BULL"

def test_construction_input_default_max_positions():
    assert PortfolioConstructionInput().max_positions == 3

def test_construction_input_schema_version():
    assert PortfolioConstructionInput().schema_version == "185"

def test_construction_input_no_margin():
    assert PortfolioConstructionInput().no_margin is True

def test_construction_input_no_leverage():
    assert PortfolioConstructionInput().no_leverage is True

def test_construction_input_default_holdings_empty():
    assert PortfolioConstructionInput().holdings == []


# ── PortfolioConstructionResult ───────────────────────────────────────────────
def test_construction_result_paper_only():
    assert PortfolioConstructionResult().paper_only is True

def test_construction_result_portfolio_only():
    assert PortfolioConstructionResult().portfolio_only is True

def test_construction_result_no_real_orders():
    assert PortfolioConstructionResult().no_real_orders is True

def test_construction_result_default_grade():
    assert PortfolioConstructionResult().final_portfolio_grade == "BALANCED"

def test_construction_result_default_action():
    assert PortfolioConstructionResult().action == "PORTFOLIO_ONLY"

def test_construction_result_schema_version():
    assert PortfolioConstructionResult().schema_version == "185"

def test_construction_result_default_keep_list():
    assert PortfolioConstructionResult().suggested_keep_list == []


# ── RebalanceInput ────────────────────────────────────────────────────────────
def test_rebalance_input_paper_only():
    assert RebalanceInput().paper_only is True

def test_rebalance_input_no_real_orders():
    assert RebalanceInput().no_real_orders is True

def test_rebalance_input_schema_version():
    assert RebalanceInput().schema_version == "185"

def test_rebalance_input_default_threshold():
    assert RebalanceInput().rebalance_threshold_pct == 10.0


# ── RebalancePlan ─────────────────────────────────────────────────────────────
def test_rebalance_plan_paper_only():
    assert RebalancePlan().paper_only is True

def test_rebalance_plan_no_real_orders():
    assert RebalancePlan().no_real_orders is True

def test_rebalance_plan_default_not_needed():
    assert RebalancePlan().rebalance_needed is False

def test_rebalance_plan_schema_version():
    assert RebalancePlan().schema_version == "185"


# ── RebalanceAction ───────────────────────────────────────────────────────────
def test_rebalance_action_paper_only():
    assert RebalanceAction().paper_only is True

def test_rebalance_action_no_real_orders():
    assert RebalanceAction().no_real_orders is True

def test_rebalance_action_default_type():
    assert RebalanceAction().action_type == "OBSERVE"

def test_rebalance_action_schema_version():
    assert RebalanceAction().schema_version == "185"


# ── PortfolioExposureReport ───────────────────────────────────────────────────
def test_exposure_report_paper_only():
    assert PortfolioExposureReport().paper_only is True

def test_exposure_report_no_real_orders():
    assert PortfolioExposureReport().no_real_orders is True

def test_exposure_report_default_ok():
    assert PortfolioExposureReport().exposure_ok is True

def test_exposure_report_schema_version():
    assert PortfolioExposureReport().schema_version == "185"


# ── SectorExposureReport ──────────────────────────────────────────────────────
def test_sector_report_paper_only():
    assert SectorExposureReport().paper_only is True

def test_sector_report_sector_ok_default():
    assert SectorExposureReport().sector_ok is True

def test_sector_report_schema_version():
    assert SectorExposureReport().schema_version == "185"


# ── ThemeExposureReport ───────────────────────────────────────────────────────
def test_theme_report_paper_only():
    assert ThemeExposureReport().paper_only is True

def test_theme_report_theme_ok_default():
    assert ThemeExposureReport().theme_ok is True

def test_theme_report_schema_version():
    assert ThemeExposureReport().schema_version == "185"


# ── CorrelationRiskReport ─────────────────────────────────────────────────────
def test_correlation_report_paper_only():
    assert CorrelationRiskReport().paper_only is True

def test_correlation_report_ok_default():
    assert CorrelationRiskReport().correlation_ok is True

def test_correlation_report_schema_version():
    assert CorrelationRiskReport().schema_version == "185"


# ── ConcentrationLimit ────────────────────────────────────────────────────────
def test_concentration_limit_paper_only():
    assert ConcentrationLimit().paper_only is True

def test_concentration_limit_max_single():
    assert ConcentrationLimit().max_single_position_pct == 25.0

def test_concentration_limit_schema_version():
    assert ConcentrationLimit().schema_version == "185"


# ── DiversificationScore ──────────────────────────────────────────────────────
def test_diversification_score_paper_only():
    assert DiversificationScore().paper_only is True

def test_diversification_score_default():
    assert DiversificationScore().score == 0.0

def test_diversification_score_schema_version():
    assert DiversificationScore().schema_version == "185"


# ── RotationCandidate ─────────────────────────────────────────────────────────
def test_rotation_candidate_paper_only():
    assert RotationCandidate().paper_only is True

def test_rotation_candidate_action_observe():
    assert RotationCandidate().suggested_action == "OBSERVE"

def test_rotation_candidate_schema_version():
    assert RotationCandidate().schema_version == "185"


# ── KeepOrReplaceDecision ─────────────────────────────────────────────────────
def test_keep_or_replace_paper_only():
    assert KeepOrReplaceDecision().paper_only is True

def test_keep_or_replace_default_decision():
    assert KeepOrReplaceDecision().decision == "OBSERVE"

def test_keep_or_replace_schema_version():
    assert KeepOrReplaceDecision().schema_version == "185"


# ── PortfolioRiskBudget ───────────────────────────────────────────────────────
def test_portfolio_risk_budget_paper_only():
    assert PortfolioRiskBudget().paper_only is True

def test_portfolio_risk_budget_max_exposure():
    assert PortfolioRiskBudget().max_total_exposure_pct == 60.0

def test_portfolio_risk_budget_schema_version():
    assert PortfolioRiskBudget().schema_version == "185"


# ── PortfolioDashboard ────────────────────────────────────────────────────────
def test_portfolio_dashboard_paper_only():
    assert PortfolioDashboard().paper_only is True

def test_portfolio_dashboard_no_real_orders():
    assert PortfolioDashboard().no_real_orders is True

def test_portfolio_dashboard_schema_version():
    assert PortfolioDashboard().schema_version == "185"


# ── PortfolioRebalanceReport ──────────────────────────────────────────────────
def test_rebalance_report_paper_only():
    assert PortfolioRebalanceReport().paper_only is True

def test_rebalance_report_portfolio_only():
    assert PortfolioRebalanceReport().portfolio_only is True

def test_rebalance_report_version():
    assert PortfolioRebalanceReport().version == "1.8.5"

def test_rebalance_report_schema_version():
    assert PortfolioRebalanceReport().schema_version == "185"


# ── PortfolioHealthSummary ────────────────────────────────────────────────────
def test_health_summary_paper_only():
    assert PortfolioHealthSummary().paper_only is True

def test_health_summary_no_real_orders():
    assert PortfolioHealthSummary().no_real_orders is True

def test_health_summary_schema_version():
    assert PortfolioHealthSummary().schema_version == "185"

def test_health_summary_default_not_passed():
    assert PortfolioHealthSummary().all_passed is False


# ── get_all_model_names ───────────────────────────────────────────────────────
def test_get_all_model_names_count():
    assert len(get_all_model_names()) == 20

def test_get_all_model_names_portfolio_profile():
    assert "PortfolioProfile" in get_all_model_names()

def test_get_all_model_names_portfolio_holding():
    assert "PortfolioHolding" in get_all_model_names()

def test_get_all_model_names_construction_input():
    assert "PortfolioConstructionInput" in get_all_model_names()

def test_get_all_model_names_rebalance_plan():
    assert "RebalancePlan" in get_all_model_names()

def test_get_all_model_names_health_summary():
    assert "PortfolioHealthSummary" in get_all_model_names()
