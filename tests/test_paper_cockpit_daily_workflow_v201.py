"""
tests/test_paper_cockpit_daily_workflow_v201.py
v2.0.1 Paper Cockpit — Daily Workflow Tests (50+ tests)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
    DailyWorkflowInput, DailyWorkflowResult, DailyWorkflowCandidateResult,
    DailyWorkflowSummary, CandidateRankEntry,
    run_daily_workflow, classify_final_action, build_candidate_ranking,
    DAILY_FINAL_ACTIONS,
)


# --- DailyWorkflowInput tests ---

def test_daily_workflow_input_schema():
    inp = DailyWorkflowInput()
    assert inp.schema_version == "201"

def test_daily_workflow_input_paper_only():
    inp = DailyWorkflowInput()
    assert inp.paper_only is True

def test_daily_workflow_input_no_real_orders():
    inp = DailyWorkflowInput()
    assert inp.no_real_orders is True

def test_daily_workflow_input_human_review():
    inp = DailyWorkflowInput()
    assert inp.human_review_required is True

def test_daily_workflow_input_default_capital():
    inp = DailyWorkflowInput()
    assert inp.capital_twd == 300000.0

def test_daily_workflow_input_default_regime():
    inp = DailyWorkflowInput()
    assert inp.market_regime == "BULL"

def test_daily_workflow_input_custom():
    inp = DailyWorkflowInput(candidates=["2330", "2454"], market_regime="BEAR")
    assert inp.candidates == ["2330", "2454"]
    assert inp.market_regime == "BEAR"

def test_daily_workflow_input_risk_budget_remaining():
    inp = DailyWorkflowInput(risk_budget_remaining_pct=50.0)
    assert inp.risk_budget_remaining_pct == 50.0


# --- run_daily_workflow tests ---

def test_run_daily_workflow_no_args():
    result = run_daily_workflow()
    assert isinstance(result, DailyWorkflowResult)

def test_run_daily_workflow_empty_candidates():
    inp = DailyWorkflowInput(candidates=[])
    result = run_daily_workflow(inp)
    assert result.candidate_results == []
    assert result.summary.total_candidates == 0

def test_run_daily_workflow_single_candidate():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    assert len(result.candidate_results) == 1

def test_run_daily_workflow_multiple_candidates():
    inp = DailyWorkflowInput(candidates=["2330", "2454", "2317"])
    result = run_daily_workflow(inp)
    assert len(result.candidate_results) == 3

def test_run_daily_workflow_result_paper_only():
    result = run_daily_workflow()
    assert result.paper_only is True

def test_run_daily_workflow_result_no_real_orders():
    result = run_daily_workflow()
    assert result.no_real_orders is True

def test_run_daily_workflow_result_no_broker():
    result = run_daily_workflow()
    assert result.no_broker is True

def test_run_daily_workflow_cockpit_executes_order_false():
    result = run_daily_workflow()
    assert result.cockpit_executes_order is False

def test_run_daily_workflow_human_review_required():
    result = run_daily_workflow()
    assert result.human_review_required is True

def test_run_daily_workflow_version():
    result = run_daily_workflow()
    assert result.version == "2.0.1"

def test_run_daily_workflow_schema_version():
    result = run_daily_workflow()
    assert result.schema_version == "201"

def test_run_daily_workflow_summary_not_none():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    assert result.summary is not None

def test_run_daily_workflow_cli_display_not_none():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    assert result.cli_display is not None

def test_run_daily_workflow_candidate_ranking():
    inp = DailyWorkflowInput(candidates=["2330", "2454"])
    result = run_daily_workflow(inp)
    assert len(result.candidate_ranking) == 2

def test_run_daily_workflow_regime_bull():
    inp = DailyWorkflowInput(candidates=["2330"], market_regime="BULL")
    result = run_daily_workflow(inp)
    assert result.market_regime == "BULL"

def test_run_daily_workflow_regime_bear():
    inp = DailyWorkflowInput(candidates=["2330"], market_regime="BEAR")
    result = run_daily_workflow(inp)
    assert result.market_regime == "BEAR"

def test_run_daily_workflow_candidate_result_symbol():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    assert result.candidate_results[0].symbol == "2330"

def test_run_daily_workflow_candidate_final_action_valid():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    assert result.candidate_results[0].final_action in DAILY_FINAL_ACTIONS

def test_run_daily_workflow_candidate_human_review():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    assert result.candidate_results[0].human_review_requirement is True

def test_run_daily_workflow_watchlist_summary_populated():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    assert result.candidate_results[0].watchlist_summary != ""

def test_run_daily_workflow_candidate_rank_assigned():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    assert result.candidate_results[0].candidate_rank == 1

def test_run_daily_workflow_with_candidate_data():
    inp = DailyWorkflowInput(candidates=["2330"])
    cdata = {
        "2330": {
            "abc_type": "A_PULLBACK_10MA",
            "stop_distance_pct": 0.08,
            "entry_price": 920.0,
        }
    }
    result = run_daily_workflow(inp, cdata)
    assert result.candidate_results[0].abc_type == "A_PULLBACK_10MA"


# --- WAIT action ---

def test_classify_final_action_wait_no_position():
    action = classify_final_action("2330", "NO_ENTRY", [], True, True, has_position=False)
    assert action == "WAIT"

def test_classify_final_action_no_entry_blocking_reasons():
    action = classify_final_action("2330", "NO_ENTRY", ["trend_broken"], True, True)
    assert action == "NO_ENTRY"

def test_classify_final_action_no_entry_risk_not_ok():
    action = classify_final_action("2330", "A_PULLBACK_10MA", [], False, True)
    assert action == "NO_ENTRY"

def test_classify_final_action_no_entry_sizing_not_ok():
    action = classify_final_action("2330", "A_PULLBACK_10MA", [], True, False)
    assert action == "NO_ENTRY"


# --- PAPER_BUY_PLAN action ---

def test_classify_final_action_paper_buy_plan():
    action = classify_final_action("2330", "A_PULLBACK_10MA", [], True, True, has_position=False)
    assert action == "PAPER_BUY_PLAN"

def test_classify_final_action_paper_buy_plan_b_breakout():
    action = classify_final_action("2330", "B_BREAKOUT_BASE", [], True, True, has_position=False)
    assert action == "PAPER_BUY_PLAN"

def test_classify_final_action_paper_buy_plan_c_reclaim():
    action = classify_final_action("2330", "C_RECLAIM_20MA", [], True, True, has_position=False)
    assert action == "PAPER_BUY_PLAN"


# --- PAPER_ADD_PLAN action ---

def test_classify_final_action_paper_add_plan():
    action = classify_final_action("2330", "A_PULLBACK_10MA", [], True, True, has_position=True)
    assert action == "PAPER_ADD_PLAN"


# --- WATCH action ---

def test_classify_final_action_watch():
    action = classify_final_action("2330", "NO_ENTRY", [], True, True, has_position=True, position_profit_pct=0.10)
    assert action == "WATCH"


# --- PAPER_REDUCE_PLAN action ---

def test_classify_final_action_paper_reduce_plan():
    action = classify_final_action("2330", "NO_ENTRY", [], True, True, has_position=True, position_profit_pct=0.30)
    assert action == "PAPER_REDUCE_PLAN"


# --- PAPER_EXIT_PLAN action ---

def test_classify_final_action_paper_exit_plan():
    action = classify_final_action("2330", "NO_ENTRY", [], True, True, has_position=True, position_profit_pct=-0.10)
    assert action == "PAPER_EXIT_PLAN"


# --- Candidate ranking tests ---

def test_build_candidate_ranking_empty():
    ranking = build_candidate_ranking([])
    assert ranking == []

def test_build_candidate_ranking_sorted_descending():
    candidates = [
        {"symbol": "A", "total_score": 70.0, "final_action": "WAIT"},
        {"symbol": "B", "total_score": 90.0, "final_action": "PAPER_BUY_PLAN"},
        {"symbol": "C", "total_score": 50.0, "final_action": "NO_ENTRY"},
    ]
    ranking = build_candidate_ranking(candidates)
    assert ranking[0].symbol == "B"
    assert ranking[1].symbol == "A"
    assert ranking[2].symbol == "C"

def test_build_candidate_ranking_rank_numbers():
    candidates = [
        {"symbol": "A", "total_score": 90.0},
        {"symbol": "B", "total_score": 70.0},
    ]
    ranking = build_candidate_ranking(candidates)
    assert ranking[0].rank == 1
    assert ranking[1].rank == 2

def test_build_candidate_ranking_schema_version():
    candidates = [{"symbol": "A", "total_score": 90.0}]
    ranking = build_candidate_ranking(candidates)
    assert ranking[0].schema_version == "201"

def test_build_candidate_ranking_paper_only():
    candidates = [{"symbol": "A", "total_score": 90.0}]
    ranking = build_candidate_ranking(candidates)
    assert ranking[0].paper_only is True


# --- Summary tests ---

def test_daily_workflow_summary_total_candidates():
    inp = DailyWorkflowInput(candidates=["2330", "2454"])
    result = run_daily_workflow(inp)
    assert result.summary.total_candidates == 2

def test_daily_workflow_summary_schema_version():
    result = run_daily_workflow()
    assert result.summary.schema_version == "201"

def test_daily_workflow_summary_all_counts_sum():
    inp = DailyWorkflowInput(candidates=["2330", "2454", "2317"])
    result = run_daily_workflow(inp)
    s = result.summary
    total = (s.watch_count + s.wait_count + s.paper_buy_plan_count +
             s.paper_add_plan_count + s.paper_reduce_plan_count +
             s.paper_exit_plan_count + s.no_entry_count)
    assert total == s.total_candidates
