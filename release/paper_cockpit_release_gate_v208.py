"""
release/paper_cockpit_release_gate_v208.py
v2.0.8 Paper Portfolio Exposure & Theme Concentration Risk Control — Release Gate
[!] Paper Only. Research Only. Exposure Analysis Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

GATE_VERSION = "2.0.8"
GATE_RELEASE = "Paper Portfolio Exposure & Theme Concentration Risk Control"
BASELINE_TESTS = 35005
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = ("2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4", "2.0.5", "2.0.6", "2.0.7", "2.0.8")


def run_release_gate():
    """Run all release gate checks for v2.0.8. Returns result dict."""
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
    chk("gate_version_208", lambda: None if GATE_VERSION == "2.0.8" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.8")))
    chk("baseline_tests_35005", lambda: None if BASELINE_TESTS == 35005 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 35005")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import VERSION, SCHEMA_VERSION
    chk("module_version_208", lambda: None if VERSION == "2.0.8" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.8, got {VERSION}")))
    chk("schema_version_208", lambda: None if SCHEMA_VERSION == "208" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 208, got {SCHEMA_VERSION}")))

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
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V208["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V208["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_exposure_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V208["exposure_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("exposure_actions_recommendation_only must be True")))

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
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureItem
    chk("exposure_item_schema_callable", lambda: ExposureItem())

    # --- risk cap policy callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import PortfolioRiskCapPolicy
    chk("risk_cap_policy_callable", lambda: PortfolioRiskCapPolicy())
    chk("risk_cap_policy_auto_apply_false", lambda: None if PortfolioRiskCapPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must always be False")))

    # --- candidate exposure adjustment callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import (
        CandidateExposureAdjustment, adjust_candidate_exposure,
    )
    chk("candidate_exposure_adjustment_callable", lambda: CandidateExposureAdjustment())
    chk("adjust_candidate_exposure_callable", lambda: adjust_candidate_exposure(
        "2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 75.0
    ))

    # --- exposure summary callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureSummary
    chk("exposure_summary_callable", lambda: ExposureSummary())
    chk("exposure_summary_not_none", lambda: None if run_exposure_review().exposure_summary is not None else (_ for _ in ()).throw(
        AssertionError("exposure_summary must not be None")))

    # --- evaluate_concentration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import evaluate_concentration
    chk("evaluate_concentration_callable", lambda: evaluate_concentration())

    # --- build_warning_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import build_warning_queue
    chk("build_warning_queue_callable", lambda: build_warning_queue())

    # --- build_risk_cap_queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import build_risk_cap_queue
    chk("build_risk_cap_queue_callable", lambda: build_risk_cap_queue())

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import (
        export_exposure_json, export_exposure_markdown,
        export_exposure_item_csv, export_risk_cap_csv,
        export_candidate_exposure_csv, export_exposure_audit_snapshot,
    )
    result = run_exposure_review()
    chk("export_json_callable", lambda: export_exposure_json(result))
    chk("export_json_valid", lambda: None if export_exposure_json(result).is_valid else (_ for _ in ()).throw(
        AssertionError("export_exposure_json must be valid")))
    chk("export_md_callable", lambda: export_exposure_markdown(result))
    chk("export_md_valid", lambda: None if export_exposure_markdown(result).is_valid else (_ for _ in ()).throw(
        AssertionError("export_exposure_markdown must be valid")))
    chk("export_exposure_item_csv_callable", lambda: export_exposure_item_csv(result))
    chk("export_exposure_item_csv_valid", lambda: None if export_exposure_item_csv(result).is_valid else (_ for _ in ()).throw(
        AssertionError("export_exposure_item_csv must be valid")))
    chk("export_risk_cap_csv_callable", lambda: export_risk_cap_csv(result))
    chk("export_risk_cap_csv_valid", lambda: None if export_risk_cap_csv(result).is_valid else (_ for _ in ()).throw(
        AssertionError("export_risk_cap_csv must be valid")))
    chk("export_candidate_exposure_csv_callable", lambda: export_candidate_exposure_csv(result))
    chk("export_candidate_exposure_csv_valid", lambda: None if export_candidate_exposure_csv(result).is_valid else (_ for _ in ()).throw(
        AssertionError("export_candidate_exposure_csv must be valid")))
    chk("export_audit_callable", lambda: export_exposure_audit_snapshot(result))

    # --- CLI callable ---
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
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' missing")))

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

    # --- all 10 v208 command_map entries present in runtime dispatch ---
    chk("v208_commands_in_provider_commands", lambda: None if all(
        c in cmd_names for c in [
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
        ]
    ) else (_ for _ in ()).throw(AssertionError("Not all v208 commands in PROVIDER_COMMANDS")))

    # --- GUI import safe ---
    chk("gui_importable", lambda: __import__("gui.small_capital_strategy_panel", fromlist=["PANEL_VERSION_V208"]))
    from gui.small_capital_strategy_panel import PANEL_VERSION_V208, PANEL_VERSION
    chk("panel_version_208", lambda: None if PANEL_VERSION_V208 == "2.0.8" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V208 2.0.8, got {PANEL_VERSION_V208}")))
    chk("panel_version_still_200", lambda: None if PANEL_VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"PANEL_VERSION must stay 2.0.0, got {PANEL_VERSION}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v208_tab_names, render_all_tabs
    tab_names = get_tab_names()
    for tab in ["portfolio_exposure_v208", "theme_concentration_v208", "exposure_warning_queue_v208"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing")))
    chk("get_v208_tab_names_3", lambda: None if len(get_v208_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v208 tabs, got {len(get_v208_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    render_result = render_all_tabs()
    for tab in ["portfolio_exposure_v208", "theme_concentration_v208", "exposure_warning_queue_v208"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' has error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_no_error_tabs", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs error tabs: {error_tabs}")))

    # --- paper-only guard ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V208.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("paper_only guard must be enabled")))
    chk("broker_execution_disabled", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("broker execution must be disabled")))
    chk("production_trading_blocked_gate", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("production trading must be blocked")))
    chk("no_real_orders_gate", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V208.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V208.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- auto_apply_enabled / should_auto_apply always False ---
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import (
        PortfolioRiskCapPolicy as RCP208, CandidateExposureAdjustment as CEA208,
        ExposureReviewResult as ERR208,
    )
    chk("should_auto_apply_review_result_always_false", lambda: None if ERR208(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("ExposureReviewResult.should_auto_apply must always be False")))
    chk("auto_apply_enabled_review_result_always_false", lambda: None if ERR208(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("ExposureReviewResult.auto_apply_enabled must always be False")))
    chk("auto_apply_enabled_policy_always_false", lambda: None if RCP208(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("PortfolioRiskCapPolicy.auto_apply_enabled must always be False")))
    chk("should_auto_apply_adj_always_false", lambda: None if CEA208(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("CandidateExposureAdjustment.should_auto_apply must always be False")))
    chk("exposure_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V208.get("exposure_actions_recommendation_only") is True else (_ for _ in ()).throw(
        AssertionError("exposure_actions_recommendation_only must be True")))

    # --- backward compatibility with v2.0.7 ---
    chk("import_v207_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v207", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        VERSION as V207, run_theme_rotation_review as rtr207,
    )
    chk("v207_version_unchanged", lambda: None if V207 == "2.0.7" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.7 VERSION changed to {V207}")))
    chk("v207_run_theme_rotation_review_callable", lambda: rtr207())

    # --- v201 health relative-path compatibility ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found")))

    # --- scenarios and fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v208 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v208 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))

    gate_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_release_gate_v208] {passed}/{total} passed")
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
