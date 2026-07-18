"""
release/decision_workflow_release_gate_v188.py
Release gate for Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Workflow Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List


class DecisionWorkflowReleaseGate:
    VERSION = "1.8.8"
    RELEASE_NAME = "Paper Decision Workflow Runner"
    MIN_SCENARIOS = 75
    MIN_FIXTURES = 75
    MIN_CLI = 21
    MIN_HEALTH_CHECKS = 60
    BASELINE_TESTS = 25143
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
        self._results.append({"name": name, "passed": passed, "error": None if passed else str(result)})

    def run(self) -> Dict[str, Any]:
        self._results = []

        # ── version ──────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_version_v188 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version,
            get_workflow_types, get_workflow_steps, get_final_workflow_grades,
            get_allowed_workflow_actions, get_forbidden_workflow_actions,
        )
        self._gate("version_188", lambda: VERSION == "1.8.8")
        self._gate("release_name_workflow_runner", lambda: RELEASE_NAME == "Paper Decision Workflow Runner")
        self._gate("schema_188", lambda: SCHEMA_VERSION == "188")
        self._gate("verify_version_true", lambda: verify_version() is True)
        self._gate("workflow_types_12", lambda: len(get_workflow_types()) == 12)
        self._gate("workflow_steps_20", lambda: len(get_workflow_steps()) == 20)
        self._gate("final_grades_5", lambda: len(get_final_workflow_grades()) == 5)
        self._gate("allowed_actions_20", lambda: len(get_allowed_workflow_actions()) == 20)
        self._gate("forbidden_actions_no_buy", lambda: "BUY" in get_forbidden_workflow_actions())
        self._gate("forbidden_actions_no_broker_order", lambda: "BROKER_ORDER" in get_forbidden_workflow_actions())

        # ── safety ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_safety_v188 import (
            SAFETY_FLAGS, run_safety_audit, is_forbidden_action, is_allowed_action,
            is_safe_output_path,
        )
        self._gate("safety_audit_pass", lambda: run_safety_audit()["all_safe"] is True)
        self._gate("safety_paper_only_true", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._gate("safety_no_real_orders_true", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._gate("safety_no_broker_true", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._gate("safety_not_investment_advice_true", lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._gate("safety_production_trading_blocked_true", lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._gate("safety_broker_execution_false", lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._gate("safety_real_order_false", lambda: SAFETY_FLAGS["real_order"] is False)
        self._gate("safety_buy_forbidden", lambda: is_forbidden_action("BUY") is True)
        self._gate("safety_sell_forbidden", lambda: is_forbidden_action("SELL") is True)
        self._gate("safety_wait_allowed", lambda: is_allowed_action("WAIT") is True)
        self._gate("safety_decision_only_allowed", lambda: is_allowed_action("DECISION_ONLY") is True)
        self._gate("safety_workflow_only_allowed", lambda: is_allowed_action("WORKFLOW_ONLY") is True)
        self._gate("safety_safe_path_reports", lambda: is_safe_output_path("reports/") is True)
        self._gate("safety_unsafe_path_prod_db", lambda: is_safe_output_path("production_db") is False)

        # ── models ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_models_v188 import (
            WorkflowInput, WorkflowResult, WorkflowContext, WorkflowStep,
            WorkflowStepResult, WorkflowRunManifest, DailyWorkflowPlan,
            WeeklyWorkflowPlan, PreMarketWorkflow, PostMarketWorkflow,
            WatchlistWorkflow, CandidateWorkflow, RiskWorkflow, PortfolioWorkflow,
            ReportWorkflow, EvidenceWorkflow, AuditWorkflow,
            WorkflowBlockReason, WorkflowValidationResult, WorkflowHealthSummary,
            WorkflowDashboard, WorkflowExportManifest, get_all_model_names,
        )
        self._gate("model_count_22", lambda: len(get_all_model_names()) == 22)
        self._gate("model_WorkflowInput_paper_only", lambda: WorkflowInput().paper_only is True)
        self._gate("model_WorkflowResult_paper_only", lambda: WorkflowResult().paper_only is True)
        self._gate("model_DailyWorkflowPlan_paper_only", lambda: DailyWorkflowPlan().paper_only is True)
        self._gate("model_WeeklyWorkflowPlan_paper_only", lambda: WeeklyWorkflowPlan().paper_only is True)
        self._gate("model_WorkflowDashboard_paper_only", lambda: WorkflowDashboard().paper_only is True)
        self._gate("model_WorkflowExportManifest_paper_only", lambda: WorkflowExportManifest().paper_only is True)

        # ── engine ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_engine_v188 import (
            run_workflow, build_daily_workflow, build_weekly_workflow,
            build_pre_market_workflow, build_post_market_workflow,
            build_watchlist_workflow, build_candidate_workflow,
            build_risk_workflow, build_portfolio_workflow,
            build_report_workflow, build_evidence_workflow, build_audit_workflow,
            build_workflow_dashboard, build_workflow_export_manifest,
            validate_workflow_result, get_engine_info,
        )
        _inp = WorkflowInput()
        _result = run_workflow(_inp)
        self._gate("engine_run_workflow_paper_only", lambda: _result.paper_only is True)
        self._gate("engine_run_workflow_no_real_orders", lambda: _result.no_real_orders is True)
        self._gate("engine_run_workflow_grade_valid", lambda: _result.final_workflow_grade in ("COMPLETE", "PARTIAL", "BLOCKED"))
        self._gate("engine_run_workflow_action_valid", lambda: is_allowed_action(_result.workflow_action))
        self._gate("engine_run_workflow_steps_20", lambda: len(_result.workflow_steps) == 20)
        self._gate("engine_daily_workflow_type", lambda: build_daily_workflow(_inp).workflow_type == "daily_workflow")
        self._gate("engine_weekly_workflow_type", lambda: build_weekly_workflow(_inp).workflow_type == "weekly_workflow")
        self._gate("engine_pre_market_workflow_type", lambda: build_pre_market_workflow(_inp).workflow_type == "pre_market_workflow")
        self._gate("engine_post_market_workflow_type", lambda: build_post_market_workflow(_inp).workflow_type == "post_market_workflow")
        self._gate("engine_watchlist_workflow_type", lambda: build_watchlist_workflow(_inp).workflow_type == "watchlist_workflow")
        self._gate("engine_candidate_workflow_type", lambda: build_candidate_workflow(_inp).workflow_type == "candidate_review_workflow")
        self._gate("engine_risk_workflow_type", lambda: build_risk_workflow(_inp).workflow_type == "risk_review_workflow")
        self._gate("engine_portfolio_workflow_type", lambda: build_portfolio_workflow(_inp).workflow_type == "portfolio_review_workflow")
        self._gate("engine_report_workflow_type", lambda: build_report_workflow(_inp).workflow_type == "report_generation_workflow")
        self._gate("engine_evidence_workflow_type", lambda: build_evidence_workflow(_inp).workflow_type == "evidence_pack_workflow")
        self._gate("engine_audit_workflow_type", lambda: build_audit_workflow(_inp).workflow_type == "audit_trail_workflow")
        self._gate("engine_dashboard_paper_only", lambda: build_workflow_dashboard(_result).paper_only is True)
        self._gate("engine_export_manifest_paper_only", lambda: build_workflow_export_manifest(_result).paper_only is True)
        self._gate("engine_validation_paper_only", lambda: validate_workflow_result(_result).paper_only is True)

        # ── report ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_report_v188 import (
            export_as_json, export_as_markdown, export_as_console_summary,
            export_as_dashboard_payload,
        )
        self._gate("report_json_is_str", lambda: isinstance(export_as_json(_result), str))
        self._gate("report_markdown_is_str", lambda: isinstance(export_as_markdown(_result), str))
        self._gate("report_console_is_str", lambda: isinstance(export_as_console_summary(_result), str))
        self._gate("report_dashboard_is_dict", lambda: isinstance(export_as_dashboard_payload(_result), dict))

        # ── scenarios ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_scenarios_v188 import (
            count_scenarios, get_scenarios, get_scenario_by_id,
        )
        self._gate("scenarios_75", lambda: count_scenarios() == 75)
        self._gate("scenarios_list_75", lambda: len(get_scenarios()) == 75)
        self._gate("scenario_dw188_001_exists", lambda: get_scenario_by_id("DW188-001") is not None)
        self._gate("scenarios_all_paper_only", lambda: all(s.get("paper_only") for s in get_scenarios()))
        self._gate("scenarios_all_no_real_orders", lambda: all(s.get("no_real_orders") for s in get_scenarios()))

        # ── fixtures ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_fixtures_v188 import (
            get_fixture_count, get_fixture_dir, get_fixture_info, get_fixtures,
        )
        self._gate("fixtures_75", lambda: get_fixture_count() == 75)
        self._gate("fixtures_dir_is_str", lambda: isinstance(get_fixture_dir(), str))
        self._gate("fixtures_info_paper_only", lambda: get_fixture_info()["paper_only"] is True)
        self._gate("fixtures_all_paper_only", lambda: all(f.get("paper_only") for f in get_fixtures()))
        self._gate("fixtures_all_no_real_orders", lambda: all(f.get("no_real_orders") for f in get_fixtures()))

        # ── CLI ───────────────────────────────────────────────────────────────
        from cli.command_registry import get_commands_by_group
        _dw_cmds = get_commands_by_group("decision_workflow")
        self._gate("cli_decision_workflow_group_exists", lambda: len(_dw_cmds) >= 21)
        self._gate("cli_decision_workflow_count_21", lambda: len(_dw_cmds) == 21)
        _dw_names = {c.name for c in _dw_cmds}
        self._gate("cli_decision_workflow_version_exists", lambda: "decision-workflow-version" in _dw_names)
        self._gate("cli_decision_workflow_run_exists", lambda: "decision-workflow-run" in _dw_names)
        self._gate("cli_decision_workflow_daily_exists", lambda: "decision-workflow-daily" in _dw_names)
        self._gate("cli_decision_workflow_weekly_exists", lambda: "decision-workflow-weekly" in _dw_names)
        self._gate("cli_decision_workflow_health_exists", lambda: "decision-workflow-health" in _dw_names)
        self._gate("cli_decision_workflow_gate_exists", lambda: "decision-workflow-gate" in _dw_names)

        # ── GUI ───────────────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import (
            _TABS_V188_DECISION_WORKFLOW, _TABS, PANEL_VERSION,
            render_decision_workflow_tab, render_daily_workflow_tab,
            render_weekly_workflow_tab,
        )
        self._gate("gui_panel_version_188", lambda: PANEL_VERSION in ("1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6"))
        self._gate("gui_v188_tabs_count_3", lambda: len(_TABS_V188_DECISION_WORKFLOW) == 3)
        self._gate("gui_decision_workflow_tab_in_tabs", lambda: "decision_workflow" in _TABS_V188_DECISION_WORKFLOW)
        self._gate("gui_daily_workflow_tab_in_tabs", lambda: "daily_workflow" in _TABS_V188_DECISION_WORKFLOW)
        self._gate("gui_weekly_workflow_tab_in_tabs", lambda: "weekly_workflow" in _TABS_V188_DECISION_WORKFLOW)
        self._gate("gui_tabs_include_v188", lambda: all(t in _TABS for t in _TABS_V188_DECISION_WORKFLOW))
        self._gate("gui_render_decision_workflow_tab", lambda: render_decision_workflow_tab()["paper_only"] is True)
        self._gate("gui_render_daily_workflow_tab", lambda: render_daily_workflow_tab()["paper_only"] is True)
        self._gate("gui_render_weekly_workflow_tab", lambda: render_weekly_workflow_tab()["paper_only"] is True)

        # ── health check ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_health_v188 import run_health_check
        _health = run_health_check()
        self._gate("health_check_passes", lambda: _health.all_passed is True)
        self._gate("health_check_total_gte_60", lambda: _health.total >= 60)
        self._gate("health_check_no_failures", lambda: _health.failed == 0)

        # ── backward compat ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_report_version_v187 import VERSION as V187
        self._gate("backward_compat_v187_accessible", lambda: V187 == "1.8.7")
        from paper_trading.small_capital_strategy.decision_cockpit_version_v186 import VERSION as V186
        self._gate("backward_compat_v186_accessible", lambda: V186 == "1.8.6")

        # ── no forbidden output ───────────────────────────────────────────────
        _json_out = export_as_json(_result)
        self._gate("no_forbidden_buy_in_json", lambda: "\"BUY\"" not in _json_out)
        self._gate("no_forbidden_sell_in_json", lambda: "\"SELL\"" not in _json_out)
        self._gate("no_forbidden_order_in_json", lambda: "\"ORDER\"" not in _json_out)
        self._gate("no_forbidden_execute_in_json", lambda: "\"EXECUTE\"" not in _json_out)
        self._gate("no_forbidden_broker_order_in_json", lambda: "BROKER_ORDER" not in _json_out)

        total = len(self._results)
        passed = sum(1 for r in self._results if r["passed"])
        failed_items = [r for r in self._results if not r["passed"]]
        all_passed = len(failed_items) == 0

        return {
            "version": self.VERSION,
            "release_name": self.RELEASE_NAME,
            "total": total,
            "passed": passed,
            "failed": len(failed_items),
            "all_passed": all_passed,
            "status": "PASS" if all_passed else "FAIL",
            "failed_items": failed_items,
            "paper_only": True,
            "research_only": True,
            "workflow_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
            "production_trading_blocked": True,
        }


def run_release_gate() -> Dict[str, Any]:
    return DecisionWorkflowReleaseGate().run()


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Decision Workflow Release Gate v1.8.8: {result['status']} ({result['passed']}/{result['total']})")
    if result["failed_items"]:
        for item in result["failed_items"]:
            print(f"  FAIL: {item['name']}: {item['error']}")
    if not result["all_passed"]:
        import sys; sys.exit(1)
