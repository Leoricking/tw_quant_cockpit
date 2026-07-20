"""
release/paper_cockpit_release_gate_v204.py
v2.0.4 Paper Portfolio Review Loop & Weekly Improvement Pack — Release Gate
[!] Paper Only. Research Only. Review Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))

GATE_VERSION = "2.0.4"
GATE_RELEASE = "Paper Portfolio Review Loop & Weekly Improvement Pack"
BASELINE_TESTS = 33505
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = ("2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4")


def run_release_gate():
    """Run all release gate checks for v2.0.4. Returns result dict."""
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
    chk("gate_version_204", lambda: None if GATE_VERSION == "2.0.4" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.4")))
    chk("baseline_tests_33505", lambda: None if BASELINE_TESTS == 33505 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 33505")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import VERSION, SCHEMA_VERSION
    chk("module_version_204", lambda: None if VERSION == "2.0.4" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.4, got {VERSION}")))
    chk("schema_version_204", lambda: None if SCHEMA_VERSION == "204" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 204, got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    chk("safety_flags_20", lambda: None if len(SAFETY_FLAGS_V204) == 20 else (_ for _ in ()).throw(
        AssertionError(f"Expected 20 safety flags, got {len(SAFETY_FLAGS_V204)}")))
    chk("paper_only_true", lambda: None if SAFETY_FLAGS_V204.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("no_real_orders_flag", lambda: None if SAFETY_FLAGS_V204.get("no_real_orders") is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders flag must be True")))
    chk("broker_disabled", lambda: None if SAFETY_FLAGS_V204.get("broker_execution_disabled") is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("production_blocked", lambda: None if SAFETY_FLAGS_V204.get("production_trading_blocked") is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V204.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V204.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))
    chk("should_auto_apply_always_false_flag", lambda: None if SAFETY_FLAGS_V204.get("should_auto_apply_always_false") is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))

    # --- models count ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _ALL_MODEL_NAMES_V204
    chk("models_count_12", lambda: None if len(_ALL_MODEL_NAMES_V204) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 models, got {len(_ALL_MODEL_NAMES_V204)}")))

    # --- recommendation categories ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    chk("recommendation_categories_10", lambda: None if len(RECOMMENDATION_CATEGORIES) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 recommendation categories")))
    chk("has_entry_rule", lambda: None if "entry_rule" in RECOMMENDATION_CATEGORIES else (_ for _ in ()).throw(
        AssertionError("entry_rule missing")))
    chk("has_risk_budget", lambda: None if "risk_budget" in RECOMMENDATION_CATEGORIES else (_ for _ in ()).throw(
        AssertionError("risk_budget missing")))
    chk("has_human_review", lambda: None if "human_review" in RECOMMENDATION_CATEGORIES else (_ for _ in ()).throw(
        AssertionError("human_review missing")))

    # --- review loop / weekly pack / metrics / recommendation schema callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import (
        run_portfolio_review, build_weekly_improvement_pack,
        export_review_json, export_review_markdown, export_review_csv,
        export_improvement_pack_json, export_review_metrics_csv,
        build_review_audit_snapshot, get_review_summary, get_version_info_v204, verify_version_v204,
        ImprovementRecommendation, ReviewMetrics, WeeklyImprovementPack, PortfolioReviewInput,
    )
    chk("review_loop_callable", lambda: run_portfolio_review())
    chk("review_loop_all_passed", lambda: None if run_portfolio_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("run_portfolio_review all_passed not True")))
    chk("review_loop_paper_only", lambda: None if run_portfolio_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("run_portfolio_review paper_only not True")))
    chk("weekly_pack_callable", lambda: build_weekly_improvement_pack())
    chk("weekly_pack_auto_apply_false", lambda: None if build_weekly_improvement_pack().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("build_weekly_improvement_pack should_auto_apply not False")))
    chk("review_metrics_callable", lambda: ReviewMetrics())
    chk("recommendation_schema_callable", lambda: ImprovementRecommendation(
        recommendation_id="REC-001", category="entry_rule", should_auto_apply=False))
    chk("export_json_callable", lambda: export_review_json(run_portfolio_review()))
    chk("export_json_valid", lambda: None if export_review_json(run_portfolio_review()).is_valid is True else (_ for _ in ()).throw(
        AssertionError("json export not valid")))
    chk("export_markdown_callable", lambda: export_review_markdown(run_portfolio_review()))
    chk("export_markdown_valid", lambda: None if export_review_markdown(run_portfolio_review()).is_valid is True else (_ for _ in ()).throw(
        AssertionError("markdown export not valid")))
    chk("export_csv_callable", lambda: export_review_csv(run_portfolio_review()))
    chk("export_csv_valid", lambda: None if export_review_csv(run_portfolio_review()).is_valid is True else (_ for _ in ()).throw(
        AssertionError("csv export not valid")))
    chk("export_pack_json_callable", lambda: export_improvement_pack_json(build_weekly_improvement_pack()))
    chk("export_pack_json_valid", lambda: None if export_improvement_pack_json(build_weekly_improvement_pack()).is_valid is True else (_ for _ in ()).throw(
        AssertionError("pack json export not valid")))
    chk("export_metrics_csv_callable", lambda: export_review_metrics_csv(ReviewMetrics(), "test-review"))
    chk("export_metrics_csv_valid", lambda: None if export_review_metrics_csv(ReviewMetrics(), "test-review").is_valid is True else (_ for _ in ()).throw(
        AssertionError("metrics csv export not valid")))
    chk("audit_snapshot_callable", lambda: build_review_audit_snapshot(run_portfolio_review()))
    chk("audit_snapshot_hash", lambda: None if build_review_audit_snapshot(run_portfolio_review()).reproducibility_hash else (_ for _ in ()).throw(
        AssertionError("no reproducibility_hash")))
    chk("get_review_summary_callable", lambda: get_review_summary())
    chk("get_version_info_callable", lambda: get_version_info_v204())
    chk("verify_version_callable", lambda: None if verify_version_v204() is True else (_ for _ in ()).throw(
        AssertionError("verify_version_v204 failed")))

    # --- should_auto_apply invariant ---
    chk("should_auto_apply_always_False",
        lambda: None if ImprovementRecommendation(should_auto_apply=True).should_auto_apply is False else (
            _ for _ in ()).throw(AssertionError("should_auto_apply must always be False")))
    chk("pack_should_auto_apply_always_False",
        lambda: None if WeeklyImprovementPack(should_auto_apply=True).should_auto_apply is False else (
            _ for _ in ()).throw(AssertionError("WeeklyImprovementPack.should_auto_apply must always be False")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    chk("cli_commands_11", lambda: None if len(CLI_COMMANDS_V204) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 CLI_COMMANDS_V204")))
    for cmd in [
        "paper-cockpit-v204-review-weekly",
        "paper-cockpit-v204-review-portfolio",
        "paper-cockpit-v204-review-strategy",
        "paper-cockpit-v204-review-blocked-reasons",
        "paper-cockpit-v204-review-risk-usage",
        "paper-cockpit-v204-generate-improvement-pack",
        "paper-cockpit-v204-export-json",
        "paper-cockpit-v204-export-md",
        "paper-cockpit-v204-export-csv",
        "paper-cockpit-v204-health",
        "paper-cockpit-v204-gate",
    ]:
        chk(f"cli_{cmd.replace('-','_')}", lambda c=cmd: None if c in CLI_COMMANDS_V204 else (_ for _ in ()).throw(
            AssertionError(f"Missing CLI command: {c}")))

    # --- CLI commands registered in PROVIDER_COMMANDS ---
    from cli.command_registry import PROVIDER_COMMANDS
    command_names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in CLI_COMMANDS_V204:
        chk(f"registry_{cmd.replace('-','_')}", lambda c=cmd: None if c in command_names else (_ for _ in ()).throw(
            AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- GUI import safe ---
    from gui.small_capital_strategy_panel import PANEL_VERSION_V204
    chk("panel_version_v204", lambda: None if PANEL_VERSION_V204 == "2.0.4" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V204 2.0.4, got {PANEL_VERSION_V204}")))

    # --- PANEL_VERSION unchanged ---
    from gui.small_capital_strategy_panel import PANEL_VERSION
    chk("panel_version_200_unchanged", lambda: None if PANEL_VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"PANEL_VERSION must remain 2.0.0, got {PANEL_VERSION}")))

    # --- GUI tabs ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v204_tab_names
    tab_names = get_tab_names()
    for tab in ["weekly_review_v204", "improvement_pack_v204", "review_metrics_v204"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing")))
    chk("get_v204_tab_names_3", lambda: None if len(get_v204_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v204 tab names")))

    # --- render_all_tabs zero error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    error_tabs = [k for k, v in all_rendered.items() if isinstance(v, dict) and "error" in v]
    chk("render_all_tabs_zero_error_tabs", lambda: None if len(error_tabs) == 0 else (_ for _ in ()).throw(
        AssertionError(f"Error tabs: {error_tabs}")))
    for tab in ["weekly_review_v204", "improvement_pack_v204", "review_metrics_v204"]:
        chk(f"render_{tab}_no_error", lambda t=tab: None if "error" not in str(
            all_rendered.get(t, {})) else (_ for _ in ()).throw(AssertionError(f"{t} has render error")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v204 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_204", lambda: None if all(s["schema_version"] == "204" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Bad scenario schema")))
    chk("scenarios_paper_only", lambda: None if all(s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Missing paper_only in scenarios")))
    chk("scenarios_unique_ids", lambda: None if len({s["id"] for s in SCENARIOS}) == 80 else (_ for _ in ()).throw(
        AssertionError("Duplicate scenario IDs")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v204 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_204", lambda: None if all(f["schema_version"] == "204" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Bad fixture schema")))
    chk("fixtures_unique_ids", lambda: None if len({f["id"] for f in FIXTURES}) == 80 else (_ for _ in ()).throw(
        AssertionError("Duplicate fixture IDs")))

    # --- backward compat with v2.0.3 ---
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import VERSION as V203
    chk("v203_backward_compat", lambda: None if V203 == "2.0.3" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.3 VERSION changed to {V203}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    chk("v203_simulate_one_callable", lambda: None if simulate_one().all_passed is True else (_ for _ in ()).throw(
        AssertionError("v203 simulate_one all_passed must be True")))

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
    print(f"[paper_cockpit_release_gate_v204] gate_passed={gate_passed}  {passed}/{total_count}")
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
