"""
paper_trading/small_capital_strategy/strategy_governance_dashboard_health_v197.py
Health check for Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only. Quality Analytics Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List

MIN_CHECKS = 60


class StrategyGovernanceDashboardHealthCheck:
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
        self._checks = []

        # ── version (7) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_version_v197 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_decision_quality_metrics, get_decision_quality_grades,
            get_analytics_windows, get_dashboard_panels, get_hard_block_conditions,
            get_forbidden_dashboard_actions, get_allowed_dashboard_actions,
        )
        self._check("version_is_197", lambda: VERSION == "1.9.7")
        self._check("release_name_correct",
                    lambda: RELEASE_NAME == "Paper Strategy Governance Dashboard & Decision Quality Analytics Lab")
        self._check("schema_version_197", lambda: SCHEMA_VERSION == "197")
        self._check("verify_version_returns_true", lambda: verify_version() is True)
        self._check("is_known_release_v197",
                    lambda: is_known_release("Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7"))
        self._check("version_info_paper_only", lambda: get_version_info()["paper_only"] is True)
        self._check("version_info_governance_analytics_only",
                    lambda: get_version_info()["governance_analytics_only"] is True)

        # ── quality metrics (3) ───────────────────────────────────────────────
        self._check("quality_metrics_count_12", lambda: len(get_decision_quality_metrics()) == 12)
        self._check("quality_metrics_has_evidence_coverage",
                    lambda: "evidence_coverage_score" in get_decision_quality_metrics())
        self._check("quality_metrics_has_registry_integrity",
                    lambda: "registry_integrity_score" in get_decision_quality_metrics())

        # ── quality grades (3) ────────────────────────────────────────────────
        self._check("quality_grades_count_5", lambda: len(get_decision_quality_grades()) == 5)
        self._check("quality_grades_has_excellent",
                    lambda: "EXCELLENT" in get_decision_quality_grades())
        self._check("quality_grades_has_invalid",
                    lambda: "INVALID" in get_decision_quality_grades())

        # ── analytics windows (3) ────────────────────────────────────────────
        self._check("analytics_windows_count_5", lambda: len(get_analytics_windows()) == 5)
        self._check("analytics_windows_has_daily",
                    lambda: "DAILY" in get_analytics_windows())
        self._check("analytics_windows_has_full_history",
                    lambda: "FULL_HISTORY" in get_analytics_windows())

        # ── dashboard panels (3) ─────────────────────────────────────────────
        self._check("dashboard_panels_count_12", lambda: len(get_dashboard_panels()) == 12)
        self._check("dashboard_panels_has_quality_overview",
                    lambda: "quality_overview" in get_dashboard_panels())
        self._check("dashboard_panels_has_export_manifest",
                    lambda: "export_manifest" in get_dashboard_panels())

        # ── hard block conditions (3) ─────────────────────────────────────────
        self._check("hard_block_conditions_count_17",
                    lambda: len(get_hard_block_conditions()) == 17)
        self._check("hard_block_has_real_order_requested",
                    lambda: "real_order_requested" in get_hard_block_conditions())
        self._check("hard_block_has_analytics_execute_decision",
                    lambda: "analytics_tries_to_execute_decision" in get_hard_block_conditions())

        # ── forbidden / allowed actions (4) ──────────────────────────────────
        self._check("forbidden_dashboard_actions_count_9",
                    lambda: len(get_forbidden_dashboard_actions()) == 9)
        self._check("allowed_dashboard_actions_count_18",
                    lambda: len(get_allowed_dashboard_actions()) == 18)
        self._check("forbidden_has_broker_order",
                    lambda: "BROKER_ORDER" in get_forbidden_dashboard_actions())
        self._check("allowed_has_governance_dashboard_health",
                    lambda: "GOVERNANCE_DASHBOARD_HEALTH" in get_allowed_dashboard_actions())

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_safety_v197 import (
            SAFETY_FLAGS, run_safety_audit, assert_safe,
            is_forbidden_action, is_allowed_action, validate_dashboard_action,
            FORBIDDEN_DASHBOARD_ACTIONS, ALLOWED_DASHBOARD_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_flag_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_flag_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_flag_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_flag_governance_analytics_only",
                    lambda: SAFETY_FLAGS["governance_analytics_only"] is True)
        self._check("safety_flag_dashboard_only",
                    lambda: SAFETY_FLAGS["dashboard_only"] is True)
        self._check("safety_flag_no_production_mutation",
                    lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._check("safety_flag_no_automatic_rollback",
                    lambda: SAFETY_FLAGS["no_automatic_rollback"] is True)
        self._check("safety_flag_analytics_does_not_execute",
                    lambda: SAFETY_FLAGS["analytics_executes_decision"] is False)
        self._check("safety_assert_no_raise", lambda: (assert_safe(), True)[1])

        # ── models (8) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_models_v197 import (
            StrategyGovernanceDashboardInput, StrategyGovernanceDashboardResult,
            StrategyDecisionQualityScore, StrategyDecisionQualityMetric,
            StrategyDecisionQualitySummary, StrategyDecisionQualityGrade,
            StrategyDecisionAnalyticsWindow, StrategyDecisionOutcomeSummary,
            StrategyDecisionOutcomeBucket, StrategyEvidenceCoverageSummary,
            StrategyEvidenceGap, StrategyGovernanceViolationSummary,
            StrategyGovernanceViolationPattern, StrategyRollbackReviewFrequency,
            StrategyApprovalQualitySummary, StrategyRejectionQualitySummary,
            StrategyMonitoringDecisionQualitySummary, StrategyDecisionConsistencySummary,
            StrategyDecisionTrend, StrategyDecisionDashboardPanel,
            StrategyDecisionDashboardExport, StrategyDecisionQualityReport,
            StrategyDecisionQualityAuditTrail, StrategyDecisionQualityHealthSummary,
            StrategyDecisionQualityValidationResult, get_all_model_names,
        )
        self._check("model_dashboard_input_paper_only",
                    lambda: StrategyGovernanceDashboardInput().paper_only is True)
        self._check("model_dashboard_result_paper_only",
                    lambda: StrategyGovernanceDashboardResult().paper_only is True)
        self._check("model_quality_score_schema_197",
                    lambda: StrategyDecisionQualityScore().schema_version == "197")
        self._check("model_quality_grade_default_invalid",
                    lambda: StrategyDecisionQualityGrade().grade == "INVALID")
        self._check("model_approval_summary_no_auto_approval",
                    lambda: StrategyApprovalQualitySummary().auto_approval is False)
        self._check("model_rollback_freq_no_auto_rollback",
                    lambda: StrategyRollbackReviewFrequency().auto_rollback is False)
        self._check("model_audit_trail_immutable",
                    lambda: StrategyDecisionQualityAuditTrail().immutable is True)
        self._check("model_count_25", lambda: len(get_all_model_names()) == 25)

        # ── engine (6) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_engine_v197 import (
            validate_dashboard_action, validate_analytics_window,
            build_dashboard_input, build_quality_score, build_quality_grade,
            build_evidence_coverage_summary, build_outcome_summary,
            build_dashboard_panel, build_dashboard_export, get_engine_info,
        )
        self._check("engine_info_paper_only",
                    lambda: get_engine_info()["paper_only"] is True)
        self._check("engine_validate_action_buy_blocked",
                    lambda: validate_dashboard_action("BUY")["blocked"] is True)
        self._check("engine_validate_action_health_valid",
                    lambda: validate_dashboard_action("GOVERNANCE_DASHBOARD_HEALTH")["valid"] is True)
        self._check("engine_build_input_missing_source_blocked",
                    lambda: build_dashboard_input("")["blocked"] is True)
        self._check("engine_build_quality_score_missing_id_blocked",
                    lambda: build_quality_score("")["blocked"] is True)
        self._check("engine_build_dashboard_panel_unknown_blocked",
                    lambda: build_dashboard_panel("UNKNOWN_PANEL")["blocked"] is True)

        # ── report (4) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_report_v197 import (
            export_quality_overview_report, export_full_dashboard_pack,
            get_report_section_names, export_scorecard_report,
        )
        self._check("report_sections_count_ge_12",
                    lambda: len(get_report_section_names()) >= 12)
        self._check("report_export_overview_blocked_missing_source",
                    lambda: export_quality_overview_report("")["blocked"] is True)
        self._check("report_full_pack_paper_only",
                    lambda: export_full_dashboard_pack("REG-001")["paper_only"] is True)
        self._check("report_full_pack_analytics_not_execute",
                    lambda: export_full_dashboard_pack("REG-001")["analytics_executes_decision"] is False)

        # ── scenarios (3) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_scenarios_v197 import (
            get_all_scenarios, get_scenario_count, get_scenario_by_id,
        )
        self._check("scenarios_count_75", lambda: get_scenario_count() == 75)
        self._check("scenarios_all_paper_only",
                    lambda: all(s["paper_only"] for s in get_all_scenarios()))
        self._check("scenario_by_id_found",
                    lambda: get_scenario_by_id("SP197-001").get("scenario_id") == "SP197-001")

        # ── fixtures (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_fixtures_v197 import (
            get_all_fixtures, get_fixture_count, get_fixture_by_id,
        )
        self._check("fixtures_count_75", lambda: get_fixture_count() == 75)
        self._check("fixtures_all_paper_only",
                    lambda: all(f["paper_only"] for f in get_all_fixtures()))
        self._check("fixture_by_id_found",
                    lambda: get_fixture_by_id("SMF197-001") is not None)

        # ── CLI (2) ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_governance_dashboard_version_v197 import MIN_CLI
        self._check("min_cli_16", lambda: MIN_CLI >= 16)
        self._check("allowed_actions_covers_cli",
                    lambda: len(get_allowed_dashboard_actions()) >= MIN_CLI)

        # ── backward compat (4) ──────────────────────────────────────────────
        self._check("backward_compat_v196",
                    lambda: is_known_release("Paper Strategy Decision Registry & Governance Lab v1.9.6"))
        self._check("backward_compat_v195",
                    lambda: is_known_release("Paper Strategy Review Alert & Human Approval Lab v1.9.5"))
        self._check("backward_compat_v194",
                    lambda: is_known_release("Paper Strategy Monitoring & Drift Detection Lab v1.9.4"))
        self._check("backward_compat_v190",
                    lambda: is_known_release("Paper Trading Performance Review & Strategy Improvement Lab v1.9.0"))

        # ── forbidden action words (3) ────────────────────────────────────────
        self._check("forbidden_buy_blocked",
                    lambda: is_forbidden_action("BUY") is True)
        self._check("forbidden_sell_blocked",
                    lambda: is_forbidden_action("SELL") is True)
        self._check("forbidden_broker_order_blocked",
                    lambda: is_forbidden_action("BROKER_ORDER") is True)

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)
        return {
            "all_passed": failed == 0,
            "status": "PASS" if failed == 0 else "FAIL",
            "passed": passed,
            "failed": failed,
            "total": total,
            "checks": list(self._checks),
            "paper_only": True,
            "governance_analytics_only": True,
            "dashboard_only": True,
            "no_real_orders": True,
            "schema_version": "197",
        }


def run_health_check() -> Dict[str, Any]:
    return StrategyGovernanceDashboardHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Strategy Governance Dashboard Health v1.9.7: {'PASS' if result['all_passed'] else 'FAIL'}  "
          f"{result['passed']}/{result['total']}")
    if not result["all_passed"]:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
