"""
paper_trading/small_capital_strategy/simulation_matrix_health_v181.py
Health checks for Simulation Scenario Matrix & Stress Test Lab v1.8.1. 60+ checks.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Callable, Dict, List

_SCHEMA  = "181"
_POLICY  = "1.8.1-simulation-scenario-matrix-stress-test"
MIN_HEALTH_CHECKS = 60


def _check(name: str, fn: Callable[[], bool]) -> Dict[str, Any]:
    try:
        passed = bool(fn())
        return {"name": name, "passed": passed, "error": None}
    except Exception as e:
        return {"name": name, "passed": False, "error": str(e)}


def _get_all_checks() -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []

    # ── Version checks (10) ─────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.simulation_matrix_version_v181 import (
        VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
        MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
        INCLUDED_RELEASES,
        get_version_info, verify_version, is_known_release, check_minimum_version,
    )
    checks.append(_check("version_181",
        lambda: VERSION == "1.8.1"))
    checks.append(_check("release_name_correct",
        lambda: RELEASE_NAME == "Simulation Scenario Matrix & Stress Test Lab"))
    checks.append(_check("base_release_correct",
        lambda: BASE_RELEASE == "1.8.0 Paper Simulation & Performance Lab"))
    checks.append(_check("schema_version_181",
        lambda: SCHEMA_VERSION == "181"))
    checks.append(_check("policy_version_correct",
        lambda: POLICY_VERSION == "1.8.1-simulation-scenario-matrix-stress-test"))
    checks.append(_check("verify_version_true",
        verify_version))
    checks.append(_check("known_release_v181",
        lambda: is_known_release("Simulation Scenario Matrix & Stress Test Lab")))
    checks.append(_check("version_info_dict",
        lambda: isinstance(get_version_info(), dict)))
    checks.append(_check("included_releases_count_ge11",
        lambda: len(INCLUDED_RELEASES) >= 11))
    checks.append(_check("check_minimum_version_self",
        lambda: check_minimum_version("1.8.1")))

    # ── Safety checks (12) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.simulation_matrix_safety_v181 import (
        run_safety_audit, assert_safe, get_safety_flags, SAFETY_FLAGS,
    )
    checks.append(_check("safety_paper_only",
        lambda: SAFETY_FLAGS["paper_only"] is True))
    checks.append(_check("safety_research_only",
        lambda: SAFETY_FLAGS["research_only"] is True))
    checks.append(_check("safety_simulate_only",
        lambda: SAFETY_FLAGS["simulate_only"] is True))
    checks.append(_check("safety_stress_test_only",
        lambda: SAFETY_FLAGS["stress_test_only"] is True))
    checks.append(_check("safety_no_real_orders",
        lambda: SAFETY_FLAGS["no_real_orders"] is True))
    checks.append(_check("safety_no_broker",
        lambda: SAFETY_FLAGS["no_broker"] is True))
    checks.append(_check("safety_no_margin",
        lambda: SAFETY_FLAGS["no_margin"] is True))
    checks.append(_check("safety_no_production_db_writes",
        lambda: SAFETY_FLAGS["no_production_db_writes"] is True))
    checks.append(_check("safety_real_order_false",
        lambda: SAFETY_FLAGS["real_order"] is False))
    checks.append(_check("safety_real_trading_false",
        lambda: SAFETY_FLAGS["real_trading"] is False))
    checks.append(_check("safety_broker_execution_false",
        lambda: SAFETY_FLAGS["broker_execution"] is False))
    checks.append(_check("safety_assert_no_raise",
        lambda: (assert_safe(), True)[1]))

    # ── Model checks (6) ────────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import (
        SimulationMatrixInput, SimulationMatrixConfig, SimulationMatrixAxis,
        SimulationMatrixCell, SimulationMatrixResult, StressTestScenario,
        StressTestResult, StressDrawdownShock, StressLosingStreakShock,
        StressRegimeShiftShock, StressThemeCollapseShock, StressMistakeInjection,
        RobustnessScore, ScenarioMatrixDashboard, ScenarioMatrixReport,
        ScenarioMatrixHealthSummary,
        get_all_model_names,
    )
    checks.append(_check("model_names_count_16",
        lambda: len(get_all_model_names()) == 16))
    checks.append(_check("model_input_paper_only",
        lambda: SimulationMatrixInput().paper_only is True))
    checks.append(_check("model_input_no_real_orders",
        lambda: SimulationMatrixInput().no_real_orders is True))
    checks.append(_check("model_dashboard_version",
        lambda: ScenarioMatrixDashboard().version == "1.8.1"))
    checks.append(_check("model_robustness_score_default",
        lambda: RobustnessScore().score == 0.0))
    checks.append(_check("model_robustness_paper_only",
        lambda: RobustnessScore().paper_only is True))

    # ── Engine checks (8) ───────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.simulation_matrix_engine_v181 import (
        ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
        validate_action, run_matrix_cell,
    )
    checks.append(_check("engine_allowed_actions_ge13",
        lambda: len(ALLOWED_OUTPUT_ACTIONS) >= 13))
    checks.append(_check("engine_forbidden_words_ge9",
        lambda: len(FORBIDDEN_OUTPUT_WORDS) >= 9))
    checks.append(_check("engine_validate_paper_entry_allowed",
        lambda: validate_action("PAPER_ENTRY_ALLOWED") is True))
    checks.append(_check("engine_validate_buy_false",
        lambda: validate_action("BUY") is False))
    checks.append(_check("engine_run_matrix_cell_paper_only",
        lambda: run_matrix_cell(SimulationMatrixInput()).paper_only is True))
    checks.append(_check("engine_no_BUY_in_allowed_actions",
        lambda: "BUY" not in ALLOWED_OUTPUT_ACTIONS))
    checks.append(_check("engine_stress_test_only_in_allowed",
        lambda: "STRESS_TEST_ONLY" in ALLOWED_OUTPUT_ACTIONS))
    checks.append(_check("engine_valid_grades_has_robust",
        lambda: "ROBUST" in VALID_FINAL_GRADES))

    # ── Stress engine checks (6) ─────────────────────────────────────────────
    from paper_trading.small_capital_strategy.simulation_stress_engine_v181 import (
        STRESS_TEST_TYPES, run_stress_test, run_all_stress_tests,
    )
    checks.append(_check("stress_types_ge10",
        lambda: len(STRESS_TEST_TYPES) >= 10))
    checks.append(_check("stress_run_market_crash_returns_result",
        lambda: isinstance(run_stress_test("MARKET_CRASH"), StressTestResult)))
    checks.append(_check("stress_market_crash_paper_only",
        lambda: run_stress_test("MARKET_CRASH").paper_only is True))
    checks.append(_check("stress_market_crash_stress_test_only",
        lambda: run_stress_test("MARKET_CRASH").stress_test_only is True))
    checks.append(_check("stress_run_all_ge10",
        lambda: len(run_all_stress_tests()) >= 10))
    checks.append(_check("stress_survived_count_is_int",
        lambda: isinstance(
            sum(1 for r in run_all_stress_tests() if r.survived), int
        )))

    # ── Scenario checks (5) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.simulation_matrix_scenarios_v181 import (
        get_scenario_count, get_all_scenarios, get_scenario_by_id,
        get_scenario_categories,
    )
    checks.append(_check("scenarios_count_ge75",
        lambda: get_scenario_count() >= 75))
    checks.append(_check("scenarios_all_have_id",
        lambda: all("id" in s for s in get_all_scenarios())))
    checks.append(_check("scenarios_all_paper_only_true",
        lambda: all(s.get("paper_only") is True for s in get_all_scenarios())))
    checks.append(_check("scenarios_categories_ge5",
        lambda: len(get_scenario_categories()) >= 5))
    checks.append(_check("scenarios_sm181_001_exists",
        lambda: get_scenario_by_id("SM181-001") is not None))

    # ── Report checks (4) ────────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.simulation_matrix_report_v181 import (
        REPORT_SECTIONS, get_report_info, get_report_section_names,
    )
    checks.append(_check("report_sections_ge10",
        lambda: len(REPORT_SECTIONS) >= 10))
    checks.append(_check("report_info_dict",
        lambda: isinstance(get_report_info(), dict)))
    checks.append(_check("report_has_matrix_summary",
        lambda: "matrix_summary" in REPORT_SECTIONS))
    checks.append(_check("report_has_final_grade",
        lambda: "final_grade" in REPORT_SECTIONS))

    # ── No forbidden words in ALLOWED_OUTPUT_ACTIONS (4) ────────────────────
    checks.append(_check("no_BUY_in_allowed_actions",
        lambda: "BUY" not in ALLOWED_OUTPUT_ACTIONS))
    checks.append(_check("no_SELL_in_allowed_actions",
        lambda: "SELL" not in ALLOWED_OUTPUT_ACTIONS))
    checks.append(_check("no_ORDER_in_allowed_actions",
        lambda: "ORDER" not in ALLOWED_OUTPUT_ACTIONS))
    checks.append(_check("no_EXECUTE_in_allowed_actions",
        lambda: "EXECUTE" not in ALLOWED_OUTPUT_ACTIONS))

    # ── Version threshold checks (5) ─────────────────────────────────────────
    checks.append(_check("version_min_scenarios_75",
        lambda: MIN_SCENARIOS == 75))
    checks.append(_check("version_min_fixtures_75",
        lambda: MIN_FIXTURES == 75))
    checks.append(_check("version_min_cli_20",
        lambda: MIN_CLI == 20))
    checks.append(_check("version_min_health_ge55",
        lambda: MIN_HEALTH >= 55))
    checks.append(_check("version_min_gate_ge55",
        lambda: MIN_GATE >= 55))

    return checks


def run_health_check() -> "ScenarioMatrixHealthSummary":
    """
    Run all health checks and return ScenarioMatrixHealthSummary.
    [!] Paper Only. Research Only. Simulate Only. No Real Orders.
    """
    from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import ScenarioMatrixHealthSummary
    checks = _get_all_checks()
    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    total = len(checks)
    all_passed = failed == 0
    status = "PASS" if all_passed else "FAIL"
    return ScenarioMatrixHealthSummary(
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
    print(f"[v1.8.1 Simulation Matrix Health]")
    print(f"  Status:  {result.status}")
    print(f"  Passed:  {result.passed} / {result.total}")
    print(f"  Failed:  {result.failed}")
    if result.failed > 0:
        for c in result.checks:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
    assert result.all_passed, f"Health check FAILED: {result.failed} failures"
    print("[OK] simulation_matrix_health_v181 PASS")
