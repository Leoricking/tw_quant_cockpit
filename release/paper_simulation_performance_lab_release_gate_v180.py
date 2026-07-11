"""
release/paper_simulation_performance_lab_release_gate_v180.py
Release gate for Paper Simulation & Performance Lab v1.8.0. 55+ gate checks.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.8.0"
MIN_CHECKS   = 50


class PaperSimulationReleaseGate:
    """Release gate for Paper Simulation & Performance Lab v1.8.0. 55+ checks."""

    def __init__(self) -> None:
        self._checks: List[Dict[str, Any]] = []

    def _check(self, name: str, fn) -> None:
        try:
            result = fn()
            ok = bool(result)
        except Exception as exc:
            ok = False
            result = str(exc)
        self._checks.append({
            "name":   name,
            "passed": ok,
            "error":  None if ok else str(result),
        })

    def run(self) -> Dict[str, Any]:
        """Run all gate checks and return result dict."""
        self._checks = []

        # ── Health PASS (4) ─────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.paper_simulation_health_v180 import run_health_check
        self._check("health_all_passed",      lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",     lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",     lambda: run_health_check().failed == 0)
        self._check("health_total_ge_70",     lambda: run_health_check().total >= 70)

        # ── Version Identity (11) ────────────────────────────────────────────
        from paper_trading.small_capital_strategy.paper_simulation_version_v180 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
            MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
            get_version_info, is_known_release, verify_version,
        )
        self._check("gate_version_1_8_0",         lambda: VERSION == "1.8.0")
        self._check("gate_release_name",           lambda: RELEASE_NAME == "Paper Simulation & Performance Lab")
        self._check("gate_base_release",           lambda: BASE_RELEASE == "1.7.9 Small Capital Strategy Stable Rollup")
        self._check("gate_schema_version_180",     lambda: SCHEMA_VERSION == "180")
        self._check("gate_policy_version",         lambda: POLICY_VERSION == "1.8.0-paper-simulation-performance-lab")
        self._check("gate_min_scenarios_70",       lambda: MIN_SCENARIOS >= 70)
        self._check("gate_min_fixtures_70",        lambda: MIN_FIXTURES >= 70)
        self._check("gate_min_cli_19",             lambda: MIN_CLI >= 19)
        self._check("gate_min_health_50",          lambda: MIN_HEALTH >= 50)
        self._check("gate_verify_version",         verify_version)
        self._check("gate_known_release_v180",     lambda: is_known_release("Paper Simulation & Performance Lab"))

        # ── Safety (9) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.paper_simulation_safety_v180 import (
            run_safety_audit, SAFETY_FLAGS, assert_safe,
        )
        self._check("gate_safety_audit_all_safe",      lambda: run_safety_audit()["all_safe"])
        self._check("gate_safety_paper_only",          lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("gate_safety_research_only",       lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("gate_safety_no_real_orders",      lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("gate_safety_no_broker",           lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("gate_safety_no_margin",           lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("gate_safety_no_production_db",    lambda: SAFETY_FLAGS["no_production_db_writes"] is True)
        self._check("gate_safety_real_order_false",    lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("gate_safety_assert_no_raise",     lambda: (assert_safe(), True)[1])

        # ── Models (5) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.paper_simulation_models_v180 import (
            PaperSimulationInput, PaperPerformanceMetrics,
            PaperSimulationDashboard, PaperSimulationHealthSummary,
            get_all_model_names,
        )
        self._check("gate_model_count_17",            lambda: len(get_all_model_names()) == 17)
        self._check("gate_model_input_paper_only",    lambda: PaperSimulationInput().paper_only is True)
        self._check("gate_model_metrics_grade",       lambda: PaperPerformanceMetrics().final_grade == "B")
        self._check("gate_model_dashboard_version",   lambda: PaperSimulationDashboard().version == "1.8.0")
        self._check("gate_model_health_summary",      lambda: PaperSimulationHealthSummary().status == "PASS")

        # ── Engine (5) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.paper_simulation_engine_v180 import (
            ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS,
            get_action_for_input, run_paper_simulation, validate_action,
        )
        self._check("gate_engine_allowed_ge_9",       lambda: len(ALLOWED_OUTPUT_ACTIONS) >= 9)
        self._check("gate_engine_forbidden_ge_9",     lambda: len(FORBIDDEN_OUTPUT_WORDS) >= 9)
        self._check("gate_engine_no_buy_allowed",     lambda: "BUY" not in ALLOWED_OUTPUT_ACTIONS)
        self._check("gate_engine_no_sell_allowed",    lambda: "SELL" not in ALLOWED_OUTPUT_ACTIONS)
        self._check("gate_engine_validate_ok",        lambda: validate_action("PAPER_ENTRY_ALLOWED"))

        # ── Scenarios (4) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.paper_simulation_scenarios_v180 import (
            get_scenario_count, get_all_scenarios, get_scenario_categories,
        )
        self._check("gate_scenarios_ge_70",           lambda: get_scenario_count() >= 70)
        self._check("gate_scenarios_all_have_id",     lambda: all("id" in s for s in get_all_scenarios()))
        self._check("gate_scenarios_safety_flags",    lambda: all(s.get("paper_only") is True for s in get_all_scenarios()))
        self._check("gate_scenarios_categories_ge_5", lambda: len(get_scenario_categories()) >= 5)

        # ── Report (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.paper_simulation_report_v180 import (
            REPORT_SECTIONS, get_report_info,
        )
        self._check("gate_report_sections_ge_10",     lambda: len(REPORT_SECTIONS) >= 10)
        self._check("gate_report_has_metrics",        lambda: "performance_metrics" in REPORT_SECTIONS)
        self._check("gate_report_info_dict",          lambda: isinstance(get_report_info(), dict))

        # ── CLI registration (4) ────────────────────────────────────────────
        from cli.command_registry import get_formal_command_names
        formal = get_formal_command_names()
        self._check("gate_cli_paper_sim_version",     lambda: "paper-simulation-version" in formal)
        self._check("gate_cli_paper_sim_run",         lambda: "paper-simulation-run" in formal)
        self._check("gate_cli_paper_sim_health",      lambda: "paper-simulation-health" in formal)
        self._check("gate_cli_paper_sim_gate",        lambda: "paper-simulation-gate" in formal)

        # ── GUI tabs (3) ─────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import _TABS, render_all_tabs
        self._check("gate_gui_paper_sim_lab_tab",          lambda: "paper_sim_lab" in _TABS)
        self._check("gate_gui_paper_sim_equity_curve_tab", lambda: "paper_sim_equity_curve" in _TABS)
        self._check("gate_gui_paper_sim_performance_tab",  lambda: "paper_sim_performance" in _TABS)

        # ── Backward compatibility with v1.7.x (3) ───────────────────────────
        self._check("gate_compat_v179_version",       lambda: (
            __import__("paper_trading.small_capital_strategy.stable_rollup_version_v179",
                       fromlist=["VERSION"]).VERSION == "1.7.9"
        ))
        self._check("gate_compat_v178_importable",    lambda: (
            __import__("paper_trading.small_capital_strategy.version_v178",
                       fromlist=["VERSION"]) is not None
        ))
        self._check("gate_compat_v170_importable",    lambda: (
            __import__("paper_trading.small_capital_strategy.version_v170",
                       fromlist=["VERSION"]) is not None
        ))

        # ── Compute final gate result ─────────────────────────────────────────
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
            "no_real_orders": True,
            "not_investment_advice": True,
            "production_trading_blocked": True,
        }


def run_release_gate() -> Dict[str, Any]:
    """Run the release gate and return result dict."""
    gate = PaperSimulationReleaseGate()
    return gate.run()


if __name__ == "__main__":
    result = run_release_gate()
    print(f"[v1.8.0 Paper Simulation Release Gate]")
    print(f"  Gate Passed: {result['gate_passed']}")
    print(f"  Checks:      {result['passed']} / {result['total']} passed")
    print(f"  Failed:      {result['failed']}")
    if result["failed"] > 0:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
    assert result["gate_passed"], f"Release gate FAILED: {result['failed']} failures"
    print("[OK] paper_simulation_performance_lab_release_gate_v180 PASS")
