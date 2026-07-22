"""
paper_trading/small_capital_strategy/paper_cockpit_health_v208.py
v2.0.8 Paper Portfolio Exposure & Theme Concentration Risk Control — Health Check
[!] Paper Only. Research Only. Exposure Analysis Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

HEALTH_VERSION = "2.0.8"
HEALTH_RELEASE = "Paper Portfolio Exposure & Theme Concentration Risk Control"


def run_health_check():
    """Run all health checks for v2.0.8 paper cockpit. Returns result dict."""
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
    chk("version_title_208", lambda: None if HEALTH_VERSION == "2.0.8" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.8 got {HEALTH_VERSION}")))
    chk("release_name_exposure", lambda: None if "Exposure" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Exposure': {HEALTH_RELEASE}")))
    chk("release_name_concentration", lambda: None if "Concentration" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Concentration': {HEALTH_RELEASE}")))

    # --- module import ---
    chk("import_paper_cockpit_v208", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v208",
        fromlist=["VERSION"]))

    # --- version constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_208", lambda: None if VERSION == "2.0.8" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.8 got {VERSION}")))
    chk("schema_version_is_208", lambda: None if SCHEMA_VERSION == "208" else (_ for _ in ()).throw(
        AssertionError(f"Expected 208 got {SCHEMA_VERSION}")))
    chk("release_name_contains_exposure", lambda: None if "Exposure" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Exposure': {RELEASE_NAME}")))
    chk("release_name_contains_concentration", lambda: None if "Concentration" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Concentration': {RELEASE_NAME}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    chk("safety_flags_count_21", lambda: None if len(SAFETY_FLAGS_V208) == 21 else (_ for _ in ()).throw(
        AssertionError(f"Expected 21 SAFETY_FLAGS_V208, got {len(SAFETY_FLAGS_V208)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V208["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V208["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V208["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V208["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_exposure_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V208["exposure_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("exposure_actions_recommendation_only must be True")))
    chk("safety_broker_execution_disabled", lambda: None if SAFETY_FLAGS_V208["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_trading_blocked", lambda: None if SAFETY_FLAGS_V208["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))

    # --- exposure types ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_TYPES
    chk("exposure_types_count_9", lambda: None if len(EXPOSURE_TYPES) == 9 else (_ for _ in ()).throw(
        AssertionError(f"Expected 9 EXPOSURE_TYPES, got {len(EXPOSURE_TYPES)}")))
    for et in ["theme", "sector", "style", "volatility", "liquidity",
               "market_regime", "candidate_pool", "promotion_queue", "watchlist"]:
        chk(f"exposure_type_{et}", lambda s=et: None if s in EXPOSURE_TYPES else (
            _ for _ in ()).throw(AssertionError(f"Missing exposure type: {s}")))

    # --- warning levels ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import WARNING_LEVELS
    chk("warning_levels_count_5", lambda: None if len(WARNING_LEVELS) == 5 else (_ for _ in ()).throw(
        AssertionError(f"Expected 5 WARNING_LEVELS, got {len(WARNING_LEVELS)}")))
    for wl in ["none", "low", "medium", "high", "critical"]:
        chk(f"warning_level_{wl}", lambda s=wl: None if s in WARNING_LEVELS else (
            _ for _ in ()).throw(AssertionError(f"Missing warning level: {s}")))

    # --- exposure actions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_ACTIONS
    chk("exposure_actions_count_7", lambda: None if len(EXPOSURE_ACTIONS) == 7 else (_ for _ in ()).throw(
        AssertionError(f"Expected 7 EXPOSURE_ACTIONS, got {len(EXPOSURE_ACTIONS)}")))
    for ea in ["allow", "monitor", "reduce_priority", "freeze_new_candidates",
               "require_rescore", "block_promotion", "human_review_required"]:
        chk(f"exposure_action_{ea}", lambda s=ea: None if s in EXPOSURE_ACTIONS else (
            _ for _ in ()).throw(AssertionError(f"Missing exposure action: {s}")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    chk("cli_commands_count_10", lambda: None if len(CLI_COMMANDS_V208) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI_COMMANDS_V208, got {len(CLI_COMMANDS_V208)}")))
    for cmd in [
        "paper-cockpit-v208-review-exposure",
        "paper-cockpit-v208-evaluate-concentration",
        "paper-cockpit-v208-build-warning-queue",
        "paper-cockpit-v208-build-risk-cap-queue",
        "paper-cockpit-v208-adjust-candidate-exposure",
        "paper-cockpit-v208-export-json",
        "paper-cockpit-v208-export-md",
        "paper-cockpit-v208-export-csv",
        "paper-cockpit-v208-health",
        "paper-cockpit-v208-gate",
    ]:
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V208 else (
            _ for _ in ()).throw(AssertionError(f"Missing CLI command: {c}")))

    # --- GUI tabs ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import GUI_TABS_V208
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V208) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI_TABS_V208, got {len(GUI_TABS_V208)}")))
    for tab in ["portfolio_exposure_v208", "theme_concentration_v208", "exposure_warning_queue_v208"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in GUI_TABS_V208 else (
            _ for _ in ()).throw(AssertionError(f"Missing GUI tab: {t}")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import (
        ExposureItem, PortfolioRiskCapPolicy, CandidateExposureAdjustment,
        ExposureSummary, ExposureReviewInput, ExposureReviewResult,
        ExposureExportResult, ExposureAuditSnapshot, ExposureReport,
        ExposureItemCSV, RiskCapCSV, CandidateExposureCSV,
        V208HealthSummary, V208ReleaseSummary, _ALL_MODEL_NAMES_V208,
    )
    chk("model_ExposureItem", lambda: ExposureItem())
    chk("model_PortfolioRiskCapPolicy", lambda: PortfolioRiskCapPolicy())
    chk("model_CandidateExposureAdjustment", lambda: CandidateExposureAdjustment())
    chk("model_ExposureSummary", lambda: ExposureSummary())
    chk("model_ExposureReviewInput", lambda: ExposureReviewInput())
    chk("model_ExposureReviewResult", lambda: ExposureReviewResult())
    chk("model_ExposureExportResult", lambda: ExposureExportResult())
    chk("model_ExposureAuditSnapshot", lambda: ExposureAuditSnapshot())
    chk("model_ExposureReport", lambda: ExposureReport())
    chk("model_ExposureItemCSV", lambda: ExposureItemCSV())
    chk("model_RiskCapCSV", lambda: RiskCapCSV())
    chk("model_CandidateExposureCSV", lambda: CandidateExposureCSV())
    chk("model_V208HealthSummary", lambda: V208HealthSummary())
    chk("model_V208ReleaseSummary", lambda: V208ReleaseSummary())
    chk("model_count_14", lambda: None if len(_ALL_MODEL_NAMES_V208) == 14 else (_ for _ in ()).throw(
        AssertionError(f"Expected 14 models, got {len(_ALL_MODEL_NAMES_V208)}")))

    # --- should_auto_apply / auto_apply_enabled invariants ---
    chk("risk_cap_policy_auto_apply_false", lambda: None if PortfolioRiskCapPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("PortfolioRiskCapPolicy.auto_apply_enabled must always be False")))
    chk("candidate_exposure_adj_should_auto_apply_false", lambda: None if CandidateExposureAdjustment(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("CandidateExposureAdjustment.should_auto_apply must always be False")))
    chk("review_result_should_auto_apply_false", lambda: None if ExposureReviewResult(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("ExposureReviewResult.should_auto_apply must always be False")))
    chk("review_result_auto_apply_enabled_false", lambda: None if ExposureReviewResult(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("ExposureReviewResult.auto_apply_enabled must always be False")))

    # --- portfolio exposure engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    chk("run_exposure_review_callable", lambda: run_exposure_review())
    chk("run_exposure_review_paper_only", lambda: None if run_exposure_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("run_exposure_review_all_passed", lambda: None if run_exposure_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("run_exposure_review_should_auto_apply_false", lambda: None if run_exposure_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))
    chk("run_exposure_review_auto_apply_enabled_false", lambda: None if run_exposure_review().auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))

    # --- exposure item schema callable ---
    chk("exposure_item_callable", lambda: ExposureItem())

    # --- risk cap policy callable ---
    chk("risk_cap_policy_callable", lambda: PortfolioRiskCapPolicy())

    # --- candidate exposure adjustment callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    chk("adjust_candidate_exposure_callable", lambda: adjust_candidate_exposure(
        "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 75.0
    ))

    # --- exposure summary callable ---
    chk("exposure_summary_not_none", lambda: None if run_exposure_review().exposure_summary is not None else (_ for _ in ()).throw(
        AssertionError("exposure_summary must not be None")))

    # --- evaluate_concentration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import evaluate_concentration
    chk("evaluate_concentration_callable", lambda: evaluate_concentration())
    chk("evaluate_concentration_is_list", lambda: None if isinstance(evaluate_concentration(), list) else (_ for _ in ()).throw(
        AssertionError("evaluate_concentration() must return a list")))

    # --- build_warning_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import build_warning_queue
    chk("build_warning_queue_callable", lambda: build_warning_queue())
    chk("build_warning_queue_is_list", lambda: None if isinstance(build_warning_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_warning_queue() must return a list")))

    # --- build_risk_cap_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import build_risk_cap_queue
    chk("build_risk_cap_queue_callable", lambda: build_risk_cap_queue())
    chk("build_risk_cap_queue_is_list", lambda: None if isinstance(build_risk_cap_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_risk_cap_queue() must return a list")))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import (
        export_exposure_json, export_exposure_markdown,
        export_exposure_item_csv, export_risk_cap_csv,
        export_candidate_exposure_csv, export_exposure_audit_snapshot,
    )
    result = run_exposure_review()
    chk("export_json_callable", lambda: export_exposure_json(result))
    chk("export_json_valid", lambda: None if export_exposure_json(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_exposure_json is_valid must be True")))
    chk("export_md_callable", lambda: export_exposure_markdown(result))
    chk("export_md_valid", lambda: None if export_exposure_markdown(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_exposure_markdown is_valid must be True")))
    chk("export_exposure_item_csv_callable", lambda: export_exposure_item_csv(result))
    chk("export_exposure_item_csv_valid", lambda: None if export_exposure_item_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_exposure_item_csv is_valid must be True")))
    chk("export_risk_cap_csv_callable", lambda: export_risk_cap_csv(result))
    chk("export_risk_cap_csv_valid", lambda: None if export_risk_cap_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_risk_cap_csv is_valid must be True")))
    chk("export_candidate_exposure_csv_callable", lambda: export_candidate_exposure_csv(result))
    chk("export_candidate_exposure_csv_valid", lambda: None if export_candidate_exposure_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_candidate_exposure_csv is_valid must be True")))
    chk("export_audit_callable", lambda: export_exposure_audit_snapshot(result))

    # --- CLI callable (from command_registry) ---
    chk("cli_registry_importable", lambda: __import__("cli.command_registry", fromlist=["PROVIDER_COMMANDS"]))
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v208-review-exposure",
        "paper-cockpit-v208-evaluate-concentration",
        "paper-cockpit-v208-build-warning-queue",
        "paper-cockpit-v208-build-risk-cap-queue",
        "paper-cockpit-v208-adjust-candidate-exposure",
        "paper-cockpit-v208-export-json",
        "paper-cockpit-v208-export-md",
        "paper-cockpit-v208-export-csv",
        "paper-cockpit-v208-health",
        "paper-cockpit-v208-gate",
    ]:
        chk(f"cli_registry_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- all 10 v208 CLI handlers exist in main.py ---
    chk("main_importable", lambda: __import__("main", fromlist=["cmd_paper_cockpit_v208_review_exposure"]))
    import main as _main_module
    for handler_name in [
        "cmd_paper_cockpit_v208_review_exposure",
        "cmd_paper_cockpit_v208_evaluate_concentration",
        "cmd_paper_cockpit_v208_build_warning_queue",
        "cmd_paper_cockpit_v208_build_risk_cap_queue",
        "cmd_paper_cockpit_v208_adjust_candidate_exposure",
        "cmd_paper_cockpit_v208_export_json",
        "cmd_paper_cockpit_v208_export_md",
        "cmd_paper_cockpit_v208_export_csv",
        "cmd_paper_cockpit_v208_health",
        "cmd_paper_cockpit_v208_gate",
    ]:
        chk(f"main_handler_{handler_name}_exists", lambda n=handler_name: None if hasattr(_main_module, n) else (
            _ for _ in ()).throw(AssertionError(f"main.py missing handler: '{n}'")))
        chk(f"main_handler_{handler_name}_callable", lambda n=handler_name: None if callable(getattr(_main_module, n)) else (
            _ for _ in ()).throw(AssertionError(f"handler '{n}' is not callable")))

    # --- no fake isolated module-level command_map ---
    chk("no_fake_isolated_command_map", lambda: None if not hasattr(_main_module, "_ISOLATED_V208_COMMAND_MAP") else (_ for _ in ()).throw(
        AssertionError("main.py must not have isolated command_map for v208")))

    # --- GUI import safe ---
    chk("gui_importable", lambda: __import__("gui.small_capital_strategy_panel", fromlist=["PANEL_VERSION_V208"]))
    from gui.small_capital_strategy_panel import PANEL_VERSION_V208
    chk("panel_version_208", lambda: None if PANEL_VERSION_V208 == "2.0.8" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V208 2.0.8, got {PANEL_VERSION_V208}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v208_tab_names
    tab_names = get_tab_names()
    for tab in ["portfolio_exposure_v208", "theme_concentration_v208", "exposure_warning_queue_v208"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing from tab_names")))
    chk("get_v208_tab_names_3", lambda: None if len(get_v208_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v208 tab names, got {len(get_v208_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    render_result = render_all_tabs()
    for tab in ["portfolio_exposure_v208", "theme_concentration_v208", "exposure_warning_queue_v208"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' rendered with error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_global_no_error_tabs", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has global error tabs: {error_tabs}")))

    # --- paper-only guard enabled ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V208.get("paper_only") is True else (_ for _ in ()).throw(
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
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V208.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- no real account sync ---
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V208.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))

    # --- auto_apply_enabled always False ---
    chk("auto_apply_enabled_always_false_flag", lambda: None if SAFETY_FLAGS_V208.get("auto_apply_enabled_always_false") is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false flag must be True")))

    # --- exposure actions are recommendation only ---
    chk("exposure_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V208.get("exposure_actions_recommendation_only") is True else (_ for _ in ()).throw(
        AssertionError("exposure_actions_recommendation_only must be True")))

    # --- backward compatibility with v2.0.7 ---
    chk("import_v207_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v207", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import VERSION as V207
    chk("v207_version_unchanged", lambda: None if V207 == "2.0.7" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.7 VERSION changed to {V207}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    chk("v207_run_theme_rotation_review_callable", lambda: run_theme_rotation_review())

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found via relative path")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v208 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_version_208", lambda: None if all(
        s["schema_version"] == "208" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios have wrong schema_version")))
    chk("scenarios_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing paper_only=True")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v208 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_version_208", lambda: None if all(
        f["schema_version"] == "208" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures have wrong schema_version")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures missing fixture_id")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v208] {passed}/{total} passed")
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
