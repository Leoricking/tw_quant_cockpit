"""
tests/test_optimization_engine_v182.py
Tests for optimization engine v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.optimization_engine_v182 import (
    ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
    validate_action, validate_grade, run_parameter_search, rank_parameter_sets,
    compute_stability_score, get_engine_info,
)
from paper_trading.small_capital_strategy.optimization_models_v182 import (
    ParameterGrid, OptimizationConfig, ParameterSet, ParameterSearchResult,
    ParameterRanking, StabilityScore,
)


# --- ALLOWED_OUTPUT_ACTIONS ---
def test_allowed_actions_count_14():
    assert len(ALLOWED_OUTPUT_ACTIONS) == 14

def test_allowed_actions_frozenset():
    assert isinstance(ALLOWED_OUTPUT_ACTIONS, frozenset)

def test_allowed_actions_observe():
    assert "OBSERVE" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_wait():
    assert "WAIT" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_paper_plan_ready():
    assert "PAPER_PLAN_READY" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_paper_entry_allowed():
    assert "PAPER_ENTRY_ALLOWED" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_paper_add_allowed():
    assert "PAPER_ADD_ALLOWED" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_reduce_risk():
    assert "REDUCE_RISK" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_review_required():
    assert "REVIEW_REQUIRED" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_blocked():
    assert "BLOCKED" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_no_trade():
    assert "NO_TRADE" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_research_only():
    assert "RESEARCH_ONLY" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_read_report():
    assert "READ_REPORT" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_simulate_only():
    assert "SIMULATE_ONLY" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_stress_test_only():
    assert "STRESS_TEST_ONLY" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_actions_validation_only():
    assert "VALIDATION_ONLY" in ALLOWED_OUTPUT_ACTIONS


# --- FORBIDDEN_OUTPUT_WORDS ---
def test_forbidden_words_count_9():
    assert len(FORBIDDEN_OUTPUT_WORDS) == 9

def test_forbidden_words_frozenset():
    assert isinstance(FORBIDDEN_OUTPUT_WORDS, frozenset)

def test_forbidden_buy():
    assert "BUY" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_sell():
    assert "SELL" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_order():
    assert "ORDER" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_execute():
    assert "EXECUTE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_submit_order():
    assert "SUBMIT_ORDER" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_auto_trade():
    assert "AUTO_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_real_trade():
    assert "REAL_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_live_trade():
    assert "LIVE_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_broker_order():
    assert "BROKER_ORDER" in FORBIDDEN_OUTPUT_WORDS


# --- VALID_FINAL_GRADES ---
def test_valid_grades_count_5():
    assert len(VALID_FINAL_GRADES) == 5

def test_valid_grades_frozenset():
    assert isinstance(VALID_FINAL_GRADES, frozenset)

def test_valid_grades_robust():
    assert "ROBUST" in VALID_FINAL_GRADES

def test_valid_grades_acceptable():
    assert "ACCEPTABLE" in VALID_FINAL_GRADES

def test_valid_grades_unstable():
    assert "UNSTABLE" in VALID_FINAL_GRADES

def test_valid_grades_overfitted():
    assert "OVERFITTED" in VALID_FINAL_GRADES

def test_valid_grades_blocked():
    assert "BLOCKED" in VALID_FINAL_GRADES


# --- validate_action ---
def test_validate_action_blocked():
    assert validate_action("BLOCKED") is True

def test_validate_action_paper_entry():
    assert validate_action("PAPER_ENTRY_ALLOWED") is True

def test_validate_action_validation_only():
    assert validate_action("VALIDATION_ONLY") is True

def test_validate_action_invalid():
    assert validate_action("BUY") is False

def test_validate_action_empty():
    assert validate_action("") is False


# --- validate_grade ---
def test_validate_grade_robust():
    assert validate_grade("ROBUST") is True

def test_validate_grade_blocked():
    assert validate_grade("BLOCKED") is True

def test_validate_grade_invalid():
    assert validate_grade("EXCELLENT") is False


# --- run_parameter_search ---
def test_search_returns_result():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    assert isinstance(result, ParameterSearchResult)

def test_search_total_gt_0():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    assert result.total_parameter_sets > 0

def test_search_valid_gt_0():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    assert result.valid_parameter_sets > 0

def test_search_sets_list():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    assert isinstance(result.parameter_sets, list)
    assert len(result.parameter_sets) > 0

def test_search_paper_only():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    assert result.paper_only is True

def test_search_mode():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    assert result.search_mode == "GRID_SEARCH"

def test_search_best_id_not_empty():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    assert result.best_parameter_set_id != ""

def test_search_valid_plus_blocked_eq_total():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    assert result.valid_parameter_sets + result.blocked_parameter_sets == result.total_parameter_sets


# --- rank_parameter_sets ---
def test_ranking_returns_list():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    rankings = rank_parameter_sets(result)
    assert isinstance(rankings, list)

def test_ranking_items_type():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    rankings = rank_parameter_sets(result)
    assert len(rankings) > 0
    assert isinstance(rankings[0], ParameterRanking)

def test_ranking_first_rank_is_1():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    rankings = rank_parameter_sets(result)
    assert rankings[0].rank == 1

def test_ranking_grades_valid():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    rankings = rank_parameter_sets(result)
    for r in rankings:
        assert r.final_grade in VALID_FINAL_GRADES

def test_ranking_paper_only():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    rankings = rank_parameter_sets(result)
    for r in rankings:
        assert r.paper_only is True


# --- compute_stability_score ---
def test_stability_returns_model():
    ps = ParameterSet(win_rate_pct=58.0, profit_factor=1.8, single_trade_risk_pct=1.0, max_drawdown_pct=5.0)
    result = compute_stability_score(ps)
    assert isinstance(result, StabilityScore)

def test_stability_score_range():
    ps = ParameterSet(win_rate_pct=58.0, profit_factor=1.8, single_trade_risk_pct=1.0, max_drawdown_pct=5.0)
    result = compute_stability_score(ps)
    assert 0 <= result.score <= 100.0

def test_stability_paper_only():
    ps = ParameterSet(win_rate_pct=58.0, profit_factor=1.8, single_trade_risk_pct=1.0, max_drawdown_pct=5.0)
    result = compute_stability_score(ps)
    assert result.paper_only is True

def test_stability_grade_valid():
    ps = ParameterSet(win_rate_pct=58.0, profit_factor=1.8, single_trade_risk_pct=1.0, max_drawdown_pct=5.0)
    result = compute_stability_score(ps)
    assert result.stability_grade in ("STABLE", "ACCEPTABLE", "UNSTABLE", "BLOCKED")


# --- get_engine_info ---
def test_engine_info_returns_dict():
    assert isinstance(get_engine_info(), dict)

def test_engine_info_version():
    assert get_engine_info()["version"] == "1.8.2"

def test_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True

def test_engine_info_validation_only():
    assert get_engine_info()["validation_only"] is True

def test_engine_info_no_real_orders():
    assert get_engine_info()["no_real_orders"] is True

def test_engine_info_schema_version():
    assert get_engine_info()["schema_version"] == "182"

def test_engine_info_actions_count():
    assert len(get_engine_info()["allowed_output_actions"]) == 14

def test_engine_info_forbidden_count():
    assert len(get_engine_info()["forbidden_output_words"]) == 9

def test_engine_info_grades_count():
    assert len(get_engine_info()["valid_final_grades"]) == 5

def test_no_forbidden_in_allowed():
    for word in FORBIDDEN_OUTPUT_WORDS:
        assert word not in ALLOWED_OUTPUT_ACTIONS
