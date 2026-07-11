"""
paper_trading/small_capital_strategy/paper_simulation_health_v180.py
Health checks for Paper Simulation & Performance Lab v1.8.0. 70+ checks.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Callable, Dict, List

_SCHEMA  = "180"
_POLICY  = "1.8.0-paper-simulation-performance-lab"
_LINEAGE = "paper_trading.small_capital_strategy.paper_simulation_health_v180"

MIN_HEALTH_CHECKS = 70


def _check(name: str, fn: Callable[[], bool]) -> Dict[str, Any]:
    try:
        passed = bool(fn())
        return {"name": name, "passed": passed, "error": None}
    except Exception as e:
        return {"name": name, "passed": False, "error": str(e)}


def _get_all_checks() -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []

    # ── Version checks (10) ─────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.paper_simulation_version_v180 import (
        VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
        MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
        KNOWN_RELEASE_NAMES, INCLUDED_RELEASES,
        get_version_info, verify_version, is_known_release, check_minimum_version,
    )
    checks.append(_check("version_180",               lambda: VERSION == "1.8.0"))
    checks.append(_check("release_name_correct",      lambda: RELEASE_NAME == "Paper Simulation & Performance Lab"))
    checks.append(_check("base_release_correct",      lambda: BASE_RELEASE == "1.7.9 Small Capital Strategy Stable Rollup"))
    checks.append(_check("schema_version_180",        lambda: SCHEMA_VERSION == "180"))
    checks.append(_check("policy_version_correct",    lambda: POLICY_VERSION == "1.8.0-paper-simulation-performance-lab"))
    checks.append(_check("verify_version_true",       verify_version))
    checks.append(_check("known_release_v180",        lambda: is_known_release("Paper Simulation & Performance Lab")))
    checks.append(_check("known_release_v179",        lambda: is_known_release("Small Capital Strategy Stable Rollup")))
    checks.append(_check("version_info_dict",         lambda: isinstance(get_version_info(), dict)))
    checks.append(_check("included_releases_count",   lambda: len(INCLUDED_RELEASES) >= 10))

    # ── Safety checks (12) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.paper_simulation_safety_v180 import (
        run_safety_audit, assert_safe, get_safety_flags, SAFETY_FLAGS,
    )
    checks.append(_check("safety_audit_all_safe",         lambda: run_safety_audit()["all_safe"]))
    checks.append(_check("safety_no_real_order",          lambda: SAFETY_FLAGS["real_order"] is False))
    checks.append(_check("safety_no_broker_exec",         lambda: SAFETY_FLAGS["broker_execution"] is False))
    checks.append(_check("safety_no_real_trading",        lambda: SAFETY_FLAGS["real_trading"] is False))
    checks.append(_check("safety_no_real_account",        lambda: SAFETY_FLAGS["real_account"] is False))
    checks.append(_check("safety_paper_only",             lambda: SAFETY_FLAGS["paper_only"] is True))
    checks.append(_check("safety_research_only",          lambda: SAFETY_FLAGS["research_only"] is True))
    checks.append(_check("safety_no_real_orders",         lambda: SAFETY_FLAGS["no_real_orders"] is True))
    checks.append(_check("safety_no_broker",              lambda: SAFETY_FLAGS["no_broker"] is True))
    checks.append(_check("safety_no_margin",              lambda: SAFETY_FLAGS["no_margin"] is True))
    checks.append(_check("safety_assert_no_raise",        lambda: (assert_safe(), True)[1]))
    checks.append(_check("safety_no_production_writes",   lambda: SAFETY_FLAGS["no_production_db_writes"] is True))

    # ── Model checks (17) ───────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import (
        PaperSimulationInput, PaperSimulationConfig, PaperSimulationScenario,
        PaperSimulationTrade, PaperSimulationPosition, PaperSimulationPortfolio,
        PaperSimulationResult, PaperPerformanceMetrics, PaperEquityCurve,
        PaperDrawdownReport, PaperRiskReport, PaperRegimePerformance,
        PaperThemePerformance, PaperABCPerformance, PaperMistakeImpactReport,
        PaperSimulationDashboard, PaperSimulationHealthSummary,
        get_all_model_names,
    )
    checks.append(_check("model_input_paper_only",        lambda: PaperSimulationInput().paper_only is True))
    checks.append(_check("model_input_no_real_orders",    lambda: PaperSimulationInput().no_real_orders is True))
    checks.append(_check("model_config_capital",          lambda: PaperSimulationConfig().initial_capital == 300000.0))
    checks.append(_check("model_config_risk_pcts",        lambda: len(PaperSimulationConfig().risk_per_trade_pcts) == 3))
    checks.append(_check("model_scenario_paper_only",     lambda: PaperSimulationScenario().paper_only is True))
    checks.append(_check("model_trade_paper_only",        lambda: PaperSimulationTrade().paper_only is True))
    checks.append(_check("model_position_paper_only",     lambda: PaperSimulationPosition().paper_only is True))
    checks.append(_check("model_portfolio_paper_only",    lambda: PaperSimulationPortfolio().paper_only is True))
    checks.append(_check("model_result_paper_only",       lambda: PaperSimulationResult().paper_only is True))
    checks.append(_check("model_metrics_grade_b",         lambda: PaperPerformanceMetrics().final_grade == "B"))
    checks.append(_check("model_equity_curve_empty",      lambda: isinstance(PaperEquityCurve().values, list)))
    checks.append(_check("model_drawdown_zero",           lambda: PaperDrawdownReport().max_drawdown_pct == 0.0))
    checks.append(_check("model_risk_report_pass",        lambda: PaperRiskReport().risk_status == "PASS"))
    checks.append(_check("model_regime_perf_bull",        lambda: PaperRegimePerformance().regime == "BULL"))
    checks.append(_check("model_theme_perf",              lambda: isinstance(PaperThemePerformance().theme, str)))
    checks.append(_check("model_abc_perf",                lambda: PaperABCPerformance().abc_type == "A"))
    checks.append(_check("model_mistake_impact",          lambda: PaperMistakeImpactReport().mistake_type == "none"))
    checks.append(_check("model_dashboard_version",       lambda: PaperSimulationDashboard().version == "1.8.0"))
    checks.append(_check("model_health_summary_pass",     lambda: PaperSimulationHealthSummary().status == "PASS"))
    checks.append(_check("model_names_count_17",          lambda: len(get_all_model_names()) == 17))

    # ── Engine checks (8) ───────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.paper_simulation_engine_v180 import (
        run_paper_simulation, get_action_for_input, get_engine_info,
        ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, validate_action,
    )
    checks.append(_check("engine_allowed_actions_nonempty",  lambda: len(ALLOWED_OUTPUT_ACTIONS) >= 9))
    checks.append(_check("engine_forbidden_words_nonempty",  lambda: len(FORBIDDEN_OUTPUT_WORDS) >= 9))
    checks.append(_check("engine_paper_entry_allowed",       lambda: (
        get_action_for_input(PaperSimulationInput(
            market_regime="BULL", theme_rank="LEADER", watchlist_rank="CORE",
            abc_buy_point="A", mistake_taxonomy_effect="none",
            risk_dashboard_status="PASS", integrated_decision="PAPER_ENTRY_ALLOWED",
        )) == "PAPER_ENTRY_ALLOWED"
    )))
    checks.append(_check("engine_blocked_on_risk_off",       lambda: (
        get_action_for_input(PaperSimulationInput(
            market_regime="RISK_OFF", integrated_decision="PAPER_ENTRY_ALLOWED",
        )) == "BLOCKED"
    )))
    checks.append(_check("engine_blocked_on_no_stop_loss",   lambda: (
        get_action_for_input(PaperSimulationInput(
            mistake_taxonomy_effect="no_stop_loss",
        )) == "BLOCKED"
    )))
    checks.append(_check("engine_validate_action_true",      lambda: validate_action("PAPER_ENTRY_ALLOWED")))
    checks.append(_check("engine_validate_forbidden_false",  lambda: not validate_action("BUY")))
    checks.append(_check("engine_run_returns_result",        lambda: (
        run_paper_simulation(PaperSimulationInput()).paper_only is True
    )))

    # ── Metrics checks (7) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.paper_simulation_metrics_v180 import (
        compute_metrics, compute_equity_curve, compute_drawdown_report,
        compute_risk_report, compute_regime_performance, compute_theme_performance,
        compute_abc_performance, compute_mistake_impact, get_metrics_info,
        VALID_GRADES,
    )
    checks.append(_check("metrics_empty_returns_metrics",   lambda: isinstance(compute_metrics([]), PaperPerformanceMetrics)))
    checks.append(_check("metrics_valid_grades_count",      lambda: len(VALID_GRADES) == 5))
    checks.append(_check("metrics_grade_a_in_grades",       lambda: "A" in VALID_GRADES))
    checks.append(_check("metrics_blocked_in_grades",       lambda: "BLOCKED" in VALID_GRADES))
    checks.append(_check("metrics_equity_curve_empty",      lambda: isinstance(compute_equity_curve([]), PaperEquityCurve)))
    checks.append(_check("metrics_drawdown_empty",          lambda: isinstance(
        compute_drawdown_report(compute_equity_curve([])), PaperDrawdownReport
    )))
    checks.append(_check("metrics_info_dict",               lambda: isinstance(get_metrics_info(), dict)))

    # ── Scenarios checks (5) ─────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.paper_simulation_scenarios_v180 import (
        get_scenario_count, get_all_scenarios, get_scenario_by_id,
        get_scenarios_by_category, get_scenario_categories, get_scenarios_info,
    )
    checks.append(_check("scenarios_count_ge_70",            lambda: get_scenario_count() >= 70))
    checks.append(_check("scenarios_all_have_id",            lambda: all("id" in s for s in get_all_scenarios())))
    checks.append(_check("scenarios_all_have_expected",      lambda: all("expected_action" in s for s in get_all_scenarios())))
    checks.append(_check("scenarios_sc180_001_exists",       lambda: get_scenario_by_id("SC180-001") is not None))
    checks.append(_check("scenarios_categories_nonempty",    lambda: len(get_scenario_categories()) >= 5))

    # ── Report checks (4) ────────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.paper_simulation_report_v180 import (
        get_report_info, get_report_section_names, REPORT_SECTIONS,
    )
    checks.append(_check("report_sections_count",            lambda: len(REPORT_SECTIONS) >= 10))
    checks.append(_check("report_info_dict",                 lambda: isinstance(get_report_info(), dict)))
    checks.append(_check("report_section_names_list",        lambda: isinstance(get_report_section_names(), list)))
    checks.append(_check("report_has_performance_metrics",   lambda: "performance_metrics" in REPORT_SECTIONS))

    # ── No forbidden action words in module source (4) ────────────────────────
    checks.append(_check("no_BUY_in_allowed_actions",        lambda: "BUY" not in ALLOWED_OUTPUT_ACTIONS))
    checks.append(_check("no_SELL_in_allowed_actions",       lambda: "SELL" not in ALLOWED_OUTPUT_ACTIONS))
    checks.append(_check("no_ORDER_in_allowed_actions",      lambda: "ORDER" not in ALLOWED_OUTPUT_ACTIONS))
    checks.append(_check("no_EXECUTE_in_allowed_actions",    lambda: "EXECUTE" not in ALLOWED_OUTPUT_ACTIONS))

    # ── Version minimum checks (3) ────────────────────────────────────────────
    checks.append(_check("version_min_scenarios_70",         lambda: MIN_SCENARIOS == 70))
    checks.append(_check("version_min_fixtures_70",          lambda: MIN_FIXTURES == 70))
    checks.append(_check("version_min_cli_19",               lambda: MIN_CLI == 19))

    return checks


def run_health_check() -> "PaperSimulationHealthSummary":
    """
    Run all health checks and return PaperSimulationHealthSummary.
    [!] Paper Only. Research Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.paper_simulation_models_v180 import PaperSimulationHealthSummary
    checks = _get_all_checks()
    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    total = len(checks)
    all_passed = failed == 0
    status = "PASS" if all_passed else "FAIL"
    return PaperSimulationHealthSummary(
        status=status,
        passed=passed,
        failed=failed,
        total=total,
        all_passed=all_passed,
        checks=checks,
        schema_version=_SCHEMA,
        paper_only=True,
        not_investment_advice=True,
        no_real_orders=True,
    )


if __name__ == "__main__":
    result = run_health_check()
    print(f"[v1.8.0 Paper Simulation Health]")
    print(f"  Status:  {result.status}")
    print(f"  Passed:  {result.passed} / {result.total}")
    print(f"  Failed:  {result.failed}")
    if result.failed > 0:
        for c in result.checks:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
    assert result.all_passed, f"Health check FAILED: {result.failed} failures"
    print("[OK] paper_simulation_health_v180 PASS")
