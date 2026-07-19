"""
release/strategy_review_release_gate_v195.py
Release gate for Paper Strategy Review Alert & Human Approval Lab v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List


class StrategyReviewReleaseGate:
    VERSION = "1.9.5"
    RELEASE_NAME = "Paper Strategy Review Alert & Human Approval Lab"
    MIN_SCENARIOS = 75
    MIN_FIXTURES = 75
    MIN_CLI = 18
    MIN_HEALTH_CHECKS = 60
    BASELINE_TESTS = 28947
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
        from paper_trading.small_capital_strategy.strategy_review_version_v195 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version,
            get_review_alert_categories, get_review_severities,
            get_review_decision_states, get_review_recommendations,
            get_forbidden_review_actions, get_allowed_review_actions,
            get_hard_block_conditions, is_known_release,
        )
        self._gate("version_195", lambda: VERSION == "1.9.5")
        self._gate("release_name_review",
                   lambda: RELEASE_NAME == "Paper Strategy Review Alert & Human Approval Lab")
        self._gate("schema_195", lambda: SCHEMA_VERSION == "195")
        self._gate("verify_version_true", lambda: verify_version() is True)
        self._gate("review_alert_categories_count_14",
                   lambda: len(get_review_alert_categories()) == 14)
        self._gate("review_severities_count_5", lambda: len(get_review_severities()) == 5)
        self._gate("review_decision_states_count_10",
                   lambda: len(get_review_decision_states()) == 10)
        self._gate("hard_block_conditions_count_19",
                   lambda: len(get_hard_block_conditions()) == 19)

        # ── safety (13) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_safety_v195 import (
            SAFETY_FLAGS, run_safety_audit, is_forbidden_action, is_allowed_action,
            is_safe_output_path, FORBIDDEN_REVIEW_ACTIONS,
            ALLOWED_REVIEW_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._gate("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._gate("safety_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._gate("safety_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._gate("safety_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._gate("safety_review_only", lambda: SAFETY_FLAGS["review_only"] is True)
        self._gate("safety_human_approval_only",
                   lambda: SAFETY_FLAGS["human_approval_only"] is True)
        self._gate("safety_not_investment_advice",
                   lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._gate("safety_no_production_mutation",
                   lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._gate("safety_no_live_activation",
                   lambda: SAFETY_FLAGS["no_live_strategy_activation"] is True)
        self._gate("safety_broker_execution_false",
                   lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._gate("safety_auto_approval_false",
                   lambda: SAFETY_FLAGS["auto_approval"] is False)
        self._gate("safety_forbidden_buy",
                   lambda: is_forbidden_action("BUY") is True)
        self._gate("safety_allowed_review",
                   lambda: is_allowed_action("REVIEW") is True)

        # ── models (6) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_models_v195 import (
            StrategyReviewInput, HumanApprovalDecision,
            RollbackReviewTicket, ReviewRecommendation, get_all_model_names,
        )
        self._gate("models_count_25", lambda: len(get_all_model_names()) == 25)
        self._gate("model_input_paper_only",
                   lambda: StrategyReviewInput().paper_only is True)
        self._gate("model_approval_decision_auto_approval_false",
                   lambda: HumanApprovalDecision().auto_approval is False)
        self._gate("model_rollback_ticket_auto_rollback_false",
                   lambda: RollbackReviewTicket().auto_rollback is False)
        self._gate("model_recommendation_no_production_mutation",
                   lambda: ReviewRecommendation().no_production_strategy_mutation is True)
        self._gate("model_input_schema_195",
                   lambda: StrategyReviewInput().schema_version == "195")

        # ── engine (8) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_engine_v195 import (
            validate_review_action, validate_review_decision_state,
            validate_review_alert_category, build_human_approval_request,
            build_review_alert, build_rollback_review_ticket,
            build_review_dashboard, build_review_evidence_pack,
        )
        self._gate("engine_forbidden_buy_blocked",
                   lambda: validate_review_action("BUY")["blocked"] is True)
        self._gate("engine_allowed_review_valid",
                   lambda: validate_review_action("REVIEW")["valid"] is True)
        self._gate("engine_decision_state_approved_paper",
                   lambda: validate_review_decision_state("APPROVED_FOR_PAPER_ONLY")["valid"] is True)
        self._gate("engine_alert_category_rollback_trigger",
                   lambda: validate_review_alert_category("ROLLBACK_TRIGGER_REVIEW")["valid"] is True)
        self._gate("engine_approval_request_missing_id_blocked",
                   lambda: build_human_approval_request("", "a", "c")["blocked"] is True)
        self._gate("engine_review_alert_valid",
                   lambda: build_review_alert("REV-G1", "DRAWDOWN_REVIEW")["valid"] is True)
        self._gate("engine_rollback_ticket_auto_rollback_false",
                   lambda: build_rollback_review_ticket("R1", "T1")["auto_rollback"] is False)
        self._gate("engine_dashboard_missing_id_blocked",
                   lambda: build_review_dashboard("", "REV-G1")["blocked"] is True)

        # ── report (5) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_report_v195 import (
            export_review_summary, export_human_approval_report,
            export_rollback_review_report, export_full_review_pack,
            get_report_section_names,
        )
        self._gate("report_summary_missing_id_blocked",
                   lambda: export_review_summary("")["blocked"] is True)
        self._gate("report_summary_valid",
                   lambda: export_review_summary("REV-G2")["valid"] is True)
        self._gate("report_human_approval_auto_approval_false",
                   lambda: export_human_approval_report("REV-G2")["auto_approval"] is False)
        self._gate("report_rollback_auto_rollback_false",
                   lambda: export_rollback_review_report("REV-G2")["auto_rollback"] is False)
        self._gate("report_section_names_count",
                   lambda: len(get_report_section_names()) >= 10)

        # ── fixtures (4) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_fixtures_v195 import (
            get_all_fixtures, get_blocked_fixtures, get_drift_fixtures,
        )
        self._gate("fixtures_count_75", lambda: len(get_all_fixtures()) == 75)
        self._gate("fixtures_all_paper_only",
                   lambda: all(f["paper_only"] is True for f in get_all_fixtures()))
        self._gate("fixtures_all_schema_195",
                   lambda: all(f["schema_version"] == "195" for f in get_all_fixtures()))
        self._gate("fixtures_blocked_exists",
                   lambda: len(get_blocked_fixtures()) > 0)

        # ── scenarios (4) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_scenarios_v195 import (
            get_all_scenarios, get_blocked_scenarios, get_drift_scenarios,
        )
        self._gate("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._gate("scenarios_all_paper_only",
                   lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._gate("scenarios_all_schema_195",
                   lambda: all(s["schema_version"] == "195" for s in get_all_scenarios()))
        self._gate("scenarios_drift_exists",
                   lambda: len(get_drift_scenarios()) > 0)

        # ── GUI (6) ───────────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import (
            PANEL_VERSION, get_panel_info,
            render_review_alerts_tab,
            render_human_approval_tab,
            render_rollback_review_tab,
            get_review_tab_names,
        )
        self._gate("gui_panel_version_195", lambda: PANEL_VERSION in ("1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10"))
        self._gate("gui_panel_info_paper_only",
                   lambda: get_panel_info()["paper_only"] is True)
        self._gate("gui_review_alerts_tab_paper_only",
                   lambda: render_review_alerts_tab()["paper_only"] is True)
        self._gate("gui_human_approval_tab_auto_approval_false",
                   lambda: render_human_approval_tab()["auto_approval"] is False)
        self._gate("gui_rollback_review_tab_auto_rollback_false",
                   lambda: render_rollback_review_tab()["auto_rollback"] is False)
        self._gate("gui_review_tab_names_count",
                   lambda: len(get_review_tab_names()) == 3)

        # ── CLI (4) ───────────────────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        sr_commands = [c for c in PROVIDER_COMMANDS if c.name.startswith("strategy-review-")]
        self._gate("cli_review_commands_count_18",
                   lambda: len(sr_commands) >= 18)
        self._gate("cli_review_version_command",
                   lambda: any(c.name == "strategy-review-version" for c in sr_commands))
        self._gate("cli_review_approval_command",
                   lambda: any(c.name == "strategy-review-approval" for c in sr_commands))
        self._gate("cli_review_safety_audit_command",
                   lambda: any(c.name == "strategy-review-safety-audit" for c in sr_commands))

        # ── health (2) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_review_health_v195 import run_health_check
        health = run_health_check()
        self._gate("health_all_passed", lambda: health["all_passed"] is True)
        self._gate("health_check_count_ge_60", lambda: health["total"] >= 60)

        # ── backward compat (2) ───────────────────────────────────────────────
        self._gate("backward_compat_panel_version",
                   lambda: get_panel_info()["panel_version"] in ("1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10"))
        self._gate("backward_compat_tab_count",
                   lambda: get_panel_info()["tab_count"] >= 157)

        # ── recommendations (2) ───────────────────────────────────────────────
        self._gate("recommendations_count_10",
                   lambda: len(get_review_recommendations()) == 10)
        self._gate("recommendations_has_escalate_to_manual",
                   lambda: "ESCALATE_TO_MANUAL_REVIEW" in get_review_recommendations())

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
            "review_only": True,
            "human_approval_only": True,
            "rollback_review_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
            "no_auto_approval": True,
            "no_auto_rollback": True,
            "schema_version": "195",
        }


def run_release_gate() -> Dict[str, Any]:
    """Run release gate and return result dict."""
    gate = StrategyReviewReleaseGate()
    return gate.run()


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Strategy Review Release Gate v1.9.5: {result['passed_count']}/{result['total']} passed")
    if result["failed_count"] > 0:
        for r in result["results"]:
            if not r["passed"]:
                print(f"  FAIL: {r['name']} — {r['error']}")
    else:
        print("PASS all gates")
