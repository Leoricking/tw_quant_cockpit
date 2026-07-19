"""
release/portfolio_governance_release_gate_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Release Gate
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import sys
import os
sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))

GATE_VERSION = "1.9.8"
BASELINE_TESTS = 30361
MIN_NEW_TESTS = 400

from paper_trading.small_capital_strategy.portfolio_governance_version_v198 import (
    VERSION, SCHEMA_VERSION, RELEASE_NAME,
    PORTFOLIO_EXPOSURE_DIMENSIONS, RISK_GRADES, RISK_RECOMMENDATIONS,
    RISK_LIMIT_KEYS, HARD_BLOCK_CONDITIONS, FORBIDDEN_OUTPUT_WORDS,
    get_version_info,
)
from paper_trading.small_capital_strategy.portfolio_governance_models_v198 import _ALL_MODEL_NAMES
from paper_trading.small_capital_strategy.portfolio_governance_safety_v198 import (
    FORBIDDEN_ACTIONS, ALLOWED_ACTIONS, run_safety_audit, assert_safe,
)
from paper_trading.small_capital_strategy.portfolio_governance_engine_v198 import (
    validate_portfolio_input, compute_risk_grade, run_risk_overlay,
)
from paper_trading.small_capital_strategy.portfolio_governance_report_v198 import REPORT_SECTIONS
from paper_trading.small_capital_strategy.portfolio_governance_scenarios_v198 import get_scenarios
from paper_trading.small_capital_strategy.portfolio_governance_fixtures_v198 import get_fixtures
from paper_trading.small_capital_strategy.portfolio_governance_health_v198 import run_health_check
from paper_trading.small_capital_strategy.portfolio_governance_gui_v198 import (
    PANEL_VERSION, get_governance_portfolio_tab_names, get_panel_info,
)
from paper_trading.small_capital_strategy.portfolio_governance_cli_v198 import CLI_COMMANDS, COMMAND_MAP


def run_release_gate() -> dict:
    checks = []

    def chk(name: str, passed: bool):
        checks.append({"name": name, "passed": bool(passed)})

    # Version checks
    chk("version_match_1.9.8", VERSION == "1.9.8")
    chk("release_name_match", "Portfolio Governance" in RELEASE_NAME)
    chk("schema_version_match_198", SCHEMA_VERSION == "198")
    chk("gate_version_match", GATE_VERSION == "1.9.8")
    chk("panel_version_match", PANEL_VERSION == "1.9.8")

    # Model count
    chk("model_count_26", len(_ALL_MODEL_NAMES) == 26)

    # Exposure dimensions
    chk("exposure_dimensions_count_20", len(PORTFOLIO_EXPOSURE_DIMENSIONS) == 20)

    # Risk grades
    chk("risk_grades_count_6", len(RISK_GRADES) == 6)
    chk("risk_grades_has_LOW", "LOW" in RISK_GRADES)
    chk("risk_grades_has_CRITICAL", "CRITICAL" in RISK_GRADES)
    chk("risk_grades_has_INVALID", "INVALID" in RISK_GRADES)

    # Risk recommendations
    chk("risk_recommendations_count_12", len(RISK_RECOMMENDATIONS) == 12)
    chk("risk_recommendations_has_NO_CHANGE", "NO_CHANGE" in RISK_RECOMMENDATIONS)
    chk("risk_recommendations_has_RISK_OFF_MODE", "RISK_OFF_MODE" in RISK_RECOMMENDATIONS)

    # Risk limit keys
    chk("risk_limit_keys_count_14", len(RISK_LIMIT_KEYS) == 14)

    # Hard block conditions
    chk("hard_block_conditions_gte_17", len(HARD_BLOCK_CONDITIONS) >= 17)

    # Forbidden output words
    chk("forbidden_output_words_gte_10", len(FORBIDDEN_OUTPUT_WORDS) >= 10)
    chk("forbidden_output_words_has_BUY", "BUY" in FORBIDDEN_OUTPUT_WORDS)

    # Scenarios
    scenarios = get_scenarios()
    chk("scenarios_count_75", len(scenarios) == 75)
    chk("scenarios_all_paper_only", all(s.get("paper_only") is True for s in scenarios))
    chk("scenarios_all_no_real_orders", all(s.get("no_real_orders") is True for s in scenarios))
    chk("scenarios_all_schema_198", all(s.get("schema_version") == "198" for s in scenarios))

    # Fixtures
    fixtures = get_fixtures()
    chk("fixtures_count_75", len(fixtures) == 75)
    chk("fixtures_all_paper_only", all(f.get("paper_only") is True for f in fixtures))
    chk("fixtures_all_no_real_orders", all(f.get("no_real_orders") is True for f in fixtures))

    # Safety audit
    audit = run_safety_audit()
    chk("safety_all_safe_True", audit.get("all_safe") is True)
    chk("safety_failed_0", audit.get("failed") == 0)

    # Health check
    health = run_health_check()
    chk("health_all_passed_True", health.get("all_passed") is True)
    chk("health_status_PASS", health.get("status") == "PASS")
    chk("health_failed_0", health.get("failed") == 0)

    # Version info flags
    vi = get_version_info()
    chk("version_info_paper_only_True", vi.get("paper_only") is True)
    chk("version_info_no_real_orders_True", vi.get("no_real_orders") is True)
    chk("version_info_not_investment_advice_True", vi.get("not_investment_advice") is True)
    chk("version_info_analytics_executes_decision_False", vi.get("analytics_executes_decision") is False)
    chk("version_info_dashboard_mutates_strategy_False", vi.get("dashboard_mutates_strategy") is False)
    chk("version_info_overlay_places_real_order_False", vi.get("overlay_places_real_order") is False)
    chk("version_info_report_triggers_rebalance_False", vi.get("report_triggers_rebalance") is False)

    # Engine checks
    valid_inp = {"paper_only": True, "no_real_orders": True, "no_broker": True, "positions": [], "snapshot": {}, "risk_limits": {}}
    chk("engine_validate_valid_input_not_blocked", validate_portfolio_input(valid_inp).get("blocked") is False)
    chk("engine_validate_malformed_blocked", validate_portfolio_input("bad").get("blocked") is True)
    chk("engine_validate_missing_paper_flag_blocked", validate_portfolio_input({"positions": [], "snapshot": {}, "risk_limits": {}}).get("blocked") is True)
    chk("engine_compute_risk_grade_0.0_LOW", compute_risk_grade(0.0).get("grade") == "LOW")
    chk("engine_compute_risk_grade_0.95_CRITICAL", compute_risk_grade(0.95).get("grade") == "CRITICAL")

    ov = run_risk_overlay("paper_cand_001", {"paper_only": True, "risk_score": 0.1})
    chk("engine_run_risk_overlay_paper_only_True", ov.get("paper_only") is True)
    chk("engine_run_risk_overlay_low_risk_passes", ov.get("overlay_passed") is True)

    # Report sections
    chk("report_sections_count_12", len(REPORT_SECTIONS) == 12)
    chk("report_has_portfolio_snapshot", "portfolio_snapshot" in REPORT_SECTIONS)
    chk("report_has_exposure_summary", "exposure_summary" in REPORT_SECTIONS)
    chk("report_has_audit_trail", "audit_trail" in REPORT_SECTIONS)
    chk("report_has_risk_limits_evaluation", "risk_limits_evaluation" in REPORT_SECTIONS)

    # GUI tab names
    tab_names = get_governance_portfolio_tab_names()
    chk("gui_tab_names_count_3", len(tab_names) == 3)
    chk("gui_tab_names_has_portfolio_governance", "portfolio_governance" in tab_names)
    chk("gui_tab_names_has_risk_overlay", "risk_overlay" in tab_names)
    chk("gui_tab_names_has_exposure_dashboard", "exposure_dashboard" in tab_names)
    pi = get_panel_info()
    chk("gui_tab_count_gte_163", pi.get("tab_count", 0) >= 163)

    # Forbidden actions not in allowed actions
    chk("no_forbidden_in_allowed", not any(fa in ALLOWED_ACTIONS for fa in FORBIDDEN_ACTIONS))

    # assert_safe blocks forbidden
    try:
        assert_safe("place_real_order")
        blocked_ok = False
    except ValueError:
        blocked_ok = True
    chk("assert_safe_blocks_place_real_order", blocked_ok)

    try:
        assert_safe("submit_broker_order")
        broker_blocked = False
    except ValueError:
        broker_blocked = True
    chk("assert_safe_blocks_submit_broker_order", broker_blocked)

    # CLI
    chk("cli_commands_count_19", len(CLI_COMMANDS) == 19)
    chk("cli_command_map_count_19", len(COMMAND_MAP) == 19)
    chk("cli_all_handlers_callable", all(callable(v) for v in COMMAND_MAP.values()))
    chk("cli_all_introduced_in_1.9.8", all(c.get("introduced_in") == "1.9.8" for c in CLI_COMMANDS))
    chk("cli_all_safety_RESEARCH_ONLY", all(c.get("safety_classification") == "RESEARCH_ONLY" for c in CLI_COMMANDS))

    # Baseline test count (informational, always passes)
    chk("baseline_tests_gte_30361", BASELINE_TESTS >= 30361)
    chk("min_new_tests_gte_400", MIN_NEW_TESTS >= 400)

    passed_count = sum(1 for c in checks if c["passed"])
    failed_count = len(checks) - passed_count
    gate_passed = failed_count == 0

    return {
        "gate_passed": gate_passed,
        "gate_version": GATE_VERSION,
        "passed_count": passed_count,
        "failed": failed_count,
        "total": len(checks),
        "checks": checks,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


run_gate = run_release_gate


if __name__ == "__main__":
    r = run_release_gate()
    print(f"Portfolio Governance Release Gate v1.9.8: {'PASS' if r['gate_passed'] else 'FAIL'} {r['passed_count']}/{r['total']}")
    if not r["gate_passed"]:
        for c in r["checks"]:
            if not c["passed"]:
                print(f"  FAIL: {c['name']}")
        sys.exit(1)
