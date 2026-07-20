"""
tests/test_paper_cockpit_batch_comparison_v203.py
v2.0.3 Batch Comparison & Simulation Ranking Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# BatchComparison model
# ---------------------------------------------------------------------------

def test_batch_comparison_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert obj is not None

def test_batch_comparison_has_strategy_profile_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "strategy_profile_id")

def test_batch_comparison_has_total_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "total_candidates")

def test_batch_comparison_has_allowed_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "allowed_count")

def test_batch_comparison_has_blocked_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "blocked_count")

def test_batch_comparison_has_paper_buy_plan_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "paper_buy_plan_count")

def test_batch_comparison_has_paper_add_plan_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "paper_add_plan_count")

def test_batch_comparison_has_reduce_plan_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "reduce_plan_count")

def test_batch_comparison_has_exit_plan_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "exit_plan_count")

def test_batch_comparison_has_no_entry_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "no_entry_count")

def test_batch_comparison_has_avg_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "avg_score")

def test_batch_comparison_has_avg_risk_used():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "avg_risk_used")

def test_batch_comparison_has_human_review_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "human_review_count")

def test_batch_comparison_has_top_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "top_candidates")

def test_batch_comparison_has_worst_blocked_reasons():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "worst_blocked_reasons")

def test_batch_comparison_has_simulation_quality_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert hasattr(obj, "simulation_quality_score")

def test_batch_comparison_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert obj.paper_only is True

def test_batch_comparison_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchComparison
    obj = BatchComparison()
    assert obj.no_real_orders is True

# ---------------------------------------------------------------------------
# build_batch_comparison function
# ---------------------------------------------------------------------------

def test_build_batch_comparison_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison
    result = build_batch_comparison(simulate_one(), "P001")
    assert result is not None

def test_build_batch_comparison_profile_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison
    result = build_batch_comparison(simulate_one(), "P001")
    assert result.strategy_profile_id == "P001"

def test_build_batch_comparison_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison
    result = build_batch_comparison(simulate_one(), "P001")
    assert result.paper_only is True

def test_build_batch_comparison_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison
    result = build_batch_comparison(simulate_one(), "P001")
    assert result.no_real_orders is True

def test_build_batch_comparison_quality_score_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison
    result = build_batch_comparison(simulate_one(), "P001")
    assert isinstance(result.simulation_quality_score, (int, float))

def test_build_batch_comparison_different_profiles():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison
    r1 = build_batch_comparison(simulate_one(), "P001")
    r2 = build_batch_comparison(simulate_one(), "P002")
    assert r1.strategy_profile_id == "P001"
    assert r2.strategy_profile_id == "P002"

# ---------------------------------------------------------------------------
# BATCH_COMPARISON_FIELDS constant
# ---------------------------------------------------------------------------

def test_batch_comparison_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BATCH_COMPARISON_FIELDS
    assert len(BATCH_COMPARISON_FIELDS) == 15

def test_batch_comparison_fields_all_15_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BATCH_COMPARISON_FIELDS
    required = [
        "strategy_profile_id", "total_candidates", "allowed_count", "blocked_count",
        "paper_buy_plan_count", "paper_add_plan_count", "reduce_plan_count",
        "exit_plan_count", "no_entry_count", "avg_score", "avg_risk_used",
        "human_review_count", "top_candidates", "worst_blocked_reasons",
        "simulation_quality_score",
    ]
    for field in required:
        assert field in BATCH_COMPARISON_FIELDS, f"{field} missing"

# ---------------------------------------------------------------------------
# SimulationRanking model
# ---------------------------------------------------------------------------

def test_simulation_ranking_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert obj is not None

def test_simulation_ranking_has_rank():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert hasattr(obj, "rank")

def test_simulation_ranking_has_profile_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert hasattr(obj, "profile_id")

def test_simulation_ranking_has_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert hasattr(obj, "scenario_id")

def test_simulation_ranking_has_quality_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert hasattr(obj, "quality_score")

def test_simulation_ranking_has_risk_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert hasattr(obj, "risk_score")

def test_simulation_ranking_has_selectivity_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert hasattr(obj, "selectivity_score")

def test_simulation_ranking_has_actionability_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert hasattr(obj, "actionability_score")

def test_simulation_ranking_has_review_burden_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert hasattr(obj, "review_burden_score")

def test_simulation_ranking_has_safety_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert hasattr(obj, "safety_score")

def test_simulation_ranking_has_final_grade():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert hasattr(obj, "final_grade")

def test_simulation_ranking_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationRanking
    obj = SimulationRanking()
    assert obj.paper_only is True

# ---------------------------------------------------------------------------
# rank_simulations function
# ---------------------------------------------------------------------------

def test_rank_simulations_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison, rank_simulations
    comparisons = [build_batch_comparison(simulate_one(), "P001")]
    results = rank_simulations(comparisons)
    assert results is not None

def test_rank_simulations_returns_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison, rank_simulations
    comparisons = [build_batch_comparison(simulate_one(), "P001")]
    results = rank_simulations(comparisons)
    assert isinstance(results, list)

def test_rank_simulations_correct_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison, rank_simulations
    comparisons = [
        build_batch_comparison(simulate_one(), "P001"),
        build_batch_comparison(simulate_one(), "P002"),
    ]
    results = rank_simulations(comparisons)
    assert len(results) == 2

def test_rank_simulations_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison, rank_simulations
    comparisons = [build_batch_comparison(simulate_one(), "P001")]
    results = rank_simulations(comparisons)
    for r in results:
        assert r.paper_only is True

def test_rank_simulations_has_final_grade():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison, rank_simulations
    comparisons = [build_batch_comparison(simulate_one(), "P001")]
    results = rank_simulations(comparisons)
    for r in results:
        assert r.final_grade is not None

def test_rank_simulations_rank_is_1_for_single():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison, rank_simulations
    comparisons = [build_batch_comparison(simulate_one(), "P001")]
    results = rank_simulations(comparisons)
    assert results[0].rank == 1

# ---------------------------------------------------------------------------
# SIMULATION_RANKING_FIELDS constant
# ---------------------------------------------------------------------------

def test_ranking_fields_all_10_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SIMULATION_RANKING_FIELDS
    required = [
        "rank", "profile_id", "scenario_id", "quality_score", "risk_score",
        "selectivity_score", "actionability_score", "review_burden_score",
        "safety_score", "final_grade",
    ]
    for field in required:
        assert field in SIMULATION_RANKING_FIELDS, f"{field} missing"
