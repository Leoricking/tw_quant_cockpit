"""
release/simulation_scenario_matrix_release_gate_v181.py
Release gate for Simulation Scenario Matrix & Stress Test Lab v1.8.1. 55+ checks.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.8.1"
MIN_CHECKS   = 55


class SimulationMatrixReleaseGate:
    """Release gate for Simulation Scenario Matrix & Stress Test Lab v1.8.1."""

    def __init__(self) -> None:
        self._checks: List[Dict[str, Any]] = []

    def _check(self, name: str, fn) -> None:
        try:
            result = fn()
            ok = bool(result)
        except Exception as exc:
            ok = False
            result = str(exc)
        self._checks.append({"name": name, "passed": ok,
                              "error": None if ok else str(result)})

    def run(self) -> Dict[str, Any]:
        """Run all gate checks and return result dict."""
        self._checks = []

        # ── Health PASS (4) ─────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.simulation_matrix_health_v181 import run_health_check
        self._check("health_all_passed",      lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",     lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",     lambda: run_health_check().failed == 0)
        self._check("health_total_ge_60",     lambda: run_health_check().total >= 60)

        # ── Version Identity (11) ────────────────────────────────────────────
        from paper_trading.small_capital_strategy.simulation_matrix_version_v181 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
            MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
            get_version_info, is_known_release, verify_version,
        )
        self._check("gate_version_1_8_1",         lambda: VERSION == "1.8.1")
        self._check("gate_release_name",           lambda: RELEASE_NAME == "Simulation Scenario Matrix & Stress Test Lab")
        self._check("gate_base_release",           lambda: BASE_RELEASE == "1.8.0 Paper Simulation & Performance Lab")
        self._check("gate_schema_version_181",     lambda: SCHEMA_VERSION == "181")
        self._check("gate_policy_version",         lambda: POLICY_VERSION == "1.8.1-simulation-scenario-matrix-stress-test")
        self._check("gate_min_scenarios_75",       lambda: MIN_SCENARIOS >= 75)
        self._check("gate_min_fixtures_75",        lambda: MIN_FIXTURES >= 75)
        self._check("gate_min_cli_20",             lambda: MIN_CLI >= 20)
        self._check("gate_min_health_55",          lambda: MIN_HEALTH >= 55)
        self._check("gate_verify_version",         verify_version)
        self._check("gate_known_release_v181",     lambda: is_known_release("Simulation Scenario Matrix & Stress Test Lab"))

        # ── Safety (9) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.simulation_matrix_safety_v181 import (
            run_safety_audit, SAFETY_FLAGS, assert_safe,
        )
        self._check("gate_safety_audit_all_safe",      lambda: run_safety_audit()["all_safe"])
        self._check("gate_safety_paper_only",          lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("gate_safety_research_only",       lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("gate_safety_simulate_only",       lambda: SAFETY_FLAGS["simulate_only"] is True)
        self._check("gate_safety_stress_test_only",    lambda: SAFETY_FLAGS["stress_test_only"] is True)
        self._check("gate_safety_no_real_orders",      lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("gate_safety_no_broker",           lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("gate_safety_real_order_false",    lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("gate_safety_assert_no_raise",     lambda: (assert_safe(), True)[1])

        # ── Models (5) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import (
            SimulationMatrixInput, ScenarioMatrixDashboard,
            RobustnessScore, ScenarioMatrixHealthSummary, get_all_model_names,
        )
        self._check("gate_model_count_16",            lambda: len(get_all_model_names()) == 16)
        self._check("gate_model_input_paper_only",    lambda: SimulationMatrixInput().paper_only is True)
        self._check("gate_model_dashboard_version",   lambda: ScenarioMatrixDashboard().version == "1.8.1")
        self._check("gate_model_health_summary",      lambda: ScenarioMatrixHealthSummary().status == "PASS")
        self._check("gate_model_robustness_score",    lambda: RobustnessScore().final_grade == "FRAGILE")

        # ── Matrix Engine (5) ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.simulation_matrix_engine_v181 import (
            ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
            run_matrix_cell, validate_action,
        )
        self._check("gate_engine_allowed_ge_13",      lambda: len(ALLOWED_OUTPUT_ACTIONS) >= 13)
        self._check("gate_engine_no_buy_allowed",     lambda: "BUY" not in ALLOWED_OUTPUT_ACTIONS)
        self._check("gate_engine_stress_test_only",   lambda: "STRESS_TEST_ONLY" in ALLOWED_OUTPUT_ACTIONS)
        self._check("gate_engine_valid_grades_5",     lambda: len(VALID_FINAL_GRADES) == 5)
        self._check("gate_engine_validate_ok",        lambda: validate_action("PAPER_ENTRY_ALLOWED"))

        # ── Stress Engine (5) ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.simulation_stress_engine_v181 import (
            STRESS_TEST_TYPES, run_stress_test, run_all_stress_tests,
        )
        self._check("gate_stress_types_ge_10",        lambda: len(STRESS_TEST_TYPES) >= 10)
        self._check("gate_stress_market_crash",       lambda: run_stress_test("MARKET_CRASH").paper_only is True)
        self._check("gate_stress_no_stop_loss",       lambda: not run_stress_test("NO_STOP_LOSS_INJECTION").survived)
        self._check("gate_stress_all_tests",          lambda: len(run_all_stress_tests()) >= 10)
        self._check("gate_stress_test_only_flag",     lambda: run_stress_test("MARKET_CRASH").stress_test_only is True)

        # ── Scenarios (4) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.simulation_matrix_scenarios_v181 import (
            get_scenario_count, get_all_scenarios, get_scenario_categories,
        )
        self._check("gate_scenarios_ge_75",           lambda: get_scenario_count() >= 75)
        self._check("gate_scenarios_all_have_id",     lambda: all("id" in s for s in get_all_scenarios()))
        self._check("gate_scenarios_safety_flags",    lambda: all(s.get("paper_only") is True for s in get_all_scenarios()))
        self._check("gate_scenarios_categories_ge_5", lambda: len(get_scenario_categories()) >= 5)

        # ── Report (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.simulation_matrix_report_v181 import (
            REPORT_SECTIONS, get_report_info,
        )
        self._check("gate_report_sections_ge_10",     lambda: len(REPORT_SECTIONS) >= 10)
        self._check("gate_report_has_matrix_summary", lambda: "matrix_summary" in REPORT_SECTIONS)
        self._check("gate_report_info_dict",          lambda: isinstance(get_report_info(), dict))

        # ── CLI registration (4) ────────────────────────────────────────────
        from cli.command_registry import get_formal_command_names
        formal = get_formal_command_names()
        self._check("gate_cli_sim_matrix_version",    lambda: "simulation-matrix-version" in formal)
        self._check("gate_cli_sim_matrix_run",        lambda: "simulation-matrix-run" in formal)
        self._check("gate_cli_sim_stress_test",       lambda: "simulation-stress-test" in formal)
        self._check("gate_cli_sim_matrix_health",     lambda: "simulation-matrix-health" in formal)

        # ── GUI tabs (3) ─────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import _TABS
        self._check("gate_gui_sim_matrix_tab",        lambda: "sim_matrix_lab" in _TABS)
        self._check("gate_gui_stress_test_tab",       lambda: "sim_stress_test" in _TABS)
        self._check("gate_gui_robustness_score_tab",  lambda: "sim_robustness_score" in _TABS)

        # ── Backward compat (3) ──────────────────────────────────────────────
        self._check("gate_compat_v180_version",       lambda: (
            __import__("paper_trading.small_capital_strategy.paper_simulation_version_v180",
                       fromlist=["VERSION"]).VERSION == "1.8.0"
        ))
        self._check("gate_compat_v179_version",       lambda: (
            __import__("paper_trading.small_capital_strategy.stable_rollup_version_v179",
                       fromlist=["VERSION"]).VERSION == "1.7.9"
        ))
        self._check("gate_compat_v170_importable",    lambda: (
            __import__("paper_trading.small_capital_strategy.version_v170",
                       fromlist=["VERSION"]) is not None
        ))

        total = len(self._checks)
        passed_count = sum(1 for c in self._checks if c["passed"])
        failed_count = total - passed_count
        gate_passed = failed_count == 0

        return {
            "gate_version": GATE_VERSION,
            "total": total,
            "passed": passed_count,
            "failed": failed_count,
            "gate_passed": gate_passed,
            "checks": self._checks,
            "paper_only": True,
            "research_only": True,
            "simulate_only": True,
            "stress_test_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
            "production_trading_blocked": True,
        }


def run_release_gate() -> Dict[str, Any]:
    """Run the release gate and return result dict."""
    return SimulationMatrixReleaseGate().run()


if __name__ == "__main__":
    result = run_release_gate()
    print(f"[v1.8.1 Simulation Matrix Release Gate]")
    print(f"  Gate Passed: {result['gate_passed']}")
    print(f"  Checks:      {result['passed']} / {result['total']} passed")
    print(f"  Failed:      {result['failed']}")
    if result["failed"] > 0:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
    assert result["gate_passed"], f"Release gate FAILED: {result['failed']} failures"
    print("[OK] simulation_scenario_matrix_release_gate_v181 PASS")
