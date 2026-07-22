"""
release/paper_cockpit_release_gate_v207.py
v2.0.7 Paper Theme Rotation & Market Regime Control — Release Gate
[!] Paper Only. Research Only. Theme Rotation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

GATE_VERSION = "2.0.7"
GATE_RELEASE = "Paper Theme Rotation & Market Regime Control"
BASELINE_TESTS = 34632
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = ("2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4", "2.0.5", "2.0.6", "2.0.7")


def run_release_gate():
    """Run all release gate checks for v2.0.7. Returns result dict."""
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
    chk("gate_version_207", lambda: None if GATE_VERSION == "2.0.7" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.7")))
    chk("baseline_tests_34632", lambda: None if BASELINE_TESTS == 34632 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 34632")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import VERSION, SCHEMA_VERSION
    chk("module_version_207", lambda: None if VERSION == "2.0.7" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.7, got {VERSION}")))
    chk("schema_version_207", lambda: None if SCHEMA_VERSION == "207" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 207, got {SCHEMA_VERSION}")))

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
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V207["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_should_auto_apply_theme_rotation_always_false", lambda: None if SAFETY_FLAGS_V207["should_auto_apply_theme_rotation_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_theme_rotation_always_false must be True")))

    # --- theme rotation engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    chk("run_theme_rotation_review_callable", lambda: run_theme_rotation_review())
    chk("run_theme_rotation_review_paper_only", lambda: None if run_theme_rotation_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("run_theme_rotation_review_all_passed", lambda: None if run_theme_rotation_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("run_theme_rotation_review_should_auto_apply_false", lambda: None if run_theme_rotation_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))

    # --- market regime engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import evaluate_market_regime
    chk("evaluate_market_regime_callable", lambda: evaluate_market_regime())
    chk("evaluate_market_regime_auto_apply_false", lambda: None if evaluate_market_regime().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))

    # --- theme strength schema callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeStrengthItem
    chk("theme_strength_schema_callable", lambda: ThemeStrengthItem())

    # --- candidate priority adjustment callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import adjust_candidate_priority, MarketRegime
    chk("adjust_candidate_priority_callable", lambda: adjust_candidate_priority(
        "2330", "台積電", "CAND-001",
        ThemeStrengthItem(theme_id="THEME-AI", theme_state="leading"),
        MarketRegime(market_state="range_bound"),
    ))

    # --- theme rotation summary callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeRotationSummary
    chk("theme_rotation_summary_callable", lambda: ThemeRotationSummary())
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
    chk("export_json_valid", lambda: None if export_theme_rotation_json(result).is_valid else (_ for _ in ()).throw(
        AssertionError("export_theme_rotation_json must be valid")))
    chk("export_md_callable", lambda: export_theme_rotation_markdown(result))
    chk("export_md_valid", lambda: None if export_theme_rotation_markdown(result).is_valid else (_ for _ in ()).throw(
        AssertionError("export_theme_rotation_markdown must be valid")))
    chk("export_theme_strength_csv_callable", lambda: export_theme_strength_csv(result))
    chk("export_market_regime_csv_callable", lambda: export_market_regime_csv(result))
    chk("export_candidate_priority_csv_callable", lambda: export_candidate_priority_csv(result))
    chk("export_audit_callable", lambda: export_theme_rotation_audit_snapshot(result))

    # --- CLI callable ---
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
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' missing")))

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
    from gui.small_capital_strategy_panel import PANEL_VERSION_V207, PANEL_VERSION
    chk("panel_version_207", lambda: None if PANEL_VERSION_V207 == "2.0.7" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V207 2.0.7, got {PANEL_VERSION_V207}")))
    chk("panel_version_still_200", lambda: None if PANEL_VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"PANEL_VERSION must stay 2.0.0, got {PANEL_VERSION}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v207_tab_names, render_all_tabs
    tab_names = get_tab_names()
    for tab in ["theme_rotation_v207", "market_regime_v207", "candidate_priority_adjustment_v207"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing")))
    chk("get_v207_tab_names_3", lambda: None if len(get_v207_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v207 tabs, got {len(get_v207_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    render_result = render_all_tabs()
    for tab in ["theme_rotation_v207", "market_regime_v207", "candidate_priority_adjustment_v207"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' has error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_no_error_tabs", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs error tabs: {error_tabs}")))

    # --- paper-only guard ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V207.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("paper_only guard must be enabled")))
    chk("broker_execution_disabled", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("broker execution must be disabled")))
    chk("production_trading_blocked_gate", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("production trading must be blocked")))
    chk("no_real_orders_gate", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V207.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V207.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- should_auto_apply always False ---
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        MarketRegime as MR207, CandidatePriorityAdjustment as CPA207,
        ThemeRotationReviewResult as TRRR207,
    )
    chk("should_auto_apply_market_regime_always_false", lambda: None if MR207(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("MarketRegime.should_auto_apply must always be False")))
    chk("should_auto_apply_candidate_priority_always_false", lambda: None if CPA207(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("CandidatePriorityAdjustment.should_auto_apply must always be False")))
    chk("should_auto_apply_review_result_always_false", lambda: None if TRRR207(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("ThemeRotationReviewResult.should_auto_apply must always be False")))
    chk("candidate_promotion_allowed_is_recommendation_only", lambda: None if result.should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("candidate_promotion_allowed must be recommendation only")))

    # --- backward compatibility with v2.0.6 ---
    chk("import_v206_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v206", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        VERSION as V206, run_lifecycle_review as rlr206,
    )
    chk("v206_version_unchanged", lambda: None if V206 == "2.0.6" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.6 VERSION changed to {V206}")))
    chk("v206_run_lifecycle_review_callable", lambda: rlr206())

    # --- v201 health relative-path compatibility ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found")))

    # --- scenarios and fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v207 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v207 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))

    gate_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_release_gate_v207] {passed}/{total} passed")
    return {
        "gate_passed": gate_passed,
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
