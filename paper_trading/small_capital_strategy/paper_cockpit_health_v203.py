"""
paper_trading/small_capital_strategy/paper_cockpit_health_v203.py
v2.0.3 Paper Strategy Simulation Batch & Scenario Replay — Health Check
[!] Paper Only. Research Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("D:/code/Claude/tw_quant_cockpit"))

HEALTH_VERSION = "2.0.3"
HEALTH_RELEASE = "Paper Strategy Simulation Batch & Scenario Replay"


def run_health_check():
    """Run all health checks for v2.0.3. Returns result dict."""
    passed = 0
    failed = 0
    errors = []

    def chk(name, fn):
        nonlocal passed, failed
        try:
            fn()
            passed += 1
        except Exception as e:
            failed += 1
            errors.append(f"FAIL:{name}:{e}")

    # --- import ---
    chk("import_v203", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v203", fromlist=["VERSION"]))

    # --- version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import VERSION, SCHEMA_VERSION
    chk("version_203", lambda: None if VERSION == "2.0.3" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.3 got {VERSION}")))
    chk("schema_version_203", lambda: None if SCHEMA_VERSION == "203" else (_ for _ in ()).throw(
        AssertionError(f"Expected 203 got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("no_real_orders_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("broker_disabled_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("production_blocked_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    chk("safety_flags_20", lambda: None if len(SAFETY_FLAGS_V203) == 20 else (_ for _ in ()).throw(
        AssertionError(f"Expected 20 safety flags, got {len(SAFETY_FLAGS_V203)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V203["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_no_real_orders", lambda: None if SAFETY_FLAGS_V203["no_real_orders"] is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders must be True")))
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V203["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_broker_disabled", lambda: None if SAFETY_FLAGS_V203["broker_execution_disabled"] is True else (
        _ for _ in ()).throw(AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_blocked", lambda: None if SAFETY_FLAGS_V203["production_trading_blocked"] is True else (
        _ for _ in ()).throw(AssertionError("production_trading_blocked must be True")))

    # --- constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import (
        MARKET_CONDITIONS, ENTRY_STYLES, CLI_COMMANDS_V203, GUI_TABS_V203,
        SCENARIO_REPLAY_FIELDS, STRATEGY_PROFILE_FIELDS, BATCH_COMPARISON_FIELDS,
        SIMULATION_RANKING_FIELDS, _ALL_MODEL_NAMES_V203,
    )
    chk("market_conditions_8", lambda: None if len(MARKET_CONDITIONS) == 8 else (_ for _ in ()).throw(
        AssertionError(f"Expected 8 market conditions")))
    chk("entry_styles_7", lambda: None if len(ENTRY_STYLES) == 7 else (_ for _ in ()).throw(
        AssertionError(f"Expected 7 entry styles")))
    chk("cli_commands_10", lambda: None if len(CLI_COMMANDS_V203) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI commands")))
    chk("gui_tabs_3", lambda: None if len(GUI_TABS_V203) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI tabs")))
    chk("scenario_replay_fields_12", lambda: None if len(SCENARIO_REPLAY_FIELDS) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 scenario replay fields")))
    chk("strategy_profile_fields_12", lambda: None if len(STRATEGY_PROFILE_FIELDS) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 strategy profile fields")))
    chk("batch_comparison_fields_15", lambda: None if len(BATCH_COMPARISON_FIELDS) == 15 else (_ for _ in ()).throw(
        AssertionError(f"Expected 15 batch comparison fields")))
    chk("ranking_fields_10", lambda: None if len(SIMULATION_RANKING_FIELDS) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 ranking fields")))
    chk("models_12", lambda: None if len(_ALL_MODEL_NAMES_V203) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 models")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import (
        SimulationInput, ScenarioReplaySchema, StrategyProfile, SimulationCandidateResult,
        BatchComparison, SimulationRanking, SimulationExportResult, SimulationAuditSnapshot,
        SimulationResult, BatchSimulationResult, V203HealthSummary, V203ReleaseSummary,
    )
    chk("model_SimulationInput", lambda: SimulationInput())
    chk("model_ScenarioReplaySchema", lambda: ScenarioReplaySchema())
    chk("model_StrategyProfile", lambda: StrategyProfile())
    chk("model_SimulationCandidateResult", lambda: SimulationCandidateResult())
    chk("model_BatchComparison", lambda: BatchComparison())
    chk("model_SimulationRanking", lambda: SimulationRanking())
    chk("model_SimulationExportResult", lambda: SimulationExportResult())
    chk("model_SimulationAuditSnapshot", lambda: SimulationAuditSnapshot())
    chk("model_SimulationResult", lambda: SimulationResult())
    chk("model_BatchSimulationResult", lambda: BatchSimulationResult())
    chk("model_V203HealthSummary", lambda: V203HealthSummary())
    chk("model_V203ReleaseSummary", lambda: V203ReleaseSummary())

    # --- engine functions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import (
        simulate_one, replay_scenario, simulate_batch, build_batch_comparison,
        rank_simulations, export_simulation_json, export_simulation_markdown,
        export_simulation_csv, build_simulation_audit_snapshot,
        get_simulation_summary, get_version_info_v203, verify_version_v203,
    )
    chk("fn_simulate_one", lambda: simulate_one())
    chk("fn_simulate_one_all_passed", lambda: None if simulate_one().all_passed is True else (
        _ for _ in ()).throw(AssertionError("simulate_one all_passed not True")))
    chk("fn_simulate_one_paper_only", lambda: None if simulate_one().paper_only is True else (
        _ for _ in ()).throw(AssertionError("simulate_one paper_only not True")))
    chk("fn_simulate_one_no_real_orders", lambda: None if simulate_one().no_real_orders is True else (
        _ for _ in ()).throw(AssertionError("simulate_one no_real_orders not True")))
    chk("fn_replay_scenario", lambda: replay_scenario())
    chk("fn_simulate_batch", lambda: simulate_batch())
    chk("fn_simulate_batch_all_passed", lambda: None if simulate_batch().all_passed is True else (
        _ for _ in ()).throw(AssertionError("simulate_batch all_passed not True")))
    chk("fn_export_json", lambda: export_simulation_json(simulate_one()))
    chk("fn_export_json_valid", lambda: None if export_simulation_json(simulate_one()).is_valid is True else (
        _ for _ in ()).throw(AssertionError("json export not valid")))
    chk("fn_export_markdown", lambda: export_simulation_markdown(simulate_one()))
    chk("fn_export_markdown_valid", lambda: None if export_simulation_markdown(simulate_one()).is_valid is True else (
        _ for _ in ()).throw(AssertionError("markdown export not valid")))
    chk("fn_export_csv", lambda: export_simulation_csv(simulate_one()))
    chk("fn_export_csv_valid", lambda: None if export_simulation_csv(simulate_one()).is_valid is True else (
        _ for _ in ()).throw(AssertionError("csv export not valid")))
    chk("fn_audit_snapshot", lambda: build_simulation_audit_snapshot(simulate_one()))
    chk("fn_audit_snapshot_hash", lambda: None if build_simulation_audit_snapshot(
        simulate_one()).reproducibility_hash else (_ for _ in ()).throw(AssertionError("no hash")))
    chk("fn_get_simulation_summary", lambda: get_simulation_summary())
    chk("fn_get_version_info", lambda: get_version_info_v203())
    chk("fn_verify_version", lambda: None if verify_version_v203() is True else (_ for _ in ()).throw(
        AssertionError("verify_version_v203 failed")))

    # --- simulation engine callable ---
    chk("simulation_engine_callable", lambda: simulate_one(SimulationInput(
        watchlist=["2330", "2317"], market_condition="bull_trend")))
    chk("scenario_replay_callable", lambda: replay_scenario(ScenarioReplaySchema(
        scenario_id="SC001", market_condition="pullback")))
    chk("batch_comparison_callable", lambda: build_batch_comparison(simulate_one(), "P001"))
    chk("ranking_callable", lambda: rank_simulations([build_batch_comparison(simulate_one(), "P001")]))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    chk("scenarios_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios")))
    chk("scenarios_schema_203", lambda: None if all(s["schema_version"] == "203" for s in SCENARIOS) else (
        _ for _ in ()).throw(AssertionError("Bad scenario schema")))
    chk("scenarios_paper_only", lambda: None if all(s["paper_only"] is True for s in SCENARIOS) else (
        _ for _ in ()).throw(AssertionError("Missing paper_only")))
    chk("scenarios_unique_ids", lambda: None if len({s["id"] for s in SCENARIOS}) == 80 else (
        _ for _ in ()).throw(AssertionError("Duplicate scenario IDs")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    chk("fixtures_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures")))
    chk("fixtures_schema_203", lambda: None if all(f["schema_version"] == "203" for f in FIXTURES) else (
        _ for _ in ()).throw(AssertionError("Bad fixture schema")))
    chk("fixtures_fixture_id", lambda: None if all("fixture_id" in f for f in FIXTURES) else (
        _ for _ in ()).throw(AssertionError("Missing fixture_id")))
    chk("fixtures_unique_ids", lambda: None if len({f["id"] for f in FIXTURES}) == 80 else (
        _ for _ in ()).throw(AssertionError("Duplicate fixture IDs")))

    # --- GUI ---
    from gui.small_capital_strategy_panel import PANEL_VERSION, PANEL_VERSION_V203, get_tab_names, get_v203_tab_names
    chk("panel_version_v203", lambda: None if PANEL_VERSION_V203 == "2.0.3" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V203 2.0.3, got {PANEL_VERSION_V203}")))
    chk("panel_version_unchanged", lambda: None if PANEL_VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"PANEL_VERSION must remain 2.0.0, got {PANEL_VERSION}")))
    tab_names = get_tab_names()
    for tab in GUI_TABS_V203:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' missing")))
    chk("get_v203_tab_names_3", lambda: None if len(get_v203_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v203 tab names")))

    # --- render_all_tabs no errors ---
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    chk("render_all_tabs_no_error_simulation_batch", lambda: None if "error" not in str(
        all_rendered.get("simulation_batch_v203", {})) else (_ for _ in ()).throw(
        AssertionError("simulation_batch_v203 has render error")))
    chk("render_all_tabs_no_error_scenario_replay", lambda: None if "error" not in str(
        all_rendered.get("scenario_replay_v203", {})) else (_ for _ in ()).throw(
        AssertionError("scenario_replay_v203 has render error")))
    chk("render_all_tabs_no_error_strategy_comparison", lambda: None if "error" not in str(
        all_rendered.get("strategy_comparison_v203", {})) else (_ for _ in ()).throw(
        AssertionError("strategy_comparison_v203 has render error")))
    error_tabs = [k for k, v in all_rendered.items() if isinstance(v, dict) and "error" in v]
    chk("render_all_tabs_zero_error_tabs", lambda: None if len(error_tabs) == 0 else (_ for _ in ()).throw(
        AssertionError(f"Error tabs: {error_tabs}")))

    # --- CLI ---
    from cli.command_registry import PROVIDER_COMMANDS
    command_names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in CLI_COMMANDS_V203:
        chk(f"cli_{cmd.replace('-','_')}", lambda c=cmd: None if c in command_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' missing")))

    # --- backward compatibility ---
    chk("backward_compat_v202", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v202", fromlist=["VERSION"]))
    chk("backward_compat_v201", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v201", fromlist=["VERSION"]))
    chk("backward_compat_v200", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v200", fromlist=["VERSION"]))

    # --- no real account sync / no automatic rebalance ---
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V203.get("no_real_account_sync") is True else (
        _ for _ in ()).throw(AssertionError("no_real_account_sync must be True")))
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V203.get("no_automatic_rebalance") is True else (
        _ for _ in ()).throw(AssertionError("no_automatic_rebalance must be True")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v203] {passed}/{total} passed")
    return {
        "all_passed": all_passed,
        "passed": passed,
        "failed": failed,
        "total": total,
        "errors": errors,
        "version": HEALTH_VERSION,
        "release": HEALTH_RELEASE,
    }


if __name__ == "__main__":
    result = run_health_check()
    if not result["all_passed"]:
        for e in result["errors"]:
            print(e)
        sys.exit(1)
    sys.exit(0)
