"""
tests/test_portfolio_construction_engine_v185.py
Tests for portfolio_construction_engine_v185 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_construction_engine_v185 import (
    ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
    CAPITAL_STAGES, WEIGHTING_METHODS, KEEP_REPLACE_ACTIONS,
    validate_action, validate_grade,
    run_portfolio_construction, run_rebalance, build_portfolio_dashboard,
    get_engine_info,
    _compute_equal_weights, _compute_conviction_weights,
    _compute_volatility_adjusted_weights, _herfindahl_index, _diversification_score,
    _check_hard_blocks, _grade_portfolio, _keep_or_replace_decision,
)
from paper_trading.small_capital_strategy.portfolio_construction_models_v185 import (
    PortfolioConstructionInput, PortfolioHolding, PortfolioCandidate, RebalanceInput,
)


# ── Constants ──────────────────────────────────────────────────────────────────
def test_allowed_actions_count():
    assert len(ALLOWED_OUTPUT_ACTIONS) == 16

def test_forbidden_words_count():
    assert len(FORBIDDEN_OUTPUT_WORDS) == 9

def test_valid_grades_count():
    assert len(VALID_FINAL_GRADES) == 6

def test_capital_stages_count():
    assert len(CAPITAL_STAGES) == 4

def test_weighting_methods_count():
    assert len(WEIGHTING_METHODS) == 10

def test_portfolio_only_in_actions():
    assert "PORTFOLIO_ONLY" in ALLOWED_OUTPUT_ACTIONS

def test_blocked_in_actions():
    assert "BLOCKED" in ALLOWED_OUTPUT_ACTIONS

def test_reduce_risk_in_actions():
    assert "REDUCE_RISK" in ALLOWED_OUTPUT_ACTIONS

def test_buy_not_in_actions():
    assert "BUY" not in ALLOWED_OUTPUT_ACTIONS

def test_sell_not_in_actions():
    assert "SELL" not in ALLOWED_OUTPUT_ACTIONS

def test_buy_in_forbidden():
    assert "BUY" in FORBIDDEN_OUTPUT_WORDS

def test_sell_in_forbidden():
    assert "SELL" in FORBIDDEN_OUTPUT_WORDS

def test_order_in_forbidden():
    assert "ORDER" in FORBIDDEN_OUTPUT_WORDS

def test_execute_in_forbidden():
    assert "EXECUTE" in FORBIDDEN_OUTPUT_WORDS

def test_auto_trade_in_forbidden():
    assert "AUTO_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_real_trade_in_forbidden():
    assert "REAL_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_live_trade_in_forbidden():
    assert "LIVE_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_broker_order_in_forbidden():
    assert "BROKER_ORDER" in FORBIDDEN_OUTPUT_WORDS

def test_balanced_in_grades():
    assert "BALANCED" in VALID_FINAL_GRADES

def test_blocked_in_grades():
    assert "BLOCKED" in VALID_FINAL_GRADES

def test_overexposed_in_grades():
    assert "OVEREXPOSED" in VALID_FINAL_GRADES

def test_concentrated_in_grades():
    assert "CONCENTRATED" in VALID_FINAL_GRADES

def test_high_risk_in_grades():
    assert "HIGH_RISK" in VALID_FINAL_GRADES

def test_capital_stage_300k():
    assert 300000 in CAPITAL_STAGES

def test_capital_stage_3m():
    assert 3000000 in CAPITAL_STAGES


# ── validate_action ────────────────────────────────────────────────────────────
def test_validate_action_portfolio_only():
    assert validate_action("PORTFOLIO_ONLY") is True

def test_validate_action_blocked():
    assert validate_action("BLOCKED") is True

def test_validate_action_reduce_risk():
    assert validate_action("REDUCE_RISK") is True

def test_validate_action_observe():
    assert validate_action("OBSERVE") is True

def test_validate_action_buy_false():
    assert validate_action("BUY") is False

def test_validate_action_sell_false():
    assert validate_action("SELL") is False


# ── validate_grade ─────────────────────────────────────────────────────────────
def test_validate_grade_balanced():
    assert validate_grade("BALANCED") is True

def test_validate_grade_blocked():
    assert validate_grade("BLOCKED") is True

def test_validate_grade_overexposed():
    assert validate_grade("OVEREXPOSED") is True

def test_validate_grade_invalid():
    assert validate_grade("BUY") is False


# ── _compute_equal_weights ─────────────────────────────────────────────────────
def test_equal_weights_1():
    assert _compute_equal_weights(1) == [100.0]

def test_equal_weights_2():
    w = _compute_equal_weights(2)
    assert len(w) == 2
    assert abs(w[0] - 50.0) < 0.01

def test_equal_weights_4():
    w = _compute_equal_weights(4)
    assert len(w) == 4
    assert abs(w[0] - 25.0) < 0.01

def test_equal_weights_0():
    assert _compute_equal_weights(0) == []


# ── _herfindahl_index ──────────────────────────────────────────────────────────
def test_hhi_equal_4():
    hhi = _herfindahl_index([25.0, 25.0, 25.0, 25.0])
    assert abs(hhi - 0.25) < 0.001

def test_hhi_concentrated():
    hhi = _herfindahl_index([100.0])
    assert abs(hhi - 1.0) < 0.001

def test_hhi_empty():
    assert _herfindahl_index([]) == 0.0


# ── _diversification_score ────────────────────────────────────────────────────
def test_div_score_equal_4():
    hhi = _herfindahl_index([25.0, 25.0, 25.0, 25.0])
    score = _diversification_score(hhi, 4)
    assert score == 100.0

def test_div_score_concentrated():
    hhi = _herfindahl_index([100.0])
    score = _diversification_score(hhi, 1)
    assert score >= 0.0

def test_div_score_0_positions():
    assert _diversification_score(1.0, 0) == 0.0


# ── run_portfolio_construction ─────────────────────────────────────────────────
def test_empty_portfolio_balanced():
    inp = PortfolioConstructionInput(capital=300000.0, market_regime="BULL")
    result = run_portfolio_construction(inp)
    assert result.final_portfolio_grade == "BALANCED"

def test_empty_portfolio_portfolio_only_action():
    inp = PortfolioConstructionInput(capital=300000.0, market_regime="BULL")
    result = run_portfolio_construction(inp)
    assert result.action == "PORTFOLIO_ONLY"

def test_empty_portfolio_paper_only():
    inp = PortfolioConstructionInput(capital=300000.0, market_regime="BULL")
    assert run_portfolio_construction(inp).paper_only is True

def test_empty_portfolio_portfolio_only():
    inp = PortfolioConstructionInput(capital=300000.0, market_regime="BULL")
    assert run_portfolio_construction(inp).portfolio_only is True

def test_empty_portfolio_no_real_orders():
    inp = PortfolioConstructionInput(capital=300000.0, market_regime="BULL")
    assert run_portfolio_construction(inp).no_real_orders is True

def test_blocked_regime():
    inp = PortfolioConstructionInput(capital=300000.0, market_regime="BLOCKED")
    assert run_portfolio_construction(inp).final_portfolio_grade == "BLOCKED"

def test_blocked_regime_action():
    inp = PortfolioConstructionInput(capital=300000.0, market_regime="BLOCKED")
    assert run_portfolio_construction(inp).action == "BLOCKED"

def test_high_ruin_risk_blocked():
    inp = PortfolioConstructionInput(capital=300000.0, monte_carlo_ruin_risk_pct=25.0)
    assert run_portfolio_construction(inp).final_portfolio_grade == "BLOCKED"

def test_low_cash_reserve_blocked():
    inp = PortfolioConstructionInput(capital=300000.0, min_cash_reserve_pct=2.0)
    assert run_portfolio_construction(inp).final_portfolio_grade == "BLOCKED"

def test_holding_count_zero_empty():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert run_portfolio_construction(inp).holding_count == 0

def test_holding_count_with_holdings():
    h = PortfolioHolding(ticker="A", value=100000.0, above_10ma=True, above_20ma=True)
    inp = PortfolioConstructionInput(capital=300000.0, holdings=[h])
    assert run_portfolio_construction(inp).holding_count == 1

def test_three_holdings_count():
    holdings = [
        PortfolioHolding(ticker="A", value=100000.0, above_10ma=True, above_20ma=True),
        PortfolioHolding(ticker="B", value=100000.0, above_10ma=True, above_20ma=True),
        PortfolioHolding(ticker="C", value=100000.0, above_10ma=True, above_20ma=True),
    ]
    inp = PortfolioConstructionInput(capital=300000.0, holdings=holdings)
    assert run_portfolio_construction(inp).holding_count == 3

def test_keep_above_10ma_20ma():
    h = PortfolioHolding(ticker="KEEP", above_10ma=True, above_20ma=True, value=100000.0)
    inp = PortfolioConstructionInput(capital=300000.0, holdings=[h])
    result = run_portfolio_construction(inp)
    assert "KEEP" in result.suggested_keep_list

def test_reduce_no_10ma():
    h = PortfolioHolding(ticker="RED", above_10ma=False, above_20ma=True, value=100000.0)
    inp = PortfolioConstructionInput(capital=300000.0, holdings=[h])
    result = run_portfolio_construction(inp)
    assert "RED" in result.suggested_reduce_list

def test_replace_no_20ma():
    h = PortfolioHolding(ticker="RPL", above_10ma=False, above_20ma=False, value=100000.0)
    inp = PortfolioConstructionInput(capital=300000.0, holdings=[h])
    result = run_portfolio_construction(inp)
    assert "RPL" in result.suggested_replace_list

def test_cash_reserve_computed():
    inp = PortfolioConstructionInput(capital=300000.0, min_cash_reserve_pct=20.0)
    result = run_portfolio_construction(inp)
    assert result.cash_reserve_pct >= 20.0

def test_cash_reserve_amount_gt0():
    inp = PortfolioConstructionInput(capital=300000.0, min_cash_reserve_pct=20.0)
    result = run_portfolio_construction(inp)
    assert result.cash_reserve_amount > 0

def test_mc_ruin_adjustment_zero():
    inp = PortfolioConstructionInput(capital=300000.0, monte_carlo_ruin_risk_pct=0.0)
    assert run_portfolio_construction(inp).monte_carlo_ruin_risk_adjustment == 1.0

def test_mc_ruin_adjustment_medium():
    inp = PortfolioConstructionInput(capital=300000.0, monte_carlo_ruin_risk_pct=8.0)
    assert run_portfolio_construction(inp).monte_carlo_ruin_risk_adjustment == 0.7

def test_mc_ruin_adjustment_high():
    inp = PortfolioConstructionInput(capital=300000.0, monte_carlo_ruin_risk_pct=15.0)
    assert run_portfolio_construction(inp).monte_carlo_ruin_risk_adjustment == 0.5

def test_result_action_valid():
    inp = PortfolioConstructionInput(capital=300000.0)
    result = run_portfolio_construction(inp)
    assert result.action in ALLOWED_OUTPUT_ACTIONS

def test_result_grade_valid():
    inp = PortfolioConstructionInput(capital=300000.0)
    result = run_portfolio_construction(inp)
    assert result.final_portfolio_grade in VALID_FINAL_GRADES

def test_result_schema_version():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert run_portfolio_construction(inp).schema_version == "185"

def test_capital_500k():
    inp = PortfolioConstructionInput(capital=500000.0)
    assert run_portfolio_construction(inp).capital == 500000.0

def test_capital_1m():
    inp = PortfolioConstructionInput(capital=1000000.0)
    assert run_portfolio_construction(inp).capital == 1000000.0

def test_capital_3m():
    inp = PortfolioConstructionInput(capital=3000000.0)
    assert run_portfolio_construction(inp).capital == 3000000.0

def test_blocked_candidate_blocked_regime():
    c = PortfolioCandidate(ticker="BLK", market_regime_compatible=False)
    inp = PortfolioConstructionInput(capital=300000.0, market_regime="BULL", candidates=[c])
    result = run_portfolio_construction(inp)
    assert "BLK" in result.blocked_candidates


# ── run_rebalance ──────────────────────────────────────────────────────────────
def test_rebalance_empty_not_needed():
    ri = RebalanceInput(capital=300000.0, holdings=[], rebalance_threshold_pct=10.0)
    assert run_rebalance(ri).rebalance_needed is False

def test_rebalance_plan_paper_only():
    ri = RebalanceInput(capital=300000.0)
    assert run_rebalance(ri).paper_only is True

def test_rebalance_no_real_orders():
    ri = RebalanceInput(capital=300000.0)
    assert run_rebalance(ri).no_real_orders is True

def test_rebalance_drift_detected():
    h = PortfolioHolding(ticker="A", weight_pct=50.0, value=150000.0, above_10ma=True, above_20ma=True)
    ri = RebalanceInput(capital=300000.0, holdings=[h],
                        rebalance_threshold_pct=5.0, target_weights={"A": 33.33})
    plan = run_rebalance(ri)
    assert plan.total_drift_pct > 0

def test_rebalance_needed_on_drift():
    h = PortfolioHolding(ticker="A", weight_pct=60.0, value=180000.0, above_10ma=True, above_20ma=True)
    ri = RebalanceInput(capital=300000.0, holdings=[h],
                        rebalance_threshold_pct=5.0, target_weights={"A": 33.33})
    plan = run_rebalance(ri)
    assert plan.rebalance_needed is True

def test_rebalance_action_list():
    h = PortfolioHolding(ticker="A", weight_pct=33.0, value=100000.0, above_10ma=True, above_20ma=True)
    ri = RebalanceInput(capital=300000.0, holdings=[h], target_weights={"A": 33.33})
    plan = run_rebalance(ri)
    assert isinstance(plan.actions, list)


# ── build_portfolio_dashboard ──────────────────────────────────────────────────
def test_dashboard_paper_only():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert build_portfolio_dashboard(inp).paper_only is True

def test_dashboard_no_real_orders():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert build_portfolio_dashboard(inp).no_real_orders is True

def test_dashboard_schema_version():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert build_portfolio_dashboard(inp).schema_version == "185"

def test_dashboard_profile_not_none():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert build_portfolio_dashboard(inp).profile is not None

def test_dashboard_exposure_report_not_none():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert build_portfolio_dashboard(inp).exposure_report is not None

def test_dashboard_sector_report_not_none():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert build_portfolio_dashboard(inp).sector_report is not None

def test_dashboard_theme_report_not_none():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert build_portfolio_dashboard(inp).theme_report is not None

def test_dashboard_correlation_report_not_none():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert build_portfolio_dashboard(inp).correlation_report is not None

def test_dashboard_diversification_score_not_none():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert build_portfolio_dashboard(inp).diversification_score is not None

def test_dashboard_rebalance_plan_not_none():
    inp = PortfolioConstructionInput(capital=300000.0)
    assert build_portfolio_dashboard(inp).rebalance_plan is not None


# ── get_engine_info ────────────────────────────────────────────────────────────
def test_engine_info_dict():
    assert isinstance(get_engine_info(), dict)

def test_engine_info_version():
    assert get_engine_info()["version"] == "1.8.5"

def test_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True

def test_engine_info_portfolio_only():
    assert get_engine_info()["portfolio_only"] is True

def test_engine_info_no_real_orders():
    assert get_engine_info()["no_real_orders"] is True

def test_engine_info_has_allowed_actions():
    assert "allowed_output_actions" in get_engine_info()

def test_engine_info_has_forbidden_words():
    assert "forbidden_output_words" in get_engine_info()

def test_engine_info_has_capital_stages():
    assert "capital_stages" in get_engine_info()
