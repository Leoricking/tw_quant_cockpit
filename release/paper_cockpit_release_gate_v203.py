"""
release/paper_cockpit_release_gate_v203.py
v2.0.3 Paper Strategy Simulation Batch & Scenario Replay — Release Gate
[!] Paper Only. Research Only. Simulate Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("D:/code/Claude/tw_quant_cockpit"))

GATE_VERSION = "2.0.3"
GATE_RELEASE = "Paper Strategy Simulation Batch & Scenario Replay"
BASELINE_TESTS = 33205
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = ("2.0.0", "2.0.1", "2.0.2", "2.0.3")


def run_release_gate():
    """Run all release gate checks for v2.0.3. Returns result dict."""
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

    # --- gate version checks ---
    chk("gate_version_203", lambda: None if GATE_VERSION == "2.0.3" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.3")))
    chk("baseline_tests_33205", lambda: None if BASELINE_TESTS == 33205 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 33205")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import VERSION, SCHEMA_VERSION
    chk("module_version_203", lambda: None if VERSION == "2.0.3" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.3, got {VERSION}")))
    chk("schema_version_203", lambda: None if SCHEMA_VERSION == "203" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 203, got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    chk("safety_flags_20", lambda: None if len(SAFETY_FLAGS_V203) == 20 else (_ for _ in ()).throw(
        AssertionError(f"Expected 20 safety flags, got {len(SAFETY_FLAGS_V203)}")))
    chk("paper_only_true", lambda: None if SAFETY_FLAGS_V203.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("no_real_orders_flag", lambda: None if SAFETY_FLAGS_V203.get("no_real_orders") is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders flag must be True")))
    chk("broker_disabled", lambda: None if SAFETY_FLAGS_V203.get("broker_execution_disabled") is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("production_blocked", lambda: None if SAFETY_FLAGS_V203.get("production_trading_blocked") is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V203.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V203.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- models count ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import _ALL_MODEL_NAMES_V203
    chk("models_count_12", lambda: None if len(_ALL_MODEL_NAMES_V203) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 models, got {len(_ALL_MODEL_NAMES_V203)}")))

    # --- market conditions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import MARKET_CONDITIONS
    chk("market_conditions_8", lambda: None if len(MARKET_CONDITIONS) == 8 else (_ for _ in ()).throw(
        AssertionError(f"Expected 8 market conditions")))
    chk("has_bull_trend", lambda: None if "bull_trend" in MARKET_CONDITIONS else (_ for _ in ()).throw(
        AssertionError("bull_trend missing")))
    chk("has_pullback", lambda: None if "pullback" in MARKET_CONDITIONS else (_ for _ in ()).throw(
        AssertionError("pullback missing")))

    # --- entry styles ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ENTRY_STYLES
    chk("entry_styles_7", lambda: None if len(ENTRY_STYLES) == 7 else (_ for _ in ()).throw(
        AssertionError(f"Expected 7 entry styles")))
    chk("has_conservative", lambda: None if "conservative" in ENTRY_STYLES else (_ for _ in ()).throw(
        AssertionError("conservative missing")))

    # --- scenario replay fields ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SCENARIO_REPLAY_FIELDS
    chk("scenario_replay_fields_12", lambda: None if len(SCENARIO_REPLAY_FIELDS) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 scenario replay fields")))
    chk("has_scenario_id", lambda: None if "scenario_id" in SCENARIO_REPLAY_FIELDS else (_ for _ in ()).throw(
        AssertionError("scenario_id missing from SCENARIO_REPLAY_FIELDS")))

    # --- strategy profile fields ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import STRATEGY_PROFILE_FIELDS
    chk("strategy_profile_fields_12", lambda: None if len(STRATEGY_PROFILE_FIELDS) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 strategy profile fields")))
    chk("has_profile_id", lambda: None if "profile_id" in STRATEGY_PROFILE_FIELDS else (_ for _ in ()).throw(
        AssertionError("profile_id missing from STRATEGY_PROFILE_FIELDS")))

    # --- batch comparison fields ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BATCH_COMPARISON_FIELDS
    chk("batch_comparison_fields_15", lambda: None if len(BATCH_COMPARISON_FIELDS) == 15 else (_ for _ in ()).throw(
        AssertionError(f"Expected 15 batch comparison fields")))

    # --- ranking fields ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SIMULATION_RANKING_FIELDS
    chk("ranking_fields_10", lambda: None if len(SIMULATION_RANKING_FIELDS) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 ranking fields")))

    # --- simulation engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import (
        simulate_one, replay_scenario, simulate_batch, build_batch_comparison,
        rank_simulations, export_simulation_json, export_simulation_markdown,
        export_simulation_csv, build_simulation_audit_snapshot,
        get_simulation_summary, get_version_info_v203, verify_version_v203,
    )
    chk("simulate_one_callable", lambda: simulate_one())
    chk("simulate_one_all_passed", lambda: None if simulate_one().all_passed is True else (_ for _ in ()).throw(
        AssertionError("simulate_one all_passed not True")))
    chk("simulate_one_paper_only", lambda: None if simulate_one().paper_only is True else (_ for _ in ()).throw(
        AssertionError("simulate_one paper_only not True")))
    chk("replay_scenario_callable", lambda: replay_scenario())
    chk("simulate_batch_callable", lambda: simulate_batch())
    chk("simulate_batch_all_passed", lambda: None if simulate_batch().all_passed is True else (_ for _ in ()).throw(
        AssertionError("simulate_batch all_passed not True")))
    chk("export_json_callable", lambda: export_simulation_json(simulate_one()))
    chk("export_json_valid", lambda: None if export_simulation_json(simulate_one()).is_valid is True else (_ for _ in ()).throw(
        AssertionError("json export not valid")))
    chk("export_markdown_callable", lambda: export_simulation_markdown(simulate_one()))
    chk("export_markdown_valid", lambda: None if export_simulation_markdown(simulate_one()).is_valid is True else (_ for _ in ()).throw(
        AssertionError("markdown export not valid")))
    chk("export_csv_callable", lambda: export_simulation_csv(simulate_one()))
    chk("export_csv_valid", lambda: None if export_simulation_csv(simulate_one()).is_valid is True else (_ for _ in ()).throw(
        AssertionError("csv export not valid")))
    chk("audit_snapshot_callable", lambda: build_simulation_audit_snapshot(simulate_one()))
    chk("audit_snapshot_hash", lambda: None if build_simulation_audit_snapshot(simulate_one()).reproducibility_hash else (_ for _ in ()).throw(
        AssertionError("no reproducibility_hash")))
    chk("get_simulation_summary_callable", lambda: get_simulation_summary())
    chk("get_version_info_callable", lambda: get_version_info_v203())
    chk("verify_version_callable", lambda: None if verify_version_v203() is True else (_ for _ in ()).throw(
        AssertionError("verify_version_v203 failed")))
    chk("build_batch_comparison_callable", lambda: build_batch_comparison(simulate_one(), "P001"))
    chk("rank_simulations_callable", lambda: rank_simulations([build_batch_comparison(simulate_one(), "P001")]))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    chk("cli_commands_10", lambda: None if len(CLI_COMMANDS_V203) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI_COMMANDS_V203")))
    for cmd in [
        "paper-cockpit-v203-simulate-one",
        "paper-cockpit-v203-simulate-batch",
        "paper-cockpit-v203-replay-scenario",
        "paper-cockpit-v203-compare-profiles",
        "paper-cockpit-v203-rank-results",
        "paper-cockpit-v203-export-json",
        "paper-cockpit-v203-export-md",
        "paper-cockpit-v203-export-csv",
        "paper-cockpit-v203-health",
        "paper-cockpit-v203-gate",
    ]:
        chk(f"cli_{cmd.replace('-','_')}", lambda c=cmd: None if c in CLI_COMMANDS_V203 else (_ for _ in ()).throw(
            AssertionError(f"Missing CLI command: {c}")))

    # --- CLI commands registered in PROVIDER_COMMANDS ---
    from cli.command_registry import PROVIDER_COMMANDS
    command_names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in CLI_COMMANDS_V203:
        chk(f"registry_{cmd.replace('-','_')}", lambda c=cmd: None if c in command_names else (_ for _ in ()).throw(
            AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- GUI import safe ---
    from gui.small_capital_strategy_panel import PANEL_VERSION_V203
    chk("panel_version_v203", lambda: None if PANEL_VERSION_V203 == "2.0.3" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V203 2.0.3, got {PANEL_VERSION_V203}")))

    # --- PANEL_VERSION unchanged ---
    from gui.small_capital_strategy_panel import PANEL_VERSION
    chk("panel_version_200_unchanged", lambda: None if PANEL_VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"PANEL_VERSION must remain 2.0.0, got {PANEL_VERSION}")))

    # --- GUI tabs ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v203_tab_names
    tab_names = get_tab_names()
    for tab in ["simulation_batch_v203", "scenario_replay_v203", "strategy_comparison_v203"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing")))
    chk("get_v203_tab_names_3", lambda: None if len(get_v203_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v203 tab names")))

    # --- render_all_tabs zero error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    error_tabs = [k for k, v in all_rendered.items() if isinstance(v, dict) and "error" in v]
    chk("render_all_tabs_zero_error_tabs", lambda: None if len(error_tabs) == 0 else (_ for _ in ()).throw(
        AssertionError(f"Error tabs: {error_tabs}")))
    for tab in ["simulation_batch_v203", "scenario_replay_v203", "strategy_comparison_v203"]:
        chk(f"render_{tab}_no_error", lambda t=tab: None if "error" not in str(
            all_rendered.get(t, {})) else (_ for _ in ()).throw(AssertionError(f"{t} has render error")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_203", lambda: None if all(s["schema_version"] == "203" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Bad scenario schema")))
    chk("scenarios_paper_only", lambda: None if all(s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Missing paper_only in scenarios")))
    chk("scenarios_unique_ids", lambda: None if len({s["id"] for s in SCENARIOS}) == 80 else (_ for _ in ()).throw(
        AssertionError("Duplicate scenario IDs")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_203", lambda: None if all(f["schema_version"] == "203" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Bad fixture schema")))
    chk("fixtures_unique_ids", lambda: None if len({f["id"] for f in FIXTURES}) == 80 else (_ for _ in ()).throw(
        AssertionError("Duplicate fixture IDs")))

    # --- backward compat with v2.0.2 ---
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import VERSION as V202
    chk("v202_backward_compat", lambda: None if V202 == "2.0.2" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.2 VERSION changed to {V202}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    chk("v202_export_json_callable", lambda: None if export_json().is_valid is True else (_ for _ in ()).throw(
        AssertionError("v202 export_json is_valid must be True")))

    # --- backward compat with v2.0.1 ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import VERSION as V201
    chk("v201_backward_compat", lambda: None if V201 == "2.0.1" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.1 VERSION changed to {V201}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import run_daily_workflow
    chk("v201_workflow_callable", lambda: None if run_daily_workflow().paper_only is True else (_ for _ in ()).throw(
        AssertionError("v201 workflow paper_only must be True")))

    # --- backward compat with v2.0.0 ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION as V200
    chk("v200_backward_compat", lambda: None if V200 == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.0 VERSION changed to {V200}")))

    gate_passed = (failed == 0)
    total_count = passed + failed
    print(f"[paper_cockpit_release_gate_v203] gate_passed={gate_passed}  {passed}/{total_count}")
    return {
        "gate_passed": gate_passed,
        "passed_count": passed,
        "failed_count": failed,
        "total_count": total_count,
        "errors": errors,
        "gate_version": GATE_VERSION,
        "gate_release": GATE_RELEASE,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
    }


if __name__ == "__main__":
    result = run_release_gate()
    if not result["gate_passed"]:
        for e in result["errors"]:
            print(e)
        sys.exit(1)
    sys.exit(0)
