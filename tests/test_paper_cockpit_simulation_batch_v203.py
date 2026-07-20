"""
tests/test_paper_cockpit_simulation_batch_v203.py
v2.0.3 Simulation Batch Engine Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# models
# ---------------------------------------------------------------------------

def test_simulation_input_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationInput
    obj = SimulationInput()
    assert obj is not None

def test_simulation_result_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationResult
    obj = SimulationResult()
    assert obj is not None

def test_batch_simulation_result_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BatchSimulationResult
    obj = BatchSimulationResult()
    assert obj is not None

def test_simulation_candidate_result_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationCandidateResult
    obj = SimulationCandidateResult()
    assert obj is not None

def test_simulation_input_default_watchlist():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationInput
    obj = SimulationInput()
    assert isinstance(obj.watchlist, list)

def test_simulation_input_custom_watchlist():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationInput
    obj = SimulationInput(watchlist=["2330", "2317", "2454"])
    assert len(obj.watchlist) == 3

def test_simulation_input_market_condition():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationInput
    obj = SimulationInput(market_condition="bull_trend")
    assert obj.market_condition == "bull_trend"

def test_simulation_input_paper_only_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationInput
    obj = SimulationInput()
    assert obj.paper_only is True

def test_simulation_input_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationInput
    obj = SimulationInput()
    assert obj.no_real_orders is True

# ---------------------------------------------------------------------------
# simulate_one
# ---------------------------------------------------------------------------

def test_simulate_one_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result is not None

def test_simulate_one_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.all_passed is True

def test_simulate_one_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.paper_only is True

def test_simulate_one_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.no_real_orders is True

def test_simulate_one_has_simulation_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.simulation_id

def test_simulate_one_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.simulation_version == "2.0.3"

def test_simulate_one_has_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.scenario_id is not None

def test_simulate_one_has_watchlist_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.watchlist_snapshot is not None

def test_simulate_one_has_rule_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.rule_snapshot is not None

def test_simulate_one_has_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.paper_only_safety_snapshot is not None

def test_simulate_one_has_final_action_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.final_action_summary is not None

def test_simulate_one_with_custom_watchlist():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, SimulationInput
    result = simulate_one(SimulationInput(watchlist=["2330", "2317"], market_condition="bull_trend"))
    assert result.all_passed is True

def test_simulate_one_with_pullback():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, SimulationInput
    result = simulate_one(SimulationInput(market_condition="pullback"))
    assert result.paper_only is True

def test_simulate_one_with_breakdown():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, SimulationInput
    result = simulate_one(SimulationInput(market_condition="breakdown"))
    assert result.all_passed is True

def test_simulate_one_with_panic_selloff():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, SimulationInput
    result = simulate_one(SimulationInput(market_condition="panic_selloff"))
    assert result.all_passed is True

def test_simulate_one_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.no_broker is True

def test_simulate_one_production_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.paper_only_safety_snapshot is True

# ---------------------------------------------------------------------------
# simulate_batch
# ---------------------------------------------------------------------------

def test_simulate_batch_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    assert result is not None

def test_simulate_batch_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    assert result.all_passed is True

def test_simulate_batch_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    assert result.paper_only is True

def test_simulate_batch_total_simulations():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    assert len(result.simulations) >= 1

def test_simulate_batch_has_results():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    assert isinstance(result.simulations, list)
    assert len(result.simulations) >= 1

def test_simulate_batch_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    assert result.no_real_orders is True

def test_simulate_batch_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    assert result.schema_version == "203"

def test_simulate_batch_has_batch_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    assert result.batch_id

def test_simulate_batch_results_all_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    for r in result.simulations:
        assert r.paper_only is True

def test_simulate_batch_results_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    for r in result.simulations:
        assert r.no_real_orders is True

# ---------------------------------------------------------------------------
# get_simulation_summary
# ---------------------------------------------------------------------------

def test_get_simulation_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import get_simulation_summary
    summary = get_simulation_summary()
    assert summary is not None

def test_get_simulation_summary_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import get_simulation_summary
    summary = get_simulation_summary()
    assert summary.get("version") == "2.0.3"

def test_get_simulation_summary_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import get_simulation_summary
    summary = get_simulation_summary()
    assert summary.get("paper_only") is True

def test_get_simulation_summary_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import get_simulation_summary
    summary = get_simulation_summary()
    assert summary.get("no_real_orders") is True

def test_get_simulation_summary_is_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import get_simulation_summary
    summary = get_simulation_summary()
    assert isinstance(summary, dict)
