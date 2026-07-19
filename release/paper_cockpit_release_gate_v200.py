"""
release/paper_cockpit_release_gate_v200.py
v2.0.0 Paper Cockpit Unified Entry & Strategy Decision Console — Release Gate
[!] Paper Only. Research Only. Simulate Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))

GATE_VERSION = "2.0.0"
GATE_RELEASE = "Paper Cockpit Unified Entry & Strategy Decision Console"
BASELINE_TESTS = 31925
MIN_NEW_TESTS = 500
EXPECTED_PANEL_VERSIONS = (
    "1.9.10", "2.0.0",
)


def run_release_gate():
    """Run all release gate checks for v2.0.0. Returns result dict."""
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

    # --- version checks ---
    chk("gate_version_200", lambda: None if GATE_VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.0")))
    chk("baseline_tests_31925", lambda: None if BASELINE_TESTS == 31925 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 31925")))
    chk("min_new_tests_500", lambda: None if MIN_NEW_TESTS == 500 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 500")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION, SCHEMA_VERSION
    chk("module_version_200", lambda: None if VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.0")))
    chk("schema_version_200", lambda: None if SCHEMA_VERSION == "200" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 200")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import _ALL_MODEL_NAMES
    chk("models_count_23", lambda: None if len(_ALL_MODEL_NAMES) == 23 else (_ for _ in ()).throw(
        AssertionError(f"Expected 23 models")))

    # --- safety ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import (
        SAFETY_FLAGS, FORBIDDEN_ACTIONS, ALLOWED_ACTIONS, HARD_BLOCK_CONDITIONS,
        NO_ENTRY_CONDITIONS, CLI_COMMANDS, GUI_TABS,
    )
    chk("safety_flags_30", lambda: None if len(SAFETY_FLAGS) == 30 else (_ for _ in ()).throw(
        AssertionError(f"Expected 30 safety flags")))
    chk("forbidden_10", lambda: None if len(FORBIDDEN_ACTIONS) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 forbidden")))
    chk("allowed_9", lambda: None if len(ALLOWED_ACTIONS) == 9 else (_ for _ in ()).throw(
        AssertionError(f"Expected 9 allowed")))
    chk("hard_block_22", lambda: None if len(HARD_BLOCK_CONDITIONS) == 22 else (_ for _ in ()).throw(
        AssertionError(f"Expected 22 hard blocks")))
    chk("no_entry_8", lambda: None if len(NO_ENTRY_CONDITIONS) == 8 else (_ for _ in ()).throw(
        AssertionError(f"Expected 8 no-entry conditions")))
    chk("cli_commands_17", lambda: None if len(CLI_COMMANDS) == 17 else (_ for _ in ()).throw(
        AssertionError(f"Expected 17 CLI")))
    chk("gui_tabs_3", lambda: None if len(GUI_TABS) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI tabs")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_no_real_orders", lambda: None if SAFETY_FLAGS.get("no_real_orders") is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders must be True")))
    chk("safety_cockpit_executes_order_false", lambda: None if SAFETY_FLAGS.get(
        "cockpit_executes_order") is False else (_ for _ in ()).throw(
        AssertionError("cockpit_executes_order must be False")))
    chk("forbidden_buy_present", lambda: None if "BUY" in FORBIDDEN_ACTIONS else (_ for _ in ()).throw(
        AssertionError("BUY must be in FORBIDDEN_ACTIONS")))
    chk("forbidden_sell_present", lambda: None if "SELL" in FORBIDDEN_ACTIONS else (_ for _ in ()).throw(
        AssertionError("SELL must be in FORBIDDEN_ACTIONS")))
    chk("forbidden_order_present", lambda: None if "ORDER" in FORBIDDEN_ACTIONS else (_ for _ in ()).throw(
        AssertionError("ORDER must be in FORBIDDEN_ACTIONS")))
    chk("allowed_paper_watch_only", lambda: None if "PAPER_WATCH_ONLY" in ALLOWED_ACTIONS else (_ for _ in ()).throw(
        AssertionError("PAPER_WATCH_ONLY must be in ALLOWED_ACTIONS")))
    chk("allowed_paper_block_new_entry", lambda: None if "PAPER_BLOCK_NEW_ENTRY" in ALLOWED_ACTIONS else (
        _ for _ in ()).throw(AssertionError("PAPER_BLOCK_NEW_ENTRY must be in ALLOWED_ACTIONS")))

    # --- engine functions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import (
        verify_version, run_cockpit, get_cockpit_summary, validate_cockpit,
        check_portfolio_risk, check_position_sizing, classify_abc, score_candidate,
        score_watchlist, PaperCockpitInput,
    )
    chk("fn_verify_version", lambda: None if verify_version() is True else (_ for _ in ()).throw(
        AssertionError("verify_version failed")))
    chk("fn_run_cockpit_returns_result", lambda: None if run_cockpit() is not None else (_ for _ in ()).throw(
        AssertionError("run_cockpit returned None")))
    chk("fn_run_cockpit_paper_only", lambda: None if run_cockpit().paper_only is True else (_ for _ in ()).throw(
        AssertionError("run_cockpit result paper_only not True")))
    chk("fn_run_cockpit_no_order", lambda: None if run_cockpit().cockpit_executes_order is False else (
        _ for _ in ()).throw(AssertionError("cockpit_executes_order must be False")))
    chk("fn_get_cockpit_summary", lambda: None if get_cockpit_summary() is not None else (_ for _ in ()).throw(
        AssertionError("get_cockpit_summary returned None")))
    chk("fn_validate_default_input", lambda: None if validate_cockpit(PaperCockpitInput()).is_valid is True else (
        _ for _ in ()).throw(AssertionError("Default input validation failed")))
    chk("fn_portfolio_risk_ok_default", lambda: None if check_portfolio_risk().overall_ok is True else (
        _ for _ in ()).throw(AssertionError("Default portfolio risk not ok")))
    chk("fn_sizing_default_ok", lambda: None if check_position_sizing().sizing_ok is True else (_ for _ in ()).throw(
        AssertionError("Default sizing not ok")))
    chk("fn_watchlist_score", lambda: score_watchlist(["2330"]))
    chk("fn_candidate_score", lambda: score_candidate("2330"))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v200 import SCENARIOS
    chk("scenarios_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios")))
    chk("scenarios_all_schema_200", lambda: None if all(
        s["schema_version"] == "200" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Bad scenario schema_version")))
    chk("scenarios_all_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Missing paper_only")))
    chk("scenarios_unique_ids", lambda: None if len({s["id"] for s in SCENARIOS}) == 80 else (_ for _ in ()).throw(
        AssertionError("Duplicate scenario IDs")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v200 import FIXTURES
    chk("fixtures_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures")))
    chk("fixtures_all_schema_200", lambda: None if all(
        f["schema_version"] == "200" for f in FIXTURES) else (_ for _ in ()).throw(
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
    from gui.small_capital_strategy_panel import PANEL_VERSION, get_tab_names, get_cockpit_tab_names
    chk("panel_version_200", lambda: None if PANEL_VERSION in EXPECTED_PANEL_VERSIONS else (_ for _ in ()).throw(
        AssertionError(f"Panel version {PANEL_VERSION} not in {EXPECTED_PANEL_VERSIONS}")))
    tab_names = get_tab_names()
    for tab in ["paper_cockpit", "strategy_decision_console", "decision_ticket"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' missing")))
    chk("get_cockpit_tab_names_3", lambda: None if len(get_cockpit_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 cockpit tab names")))

    # --- CLI ---
    from cli.command_registry import PROVIDER_COMMANDS
    command_names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in [
        "paper-cockpit-version", "paper-cockpit-run", "paper-cockpit-watchlist",
        "paper-cockpit-score", "paper-cockpit-abc-check", "paper-cockpit-risk-check",
        "paper-cockpit-sizing-check", "paper-cockpit-no-entry",
        "paper-cockpit-decision-ticket", "paper-cockpit-dashboard", "paper-cockpit-report",
        "paper-cockpit-export", "paper-cockpit-health", "paper-cockpit-gate",
        "paper-cockpit-scenarios", "paper-cockpit-fixtures", "paper-cockpit-safety-audit",
    ]:
        chk(f"cli_{cmd.replace('-','_')}", lambda c=cmd: None if c in command_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' missing")))

    # --- no forbidden output ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import FORBIDDEN_ACTIONS
    summary = get_cockpit_summary()
    summary_str = str(summary)
    chk("summary_no_buy_word", lambda: None if "BUY" not in summary_str else (_ for _ in ()).throw(
        AssertionError("BUY found in cockpit summary")))
    chk("summary_no_sell_word", lambda: None if "SELL" not in summary_str else (_ for _ in ()).throw(
        AssertionError("SELL found in cockpit summary")))

    # --- safety audit ---
    chk("no_broker_flag_in_safety", lambda: None if SAFETY_FLAGS.get("no_broker") is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("no_margin_flag_in_safety", lambda: None if SAFETY_FLAGS.get("no_margin") is True else (_ for _ in ()).throw(
        AssertionError("no_margin must be True")))
    chk("no_leverage_flag_in_safety", lambda: None if SAFETY_FLAGS.get("no_leverage") is True else (_ for _ in ()).throw(
        AssertionError("no_leverage must be True")))
    chk("not_investment_advice_in_safety", lambda: None if SAFETY_FLAGS.get(
        "not_investment_advice") is True else (_ for _ in ()).throw(
        AssertionError("not_investment_advice must be True")))
    chk("human_review_required_in_safety", lambda: None if SAFETY_FLAGS.get(
        "human_review_required") is True else (_ for _ in ()).throw(
        AssertionError("human_review_required must be True")))

    # --- backward compat ---
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import COVERED_VERSIONS
    chk("covers_v170", lambda: None if "1.7.0" in COVERED_VERSIONS else (_ for _ in ()).throw(
        AssertionError("1.7.0 not in COVERED_VERSIONS")))
    chk("covers_v1910", lambda: None if "1.9.10" in COVERED_VERSIONS else (_ for _ in ()).throw(
        AssertionError("1.9.10 not in COVERED_VERSIONS")))
    chk("covers_v180", lambda: None if "1.8.0" in COVERED_VERSIONS else (_ for _ in ()).throw(
        AssertionError("1.8.0 not in COVERED_VERSIONS")))
    chk("covers_v190", lambda: None if "1.9.0" in COVERED_VERSIONS else (_ for _ in ()).throw(
        AssertionError("1.9.0 not in COVERED_VERSIONS")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_release_gate_v200] {passed}/{total} passed")
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
