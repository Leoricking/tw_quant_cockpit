"""
tests/test_paper_cockpit_v203.py
v2.0.3 Paper Strategy Simulation Batch & Scenario Replay — Core Module Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# import
# ---------------------------------------------------------------------------

def test_import_v203():
    import paper_trading.small_capital_strategy.paper_cockpit_v203

def test_version_is_203():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import VERSION
    assert VERSION == "2.0.3"

def test_schema_version_203():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "203"

def test_release_name():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import RELEASE_NAME
    assert "Simulation" in RELEASE_NAME or "Scenario" in RELEASE_NAME or "Batch" in RELEASE_NAME

# ---------------------------------------------------------------------------
# safety constants
# ---------------------------------------------------------------------------

def test_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True

# ---------------------------------------------------------------------------
# safety flags
# ---------------------------------------------------------------------------

def test_safety_flags_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert len(SAFETY_FLAGS_V203) == 20

def test_safety_flag_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["paper_only"] is True

def test_safety_flag_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["no_real_orders"] is True

def test_safety_flag_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["no_broker"] is True

def test_safety_flag_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["broker_execution_disabled"] is True

def test_safety_flag_production_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["production_trading_blocked"] is True

def test_safety_flag_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["no_real_account_sync"] is True

def test_safety_flag_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203["no_automatic_rebalance"] is True

def test_safety_flag_no_margin():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203.get("no_margin") is True

def test_safety_flag_no_leverage():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert SAFETY_FLAGS_V203.get("no_leverage") is True

def test_safety_flags_are_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert isinstance(SAFETY_FLAGS_V203, dict)

def test_all_safety_flags_bool():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    for k, v in SAFETY_FLAGS_V203.items():
        assert isinstance(v, bool), f"Flag {k} is not bool"

# ---------------------------------------------------------------------------
# market conditions
# ---------------------------------------------------------------------------

def test_market_conditions_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    assert len(MARKET_CONDITIONS) == 8

def test_market_condition_bull_trend():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    assert "bull_trend" in MARKET_CONDITIONS

def test_market_condition_pullback():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    assert "pullback" in MARKET_CONDITIONS

def test_market_condition_range_bound():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    assert "range_bound" in MARKET_CONDITIONS

def test_market_condition_breakdown():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    assert "breakdown" in MARKET_CONDITIONS

def test_market_condition_panic_selloff():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    assert "panic_selloff" in MARKET_CONDITIONS

def test_market_condition_rebound():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    assert "rebound" in MARKET_CONDITIONS

def test_market_condition_high_volatility():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    assert "high_volatility" in MARKET_CONDITIONS

def test_market_condition_low_liquidity():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    assert "low_liquidity" in MARKET_CONDITIONS

def test_market_conditions_all_str():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    for c in MARKET_CONDITIONS:
        assert isinstance(c, str)

def test_market_conditions_no_duplicates():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    assert len(MARKET_CONDITIONS) == len(set(MARKET_CONDITIONS))

# ---------------------------------------------------------------------------
# entry styles
# ---------------------------------------------------------------------------

def test_entry_styles_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ENTRY_STYLES
    assert len(ENTRY_STYLES) == 7

def test_entry_style_conservative():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ENTRY_STYLES
    assert "conservative" in ENTRY_STYLES

def test_entry_style_balanced():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ENTRY_STYLES
    assert "balanced" in ENTRY_STYLES

def test_entry_style_aggressive():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ENTRY_STYLES
    assert "aggressive" in ENTRY_STYLES

def test_entry_style_second_wave():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ENTRY_STYLES
    assert "second_wave" in ENTRY_STYLES

def test_entry_style_abc_pullback():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ENTRY_STYLES
    assert "abc_pullback" in ENTRY_STYLES

def test_entry_style_breakout_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ENTRY_STYLES
    assert "breakout_only" in ENTRY_STYLES

def test_entry_style_risk_first():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ENTRY_STYLES
    assert "risk_first" in ENTRY_STYLES

def test_entry_styles_no_duplicates():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ENTRY_STYLES
    assert len(ENTRY_STYLES) == len(set(ENTRY_STYLES))

# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def test_cli_commands_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert len(CLI_COMMANDS_V203) == 10

def test_cli_simulate_one():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert "paper-cockpit-v203-simulate-one" in CLI_COMMANDS_V203

def test_cli_simulate_batch():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert "paper-cockpit-v203-simulate-batch" in CLI_COMMANDS_V203

def test_cli_replay_scenario():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert "paper-cockpit-v203-replay-scenario" in CLI_COMMANDS_V203

def test_cli_compare_profiles():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert "paper-cockpit-v203-compare-profiles" in CLI_COMMANDS_V203

def test_cli_rank_results():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert "paper-cockpit-v203-rank-results" in CLI_COMMANDS_V203

def test_cli_export_json():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert "paper-cockpit-v203-export-json" in CLI_COMMANDS_V203

def test_cli_export_md():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert "paper-cockpit-v203-export-md" in CLI_COMMANDS_V203

def test_cli_export_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert "paper-cockpit-v203-export-csv" in CLI_COMMANDS_V203

def test_cli_health():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert "paper-cockpit-v203-health" in CLI_COMMANDS_V203

def test_cli_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert "paper-cockpit-v203-gate" in CLI_COMMANDS_V203

# ---------------------------------------------------------------------------
# GUI tabs
# ---------------------------------------------------------------------------

def test_gui_tabs_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import GUI_TABS_V203
    assert len(GUI_TABS_V203) == 3

def test_gui_tab_simulation_batch():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import GUI_TABS_V203
    assert "simulation_batch_v203" in GUI_TABS_V203

def test_gui_tab_scenario_replay():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import GUI_TABS_V203
    assert "scenario_replay_v203" in GUI_TABS_V203

def test_gui_tab_strategy_comparison():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import GUI_TABS_V203
    assert "strategy_comparison_v203" in GUI_TABS_V203

# ---------------------------------------------------------------------------
# field lists
# ---------------------------------------------------------------------------

def test_scenario_replay_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SCENARIO_REPLAY_FIELDS
    assert len(SCENARIO_REPLAY_FIELDS) == 12

def test_scenario_replay_has_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SCENARIO_REPLAY_FIELDS
    assert "scenario_id" in SCENARIO_REPLAY_FIELDS

def test_strategy_profile_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import STRATEGY_PROFILE_FIELDS
    assert len(STRATEGY_PROFILE_FIELDS) == 12

def test_strategy_profile_has_profile_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import STRATEGY_PROFILE_FIELDS
    assert "profile_id" in STRATEGY_PROFILE_FIELDS

def test_batch_comparison_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BATCH_COMPARISON_FIELDS
    assert len(BATCH_COMPARISON_FIELDS) == 15

def test_batch_comparison_has_quality_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BATCH_COMPARISON_FIELDS
    assert "simulation_quality_score" in BATCH_COMPARISON_FIELDS

def test_ranking_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SIMULATION_RANKING_FIELDS
    assert len(SIMULATION_RANKING_FIELDS) == 10

def test_ranking_has_final_grade():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SIMULATION_RANKING_FIELDS
    assert "final_grade" in SIMULATION_RANKING_FIELDS

def test_models_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import _ALL_MODEL_NAMES_V203
    assert len(_ALL_MODEL_NAMES_V203) == 12

# ---------------------------------------------------------------------------
# version info
# ---------------------------------------------------------------------------

def test_get_version_info_v203():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import get_version_info_v203
    info = get_version_info_v203()
    assert info["version"] == "2.0.3"

def test_verify_version_v203():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import verify_version_v203
    assert verify_version_v203() is True

def test_baseline_tests():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BASELINE_TESTS
    assert BASELINE_TESTS == 33205

def test_min_new_tests():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300
