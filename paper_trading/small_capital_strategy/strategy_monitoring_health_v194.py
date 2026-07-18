"""
paper_trading/small_capital_strategy/strategy_monitoring_health_v194.py
Health check for Paper Strategy Monitoring & Drift Detection Lab v1.9.4.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List


class StrategyMonitoringHealthCheck:
    def __init__(self) -> None:
        self._checks: List[Dict[str, Any]] = []

    def _check(self, name: str, fn) -> None:
        try:
            result = fn()
            ok = bool(result)
        except Exception as exc:
            ok = False
            result = str(exc)
        self._checks.append({"name": name, "passed": ok, "error": None if ok else str(result)})

    def run(self) -> "MonitoringHealthSummary":
        from paper_trading.small_capital_strategy.strategy_monitoring_models_v194 import MonitoringHealthSummary
        self._checks = []

        # ── version (6) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_version_v194 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_drift_categories, get_drift_severities,
            get_monitoring_statuses, get_monitoring_recommendations,
            get_forbidden_monitoring_actions, get_allowed_monitoring_actions,
            get_hard_block_conditions,
        )
        self._check("version_is_194", lambda: VERSION == "1.9.4")
        self._check("release_name_correct",
                    lambda: RELEASE_NAME == "Paper Strategy Monitoring & Drift Detection Lab")
        self._check("schema_version_194", lambda: SCHEMA_VERSION == "194")
        self._check("verify_version_returns_true", lambda: verify_version() is True)
        self._check("is_known_release_v194",
                    lambda: is_known_release("Paper Strategy Monitoring & Drift Detection Lab v1.9.4"))
        self._check("version_info_paper_only", lambda: get_version_info()["paper_only"] is True)

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_safety_v194 import (
            SAFETY_FLAGS, run_safety_audit, is_safe_output_path, is_forbidden_action,
            is_allowed_action, validate_monitoring_action,
            FORBIDDEN_MONITORING_ACTIONS, ALLOWED_MONITORING_ACTIONS,
            HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_flag_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_flag_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_flag_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_flag_monitoring_only",
                    lambda: SAFETY_FLAGS["monitoring_only"] is True)
        self._check("safety_flag_drift_detection_only",
                    lambda: SAFETY_FLAGS["drift_detection_only"] is True)
        self._check("safety_flag_not_investment_advice",
                    lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._check("safety_flag_no_production_mutation",
                    lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._check("safety_flag_broker_execution_false",
                    lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_flag_live_strategy_activation_false",
                    lambda: SAFETY_FLAGS["live_strategy_activation"] is False)

        # ── drift categories (3) ──────────────────────────────────────────────
        self._check("drift_categories_count_17", lambda: len(get_drift_categories()) == 17)
        self._check("drift_categories_has_win_rate",
                    lambda: "WIN_RATE_DRIFT" in get_drift_categories())
        self._check("drift_categories_has_market_regime",
                    lambda: "MARKET_REGIME_MISMATCH_DRIFT" in get_drift_categories())

        # ── drift severities (2) ──────────────────────────────────────────────
        self._check("drift_severities_count_5", lambda: len(get_drift_severities()) == 5)
        self._check("drift_severities_has_critical",
                    lambda: "CRITICAL" in get_drift_severities())

        # ── monitoring statuses (2) ───────────────────────────────────────────
        self._check("monitoring_statuses_count_6",
                    lambda: len(get_monitoring_statuses()) == 6)
        self._check("monitoring_statuses_has_rollback_required",
                    lambda: "ROLLBACK_REQUIRED" in get_monitoring_statuses())

        # ── monitoring recommendations (2) ────────────────────────────────────
        self._check("recommendations_count_13",
                    lambda: len(get_monitoring_recommendations()) == 13)
        self._check("recommendations_has_continue_monitoring",
                    lambda: "CONTINUE_MONITORING" in get_monitoring_recommendations())

        # ── models (26) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_models_v194 import (
            StrategyMonitoringInput, StrategyMonitoringResult,
            MonitoringPackageSnapshot, MonitoringRuleSnapshot, MonitoringWindow,
            MonitoringMetricSnapshot, MonitoringBaselineSnapshot,
            MonitoringCurrentSnapshot, StrategyDriftSignal, DriftDetectionResult,
            DriftSeverity, DriftCategory, MonitoringRiskStatus,
            MonitoringPerformanceStatus, MonitoringSignalQualityStatus,
            MonitoringGuardrailStatus, MonitoringRollbackTrigger,
            MonitoringReviewAlert, MonitoringFinding, MonitoringRecommendation,
            MonitoringExportManifest, MonitoringEvidencePack, MonitoringAuditTrail,
            MonitoringDashboard, MonitoringHealthSummary as MHS,
            MonitoringValidationResult, get_all_model_names,
        )
        self._check("model_monitoring_input_paper_only",
                    lambda: StrategyMonitoringInput().paper_only is True)
        self._check("model_monitoring_result_no_real_orders",
                    lambda: StrategyMonitoringResult().no_real_orders is True)
        self._check("model_package_snapshot_monitoring_only",
                    lambda: MonitoringPackageSnapshot().monitoring_only is True)
        self._check("model_rule_snapshot_not_investment_advice",
                    lambda: MonitoringRuleSnapshot().not_investment_advice is True)
        self._check("model_monitoring_window_paper_only",
                    lambda: MonitoringWindow().paper_only is True)
        self._check("model_metric_snapshot_schema",
                    lambda: MonitoringMetricSnapshot().schema_version == "194")
        self._check("model_baseline_snapshot_no_real_orders",
                    lambda: MonitoringBaselineSnapshot().no_real_orders is True)
        self._check("model_current_snapshot_not_investment_advice",
                    lambda: MonitoringCurrentSnapshot().not_investment_advice is True)
        self._check("model_drift_signal_drift_detection_only",
                    lambda: StrategyDriftSignal().drift_detection_only is True)
        self._check("model_drift_result_no_real_orders",
                    lambda: DriftDetectionResult().no_real_orders is True)
        self._check("model_drift_severity_paper_only",
                    lambda: DriftSeverity().paper_only is True)
        self._check("model_drift_category_not_investment_advice",
                    lambda: DriftCategory().not_investment_advice is True)
        self._check("model_risk_status_monitoring_only",
                    lambda: MonitoringRiskStatus().monitoring_only is True)
        self._check("model_performance_status_paper_only",
                    lambda: MonitoringPerformanceStatus().paper_only is True)
        self._check("model_signal_quality_status_no_real_orders",
                    lambda: MonitoringSignalQualityStatus().no_real_orders is True)
        self._check("model_guardrail_status_not_investment_advice",
                    lambda: MonitoringGuardrailStatus().not_investment_advice is True)
        self._check("model_rollback_trigger_auto_rollback_false",
                    lambda: MonitoringRollbackTrigger().auto_rollback is False)
        self._check("model_review_alert_paper_only",
                    lambda: MonitoringReviewAlert().paper_only is True)
        self._check("model_finding_not_investment_advice",
                    lambda: MonitoringFinding().not_investment_advice is True)
        self._check("model_recommendation_production_trading_blocked",
                    lambda: MonitoringRecommendation().production_trading_blocked is True)
        self._check("model_export_manifest_report_only",
                    lambda: MonitoringExportManifest().report_only is True)
        self._check("model_evidence_pack_audit_only",
                    lambda: MonitoringEvidencePack().audit_only is True)
        self._check("model_audit_trail_audit_only",
                    lambda: MonitoringAuditTrail().audit_only is True)
        self._check("model_dashboard_no_real_orders",
                    lambda: MonitoringDashboard().no_real_orders is True)
        self._check("model_health_summary_schema",
                    lambda: MHS().schema_version == "194")
        self._check("model_validation_result_monitoring_only",
                    lambda: MonitoringValidationResult().monitoring_only is True)
        self._check("model_names_count_26",
                    lambda: len(get_all_model_names()) == 26)

        # ── engine (8) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_engine_v194 import (
            validate_monitoring_action as vma, run_drift_detection,
            build_monitoring_package_snapshot, build_rollback_alert,
            build_monitoring_recommendation, build_monitoring_evidence_pack,
            build_monitoring_audit_trail, build_monitoring_dashboard,
            build_monitoring_export_manifest, get_engine_info,
        )
        self._check("engine_validate_allowed_action",
                    lambda: vma("MONITOR")["valid"] is True)
        self._check("engine_validate_forbidden_action",
                    lambda: vma("BUY")["blocked"] is True)
        self._check("engine_drift_detection_missing_id_blocked",
                    lambda: run_drift_detection("", "base", "curr", "win")["blocked"] is True)
        self._check("engine_drift_detection_valid",
                    lambda: run_drift_detection("MON-H1", "BASE-H1", "CURR-H1", "WIN-H1")["valid"] is True)
        self._check("engine_package_snapshot_missing_id_blocked",
                    lambda: build_monitoring_package_snapshot("", "pkg", "roll")["blocked"] is True)
        self._check("engine_package_snapshot_valid",
                    lambda: build_monitoring_package_snapshot("PKG-H1", "pkg-src", "roll-src")["valid"] is True)
        self._check("engine_rollback_alert_missing_id_blocked",
                    lambda: build_rollback_alert("", "WIN_RATE")["blocked"] is True)
        self._check("engine_rollback_alert_auto_rollback_false",
                    lambda: build_rollback_alert("ALT-H1", "WIN_RATE")["auto_rollback"] is False)

        # ── report (5) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_report_v194 import (
            export_monitoring_summary, export_drift_report,
            export_rollback_trigger_report, export_full_monitoring_pack,
            get_report_section_names,
        )
        self._check("report_summary_missing_id_blocked",
                    lambda: export_monitoring_summary("")["blocked"] is True)
        self._check("report_summary_valid",
                    lambda: export_monitoring_summary("MON-H2")["valid"] is True)
        self._check("report_drift_valid",
                    lambda: export_drift_report("MON-H2")["valid"] is True)
        self._check("report_rollback_trigger_auto_rollback_false",
                    lambda: export_rollback_trigger_report("MON-H2")["auto_rollback"] is False)
        self._check("report_section_names_count",
                    lambda: len(get_report_section_names()) >= 10)

        # ── fixtures (4) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_fixtures_v194 import (
            get_all_fixtures, get_fixture_ids, get_blocked_fixtures, get_drift_fixtures,
        )
        self._check("fixtures_count_75", lambda: len(get_all_fixtures()) == 75)
        self._check("fixtures_all_have_schema_version",
                    lambda: all(f["schema_version"] == "194" for f in get_all_fixtures()))
        self._check("fixtures_all_have_paper_only",
                    lambda: all(f["paper_only"] is True for f in get_all_fixtures()))
        self._check("fixtures_blocked_exists",
                    lambda: len(get_blocked_fixtures()) > 0)

        # ── scenarios (4) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_scenarios_v194 import (
            get_all_scenarios, get_scenario_ids, get_blocked_scenarios, get_drift_scenarios,
        )
        self._check("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._check("scenarios_all_have_schema_version",
                    lambda: all(s["schema_version"] == "194" for s in get_all_scenarios()))
        self._check("scenarios_all_have_paper_only",
                    lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._check("scenarios_drift_exists",
                    lambda: len(get_drift_scenarios()) > 0)

        # ── backward compat (4) ───────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION, get_panel_info
        self._check("backward_compat_panel_version_194",
                    lambda: PANEL_VERSION in ("1.9.4", "1.9.5"))
        self._check("backward_compat_panel_info_paper_only",
                    lambda: get_panel_info()["paper_only"] is True)
        self._check("backward_compat_panel_info_no_real_orders",
                    lambda: get_panel_info()["no_real_orders"] is True)
        self._check("backward_compat_panel_tab_count",
                    lambda: get_panel_info()["tab_count"] >= 154)

        # ── hard block conditions (2) ─────────────────────────────────────────
        self._check("hard_block_conditions_count_20",
                    lambda: len(get_hard_block_conditions()) == 20)
        self._check("hard_block_conditions_has_missing_promotion_package",
                    lambda: "missing_promotion_package_source" in get_hard_block_conditions())

        # ── forbidden actions (2) ─────────────────────────────────────────────
        self._check("forbidden_actions_count_9",
                    lambda: len(get_forbidden_monitoring_actions()) == 9)
        self._check("forbidden_actions_has_buy",
                    lambda: "BUY" in get_forbidden_monitoring_actions())

        # ── allowed actions (2) ───────────────────────────────────────────────
        self._check("allowed_actions_count_16",
                    lambda: len(get_allowed_monitoring_actions()) == 16)
        self._check("allowed_actions_has_monitor",
                    lambda: "MONITOR" in get_allowed_monitoring_actions())

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)
        from paper_trading.small_capital_strategy.strategy_monitoring_models_v194 import MonitoringHealthSummary
        return MonitoringHealthSummary(
            passed=passed,
            failed=failed,
            total=total,
            all_passed=(failed == 0),
            checks=list(self._checks),
        )


def run_health_check() -> Dict[str, Any]:
    """Run health check and return summary dict."""
    checker = StrategyMonitoringHealthCheck()
    summary = checker.run()
    return {
        "passed": summary.passed,
        "failed": summary.failed,
        "total": summary.total,
        "all_passed": summary.all_passed,
        "status": "PASS" if summary.all_passed else "FAIL",
        "checks": summary.checks,
        "paper_only": True,
        "no_real_orders": True,
        "monitoring_only": True,
        "schema_version": "194",
    }


if __name__ == "__main__":
    result = run_health_check()
    print(f"Strategy Monitoring Health v1.9.4: {result['passed']}/{result['total']} passed")
    if result["failed"] > 0:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  FAIL: {c['name']} — {c['error']}")
    else:
        print("PASS all checks")
