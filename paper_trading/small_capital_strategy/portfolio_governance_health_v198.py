"""
paper_trading/small_capital_strategy/portfolio_governance_health_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Health Check
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import sys
import os
sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))

from paper_trading.small_capital_strategy.portfolio_governance_version_v198 import (
    VERSION, SCHEMA_VERSION, RELEASE_NAME,
    PORTFOLIO_EXPOSURE_DIMENSIONS, RISK_GRADES, RISK_RECOMMENDATIONS,
    RISK_LIMIT_KEYS, DASHBOARD_PANELS, HARD_BLOCK_CONDITIONS,
    FORBIDDEN_OUTPUT_WORDS, _PAPER_HEADER,
    get_version_info, verify_version, get_exposure_dimensions,
    get_risk_grades, get_risk_recommendations, get_risk_limit_keys,
    get_dashboard_panels, get_hard_block_conditions, get_forbidden_output_words,
)
from paper_trading.small_capital_strategy.portfolio_governance_models_v198 import (
    _ALL_MODEL_NAMES,
    PaperPortfolioGovernanceInput, PaperPortfolioGovernanceResult,
    PaperPortfolioSnapshot, PaperPortfolioPosition,
    PaperPortfolioRiskOverlay, PaperPortfolioRiskLimit,
    PaperPortfolioGovernanceDashboard, PaperPortfolioGovernanceReport,
    PaperPortfolioAuditTrail, PaperPortfolioValidationResult,
)
from paper_trading.small_capital_strategy.portfolio_governance_safety_v198 import (
    SAFETY_FLAGS, FORBIDDEN_ACTIONS, ALLOWED_ACTIONS,
    HARD_BLOCK_CONDITIONS as SAFETY_HARD_BLOCKS,
    run_safety_audit, assert_safe,
)
from paper_trading.small_capital_strategy.portfolio_governance_engine_v198 import (
    validate_portfolio_input, validate_risk_grade, validate_risk_recommendation,
    compute_risk_score, compute_risk_grade, evaluate_risk_limits,
    detect_concentration_risk, detect_correlation_risk, run_risk_overlay,
    generate_recommendations, build_exposure_summary, build_portfolio_dashboard,
    build_governance_report, build_audit_trail_entry, export_governance_pack,
)
from paper_trading.small_capital_strategy.portfolio_governance_report_v198 import (
    REPORT_SECTIONS, export_full_governance_pack,
)
from paper_trading.small_capital_strategy.portfolio_governance_scenarios_v198 import get_scenarios
from paper_trading.small_capital_strategy.portfolio_governance_fixtures_v198 import get_fixtures
from paper_trading.small_capital_strategy.portfolio_governance_gui_v198 import (
    PANEL_VERSION, PANEL_TITLE, get_panel_info,
    get_governance_portfolio_tab_names, render_all_tabs,
    render_portfolio_governance_tab, render_risk_overlay_tab, render_exposure_dashboard_tab,
)
from paper_trading.small_capital_strategy.portfolio_governance_cli_v198 import (
    CLI_COMMANDS, COMMAND_MAP,
)


def run_health_check() -> dict:
    checks = []

    def chk(name: str, passed: bool):
        checks.append({"name": name, "passed": passed})

    # Version checks
    chk("version_is_1.9.8", VERSION == "1.9.8")
    chk("schema_version_is_198", SCHEMA_VERSION == "198")
    chk("release_name_contains_governance", "Governance" in RELEASE_NAME)
    chk("release_name_contains_risk_overlay", "Risk Overlay" in RELEASE_NAME)
    chk("verify_version_returns_True", verify_version() is True)

    # Exposure dimensions
    chk("exposure_dimensions_count_20", len(PORTFOLIO_EXPOSURE_DIMENSIONS) == 20)
    chk("exposure_dimensions_has_symbol_exposure", "symbol_exposure" in PORTFOLIO_EXPOSURE_DIMENSIONS)
    chk("exposure_dimensions_has_tsmc_sensitivity", "tsmc_sensitivity" in PORTFOLIO_EXPOSURE_DIMENSIONS)
    chk("get_exposure_dimensions_returns_list", isinstance(get_exposure_dimensions(), list))
    chk("get_exposure_dimensions_count_20", len(get_exposure_dimensions()) == 20)

    # Risk grades
    chk("risk_grades_count_6", len(RISK_GRADES) == 6)
    chk("risk_grades_has_LOW", "LOW" in RISK_GRADES)
    chk("risk_grades_has_CRITICAL", "CRITICAL" in RISK_GRADES)
    chk("risk_grades_has_INVALID", "INVALID" in RISK_GRADES)
    chk("get_risk_grades_returns_list", isinstance(get_risk_grades(), list))

    # Risk recommendations
    chk("risk_recommendations_count_12", len(RISK_RECOMMENDATIONS) == 12)
    chk("risk_recommendations_has_NO_CHANGE", "NO_CHANGE" in RISK_RECOMMENDATIONS)
    chk("risk_recommendations_has_RISK_OFF_MODE", "RISK_OFF_MODE" in RISK_RECOMMENDATIONS)
    chk("get_risk_recommendations_returns_list", isinstance(get_risk_recommendations(), list))

    # Risk limit keys
    chk("risk_limit_keys_count_14", len(RISK_LIMIT_KEYS) == 14)
    chk("risk_limit_keys_has_max_single_symbol_weight", "max_single_symbol_weight" in RISK_LIMIT_KEYS)
    chk("get_risk_limit_keys_returns_list", isinstance(get_risk_limit_keys(), list))

    # Hard block conditions
    chk("hard_block_conditions_gte_17", len(HARD_BLOCK_CONDITIONS) >= 17)
    chk("hard_block_has_real_order_requested", "real_order_requested" in HARD_BLOCK_CONDITIONS)
    chk("get_hard_block_conditions_returns_list", isinstance(get_hard_block_conditions(), list))

    # Forbidden output words
    chk("forbidden_output_words_gte_10", len(FORBIDDEN_OUTPUT_WORDS) >= 10)
    chk("forbidden_output_words_has_BUY", "BUY" in FORBIDDEN_OUTPUT_WORDS)
    chk("get_forbidden_output_words_returns_list", isinstance(get_forbidden_output_words(), list))

    # Model count
    chk("model_count_26", len(_ALL_MODEL_NAMES) == 26)
    chk("model_names_are_strings", all(isinstance(n, str) for n in _ALL_MODEL_NAMES))

    # Model paper_only
    chk("GovernanceInput_paper_only", PaperPortfolioGovernanceInput().paper_only is True)
    chk("GovernanceInput_schema_198", PaperPortfolioGovernanceInput().schema_version == "198")
    chk("GovernanceResult_paper_only", PaperPortfolioGovernanceResult().paper_only is True)
    chk("Snapshot_paper_only", PaperPortfolioSnapshot().paper_only is True)
    chk("Position_paper_only", PaperPortfolioPosition().paper_only is True)
    chk("RiskOverlay_no_real_orders", PaperPortfolioRiskOverlay().no_real_orders is True)
    chk("Dashboard_dashboard_mutates_strategy_False", PaperPortfolioGovernanceDashboard().dashboard_mutates_strategy is False)
    chk("Report_report_triggers_rebalance_False", PaperPortfolioGovernanceReport().report_triggers_rebalance is False)
    chk("AuditTrail_immutable_True", PaperPortfolioAuditTrail().immutable is True)
    chk("ValidationResult_paper_only", PaperPortfolioValidationResult().paper_only is True)

    # Safety flags
    chk("safety_paper_only_True", SAFETY_FLAGS.get("paper_only") is True)
    chk("safety_no_real_orders_True", SAFETY_FLAGS.get("no_real_orders") is True)
    chk("safety_analytics_executes_decision_False", SAFETY_FLAGS.get("analytics_executes_decision") is False)
    chk("safety_dashboard_mutates_strategy_False", SAFETY_FLAGS.get("dashboard_mutates_strategy") is False)
    chk("safety_overlay_places_real_order_False", SAFETY_FLAGS.get("overlay_places_real_order") is False)
    chk("safety_report_triggers_rebalance_False", SAFETY_FLAGS.get("report_triggers_rebalance") is False)
    chk("safety_broker_connection_enabled_False", SAFETY_FLAGS.get("broker_connection_enabled") is False)

    # Safety audit
    audit = run_safety_audit()
    chk("safety_audit_all_safe_True", audit.get("all_safe") is True)
    chk("safety_audit_failed_0", audit.get("failed") == 0)
    chk("safety_audit_passed_gt_0", audit.get("passed", 0) > 0)

    # Forbidden actions
    chk("forbidden_actions_count_15", len(FORBIDDEN_ACTIONS) == 15)
    chk("forbidden_actions_has_place_real_order", "place_real_order" in FORBIDDEN_ACTIONS)
    chk("allowed_actions_count_20", len(ALLOWED_ACTIONS) == 20)
    chk("allowed_actions_has_run_portfolio_governance", "run_portfolio_governance" in ALLOWED_ACTIONS)

    # Engine functions
    valid_inp = {"paper_only": True, "no_real_orders": True, "no_broker": True, "positions": [], "snapshot": {}, "risk_limits": {}}
    vi = validate_portfolio_input(valid_inp)
    chk("validate_portfolio_input_valid_not_blocked", vi.get("blocked") is False)

    bad_inp = "not_a_dict"
    bi = validate_portfolio_input(bad_inp)
    chk("validate_portfolio_input_malformed_blocked", bi.get("blocked") is True)

    missing_flag = {"positions": [], "snapshot": {}, "risk_limits": {}}
    mf = validate_portfolio_input(missing_flag)
    chk("validate_portfolio_input_missing_flag_blocked", mf.get("blocked") is True)

    # validate_risk_grade
    chk("validate_risk_grade_LOW_valid", validate_risk_grade("LOW").get("valid") is True)
    chk("validate_risk_grade_UNKNOWN_invalid", validate_risk_grade("UNKNOWN").get("valid") is False)

    # compute_risk_grade
    chk("compute_risk_grade_0.0_is_LOW", compute_risk_grade(0.0).get("grade") == "LOW")
    chk("compute_risk_grade_0.95_is_CRITICAL", compute_risk_grade(0.95).get("grade") == "CRITICAL")

    # run_risk_overlay
    ov = run_risk_overlay("EXECUTE_candidate", {"paper_only": True})
    chk("run_risk_overlay_blocks_forbidden_word", ov.get("blocked") is True)

    ov2 = run_risk_overlay("paper_candidate_001", {"paper_only": True, "risk_score": 0.1})
    chk("run_risk_overlay_passes_low_risk", ov2.get("overlay_passed") is True)

    # generate_recommendations
    rec = generate_recommendations("LOW", [])
    chk("generate_recommendations_returns_dict", isinstance(rec, dict))
    chk("generate_recommendations_has_recommendations", "recommendations" in rec)

    # Scenarios and fixtures
    scenarios = get_scenarios()
    chk("scenarios_count_75", len(scenarios) == 75)
    chk("scenarios_all_paper_only", all(s.get("paper_only") is True for s in scenarios))

    fixtures = get_fixtures()
    chk("fixtures_count_75", len(fixtures) == 75)
    chk("fixtures_all_paper_only", all(f.get("paper_only") is True for f in fixtures))

    # Report sections
    chk("report_sections_count_12", len(REPORT_SECTIONS) == 12)
    chk("report_sections_has_audit_trail", "audit_trail" in REPORT_SECTIONS)

    # export_full_governance_pack
    pack = export_full_governance_pack()
    chk("export_full_governance_pack_returns_dict", isinstance(pack, dict))
    chk("export_full_governance_pack_paper_only_True", pack.get("paper_only") is True)

    # GUI
    chk("panel_version_1.9.8", PANEL_VERSION == "1.9.8")
    chk("panel_title_contains_1.9.8", "1.9.8" in PANEL_TITLE)
    chk("panel_title_contains_Governance", "Governance" in PANEL_TITLE)
    tab_names = get_governance_portfolio_tab_names()
    chk("governance_tab_names_count_3", len(tab_names) == 3)
    chk("tab_names_has_portfolio_governance", "portfolio_governance" in tab_names)
    chk("tab_names_has_risk_overlay", "risk_overlay" in tab_names)
    chk("tab_names_has_exposure_dashboard", "exposure_dashboard" in tab_names)
    pi = get_panel_info()
    chk("panel_info_paper_only_True", pi.get("paper_only") is True)
    chk("panel_info_tab_count_gte_163", pi.get("tab_count", 0) >= 163)

    pg_tab = render_portfolio_governance_tab()
    chk("render_portfolio_governance_tab_paper_only", pg_tab.get("paper_only") is True)
    chk("render_portfolio_governance_tab_no_real_orders", pg_tab.get("no_real_orders") is True)
    chk("render_portfolio_governance_tab_portfolio_governance_only", pg_tab.get("portfolio_governance_only") is True)
    chk("render_portfolio_governance_tab_dashboard_mutates_strategy_False", pg_tab.get("dashboard_mutates_strategy") is False)

    ro_tab = render_risk_overlay_tab()
    chk("render_risk_overlay_tab_paper_only", ro_tab.get("paper_only") is True)
    chk("render_risk_overlay_tab_risk_overlay_only", ro_tab.get("risk_overlay_only") is True)

    ed_tab = render_exposure_dashboard_tab()
    chk("render_exposure_dashboard_tab_paper_only", ed_tab.get("paper_only") is True)
    chk("render_exposure_dashboard_tab_exposure_dashboard_only", ed_tab.get("exposure_dashboard_only") is True)

    all_tabs = render_all_tabs()
    chk("render_all_tabs_has_portfolio_governance", "portfolio_governance" in all_tabs)
    chk("render_all_tabs_has_risk_overlay", "risk_overlay" in all_tabs)
    chk("render_all_tabs_has_exposure_dashboard", "exposure_dashboard" in all_tabs)

    # CLI
    chk("cli_commands_count_19", len(CLI_COMMANDS) == 19)
    chk("cli_command_map_count_19", len(COMMAND_MAP) == 19)
    chk("cli_all_handlers_callable", all(callable(v) for v in COMMAND_MAP.values()))
    chk("cli_all_introduced_in_1.9.8", all(c.get("introduced_in") == "1.9.8" for c in CLI_COMMANDS))
    chk("cli_all_safety_RESEARCH_ONLY", all(c.get("safety_classification") == "RESEARCH_ONLY" for c in CLI_COMMANDS))

    # Paper header
    chk("paper_header_paper_only_True", _PAPER_HEADER.get("paper_only") is True)
    chk("paper_header_no_real_orders_True", _PAPER_HEADER.get("no_real_orders") is True)
    chk("paper_header_analytics_executes_decision_False", _PAPER_HEADER.get("analytics_executes_decision") is False)
    chk("paper_header_dashboard_mutates_strategy_False", _PAPER_HEADER.get("dashboard_mutates_strategy") is False)

    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    total = len(checks)
    all_passed = failed == 0

    return {
        "all_passed": all_passed,
        "status": "PASS" if all_passed else "FAIL",
        "passed": passed,
        "failed": failed,
        "total": total,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "version": "1.9.8",
        "checks": checks,
    }


if __name__ == "__main__":
    result = run_health_check()
    print(f"Portfolio Governance Health v1.9.8: {result['status']} {result['passed']}/{result['total']}")
    if not result["all_passed"]:
        for c in result.get("checks", []):
            if not c["passed"]:
                print(f"  FAIL: {c['name']}")
        sys.exit(1)
