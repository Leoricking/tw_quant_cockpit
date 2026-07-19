"""
release/decision_report_release_gate_v187.py
Release gate for Decision Report Export & Evidence Pack v1.8.7. 60+ gate checks.
gate_passed=True required for release.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.8.7"
MIN_CHECKS = 60


class DecisionReportReleaseGate:
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

    def run(self) -> Dict[str, Any]:
        self._checks = []

        # ── health (4) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_health_v187 import run_health_check
        _health = run_health_check()
        self._check("health_all_passed", lambda: _health.all_passed is True)
        self._check("health_status_pass", lambda: _health.status == "PASS")
        self._check("health_failed_zero", lambda: _health.failed == 0)
        self._check("health_total_ge_60", lambda: _health.total >= 60)

        # ── version (5) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_version_v187 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_report_types, get_export_formats, get_final_report_grades,
        )
        self._check("gate_version_187", lambda: VERSION == "1.8.7")
        self._check("gate_release_name", lambda: RELEASE_NAME == "Decision Report Export & Evidence Pack")
        self._check("gate_schema_version_187", lambda: SCHEMA_VERSION == "187")
        self._check("gate_verify_version", lambda: verify_version() is True)
        self._check("gate_is_known_release", lambda: is_known_release("Decision Report Export & Evidence Pack v1.8.7"))

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_safety_v187 import (
            SAFETY_FLAGS, run_safety_audit, is_safe_output_path, is_forbidden_action,
            is_allowed_action, FORBIDDEN_REPORT_ACTIONS, ALLOWED_REPORT_ACTIONS,
            HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_paper_only_true", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_no_real_orders_true", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_no_broker_true", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_not_investment_advice_true", lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._check("safety_production_trading_blocked_true", lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_broker_execution_false", lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_real_order_false", lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("safety_forbidden_actions_count_ge_8", lambda: len(FORBIDDEN_REPORT_ACTIONS) >= 8)
        self._check("safety_hard_block_conditions_count_ge_10", lambda: len(HARD_BLOCK_CONDITIONS) >= 10)

        # ── models (5) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_models_v187 import (
            DecisionReportInput, DecisionReportResult, DailyDecisionReport,
            WeeklyDecisionReport, get_all_model_names,
        )
        self._check("models_count_22", lambda: len(get_all_model_names()) == 22)
        self._check("models_input_paper_only", lambda: DecisionReportInput().paper_only is True)
        self._check("models_result_no_real_orders", lambda: DecisionReportResult().no_real_orders is True)
        self._check("models_daily_production_trading_blocked", lambda: DailyDecisionReport().production_trading_blocked is True)
        self._check("models_weekly_not_investment_advice", lambda: WeeklyDecisionReport().not_investment_advice is True)

        # ── engine (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_engine_v187 import (
            validate_report_action, validate_report_grade, validate_report_type,
            build_candidate_evidence_item, build_block_reason_evidence,
            build_evidence_pack, build_audit_trail, build_daily_report,
            build_weekly_report, run_decision_report, build_export_manifest,
            validate_report, get_engine_info,
        )
        _inp = DecisionReportInput()
        self._check("engine_validate_action_wait", lambda: validate_report_action("WAIT") is True)
        self._check("engine_reject_forbidden_buy", lambda: validate_report_action("BUY") is False)
        self._check("engine_validate_grade_complete", lambda: validate_report_grade("COMPLETE") is True)
        self._check("engine_validate_type_daily", lambda: validate_report_type("daily_decision_report") is True)
        self._check("engine_build_daily_report_type", lambda: build_daily_report(_inp).report_type == "daily_decision_report")
        self._check("engine_build_weekly_report_type", lambda: build_weekly_report(_inp).report_type == "weekly_decision_report")
        self._check("engine_build_audit_trail", lambda: build_audit_trail(_inp).audit_complete is True)
        self._check("engine_build_evidence_pack", lambda: build_evidence_pack(_inp).paper_only is True)
        self._check("engine_run_decision_report_paper_only", lambda: run_decision_report(_inp).paper_only is True)
        self._check("engine_info_version_187", lambda: get_engine_info()["version"] == "1.8.7")

        # ── export (5) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_export_v187 import (
            export_as_json, export_as_markdown, export_as_csv_rows,
            export_as_console_summary, export_as_dashboard_payload,
            run_all_exports, get_export_info,
        )
        _res = run_decision_report(_inp)
        self._check("export_json_parseable", lambda: __import__("json").loads(export_as_json(_res)).get("paper_only") is True)
        self._check("export_markdown_contains_header", lambda: "Decision Report Export" in export_as_markdown(_res))
        self._check("export_csv_rows_list", lambda: len(export_as_csv_rows(_res)) > 1)
        self._check("export_console_summary_str", lambda: "Decision Report" in export_as_console_summary(_res))
        self._check("export_dashboard_paper_only", lambda: export_as_dashboard_payload(_res)["paper_only"] is True)

        # ── scenarios (4) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_scenarios_v187 import (
            count_scenarios, get_scenarios, get_scenario_by_id, get_scenarios_by_category,
        )
        self._check("scenarios_count_eq_75", lambda: count_scenarios() == 75)
        self._check("scenarios_list_len_75", lambda: len(get_scenarios()) == 75)
        self._check("scenarios_dr187_001_exists", lambda: get_scenario_by_id("DR187-001") is not None)
        self._check("scenarios_dr187_001_paper_only", lambda: get_scenario_by_id("DR187-001")["paper_only"] is True)

        # ── fixtures (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_fixtures_v187 import (
            get_fixture_count, get_fixture_dir, get_fixture_info,
        )
        self._check("fixtures_count_75", lambda: get_fixture_count() == 75)
        self._check("fixtures_dir_str", lambda: isinstance(get_fixture_dir(), str))
        self._check("fixtures_info_paper_only", lambda: get_fixture_info()["paper_only"] is True)

        # ── GUI (3) ───────────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import (
            PANEL_VERSION, render_decision_report_tab,
            render_evidence_pack_tab, render_audit_trail_report_tab,
        )
        self._check("gui_panel_version_187", lambda: PANEL_VERSION in ("1.8.7", "1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10", "2.0.0"))
        self._check("gui_render_decision_report_tab", lambda: render_decision_report_tab()["paper_only"] is True)
        self._check("gui_render_evidence_pack_tab", lambda: render_evidence_pack_tab()["paper_only"] is True)

        # ── CLI (3) ───────────────────────────────────────────────────────────
        from cli.command_registry import get_all_commands, get_commands_by_group
        _dr_cmds = get_commands_by_group("decision_report")
        self._check("cli_decision_report_group_exists", lambda: len(_dr_cmds) >= 23)
        self._check("cli_decision_report_run_exists", lambda: any(c.name == "decision-report-run" for c in _dr_cmds))
        self._check("cli_all_dr_commands_research_only", lambda: all(c.safety_classification == "RESEARCH_ONLY" for c in _dr_cmds))

        # ── backward compat (5) ───────────────────────────────────────────────
        self._check("compat_report_types_daily", lambda: "daily_decision_report" in get_report_types())
        self._check("compat_report_types_weekly", lambda: "weekly_decision_report" in get_report_types())
        self._check("compat_export_formats_json", lambda: "json" in get_export_formats())
        self._check("compat_export_formats_markdown", lambda: "markdown" in get_export_formats())
        self._check("compat_final_grades_complete", lambda: "COMPLETE" in get_final_report_grades())

        # ── no forbidden actions (3) ──────────────────────────────────────────
        self._check("no_forbidden_buy_in_engine", lambda: validate_report_action("BUY") is False)
        self._check("no_forbidden_sell_in_engine", lambda: validate_report_action("SELL") is False)
        self._check("no_forbidden_execute_in_engine", lambda: validate_report_action("EXECUTE") is False)

        total = len(self._checks)
        passed = sum(1 for c in self._checks if c["passed"])
        failed = total - passed
        gate_passed = (failed == 0 and total >= MIN_CHECKS)
        return {
            "gate_version": GATE_VERSION,
            "total": total, "passed": passed, "failed": failed,
            "gate_passed": gate_passed,
            "status": "PASS" if gate_passed else "FAIL",
            "checks": self._checks,
            "paper_only": True, "report_only": True, "audit_only": True,
            "no_real_orders": True, "schema_version": "187",
        }


def run_gate() -> Dict[str, Any]:
    return DecisionReportReleaseGate().run()


if __name__ == "__main__":
    result = run_gate()
    print(f"Decision Report Release Gate v1.8.7: {result['status']} ({result['passed']}/{result['total']})")
    if not result["gate_passed"]:
        import sys; sys.exit(1)
