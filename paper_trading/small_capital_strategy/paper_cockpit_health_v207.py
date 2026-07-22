"""
paper_trading/small_capital_strategy/paper_cockpit_health_v207.py
v2.0.7 Paper Theme Rotation & Market Regime Control — Health Check
[!] Paper Only. Research Only. Theme Rotation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

# Ensure repo root is importable when run directly
_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

HEALTH_VERSION = "2.0.7"
HEALTH_RELEASE = "Paper Theme Rotation & Market Regime Control"


def run_health_check():
    """Run all health checks for v2.0.7 paper cockpit. Returns result dict."""
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
    chk("version_title_207", lambda: None if HEALTH_VERSION == "2.0.7" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.7 got {HEALTH_VERSION}")))
    chk("release_name_theme_rotation", lambda: None if "Theme" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Theme': {HEALTH_RELEASE}")))

    # --- module import ---
    chk("import_paper_cockpit_v207", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v207",
        fromlist=["VERSION"]))

    # --- version constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_207", lambda: None if VERSION == "2.0.7" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.7 got {VERSION}")))
    chk("schema_version_is_207", lambda: None if SCHEMA_VERSION == "207" else (_ for _ in ()).throw(
        AssertionError(f"Expected 207 got {SCHEMA_VERSION}")))
    chk("release_name_contains_theme", lambda: None if "Theme" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Theme': {RELEASE_NAME}")))
    chk("release_name_contains_regime", lambda: None if "Regime" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Regime': {RELEASE_NAME}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    chk("safety_flags_count_20", lambda: None if len(SAFETY_FLAGS_V207) == 20 else (_ for _ in ()).throw(
        AssertionError(f"Expected 20 SAFETY_FLAGS_V207, got {len(SAFETY_FLAGS_V207)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V207["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V207["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V207["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_should_auto_apply_theme_rotation_always_false", lambda: None if SAFETY_FLAGS_V207["should_auto_apply_theme_rotation_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_theme_rotation_always_false must be True")))
    chk("safety_broker_execution_disabled", lambda: None if SAFETY_FLAGS_V207["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_trading_blocked", lambda: None if SAFETY_FLAGS_V207["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))

    # --- theme states ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    chk("theme_states_count_10", lambda: None if len(THEME_STATES) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 THEME_STATES, got {len(THEME_STATES)}")))
    for st in ["emerging", "strengthening", "leading", "crowded", "overheating",
               "weakening", "cooling", "stale", "risk_off", "neutral"]:
        chk(f"theme_state_{st}", lambda s=st: None if s in THEME_STATES else (
            _ for _ in ()).throw(AssertionError(f"Missing theme state: {s}")))

    # --- market states ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MARKET_STATES
    chk("market_states_count_7", lambda: None if len(MARKET_STATES) == 7 else (_ for _ in ()).throw(
        AssertionError(f"Expected 7 MARKET_STATES, got {len(MARKET_STATES)}")))
    for ms in ["strong_uptrend", "healthy_pullback", "range_bound", "weak_rebound",
               "downtrend", "high_volatility", "risk_off"]:
        chk(f"market_state_{ms}", lambda s=ms: None if s in MARKET_STATES else (
            _ for _ in ()).throw(AssertionError(f"Missing market state: {s}")))

    # --- allowed risk modes ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ALLOWED_RISK_MODES
    chk("allowed_risk_modes_count_5", lambda: None if len(ALLOWED_RISK_MODES) == 5 else (_ for _ in ()).throw(
        AssertionError(f"Expected 5 ALLOWED_RISK_MODES, got {len(ALLOWED_RISK_MODES)}")))
    for rm in ["aggressive_paper", "normal_paper", "defensive_paper", "observation_only", "freeze_promotion"]:
        chk(f"allowed_risk_mode_{rm}", lambda r=rm: None if r in ALLOWED_RISK_MODES else (
            _ for _ in ()).throw(AssertionError(f"Missing risk mode: {r}")))

    # --- theme actions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_ACTIONS
    chk("theme_actions_count_7", lambda: None if len(THEME_ACTIONS) == 7 else (_ for _ in ()).throw(
        AssertionError(f"Expected 7 THEME_ACTIONS, got {len(THEME_ACTIONS)}")))
    for ta in ["increase_attention", "keep_priority", "reduce_priority", "freeze_new_candidates",
               "require_rescore", "downgrade_theme", "human_review_required"]:
        chk(f"theme_action_{ta}", lambda a=ta: None if a in THEME_ACTIONS else (
            _ for _ in ()).throw(AssertionError(f"Missing theme action: {a}")))

    # --- priority changes ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import PRIORITY_CHANGES
    chk("priority_changes_count_6", lambda: None if len(PRIORITY_CHANGES) == 6 else (_ for _ in ()).throw(
        AssertionError(f"Expected 6 PRIORITY_CHANGES, got {len(PRIORITY_CHANGES)}")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    chk("cli_commands_count_11", lambda: None if len(CLI_COMMANDS_V207) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 CLI_COMMANDS_V207, got {len(CLI_COMMANDS_V207)}")))
    for cmd in [
        "paper-cockpit-v207-review-theme-rotation",
        "paper-cockpit-v207-evaluate-market-regime",
        "paper-cockpit-v207-rank-themes",
        "paper-cockpit-v207-detect-overheating",
        "paper-cockpit-v207-detect-weakening",
        "paper-cockpit-v207-adjust-candidate-priority",
        "paper-cockpit-v207-export-json",
        "paper-cockpit-v207-export-md",
        "paper-cockpit-v207-export-csv",
        "paper-cockpit-v207-health",
        "paper-cockpit-v207-gate",
    ]:
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V207 else (
            _ for _ in ()).throw(AssertionError(f"Missing CLI command: {c}")))

    # --- GUI tabs ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import GUI_TABS_V207
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V207) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI_TABS_V207, got {len(GUI_TABS_V207)}")))
    for tab in ["theme_rotation_v207", "market_regime_v207", "candidate_priority_adjustment_v207"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in GUI_TABS_V207 else (
            _ for _ in ()).throw(AssertionError(f"Missing GUI tab: {t}")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        ThemeStrengthItem, MarketRegime, CandidatePriorityAdjustment,
        ThemeRotationSummary, ThemeRotationReviewInput, ThemeRotationReviewResult,
        ThemeRotationExportResult, ThemeRotationAuditSnapshot, ThemeRotationReport,
        ThemeStrengthCSV, MarketRegimeCSV, V207HealthSummary, V207ReleaseSummary,
        _ALL_MODEL_NAMES_V207,
    )
    chk("model_ThemeStrengthItem", lambda: ThemeStrengthItem())
    chk("model_MarketRegime", lambda: MarketRegime())
    chk("model_CandidatePriorityAdjustment", lambda: CandidatePriorityAdjustment())
    chk("model_ThemeRotationSummary", lambda: ThemeRotationSummary())
    chk("model_ThemeRotationReviewInput", lambda: ThemeRotationReviewInput())
    chk("model_ThemeRotationReviewResult", lambda: ThemeRotationReviewResult())
    chk("model_ThemeRotationExportResult", lambda: ThemeRotationExportResult())
    chk("model_ThemeRotationAuditSnapshot", lambda: ThemeRotationAuditSnapshot())
    chk("model_ThemeRotationReport", lambda: ThemeRotationReport())
    chk("model_ThemeStrengthCSV", lambda: ThemeStrengthCSV())
    chk("model_MarketRegimeCSV", lambda: MarketRegimeCSV())
    chk("model_V207HealthSummary", lambda: V207HealthSummary())
    chk("model_V207ReleaseSummary", lambda: V207ReleaseSummary())
    chk("model_count_13", lambda: None if len(_ALL_MODEL_NAMES_V207) == 13 else (_ for _ in ()).throw(
        AssertionError(f"Expected 13 models, got {len(_ALL_MODEL_NAMES_V207)}")))

    # --- should_auto_apply invariants ---
    chk("market_regime_auto_apply_false", lambda: None if MarketRegime(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("MarketRegime.should_auto_apply must always be False")))
    chk("candidate_priority_auto_apply_false", lambda: None if CandidatePriorityAdjustment(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("CandidatePriorityAdjustment.should_auto_apply must always be False")))
    chk("review_result_auto_apply_false", lambda: None if ThemeRotationReviewResult(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("ThemeRotationReviewResult.should_auto_apply must always be False")))

    # --- theme rotation engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    chk("theme_rotation_review_callable", lambda: run_theme_rotation_review())
    chk("theme_rotation_review_paper_only", lambda: None if run_theme_rotation_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("theme_rotation_review_all_passed", lambda: None if run_theme_rotation_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("theme_rotation_review_should_auto_apply_false", lambda: None if run_theme_rotation_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))

    # --- market regime engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import evaluate_market_regime
    chk("evaluate_market_regime_callable", lambda: evaluate_market_regime())
    chk("evaluate_market_regime_should_auto_apply_false", lambda: None if evaluate_market_regime().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))

    # --- theme strength schema callable ---
    chk("theme_strength_item_callable", lambda: ThemeStrengthItem())

    # --- rank_themes callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import rank_themes
    chk("rank_themes_callable", lambda: rank_themes())
    chk("rank_themes_is_list", lambda: None if isinstance(rank_themes(), list) else (_ for _ in ()).throw(
        AssertionError("rank_themes() must return a list")))

    # --- detect_overheating callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_overheating
    chk("detect_overheating_callable", lambda: detect_overheating())
    chk("detect_overheating_is_list", lambda: None if isinstance(detect_overheating(), list) else (_ for _ in ()).throw(
        AssertionError("detect_overheating() must return a list")))

    # --- detect_weakening callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_weakening
    chk("detect_weakening_callable", lambda: detect_weakening())
    chk("detect_weakening_is_list", lambda: None if isinstance(detect_weakening(), list) else (_ for _ in ()).throw(
        AssertionError("detect_weakening() must return a list")))

    # --- candidate priority adjustment callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import adjust_candidate_priority
    chk("adjust_candidate_priority_callable", lambda: adjust_candidate_priority(
        "2330", "台積電", "CAND-001", ThemeStrengthItem(theme_id="THEME-AI", theme_state="leading"),
        MarketRegime(market_state="range_bound"),
    ))

    # --- theme rotation summary callable ---
    chk("theme_rotation_summary_not_none", lambda: None if run_theme_rotation_review().theme_rotation_summary is not None else (_ for _ in ()).throw(
        AssertionError("theme_rotation_summary must not be None")))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        export_theme_rotation_json, export_theme_rotation_markdown,
        export_theme_strength_csv, export_market_regime_csv,
        export_candidate_priority_csv, export_theme_rotation_audit_snapshot,
    )
    result = run_theme_rotation_review()
    chk("export_json_callable", lambda: export_theme_rotation_json(result))
    chk("export_json_valid", lambda: None if export_theme_rotation_json(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_theme_rotation_json is_valid must be True")))
    chk("export_md_callable", lambda: export_theme_rotation_markdown(result))
    chk("export_md_valid", lambda: None if export_theme_rotation_markdown(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_theme_rotation_markdown is_valid must be True")))
    chk("export_theme_strength_csv_callable", lambda: export_theme_strength_csv(result))
    chk("export_theme_strength_csv_valid", lambda: None if export_theme_strength_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_theme_strength_csv is_valid must be True")))
    chk("export_market_regime_csv_callable", lambda: export_market_regime_csv(result))
    chk("export_market_regime_csv_valid", lambda: None if export_market_regime_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_market_regime_csv is_valid must be True")))
    chk("export_candidate_priority_csv_callable", lambda: export_candidate_priority_csv(result))
    chk("export_candidate_priority_csv_valid", lambda: None if export_candidate_priority_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_candidate_priority_csv is_valid must be True")))
    chk("export_audit_callable", lambda: export_theme_rotation_audit_snapshot(result))

    # --- CLI callable (from command_registry) ---
    chk("cli_registry_importable", lambda: __import__("cli.command_registry", fromlist=["PROVIDER_COMMANDS"]))
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v207-review-theme-rotation",
        "paper-cockpit-v207-evaluate-market-regime",
        "paper-cockpit-v207-rank-themes",
        "paper-cockpit-v207-detect-overheating",
        "paper-cockpit-v207-detect-weakening",
        "paper-cockpit-v207-adjust-candidate-priority",
        "paper-cockpit-v207-export-json",
        "paper-cockpit-v207-export-md",
        "paper-cockpit-v207-export-csv",
        "paper-cockpit-v207-health",
        "paper-cockpit-v207-gate",
    ]:
        chk(f"cli_registry_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- all 11 v207 CLI handlers exist as module-level functions in main.py ---
    chk("main_importable", lambda: __import__("main", fromlist=["cmd_paper_cockpit_v207_review_theme_rotation"]))
    import main as _main_module
    for handler_name in [
        "cmd_paper_cockpit_v207_review_theme_rotation",
        "cmd_paper_cockpit_v207_evaluate_market_regime",
        "cmd_paper_cockpit_v207_rank_themes",
        "cmd_paper_cockpit_v207_detect_overheating",
        "cmd_paper_cockpit_v207_detect_weakening",
        "cmd_paper_cockpit_v207_adjust_candidate_priority",
        "cmd_paper_cockpit_v207_export_json",
        "cmd_paper_cockpit_v207_export_md",
        "cmd_paper_cockpit_v207_export_csv",
        "cmd_paper_cockpit_v207_health",
        "cmd_paper_cockpit_v207_gate",
    ]:
        chk(f"main_handler_{handler_name}_exists", lambda n=handler_name: None if hasattr(_main_module, n) else (
            _ for _ in ()).throw(AssertionError(f"main.py missing handler: '{n}'")))
        chk(f"main_handler_{handler_name}_callable", lambda n=handler_name: None if callable(getattr(_main_module, n)) else (
            _ for _ in ()).throw(AssertionError(f"handler '{n}' is not callable")))

    # --- GUI import safe ---
    chk("gui_importable", lambda: __import__("gui.small_capital_strategy_panel", fromlist=["PANEL_VERSION_V207"]))
    from gui.small_capital_strategy_panel import PANEL_VERSION_V207
    chk("panel_version_207", lambda: None if PANEL_VERSION_V207 == "2.0.7" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V207 2.0.7, got {PANEL_VERSION_V207}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v207_tab_names
    tab_names = get_tab_names()
    for tab in ["theme_rotation_v207", "market_regime_v207", "candidate_priority_adjustment_v207"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing from tab_names")))
    chk("get_v207_tab_names_3", lambda: None if len(get_v207_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v207 tab names, got {len(get_v207_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    render_result = render_all_tabs()
    for tab in ["theme_rotation_v207", "market_regime_v207", "candidate_priority_adjustment_v207"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' rendered with error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_global_no_error_tabs", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has global error tabs: {error_tabs}")))

    # --- paper-only guard enabled ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V207.get("paper_only") is True else (_ for _ in ()).throw(
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
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V207.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- no real account sync ---
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V207.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))

    # --- should_auto_apply always False ---
    chk("should_auto_apply_always_false_flag", lambda: None if SAFETY_FLAGS_V207.get("should_auto_apply_always_false") is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false flag must be True")))

    # --- candidate_promotion_allowed is recommendation only ---
    regime = evaluate_market_regime()
    chk("candidate_promotion_is_recommendation_only", lambda: None if regime.should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("candidate_promotion_allowed must be recommendation only (should_auto_apply=False)")))

    # --- backward compatibility with v2.0.6 ---
    chk("import_v206_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v206", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import VERSION as V206
    chk("v206_version_unchanged", lambda: None if V206 == "2.0.6" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.6 VERSION changed to {V206}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    chk("v206_run_lifecycle_review_callable", lambda: run_lifecycle_review())

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found via relative path")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v207 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_version_207", lambda: None if all(
        s["schema_version"] == "207" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios have wrong schema_version")))
    chk("scenarios_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing paper_only=True")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v207 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_version_207", lambda: None if all(
        f["schema_version"] == "207" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures have wrong schema_version")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures missing fixture_id")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v207] {passed}/{total} passed")
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
