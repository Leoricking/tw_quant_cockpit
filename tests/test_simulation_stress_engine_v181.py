"""
tests/test_simulation_stress_engine_v181.py
Tests for simulation_stress_engine_v181 — stress test engine.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import StressTestResult
from paper_trading.small_capital_strategy.simulation_stress_engine_v181 import (
    STRESS_TEST_TYPES, run_stress_test, run_all_stress_tests, get_stress_engine_info,
)

# ── STRESS_TEST_TYPES ──────────────────────────────────────────────────────────

def test_stress_test_types_is_list():
    assert isinstance(STRESS_TEST_TYPES, list)

def test_stress_test_types_ge_10():
    assert len(STRESS_TEST_TYPES) >= 10

def test_stress_test_types_ge_12():
    assert len(STRESS_TEST_TYPES) >= 12

def test_stress_types_contains_market_crash():
    assert "MARKET_CRASH" in STRESS_TEST_TYPES

def test_stress_types_contains_theme_collapse():
    assert "THEME_COLLAPSE" in STRESS_TEST_TYPES

def test_stress_types_contains_liquidity_shrink():
    assert "LIQUIDITY_SHRINK" in STRESS_TEST_TYPES

def test_stress_types_contains_volatility_spike():
    assert "VOLATILITY_SPIKE" in STRESS_TEST_TYPES

def test_stress_types_contains_losing_streak_3():
    assert "LOSING_STREAK_3" in STRESS_TEST_TYPES

def test_stress_types_contains_losing_streak_5():
    assert "LOSING_STREAK_5" in STRESS_TEST_TYPES

def test_stress_types_contains_losing_streak_8():
    assert "LOSING_STREAK_8" in STRESS_TEST_TYPES

def test_stress_types_contains_gap_down():
    assert "GAP_DOWN_STOP_LOSS" in STRESS_TEST_TYPES

def test_stress_types_contains_overtrading():
    assert "OVERTRADING_INJECTION" in STRESS_TEST_TYPES

def test_stress_types_contains_no_stop_loss():
    assert "NO_STOP_LOSS_INJECTION" in STRESS_TEST_TYPES

def test_stress_types_contains_oversized_position():
    assert "OVERSIZED_POSITION_INJECTION" in STRESS_TEST_TYPES

def test_stress_types_contains_risk_off():
    assert "RISK_OFF_REGIME_SHIFT" in STRESS_TEST_TYPES

def test_stress_types_all_strings():
    assert all(isinstance(t, str) for t in STRESS_TEST_TYPES)


# ── run_stress_test() — result structure ──────────────────────────────────────

def test_run_stress_test_returns_result():
    result = run_stress_test("MARKET_CRASH")
    assert isinstance(result, StressTestResult)

def test_run_stress_test_paper_only():
    assert run_stress_test("MARKET_CRASH").paper_only is True

def test_run_stress_test_research_only():
    assert run_stress_test("MARKET_CRASH").research_only is True

def test_run_stress_test_simulate_only():
    assert run_stress_test("MARKET_CRASH").simulate_only is True

def test_run_stress_test_stress_test_only():
    assert run_stress_test("MARKET_CRASH").stress_test_only is True

def test_run_stress_test_no_real_orders():
    assert run_stress_test("MARKET_CRASH").no_real_orders is True

def test_run_stress_test_not_investment_advice():
    assert run_stress_test("MARKET_CRASH").not_investment_advice is True

def test_run_stress_test_schema_version():
    assert run_stress_test("MARKET_CRASH").schema_version == "181"

def test_run_stress_test_shock_type_in_result():
    result = run_stress_test("MARKET_CRASH")
    assert result.shock_type == "MARKET_CRASH"

def test_run_stress_test_scenario_id_not_empty():
    result = run_stress_test("MARKET_CRASH")
    assert result.scenario_id != ""

def test_run_stress_test_custom_scenario_id():
    result = run_stress_test("MARKET_CRASH", scenario_id="MY-001")
    assert result.scenario_id == "MY-001"

def test_run_stress_test_final_capital_nonnegative():
    result = run_stress_test("MARKET_CRASH")
    assert result.final_capital >= 0.0

def test_run_stress_test_return_pct_is_negative():
    result = run_stress_test("MARKET_CRASH")
    assert result.total_return_pct < 0.0

def test_run_stress_test_drawdown_nonnegative():
    result = run_stress_test("MARKET_CRASH")
    assert result.max_drawdown_pct >= 0.0


# ── run_stress_test() — specific shock types ──────────────────────────────────

def test_market_crash_survived():
    result = run_stress_test("MARKET_CRASH")
    assert result.survived is True

def test_market_crash_return_minus_25():
    result = run_stress_test("MARKET_CRASH")
    assert result.total_return_pct == -25.0

def test_market_crash_drawdown_25():
    result = run_stress_test("MARKET_CRASH")
    assert result.max_drawdown_pct == 25.0

def test_market_crash_paper_only():
    assert run_stress_test("MARKET_CRASH").paper_only is True

def test_no_stop_loss_not_survived():
    result = run_stress_test("NO_STOP_LOSS_INJECTION")
    assert result.survived is False

def test_no_stop_loss_return_minus_12():
    result = run_stress_test("NO_STOP_LOSS_INJECTION")
    assert result.total_return_pct == -12.0

def test_liquidity_shrink_survived():
    result = run_stress_test("LIQUIDITY_SHRINK")
    assert result.survived is True

def test_losing_streak_3_survived():
    result = run_stress_test("LOSING_STREAK_3")
    assert result.survived is True

def test_losing_streak_8_survived_at_1pct_risk():
    # With 1% risk, 8 losses = 8% drawdown, final = 300000*0.92 > 300000*0.5
    result = run_stress_test("LOSING_STREAK_8", initial_capital=300000.0, risk_pct=1.0)
    assert result.survived is True

def test_risk_off_regime_survived():
    result = run_stress_test("RISK_OFF_REGIME_SHIFT")
    assert result.survived is True

def test_unknown_shock_type_blocked():
    result = run_stress_test("UNKNOWN_SHOCK_XYZ")
    assert result.action == "BLOCKED"

def test_unknown_shock_type_not_survived():
    result = run_stress_test("UNKNOWN_SHOCK_XYZ")
    assert result.survived is False

def test_theme_collapse_action_blocked():
    assert run_stress_test("THEME_COLLAPSE").action == "BLOCKED"

def test_gap_down_action_review_required():
    assert run_stress_test("GAP_DOWN_STOP_LOSS").action == "REVIEW_REQUIRED"

def test_overtrading_action_reduce_risk():
    assert run_stress_test("OVERTRADING_INJECTION").action == "REDUCE_RISK"

def test_volatility_spike_action_reduce_risk():
    assert run_stress_test("VOLATILITY_SPIKE").action == "REDUCE_RISK"

def test_losing_streak_3_action_review_required():
    assert run_stress_test("LOSING_STREAK_3").action == "REVIEW_REQUIRED"

def test_risk_off_action_blocked():
    assert run_stress_test("RISK_OFF_REGIME_SHIFT").action == "BLOCKED"

def test_liquidity_shrink_action_reduce_risk():
    assert run_stress_test("LIQUIDITY_SHRINK").action == "REDUCE_RISK"

def test_oversized_position_action_reduce_risk():
    assert run_stress_test("OVERSIZED_POSITION_INJECTION").action == "REDUCE_RISK"


# ── run_all_stress_tests() ────────────────────────────────────────────────────

def test_run_all_stress_tests_is_list():
    assert isinstance(run_all_stress_tests(), list)

def test_run_all_stress_tests_ge_10():
    assert len(run_all_stress_tests()) >= 10

def test_run_all_stress_tests_count_matches_types():
    assert len(run_all_stress_tests()) == len(STRESS_TEST_TYPES)

def test_run_all_stress_tests_all_results():
    results = run_all_stress_tests()
    assert all(isinstance(r, StressTestResult) for r in results)

def test_run_all_stress_tests_all_paper_only():
    results = run_all_stress_tests()
    assert all(r.paper_only is True for r in results)

def test_run_all_stress_tests_all_stress_test_only():
    results = run_all_stress_tests()
    assert all(r.stress_test_only is True for r in results)

def test_run_all_stress_tests_all_no_real_orders():
    results = run_all_stress_tests()
    assert all(r.no_real_orders is True for r in results)

def test_run_all_stress_tests_all_have_scenario_id():
    results = run_all_stress_tests()
    assert all(r.scenario_id != "" for r in results)

def test_run_all_stress_tests_all_have_shock_type():
    results = run_all_stress_tests()
    assert all(r.shock_type in STRESS_TEST_TYPES for r in results)

def test_run_all_stress_tests_no_stop_loss_in_results():
    results = run_all_stress_tests()
    no_stop = [r for r in results if r.shock_type == "NO_STOP_LOSS_INJECTION"]
    assert len(no_stop) == 1
    assert no_stop[0].survived is False

def test_run_all_stress_tests_some_survive():
    results = run_all_stress_tests()
    survived = [r for r in results if r.survived]
    assert len(survived) >= 5


# ── get_stress_engine_info() ──────────────────────────────────────────────────

def test_stress_engine_info_is_dict():
    assert isinstance(get_stress_engine_info(), dict)

def test_stress_engine_info_paper_only():
    assert get_stress_engine_info()["paper_only"] is True

def test_stress_engine_info_research_only():
    assert get_stress_engine_info()["research_only"] is True

def test_stress_engine_info_stress_test_only():
    assert get_stress_engine_info()["stress_test_only"] is True

def test_stress_engine_info_no_real_orders():
    assert get_stress_engine_info()["no_real_orders"] is True

def test_stress_engine_info_production_blocked():
    assert get_stress_engine_info()["production_trading_blocked"] is True

def test_stress_engine_info_schema():
    assert get_stress_engine_info()["schema"] == "181"

def test_stress_engine_info_count():
    info = get_stress_engine_info()
    assert info["stress_test_count"] >= 10

def test_stress_engine_info_types_list():
    info = get_stress_engine_info()
    assert isinstance(info["stress_test_types"], list)
    assert "MARKET_CRASH" in info["stress_test_types"]
