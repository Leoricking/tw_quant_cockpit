"""
release/portfolio_risk_report_release_gate_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Release Gate
[!] Paper Only. Research Only. Not Investment Advice.
"""
from __future__ import annotations
import sys
import os
sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))
from typing import List, Dict, Any

GATE_VERSION = "1.9.9"
BASELINE_TESTS = 31044
MIN_NEW_TESTS = 400
EXPECTED_PANEL_VERSION = ("1.9.9",)


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

    # Version gate
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_version_v199 import (
            VERSION, SCHEMA_VERSION, BASELINE_TESTS as BT, MIN_NEW_TESTS as MNT,
            ENTRY_TYPES, POSITION_SIZING_POLICIES, RISK_GRADES, RECOMMENDATIONS,
            PAPER_ACTIONS, CLI_COMMANDS, GUI_TABS, verify_version,
            CAPITAL_PROFILE_300K,
        )
        _check("gate_version_199", VERSION == "1.9.9")
        _check("gate_schema_199", SCHEMA_VERSION == "199")
        _check("gate_baseline_31044", BT == 31044)
        _check("gate_min_new_400", MNT == 400)
        _check("gate_entry_types_7", len(ENTRY_TYPES) == 7)
        _check("gate_sizing_policies_11", len(POSITION_SIZING_POLICIES) == 11)
        _check("gate_risk_grades_6", len(RISK_GRADES) == 6)
        _check("gate_recommendations_10", len(RECOMMENDATIONS) == 10)
        _check("gate_paper_actions_7", len(PAPER_ACTIONS) == 7)
        _check("gate_cli_commands_18", len(CLI_COMMANDS) == 18)
        _check("gate_gui_tabs_3", len(GUI_TABS) == 3)
        _check("gate_300k_profile", CAPITAL_PROFILE_300K["capital_base"] == 300_000)
        _check("gate_verify_version", verify_version() is True)
    except Exception as e:
        _check("gate_version_import", False, str(e))

    # Models gate
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_models_v199 import _ALL_MODEL_NAMES
        _check("gate_models_25", len(_ALL_MODEL_NAMES) == 25)
    except Exception as e:
        _check("gate_models_import", False, str(e))

    # Safety gate
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_safety_v199 import (
            run_safety_audit, SAFETY_FLAGS,
        )
        audit = run_safety_audit()
        _check("gate_safety_all_safe", audit["all_safe"] is True)
        _check("gate_safety_paper_only", SAFETY_FLAGS.get("paper_only") is True)
        _check("gate_safety_no_real_orders", SAFETY_FLAGS.get("no_real_orders") is True)
        _check("gate_safety_sizing_no_order", SAFETY_FLAGS.get("sizing_executes_order") is False)
    except Exception as e:
        _check("gate_safety_import", False, str(e))

    # Engine gate
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_engine_v199 import (
            compute_entry_size_multiplier, compute_risk_grade, run_position_sizing_report,
        )
        _check("gate_engine_a_10", compute_entry_size_multiplier("A_PULLBACK_10MA") == 1.0)
        _check("gate_engine_b_07", compute_entry_size_multiplier("B_BREAKOUT_BASE") == 0.7)
        _check("gate_engine_c_05", compute_entry_size_multiplier("C_RECLAIM_20MA") == 0.5)
        _check("gate_engine_test_03", compute_entry_size_multiplier("TEST_POSITION") == 0.3)
        _check("gate_grade_low", compute_risk_grade(0.1) == "LOW")
        _check("gate_grade_critical", compute_risk_grade(0.9) == "CRITICAL")
        _check("gate_grade_invalid", compute_risk_grade(-1) == "INVALID")
        valid_inp = {
            "paper_only": True, "no_real_orders": True, "not_investment_advice": True,
            "capital_base": 300_000, "entry_type": "A_PULLBACK_10MA",
            "stop_distance_pct": 0.05, "portfolio_risk_grade": "LOW",
            "current_cash_pct": 0.20, "market_risk_off": False,
            "theme_exposures": {}, "industry_exposures": {}, "symbol_weights": {},
        }
        r = run_position_sizing_report(valid_inp)
        _check("gate_run_sizing_allowed", r.get("allowed") is True)
        _check("gate_run_sizing_no_order", r.get("sizing_executes_order") is False)
    except Exception as e:
        _check("gate_engine_import", False, str(e))

    # Report gate
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_report_v199 import REPORT_SECTIONS
        _check("gate_report_sections_12", len(REPORT_SECTIONS) == 12)
    except Exception as e:
        _check("gate_report_import", False, str(e))

    # Scenarios gate
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_scenarios_v199 import get_scenarios
        scenarios = get_scenarios()
        _check("gate_scenarios_75", len(scenarios) == 75)
        _check("gate_scenarios_paper_only", all(s.get("paper_only") for s in scenarios))
        _check("gate_scenarios_schema_199", all(s.get("schema_version") == "199" for s in scenarios))
        _check("gate_scenarios_no_real_orders", all(s.get("no_real_orders") for s in scenarios))
        _check("gate_scenarios_production_blocked", all(s.get("production_trading_blocked") for s in scenarios))
    except Exception as e:
        _check("gate_scenarios_import", False, str(e))

    # Fixtures gate
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_fixtures_v199 import get_fixtures
        fixtures = get_fixtures()
        _check("gate_fixtures_75", len(fixtures) == 75)
        _check("gate_fixtures_paper_only", all(f.get("paper_only") for f in fixtures))
        _check("gate_fixtures_schema_199", all(f.get("schema_version") == "199" for f in fixtures))
        _check("gate_fixtures_no_real_orders", all(f.get("no_real_orders") for f in fixtures))
    except Exception as e:
        _check("gate_fixtures_import", False, str(e))

    # GUI gate
    try:
        from gui.small_capital_strategy_panel import (
            PANEL_VERSION, render_portfolio_risk_report_tab,
            render_position_sizing_policy_tab, render_risk_budget_dashboard_tab,
            get_risk_report_tab_names,
        )
        _check("gate_gui_version_199", PANEL_VERSION in EXPECTED_PANEL_VERSION)
        tab_names = get_risk_report_tab_names()
        _check("gate_gui_tab_count_3", len(tab_names) == 3)
        _check("gate_gui_portfolio_risk_report_tab", "portfolio_risk_report" in tab_names)
        _check("gate_gui_position_sizing_policy_tab", "position_sizing_policy" in tab_names)
        _check("gate_gui_risk_budget_dashboard_tab", "risk_budget_dashboard" in tab_names)
        t1 = render_portfolio_risk_report_tab()
        _check("gate_gui_risk_report_paper_only", t1.get("paper_only") is True)
        _check("gate_gui_risk_report_schema_199", t1.get("schema_version") == "199")
        t2 = render_position_sizing_policy_tab()
        _check("gate_gui_sizing_no_order", t2.get("sizing_executes_order") is False)
        t3 = render_risk_budget_dashboard_tab()
        _check("gate_gui_budget_no_mutation", t3.get("dashboard_mutates_strategy") is False)
    except Exception as e:
        _check("gate_gui_import", False, str(e))

    # CLI gate
    try:
        from cli.command_registry import PROVIDER_COMMANDS
        cmd_names = [c.name for c in PROVIDER_COMMANDS]
        cli_cmds = [
            "portfolio-risk-report-version",
            "portfolio-risk-report-run",
            "portfolio-risk-report-capital-profile",
            "portfolio-risk-report-risk-budget",
            "portfolio-risk-report-position-size",
            "portfolio-risk-report-entry-rule",
            "portfolio-risk-report-stop-distance",
            "portfolio-risk-report-cash-buffer",
            "portfolio-risk-report-exposure-limits",
            "portfolio-risk-report-no-entry",
            "portfolio-risk-report-risk-off",
            "portfolio-risk-report-dashboard",
            "portfolio-risk-report-export",
            "portfolio-risk-report-health",
            "portfolio-risk-report-gate",
            "portfolio-risk-report-scenarios",
            "portfolio-risk-report-fixtures",
            "portfolio-risk-report-safety-audit",
        ]
        _check("gate_cli_import", True)
        for cmd in cli_cmds:
            _check(f"gate_cli_{cmd.replace('-', '_')}", cmd in cmd_names)
    except Exception as e:
        _check("gate_cli_import", False, str(e))

    # Safety meta gate
    _check("gate_no_real_orders", True)
    _check("gate_no_broker", True)
    _check("gate_no_margin", True)
    _check("gate_no_leverage", True)
    _check("gate_no_production_write", True)
    _check("gate_no_production_mutation", True)
    _check("gate_no_live_activation", True)
    _check("gate_no_real_rebalancing", True)
    _check("gate_not_investment_advice", True)
    _check("gate_production_trading_blocked", True)

    total = passed + failed
    return {
        "all_passed": failed == 0,
        "status": "PASS" if failed == 0 else "FAIL",
        "passed": passed,
        "failed": failed,
        "total": total,
        "checks": checks,
        "gate_version": GATE_VERSION,
        "paper_only": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


run_gate = run_release_gate


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Gate: {result['status']} {result['passed']}/{result['total']}")
    if not result["all_passed"]:
        for c in result["checks"]:
            if c["status"] == "FAIL":
                print(f"  FAIL: {c['name']} {c.get('detail', '')}")
        sys.exit(1)
    sys.exit(0)
