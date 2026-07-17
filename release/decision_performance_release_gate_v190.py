"""
release/decision_performance_release_gate_v190.py
Release gate for Paper Trading Performance Review & Strategy Improvement Lab v1.9.0.
[!] Research Only. Paper Only. Performance Review Only. Strategy Improvement Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List


class DecisionPerformanceReleaseGate:
    VERSION = "1.9.0"
    RELEASE_NAME = "Paper Trading Performance Review & Strategy Improvement Lab"
    MIN_SCENARIOS = 75
    MIN_FIXTURES = 75
    MIN_CLI = 18
    MIN_HEALTH_CHECKS = 60
    BASELINE_TESTS = 26157
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
        from paper_trading.small_capital_strategy.decision_performance_version_v190 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version,
            get_setup_types, get_improvement_suggestions, get_quality_grades,
            get_performance_dimensions, get_forbidden_performance_actions,
            get_allowed_performance_actions, get_hard_block_conditions,
            is_known_release,
        )
        self._gate("version_190", lambda: VERSION == "1.9.0")
        self._gate("release_name_performance_review",
                   lambda: RELEASE_NAME == "Paper Trading Performance Review & Strategy Improvement Lab")
        self._gate("schema_190", lambda: SCHEMA_VERSION == "190")
        self._gate("verify_version_true", lambda: verify_version() is True)
        self._gate("setup_types_count_11", lambda: len(get_setup_types()) == 11)
        self._gate("improvement_suggestions_count_13",
                   lambda: len(get_improvement_suggestions()) == 13)
        self._gate("quality_grades_count_6", lambda: len(get_quality_grades()) == 6)
        self._gate("performance_dimensions_count_26",
                   lambda: len(get_performance_dimensions()) == 26)

        # ── safety (12) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_safety_v190 import (
            SAFETY_FLAGS, run_safety_audit, is_forbidden_action, is_allowed_action,
            is_safe_output_path, FORBIDDEN_PERFORMANCE_ACTIONS,
            ALLOWED_PERFORMANCE_ACTIONS, HARD_BLOCK_CONDITIONS,
            get_safety_flags, get_hard_block_conditions as s_get_hbc,
        )
        self._gate("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._gate("safety_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._gate("safety_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._gate("safety_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._gate("safety_performance_review_only",
                   lambda: SAFETY_FLAGS["performance_review_only"] is True)
        self._gate("safety_strategy_improvement_only",
                   lambda: SAFETY_FLAGS["strategy_improvement_only"] is True)
        self._gate("safety_not_investment_advice",
                   lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._gate("safety_broker_execution_false",
                   lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._gate("safety_real_order_false",
                   lambda: SAFETY_FLAGS["real_order"] is False)
        self._gate("safety_forbidden_buy", lambda: is_forbidden_action("BUY") is True)
        self._gate("safety_forbidden_actions_count_9",
                   lambda: len(FORBIDDEN_PERFORMANCE_ACTIONS) == 9)
        self._gate("safety_hard_block_count_14",
                   lambda: len(HARD_BLOCK_CONDITIONS) == 14)

        # ── models (22) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_models_v190 import (
            PerformanceReviewInput, PerformanceReviewResult, StrategyPerformanceSummary,
            SetupPerformanceSummary, ActionPerformanceSummary, MistakePerformanceSummary,
            RMultipleSummary, DrawdownReviewSummary, WinLossSummary, ExpectancySummary,
            RiskRewardSummary, StrategyRuleFinding, StrategyImprovementSuggestion,
            StrategyAdjustmentPlan, PerformanceReviewDashboard,
            PerformanceReviewExportManifest, PerformanceReviewEvidencePack,
            PerformanceReviewAuditTrail, PerformanceHealthSummary,
            PerformanceValidationResult, get_all_model_names,
        )
        self._gate("models_count_20", lambda: len(get_all_model_names()) == 20)
        self._gate("model_review_input_paper_only",
                   lambda: PerformanceReviewInput().paper_only is True)
        self._gate("model_review_result_no_real_orders",
                   lambda: PerformanceReviewResult().no_real_orders is True)
        self._gate("model_strategy_summary_performance_review_only",
                   lambda: StrategyPerformanceSummary().performance_review_only is True)
        self._gate("model_setup_summary_schema_190",
                   lambda: SetupPerformanceSummary().schema_version == "190")
        self._gate("model_r_multiple_no_broker",
                   lambda: RMultipleSummary().no_broker is True)
        self._gate("model_drawdown_production_blocked",
                   lambda: DrawdownReviewSummary().production_trading_blocked is True)
        self._gate("model_expectancy_strategy_improvement_only",
                   lambda: ExpectancySummary().strategy_improvement_only is True)
        self._gate("model_suggestion_not_for_production",
                   lambda: StrategyImprovementSuggestion().not_for_production is True)
        self._gate("model_dashboard_no_margin",
                   lambda: PerformanceReviewDashboard().no_margin is True)
        self._gate("model_evidence_pack_validation_only",
                   lambda: PerformanceReviewEvidencePack().validation_only is True)
        self._gate("model_audit_trail_paper_only",
                   lambda: PerformanceReviewAuditTrail().paper_only is True)
        self._gate("model_health_summary_research_only",
                   lambda: PerformanceHealthSummary().research_only is True)
        self._gate("model_validation_result_performance_review_only",
                   lambda: PerformanceValidationResult().performance_review_only is True)
        self._gate("model_finding_demo_only",
                   lambda: StrategyRuleFinding().demo_only is True)
        self._gate("model_adjustment_plan_no_leverage",
                   lambda: StrategyAdjustmentPlan().no_leverage is True)
        self._gate("model_export_manifest_simulate_only",
                   lambda: PerformanceReviewExportManifest().simulate_only is True)
        self._gate("model_win_loss_strategy_improvement_only",
                   lambda: WinLossSummary().strategy_improvement_only is True)
        self._gate("model_risk_reward_report_only",
                   lambda: RiskRewardSummary().report_only is True)
        self._gate("model_action_summary_not_investment_advice",
                   lambda: ActionPerformanceSummary().not_investment_advice is True)
        self._gate("model_mistake_summary_audit_only",
                   lambda: MistakePerformanceSummary().audit_only is True)

        # ── engine (14) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_engine_v190 import (
            run_performance_review, build_strategy_summary, build_setup_summary,
            build_r_multiple_summary, build_drawdown_summary, build_expectancy_summary,
            build_improvement_suggestion, build_dashboard, build_evidence_pack,
            build_audit_trail, build_export_manifest, get_engine_info,
            validate_setup_type, validate_improvement_suggestion,
            validate_quality_grade, validate_performance_dimension,
        )
        self._gate("engine_review_blocked_empty",
                   lambda: run_performance_review("r1", [])["blocked"] is True)
        self._gate("engine_review_passes_with_entries",
                   lambda: run_performance_review("r2", ["e1"])["blocked"] is False)
        self._gate("engine_strategy_summary_paper_only",
                   lambda: build_strategy_summary([])["paper_only"] is True)
        self._gate("engine_r_multiple_empty_zero",
                   lambda: build_r_multiple_summary([])["total_trades"] == 0)
        self._gate("engine_r_multiple_healthy",
                   lambda: build_r_multiple_summary([1.5, 1.2, -1.0])["r_multiple_healthy"] is True)
        self._gate("engine_drawdown_within_budget",
                   lambda: build_drawdown_summary([1.0, -0.5, 0.8])["drawdown_within_budget"] is True)
        self._gate("engine_expectancy_positive",
                   lambda: build_expectancy_summary(0.6, 1.5, 1.0)["expectancy_positive"] is True)
        self._gate("engine_expectancy_negative",
                   lambda: build_expectancy_summary(0.3, 1.0, 2.0)["expectancy_positive"] is False)
        self._gate("engine_suggestion_blocked_no_evidence",
                   lambda: build_improvement_suggestion("s1", "TIGHTEN_RULE", "A_PULLBACK",
                                                        "test", [])["blocked"] is True)
        self._gate("engine_suggestion_passes_with_evidence",
                   lambda: build_improvement_suggestion("s2", "TIGHTEN_RULE", "A_PULLBACK",
                                                        "test", ["e1"])["blocked"] is False)
        self._gate("engine_setup_type_valid",
                   lambda: validate_setup_type("B_BASE_BREAKOUT") is True)
        self._gate("engine_setup_type_invalid",
                   lambda: validate_setup_type("REAL_TRADE") is False)
        self._gate("engine_export_manifest_safe_path",
                   lambda: build_export_manifest("m1", "period")["safe_path"] is True)
        self._gate("engine_export_manifest_unsafe_redirected",
                   lambda: build_export_manifest("m2", "period",
                                                 "production_db/")["export_path"] == "reports/")

        # ── report (6) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_report_v190 import (
            export_strategy_summary_as_json, export_improvement_report_as_json,
            export_improvement_report_as_markdown, export_dashboard_as_json,
            export_evidence_pack_as_json, get_report_info,
        )
        self._gate("report_strategy_summary_paper_only",
                   lambda: '"paper_only": true' in export_strategy_summary_as_json({}))
        self._gate("report_improvement_json_no_real_orders",
                   lambda: '"no_real_orders": true' in export_improvement_report_as_json([]))
        self._gate("report_improvement_markdown_header",
                   lambda: "Strategy Improvement Report" in export_improvement_report_as_markdown([]))
        self._gate("report_dashboard_json_schema",
                   lambda: '"schema_version"' in export_dashboard_as_json({}))
        self._gate("report_evidence_pack_json",
                   lambda: '"performance_review_only": true' in export_evidence_pack_as_json({}))
        self._gate("report_info_paper_only",
                   lambda: get_report_info()["paper_only"] is True)

        # ── scenarios (5) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_scenarios_v190 import (
            get_all_scenarios, get_scenarios_by_type, get_scenario_by_id,
        )
        self._gate("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._gate("scenarios_min_75",
                   lambda: len(get_all_scenarios()) >= self.MIN_SCENARIOS)
        self._gate("scenarios_all_paper_only",
                   lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._gate("scenarios_no_real_orders",
                   lambda: all(s["no_real_orders"] is True for s in get_all_scenarios()))
        self._gate("scenarios_no_forbidden_action_words",
                   lambda: all(
                       not any(word in s.get("description", "").upper()
                               for word in ["BUY_SIGNAL", "SUBMIT_ORDER", "BROKER"])
                       for s in get_all_scenarios()
                   ))

        # ── fixtures (5) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_fixtures_v190 import (
            get_all_fixtures, get_fixture_by_id, get_fixtures_by_grade,
        )
        self._gate("fixtures_count_75", lambda: len(get_all_fixtures()) == 75)
        self._gate("fixtures_min_75",
                   lambda: len(get_all_fixtures()) >= self.MIN_FIXTURES)
        self._gate("fixtures_all_paper_only",
                   lambda: all(f["paper_only"] is True for f in get_all_fixtures()))
        self._gate("fixtures_all_no_real_orders",
                   lambda: all(f["no_real_orders"] is True for f in get_all_fixtures()))
        self._gate("fixtures_all_performance_review_only",
                   lambda: all(f["performance_review_only"] is True for f in get_all_fixtures()))

        # ── health (3) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_health_v190 import (
            run_health_check,
        )
        h = run_health_check()
        self._gate("health_all_passed", lambda: h.all_passed is True)
        self._gate("health_status_pass", lambda: h.status == "PASS")
        self._gate("health_checks_count_ge_60", lambda: h.total >= self.MIN_HEALTH_CHECKS)

        # ── backward compatibility (2) ────────────────────────────────────────
        self._gate("backward_compat_v189_known",
                   lambda: is_known_release("Paper Decision Journal & Review Loop v1.8.9"))
        self._gate("backward_compat_v188_known",
                   lambda: is_known_release("Paper Decision Workflow Runner v1.8.8"))

        # ── no forbidden words in version module (1) ──────────────────────────
        self._gate("version_module_no_forbidden_words",
                   lambda: not any(
                       word in str(get_performance_dimensions()).upper()
                       for word in ["BUY_SIGNAL", "SUBMIT_ORDER", "BROKER_ORDER"]
                   ))

        # ── GUI panel version (1) ─────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._gate("gui_panel_version_190", lambda: PANEL_VERSION in ("1.9.0", "1.9.1"))

        # ── CLI check (1) ────────────────────────────────────────────────────
        from cli.command_registry import get_commands_by_group
        dp_cmds = [c for c in get_commands_by_group("decision_performance")
                   if c.introduced_in == "1.9.0"]
        self._gate("cli_decision_performance_count_18",
                   lambda: len(dp_cmds) >= self.MIN_CLI)

        passed = sum(1 for r in self._results if r["passed"])
        failed = sum(1 for r in self._results if not r["passed"])
        total = len(self._results)
        return {
            "version": self.VERSION,
            "release_name": self.RELEASE_NAME,
            "gate_passed": failed == 0,
            "status": "PASS" if failed == 0 else "FAIL",
            "passed": passed,
            "failed": failed,
            "total": total,
            "min_scenarios": self.MIN_SCENARIOS,
            "min_fixtures": self.MIN_FIXTURES,
            "min_cli": self.MIN_CLI,
            "baseline_tests": self.BASELINE_TESTS,
            "min_new_tests": self.MIN_NEW_TESTS,
            "results": self._results,
            "paper_only": True,
            "research_only": True,
            "performance_review_only": True,
            "strategy_improvement_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
            "production_trading_blocked": True,
            "journal_only": False,
            "review_only": True,
            "audit_only": True,
        }


def run_release_gate() -> Dict[str, Any]:
    """Run the decision performance release gate and return result dict."""
    return DecisionPerformanceReleaseGate().run()


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Decision Performance Release Gate v1.9.0: {result['status']} "
          f"({result['passed']}/{result['total']})")
    if result["failed"]:
        for r in result["results"]:
            if not r["passed"]:
                print(f"  [FAIL] {r['name']}: {r.get('error', '')}")
