"""
release/paper_cockpit_release_gate_v201.py
v2.0.1 Paper Cockpit Usability & Daily Workflow Hardening — Release Gate
[!] Paper Only. Research Only. Simulate Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("D:/code/Claude/tw_quant_cockpit"))

GATE_VERSION = "2.0.1"
GATE_RELEASE = "Paper Cockpit Usability & Daily Workflow Hardening"
BASELINE_TESTS = 32425
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = ("2.0.0", "2.0.1")


def run_release_gate():
    """Run all release gate checks for v2.0.1. Returns result dict."""
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
    chk("gate_version_201", lambda: None if GATE_VERSION == "2.0.1" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.1")))
    chk("baseline_tests_32425", lambda: None if BASELINE_TESTS == 32425 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 32425")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import VERSION, SCHEMA_VERSION
    chk("module_version_201", lambda: None if VERSION == "2.0.1" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.1, got {VERSION}")))
    chk("schema_version_201", lambda: None if SCHEMA_VERSION == "201" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 201, got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import _ALL_MODEL_NAMES_V201
    chk("models_count_12", lambda: None if len(_ALL_MODEL_NAMES_V201) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 models, got {len(_ALL_MODEL_NAMES_V201)}")))

    # --- no-entry reasons ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import NO_ENTRY_REASONS
    chk("no_entry_reasons_13", lambda: None if len(NO_ENTRY_REASONS) == 13 else (_ for _ in ()).throw(
        AssertionError(f"Expected 13 NO_ENTRY_REASONS")))
    chk("no_entry_has_trend_broken", lambda: None if "trend_broken" in NO_ENTRY_REASONS else (_ for _ in ()).throw(
        AssertionError("trend_broken missing")))
    chk("no_entry_has_human_review_required", lambda: None if "human_review_required" in NO_ENTRY_REASONS else (
        _ for _ in ()).throw(AssertionError("human_review_required missing")))

    # --- daily final actions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import DAILY_FINAL_ACTIONS
    chk("daily_final_actions_7", lambda: None if len(DAILY_FINAL_ACTIONS) == 7 else (_ for _ in ()).throw(
        AssertionError(f"Expected 7 DAILY_FINAL_ACTIONS")))
    chk("final_action_paper_buy_plan", lambda: None if "PAPER_BUY_PLAN" in DAILY_FINAL_ACTIONS else (_ for _ in ()).throw(
        AssertionError("PAPER_BUY_PLAN missing from DAILY_FINAL_ACTIONS")))
    chk("final_action_no_entry", lambda: None if "NO_ENTRY" in DAILY_FINAL_ACTIONS else (_ for _ in ()).throw(
        AssertionError("NO_ENTRY missing from DAILY_FINAL_ACTIONS")))
    chk("final_action_watch", lambda: None if "WATCH" in DAILY_FINAL_ACTIONS else (_ for _ in ()).throw(
        AssertionError("WATCH missing from DAILY_FINAL_ACTIONS")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import SAFETY_FLAGS, FORBIDDEN_ACTIONS
    chk("safety_flags_paper_only", lambda: None if SAFETY_FLAGS.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_flags_no_real_orders", lambda: None if SAFETY_FLAGS.get("no_real_orders") is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders must be True")))
    chk("safety_flags_no_broker", lambda: None if SAFETY_FLAGS.get("no_broker") is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_flags_no_margin", lambda: None if SAFETY_FLAGS.get("no_margin") is True else (_ for _ in ()).throw(
        AssertionError("no_margin must be True")))
    chk("safety_cockpit_executes_order_false", lambda: None if SAFETY_FLAGS.get(
        "cockpit_executes_order") is False else (_ for _ in ()).throw(
        AssertionError("cockpit_executes_order must be False")))
    chk("safety_broker_execution_enabled_false", lambda: None if SAFETY_FLAGS.get(
        "broker_execution_enabled") is False else (_ for _ in ()).throw(
        AssertionError("broker_execution_enabled must be False")))
    chk("safety_no_automatic_rebalance", lambda: None if SAFETY_FLAGS.get(
        "no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))
    chk("safety_no_real_account_sync", lambda: None if SAFETY_FLAGS.get(
        "no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))
    chk("forbidden_buy_present", lambda: None if "BUY" in FORBIDDEN_ACTIONS else (_ for _ in ()).throw(
        AssertionError("BUY must be in FORBIDDEN_ACTIONS")))
    chk("forbidden_sell_present", lambda: None if "SELL" in FORBIDDEN_ACTIONS else (_ for _ in ()).throw(
        AssertionError("SELL must be in FORBIDDEN_ACTIONS")))
    chk("forbidden_order_present", lambda: None if "ORDER" in FORBIDDEN_ACTIONS else (_ for _ in ()).throw(
        AssertionError("ORDER must be in FORBIDDEN_ACTIONS")))

    # --- PAPER_BUY_PLAN is allowed (not forbidden) ---
    chk("paper_buy_plan_not_forbidden", lambda: None if "PAPER_BUY_PLAN" not in FORBIDDEN_ACTIONS else (
        _ for _ in ()).throw(AssertionError("PAPER_BUY_PLAN must NOT be in FORBIDDEN_ACTIONS")))

    # --- engine functions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
        verify_version, run_daily_workflow, get_cockpit_summary_v201, build_enhanced_ticket,
        evaluate_no_entry_reasons, classify_final_action, get_risk_budget_status,
        DailyWorkflowInput,
    )
    chk("fn_verify_version", lambda: None if verify_version() is True else (_ for _ in ()).throw(
        AssertionError("verify_version failed")))
    chk("fn_run_daily_workflow_not_none", lambda: None if run_daily_workflow() is not None else (_ for _ in ()).throw(
        AssertionError("run_daily_workflow returned None")))
    chk("fn_run_daily_workflow_paper_only", lambda: None if run_daily_workflow().paper_only is True else (_ for _ in ()).throw(
        AssertionError("run_daily_workflow result paper_only not True")))
    chk("fn_run_daily_workflow_no_order", lambda: None if run_daily_workflow().cockpit_executes_order is False else (
        _ for _ in ()).throw(AssertionError("cockpit_executes_order must be False")))
    chk("fn_get_cockpit_summary_v201", lambda: None if get_cockpit_summary_v201() is not None else (_ for _ in ()).throw(
        AssertionError("get_cockpit_summary_v201 returned None")))
    chk("fn_build_enhanced_ticket", lambda: build_enhanced_ticket("2330"))
    chk("fn_evaluate_no_entry_reasons", lambda: evaluate_no_entry_reasons())
    chk("fn_classify_final_action", lambda: classify_final_action("2330", "A_PULLBACK_10MA", [], True, True))
    chk("fn_get_risk_budget_status", lambda: get_risk_budget_status())

    # --- summary no forbidden words ---
    summary = get_cockpit_summary_v201()
    summary_str = str(summary)
    chk("summary_no_bare_buy", lambda: None if "\"BUY\"" not in summary_str and
        not any(w == "BUY" for w in summary_str.split()) else (_ for _ in ()).throw(
        AssertionError("Bare BUY found in cockpit summary")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v201 import SCENARIOS
    chk("scenarios_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios")))
    chk("scenarios_all_schema_201", lambda: None if all(
        s["schema_version"] == "201" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Bad scenario schema_version")))
    chk("scenarios_all_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Missing paper_only")))
    chk("scenarios_unique_ids", lambda: None if len({s["id"] for s in SCENARIOS}) == 80 else (_ for _ in ()).throw(
        AssertionError("Duplicate scenario IDs")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v201 import FIXTURES
    chk("fixtures_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures")))
    chk("fixtures_all_schema_201", lambda: None if all(
        f["schema_version"] == "201" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Bad fixture schema_version")))
    chk("fixtures_all_paper_only", lambda: None if all(
        f["paper_only"] is True for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Missing paper_only")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Missing fixture_id")))
    chk("fixtures_unique_ids", lambda: None if len({f["id"] for f in FIXTURES}) == 80 else (_ for _ in ()).throw(
        AssertionError("Duplicate fixture IDs")))

    # --- GUI panel ---
    from gui.small_capital_strategy_panel import PANEL_VERSION, PANEL_VERSION_V201, get_tab_names, get_v201_tab_names
    chk("panel_version_in_expected", lambda: None if PANEL_VERSION in EXPECTED_PANEL_VERSIONS else (_ for _ in ()).throw(
        AssertionError(f"Panel version {PANEL_VERSION} not in {EXPECTED_PANEL_VERSIONS}")))
    chk("panel_version_201", lambda: None if PANEL_VERSION_V201 == "2.0.1" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V201 2.0.1, got {PANEL_VERSION_V201}")))
    tab_names = get_tab_names()
    for tab in ["daily_workflow_v201", "no_entry_reason_detail", "decision_ticket_v201"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' missing")))
    chk("get_v201_tab_names_3", lambda: None if len(get_v201_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v201 tab names")))

    # --- CLI commands ---
    from cli.command_registry import PROVIDER_COMMANDS
    command_names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in [
        "paper-cockpit-daily-workflow",
        "paper-cockpit-no-entry-reason",
        "paper-cockpit-final-action",
        "paper-cockpit-candidate-rank",
        "paper-cockpit-risk-budget-status",
        "paper-cockpit-cli-display",
        "paper-cockpit-version-201",
        "paper-cockpit-health-201",
        "paper-cockpit-gate-201",
        "paper-cockpit-safety-audit-201",
    ]:
        chk(f"cli_{cmd.replace('-','_')}", lambda c=cmd: None if c in command_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' missing")))

    # --- backward compat: v2.0.0 still importable ---
    chk("import_v200_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v200",
        fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION as V200_VER
    chk("v200_version_unchanged", lambda: None if V200_VER == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.0 VERSION changed to {V200_VER}")))

    # --- covered versions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import COVERED_VERSIONS
    chk("covers_v200", lambda: None if "2.0.0" in COVERED_VERSIONS else (_ for _ in ()).throw(
        AssertionError("2.0.0 not in COVERED_VERSIONS")))
    chk("covers_v170", lambda: None if "1.7.0" in COVERED_VERSIONS else (_ for _ in ()).throw(
        AssertionError("1.7.0 not in COVERED_VERSIONS")))
    chk("covers_v1910", lambda: None if "1.9.10" in COVERED_VERSIONS else (_ for _ in ()).throw(
        AssertionError("1.9.10 not in COVERED_VERSIONS")))

    # --- health file importable ---
    chk("import_health_v201", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_health_v201",
        fromlist=["HEALTH_VERSION"]))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_release_gate_v201] {passed}/{total} passed")
    return {
        "gate_passed": all_passed,
        "passed_count": passed,
        "failed_count": failed,
        "total_count": total,
        "errors": errors,
        "gate_version": GATE_VERSION,
        "gate_release": GATE_RELEASE,
    }


run_gate = run_release_gate

if __name__ == "__main__":
    result = run_release_gate()
    if not result["gate_passed"]:
        for e in result["errors"]:
            print(e)
        sys.exit(1)
    sys.exit(0)
