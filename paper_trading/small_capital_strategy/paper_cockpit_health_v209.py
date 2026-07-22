"""
paper_trading/small_capital_strategy/paper_cockpit_health_v209.py
v2.0.9 Paper Position Sizing & Risk Budget Control — Health Check
[!] Paper Only. Research Only. Position Sizing Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

HEALTH_VERSION = "2.0.9"
HEALTH_RELEASE = "Paper Position Sizing & Risk Budget Control"


def run_health_check():
    """Run all health checks for v2.0.9 paper cockpit. Returns result dict."""
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

    # --- version / title ---
    chk("version_title_209", lambda: None if HEALTH_VERSION == "2.0.9" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.9 got {HEALTH_VERSION}")))
    chk("release_name_sizing", lambda: None if "Sizing" in HEALTH_RELEASE or "Position" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Sizing': {HEALTH_RELEASE}")))
    chk("release_name_risk_budget", lambda: None if "Risk" in HEALTH_RELEASE or "Budget" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Risk'/'Budget': {HEALTH_RELEASE}")))

    # --- module import ---
    chk("import_paper_cockpit_v209", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v209",
        fromlist=["VERSION"]))

    # --- version constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_209", lambda: None if VERSION == "2.0.9" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.9 got {VERSION}")))
    chk("schema_version_is_209", lambda: None if SCHEMA_VERSION == "209" else (_ for _ in ()).throw(
        AssertionError(f"Expected 209 got {SCHEMA_VERSION}")))
    chk("release_name_contains_sizing", lambda: None if "Sizing" in RELEASE_NAME or "Position" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Sizing': {RELEASE_NAME}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    chk("safety_flags_count_21", lambda: None if len(SAFETY_FLAGS_V209) == 21 else (_ for _ in ()).throw(
        AssertionError(f"Expected 21 SAFETY_FLAGS_V209, got {len(SAFETY_FLAGS_V209)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V209["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V209["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V209["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V209["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_sizing_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V209["sizing_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("sizing_actions_recommendation_only must be True")))
    chk("safety_broker_execution_disabled", lambda: None if SAFETY_FLAGS_V209["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_trading_blocked", lambda: None if SAFETY_FLAGS_V209["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))
    chk("safety_no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V209["no_automatic_rebalance"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))
    chk("safety_no_real_account_sync", lambda: None if SAFETY_FLAGS_V209["no_real_account_sync"] is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))

    # --- size actions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SIZE_ACTIONS
    chk("size_actions_count_7", lambda: None if len(SIZE_ACTIONS) == 7 else (_ for _ in ()).throw(
        AssertionError(f"Expected 7 SIZE_ACTIONS, got {len(SIZE_ACTIONS)}")))
    for sa in ["allow_full_paper_size", "reduce_size", "minimum_probe_size",
               "observation_only", "block_new_position", "require_rescore", "human_review_required"]:
        chk(f"size_action_{sa}", lambda s=sa: None if s in SIZE_ACTIONS else (
            _ for _ in ()).throw(AssertionError(f"Missing size action: {s}")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    chk("cli_commands_count_10", lambda: None if len(CLI_COMMANDS_V209) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI_COMMANDS_V209, got {len(CLI_COMMANDS_V209)}")))
    for cmd in [
        "paper-cockpit-v209-review-sizing",
        "paper-cockpit-v209-evaluate-risk-budget",
        "paper-cockpit-v209-calculate-position-size",
        "paper-cockpit-v209-build-size-reduction-queue",
        "paper-cockpit-v209-build-blocked-sizing-queue",
        "paper-cockpit-v209-export-json",
        "paper-cockpit-v209-export-md",
        "paper-cockpit-v209-export-csv",
        "paper-cockpit-v209-health",
        "paper-cockpit-v209-gate",
    ]:
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V209 else (
            _ for _ in ()).throw(AssertionError(f"Missing CLI command: {c}")))

    # --- GUI tabs ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import GUI_TABS_V209
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V209) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI_TABS_V209, got {len(GUI_TABS_V209)}")))
    for tab in ["position_sizing_v209", "risk_budget_v209", "size_reduction_queue_v209"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in GUI_TABS_V209 else (
            _ for _ in ()).throw(AssertionError(f"Missing GUI tab: {t}")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import (
        RiskBudgetPolicy, CandidateSizingItem, PositionSizingSummary,
        SizingReviewInput, SizingReviewResult, SizingExportResult,
        SizingAuditSnapshot, SizingReport, CandidateSizingCSV,
        RiskBudgetCSV, SizeReductionCSV, V209HealthSummary,
        V209ReleaseSummary, _ALL_MODEL_NAMES_V209,
    )
    chk("model_RiskBudgetPolicy", lambda: RiskBudgetPolicy())
    chk("model_CandidateSizingItem", lambda: CandidateSizingItem())
    chk("model_PositionSizingSummary", lambda: PositionSizingSummary())
    chk("model_SizingReviewInput", lambda: SizingReviewInput())
    chk("model_SizingReviewResult", lambda: SizingReviewResult())
    chk("model_SizingExportResult", lambda: SizingExportResult())
    chk("model_SizingAuditSnapshot", lambda: SizingAuditSnapshot())
    chk("model_SizingReport", lambda: SizingReport())
    chk("model_CandidateSizingCSV", lambda: CandidateSizingCSV())
    chk("model_RiskBudgetCSV", lambda: RiskBudgetCSV())
    chk("model_SizeReductionCSV", lambda: SizeReductionCSV())
    chk("model_V209HealthSummary", lambda: V209HealthSummary())
    chk("model_V209ReleaseSummary", lambda: V209ReleaseSummary())
    chk("model_count_14", lambda: None if len(_ALL_MODEL_NAMES_V209) == 14 else (_ for _ in ()).throw(
        AssertionError(f"Expected 14 models, got {len(_ALL_MODEL_NAMES_V209)}")))

    # --- should_auto_apply / auto_apply_enabled invariants ---
    chk("risk_budget_policy_auto_apply_false", lambda: None if RiskBudgetPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("RiskBudgetPolicy.auto_apply_enabled must always be False")))
    chk("candidate_sizing_item_should_auto_apply_false", lambda: None if CandidateSizingItem(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("CandidateSizingItem.should_auto_apply must always be False")))
    chk("review_result_should_auto_apply_false", lambda: None if SizingReviewResult(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("SizingReviewResult.should_auto_apply must always be False")))
    chk("review_result_auto_apply_enabled_false", lambda: None if SizingReviewResult(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("SizingReviewResult.auto_apply_enabled must always be False")))

    # --- position sizing engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    chk("run_sizing_review_callable", lambda: run_sizing_review())
    chk("run_sizing_review_paper_only", lambda: None if run_sizing_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("run_sizing_review_all_passed", lambda: None if run_sizing_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("run_sizing_review_should_auto_apply_false", lambda: None if run_sizing_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))
    chk("run_sizing_review_auto_apply_enabled_false", lambda: None if run_sizing_review().auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))

    # --- risk budget policy callable ---
    chk("risk_budget_policy_callable", lambda: RiskBudgetPolicy())

    # --- candidate sizing item callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    chk("calculate_position_size_callable", lambda: calculate_position_size(
        "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0, 80.0, 900.0, 855.0
    ))

    # --- sizing summary callable ---
    chk("sizing_summary_not_none", lambda: None if run_sizing_review().sizing_summary is not None else (_ for _ in ()).throw(
        AssertionError("sizing_summary must not be None")))

    # --- evaluate_risk_budget callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import evaluate_risk_budget
    chk("evaluate_risk_budget_callable", lambda: evaluate_risk_budget())
    chk("evaluate_risk_budget_dict", lambda: None if isinstance(evaluate_risk_budget(), dict) else (_ for _ in ()).throw(
        AssertionError("evaluate_risk_budget() must return a dict")))

    # --- build_size_reduction_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import build_size_reduction_queue
    chk("build_size_reduction_queue_callable", lambda: build_size_reduction_queue())
    chk("build_size_reduction_queue_is_list", lambda: None if isinstance(build_size_reduction_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_size_reduction_queue() must return a list")))

    # --- build_blocked_sizing_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import build_blocked_sizing_queue
    chk("build_blocked_sizing_queue_callable", lambda: build_blocked_sizing_queue())
    chk("build_blocked_sizing_queue_is_list", lambda: None if isinstance(build_blocked_sizing_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_blocked_sizing_queue() must return a list")))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import (
        export_sizing_json, export_sizing_markdown,
        export_candidate_sizing_csv, export_risk_budget_csv,
        export_size_reduction_csv, export_sizing_audit_snapshot,
    )
    result = run_sizing_review()
    chk("export_json_callable", lambda: export_sizing_json(result))
    chk("export_json_valid", lambda: None if export_sizing_json(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_sizing_json is_valid must be True")))
    chk("export_md_callable", lambda: export_sizing_markdown(result))
    chk("export_md_valid", lambda: None if export_sizing_markdown(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_sizing_markdown is_valid must be True")))
    chk("export_candidate_csv_callable", lambda: export_candidate_sizing_csv(result))
    chk("export_candidate_csv_valid", lambda: None if export_candidate_sizing_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_candidate_sizing_csv is_valid must be True")))
    chk("export_risk_budget_csv_callable", lambda: export_risk_budget_csv(result))
    chk("export_risk_budget_csv_valid", lambda: None if export_risk_budget_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_risk_budget_csv is_valid must be True")))
    chk("export_size_reduction_csv_callable", lambda: export_size_reduction_csv(result))
    chk("export_size_reduction_csv_valid", lambda: None if export_size_reduction_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_size_reduction_csv is_valid must be True")))
    chk("export_audit_callable", lambda: export_sizing_audit_snapshot(result))

    # --- CLI callable (from command_registry) ---
    chk("cli_registry_importable", lambda: __import__("cli.command_registry", fromlist=["PROVIDER_COMMANDS"]))
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v209-review-sizing",
        "paper-cockpit-v209-evaluate-risk-budget",
        "paper-cockpit-v209-calculate-position-size",
        "paper-cockpit-v209-build-size-reduction-queue",
        "paper-cockpit-v209-build-blocked-sizing-queue",
        "paper-cockpit-v209-export-json",
        "paper-cockpit-v209-export-md",
        "paper-cockpit-v209-export-csv",
        "paper-cockpit-v209-health",
        "paper-cockpit-v209-gate",
    ]:
        chk(f"cli_registry_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- all 10 v209 CLI handlers exist in main.py ---
    chk("main_importable", lambda: __import__("main", fromlist=["cmd_paper_cockpit_v209_review_sizing"]))
    import main as _main_module
    for handler_name in [
        "cmd_paper_cockpit_v209_review_sizing",
        "cmd_paper_cockpit_v209_evaluate_risk_budget",
        "cmd_paper_cockpit_v209_calculate_position_size",
        "cmd_paper_cockpit_v209_build_size_reduction_queue",
        "cmd_paper_cockpit_v209_build_blocked_sizing_queue",
        "cmd_paper_cockpit_v209_export_json",
        "cmd_paper_cockpit_v209_export_md",
        "cmd_paper_cockpit_v209_export_csv",
        "cmd_paper_cockpit_v209_health",
        "cmd_paper_cockpit_v209_gate",
    ]:
        chk(f"main_handler_{handler_name}_exists", lambda n=handler_name: None if hasattr(_main_module, n) else (
            _ for _ in ()).throw(AssertionError(f"main.py missing handler: '{n}'")))
        chk(f"main_handler_{handler_name}_callable", lambda n=handler_name: None if callable(getattr(_main_module, n)) else (
            _ for _ in ()).throw(AssertionError(f"handler '{n}' is not callable")))

    # --- no fake isolated module-level command_map ---
    chk("no_fake_isolated_command_map", lambda: None if not hasattr(_main_module, "_ISOLATED_V209_COMMAND_MAP") else (_ for _ in ()).throw(
        AssertionError("main.py must not have isolated command_map for v209")))

    # --- GUI import safe ---
    chk("gui_importable", lambda: __import__("gui.small_capital_strategy_panel", fromlist=["PANEL_VERSION_V209"]))
    from gui.small_capital_strategy_panel import PANEL_VERSION_V209
    chk("panel_version_209", lambda: None if PANEL_VERSION_V209 == "2.0.9" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V209 2.0.9, got {PANEL_VERSION_V209}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v209_tab_names
    tab_names = get_tab_names()
    for tab in ["position_sizing_v209", "risk_budget_v209", "size_reduction_queue_v209"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing from tab_names")))
    chk("get_v209_tab_names_3", lambda: None if len(get_v209_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v209 tab names, got {len(get_v209_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    render_result = render_all_tabs()
    for tab in ["position_sizing_v209", "risk_budget_v209", "size_reduction_queue_v209"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' rendered with error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_global_no_error_tabs", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has global error tabs: {error_tabs}")))

    # --- paper-only guard enabled ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V209.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("paper_only guard must be enabled")))

    # --- broker execution disabled ---
    chk("broker_execution_disabled", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("broker execution must be disabled")))

    # --- production trading blocked ---
    chk("production_trading_blocked", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("production trading must be blocked")))

    # --- no real orders ---
    chk("no_real_orders_global", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))

    # --- no automatic rebalance ---
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V209.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- no real account sync ---
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V209.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))

    # --- auto_apply_enabled always False ---
    chk("auto_apply_enabled_always_false_flag", lambda: None if SAFETY_FLAGS_V209.get("auto_apply_enabled_always_false") is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false flag must be True")))

    # --- sizing actions are recommendation only ---
    chk("sizing_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V209.get("sizing_actions_recommendation_only") is True else (_ for _ in ()).throw(
        AssertionError("sizing_actions_recommendation_only must be True")))

    # --- backward compatibility with v2.0.8 ---
    chk("import_v208_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v208", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import VERSION as V208
    chk("v208_version_unchanged", lambda: None if V208 == "2.0.8" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.8 VERSION changed to {V208}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    chk("v208_run_exposure_review_callable", lambda: run_exposure_review())

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found via relative path")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_version_209", lambda: None if all(
        s["schema_version"] == "209" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios have wrong schema_version")))
    chk("scenarios_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing paper_only=True")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v209 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_version_209", lambda: None if all(
        f["schema_version"] == "209" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures have wrong schema_version")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures missing fixture_id")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v209] {passed}/{total} passed")
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
    sys.exit(0 if result["all_passed"] else 1)
