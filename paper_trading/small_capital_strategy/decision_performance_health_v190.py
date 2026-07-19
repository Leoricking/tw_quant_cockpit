"""
paper_trading/small_capital_strategy/decision_performance_health_v190.py
Health check for Paper Trading Performance Review & Strategy Improvement Lab v1.9.0.
[!] Research Only. Paper Only. Performance Review Only. Strategy Improvement Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List


class DecisionPerformanceHealthCheck:
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

    def run(self) -> "PerformanceHealthSummary":
        from paper_trading.small_capital_strategy.decision_performance_models_v190 import PerformanceHealthSummary
        self._checks = []

        # ── version (6) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_version_v190 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_setup_types, get_improvement_suggestions,
            get_quality_grades, get_performance_dimensions,
            get_forbidden_performance_actions, get_allowed_performance_actions,
            get_hard_block_conditions,
        )
        self._check("version_is_190", lambda: VERSION == "1.9.0")
        self._check("release_name_correct",
                    lambda: RELEASE_NAME == "Paper Trading Performance Review & Strategy Improvement Lab")
        self._check("schema_version_190", lambda: SCHEMA_VERSION == "190")
        self._check("verify_version_returns_true", lambda: verify_version() is True)
        self._check("is_known_release_v190",
                    lambda: is_known_release(
                        "Paper Trading Performance Review & Strategy Improvement Lab v1.9.0"))
        self._check("version_info_paper_only", lambda: get_version_info()["paper_only"] is True)

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_safety_v190 import (
            SAFETY_FLAGS, run_safety_audit, is_safe_output_path, is_forbidden_action,
            is_allowed_action, validate_performance_action,
            FORBIDDEN_PERFORMANCE_ACTIONS, ALLOWED_PERFORMANCE_ACTIONS,
            HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_flag_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_flag_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_flag_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_flag_performance_review_only",
                    lambda: SAFETY_FLAGS["performance_review_only"] is True)
        self._check("safety_flag_strategy_improvement_only",
                    lambda: SAFETY_FLAGS["strategy_improvement_only"] is True)
        self._check("safety_flag_not_investment_advice",
                    lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._check("safety_flag_broker_execution_false",
                    lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_flag_real_order_false",
                    lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("safety_forbidden_buy", lambda: is_forbidden_action("BUY") is True)

        # ── setup types (3) ───────────────────────────────────────────────────
        self._check("setup_types_count_11", lambda: len(get_setup_types()) == 11)
        self._check("setup_types_has_a_pullback",
                    lambda: "A_10MA_PULLBACK" in get_setup_types())
        self._check("setup_types_has_b_breakout",
                    lambda: "B_BASE_BREAKOUT" in get_setup_types())

        # ── improvement suggestions (3) ───────────────────────────────────────
        self._check("improvement_suggestions_count_13",
                    lambda: len(get_improvement_suggestions()) == 13)
        self._check("improvement_suggestions_has_keep_rule",
                    lambda: "KEEP_RULE" in get_improvement_suggestions())
        self._check("improvement_suggestions_has_block_setup",
                    lambda: "BLOCK_SETUP" in get_improvement_suggestions())

        # ── quality grades (3) ────────────────────────────────────────────────
        self._check("quality_grades_count_6", lambda: len(get_quality_grades()) == 6)
        self._check("quality_grades_has_excellent",
                    lambda: "EXCELLENT" in get_quality_grades())
        self._check("quality_grades_has_invalid",
                    lambda: "INVALID" in get_quality_grades())

        # ── performance dimensions (3) ────────────────────────────────────────
        self._check("performance_dimensions_count_26",
                    lambda: len(get_performance_dimensions()) == 26)
        self._check("performance_dimensions_has_win_rate",
                    lambda: "win_rate" in get_performance_dimensions())
        self._check("performance_dimensions_has_expectancy",
                    lambda: "expectancy_r" in get_performance_dimensions())

        # ── models (22) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_models_v190 import (
            PerformanceReviewInput, PerformanceReviewResult, StrategyPerformanceSummary,
            SetupPerformanceSummary, ActionPerformanceSummary, MistakePerformanceSummary,
            RMultipleSummary, DrawdownReviewSummary, WinLossSummary, ExpectancySummary,
            RiskRewardSummary, StrategyRuleFinding, StrategyImprovementSuggestion,
            StrategyAdjustmentPlan, PerformanceReviewDashboard,
            PerformanceReviewExportManifest, PerformanceReviewEvidencePack,
            PerformanceReviewAuditTrail, PerformanceHealthSummary as PHS,
            PerformanceValidationResult, get_all_model_names,
        )
        self._check("model_performance_review_input",
                    lambda: PerformanceReviewInput().paper_only is True)
        self._check("model_performance_review_result",
                    lambda: PerformanceReviewResult().no_real_orders is True)
        self._check("model_strategy_performance_summary",
                    lambda: StrategyPerformanceSummary().performance_review_only is True)
        self._check("model_setup_performance_summary",
                    lambda: SetupPerformanceSummary().schema_version == "190")
        self._check("model_action_performance_summary",
                    lambda: ActionPerformanceSummary().not_investment_advice is True)
        self._check("model_mistake_performance_summary",
                    lambda: MistakePerformanceSummary().audit_only is True)
        self._check("model_r_multiple_summary",
                    lambda: RMultipleSummary().no_broker is True)
        self._check("model_drawdown_review_summary",
                    lambda: DrawdownReviewSummary().production_trading_blocked is True)
        self._check("model_win_loss_summary",
                    lambda: WinLossSummary().strategy_improvement_only is True)
        self._check("model_expectancy_summary",
                    lambda: ExpectancySummary().review_only is True)
        self._check("model_risk_reward_summary",
                    lambda: RiskRewardSummary().report_only is True)
        self._check("model_strategy_rule_finding",
                    lambda: StrategyRuleFinding().demo_only is True)
        self._check("model_strategy_improvement_suggestion",
                    lambda: StrategyImprovementSuggestion().not_for_production is True)
        self._check("model_strategy_adjustment_plan",
                    lambda: StrategyAdjustmentPlan().no_margin is True)
        self._check("model_performance_review_dashboard",
                    lambda: PerformanceReviewDashboard().no_leverage is True)
        self._check("model_performance_review_export_manifest",
                    lambda: PerformanceReviewExportManifest().simulate_only is True)
        self._check("model_performance_review_evidence_pack",
                    lambda: PerformanceReviewEvidencePack().validation_only is True)
        self._check("model_performance_review_audit_trail",
                    lambda: PerformanceReviewAuditTrail().paper_only is True)
        self._check("model_performance_health_summary",
                    lambda: PHS().research_only is True)
        self._check("model_performance_validation_result",
                    lambda: PerformanceValidationResult().performance_review_only is True)
        self._check("models_count_20", lambda: len(get_all_model_names()) == 20)
        self._check("models_safety_defaults_schema",
                    lambda: PerformanceReviewInput().schema_version == "190")

        # ── engine (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_engine_v190 import (
            run_performance_review, build_strategy_summary, build_setup_summary,
            build_r_multiple_summary, build_drawdown_summary, build_expectancy_summary,
            build_improvement_suggestion, build_dashboard, build_evidence_pack,
            build_audit_trail, build_export_manifest, get_engine_info,
            validate_setup_type, validate_improvement_suggestion,
            validate_quality_grade, validate_performance_dimension,
        )
        self._check("engine_run_review_blocked_on_empty",
                    lambda: run_performance_review("r1", [])["blocked"] is True)
        self._check("engine_run_review_passes_with_entries",
                    lambda: run_performance_review("r2", ["e1", "e2"])["blocked"] is False)
        self._check("engine_build_strategy_summary_paper_only",
                    lambda: build_strategy_summary([])["paper_only"] is True)
        self._check("engine_build_r_multiple_empty",
                    lambda: build_r_multiple_summary([])["total_trades"] == 0)
        self._check("engine_build_r_multiple_healthy",
                    lambda: build_r_multiple_summary([1.5, 1.2, -1.0, 2.0, -0.8])["r_multiple_healthy"] is True)
        self._check("engine_build_drawdown_within_budget",
                    lambda: build_drawdown_summary([1.0, -0.5, 0.8, -1.0])["drawdown_within_budget"] is True)
        self._check("engine_build_expectancy_positive",
                    lambda: build_expectancy_summary(0.6, 1.5, 1.0)["expectancy_positive"] is True)
        self._check("engine_validate_setup_type",
                    lambda: validate_setup_type("A_10MA_PULLBACK") is True)
        self._check("engine_validate_improvement_suggestion",
                    lambda: validate_improvement_suggestion("KEEP_RULE") is True)
        self._check("engine_validate_performance_dimension",
                    lambda: validate_performance_dimension("win_rate") is True)

        # ── report (5) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_report_v190 import (
            export_strategy_summary_as_json, export_improvement_report_as_json,
            export_dashboard_as_json, get_report_info,
        )
        self._check("report_strategy_summary_json_has_paper_only",
                    lambda: '"paper_only": true' in export_strategy_summary_as_json({"win_rate": 0.5}))
        self._check("report_improvement_report_json",
                    lambda: '"report_type"' in export_improvement_report_as_json([]))
        self._check("report_dashboard_json",
                    lambda: '"report_type"' in export_dashboard_as_json({}))
        self._check("report_info_paper_only",
                    lambda: get_report_info()["paper_only"] is True)
        self._check("report_info_functions_list",
                    lambda: len(get_report_info()["functions"]) >= 10)

        # ── scenarios (3) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_scenarios_v190 import (
            get_all_scenarios, get_scenarios_by_type, get_scenario_by_id,
        )
        self._check("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._check("scenarios_all_paper_only",
                    lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._check("scenarios_have_complete_review",
                    lambda: len(get_scenarios_by_type("complete_performance_review")) >= 1)

        # ── fixtures (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_performance_fixtures_v190 import (
            get_all_fixtures, get_fixture_by_id,
        )
        self._check("fixtures_count_75", lambda: len(get_all_fixtures()) == 75)
        self._check("fixtures_all_paper_only",
                    lambda: all(f["paper_only"] is True for f in get_all_fixtures()))
        self._check("fixtures_all_no_real_orders",
                    lambda: all(f["no_real_orders"] is True for f in get_all_fixtures()))

        # ── safety extras (4) ─────────────────────────────────────────────────
        self._check("safety_no_broker_all_fixtures",
                    lambda: all(f["no_broker"] is True for f in get_all_fixtures()))
        self._check("safety_performance_review_only_all_fixtures",
                    lambda: all(f["performance_review_only"] is True for f in get_all_fixtures()))
        self._check("safety_safe_export_path",
                    lambda: is_safe_output_path("reports/") is True)
        self._check("safety_unsafe_export_blocked",
                    lambda: is_safe_output_path("production_db/reports/") is False)

        # ── hard block conditions (3) ─────────────────────────────────────────
        self._check("hard_block_conditions_count_14",
                    lambda: len(HARD_BLOCK_CONDITIONS) == 14)
        self._check("hard_block_has_real_order",
                    lambda: "real_order_requested" in HARD_BLOCK_CONDITIONS)
        self._check("hard_block_has_unsafe_export",
                    lambda: "unsafe_export_path" in HARD_BLOCK_CONDITIONS)

        # ── allowed / forbidden actions (4) ───────────────────────────────────
        self._check("allowed_actions_count_16",
                    lambda: len(ALLOWED_PERFORMANCE_ACTIONS) == 16)
        self._check("forbidden_actions_count_9",
                    lambda: len(FORBIDDEN_PERFORMANCE_ACTIONS) == 9)
        self._check("allowed_action_review",
                    lambda: is_allowed_action("REVIEW") is True)
        self._check("forbidden_action_buy",
                    lambda: is_forbidden_action("BUY") is True)

        # ── GUI panel check (1) ───────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._check("gui_panel_version_190", lambda: PANEL_VERSION in ("1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10"))

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)
        return PerformanceHealthSummary(
            status="PASS" if failed == 0 else "FAIL",
            passed=passed,
            failed=failed,
            total=total,
            checks=list(self._checks),
            all_passed=(failed == 0),
        )


def run_health_check() -> "PerformanceHealthSummary":
    """Run the performance health check and return summary."""
    return DecisionPerformanceHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Decision Performance Health v1.9.0: {result.status} ({result.passed}/{result.total})")
    if result.failed:
        for c in result.checks:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
