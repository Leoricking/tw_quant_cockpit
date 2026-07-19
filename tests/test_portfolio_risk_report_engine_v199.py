"""
tests/test_portfolio_risk_report_engine_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Engine Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.portfolio_risk_report_engine_v199 import (
    validate_sizing_input,
    compute_entry_size_multiplier,
    compute_risk_grade,
    compute_position_size,
    check_cash_buffer,
    check_theme_exposure,
    check_industry_exposure,
    check_symbol_weight,
    check_correlation_cluster,
    evaluate_no_entry_conditions,
    run_position_sizing_report,
)

_VALID_INPUT = {
    "paper_only": True,
    "no_real_orders": True,
    "not_investment_advice": True,
    "capital_base": 300000,
    "entry_type": "A_PULLBACK_10MA",
    "stop_distance_pct": 0.05,
}


def test_validate_sizing_input_empty_dict_returns_blocked():
    result = validate_sizing_input({})
    assert result["blocked"] is True


def test_validate_sizing_input_missing_paper_only_returns_blocked():
    inp = {k: v for k, v in _VALID_INPUT.items() if k != "paper_only"}
    result = validate_sizing_input(inp)
    assert result["blocked"] is True


def test_validate_sizing_input_missing_paper_only_has_flag():
    inp = {k: v for k, v in _VALID_INPUT.items() if k != "paper_only"}
    result = validate_sizing_input(inp)
    assert result.get("blocked") is True
    assert "missing_paper_only_flags" in result.get("block_reason", "")


def test_validate_sizing_input_missing_no_real_orders_returns_blocked():
    inp = {k: v for k, v in _VALID_INPUT.items() if k != "no_real_orders"}
    result = validate_sizing_input(inp)
    assert result["blocked"] is True


def test_validate_sizing_input_missing_not_investment_advice_returns_blocked():
    inp = {k: v for k, v in _VALID_INPUT.items() if k != "not_investment_advice"}
    result = validate_sizing_input(inp)
    assert result["blocked"] is True


def test_validate_sizing_input_missing_capital_base_returns_blocked():
    inp = {k: v for k, v in _VALID_INPUT.items() if k != "capital_base"}
    result = validate_sizing_input(inp)
    assert result["blocked"] is True


def test_validate_sizing_input_missing_entry_type_returns_blocked():
    inp = {k: v for k, v in _VALID_INPUT.items() if k != "entry_type"}
    result = validate_sizing_input(inp)
    assert result["blocked"] is True


def test_validate_sizing_input_missing_stop_distance_pct_returns_blocked():
    inp = {k: v for k, v in _VALID_INPUT.items() if k != "stop_distance_pct"}
    result = validate_sizing_input(inp)
    assert result["blocked"] is True


def test_validate_sizing_input_stop_distance_zero_returns_blocked():
    inp = {**_VALID_INPUT, "stop_distance_pct": 0}
    result = validate_sizing_input(inp)
    assert result["blocked"] is True


def test_validate_sizing_input_stop_distance_negative_returns_blocked():
    inp = {**_VALID_INPUT, "stop_distance_pct": -0.05}
    result = validate_sizing_input(inp)
    assert result["blocked"] is True


def test_validate_sizing_input_with_BUY_returns_blocked():
    inp = {**_VALID_INPUT, "action": "BUY"}
    result = validate_sizing_input(inp)
    assert result["blocked"] is True


def test_validate_sizing_input_valid_returns_allowed():
    result = validate_sizing_input(_VALID_INPUT)
    assert result["blocked"] is False


def test_compute_entry_size_multiplier_A_PULLBACK_10MA():
    assert compute_entry_size_multiplier("A_PULLBACK_10MA") == 1.0


def test_compute_entry_size_multiplier_B_BREAKOUT_BASE():
    assert compute_entry_size_multiplier("B_BREAKOUT_BASE") == 0.7


def test_compute_entry_size_multiplier_C_RECLAIM_20MA():
    assert compute_entry_size_multiplier("C_RECLAIM_20MA") == 0.5


def test_compute_entry_size_multiplier_TEST_POSITION():
    assert compute_entry_size_multiplier("TEST_POSITION") == 0.3


def test_compute_entry_size_multiplier_ADD_POSITION():
    assert compute_entry_size_multiplier("ADD_POSITION") == 0.5


def test_compute_entry_size_multiplier_REDUCE_POSITION():
    assert compute_entry_size_multiplier("REDUCE_POSITION") == 0.0


def test_compute_entry_size_multiplier_NO_ENTRY():
    assert compute_entry_size_multiplier("NO_ENTRY") == 0.0


def test_compute_entry_size_multiplier_UNKNOWN():
    assert compute_entry_size_multiplier("UNKNOWN") == 0.0


def test_compute_risk_grade_0_0_is_LOW():
    assert compute_risk_grade(0.0) == "LOW"


def test_compute_risk_grade_0_1_is_LOW():
    assert compute_risk_grade(0.1) == "LOW"


def test_compute_risk_grade_0_2_is_MODERATE():
    assert compute_risk_grade(0.2) == "MODERATE"


def test_compute_risk_grade_0_3_is_MODERATE():
    assert compute_risk_grade(0.3) == "MODERATE"


def test_compute_risk_grade_0_4_is_ELEVATED():
    assert compute_risk_grade(0.4) == "ELEVATED"


def test_compute_risk_grade_0_5_is_ELEVATED():
    assert compute_risk_grade(0.5) == "ELEVATED"


def test_compute_risk_grade_0_6_is_HIGH():
    assert compute_risk_grade(0.6) == "HIGH"


def test_compute_risk_grade_0_7_is_HIGH():
    assert compute_risk_grade(0.7) == "HIGH"


def test_compute_risk_grade_0_8_is_CRITICAL():
    assert compute_risk_grade(0.8) == "CRITICAL"


def test_compute_risk_grade_0_9_is_CRITICAL():
    assert compute_risk_grade(0.9) == "CRITICAL"


def test_compute_risk_grade_negative_is_INVALID():
    assert compute_risk_grade(-0.1) == "INVALID"


def test_compute_risk_grade_above_1_is_INVALID():
    assert compute_risk_grade(1.1) == "INVALID"


def test_compute_position_size_valid_returns_allowed():
    result = compute_position_size(300000, 0.01, 0.05, 1.0)
    assert result["allowed"] is True


def test_compute_position_size_adjusted_position_amount_gt_0():
    result = compute_position_size(300000, 0.01, 0.05, 1.0)
    assert result["adjusted_position_amount"] > 0


def test_compute_position_size_max_loss_amount():
    result = compute_position_size(300000, 0.01, 0.05, 1.0)
    assert result["max_loss_amount"] == 3000.0


def test_compute_position_size_risk_off_uses_lower_risk_pct():
    result_normal = compute_position_size(300000, 0.01, 0.05, 1.0)
    result_risk_off = compute_position_size(300000, 0.01, 0.05, 1.0, risk_off=True)
    assert result_risk_off["adjusted_position_amount"] <= result_normal["adjusted_position_amount"]


def test_compute_position_size_stop_distance_zero_returns_blocked():
    result = compute_position_size(300000, 0.01, 0.0, 1.0)
    assert result["blocked"] is True


def test_check_cash_buffer_very_low_returns_block_new_entry():
    result = check_cash_buffer(0.01)
    assert result["block_new_entry"] is True


def test_check_cash_buffer_adequate_returns_cash_buffer_ok():
    result = check_cash_buffer(0.20)
    assert result["cash_buffer_ok"] is True


def test_check_cash_buffer_weak_market_below_threshold_returns_block():
    result = check_cash_buffer(0.30, weak_market_mode=True)
    assert result["block_new_entry"] is True


def test_check_cash_buffer_weak_market_above_threshold_returns_ok():
    result = check_cash_buffer(0.60, weak_market_mode=True)
    assert result["cash_buffer_ok"] is True


def test_check_theme_exposure_exceeded():
    result = check_theme_exposure("AI", {"AI": 0.40}, 0.35)
    assert result["limit_exceeded"] is True


def test_check_theme_exposure_not_exceeded():
    result = check_theme_exposure("AI", {"AI": 0.20}, 0.35)
    assert result["limit_exceeded"] is False


def test_check_industry_exposure_exceeded():
    result = check_industry_exposure("semi", {"semi": 0.45}, 0.40)
    assert result["limit_exceeded"] is True


def test_check_industry_exposure_not_exceeded():
    result = check_industry_exposure("semi", {"semi": 0.20}, 0.40)
    assert result["limit_exceeded"] is False


def test_check_symbol_weight_exceeded():
    result = check_symbol_weight("2330", {"2330": 0.25}, 0.20)
    assert result["limit_exceeded"] is True


def test_check_symbol_weight_not_exceeded():
    result = check_symbol_weight("2330", {"2330": 0.10}, 0.20)
    assert result["limit_exceeded"] is False


def test_check_correlation_cluster_exceeded():
    result = check_correlation_cluster(0.50, 0.45)
    assert result["limit_exceeded"] is True


def test_check_correlation_cluster_not_exceeded():
    result = check_correlation_cluster(0.30, 0.45)
    assert result["limit_exceeded"] is False


def test_evaluate_no_entry_conditions_critical_grade_triggers_portfolio_risk_exceeded():
    inp = {"portfolio_risk_grade": "CRITICAL", "current_cash_pct": 0.20,
           "stop_distance_pct": 0.05, "market_risk_off": False,
           "theme_exposures": {}, "candidate_theme": ""}
    result = evaluate_no_entry_conditions(inp)
    triggered_names = [c["condition_name"] for c in result if c.get("triggered")]
    assert "portfolio_risk_exceeded" in triggered_names


def test_evaluate_no_entry_conditions_cash_too_low_triggers_cash_buffer_too_low():
    inp = {"portfolio_risk_grade": "LOW", "current_cash_pct": 0.01,
           "stop_distance_pct": 0.05, "market_risk_off": False,
           "theme_exposures": {}, "candidate_theme": ""}
    result = evaluate_no_entry_conditions(inp)
    triggered_names = [c["condition_name"] for c in result if c.get("triggered")]
    assert "cash_buffer_too_low" in triggered_names


def test_evaluate_no_entry_conditions_wide_stop_triggers_stop_distance_too_wide():
    inp = {"portfolio_risk_grade": "LOW", "current_cash_pct": 0.20,
           "stop_distance_pct": 0.20, "market_risk_off": False,
           "theme_exposures": {}, "candidate_theme": ""}
    result = evaluate_no_entry_conditions(inp)
    triggered_names = [c["condition_name"] for c in result if c.get("triggered")]
    assert "stop_distance_too_wide" in triggered_names


def test_evaluate_no_entry_conditions_market_risk_off_triggers():
    inp = {"portfolio_risk_grade": "LOW", "current_cash_pct": 0.60,
           "stop_distance_pct": 0.05, "market_risk_off": True,
           "theme_exposures": {}, "candidate_theme": ""}
    result = evaluate_no_entry_conditions(inp)
    triggered_names = [c["condition_name"] for c in result if c.get("triggered")]
    assert "market_risk_off_no_edge" in triggered_names


def test_evaluate_no_entry_conditions_theme_exceeded_triggers():
    inp = {"portfolio_risk_grade": "LOW", "current_cash_pct": 0.20,
           "stop_distance_pct": 0.05, "market_risk_off": False,
           "theme_exposures": {"AI": 0.50}, "candidate_theme": "AI"}
    result = evaluate_no_entry_conditions(inp)
    triggered_names = [c["condition_name"] for c in result if c.get("triggered")]
    assert "theme_exposure_exceeded" in triggered_names


def test_run_position_sizing_report_valid_A_returns_allowed():
    inp = {**_VALID_INPUT, "current_cash_pct": 0.20}
    result = run_position_sizing_report(inp)
    assert result["allowed"] is True


def test_run_position_sizing_report_valid_A_returns_ALLOW_NORMAL_SIZE():
    inp = {**_VALID_INPUT, "current_cash_pct": 0.20}
    result = run_position_sizing_report(inp)
    assert result["recommendation"] == "ALLOW_NORMAL_SIZE"


def test_run_position_sizing_report_valid_B_returns_allowed():
    inp = {**_VALID_INPUT, "entry_type": "B_BREAKOUT_BASE", "current_cash_pct": 0.20}
    result = run_position_sizing_report(inp)
    assert result["allowed"] is True


def test_run_position_sizing_report_valid_B_returns_ALLOW_REDUCED_SIZE():
    inp = {**_VALID_INPUT, "entry_type": "B_BREAKOUT_BASE", "current_cash_pct": 0.20}
    result = run_position_sizing_report(inp)
    assert result["recommendation"] == "ALLOW_REDUCED_SIZE"


def test_run_position_sizing_report_valid_C_returns_reduced_or_test():
    inp = {**_VALID_INPUT, "entry_type": "C_RECLAIM_20MA", "current_cash_pct": 0.20}
    result = run_position_sizing_report(inp)
    assert result["recommendation"] in ("ALLOW_REDUCED_SIZE", "TEST_POSITION_ONLY")


def test_run_position_sizing_report_critical_risk_returns_blocked():
    inp = {**_VALID_INPUT, "portfolio_risk_grade": "CRITICAL"}
    result = run_position_sizing_report(inp)
    assert result["allowed"] is False


def test_run_position_sizing_report_cash_too_low_returns_blocked():
    inp = {**_VALID_INPUT, "current_cash_pct": 0.01}
    result = run_position_sizing_report(inp)
    assert result["allowed"] is False


def test_run_position_sizing_report_sizing_executes_order_always_False():
    inp = {**_VALID_INPUT, "current_cash_pct": 0.20}
    result = run_position_sizing_report(inp)
    assert result["sizing_executes_order"] is False


def test_run_position_sizing_report_sizing_mutates_strategy_always_False():
    inp = {**_VALID_INPUT, "current_cash_pct": 0.20}
    result = run_position_sizing_report(inp)
    assert result["sizing_mutates_strategy"] is False
