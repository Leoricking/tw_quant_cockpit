"""
tests/test_paper_cockpit_scenario_replay_v203.py
v2.0.3 Scenario Replay Schema Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# ScenarioReplaySchema model
# ---------------------------------------------------------------------------

def test_scenario_replay_schema_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert obj is not None

def test_scenario_replay_schema_has_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "scenario_id")

def test_scenario_replay_schema_has_scenario_name():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "scenario_name")

def test_scenario_replay_schema_has_market_condition():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "market_condition")

def test_scenario_replay_schema_has_trend_condition():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "trend_condition")

def test_scenario_replay_schema_has_volatility_condition():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "volatility_condition")

def test_scenario_replay_schema_has_liquidity_condition():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "liquidity_condition")

def test_scenario_replay_schema_has_chip_condition():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "chip_condition")

def test_scenario_replay_schema_has_margin_condition():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "margin_condition")

def test_scenario_replay_schema_has_candidate_inputs():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "candidate_inputs")

def test_scenario_replay_schema_has_expected_block_reasons():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "expected_block_reasons")

def test_scenario_replay_schema_has_expected_final_actions():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "expected_final_actions")

def test_scenario_replay_schema_has_replay_notes():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert hasattr(obj, "replay_notes")

def test_scenario_replay_schema_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert obj.paper_only is True

def test_scenario_replay_schema_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema()
    assert obj.no_real_orders is True

def test_scenario_replay_schema_custom_market_condition():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema(market_condition="pullback")
    assert obj.market_condition == "pullback"

def test_scenario_replay_schema_custom_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    obj = ScenarioReplaySchema(scenario_id="SC001")
    assert obj.scenario_id == "SC001"

# ---------------------------------------------------------------------------
# replay_scenario function
# ---------------------------------------------------------------------------

def test_replay_scenario_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario
    result = replay_scenario()
    assert result is not None

def test_replay_scenario_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario
    result = replay_scenario()
    assert result.paper_only is True

def test_replay_scenario_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario
    result = replay_scenario()
    assert result.no_real_orders is True

def test_replay_scenario_has_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario
    result = replay_scenario()
    assert result.scenario_id is not None

def test_replay_scenario_has_replay_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario
    result = replay_scenario()
    assert result.replay_result is not None

def test_replay_scenario_with_pullback():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario, ScenarioReplaySchema
    result = replay_scenario(ScenarioReplaySchema(market_condition="pullback"))
    assert result.paper_only is True

def test_replay_scenario_with_bull_trend():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario, ScenarioReplaySchema
    result = replay_scenario(ScenarioReplaySchema(market_condition="bull_trend"))
    assert result.no_real_orders is True

def test_replay_scenario_with_breakdown():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario, ScenarioReplaySchema
    result = replay_scenario(ScenarioReplaySchema(market_condition="breakdown"))
    assert result.paper_only is True

def test_replay_scenario_with_panic_selloff():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario, ScenarioReplaySchema
    result = replay_scenario(ScenarioReplaySchema(market_condition="panic_selloff"))
    assert result.paper_only is True

def test_replay_scenario_with_range_bound():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario, ScenarioReplaySchema
    result = replay_scenario(ScenarioReplaySchema(market_condition="range_bound"))
    assert result.paper_only is True

def test_replay_scenario_with_rebound():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario, ScenarioReplaySchema
    result = replay_scenario(ScenarioReplaySchema(market_condition="rebound"))
    assert result.paper_only is True

def test_replay_scenario_with_high_volatility():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario, ScenarioReplaySchema
    result = replay_scenario(ScenarioReplaySchema(market_condition="high_volatility"))
    assert result.paper_only is True

def test_replay_scenario_with_low_liquidity():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario, ScenarioReplaySchema
    result = replay_scenario(ScenarioReplaySchema(market_condition="low_liquidity"))
    assert result.paper_only is True

def test_replay_scenario_with_custom_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario, ScenarioReplaySchema
    result = replay_scenario(ScenarioReplaySchema(scenario_id="SC001", market_condition="pullback"))
    assert result.scenario_id == "SC001"

# ---------------------------------------------------------------------------
# SCENARIO_REPLAY_FIELDS constant
# ---------------------------------------------------------------------------

def test_scenario_replay_fields_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SCENARIO_REPLAY_FIELDS
    assert isinstance(SCENARIO_REPLAY_FIELDS, list)

def test_scenario_replay_fields_has_market_condition():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SCENARIO_REPLAY_FIELDS
    assert "market_condition" in SCENARIO_REPLAY_FIELDS

def test_scenario_replay_fields_has_chip_condition():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SCENARIO_REPLAY_FIELDS
    assert "chip_condition" in SCENARIO_REPLAY_FIELDS

def test_scenario_replay_fields_has_replay_notes():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SCENARIO_REPLAY_FIELDS
    assert "replay_notes" in SCENARIO_REPLAY_FIELDS

def test_scenario_replay_fields_unique():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SCENARIO_REPLAY_FIELDS
    assert len(SCENARIO_REPLAY_FIELDS) == len(set(SCENARIO_REPLAY_FIELDS))

# ---------------------------------------------------------------------------
# scenarios file
# ---------------------------------------------------------------------------

def test_scenarios_v203_import():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    assert SCENARIOS is not None

def test_scenarios_v203_count():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_scenarios_v203_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    for s in SCENARIOS:
        assert s["schema_version"] == "203"

def test_scenarios_v203_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    for s in SCENARIOS:
        assert s["paper_only"] is True

def test_scenarios_v203_unique_ids():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    ids = {s["id"] for s in SCENARIOS}
    assert len(ids) == 80

def test_scenarios_v203_have_description():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    for s in SCENARIOS:
        assert "description" in s

def test_scenarios_v203_have_name():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    for s in SCENARIOS:
        assert "name" in s

def test_scenarios_v203_all_have_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    for s in SCENARIOS:
        assert s.get("no_real_orders") is True

def test_scenarios_v203_ids_start_with_pc203():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    for s in SCENARIOS:
        assert s["id"].startswith("PC203-")
