"""
tests/test_simulation_matrix_engine_v181.py
Tests for simulation_matrix_engine_v181 — matrix cell engine, validate_action, metrics.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import (
    SimulationMatrixInput, SimulationMatrixCell, SimulationMatrixResult,
    RobustnessScore,
)
from paper_trading.small_capital_strategy.simulation_matrix_engine_v181 import (
    ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
    run_matrix_cell, run_scenario_matrix, compute_robustness_score,
    validate_action, get_engine_info,
)


# ── Constants ──────────────────────────────────────────────────────────────────

def test_allowed_actions_is_frozenset():
    assert isinstance(ALLOWED_OUTPUT_ACTIONS, frozenset)

def test_allowed_actions_ge_13():
    assert len(ALLOWED_OUTPUT_ACTIONS) >= 13

def test_allowed_actions_no_buy():
    assert "BUY" not in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_no_sell():
    assert "SELL" not in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_no_order():
    assert "ORDER" not in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_contains_observe():
    assert "OBSERVE" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_contains_wait():
    assert "WAIT" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_contains_blocked():
    assert "BLOCKED" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_contains_paper_entry():
    assert "PAPER_ENTRY_ALLOWED" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_contains_stress_test_only():
    assert "STRESS_TEST_ONLY" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_contains_reduce_risk():
    assert "REDUCE_RISK" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_contains_review_required():
    assert "REVIEW_REQUIRED" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_contains_paper_plan_ready():
    assert "PAPER_PLAN_READY" in ALLOWED_OUTPUT_ACTIONS

def test_forbidden_words_is_frozenset():
    assert isinstance(FORBIDDEN_OUTPUT_WORDS, frozenset)

def test_forbidden_words_contains_buy():
    assert "BUY" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_words_contains_sell():
    assert "SELL" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_words_contains_execute():
    assert "EXECUTE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_words_contains_order():
    assert "ORDER" in FORBIDDEN_OUTPUT_WORDS

def test_valid_final_grades_count():
    assert len(VALID_FINAL_GRADES) == 5

def test_valid_final_grades_contains_robust():
    assert "ROBUST" in VALID_FINAL_GRADES

def test_valid_final_grades_contains_acceptable():
    assert "ACCEPTABLE" in VALID_FINAL_GRADES

def test_valid_final_grades_contains_fragile():
    assert "FRAGILE" in VALID_FINAL_GRADES

def test_valid_final_grades_contains_dangerous():
    assert "DANGEROUS" in VALID_FINAL_GRADES

def test_valid_final_grades_contains_blocked():
    assert "BLOCKED" in VALID_FINAL_GRADES


# ── validate_action() ──────────────────────────────────────────────────────────

def test_validate_paper_entry_allowed():
    assert validate_action("PAPER_ENTRY_ALLOWED") is True

def test_validate_observe():
    assert validate_action("OBSERVE") is True

def test_validate_wait():
    assert validate_action("WAIT") is True

def test_validate_blocked():
    assert validate_action("BLOCKED") is True

def test_validate_reduce_risk():
    assert validate_action("REDUCE_RISK") is True

def test_validate_stress_test_only():
    assert validate_action("STRESS_TEST_ONLY") is True

def test_validate_buy_rejected():
    assert validate_action("BUY") is False

def test_validate_sell_rejected():
    assert validate_action("SELL") is False

def test_validate_unknown_rejected():
    assert validate_action("UNKNOWN_ACTION_XYZ") is False

def test_validate_empty_rejected():
    assert validate_action("") is False


# ── run_matrix_cell() — default BULL entry ────────────────────────────────────

def test_run_cell_returns_matrix_cell():
    inp = SimulationMatrixInput()
    assert isinstance(run_matrix_cell(inp), SimulationMatrixCell)

def test_run_cell_paper_only():
    assert run_matrix_cell(SimulationMatrixInput()).paper_only is True

def test_run_cell_research_only():
    assert run_matrix_cell(SimulationMatrixInput()).research_only is True

def test_run_cell_simulate_only():
    assert run_matrix_cell(SimulationMatrixInput()).simulate_only is True

def test_run_cell_no_real_orders():
    assert run_matrix_cell(SimulationMatrixInput()).no_real_orders is True

def test_run_cell_action_in_allowed():
    cell = run_matrix_cell(SimulationMatrixInput())
    assert cell.action in ALLOWED_OUTPUT_ACTIONS

def test_run_cell_action_no_forbidden_words():
    cell = run_matrix_cell(SimulationMatrixInput())
    for w in FORBIDDEN_OUTPUT_WORDS:
        assert w not in cell.action

def test_run_cell_default_action_paper_entry():
    inp = SimulationMatrixInput()
    cell = run_matrix_cell(inp)
    assert cell.action == "PAPER_ENTRY_ALLOWED"

def test_run_cell_cell_id_not_empty():
    cell = run_matrix_cell(SimulationMatrixInput())
    assert cell.cell_id != ""

def test_run_cell_cell_id_starts_with_cell181():
    cell = run_matrix_cell(SimulationMatrixInput())
    assert cell.cell_id.startswith("CELL181")

def test_run_cell_schema_version():
    assert run_matrix_cell(SimulationMatrixInput()).schema_version == "181"

def test_run_cell_final_grade_in_valid():
    cell = run_matrix_cell(SimulationMatrixInput())
    assert cell.final_grade in VALID_FINAL_GRADES

def test_run_cell_input_params_dict():
    cell = run_matrix_cell(SimulationMatrixInput())
    assert isinstance(cell.input_params, dict)

def test_run_cell_win_rate_between_0_and_100():
    cell = run_matrix_cell(SimulationMatrixInput())
    assert 0.0 <= cell.win_rate_pct <= 100.0

def test_run_cell_max_drawdown_nonnegative():
    cell = run_matrix_cell(SimulationMatrixInput())
    assert cell.max_drawdown_pct >= 0.0


# ── run_matrix_cell() — BLOCKED scenarios ─────────────────────────────────────

def test_cell_blocked_by_risk_off():
    inp = SimulationMatrixInput(market_regime="RISK_OFF")
    assert run_matrix_cell(inp).action == "BLOCKED"

def test_cell_blocked_by_excluded_theme():
    inp = SimulationMatrixInput(theme_rank="EXCLUDED")
    assert run_matrix_cell(inp).action == "BLOCKED"

def test_cell_blocked_by_excluded_watchlist():
    inp = SimulationMatrixInput(watchlist_rank="EXCLUDED")
    assert run_matrix_cell(inp).action == "BLOCKED"

def test_cell_blocked_by_abc_blocked():
    inp = SimulationMatrixInput(abc_signal="BLOCKED")
    assert run_matrix_cell(inp).action == "BLOCKED"

def test_cell_blocked_by_behavior_blocked():
    inp = SimulationMatrixInput(behavior_risk="BLOCKED")
    assert run_matrix_cell(inp).action == "BLOCKED"

def test_cell_blocked_by_risk_dashboard_blocked():
    inp = SimulationMatrixInput(risk_dashboard="BLOCKED")
    assert run_matrix_cell(inp).action == "BLOCKED"

def test_cell_blocked_by_no_stop_loss():
    inp = SimulationMatrixInput(mistake_injection="NO_STOP_LOSS")
    assert run_matrix_cell(inp).action == "BLOCKED"

def test_cell_blocked_is_blocked_flag():
    inp = SimulationMatrixInput(market_regime="RISK_OFF")
    assert run_matrix_cell(inp).is_blocked is True

def test_cell_not_blocked_default():
    assert run_matrix_cell(SimulationMatrixInput()).is_blocked is False


# ── run_matrix_cell() — downgrade scenarios ───────────────────────────────────

def test_cell_reduce_risk_oversized():
    inp = SimulationMatrixInput(mistake_injection="OVERSIZED_POSITION")
    assert run_matrix_cell(inp).action == "REDUCE_RISK"

def test_cell_reduce_risk_overtrading():
    inp = SimulationMatrixInput(mistake_injection="OVERTRADING")
    assert run_matrix_cell(inp).action == "REDUCE_RISK"

def test_cell_reduce_risk_moved_stop():
    inp = SimulationMatrixInput(mistake_injection="MOVED_STOP_LOSS")
    assert run_matrix_cell(inp).action == "REDUCE_RISK"

def test_cell_review_required_revenge():
    inp = SimulationMatrixInput(mistake_injection="REVENGE_TRADE")
    assert run_matrix_cell(inp).action == "REVIEW_REQUIRED"

def test_cell_review_required_behavior_warning():
    inp = SimulationMatrixInput(behavior_risk="WARNING")
    assert run_matrix_cell(inp).action == "REVIEW_REQUIRED"

def test_cell_review_required_risk_dashboard_warning():
    inp = SimulationMatrixInput(risk_dashboard="WARNING")
    assert run_matrix_cell(inp).action == "REVIEW_REQUIRED"

def test_cell_wait_behavior_watch():
    inp = SimulationMatrixInput(behavior_risk="WATCH")
    assert run_matrix_cell(inp).action == "WAIT"

def test_cell_wait_not_ready():
    inp = SimulationMatrixInput(abc_signal="NOT_READY")
    assert run_matrix_cell(inp).action == "WAIT"

def test_cell_wait_weak_theme():
    inp = SimulationMatrixInput(theme_rank="WEAK")
    assert run_matrix_cell(inp).action == "WAIT"

def test_cell_observe_bear():
    inp = SimulationMatrixInput(market_regime="BEAR")
    assert run_matrix_cell(inp).action == "OBSERVE"

def test_cell_observe_unknown():
    inp = SimulationMatrixInput(market_regime="UNKNOWN")
    assert run_matrix_cell(inp).action == "OBSERVE"

def test_cell_plan_ready_range():
    inp = SimulationMatrixInput(market_regime="RANGE", abc_signal="A")
    assert run_matrix_cell(inp).action == "PAPER_PLAN_READY"


# ── run_scenario_matrix() ──────────────────────────────────────────────────────

def test_run_scenario_matrix_returns_result():
    scenarios = [SimulationMatrixInput()]
    result = run_scenario_matrix(scenarios)
    assert isinstance(result, SimulationMatrixResult)

def test_run_scenario_matrix_scenario_count():
    scenarios = [SimulationMatrixInput(), SimulationMatrixInput(market_regime="BEAR")]
    result = run_scenario_matrix(scenarios)
    assert result.scenario_count == 2

def test_run_scenario_matrix_paper_only():
    result = run_scenario_matrix([SimulationMatrixInput()])
    assert result.paper_only is True

def test_run_scenario_matrix_no_real_orders():
    result = run_scenario_matrix([SimulationMatrixInput()])
    assert result.no_real_orders is True

def test_run_scenario_matrix_final_grade_in_valid():
    result = run_scenario_matrix([SimulationMatrixInput()])
    assert result.final_grade in VALID_FINAL_GRADES

def test_run_scenario_matrix_cells_match_input():
    scenarios = [SimulationMatrixInput() for _ in range(3)]
    result = run_scenario_matrix(scenarios)
    assert len(result.cells) == 3


# ── compute_robustness_score() ────────────────────────────────────────────────

def test_compute_robustness_score_returns_robustness():
    matrix_result = run_scenario_matrix([SimulationMatrixInput()])
    score = compute_robustness_score(matrix_result)
    assert isinstance(score, RobustnessScore)

def test_compute_robustness_score_in_range():
    matrix_result = run_scenario_matrix([SimulationMatrixInput()])
    score = compute_robustness_score(matrix_result)
    assert 0.0 <= score.score <= 100.0

def test_compute_robustness_score_final_grade_valid():
    matrix_result = run_scenario_matrix([SimulationMatrixInput()])
    score = compute_robustness_score(matrix_result)
    assert score.final_grade in VALID_FINAL_GRADES

def test_compute_robustness_score_paper_only():
    matrix_result = run_scenario_matrix([SimulationMatrixInput()])
    score = compute_robustness_score(matrix_result)
    assert score.paper_only is True

def test_compute_robustness_score_with_stress_results():
    from paper_trading.small_capital_strategy.simulation_stress_engine_v181 import run_all_stress_tests
    matrix_result = run_scenario_matrix([SimulationMatrixInput()])
    stress = run_all_stress_tests()
    score = compute_robustness_score(matrix_result, stress)
    assert isinstance(score, RobustnessScore)


# ── get_engine_info() ──────────────────────────────────────────────────────────

def test_get_engine_info_is_dict():
    assert isinstance(get_engine_info(), dict)

def test_get_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True

def test_get_engine_info_no_real_orders():
    assert get_engine_info()["no_real_orders"] is True

def test_get_engine_info_production_blocked():
    assert get_engine_info()["production_trading_blocked"] is True

def test_get_engine_info_schema():
    assert get_engine_info()["schema"] == "181"

def test_get_engine_info_allowed_actions():
    info = get_engine_info()
    assert "PAPER_ENTRY_ALLOWED" in info["allowed_output_actions"]

def test_get_engine_info_forbidden_words():
    info = get_engine_info()
    assert "BUY" in info["forbidden_output_words"]
