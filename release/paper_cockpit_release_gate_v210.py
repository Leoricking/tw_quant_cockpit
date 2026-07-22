"""
release/paper_cockpit_release_gate_v210.py
v2.0.10 Paper Exit Plan & Stop-Loss Discipline Control — Release Gate
[!] Paper Only. Research Only. Exit Plan Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

GATE_VERSION = "2.0.10"
GATE_RELEASE = "Paper Exit Plan & Stop-Loss Discipline Control"
BASELINE_TESTS = 35313
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = (
    "2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4",
    "2.0.5", "2.0.6", "2.0.7", "2.0.8", "2.0.9", "2.0.10",
)


def run_release_gate():
    """Run all release gate checks for v2.0.10. Returns result dict."""
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
    chk("gate_version_210", lambda: None if GATE_VERSION == "2.0.10" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.10")))
    chk("baseline_tests_35313", lambda: None if BASELINE_TESTS == 35313 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 35313")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import VERSION, SCHEMA_VERSION
    chk("module_version_210", lambda: None if VERSION == "2.0.10" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.10, got {VERSION}")))
    chk("schema_version_210", lambda: None if SCHEMA_VERSION == "210" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 210, got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import SAFETY_FLAGS_V210
    chk("safety_flags_count_23", lambda: None if len(SAFETY_FLAGS_V210) == 23 else (_ for _ in ()).throw(
        AssertionError(f"Expected 23 SAFETY_FLAGS_V210, got {len(SAFETY_FLAGS_V210)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V210["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V210["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V210["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_exit_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V210["exit_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("exit_actions_recommendation_only must be True")))
    chk("safety_require_stop_loss_before_entry_always_true", lambda: None if SAFETY_FLAGS_V210["require_stop_loss_before_entry_always_true"] is True else (_ for _ in ()).throw(
        AssertionError("require_stop_loss_before_entry_always_true must be True")))
    chk("safety_no_automatic_exit_apply", lambda: None if SAFETY_FLAGS_V210["no_automatic_exit_apply"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_exit_apply must be True")))
    chk("safety_no_automatic_stop_loss", lambda: None if SAFETY_FLAGS_V210["no_automatic_stop_loss_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_stop_loss_execution must be True")))
    chk("safety_no_automatic_take_profit", lambda: None if SAFETY_FLAGS_V210["no_automatic_take_profit_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_take_profit_execution must be True")))

    # --- exit plan engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    chk("run_exit_plan_review_callable", lambda: run_exit_plan_review())
    chk("run_exit_plan_review_paper_only", lambda: None if run_exit_plan_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("run_exit_plan_review_all_passed", lambda: None if run_exit_plan_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("run_exit_plan_review_should_auto_apply_false", lambda: None if run_exit_plan_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))
    chk("run_exit_plan_review_auto_apply_enabled_false", lambda: None if run_exit_plan_review().auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))

    # --- exit plan policy callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import ExitPlanPolicy
    chk("exit_plan_policy_callable", lambda: ExitPlanPolicy())
    chk("exit_plan_policy_auto_apply_always_false", lambda: None if ExitPlanPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must always be False")))
    chk("exit_plan_policy_require_stop_always_true", lambda: None if ExitPlanPolicy(require_stop_loss_before_entry=False).require_stop_loss_before_entry is True else (_ for _ in ()).throw(
        AssertionError("require_stop_loss_before_entry must always be True")))

    # --- candidate exit plan schema callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import CandidateExitPlan
    chk("candidate_exit_plan_callable", lambda: CandidateExitPlan())
    chk("candidate_exit_plan_should_auto_apply_false", lambda: None if CandidateExitPlan(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("CandidateExitPlan.should_auto_apply must always be False")))

    # --- stop discipline summary callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import StopDisciplineSummary
    chk("stop_discipline_summary_callable", lambda: StopDisciplineSummary())

    # --- evaluate_stop_discipline callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_stop_discipline
    chk("evaluate_stop_discipline_callable", lambda: evaluate_stop_discipline())
    chk("evaluate_stop_discipline_paper_only", lambda: None if evaluate_stop_discipline()["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("evaluate_stop_discipline paper_only must be True")))

    # --- evaluate_reward_risk callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import evaluate_reward_risk
    chk("evaluate_reward_risk_callable", lambda: evaluate_reward_risk())
    chk("evaluate_reward_risk_schema", lambda: None if evaluate_reward_risk()["schema_version"] == "210" else (_ for _ in ()).throw(
        AssertionError("evaluate_reward_risk schema_version must be 210")))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import (
        export_exit_plan_json, export_exit_plan_markdown,
        export_candidate_exit_csv, export_stop_discipline_csv,
        export_exit_warning_csv, export_exit_audit_snapshot,
    )
    result = run_exit_plan_review()
    chk("export_json_valid", lambda: None if export_exit_plan_json(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_exit_plan_json is_valid must be True")))
    chk("export_md_valid", lambda: None if export_exit_plan_markdown(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_exit_plan_markdown is_valid must be True")))
    chk("export_candidate_csv_valid", lambda: None if export_candidate_exit_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_candidate_exit_csv is_valid must be True")))
    chk("export_stop_discipline_csv_valid", lambda: None if export_stop_discipline_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_stop_discipline_csv is_valid must be True")))
    chk("export_exit_warning_csv_valid", lambda: None if export_exit_warning_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_exit_warning_csv is_valid must be True")))
    chk("export_audit_snapshot_complete", lambda: None if export_exit_audit_snapshot(result).export_status == "complete" else (_ for _ in ()).throw(
        AssertionError("export_exit_audit_snapshot export_status must be 'complete'")))

    # --- CLI handler resolution ---
    chk("main_importable", lambda: __import__("main", fromlist=["cmd_paper_cockpit_v210_review_exit_plan"]))
    import main as _main_module
    for handler_name in [
        "cmd_paper_cockpit_v210_review_exit_plan",
        "cmd_paper_cockpit_v210_evaluate_stop_discipline",
        "cmd_paper_cockpit_v210_build_exit_warning_queue",
        "cmd_paper_cockpit_v210_build_stop_violation_queue",
        "cmd_paper_cockpit_v210_evaluate_reward_risk",
        "cmd_paper_cockpit_v210_export_json",
        "cmd_paper_cockpit_v210_export_md",
        "cmd_paper_cockpit_v210_export_csv",
        "cmd_paper_cockpit_v210_health",
        "cmd_paper_cockpit_v210_gate",
    ]:
        chk(f"main_handler_{handler_name}", lambda n=handler_name: None if hasattr(_main_module, n) and callable(getattr(_main_module, n)) else (
            _ for _ in ()).throw(AssertionError(f"main.py handler '{n}' missing or not callable")))

    # --- no fake isolated command_map ---
    chk("no_fake_isolated_command_map", lambda: None if not hasattr(_main_module, "_ISOLATED_V210_COMMAND_MAP") else (_ for _ in ()).throw(
        AssertionError("main.py must not have isolated command_map for v210")))

    # --- CLI registration health ---
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v210-review-exit-plan",
        "paper-cockpit-v210-evaluate-stop-discipline",
        "paper-cockpit-v210-build-exit-warning-queue",
        "paper-cockpit-v210-build-stop-violation-queue",
        "paper-cockpit-v210-evaluate-reward-risk",
        "paper-cockpit-v210-export-json",
        "paper-cockpit-v210-export-md",
        "paper-cockpit-v210-export-csv",
        "paper-cockpit-v210-health",
        "paper-cockpit-v210-gate",
    ]:
        chk(f"cli_registry_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- GUI import safe ---
    from gui.small_capital_strategy_panel import PANEL_VERSION_V210, get_v210_tab_names, render_all_tabs
    chk("panel_version_210", lambda: None if PANEL_VERSION_V210 == "2.0.10" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V210 2.0.10, got {PANEL_VERSION_V210}")))
    chk("get_v210_tab_names_3", lambda: None if len(get_v210_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v210 tab names, got {len(get_v210_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    render_result = render_all_tabs()
    for tab in ["exit_plan_v210", "stop_discipline_v210", "exit_warning_queue_v210"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' rendered with error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_no_global_errors", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has error tabs: {error_tabs}")))

    # --- paper-only safety ---
    chk("paper_only_safety_snapshot_true", lambda: None if run_exit_plan_review().paper_only_safety_snapshot is True else (_ for _ in ()).throw(
        AssertionError("paper_only_safety_snapshot must be True")))
    chk("auto_apply_enabled_always_false_gate", lambda: None if SAFETY_FLAGS_V210.get("auto_apply_enabled_always_false") is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("should_auto_apply_always_false_gate", lambda: None if SAFETY_FLAGS_V210.get("should_auto_apply_always_false") is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("no_broker_gate", lambda: None if SAFETY_FLAGS_V210.get("no_broker") is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("no_real_orders_gate", lambda: None if SAFETY_FLAGS_V210.get("no_real_orders") is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders must be True")))

    # --- backward compatibility with v2.0.9 ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import VERSION as V209, run_sizing_review
    chk("v209_version_unchanged", lambda: None if V209 == "2.0.9" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.9 VERSION changed to {V209}")))
    chk("v209_run_sizing_review_callable", lambda: run_sizing_review())

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found via relative path")))

    # --- scenarios and fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v210 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v210 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_release_gate_v210] {passed}/{total} passed")
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
