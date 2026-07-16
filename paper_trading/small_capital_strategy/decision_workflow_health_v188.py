"""
paper_trading/small_capital_strategy/decision_workflow_health_v188.py
Health check for Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Workflow Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List


class DecisionWorkflowHealthCheck:
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

    def run(self) -> "WorkflowHealthSummary":
        from paper_trading.small_capital_strategy.decision_workflow_models_v188 import WorkflowHealthSummary
        self._checks = []

        # ── version (5) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_version_v188 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_workflow_types, get_workflow_steps,
            get_final_workflow_grades, get_allowed_workflow_actions,
        )
        self._check("version_is_188", lambda: VERSION == "1.8.8")
        self._check("release_name_correct", lambda: RELEASE_NAME == "Paper Decision Workflow Runner")
        self._check("schema_version_188", lambda: SCHEMA_VERSION == "188")
        self._check("verify_version_returns_true", lambda: verify_version() is True)
        self._check("is_known_release_v188", lambda: is_known_release("Paper Decision Workflow Runner v1.8.8"))

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_safety_v188 import (
            SAFETY_FLAGS, run_safety_audit, is_safe_output_path, is_forbidden_action,
            is_allowed_action, validate_workflow_action, FORBIDDEN_WORKFLOW_ACTIONS,
            ALLOWED_WORKFLOW_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_flag_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_flag_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_flag_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_flag_not_investment_advice", lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._check("safety_flag_production_trading_blocked", lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_flag_broker_execution_false", lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_flag_real_order_false", lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("safety_forbidden_buy", lambda: is_forbidden_action("BUY") is True)
        self._check("safety_allowed_wait", lambda: is_allowed_action("WAIT") is True)

        # ── models (22) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_models_v188 import (
            WorkflowInput, WorkflowResult, WorkflowContext, WorkflowStep,
            WorkflowStepResult, WorkflowRunManifest, DailyWorkflowPlan,
            WeeklyWorkflowPlan, PreMarketWorkflow, PostMarketWorkflow,
            WatchlistWorkflow, CandidateWorkflow, RiskWorkflow, PortfolioWorkflow,
            ReportWorkflow, EvidenceWorkflow, AuditWorkflow,
            WorkflowBlockReason, WorkflowValidationResult, WorkflowHealthSummary as _WHS,
            WorkflowDashboard, WorkflowExportManifest, get_all_model_names,
        )
        self._check("model_WorkflowInput_paper_only", lambda: WorkflowInput().paper_only is True)
        self._check("model_WorkflowResult_paper_only", lambda: WorkflowResult().paper_only is True)
        self._check("model_WorkflowContext_paper_only", lambda: WorkflowContext().paper_only is True)
        self._check("model_WorkflowStep_paper_only", lambda: WorkflowStep().paper_only is True)
        self._check("model_WorkflowStepResult_paper_only", lambda: WorkflowStepResult().paper_only is True)
        self._check("model_WorkflowRunManifest_paper_only", lambda: WorkflowRunManifest().paper_only is True)
        self._check("model_DailyWorkflowPlan_paper_only", lambda: DailyWorkflowPlan().paper_only is True)
        self._check("model_WeeklyWorkflowPlan_paper_only", lambda: WeeklyWorkflowPlan().paper_only is True)
        self._check("model_PreMarketWorkflow_paper_only", lambda: PreMarketWorkflow().paper_only is True)
        self._check("model_PostMarketWorkflow_paper_only", lambda: PostMarketWorkflow().paper_only is True)
        self._check("model_WatchlistWorkflow_paper_only", lambda: WatchlistWorkflow().paper_only is True)
        self._check("model_CandidateWorkflow_paper_only", lambda: CandidateWorkflow().paper_only is True)
        self._check("model_RiskWorkflow_paper_only", lambda: RiskWorkflow().paper_only is True)
        self._check("model_PortfolioWorkflow_paper_only", lambda: PortfolioWorkflow().paper_only is True)
        self._check("model_ReportWorkflow_paper_only", lambda: ReportWorkflow().paper_only is True)
        self._check("model_EvidenceWorkflow_paper_only", lambda: EvidenceWorkflow().paper_only is True)
        self._check("model_AuditWorkflow_paper_only", lambda: AuditWorkflow().paper_only is True)
        self._check("model_WorkflowBlockReason_paper_only", lambda: WorkflowBlockReason().paper_only is True)
        self._check("model_WorkflowValidationResult_paper_only", lambda: WorkflowValidationResult().paper_only is True)
        self._check("model_WorkflowHealthSummary_paper_only", lambda: _WHS().paper_only is True)
        self._check("model_WorkflowDashboard_paper_only", lambda: WorkflowDashboard().paper_only is True)
        self._check("model_WorkflowExportManifest_paper_only", lambda: WorkflowExportManifest().paper_only is True)

        # ── engine (8) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_engine_v188 import (
            validate_workflow_action as eng_val_action,
            validate_workflow_grade, validate_workflow_type,
            run_workflow, build_daily_workflow, build_weekly_workflow,
            build_pre_market_workflow, build_post_market_workflow,
            build_watchlist_workflow, build_candidate_workflow,
            build_risk_workflow, build_portfolio_workflow,
            build_report_workflow, build_evidence_workflow, build_audit_workflow,
            build_workflow_dashboard, build_workflow_export_manifest,
            validate_workflow_result, get_engine_info,
        )
        _inp = WorkflowInput()
        self._check("engine_validate_action_wait", lambda: eng_val_action("WAIT") is True)
        self._check("engine_validate_grade_complete", lambda: validate_workflow_grade("COMPLETE") is True)
        self._check("engine_validate_type_daily", lambda: validate_workflow_type("daily_workflow") is True)
        self._check("engine_run_workflow_paper_only", lambda: run_workflow(_inp).paper_only is True)
        self._check("engine_run_workflow_grade", lambda: run_workflow(_inp).final_workflow_grade in ("COMPLETE", "PARTIAL", "BLOCKED"))
        self._check("engine_build_daily_workflow", lambda: build_daily_workflow(_inp).workflow_type == "daily_workflow")
        self._check("engine_build_weekly_workflow", lambda: build_weekly_workflow(_inp).workflow_type == "weekly_workflow")
        self._check("engine_build_pre_market", lambda: build_pre_market_workflow(_inp).workflow_type == "pre_market_workflow")

        # ── report (4) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_report_v188 import (
            export_as_json, export_as_markdown, export_as_console_summary,
            export_as_dashboard_payload, get_report_info,
        )
        _result = run_workflow(_inp)
        self._check("report_export_json_is_str", lambda: isinstance(export_as_json(_result), str))
        self._check("report_export_markdown_is_str", lambda: isinstance(export_as_markdown(_result), str))
        self._check("report_console_summary_is_str", lambda: isinstance(export_as_console_summary(_result), str))
        self._check("report_dashboard_payload_is_dict", lambda: isinstance(export_as_dashboard_payload(_result), dict))

        # ── scenarios (3) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_scenarios_v188 import (
            count_scenarios, get_scenarios, get_scenario_by_id,
        )
        self._check("scenarios_count_75", lambda: count_scenarios() == 75)
        self._check("scenarios_get_75", lambda: len(get_scenarios()) == 75)
        self._check("scenarios_get_by_id_dw188_001", lambda: get_scenario_by_id("DW188-001") is not None)

        # ── fixtures (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_workflow_fixtures_v188 import (
            get_fixture_count, get_fixture_dir, get_fixture_info,
        )
        self._check("fixtures_count_75", lambda: get_fixture_count() == 75)
        self._check("fixtures_dir_is_str", lambda: isinstance(get_fixture_dir(), str))
        self._check("fixtures_info_paper_only", lambda: get_fixture_info()["paper_only"] is True)

        # ── safety audit extras (3) ───────────────────────────────────────────
        self._check("safety_safe_output_path_reports", lambda: is_safe_output_path("reports/") is True)
        self._check("safety_unsafe_output_path_production_db", lambda: is_safe_output_path("production_db") is False)
        self._check("safety_forbidden_action_sell", lambda: is_forbidden_action("SELL") is True)

        # ── workflow types (3) ────────────────────────────────────────────────
        self._check("workflow_types_contains_daily", lambda: "daily_workflow" in get_workflow_types())
        self._check("workflow_types_contains_weekly", lambda: "weekly_workflow" in get_workflow_types())
        self._check("workflow_steps_count_20", lambda: len(get_workflow_steps()) == 20)

        # ── allowed actions (3) ───────────────────────────────────────────────
        self._check("allowed_actions_contains_decision_only", lambda: "DECISION_ONLY" in get_allowed_workflow_actions())
        self._check("allowed_actions_contains_workflow_only", lambda: "WORKFLOW_ONLY" in get_allowed_workflow_actions())
        self._check("allowed_actions_not_buy", lambda: "BUY" not in get_allowed_workflow_actions())

        total = len(self._checks)
        passed = sum(1 for c in self._checks if c["passed"])
        failed = total - passed
        return WorkflowHealthSummary(
            total=total, passed=passed, failed=failed,
            all_passed=(failed == 0), status="PASS" if failed == 0 else "FAIL",
        )


def run_health_check() -> "WorkflowHealthSummary":
    return DecisionWorkflowHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Decision Workflow Health v1.8.8: {result.status} ({result.passed}/{result.total})")
    if not result.all_passed:
        import sys; sys.exit(1)
