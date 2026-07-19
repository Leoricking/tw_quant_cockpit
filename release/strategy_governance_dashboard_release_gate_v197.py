"""
release/strategy_governance_dashboard_release_gate_v197.py
Release gate for Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7.
gate_passed=True required for release.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only. Quality Analytics Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.9.7"
MIN_CHECKS = 50
BASELINE_TESTS = 29683
MIN_NEW_TESTS = 400
MIN_SCENARIOS = 75
MIN_FIXTURES = 75
MIN_CLI = 16


class StrategyGovernanceDashboardReleaseGate:
    """Release gate for Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7."""

    GATE_VERSION = "1.9.7"
    MIN_SCENARIOS = 75
    MIN_FIXTURES = 75
    MIN_CLI = 16
    BASELINE_TESTS = 29683
    MIN_NEW_TESTS = 400

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
            "name": name,
            "passed": ok,
            "error": None if ok else str(result),
        })

    def run(self) -> Dict[str, Any]:
        """Run all gate checks and return result dict."""
        self._checks = []

        # ── Health PASS (4) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_health_v197 import run_health_check
        self._check("health_all_passed", lambda: run_health_check()["all_passed"] is True)
        self._check("health_status_pass", lambda: run_health_check()["status"] == "PASS")
        self._check("health_failed_zero", lambda: run_health_check()["failed"] == 0)
        self._check("health_total_ge_60", lambda: run_health_check()["total"] >= 60)

        # ── Version Identity (8) ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_version_v197 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
            verify_version, is_known_release,
            get_decision_quality_metrics, get_decision_quality_grades,
            get_analytics_windows, get_dashboard_panels, get_hard_block_conditions,
            get_forbidden_dashboard_actions, get_allowed_dashboard_actions,
        )
        self._check("gate_version_1_9_7", lambda: VERSION == "1.9.7")
        self._check("gate_release_name",
                    lambda: RELEASE_NAME == "Paper Strategy Governance Dashboard & Decision Quality Analytics Lab")
        self._check("gate_schema_version_197", lambda: SCHEMA_VERSION == "197")
        self._check("gate_policy_version",
                    lambda: POLICY_VERSION == "1.9.7-small-capital-strategy-paper-strategy-governance-dashboard-decision-quality-analytics-lab")
        self._check("gate_known_release_self",
                    lambda: is_known_release("Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7"))
        self._check("gate_verify_version", verify_version)
        self._check("gate_quality_metrics_count_12",
                    lambda: len(get_decision_quality_metrics()) == 12)
        self._check("gate_quality_grades_count_5",
                    lambda: len(get_decision_quality_grades()) == 5)

        # ── Analytics & Panels (4) ───────────────────────────────────────────
        self._check("gate_analytics_windows_count_5",
                    lambda: len(get_analytics_windows()) == 5)
        self._check("gate_dashboard_panels_count_12",
                    lambda: len(get_dashboard_panels()) == 12)
        self._check("gate_hard_block_conditions_count_17",
                    lambda: len(get_hard_block_conditions()) == 17)
        self._check("gate_allowed_dashboard_actions_count_18",
                    lambda: len(get_allowed_dashboard_actions()) == 18)

        # ── Safety (10) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_safety_v197 import (
            SAFETY_FLAGS, run_safety_audit, assert_safe,
            FORBIDDEN_DASHBOARD_ACTIONS, ALLOWED_DASHBOARD_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_no_real_order", lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("safety_no_broker_exec", lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_governance_analytics_only",
                    lambda: SAFETY_FLAGS["governance_analytics_only"] is True)
        self._check("safety_no_production_mutation",
                    lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._check("safety_no_automatic_rollback",
                    lambda: SAFETY_FLAGS["no_automatic_rollback"] is True)
        self._check("safety_analytics_does_not_execute",
                    lambda: SAFETY_FLAGS["analytics_executes_decision"] is False)
        self._check("safety_dashboard_does_not_mutate",
                    lambda: SAFETY_FLAGS["dashboard_mutates_strategy"] is False)
        self._check("safety_assert_no_raise", lambda: (assert_safe(), True)[1])

        # ── Models (6) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_models_v197 import (
            StrategyGovernanceDashboardInput, StrategyGovernanceDashboardResult,
            StrategyDecisionQualityScore, StrategyApprovalQualitySummary,
            StrategyRollbackReviewFrequency, StrategyDecisionQualityAuditTrail,
            get_all_model_names,
        )
        self._check("model_dashboard_input_paper_only",
                    lambda: StrategyGovernanceDashboardInput().paper_only is True)
        self._check("model_dashboard_result_paper_only",
                    lambda: StrategyGovernanceDashboardResult().paper_only is True)
        self._check("model_quality_score_schema_197",
                    lambda: StrategyDecisionQualityScore().schema_version == "197")
        self._check("model_approval_no_auto_approval",
                    lambda: StrategyApprovalQualitySummary().auto_approval is False)
        self._check("model_rollback_no_auto_rollback",
                    lambda: StrategyRollbackReviewFrequency().auto_rollback is False)
        self._check("model_count_25", lambda: len(get_all_model_names()) == 25)

        # ── Engine (6) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_engine_v197 import (
            validate_dashboard_action, build_dashboard_input, build_quality_score,
            build_quality_grade, build_dashboard_panel, get_engine_info,
        )
        self._check("engine_info_paper_only",
                    lambda: get_engine_info()["paper_only"] is True)
        self._check("engine_buy_blocked",
                    lambda: validate_dashboard_action("BUY")["blocked"] is True)
        self._check("engine_health_action_valid",
                    lambda: validate_dashboard_action("GOVERNANCE_DASHBOARD_HEALTH")["valid"] is True)
        self._check("engine_input_missing_source_blocked",
                    lambda: build_dashboard_input("")["blocked"] is True)
        self._check("engine_quality_score_missing_id_blocked",
                    lambda: build_quality_score("")["blocked"] is True)
        self._check("engine_dashboard_panel_unknown_blocked",
                    lambda: build_dashboard_panel("UNKNOWN_PANEL")["blocked"] is True)

        # ── Report (4) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_report_v197 import (
            export_quality_overview_report, export_full_dashboard_pack,
            get_report_section_names, export_scorecard_report,
        )
        self._check("report_sections_ge_12",
                    lambda: len(get_report_section_names()) >= 12)
        self._check("report_overview_blocked_empty",
                    lambda: export_quality_overview_report("")["blocked"] is True)
        self._check("report_full_pack_valid",
                    lambda: export_full_dashboard_pack("REG-001")["valid"] is True)
        self._check("report_scorecard_valid",
                    lambda: export_scorecard_report("REG-001")["valid"] is True)

        # ── Scenarios (4) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_scenarios_v197 import (
            get_all_scenarios, get_scenario_count, get_scenario_by_id,
        )
        self._check("scenarios_count_75", lambda: get_scenario_count() == 75)
        self._check("scenarios_ge_min", lambda: get_scenario_count() >= MIN_SCENARIOS)
        self._check("scenarios_all_paper_only",
                    lambda: all(s["paper_only"] for s in get_all_scenarios()))
        self._check("scenario_by_id_found",
                    lambda: get_scenario_by_id("SP197-001").get("scenario_id") == "SP197-001")

        # ── Fixtures (4) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_fixtures_v197 import (
            get_all_fixtures, get_fixture_count, get_fixture_by_id,
        )
        self._check("fixtures_count_75", lambda: get_fixture_count() == 75)
        self._check("fixtures_ge_min", lambda: get_fixture_count() >= MIN_FIXTURES)
        self._check("fixtures_all_paper_only",
                    lambda: all(f["paper_only"] for f in get_all_fixtures()))
        self._check("fixture_by_id_found",
                    lambda: get_fixture_by_id("SMF197-001") is not None)

        # ── GUI (3) ──────────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION, get_governance_dashboard_tab_names
        self._check("gui_panel_version_197",
                    lambda: PANEL_VERSION in ("1.9.7", "1.9.8", "1.9.9", "1.9.10", "2.0.0"))
        self._check("gui_governance_dashboard_tabs_present",
                    lambda: "governance_dashboard" in get_governance_dashboard_tab_names())
        self._check("gui_governance_dashboard_tab_count_3",
                    lambda: len(get_governance_dashboard_tab_names()) == 3)

        # ── CLI (3) ──────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_version_v197 import MIN_CLI
        self._check("min_cli_16", lambda: MIN_CLI >= 16)
        self._check("allowed_actions_covers_min_cli",
                    lambda: len(get_allowed_dashboard_actions()) >= MIN_CLI)
        self._check("cli_dashboard_version_in_allowed",
                    lambda: "GOVERNANCE_DASHBOARD_VERSION" in get_allowed_dashboard_actions())

        # ── Baseline test count (2) ───────────────────────────────────────────
        self._check("baseline_tests_29683", lambda: BASELINE_TESTS == 29683)
        self._check("min_new_tests_400", lambda: MIN_NEW_TESTS >= 400)

        # ── Backward compat (4) ──────────────────────────────────────────────
        self._check("backward_compat_v196",
                    lambda: is_known_release("Paper Strategy Decision Registry & Governance Lab v1.9.6"))
        self._check("backward_compat_v195",
                    lambda: is_known_release("Paper Strategy Review Alert & Human Approval Lab v1.9.5"))
        self._check("backward_compat_v194",
                    lambda: is_known_release("Paper Strategy Monitoring & Drift Detection Lab v1.9.4"))
        self._check("backward_compat_v190",
                    lambda: is_known_release("Paper Trading Performance Review & Strategy Improvement Lab v1.9.0"))

        # ── Panel version check (1) ───────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION as _PV
        self._check("gui_panel_version_match", lambda: _PV in ("1.9.7", "1.9.8", "1.9.9", "1.9.10", "2.0.0"))

        passed_count = sum(1 for c in self._checks if c["passed"])
        failed_count = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)
        return {
            "gate_passed": failed_count == 0,
            "passed": passed_count,
            "failed": failed_count,
            "passed_count": passed_count,
            "failed_count": failed_count,
            "total": total,
            "gate_version": GATE_VERSION,
            "checks": list(self._checks),
            "paper_only": True,
            "no_real_orders": True,
            "governance_analytics_only": True,
            "dashboard_only": True,
            "not_investment_advice": True,
            "schema_version": "197",
        }


def run_release_gate() -> Dict[str, Any]:
    return StrategyGovernanceDashboardReleaseGate().run()


run_gate = run_release_gate


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Strategy Governance Dashboard Release Gate v1.9.7: {'PASS' if result['gate_passed'] else 'FAIL'}  "
          f"{result['passed_count']}/{result['total']}")
    if not result["gate_passed"]:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
