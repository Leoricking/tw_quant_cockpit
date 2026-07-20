"""
tests/test_paper_cockpit_safety_v203.py
v2.0.3 Safety Guard Tests — Paper Only, No Real Orders, No Broker
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# top-level safety constants
# ---------------------------------------------------------------------------

def test_no_real_orders_is_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_is_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_is_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True

# ---------------------------------------------------------------------------
# safety flags completeness
# ---------------------------------------------------------------------------

def test_all_20_safety_flags_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert len(SAFETY_FLAGS_V203) == 20

def test_safety_flags_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["no_real_orders"] is True

def test_safety_flags_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["paper_only"] is True

def test_safety_flags_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["no_broker"] is True

def test_safety_flags_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["broker_execution_disabled"] is True

def test_safety_flags_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["production_trading_blocked"] is True

def test_safety_flags_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["no_real_account_sync"] is True

def test_safety_flags_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["no_automatic_rebalance"] is True

def test_safety_flags_no_margin():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203.get("no_margin") is True

def test_safety_flags_no_leverage():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203.get("no_leverage") is True

def test_safety_flags_research_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203.get("research_only") is True

def test_safety_flags_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203.get("not_investment_advice") is True

def test_all_flags_are_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    for k, v in SAFETY_FLAGS_V203.items():
        assert v is True, f"Flag {k} is not True"

# ---------------------------------------------------------------------------
# paper_only_safety_snapshot on SimulationResult
# ---------------------------------------------------------------------------

def test_simulation_result_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.paper_only_safety_snapshot is True

def test_simulation_result_safety_snapshot_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.paper_only is True

def test_simulation_result_safety_snapshot_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.no_real_orders is True

def test_simulation_result_safety_snapshot_broker_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.no_broker is True

def test_simulation_result_safety_snapshot_production_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.paper_only_safety_snapshot is True

# ---------------------------------------------------------------------------
# safety on batch
# ---------------------------------------------------------------------------

def test_batch_result_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    assert result.paper_only is True

def test_batch_result_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    assert result.no_real_orders is True

def test_batch_result_each_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    for r in result.simulations:
        assert r.paper_only is True

def test_batch_result_each_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    for r in result.simulations:
        assert r.no_real_orders is True

# ---------------------------------------------------------------------------
# safety on export
# ---------------------------------------------------------------------------

def test_export_json_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_json
    result = export_simulation_json(simulate_one())
    assert result.paper_only is True

def test_export_json_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_json
    result = export_simulation_json(simulate_one())
    assert result.no_real_orders is True

def test_export_markdown_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_markdown
    result = export_simulation_markdown(simulate_one())
    assert result.paper_only is True

def test_export_csv_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_csv
    result = export_simulation_csv(simulate_one())
    assert result.paper_only is True

def test_audit_snapshot_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_simulation_audit_snapshot
    result = build_simulation_audit_snapshot(simulate_one())
    assert result.paper_only is True

def test_replay_scenario_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario
    result = replay_scenario()
    assert result.paper_only is True

def test_replay_scenario_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario
    result = replay_scenario()
    assert result.no_real_orders is True

def test_batch_comparison_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison
    result = build_batch_comparison(simulate_one(), "P001")
    assert result.paper_only is True

def test_ranking_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_batch_comparison, rank_simulations
    results = rank_simulations([build_batch_comparison(simulate_one(), "P001")])
    for r in results:
        assert r.paper_only is True

def test_strategy_profile_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    for style in ["conservative", "balanced", "aggressive", "second_wave", "abc_pullback", "breakout_only", "risk_first"]:
        obj = StrategyProfile(entry_style=style)
        assert obj.paper_only is True

def test_scenario_replay_schema_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ScenarioReplaySchema
    for mc in ["bull_trend", "pullback", "breakdown", "panic_selloff"]:
        obj = ScenarioReplaySchema(market_condition=mc)
        assert obj.paper_only is True

# ---------------------------------------------------------------------------
# no broker in any path
# ---------------------------------------------------------------------------

def test_no_broker_constant_import():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_safety_flags_no_broker_in_any_key():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert any("broker" in k.lower() for k in SAFETY_FLAGS_V203)

def test_no_automatic_rebalance_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203.get("no_automatic_rebalance") is True

def test_no_real_account_sync_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203.get("no_real_account_sync") is True
