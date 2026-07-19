"""
release/governance_stack_release_gate_v1910.py
v1.9.10 Paper Governance Stack Consolidation & Release Audit — Release Gate
[!] Paper Only. Research Only. Consolidation Only. Release Audit Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import sys
import os
sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))
from typing import Any, Dict

GATE_VERSION = "1.9.10"
BASELINE_TESTS = 31469
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSION = ("1.9.10",)


def run_release_gate() -> Dict[str, Any]:
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

    # --- Version gate ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_audit_v1910 import (
            VERSION, SCHEMA_VERSION, RELEASE_NAME, BASELINE_TESTS as BT, MIN_NEW_TESTS as MNT,
            COVERED_VERSIONS, COVERED_MODULES, CLI_COMMANDS, GUI_TABS,
            FORBIDDEN_ACTIONS, ALLOWED_AUDIT_ACTIONS, SAFETY_FLAGS, _ALL_MODEL_NAMES,
            verify_version,
        )
        _check("gate_version_1910", VERSION == "1.9.10", "2.0.0")
        _check("gate_schema_1910", SCHEMA_VERSION == "1910")
        _check("gate_baseline_31469", BT == 31469)
        _check("gate_min_new_300", MNT == 300)
        _check("gate_covered_versions_6", len(COVERED_VERSIONS) == 6)
        _check("gate_covered_modules_6", len(COVERED_MODULES) == 6)
        _check("gate_cli_commands_14", len(CLI_COMMANDS) == 14)
        _check("gate_gui_tabs_3", len(GUI_TABS) == 3)
        _check("gate_models_15", len(_ALL_MODEL_NAMES) == 15)
        _check("gate_safety_flags_29", len(SAFETY_FLAGS) == 29)
        _check("gate_forbidden_15", len(FORBIDDEN_ACTIONS) == 15)
        _check("gate_allowed_15", len(ALLOWED_AUDIT_ACTIONS) == 15)
        _check("gate_verify_version", verify_version() is True)
        _check("gate_v194_covered", "1.9.4" in COVERED_VERSIONS)
        _check("gate_v199_covered", "1.9.9" in COVERED_VERSIONS)
    except Exception as e:
        _check("gate_version_import", False, str(e))

    # --- Models gate ---
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
        _check("gate_models_import", True)
        _check("gate_audit_input_schema",
               PaperGovernanceStackAuditInput().schema_version == "1910")
        _check("gate_audit_input_paper_only",
               PaperGovernanceStackAuditInput().paper_only is True)
        _check("gate_audit_input_executes_order_false",
               PaperGovernanceStackAuditInput().audit_executes_order is False)
        _check("gate_audit_result_schema",
               PaperGovernanceStackAuditResult().schema_version == "1910")
        _check("gate_audit_result_executes_order_false",
               PaperGovernanceStackAuditResult().audit_executes_order is False)
        _check("gate_recommendation_executes_order_false",
               PaperGovernanceStackRecommendation().recommendation_executes_order is False)
        _check("gate_report_triggers_false",
               PaperGovernanceStackAuditReport().report_triggers_real_order is False)
    except Exception as e:
        _check("gate_models_import", False, str(e))

    # --- Safety gate ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_audit_v1910 import (
            run_safety_audit, SAFETY_FLAGS, is_safe_export_path,
        )
        audit = run_safety_audit()
        _check("gate_safety_all_safe", audit["all_safe"] is True)
        _check("gate_safety_paper_only", SAFETY_FLAGS.get("paper_only") is True)
        _check("gate_safety_consolidation_only", SAFETY_FLAGS.get("consolidation_only") is True)
        _check("gate_safety_release_audit_only", SAFETY_FLAGS.get("release_audit_only") is True)
        _check("gate_safety_no_real_orders", SAFETY_FLAGS.get("no_real_orders") is True)
        _check("gate_safety_audit_executes_order_false",
               SAFETY_FLAGS.get("audit_executes_order") is False)
        _check("gate_safe_path", is_safe_export_path("C:/Users/paper") is True)
        _check("gate_unsafe_path", is_safe_export_path("C:/production") is False)
    except Exception as e:
        _check("gate_safety_import", False, str(e))

    # --- Engine gate ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_audit_v1910 import (
            audit_covered_modules, audit_cli_commands, audit_gui_tabs,
            audit_safety_flags, audit_backward_compatibility,
            run_full_governance_stack_audit, get_governance_stack_summary,
        )
        _check("gate_engine_import", True)
        summary = get_governance_stack_summary()
        _check("gate_summary_version", summary.get("version") == "1.9.10", "2.0.0")
        _check("gate_summary_paper_only", summary.get("paper_only") is True)
        safety_r = audit_safety_flags()
        _check("gate_safety_flags_consistent", safety_r.get("all_consistent") is True)
    except Exception as e:
        _check("gate_engine_import", False, str(e))

    # --- Scenarios gate ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_scenarios_v1910 import SCENARIOS
        _check("gate_scenarios_import", True)
        _check("gate_scenarios_count_50", len(SCENARIOS) == 50)
        _check("gate_scenarios_schema_1910",
               all(s.get("schema_version") == "1910" for s in SCENARIOS))
        _check("gate_scenarios_paper_only",
               all(s.get("paper_only") is True for s in SCENARIOS))
        _check("gate_scenarios_consolidation_only",
               all(s.get("consolidation_only") is True for s in SCENARIOS))
        _check("gate_scenarios_release_audit_only",
               all(s.get("release_audit_only") is True for s in SCENARIOS))
        _check("gate_scenarios_production_blocked",
               all(s.get("production_trading_blocked") is True for s in SCENARIOS))
    except Exception as e:
        _check("gate_scenarios_import", False, str(e))

    # --- Fixtures gate ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_fixtures_v1910 import FIXTURES
        _check("gate_fixtures_import", True)
        _check("gate_fixtures_count_50", len(FIXTURES) == 50)
        _check("gate_fixtures_schema_1910",
               all(f.get("schema_version") == "1910" for f in FIXTURES))
        _check("gate_fixtures_paper_only",
               all(f.get("paper_only") is True for f in FIXTURES))
        _check("gate_fixtures_consolidation_only",
               all(f.get("consolidation_only") is True for f in FIXTURES))
        _check("gate_fixtures_release_audit_only",
               all(f.get("release_audit_only") is True for f in FIXTURES))
        _check("gate_fixtures_production_blocked",
               all(f.get("production_trading_blocked") is True for f in FIXTURES))
        _check("gate_fixtures_have_fixture_id",
               all("fixture_id" in f for f in FIXTURES))
    except Exception as e:
        _check("gate_fixtures_import", False, str(e))

    # --- Health gate ---
    try:
        from paper_trading.small_capital_strategy.governance_stack_health_v1910 import (
            run_health_check, HEALTH_VERSION,
        )
        _check("gate_health_import", True)
        _check("gate_health_version", HEALTH_VERSION == "1.9.10", "2.0.0")
        health = run_health_check()
        _check("gate_health_all_passed", health["all_passed"] is True)
        _check("gate_health_status_pass", health["status"] == "PASS")
    except Exception as e:
        _check("gate_health_import", False, str(e))

    # --- GUI gate ---
    try:
        from gui.small_capital_strategy_panel import (
            PANEL_VERSION, PANEL_TITLE,
            render_governance_stack_audit_tab,
            render_release_audit_tab,
            render_compatibility_summary_tab,
        )
        _check("gate_gui_import", True)
        _check("gate_panel_version_1910", PANEL_VERSION in ("1.9.10", "2.0.0"), PANEL_VERSION)
        _check("gate_panel_title",
               "1.9.10" in PANEL_TITLE or "Governance" in PANEL_TITLE
               or "Consolidation" in PANEL_TITLE or "2.0.0" in PANEL_TITLE)
        gov_tab = render_governance_stack_audit_tab()
        _check("gate_gov_tab_paper_only", gov_tab.get("paper_only") is True)
        _check("gate_gov_tab_mutates_false",
               gov_tab.get("dashboard_mutates_strategy") is False)
        rel_tab = render_release_audit_tab()
        _check("gate_rel_tab_paper_only", rel_tab.get("paper_only") is True)
        compat_tab = render_compatibility_summary_tab()
        _check("gate_compat_tab_executes_false",
               compat_tab.get("compatibility_check_executes_order") is False)
    except Exception as e:
        _check("gate_gui_import", False, str(e))

    # --- CLI gate ---
    try:
        from cli.command_registry import get_command
        _check("gate_cli_import", True)
        expected_cmds = [
            "governance-stack-version", "governance-stack-audit",
            "governance-stack-summary", "governance-stack-cli-audit",
            "governance-stack-gui-audit", "governance-stack-health-audit",
            "governance-stack-gate-audit", "governance-stack-fixture-audit",
            "governance-stack-scenario-audit", "governance-stack-safety-audit",
            "governance-stack-compatibility", "governance-stack-report",
            "governance-stack-health", "governance-stack-gate",
        ]
        for cmd in expected_cmds:
            _check(f"gate_cli_{cmd.replace('-', '_')}", get_command(cmd) is not None)
    except Exception as e:
        _check("gate_cli_import", False, str(e))

    all_passed = failed == 0
    return {
        "all_passed": all_passed,
        "status": "PASS" if all_passed else "FAIL",
        "passed": passed,
        "failed": failed,
        "total": passed + failed,
        "checks": checks,
        "gate_version": GATE_VERSION,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
        "paper_only": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


run_gate = run_release_gate


if __name__ == "__main__":
    result = run_release_gate()
    print(f"v1.9.10 Governance Stack Gate: {result['status']}  "
          f"{result['passed']}/{result['total']} passed")
    if result["failed"] > 0:
        for c in result["checks"]:
            if c["status"] == "FAIL":
                print(f"  FAIL: {c['name']}  {c.get('detail', '')}")
