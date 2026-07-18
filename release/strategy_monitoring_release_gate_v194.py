"""
release/strategy_monitoring_release_gate_v194.py
Release gate for Paper Strategy Monitoring & Drift Detection Lab v1.9.4.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List


class StrategyMonitoringReleaseGate:
    VERSION = "1.9.4"
    RELEASE_NAME = "Paper Strategy Monitoring & Drift Detection Lab"
    MIN_SCENARIOS = 75
    MIN_FIXTURES = 75
    MIN_CLI = 18
    MIN_HEALTH_CHECKS = 60
    BASELINE_TESTS = 28407
    MIN_NEW_TESTS = 400

    def __init__(self) -> None:
        self._results: List[Dict[str, Any]] = []

    def _gate(self, name: str, fn) -> None:
        try:
            result = fn()
            passed = bool(result)
        except Exception as exc:
            passed = False
            result = str(exc)
        self._results.append({"name": name, "passed": passed,
                               "error": None if passed else str(result)})

    def run(self) -> Dict[str, Any]:
        self._results = []

        # ── version (8) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_version_v194 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version,
            get_drift_categories, get_drift_severities, get_monitoring_statuses,
            get_monitoring_recommendations, get_forbidden_monitoring_actions,
            get_allowed_monitoring_actions, get_hard_block_conditions,
            is_known_release,
        )
        self._gate("version_194", lambda: VERSION == "1.9.4")
        self._gate("release_name_monitoring",
                   lambda: RELEASE_NAME == "Paper Strategy Monitoring & Drift Detection Lab")
        self._gate("schema_194", lambda: SCHEMA_VERSION == "194")
        self._gate("verify_version_true", lambda: verify_version() is True)
        self._gate("drift_categories_count_17", lambda: len(get_drift_categories()) == 17)
        self._gate("drift_severities_count_5", lambda: len(get_drift_severities()) == 5)
        self._gate("monitoring_statuses_count_6", lambda: len(get_monitoring_statuses()) == 6)
        self._gate("hard_block_conditions_count_20",
                   lambda: len(get_hard_block_conditions()) == 20)

        # ── safety (13) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_safety_v194 import (
            SAFETY_FLAGS, run_safety_audit, is_forbidden_action, is_allowed_action,
            is_safe_output_path, FORBIDDEN_MONITORING_ACTIONS,
            ALLOWED_MONITORING_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._gate("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._gate("safety_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._gate("safety_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._gate("safety_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._gate("safety_monitoring_only",
                   lambda: SAFETY_FLAGS["monitoring_only"] is True)
        self._gate("safety_drift_detection_only",
                   lambda: SAFETY_FLAGS["drift_detection_only"] is True)
        self._gate("safety_not_investment_advice",
                   lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._gate("safety_no_production_mutation",
                   lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._gate("safety_no_live_activation",
                   lambda: SAFETY_FLAGS["no_live_strategy_activation"] is True)
        self._gate("safety_broker_execution_false",
                   lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._gate("safety_live_strategy_activation_false",
                   lambda: SAFETY_FLAGS["live_strategy_activation"] is False)
        self._gate("safety_forbidden_buy",
                   lambda: is_forbidden_action("BUY") is True)
        self._gate("safety_allowed_monitor",
                   lambda: is_allowed_action("MONITOR") is True)

        # ── models (6) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_models_v194 import (
            StrategyMonitoringInput, StrategyMonitoringResult,
            MonitoringRollbackTrigger, MonitoringRecommendation,
            get_all_model_names,
        )
        self._gate("models_count_26", lambda: len(get_all_model_names()) == 26)
        self._gate("model_input_paper_only",
                   lambda: StrategyMonitoringInput().paper_only is True)
        self._gate("model_result_no_real_orders",
                   lambda: StrategyMonitoringResult().no_real_orders is True)
        self._gate("model_rollback_trigger_auto_rollback_false",
                   lambda: MonitoringRollbackTrigger().auto_rollback is False)
        self._gate("model_recommendation_production_blocked",
                   lambda: MonitoringRecommendation().production_trading_blocked is True)
        self._gate("model_input_schema_194",
                   lambda: StrategyMonitoringInput().schema_version == "194")

        # ── engine (8) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_engine_v194 import (
            validate_monitoring_action, validate_monitoring_status,
            validate_drift_category, run_drift_detection,
            build_monitoring_package_snapshot, build_rollback_alert,
            build_monitoring_recommendation, build_monitoring_dashboard,
        )
        self._gate("engine_forbidden_buy_blocked",
                   lambda: validate_monitoring_action("BUY")["blocked"] is True)
        self._gate("engine_allowed_monitor_valid",
                   lambda: validate_monitoring_action("MONITOR")["valid"] is True)
        self._gate("engine_monitoring_status_healthy",
                   lambda: validate_monitoring_status("HEALTHY")["valid"] is True)
        self._gate("engine_drift_category_win_rate",
                   lambda: validate_drift_category("WIN_RATE_DRIFT")["valid"] is True)
        self._gate("engine_drift_detection_missing_id_blocked",
                   lambda: run_drift_detection("", "b", "c", "w")["blocked"] is True)
        self._gate("engine_drift_detection_valid",
                   lambda: run_drift_detection("M1", "B1", "C1", "W1")["valid"] is True)
        self._gate("engine_rollback_alert_auto_rollback_false",
                   lambda: build_rollback_alert("ALT-G1", "WIN_RATE")["auto_rollback"] is False)
        self._gate("engine_dashboard_missing_id_blocked",
                   lambda: build_monitoring_dashboard("", "MON-G1")["blocked"] is True)

        # ── report (5) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_report_v194 import (
            export_monitoring_summary, export_drift_report,
            export_rollback_trigger_report, export_full_monitoring_pack,
            get_report_section_names,
        )
        self._gate("report_summary_missing_id_blocked",
                   lambda: export_monitoring_summary("")["blocked"] is True)
        self._gate("report_summary_valid",
                   lambda: export_monitoring_summary("MON-G2")["valid"] is True)
        self._gate("report_rollback_trigger_auto_rollback_false",
                   lambda: export_rollback_trigger_report("MON-G2")["auto_rollback"] is False)
        self._gate("report_full_pack_paper_only",
                   lambda: export_full_monitoring_pack("MON-G2")["paper_only"] is True)
        self._gate("report_section_names_count",
                   lambda: len(get_report_section_names()) >= 10)

        # ── fixtures (4) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_fixtures_v194 import (
            get_all_fixtures, get_blocked_fixtures, get_drift_fixtures,
        )
        self._gate("fixtures_count_75", lambda: len(get_all_fixtures()) == 75)
        self._gate("fixtures_all_paper_only",
                   lambda: all(f["paper_only"] is True for f in get_all_fixtures()))
        self._gate("fixtures_all_schema_194",
                   lambda: all(f["schema_version"] == "194" for f in get_all_fixtures()))
        self._gate("fixtures_drift_exists",
                   lambda: len(get_drift_fixtures()) > 0)

        # ── scenarios (4) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_scenarios_v194 import (
            get_all_scenarios, get_blocked_scenarios, get_drift_scenarios,
        )
        self._gate("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._gate("scenarios_all_paper_only",
                   lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._gate("scenarios_all_schema_194",
                   lambda: all(s["schema_version"] == "194" for s in get_all_scenarios()))
        self._gate("scenarios_drift_exists",
                   lambda: len(get_drift_scenarios()) > 0)

        # ── GUI (4) ───────────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import (
            PANEL_VERSION, get_panel_info,
            render_strategy_monitoring_tab,
            render_drift_detection_tab,
            render_rollback_alerts_tab,
            get_monitoring_tab_names,
        )
        self._gate("gui_panel_version_194", lambda: PANEL_VERSION in ("1.9.4", "1.9.5"))
        self._gate("gui_panel_info_paper_only",
                   lambda: get_panel_info()["paper_only"] is True)
        self._gate("gui_monitoring_tab_paper_only",
                   lambda: render_strategy_monitoring_tab()["paper_only"] is True)
        self._gate("gui_drift_detection_tab_paper_only",
                   lambda: render_drift_detection_tab()["paper_only"] is True)
        self._gate("gui_rollback_alerts_tab_paper_only",
                   lambda: render_rollback_alerts_tab()["paper_only"] is True)
        self._gate("gui_monitoring_tab_names_count",
                   lambda: len(get_monitoring_tab_names()) == 3)

        # ── CLI (4) ───────────────────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        sm_commands = [c for c in PROVIDER_COMMANDS if c.name.startswith("strategy-monitoring-")]
        self._gate("cli_monitoring_commands_count_18",
                   lambda: len(sm_commands) >= 18)
        self._gate("cli_monitoring_version_command",
                   lambda: any(c.name == "strategy-monitoring-version" for c in sm_commands))
        self._gate("cli_monitoring_drift_command",
                   lambda: any(c.name == "strategy-monitoring-drift" for c in sm_commands))
        self._gate("cli_monitoring_safety_audit_command",
                   lambda: any(c.name == "strategy-monitoring-safety-audit" for c in sm_commands))

        # ── health (2) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_monitoring_health_v194 import run_health_check
        health = run_health_check()
        self._gate("health_all_passed", lambda: health["all_passed"] is True)
        self._gate("health_check_count_ge_60", lambda: health["total"] >= 60)

        # ── backward compat (2) ───────────────────────────────────────────────
        self._gate("backward_compat_panel_version",
                   lambda: get_panel_info()["panel_version"] in ("1.9.4", "1.9.5"))
        self._gate("backward_compat_tab_count",
                   lambda: get_panel_info()["tab_count"] >= 154)

        # ── recommendations (2) ───────────────────────────────────────────────
        self._gate("recommendations_count_13",
                   lambda: len(get_monitoring_recommendations()) == 13)
        self._gate("recommendations_has_rollback_to_baseline",
                   lambda: "ROLLBACK_TO_BASELINE" in get_monitoring_recommendations())

        passed = sum(1 for r in self._results if r["passed"])
        failed = sum(1 for r in self._results if not r["passed"])
        total = len(self._results)
        return {
            "gate_passed": failed == 0,
            "passed_count": passed,
            "failed_count": failed,
            "total": total,
            "passed": passed,
            "failed": failed,
            "results": self._results,
            "version": self.VERSION,
            "release_name": self.RELEASE_NAME,
            "paper_only": True,
            "research_only": True,
            "monitoring_only": True,
            "drift_detection_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
            "no_auto_rollback": True,
            "schema_version": "194",
        }


def run_release_gate() -> Dict[str, Any]:
    """Run release gate and return result dict."""
    gate = StrategyMonitoringReleaseGate()
    return gate.run()


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Strategy Monitoring Release Gate v1.9.4: {result['passed_count']}/{result['total']} passed")
    if result["failed_count"] > 0:
        for r in result["results"]:
            if not r["passed"]:
                print(f"  FAIL: {r['name']} — {r['error']}")
    else:
        print("PASS all gates")
