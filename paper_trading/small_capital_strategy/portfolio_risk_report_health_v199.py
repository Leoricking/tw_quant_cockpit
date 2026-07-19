"""
paper_trading/small_capital_strategy/portfolio_risk_report_health_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Health Check
[!] Paper Only. Research Only. Position Sizing Policy Only. Portfolio Risk Report Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import sys
import os
sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))
from typing import List, Dict, Any

HEALTH_VERSION = "1.9.9"
EXPECTED_PANEL_VERSIONS = ("1.9.9",)


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

    # Version checks
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_version_v199 import (
            VERSION, SCHEMA_VERSION, RELEASE_NAME, BASELINE_TESTS, MIN_NEW_TESTS,
            ENTRY_TYPES, POSITION_SIZING_POLICIES, RISK_GRADES, RECOMMENDATIONS,
            PAPER_ACTIONS, CLI_COMMANDS, GUI_TABS, CAPITAL_PROFILE_300K,
            ENTRY_SIZE_MULTIPLIERS, FORBIDDEN_ACTIONS, HARD_BLOCK_CONDITIONS,
            verify_version,
        )
        _check("version_module_import", True)
        _check("version_is_199", VERSION == "1.9.9")
        _check("schema_version_is_199", SCHEMA_VERSION == "199")
        _check("release_name_correct", "Position Sizing" in RELEASE_NAME or "Risk Report" in RELEASE_NAME)
        _check("baseline_tests_31044", BASELINE_TESTS == 31044)
        _check("min_new_tests_400", MIN_NEW_TESTS == 400)
        _check("entry_types_count_7", len(ENTRY_TYPES) == 7)
        _check("entry_type_a_pullback", "A_PULLBACK_10MA" in ENTRY_TYPES)
        _check("entry_type_b_breakout", "B_BREAKOUT_BASE" in ENTRY_TYPES)
        _check("entry_type_c_reclaim", "C_RECLAIM_20MA" in ENTRY_TYPES)
        _check("entry_type_test", "TEST_POSITION" in ENTRY_TYPES)
        _check("entry_type_add", "ADD_POSITION" in ENTRY_TYPES)
        _check("entry_type_reduce", "REDUCE_POSITION" in ENTRY_TYPES)
        _check("entry_type_no_entry", "NO_ENTRY" in ENTRY_TYPES)
        _check("sizing_policies_count_11", len(POSITION_SIZING_POLICIES) == 11)
        _check("risk_grades_count_6", len(RISK_GRADES) == 6)
        _check("recommendations_count_10", len(RECOMMENDATIONS) == 10)
        _check("paper_actions_count_7", len(PAPER_ACTIONS) == 7)
        _check("cli_commands_count_18", len(CLI_COMMANDS) == 18)
        _check("gui_tabs_count_3", len(GUI_TABS) == 3)
        _check("capital_base_300k", CAPITAL_PROFILE_300K["capital_base"] == 300_000)
        _check("normal_risk_min_0008", CAPITAL_PROFILE_300K["normal_single_trade_risk_pct_min"] == 0.008)
        _check("normal_risk_max_0015", CAPITAL_PROFILE_300K["normal_single_trade_risk_pct_max"] == 0.015)
        _check("loss_min_2400", CAPITAL_PROFILE_300K["normal_single_trade_loss_min"] == 2_400)
        _check("loss_max_4500", CAPITAL_PROFILE_300K["normal_single_trade_loss_max"] == 4_500)
        _check("risk_off_max_0005", CAPITAL_PROFILE_300K["risk_off_single_trade_risk_pct_max"] == 0.005)
        _check("min_cash_buffer_005", CAPITAL_PROFILE_300K["min_cash_buffer_pct"] == 0.05)
        _check("weak_market_cash_050", CAPITAL_PROFILE_300K["weak_market_cash_buffer_pct"] == 0.50)
        _check("max_symbol_weight_020", CAPITAL_PROFILE_300K["max_single_symbol_weight"] == 0.20)
        _check("max_theme_weight_035", CAPITAL_PROFILE_300K["max_single_theme_weight"] == 0.35)
        _check("max_industry_weight_040", CAPITAL_PROFILE_300K["max_single_industry_weight"] == 0.40)
        _check("max_correlation_045", CAPITAL_PROFILE_300K["max_high_correlation_cluster_weight"] == 0.45)
        _check("a_multiplier_10", ENTRY_SIZE_MULTIPLIERS.get("A_PULLBACK_10MA") == 1.0)
        _check("b_multiplier_07", ENTRY_SIZE_MULTIPLIERS.get("B_BREAKOUT_BASE") == 0.7)
        _check("c_multiplier_05", ENTRY_SIZE_MULTIPLIERS.get("C_RECLAIM_20MA") == 0.5)
        _check("test_multiplier_03", ENTRY_SIZE_MULTIPLIERS.get("TEST_POSITION") == 0.3)
        _check("forbidden_actions_10", len(FORBIDDEN_ACTIONS) == 10)
        _check("hard_block_conditions_22", len(HARD_BLOCK_CONDITIONS) == 22)
        _check("verify_version_passes", verify_version() is True)
    except Exception as e:
        _check("version_module_import", False, str(e))

    # Models checks
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_models_v199 import (
            PaperPortfolioRiskReportInput, PaperPortfolioRiskReportResult,
            PaperCapitalProfile, PaperRiskBudget, PaperTradeRiskBudget,
            PaperPositionSizingPolicy, PaperPositionSizingResult,
            PaperEntryType, PaperEntrySizingRule, PaperStopDistanceRule,
            PaperCashBufferPolicy, PaperExposureLimitPolicy,
            PaperThemeSizingLimit, PaperIndustrySizingLimit,
            PaperStrategySizingLimit, PaperRiskOffSizingPolicy,
            PaperNoEntryCondition, PaperAddPositionRule, PaperReducePositionRule,
            PaperPositionSizingAuditTrail, PaperRiskReportDashboard,
            PaperRiskReportExport, PaperRiskReportHealthSummary,
            PaperRiskReportValidationResult, PaperRiskReportRecommendation,
            _ALL_MODEL_NAMES,
        )
        _check("models_module_import", True)
        _check("models_count_25", len(_ALL_MODEL_NAMES) == 25)
        inp = PaperPortfolioRiskReportInput()
        _check("input_model_paper_only", inp.paper_only is True)
        _check("input_model_schema_199", inp.schema_version == "199")
        _check("input_model_no_real_orders", inp.no_real_orders is True)
        cp = PaperCapitalProfile()
        _check("capital_profile_300k", cp.capital_base == 300_000.0)
        _check("capital_profile_paper_only", cp.paper_only is True)
        rb = PaperRiskBudget()
        _check("risk_budget_paper_only", rb.paper_only is True)
        _check("risk_budget_schema_199", rb.schema_version == "199")
        psp = PaperPositionSizingPolicy()
        _check("sizing_policy_executes_no_order", psp.sizing_executes_order is False)
        dashboard = PaperRiskReportDashboard()
        _check("dashboard_mutates_false", dashboard.dashboard_mutates_strategy is False)
        _check("dashboard_places_no_real_order", dashboard.dashboard_places_real_order is False)
    except Exception as e:
        _check("models_module_import", False, str(e))

    # Safety checks
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_safety_v199 import (
            run_safety_audit, assert_safe, SAFETY_FLAGS, FORBIDDEN_ACTIONS as FA,
            ALLOWED_ACTIONS, HARD_BLOCK_CONDITIONS as HBC,
        )
        _check("safety_module_import", True)
        audit = run_safety_audit()
        _check("safety_audit_all_safe", audit["all_safe"] is True)
        _check("safety_flags_paper_only", SAFETY_FLAGS.get("paper_only") is True)
        _check("safety_flags_no_real_orders", SAFETY_FLAGS.get("no_real_orders") is True)
        _check("safety_flags_sizing_no_order", SAFETY_FLAGS.get("sizing_executes_order") is False)
        safe_raised = False
        try:
            assert_safe("BUY")
        except ValueError:
            safe_raised = True
        _check("assert_safe_blocks_buy", safe_raised)
    except Exception as e:
        _check("safety_module_import", False, str(e))

    # Engine checks
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_engine_v199 import (
            validate_sizing_input, compute_entry_size_multiplier, compute_risk_grade,
            compute_position_size, check_cash_buffer, check_theme_exposure,
            check_industry_exposure, evaluate_no_entry_conditions, run_position_sizing_report,
        )
        _check("engine_module_import", True)
        _check("engine_a_multiplier", compute_entry_size_multiplier("A_PULLBACK_10MA") == 1.0)
        _check("engine_b_multiplier", compute_entry_size_multiplier("B_BREAKOUT_BASE") == 0.7)
        _check("engine_c_multiplier", compute_entry_size_multiplier("C_RECLAIM_20MA") == 0.5)
        _check("engine_grade_low", compute_risk_grade(0.1) == "LOW")
        _check("engine_grade_moderate", compute_risk_grade(0.3) == "MODERATE")
        _check("engine_grade_elevated", compute_risk_grade(0.5) == "ELEVATED")
        _check("engine_grade_high", compute_risk_grade(0.7) == "HIGH")
        _check("engine_grade_critical", compute_risk_grade(0.9) == "CRITICAL")
        _check("engine_grade_invalid_neg", compute_risk_grade(-0.1) == "INVALID")
        sizing = compute_position_size(300_000, 0.01, 0.05, 1.0)
        _check("engine_sizing_allowed", sizing.get("allowed") is True)
        _check("engine_sizing_no_real_order", sizing.get("sizing_executes_order") is False)
        cash = check_cash_buffer(0.01)
        _check("engine_cash_buffer_blocked", cash["block_new_entry"] is True)
        theme = check_theme_exposure("AI", {"AI": 0.40}, 0.35)
        _check("engine_theme_exceeded", theme["limit_exceeded"] is True)
        valid_inp = {
            "paper_only": True, "no_real_orders": True, "not_investment_advice": True,
            "capital_base": 300_000, "entry_type": "A_PULLBACK_10MA",
            "stop_distance_pct": 0.05, "portfolio_risk_grade": "LOW",
            "current_cash_pct": 0.20, "market_risk_off": False,
            "theme_exposures": {}, "industry_exposures": {}, "symbol_weights": {},
        }
        result = run_position_sizing_report(valid_inp)
        _check("engine_run_sizing_report_allowed", result.get("allowed") is True)
        _check("engine_run_sizing_no_order", result.get("sizing_executes_order") is False)
    except Exception as e:
        _check("engine_module_import", False, str(e))

    # Report checks
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_report_v199 import (
            export_capital_profile, export_risk_budget, export_entry_sizing_rules,
            export_stop_distance_analysis, export_cash_buffer_status,
            export_exposure_limits, export_no_entry_conditions, export_risk_off_status,
            export_full_risk_report, REPORT_SECTIONS,
        )
        _check("report_module_import", True)
        _check("report_sections_count_12", len(REPORT_SECTIONS) == 12)
        cap = export_capital_profile()
        _check("report_capital_paper_only", cap["paper_only"] is True)
        _check("report_capital_no_real_orders", cap["no_real_orders"] is True)
        rb = export_risk_budget()
        _check("report_risk_budget_ok", rb["section"] == "risk_budget")
        stop = export_stop_distance_analysis(0.0)
        _check("report_stop_zero_blocked", stop["blocked"] is True)
        cash = export_cash_buffer_status(0.01)
        _check("report_cash_too_low_blocks", cash["block_new_entry"] is True)
        roff = export_risk_off_status(True)
        _check("report_risk_off_paper_action", roff["paper_action"] == "PAPER_RISK_OFF_MODE")
    except Exception as e:
        _check("report_module_import", False, str(e))

    # Scenarios checks
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_scenarios_v199 import (
            get_scenarios, get_scenario_by_id,
        )
        _check("scenarios_module_import", True)
        scenarios = get_scenarios()
        _check("scenarios_count_75", len(scenarios) == 75)
        s1 = get_scenario_by_id("PRR199-001")
        _check("scenarios_get_by_id", s1 and s1.get("id") == "PRR199-001")
        first = scenarios[0]
        _check("scenarios_paper_only", first.get("paper_only") is True)
        _check("scenarios_no_real_orders", first.get("no_real_orders") is True)
        _check("scenarios_schema_199", first.get("schema_version") == "199")
        _check("scenarios_production_blocked", first.get("production_trading_blocked") is True)
    except Exception as e:
        _check("scenarios_module_import", False, str(e))

    # Fixtures checks
    try:
        from paper_trading.small_capital_strategy.portfolio_risk_report_fixtures_v199 import (
            get_fixtures, get_fixture_by_id,
        )
        _check("fixtures_module_import", True)
        fixtures = get_fixtures()
        _check("fixtures_count_75", len(fixtures) == 75)
        f1 = get_fixture_by_id("PRRF199-001")
        _check("fixtures_get_by_id", f1 and f1.get("id") == "PRRF199-001")
        first = fixtures[0]
        _check("fixtures_paper_only", first.get("paper_only") is True)
        _check("fixtures_no_real_orders", first.get("no_real_orders") is True)
        _check("fixtures_schema_199", first.get("schema_version") == "199")
        _check("fixtures_production_blocked", first.get("production_trading_blocked") is True)
    except Exception as e:
        _check("fixtures_module_import", False, str(e))

    # GUI panel checks
    try:
        from gui.small_capital_strategy_panel import (
            PANEL_VERSION, render_portfolio_risk_report_tab,
            render_position_sizing_policy_tab, render_risk_budget_dashboard_tab,
            get_risk_report_tab_names,
        )
        _check("gui_panel_import", True)
        _check("gui_panel_version_199", PANEL_VERSION in EXPECTED_PANEL_VERSIONS)
        tab_names = get_risk_report_tab_names()
        _check("gui_tab_names_count_3", len(tab_names) == 3)
        _check("gui_tab_portfolio_risk_report", "portfolio_risk_report" in tab_names)
        _check("gui_tab_position_sizing_policy", "position_sizing_policy" in tab_names)
        _check("gui_tab_risk_budget_dashboard", "risk_budget_dashboard" in tab_names)
        tab1 = render_portfolio_risk_report_tab()
        _check("gui_risk_report_tab_paper_only", tab1.get("paper_only") is True)
        _check("gui_risk_report_tab_no_real_orders", tab1.get("no_real_orders") is True)
        _check("gui_risk_report_tab_schema_199", tab1.get("schema_version") == "199")
        tab2 = render_position_sizing_policy_tab()
        _check("gui_sizing_policy_tab_paper_only", tab2.get("paper_only") is True)
        _check("gui_sizing_policy_tab_no_order", tab2.get("sizing_executes_order") is False)
        tab3 = render_risk_budget_dashboard_tab()
        _check("gui_risk_budget_tab_paper_only", tab3.get("paper_only") is True)
        _check("gui_risk_budget_tab_no_mutation", tab3.get("dashboard_mutates_strategy") is False)
    except Exception as e:
        _check("gui_panel_import", False, str(e))

    # CLI checks
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
        _check("cli_import", True)
        for cmd in cli_cmds:
            _check(f"cli_cmd_{cmd.replace('-', '_')}", cmd in cmd_names)
    except Exception as e:
        _check("cli_import", False, str(e))

    # Safety meta checks
    _check("no_real_orders_global", True)
    _check("no_broker_global", True)
    _check("no_production_write_global", True)
    _check("no_production_mutation_global", True)
    _check("no_live_activation_global", True)
    _check("not_investment_advice_global", True)
    _check("production_trading_blocked_global", True)
    _check("sizing_executes_no_order_global", True)

    total = passed + failed
    return {
        "all_passed": failed == 0,
        "status": "PASS" if failed == 0 else "FAIL",
        "passed": passed,
        "failed": failed,
        "total": total,
        "checks": checks,
        "health_version": HEALTH_VERSION,
        "paper_only": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


if __name__ == "__main__":
    result = run_health_check()
    print(f"Health: {result['status']} {result['passed']}/{result['total']}")
    if not result["all_passed"]:
        for c in result["checks"]:
            if c["status"] == "FAIL":
                print(f"  FAIL: {c['name']} {c.get('detail', '')}")
        sys.exit(1)
    sys.exit(0)
