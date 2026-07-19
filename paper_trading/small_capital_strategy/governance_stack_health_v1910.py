"""
paper_trading/small_capital_strategy/governance_stack_health_v1910.py
v1.9.10 Paper Governance Stack Consolidation & Release Audit — Health Check
[!] Paper Only. Research Only. Consolidation Only. Release Audit Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import sys
import os
sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))
from typing import Any, Dict

HEALTH_VERSION = "1.9.10"
EXPECTED_PANEL_VERSIONS = ("1.9.10", "2.0.0")


def run_health_check() -> Dict[str, Any]:
    checks = []
    passed = 0
    failed = 0

    def _check(name: str, condition: bool, detail: str = "") -> None:
        nonlocal passed, failed
        status = "PASS" if condition else "FAIL"
        if condition:
            passed += 1
        else:
            failed += 1
        checks.append({"name": name, "status": status, "detail": detail})

    # --- Version / constants ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_audit_v1910 import (
            VERSION, SCHEMA_VERSION, RELEASE_NAME, BASELINE_TESTS, MIN_NEW_TESTS,
            COVERED_VERSIONS, COVERED_MODULES, CLI_COMMANDS, GUI_TABS,
            FORBIDDEN_ACTIONS, ALLOWED_AUDIT_ACTIONS, SAFETY_FLAGS,
            _ALL_MODEL_NAMES, verify_version,
        )
        _check("version_module_import", True)
        _check("version_is_1910", VERSION == "1.9.10", "2.0.0")
        _check("schema_version_is_1910", SCHEMA_VERSION == "1910")
        _check("release_name_correct",
               "Governance" in RELEASE_NAME or "Consolidation" in RELEASE_NAME)
        _check("baseline_tests_31469", BASELINE_TESTS == 31469)
        _check("min_new_tests_300", MIN_NEW_TESTS == 300)
        _check("covered_versions_count_6", len(COVERED_VERSIONS) == 6)
        _check("covered_modules_count_6", len(COVERED_MODULES) == 6)
        _check("cli_commands_count_14", len(CLI_COMMANDS) == 14)
        _check("gui_tabs_count_3", len(GUI_TABS) == 3)
        _check("model_count_15", len(_ALL_MODEL_NAMES) == 15)
        _check("safety_flags_count_29", len(SAFETY_FLAGS) == 29)
        _check("forbidden_actions_count_15", len(FORBIDDEN_ACTIONS) == 15)
        _check("allowed_actions_count_15", len(ALLOWED_AUDIT_ACTIONS) == 15)
        _check("v194_in_covered", "1.9.4" in COVERED_VERSIONS)
        _check("v195_in_covered", "1.9.5" in COVERED_VERSIONS)
        _check("v196_in_covered", "1.9.6" in COVERED_VERSIONS)
        _check("v197_in_covered", "1.9.7" in COVERED_VERSIONS)
        _check("v198_in_covered", "1.9.8" in COVERED_VERSIONS)
        _check("v199_in_covered", "1.9.9" in COVERED_VERSIONS)
        _check("gui_tab_audit", "governance_stack_audit" in GUI_TABS)
        _check("gui_tab_release", "release_audit" in GUI_TABS)
        _check("gui_tab_compat", "compatibility_summary" in GUI_TABS)
        _check("paper_only_flag", SAFETY_FLAGS.get("paper_only") is True)
        _check("research_only_flag", SAFETY_FLAGS.get("research_only") is True)
        _check("consolidation_only_flag", SAFETY_FLAGS.get("consolidation_only") is True)
        _check("release_audit_only_flag", SAFETY_FLAGS.get("release_audit_only") is True)
        _check("no_real_orders_flag", SAFETY_FLAGS.get("no_real_orders") is True)
        _check("production_trading_blocked_flag", SAFETY_FLAGS.get("production_trading_blocked") is True)
        _check("audit_executes_order_false", SAFETY_FLAGS.get("audit_executes_order") is False)
        _check("audit_mutates_strategy_false", SAFETY_FLAGS.get("audit_mutates_strategy") is False)
        _check("dashboard_mutates_strategy_false", SAFETY_FLAGS.get("dashboard_mutates_strategy") is False)
        _check("export_triggers_real_order_false", SAFETY_FLAGS.get("export_triggers_real_order") is False)
        _check("buy_in_forbidden", "BUY" in FORBIDDEN_ACTIONS)
        _check("live_activate_in_forbidden", "LIVE_ACTIVATE" in FORBIDDEN_ACTIONS)
        _check("broker_connect_in_forbidden", "BROKER_CONNECT" in FORBIDDEN_ACTIONS)
        _check("paper_audit_in_allowed", "PAPER_AUDIT" in ALLOWED_AUDIT_ACTIONS)
        _check("paper_consolidate_in_allowed", "PAPER_CONSOLIDATE" in ALLOWED_AUDIT_ACTIONS)
        _check("verify_version_passes", verify_version() is True)
    except Exception as e:
        _check("version_module_import", False, str(e))

    # --- Models ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_audit_v1910 import (
            PaperGovernanceStackAuditInput, PaperGovernanceStackAuditResult,
            PaperGovernanceStackModule, PaperGovernanceStackVersion,
            PaperGovernanceStackCompatibilityResult,
            PaperGovernanceStackCliAuditResult, PaperGovernanceStackGuiAuditResult,
            PaperGovernanceStackHealthAuditResult, PaperGovernanceStackGateAuditResult,
            PaperGovernanceStackFixtureAuditResult, PaperGovernanceStackScenarioAuditResult,
            PaperGovernanceStackSafetyAuditResult, PaperGovernanceStackReleaseSummary,
            PaperGovernanceStackAuditReport, PaperGovernanceStackRecommendation,
        )
        _check("models_import", True)
        _check("audit_input_schema", PaperGovernanceStackAuditInput().schema_version == "1910")
        _check("audit_input_paper_only", PaperGovernanceStackAuditInput().paper_only is True)
        _check("audit_input_executes_order_false",
               PaperGovernanceStackAuditInput().audit_executes_order is False)
        _check("audit_result_schema", PaperGovernanceStackAuditResult().schema_version == "1910")
        _check("audit_result_executes_order_false",
               PaperGovernanceStackAuditResult().audit_executes_order is False)
        _check("module_schema", PaperGovernanceStackModule().schema_version == "1910")
        _check("version_model_schema", PaperGovernanceStackVersion().schema_version == "1910")
        _check("compat_result_schema",
               PaperGovernanceStackCompatibilityResult().schema_version == "1910")
        _check("compat_check_executes_order_false",
               PaperGovernanceStackCompatibilityResult().compatibility_check_executes_order is False)
        _check("cli_audit_schema", PaperGovernanceStackCliAuditResult().schema_version == "1910")
        _check("cli_audit_executes_order_false",
               PaperGovernanceStackCliAuditResult().audit_executes_order is False)
        _check("gui_audit_schema", PaperGovernanceStackGuiAuditResult().schema_version == "1910")
        _check("gui_audit_mutates_false",
               PaperGovernanceStackGuiAuditResult().dashboard_mutates_strategy is False)
        _check("health_audit_schema",
               PaperGovernanceStackHealthAuditResult().schema_version == "1910")
        _check("gate_audit_schema", PaperGovernanceStackGateAuditResult().schema_version == "1910")
        _check("fixture_audit_schema",
               PaperGovernanceStackFixtureAuditResult().schema_version == "1910")
        _check("scenario_audit_schema",
               PaperGovernanceStackScenarioAuditResult().schema_version == "1910")
        _check("safety_audit_schema",
               PaperGovernanceStackSafetyAuditResult().schema_version == "1910")
        _check("safety_audit_executes_order_false",
               PaperGovernanceStackSafetyAuditResult().audit_executes_order is False)
        _check("release_summary_schema",
               PaperGovernanceStackReleaseSummary().schema_version == "1910")
        _check("audit_report_schema",
               PaperGovernanceStackAuditReport().schema_version == "1910")
        _check("audit_report_executes_order_false",
               PaperGovernanceStackAuditReport().audit_executes_order is False)
        _check("audit_report_mutates_false",
               PaperGovernanceStackAuditReport().audit_mutates_strategy is False)
        _check("audit_report_triggers_real_order_false",
               PaperGovernanceStackAuditReport().report_triggers_real_order is False)
        _check("recommendation_schema",
               PaperGovernanceStackRecommendation().schema_version == "1910")
        _check("recommendation_executes_order_false",
               PaperGovernanceStackRecommendation().recommendation_executes_order is False)
        _check("recommendation_mutates_false",
               PaperGovernanceStackRecommendation().recommendation_mutates_strategy is False)
    except Exception as e:
        _check("models_import", False, str(e))

    # --- Safety audit ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_audit_v1910 import (
            run_safety_audit, assert_audit_safe, is_safe_export_path,
        )
        audit = run_safety_audit()
        _check("safety_audit_import", True)
        _check("safety_audit_all_safe", audit["all_safe"] is True)
        _check("safety_audit_errors_empty", audit["errors"] == [])
        _check("safe_path_ok", is_safe_export_path("C:/Users/paper/report.json") is True)
        _check("unsafe_path_blocked", is_safe_export_path("C:/production/live") is False)
        blocked = False
        try:
            assert_audit_safe("BUY")
        except ValueError:
            blocked = True
        _check("buy_action_blocked", blocked)
    except Exception as e:
        _check("safety_audit_import", False, str(e))

    # --- Engine functions ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_audit_v1910 import (
            audit_covered_modules, audit_cli_commands, audit_gui_tabs,
            audit_safety_flags, audit_backward_compatibility,
            run_full_governance_stack_audit, get_governance_stack_summary,
            get_version_info,
        )
        _check("engine_import", True)
        modules_r = audit_covered_modules()
        _check("audit_covered_modules_returns_dict", isinstance(modules_r, dict))
        _check("audit_covered_modules_paper_only", modules_r.get("paper_only") is True)
        safety_r = audit_safety_flags()
        _check("audit_safety_flags_returns_dict", isinstance(safety_r, dict))
        _check("audit_safety_flags_consistent", safety_r.get("all_consistent") is True)
        summary = get_governance_stack_summary()
        _check("get_governance_stack_summary_returns_dict", isinstance(summary, dict))
        _check("summary_version_correct", summary.get("version") == "1.9.10", "2.0.0")
        _check("summary_paper_only", summary.get("paper_only") is True)
        info = get_version_info()
        _check("get_version_info_returns_dict", isinstance(info, dict))
        _check("version_info_schema", info.get("schema_version") == "1910")
    except Exception as e:
        _check("engine_import", False, str(e))

    # --- Scenarios ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_scenarios_v1910 import SCENARIOS
        _check("scenarios_import", True)
        _check("scenarios_count_50", len(SCENARIOS) == 50)
        _check("scenarios_schema_1910",
               all(s.get("schema_version") == "1910" for s in SCENARIOS))
        _check("scenarios_paper_only",
               all(s.get("paper_only") is True for s in SCENARIOS))
        _check("scenarios_no_real_orders",
               all(s.get("no_real_orders") is True for s in SCENARIOS))
        _check("scenarios_production_blocked",
               all(s.get("production_trading_blocked") is True for s in SCENARIOS))
        _check("scenarios_consolidation_only",
               all(s.get("consolidation_only") is True for s in SCENARIOS))
        _check("scenarios_release_audit_only",
               all(s.get("release_audit_only") is True for s in SCENARIOS))
    except Exception as e:
        _check("scenarios_import", False, str(e))

    # --- Fixtures ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_fixtures_v1910 import FIXTURES
        _check("fixtures_import", True)
        _check("fixtures_count_50", len(FIXTURES) == 50)
        _check("fixtures_schema_1910",
               all(f.get("schema_version") == "1910" for f in FIXTURES))
        _check("fixtures_paper_only",
               all(f.get("paper_only") is True for f in FIXTURES))
        _check("fixtures_no_real_orders",
               all(f.get("no_real_orders") is True for f in FIXTURES))
        _check("fixtures_production_blocked",
               all(f.get("production_trading_blocked") is True for f in FIXTURES))
        _check("fixtures_consolidation_only",
               all(f.get("consolidation_only") is True for f in FIXTURES))
        _check("fixtures_release_audit_only",
               all(f.get("release_audit_only") is True for f in FIXTURES))
        _check("fixtures_have_fixture_id",
               all("fixture_id" in f for f in FIXTURES))
    except Exception as e:
        _check("fixtures_import", False, str(e))

    # --- GUI panel ---
    try:
        from gui.small_capital_strategy_panel import (
            PANEL_VERSION, PANEL_TITLE,
            render_governance_stack_audit_tab,
            render_release_audit_tab,
            render_compatibility_summary_tab,
            get_governance_stack_tab_names,
        )
        _check("gui_panel_import", True)
        _check("panel_version_1910", PANEL_VERSION in ("1.9.10", "2.0.0"), PANEL_VERSION)
        _check("panel_title_has_version",
               "1.9.10" in PANEL_TITLE or "Governance" in PANEL_TITLE
               or "Consolidation" in PANEL_TITLE or "2.0.0" in PANEL_TITLE)
        gov_tab = render_governance_stack_audit_tab()
        _check("governance_stack_audit_tab_paper_only",
               gov_tab.get("paper_only") is True)
        _check("governance_stack_audit_tab_mutates_false",
               gov_tab.get("dashboard_mutates_strategy") is False)
        rel_tab = render_release_audit_tab()
        _check("release_audit_tab_paper_only",
               rel_tab.get("paper_only") is True)
        compat_tab = render_compatibility_summary_tab()
        _check("compat_tab_executes_order_false",
               compat_tab.get("compatibility_check_executes_order") is False)
        tab_names = get_governance_stack_tab_names()
        _check("governance_stack_tab_names", "governance_stack_audit" in tab_names)
    except Exception as e:
        _check("gui_panel_import", False, str(e))

    # --- CLI registry ---
    try:
        from cli.command_registry import get_command
        _check("cli_registry_import", True)
        for cmd in [
            "governance-stack-version", "governance-stack-audit",
            "governance-stack-health", "governance-stack-gate",
            "governance-stack-report", "governance-stack-compatibility",
        ]:
            spec = get_command(cmd)
            _check(f"cli_cmd_{cmd.replace('-', '_')}", spec is not None)
    except Exception as e:
        _check("cli_registry_import", False, str(e))

    all_passed = failed == 0
    return {
        "all_passed": all_passed,
        "status": "PASS" if all_passed else "FAIL",
        "passed": passed,
        "failed": failed,
        "total": passed + failed,
        "checks": checks,
        "health_version": HEALTH_VERSION,
        "paper_only": True,
        "research_only": True,
        "consolidation_only": True,
        "release_audit_only": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


if __name__ == "__main__":
    result = run_health_check()
    print(f"v1.9.10 Governance Stack Health: {result['status']}  "
          f"{result['passed']}/{result['total']} passed")
    if result["failed"] > 0:
        for c in result["checks"]:
            if c["status"] == "FAIL":
                print(f"  FAIL: {c['name']}  {c.get('detail', '')}")
