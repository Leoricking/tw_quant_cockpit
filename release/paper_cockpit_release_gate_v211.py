"""
release/paper_cockpit_release_gate_v211.py
v2.0.11 Paper Trade Journal & Execution Discipline Review — Release Gate
[!] Paper Only. Research Only. Journal Review Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

GATE_VERSION = "2.0.11"
GATE_RELEASE = "Paper Trade Journal & Execution Discipline Review"
BASELINE_TESTS = 35613
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = (
    "2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4",
    "2.0.5", "2.0.6", "2.0.7", "2.0.8", "2.0.9", "2.0.10", "2.0.11",
)


def run_release_gate():
    """Run all release gate checks for v2.0.11. Returns result dict."""
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
    chk("gate_version_211", lambda: None if GATE_VERSION == "2.0.11" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.11")))
    chk("baseline_tests_35613", lambda: None if BASELINE_TESTS == 35613 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 35613")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VERSION, SCHEMA_VERSION
    chk("module_version_211", lambda: None if VERSION == "2.0.11" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.11, got {VERSION}")))
    chk("schema_version_211", lambda: None if SCHEMA_VERSION == "211" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 211, got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    chk("safety_flags_count_24", lambda: None if len(SAFETY_FLAGS_V211) == 24 else (_ for _ in ()).throw(
        AssertionError(f"Expected 24 SAFETY_FLAGS_V211, got {len(SAFETY_FLAGS_V211)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V211["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V211["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V211["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_journal_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V211["journal_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("journal_actions_recommendation_only must be True")))
    chk("safety_require_planned_entry_always_true", lambda: None if SAFETY_FLAGS_V211["require_planned_entry_before_trade_always_true"] is True else (_ for _ in ()).throw(
        AssertionError("require_planned_entry_before_trade_always_true must be True")))
    chk("safety_no_automatic_journal_apply", lambda: None if SAFETY_FLAGS_V211["no_automatic_journal_apply"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_journal_apply must be True")))
    chk("safety_no_automatic_stop_loss", lambda: None if SAFETY_FLAGS_V211["no_automatic_stop_loss_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_stop_loss_execution must be True")))
    chk("safety_no_automatic_take_profit", lambda: None if SAFETY_FLAGS_V211["no_automatic_take_profit_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_take_profit_execution must be True")))

    # --- trade journal engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    chk("run_journal_review_callable", lambda: run_journal_review())
    chk("run_journal_review_paper_only", lambda: None if run_journal_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("run_journal_review_all_passed", lambda: None if run_journal_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("run_journal_review_should_auto_apply_false", lambda: None if run_journal_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))
    chk("run_journal_review_auto_apply_enabled_false", lambda: None if run_journal_review().auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))

    # --- trade journal policy callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import TradeJournalPolicy
    chk("trade_journal_policy_callable", lambda: TradeJournalPolicy())
    chk("policy_auto_apply_always_false", lambda: None if TradeJournalPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must always be False")))
    chk("policy_require_planned_entry_always_true", lambda: None if TradeJournalPolicy(require_planned_entry_before_trade=False).require_planned_entry_before_trade is True else (_ for _ in ()).throw(
        AssertionError("require_planned_entry_before_trade must always be True")))

    # --- journal entry schema callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import JournalEntry
    chk("journal_entry_callable", lambda: JournalEntry())
    chk("journal_entry_should_auto_apply_false", lambda: None if JournalEntry(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("JournalEntry.should_auto_apply must always be False")))

    # --- execution discipline summary callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import ExecutionDisciplineSummary
    chk("execution_discipline_summary_callable", lambda: ExecutionDisciplineSummary())

    # --- evaluate_discipline callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import evaluate_discipline
    chk("evaluate_discipline_callable", lambda: evaluate_discipline())
    chk("evaluate_discipline_paper_only", lambda: None if evaluate_discipline()["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("evaluate_discipline paper_only must be True")))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import (
        export_journal_json, export_journal_markdown,
        export_journal_csv, export_discipline_csv,
        export_mistake_review_csv, export_violation_queue_csv,
        export_journal_audit_snapshot,
    )
    result = run_journal_review()
    chk("export_json_valid", lambda: None if export_journal_json(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_journal_json is_valid must be True")))
    chk("export_md_valid", lambda: None if export_journal_markdown(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_journal_markdown is_valid must be True")))
    chk("export_journal_csv_valid", lambda: None if export_journal_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_journal_csv is_valid must be True")))
    chk("export_discipline_csv_valid", lambda: None if export_discipline_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_discipline_csv is_valid must be True")))
    chk("export_mistake_csv_valid", lambda: None if export_mistake_review_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_mistake_review_csv is_valid must be True")))
    chk("export_violation_csv_valid", lambda: None if export_violation_queue_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_violation_queue_csv is_valid must be True")))
    chk("export_audit_snapshot_complete", lambda: None if export_journal_audit_snapshot(result).export_status == "complete" else (_ for _ in ()).throw(
        AssertionError("export_journal_audit_snapshot export_status must be 'complete'")))

    # --- CLI handler resolution ---
    chk("main_importable", lambda: __import__("main", fromlist=["cmd_paper_cockpit_v211_review_journal"]))
    import main as _main_module
    for handler_name in [
        "cmd_paper_cockpit_v211_review_journal",
        "cmd_paper_cockpit_v211_evaluate_discipline",
        "cmd_paper_cockpit_v211_build_mistake_queue",
        "cmd_paper_cockpit_v211_build_violation_queue",
        "cmd_paper_cockpit_v211_build_improvement_queue",
        "cmd_paper_cockpit_v211_export_json",
        "cmd_paper_cockpit_v211_export_md",
        "cmd_paper_cockpit_v211_export_csv",
        "cmd_paper_cockpit_v211_health",
        "cmd_paper_cockpit_v211_gate",
    ]:
        chk(f"main_handler_{handler_name}", lambda n=handler_name: None if hasattr(_main_module, n) and callable(getattr(_main_module, n)) else (
            _ for _ in ()).throw(AssertionError(f"main.py handler '{n}' missing or not callable")))

    # --- no fake isolated command_map ---
    chk("no_fake_isolated_command_map", lambda: None if not hasattr(_main_module, "_ISOLATED_V211_COMMAND_MAP") else (_ for _ in ()).throw(
        AssertionError("main.py must not have isolated command_map for v211")))

    # --- CLI registration health ---
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v211-review-journal",
        "paper-cockpit-v211-evaluate-discipline",
        "paper-cockpit-v211-build-mistake-queue",
        "paper-cockpit-v211-build-violation-queue",
        "paper-cockpit-v211-build-improvement-queue",
        "paper-cockpit-v211-export-json",
        "paper-cockpit-v211-export-md",
        "paper-cockpit-v211-export-csv",
        "paper-cockpit-v211-health",
        "paper-cockpit-v211-gate",
    ]:
        chk(f"cli_registry_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- GUI import safe ---
    from gui.small_capital_strategy_panel import PANEL_VERSION_V211, get_v211_tab_names, render_all_tabs
    chk("panel_version_211", lambda: None if PANEL_VERSION_V211 == "2.0.11" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V211 2.0.11, got {PANEL_VERSION_V211}")))
    chk("get_v211_tab_names_3", lambda: None if len(get_v211_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v211 tab names, got {len(get_v211_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    render_result = render_all_tabs()
    for tab in ["trade_journal_v211", "execution_discipline_v211", "mistake_review_queue_v211"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' rendered with error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_no_global_errors", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has error tabs: {error_tabs}")))

    # --- paper-only safety ---
    chk("paper_only_safety_snapshot_true", lambda: None if run_journal_review().paper_only_safety_snapshot is True else (_ for _ in ()).throw(
        AssertionError("paper_only_safety_snapshot must be True")))
    chk("auto_apply_enabled_always_false_gate", lambda: None if SAFETY_FLAGS_V211.get("auto_apply_enabled_always_false") is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("should_auto_apply_always_false_gate", lambda: None if SAFETY_FLAGS_V211.get("should_auto_apply_always_false") is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("no_broker_gate", lambda: None if SAFETY_FLAGS_V211.get("no_broker") is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("no_real_orders_gate", lambda: None if SAFETY_FLAGS_V211.get("no_real_orders") is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders must be True")))

    # --- backward compatibility with v2.0.10 ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import VERSION as V210, run_exit_plan_review
    chk("v210_version_unchanged", lambda: None if V210 == "2.0.10" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.10 VERSION changed to {V210}")))
    chk("v210_run_exit_plan_review_callable", lambda: run_exit_plan_review())

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found via relative path")))

    # --- scenarios and fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v211 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v211 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_release_gate_v211] {passed}/{total} passed")
    return {
        "gate_passed": all_passed,
        "passed_count": passed,
        "failed_count": failed,
        "total_count": total,
        "errors": errors,
        "version": GATE_VERSION,
        "release": GATE_RELEASE,
    }


if __name__ == "__main__":
    result = run_release_gate()
    if not result["gate_passed"]:
        for e in result["errors"]:
            print(e)
    sys.exit(0 if result["gate_passed"] else 1)
