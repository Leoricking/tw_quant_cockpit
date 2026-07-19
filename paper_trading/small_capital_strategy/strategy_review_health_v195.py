"""
paper_trading/small_capital_strategy/strategy_review_health_v195.py
Health check for Paper Strategy Review Alert & Human Approval Lab v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List


class StrategyReviewHealthCheck:
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

    def run(self) -> "ReviewHealthSummary":
        from paper_trading.small_capital_strategy.strategy_review_models_v195 import ReviewHealthSummary
        self._checks = []

        # ── version (6) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_version_v195 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_review_alert_categories, get_review_severities,
            get_review_decision_states, get_review_recommendations,
            get_forbidden_review_actions, get_allowed_review_actions,
            get_hard_block_conditions,
        )
        self._check("version_is_195", lambda: VERSION == "1.9.5")
        self._check("release_name_correct",
                    lambda: RELEASE_NAME == "Paper Strategy Review Alert & Human Approval Lab")
        self._check("schema_version_195", lambda: SCHEMA_VERSION == "195")
        self._check("verify_version_returns_true", lambda: verify_version() is True)
        self._check("is_known_release_v195",
                    lambda: is_known_release("Paper Strategy Review Alert & Human Approval Lab v1.9.5"))
        self._check("version_info_paper_only", lambda: get_version_info()["paper_only"] is True)

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_safety_v195 import (
            SAFETY_FLAGS, run_safety_audit, is_safe_output_path, is_forbidden_action,
            is_allowed_action, validate_review_action,
            FORBIDDEN_REVIEW_ACTIONS, ALLOWED_REVIEW_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_flag_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_flag_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_flag_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_flag_review_only", lambda: SAFETY_FLAGS["review_only"] is True)
        self._check("safety_flag_human_approval_only",
                    lambda: SAFETY_FLAGS["human_approval_only"] is True)
        self._check("safety_flag_not_investment_advice",
                    lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._check("safety_flag_no_production_mutation",
                    lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._check("safety_flag_broker_execution_false",
                    lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_flag_auto_approval_false",
                    lambda: SAFETY_FLAGS["auto_approval"] is False)

        # ── review alert categories (3) ───────────────────────────────────────
        self._check("review_alert_categories_count_14",
                    lambda: len(get_review_alert_categories()) == 14)
        self._check("review_alert_categories_has_manual_approval",
                    lambda: "MANUAL_APPROVAL_REQUIRED" in get_review_alert_categories())
        self._check("review_alert_categories_has_rollback_trigger",
                    lambda: "ROLLBACK_TRIGGER_REVIEW" in get_review_alert_categories())

        # ── review severities (2) ─────────────────────────────────────────────
        self._check("review_severities_count_5", lambda: len(get_review_severities()) == 5)
        self._check("review_severities_has_critical",
                    lambda: "CRITICAL" in get_review_severities())

        # ── review decision states (2) ────────────────────────────────────────
        self._check("review_decision_states_count_10",
                    lambda: len(get_review_decision_states()) == 10)
        self._check("review_decision_states_has_approved_for_paper",
                    lambda: "APPROVED_FOR_PAPER_ONLY" in get_review_decision_states())

        # ── review recommendations (2) ────────────────────────────────────────
        self._check("review_recommendations_count_10",
                    lambda: len(get_review_recommendations()) == 10)
        self._check("review_recommendations_has_approve_paper",
                    lambda: "APPROVE_FOR_PAPER_ONLY" in get_review_recommendations())

        # ── models (25) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_models_v195 import (
            StrategyReviewInput, StrategyReviewResult, ReviewAlert, ReviewAlertSource,
            ReviewAlertSeverity, ReviewAlertCategory, HumanApprovalRequest,
            HumanApprovalChecklist, HumanApprovalDecision, ReviewDecisionState,
            ReviewDecisionRationale, RollbackReviewTicket, ReviewEvidenceLink,
            ReviewEvidencePack, ReviewFinding, ReviewRecommendation,
            ReviewExportManifest, ReviewAuditTrail, ReviewDashboard,
            ReviewHealthSummary as RHS, ReviewValidationResult, ReviewQueue,
            ReviewQueueSummary, ReviewSlaStatus, ReviewEscalationRule,
            get_all_model_names,
        )
        self._check("model_review_input_paper_only",
                    lambda: StrategyReviewInput().paper_only is True)
        self._check("model_review_result_no_real_orders",
                    lambda: StrategyReviewResult().no_real_orders is True)
        self._check("model_review_alert_review_only",
                    lambda: ReviewAlert().review_only is True)
        self._check("model_alert_source_monitoring_review_only",
                    lambda: ReviewAlertSource().monitoring_review_only is True)
        self._check("model_alert_severity_paper_only",
                    lambda: ReviewAlertSeverity().paper_only is True)
        self._check("model_alert_category_not_investment_advice",
                    lambda: ReviewAlertCategory().not_investment_advice is True)
        self._check("model_approval_request_auto_approval_false",
                    lambda: HumanApprovalRequest().auto_approval is False)
        self._check("model_approval_checklist_requires_manual_review",
                    lambda: HumanApprovalChecklist().requires_manual_review is True)
        self._check("model_approval_decision_auto_approval_false",
                    lambda: HumanApprovalDecision().auto_approval is False)
        self._check("model_decision_state_paper_only",
                    lambda: ReviewDecisionState().paper_only is True)
        self._check("model_decision_rationale_audit_only",
                    lambda: ReviewDecisionRationale().audit_only is True)
        self._check("model_rollback_ticket_auto_rollback_false",
                    lambda: RollbackReviewTicket().auto_rollback is False)
        self._check("model_evidence_link_report_only",
                    lambda: ReviewEvidenceLink().report_only is True)
        self._check("model_evidence_pack_audit_only",
                    lambda: ReviewEvidencePack().audit_only is True)
        self._check("model_finding_not_investment_advice",
                    lambda: ReviewFinding().not_investment_advice is True)
        self._check("model_recommendation_no_production_mutation",
                    lambda: ReviewRecommendation().no_production_strategy_mutation is True)
        self._check("model_export_manifest_report_only",
                    lambda: ReviewExportManifest().report_only is True)
        self._check("model_audit_trail_audit_only",
                    lambda: ReviewAuditTrail().audit_only is True)
        self._check("model_dashboard_no_real_orders",
                    lambda: ReviewDashboard().no_real_orders is True)
        self._check("model_health_summary_schema",
                    lambda: RHS().schema_version == "195")
        self._check("model_validation_result_review_only",
                    lambda: ReviewValidationResult().review_only is True)
        self._check("model_review_queue_auto_processing_false",
                    lambda: ReviewQueue().auto_processing is False)
        self._check("model_queue_summary_paper_only",
                    lambda: ReviewQueueSummary().paper_only is True)
        self._check("model_sla_status_paper_only",
                    lambda: ReviewSlaStatus().paper_only is True)
        self._check("model_escalation_rule_auto_escalate_execution_false",
                    lambda: ReviewEscalationRule().auto_escalate_execution is False)
        self._check("model_names_count_25",
                    lambda: len(get_all_model_names()) == 25)

        # ── engine (8) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_engine_v195 import (
            validate_review_action as vra, validate_review_decision_state,
            validate_review_alert_category, build_human_approval_request,
            build_review_alert, build_rollback_review_ticket,
            build_review_evidence_pack, build_review_dashboard, get_engine_info,
        )
        self._check("engine_validate_allowed_action",
                    lambda: vra("REVIEW")["valid"] is True)
        self._check("engine_validate_forbidden_action",
                    lambda: vra("BUY")["blocked"] is True)
        self._check("engine_decision_state_valid",
                    lambda: validate_review_decision_state("APPROVED_FOR_PAPER_ONLY")["valid"] is True)
        self._check("engine_alert_category_valid",
                    lambda: validate_review_alert_category("ROLLBACK_TRIGGER_REVIEW")["valid"] is True)
        self._check("engine_approval_request_missing_review_id_blocked",
                    lambda: build_human_approval_request("", "a", "c")["blocked"] is True)
        self._check("engine_review_alert_missing_review_id_blocked",
                    lambda: build_review_alert("", "DRAWDOWN_REVIEW")["blocked"] is True)
        self._check("engine_rollback_ticket_auto_rollback_false",
                    lambda: build_rollback_review_ticket("R1", "T1")["auto_rollback"] is False)
        self._check("engine_dashboard_missing_id_blocked",
                    lambda: build_review_dashboard("", "R1")["blocked"] is True)

        # ── report (5) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_report_v195 import (
            export_review_summary, export_human_approval_report,
            export_rollback_review_report, export_full_review_pack,
            get_report_section_names,
        )
        self._check("report_summary_missing_id_blocked",
                    lambda: export_review_summary("")["blocked"] is True)
        self._check("report_summary_valid",
                    lambda: export_review_summary("REV-H1")["valid"] is True)
        self._check("report_human_approval_auto_approval_false",
                    lambda: export_human_approval_report("REV-H1")["auto_approval"] is False)
        self._check("report_rollback_review_auto_rollback_false",
                    lambda: export_rollback_review_report("REV-H1")["auto_rollback"] is False)
        self._check("report_section_names_count",
                    lambda: len(get_report_section_names()) >= 10)

        # ── fixtures (4) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_fixtures_v195 import (
            get_all_fixtures, get_fixture_ids, get_blocked_fixtures, get_drift_fixtures,
        )
        self._check("fixtures_count_75", lambda: len(get_all_fixtures()) == 75)
        self._check("fixtures_all_have_schema_version",
                    lambda: all(f["schema_version"] == "195" for f in get_all_fixtures()))
        self._check("fixtures_all_have_paper_only",
                    lambda: all(f["paper_only"] is True for f in get_all_fixtures()))
        self._check("fixtures_blocked_exists",
                    lambda: len(get_blocked_fixtures()) > 0)

        # ── scenarios (4) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_scenarios_v195 import (
            get_all_scenarios, get_scenario_ids, get_blocked_scenarios, get_drift_scenarios,
        )
        self._check("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._check("scenarios_all_have_schema_version",
                    lambda: all(s["schema_version"] == "195" for s in get_all_scenarios()))
        self._check("scenarios_all_have_paper_only",
                    lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._check("scenarios_drift_exists",
                    lambda: len(get_drift_scenarios()) > 0)

        # ── backward compat (4) ───────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION, get_panel_info
        self._check("backward_compat_panel_version_195",
                    lambda: PANEL_VERSION in ("1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10", "2.0.0"))
        self._check("backward_compat_panel_info_paper_only",
                    lambda: get_panel_info()["paper_only"] is True)
        self._check("backward_compat_panel_info_no_real_orders",
                    lambda: get_panel_info()["no_real_orders"] is True)
        self._check("backward_compat_panel_tab_count",
                    lambda: get_panel_info()["tab_count"] >= 157)

        # ── hard block conditions (2) ─────────────────────────────────────────
        self._check("hard_block_conditions_count_19",
                    lambda: len(get_hard_block_conditions()) == 19)
        self._check("hard_block_conditions_has_missing_human_approval_checklist",
                    lambda: "missing_human_approval_checklist" in get_hard_block_conditions())

        # ── forbidden actions (2) ─────────────────────────────────────────────
        self._check("forbidden_actions_count_9",
                    lambda: len(get_forbidden_review_actions()) == 9)
        self._check("forbidden_actions_has_buy",
                    lambda: "BUY" in get_forbidden_review_actions())

        # ── allowed actions (2) ───────────────────────────────────────────────
        self._check("allowed_actions_count_18",
                    lambda: len(get_allowed_review_actions()) == 18)
        self._check("allowed_actions_has_human_approval",
                    lambda: "HUMAN_APPROVAL" in get_allowed_review_actions())

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)
        from paper_trading.small_capital_strategy.strategy_review_models_v195 import ReviewHealthSummary
        return ReviewHealthSummary(
            passed=passed, failed=failed, total=total,
            all_passed=(failed == 0), checks=list(self._checks),
        )


def run_health_check() -> Dict[str, Any]:
    """Run health check and return summary dict."""
    checker = StrategyReviewHealthCheck()
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
        "review_only": True,
        "human_approval_only": True,
        "schema_version": "195",
    }


if __name__ == "__main__":
    result = run_health_check()
    print(f"Strategy Review Health v1.9.5: {result['passed']}/{result['total']} passed")
    if result["failed"] > 0:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  FAIL: {c['name']} — {c['error']}")
    else:
        print("PASS all checks")
