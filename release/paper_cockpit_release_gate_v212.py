"""
release/paper_cockpit_release_gate_v212.py
v2.0.12 Paper Profit Taking & ETF Rebalancing Control — Release Gate
[!] Paper Only. Research Only. Profit Taking Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

GATE_VERSION = "2.0.12"
GATE_RELEASE = "Paper Profit Taking & ETF Rebalancing Control"
BASELINE_TESTS = 36361
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = (
    "2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4",
    "2.0.5", "2.0.6", "2.0.7", "2.0.8", "2.0.9", "2.0.10", "2.0.11", "2.0.12",
)


def run_release_gate():
    """Run all release gate checks for v2.0.12. Returns result dict."""
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
    chk("gate_version_212", lambda: None if GATE_VERSION == "2.0.12" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.12")))
    chk("baseline_tests_36361", lambda: None if BASELINE_TESTS == 36361 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 36361")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import VERSION, SCHEMA_VERSION
    chk("module_version_212", lambda: None if VERSION == "2.0.12" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.12, got {VERSION}")))
    chk("schema_version_212", lambda: None if SCHEMA_VERSION == "212" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 212, got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    chk("safety_flags_count_25", lambda: None if len(SAFETY_FLAGS_V212) == 25 else (_ for _ in ()).throw(
        AssertionError(f"Expected 25 SAFETY_FLAGS_V212, got {len(SAFETY_FLAGS_V212)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V212["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V212["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V212["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_profit_taking_recommendation_only", lambda: None if SAFETY_FLAGS_V212["profit_taking_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("profit_taking_recommendation_only must be True")))
    chk("safety_etf_rebalance_recommendation_only", lambda: None if SAFETY_FLAGS_V212["etf_rebalance_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("etf_rebalance_recommendation_only must be True")))
    chk("safety_no_automatic_profit_taking_action", lambda: None if SAFETY_FLAGS_V212["no_automatic_profit_taking_action"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_profit_taking_action must be True")))
    chk("safety_no_automatic_stop_loss", lambda: None if SAFETY_FLAGS_V212["no_automatic_stop_loss_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_stop_loss_execution must be True")))
    chk("safety_no_automatic_take_profit", lambda: None if SAFETY_FLAGS_V212["no_automatic_take_profit_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_take_profit_execution must be True")))
    chk("safety_require_profit_plan_always_true", lambda: None if SAFETY_FLAGS_V212["require_profit_plan_before_entry_always_true"] is True else (_ for _ in ()).throw(
        AssertionError("require_profit_plan_before_entry_always_true must be True")))
    chk("safety_profit_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V212["profit_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("profit_actions_recommendation_only must be True")))
    chk("safety_etf_rebalance_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V212["etf_rebalance_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("etf_rebalance_actions_recommendation_only must be True")))

    # --- profit taking engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    chk("run_profit_taking_review_callable", lambda: run_profit_taking_review())
    chk("run_profit_taking_review_paper_only", lambda: None if run_profit_taking_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("run_profit_taking_review_all_passed", lambda: None if run_profit_taking_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("run_profit_taking_review_should_auto_apply_false", lambda: None if run_profit_taking_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))
    chk("run_profit_taking_review_auto_apply_enabled_false", lambda: None if run_profit_taking_review().auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))

    # --- profit taking policy callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingPolicy
    chk("profit_taking_policy_callable", lambda: ProfitTakingPolicy())
    chk("policy_auto_apply_always_false", lambda: None if ProfitTakingPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must always be False")))
    chk("policy_require_profit_plan_always_true", lambda: None if ProfitTakingPolicy(require_profit_plan_before_entry=False).require_profit_plan_before_entry is True else (_ for _ in ()).throw(
        AssertionError("require_profit_plan_before_entry must always be True")))

    # --- candidate profit plan schema callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CandidateProfitPlan
    chk("candidate_profit_plan_callable", lambda: CandidateProfitPlan())
    chk("candidate_plan_should_auto_apply_false", lambda: None if CandidateProfitPlan(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("CandidateProfitPlan.should_auto_apply must always be False")))

    # --- ETF rebalancing engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    chk("evaluate_etf_rebalancing_callable", lambda: evaluate_etf_rebalancing(
        "0050", "台灣50", 0.40, 0.43, 0.50, 0.35, False))
    chk("evaluate_etf_rebalancing_paper_only", lambda: None if evaluate_etf_rebalancing(
        "0050", "台灣50", 0.40, 0.43, 0.50, 0.35, False
    ).paper_only is True else (_ for _ in ()).throw(AssertionError("paper_only must be True")))

    # --- ETF rebalancing item schema callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ETFRebalancingItem
    chk("etf_rebalancing_item_callable", lambda: ETFRebalancingItem())
    chk("etf_item_should_auto_apply_false", lambda: None if ETFRebalancingItem(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("ETFRebalancingItem.should_auto_apply must always be False")))

    # --- profit taking summary callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingSummary
    chk("profit_taking_summary_callable", lambda: ProfitTakingSummary())

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import (
        export_profit_taking_json, export_profit_taking_markdown,
        export_candidate_profit_plan_csv, export_etf_rebalancing_csv,
        export_profit_warning_queue_csv, export_giveback_review_queue_csv,
        export_profit_taking_audit_snapshot,
    )
    result = run_profit_taking_review()
    chk("export_json_valid", lambda: None if export_profit_taking_json(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_profit_taking_json is_valid must be True")))
    chk("export_md_valid", lambda: None if export_profit_taking_markdown(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_profit_taking_markdown is_valid must be True")))
    chk("export_candidate_csv_valid", lambda: None if export_candidate_profit_plan_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_candidate_profit_plan_csv is_valid must be True")))
    chk("export_etf_csv_valid", lambda: None if export_etf_rebalancing_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_etf_rebalancing_csv is_valid must be True")))
    chk("export_warning_csv_valid", lambda: None if export_profit_warning_queue_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_profit_warning_queue_csv is_valid must be True")))
    chk("export_giveback_csv_valid", lambda: None if export_giveback_review_queue_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_giveback_review_queue_csv is_valid must be True")))
    chk("export_audit_snapshot_complete", lambda: None if export_profit_taking_audit_snapshot(result).export_status == "complete" else (_ for _ in ()).throw(
        AssertionError("export_profit_taking_audit_snapshot export_status must be 'complete'")))

    # --- CLI handler resolution ---
    chk("main_importable", lambda: __import__("main", fromlist=["cmd_paper_cockpit_v212_review_profit_taking"]))
    import main as _main_module
    for handler_name in [
        "cmd_paper_cockpit_v212_review_profit_taking",
        "cmd_paper_cockpit_v212_evaluate_giveback_risk",
        "cmd_paper_cockpit_v212_build_profit_warning_queue",
        "cmd_paper_cockpit_v212_build_giveback_review_queue",
        "cmd_paper_cockpit_v212_review_etf_rebalancing",
        "cmd_paper_cockpit_v212_export_json",
        "cmd_paper_cockpit_v212_export_md",
        "cmd_paper_cockpit_v212_export_csv",
        "cmd_paper_cockpit_v212_health",
        "cmd_paper_cockpit_v212_gate",
    ]:
        chk(f"main_handler_{handler_name}", lambda n=handler_name: None if hasattr(_main_module, n) and callable(getattr(_main_module, n)) else (
            _ for _ in ()).throw(AssertionError(f"main.py handler '{n}' missing or not callable")))

    # --- no fake isolated command_map ---
    chk("no_fake_isolated_command_map", lambda: None if not hasattr(_main_module, "_ISOLATED_V212_COMMAND_MAP") else (_ for _ in ()).throw(
        AssertionError("main.py must not have isolated command_map for v212")))

    # --- CLI registration health ---
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v212-review-profit-taking",
        "paper-cockpit-v212-evaluate-giveback-risk",
        "paper-cockpit-v212-build-profit-warning-queue",
        "paper-cockpit-v212-build-giveback-review-queue",
        "paper-cockpit-v212-review-etf-rebalancing",
        "paper-cockpit-v212-export-json",
        "paper-cockpit-v212-export-md",
        "paper-cockpit-v212-export-csv",
        "paper-cockpit-v212-health",
        "paper-cockpit-v212-gate",
    ]:
        chk(f"cli_registry_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- GUI import safe ---
    from gui.small_capital_strategy_panel import PANEL_VERSION_V212, get_v212_tab_names, render_all_tabs
    chk("panel_version_212", lambda: None if PANEL_VERSION_V212 == "2.0.12" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V212 2.0.12, got {PANEL_VERSION_V212}")))
    chk("get_v212_tab_names_3", lambda: None if len(get_v212_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v212 tab names, got {len(get_v212_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    render_result = render_all_tabs()
    for tab in ["profit_taking_v212", "etf_rebalancing_v212", "giveback_review_queue_v212"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' rendered with error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_no_global_errors", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has error tabs: {error_tabs}")))

    # --- paper-only safety ---
    chk("paper_only_safety_snapshot_true", lambda: None if run_profit_taking_review().paper_only_safety_snapshot is True else (_ for _ in ()).throw(
        AssertionError("paper_only_safety_snapshot must be True")))
    chk("auto_apply_enabled_always_false_gate", lambda: None if SAFETY_FLAGS_V212.get("auto_apply_enabled_always_false") is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("should_auto_apply_always_false_gate", lambda: None if SAFETY_FLAGS_V212.get("should_auto_apply_always_false") is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("no_broker_gate", lambda: None if SAFETY_FLAGS_V212.get("no_broker") is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("no_real_orders_gate", lambda: None if SAFETY_FLAGS_V212.get("no_real_orders") is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders must be True")))
    chk("profit_actions_recommendation_only_gate", lambda: None if SAFETY_FLAGS_V212.get("profit_actions_recommendation_only") is True else (_ for _ in ()).throw(
        AssertionError("profit_actions_recommendation_only must be True")))
    chk("etf_rebalance_actions_recommendation_only_gate", lambda: None if SAFETY_FLAGS_V212.get("etf_rebalance_actions_recommendation_only") is True else (_ for _ in ()).throw(
        AssertionError("etf_rebalance_actions_recommendation_only must be True")))

    # --- backward compatibility with v2.0.11 ---
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VERSION as V211, run_journal_review
    chk("v211_version_unchanged", lambda: None if V211 == "2.0.11" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.11 VERSION changed to {V211}")))
    chk("v211_run_journal_review_callable", lambda: run_journal_review())

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found via relative path")))

    # --- scenarios and fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v212 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v212 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_release_gate_v212] {passed}/{total} passed")
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
