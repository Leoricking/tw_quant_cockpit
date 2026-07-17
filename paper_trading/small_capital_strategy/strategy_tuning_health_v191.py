"""
paper_trading/small_capital_strategy/strategy_tuning_health_v191.py
Health check for Paper Strategy Rule Tuning & Guardrail Lab v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List


class StrategyTuningHealthCheck:
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

    def run(self) -> "RuleTuningHealthSummary":
        from paper_trading.small_capital_strategy.strategy_tuning_models_v191 import RuleTuningHealthSummary
        self._checks = []

        # ── version (6) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_version_v191 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_rule_categories, get_guardrail_triggers,
            get_tuning_recommendations, get_approval_states,
            get_forbidden_tuning_actions, get_allowed_tuning_actions,
            get_hard_block_conditions,
        )
        self._check("version_is_191", lambda: VERSION == "1.9.1")
        self._check("release_name_correct",
                    lambda: RELEASE_NAME == "Paper Strategy Rule Tuning & Guardrail Lab")
        self._check("schema_version_191", lambda: SCHEMA_VERSION == "191")
        self._check("verify_version_returns_true", lambda: verify_version() is True)
        self._check("is_known_release_v191",
                    lambda: is_known_release("Paper Strategy Rule Tuning & Guardrail Lab v1.9.1"))
        self._check("version_info_paper_only", lambda: get_version_info()["paper_only"] is True)

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_safety_v191 import (
            SAFETY_FLAGS, run_safety_audit, is_safe_output_path, is_forbidden_action,
            is_allowed_action, validate_tuning_action,
            FORBIDDEN_TUNING_ACTIONS, ALLOWED_TUNING_ACTIONS,
            HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_flag_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_flag_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_flag_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_flag_tuning_only", lambda: SAFETY_FLAGS["tuning_only"] is True)
        self._check("safety_flag_guardrail_only", lambda: SAFETY_FLAGS["guardrail_only"] is True)
        self._check("safety_flag_not_investment_advice",
                    lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._check("safety_flag_no_production_mutation",
                    lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._check("safety_flag_broker_execution_false",
                    lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_flag_production_strategy_mutation_false",
                    lambda: SAFETY_FLAGS["production_strategy_mutation"] is False)

        # ── rule categories (3) ───────────────────────────────────────────────
        self._check("rule_categories_count_14", lambda: len(get_rule_categories()) == 14)
        self._check("rule_categories_has_abc_buy_point",
                    lambda: "ABC_BUY_POINT" in get_rule_categories())
        self._check("rule_categories_has_position_sizing",
                    lambda: "POSITION_SIZING" in get_rule_categories())

        # ── guardrail triggers (3) ────────────────────────────────────────────
        self._check("guardrail_triggers_count_16",
                    lambda: len(get_guardrail_triggers()) == 16)
        self._check("guardrail_triggers_has_expectancy_negative",
                    lambda: "EXPECTANCY_NEGATIVE" in get_guardrail_triggers())
        self._check("guardrail_triggers_has_win_rate_low",
                    lambda: "WIN_RATE_TOO_LOW" in get_guardrail_triggers())

        # ── tuning recommendations (3) ────────────────────────────────────────
        self._check("tuning_recommendations_count_15",
                    lambda: len(get_tuning_recommendations()) == 15)
        self._check("tuning_recommendations_has_keep_rule",
                    lambda: "KEEP_RULE" in get_tuning_recommendations())
        self._check("tuning_recommendations_has_disable_setup",
                    lambda: "DISABLE_SETUP" in get_tuning_recommendations())

        # ── approval states (2) ───────────────────────────────────────────────
        self._check("approval_states_count_6", lambda: len(get_approval_states()) == 6)
        self._check("approval_states_has_proposed",
                    lambda: "PROPOSED" in get_approval_states())

        # ── models (22) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_models_v191 import (
            StrategyRuleTuningInput, StrategyRuleTuningResult,
            StrategyRuleCandidate, StrategyRuleAdjustment,
            StrategyGuardrail, GuardrailTrigger, GuardrailSeverity, GuardrailAction,
            RuleTuningEvidence, RuleTuningFinding, RuleTuningRecommendation,
            RuleTuningBacktestSnapshot, RuleTuningReviewChecklist,
            RuleTuningApprovalState, RuleTuningExportManifest,
            RuleTuningEvidencePack, RuleTuningAuditTrail, RuleTuningDashboard,
            RuleTuningHealthSummary as RHS, RuleTuningValidationResult,
            get_all_model_names,
        )
        self._check("model_tuning_input_paper_only",
                    lambda: StrategyRuleTuningInput().paper_only is True)
        self._check("model_tuning_result_no_real_orders",
                    lambda: StrategyRuleTuningResult().no_real_orders is True)
        self._check("model_rule_candidate_tuning_only",
                    lambda: StrategyRuleCandidate().tuning_only is True)
        self._check("model_rule_adjustment_guardrail_only",
                    lambda: StrategyRuleAdjustment().guardrail_only is True)
        self._check("model_guardrail_no_production_mutation",
                    lambda: StrategyGuardrail().no_production_strategy_mutation is True)
        self._check("model_guardrail_trigger_paper_only",
                    lambda: GuardrailTrigger().paper_only is True)
        self._check("model_guardrail_severity_no_broker",
                    lambda: GuardrailSeverity().no_broker is True)
        self._check("model_guardrail_action_not_investment_advice",
                    lambda: GuardrailAction().not_investment_advice is True)
        self._check("model_evidence_production_blocked",
                    lambda: RuleTuningEvidence().production_trading_blocked is True)
        self._check("model_finding_demo_only",
                    lambda: RuleTuningFinding().demo_only is True)
        self._check("model_recommendation_not_for_production",
                    lambda: RuleTuningRecommendation().not_for_production is True)
        self._check("model_backtest_snapshot_no_margin",
                    lambda: RuleTuningBacktestSnapshot().no_margin is True)
        self._check("model_review_checklist_no_leverage",
                    lambda: RuleTuningReviewChecklist().no_leverage is True)
        self._check("model_approval_state_simulate_only",
                    lambda: RuleTuningApprovalState().simulate_only is True)
        self._check("model_export_manifest_validation_only",
                    lambda: RuleTuningExportManifest().validation_only is True)
        self._check("model_evidence_pack_report_only",
                    lambda: RuleTuningEvidencePack().report_only is True)
        self._check("model_audit_trail_audit_only",
                    lambda: RuleTuningAuditTrail().audit_only is True)
        self._check("model_dashboard_review_only",
                    lambda: RuleTuningDashboard().review_only is True)
        self._check("model_health_summary_research_only",
                    lambda: RHS().research_only is True)
        self._check("model_validation_result_tuning_only",
                    lambda: RuleTuningValidationResult().tuning_only is True)
        self._check("models_count_20", lambda: len(get_all_model_names()) == 20)
        self._check("models_schema_191",
                    lambda: StrategyRuleTuningInput().schema_version == "191")

        # ── engine (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_engine_v191 import (
            run_tuning_review, build_rule_candidate, build_rule_adjustment,
            build_guardrail, evaluate_guardrail_triggers,
            build_tuning_recommendation, build_backtest_snapshot,
            build_dashboard, build_evidence_pack, build_audit_trail,
            build_export_manifest, get_engine_info,
            validate_rule_category, validate_guardrail_trigger,
            validate_tuning_recommendation, validate_approval_state,
        )
        self._check("engine_tuning_blocked_missing_perf",
                    lambda: run_tuning_review("t1", "", "j1")["blocked"] is True)
        self._check("engine_tuning_blocked_missing_journal",
                    lambda: run_tuning_review("t2", "p1", "")["blocked"] is True)
        self._check("engine_tuning_passes_with_sources",
                    lambda: run_tuning_review("t3", "p1", "j1")["blocked"] is False)
        self._check("engine_rule_candidate_paper_only",
                    lambda: build_rule_candidate("r1", "A_PULLBACK", "ABC_BUY_POINT",
                                                 0.6, 0.3, 0.1)["paper_only"] is True)
        self._check("engine_adjustment_blocked_no_evidence",
                    lambda: build_rule_adjustment("a1", "r1", "ABC_BUY_POINT",
                                                  "TIGHTEN_RULE", "test", [])["blocked"] is True)
        self._check("engine_adjustment_passes_with_evidence",
                    lambda: build_rule_adjustment("a2", "r1", "ABC_BUY_POINT",
                                                  "TIGHTEN_RULE", "test", ["e1"])["blocked"] is False)
        self._check("engine_guardrail_blocked_no_trigger",
                    lambda: build_guardrail("g1", "test", "", "WARNING", "LOG_ONLY")["blocked"] is True)
        self._check("engine_guardrail_passes_with_trigger",
                    lambda: build_guardrail("g2", "test", "EXPECTANCY_NEGATIVE",
                                            "WARNING", "LOG_ONLY")["blocked"] is False)
        self._check("engine_evaluate_triggers_returns_list",
                    lambda: isinstance(evaluate_guardrail_triggers({"expectancy_r": -0.3}), list))
        self._check("engine_validate_rule_category",
                    lambda: validate_rule_category("ABC_BUY_POINT") is True)

        # ── report (5) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_report_v191 import (
            export_tuning_summary_as_json, export_guardrail_report_as_json,
            export_recommendations_as_json, export_dashboard_as_json,
            get_report_info,
        )
        self._check("report_tuning_summary_json_paper_only",
                    lambda: '"paper_only": true' in export_tuning_summary_as_json({}))
        self._check("report_guardrail_json_no_real_orders",
                    lambda: '"no_real_orders": true' in export_guardrail_report_as_json([]))
        self._check("report_recommendations_json_schema",
                    lambda: '"schema_version"' in export_recommendations_as_json([]))
        self._check("report_dashboard_json_tuning_only",
                    lambda: '"tuning_only": true' in export_dashboard_as_json({}))
        self._check("report_info_paper_only",
                    lambda: get_report_info()["paper_only"] is True)

        # ── scenarios (3) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_scenarios_v191 import (
            get_all_scenarios, get_scenarios_by_type, get_scenario_by_id,
        )
        self._check("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._check("scenarios_all_paper_only",
                    lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._check("scenarios_have_complete_tuning_review",
                    lambda: len(get_scenarios_by_type("complete_rule_tuning_review")) >= 1)

        # ── fixtures (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_fixtures_v191 import (
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
        self._check("safety_tuning_only_all_fixtures",
                    lambda: all(f["tuning_only"] is True for f in get_all_fixtures()))
        self._check("safety_safe_export_path",
                    lambda: is_safe_output_path("reports/") is True)
        self._check("safety_unsafe_export_blocked",
                    lambda: is_safe_output_path("production_strategy/") is False)

        # ── hard block conditions (3) ─────────────────────────────────────────
        self._check("hard_block_conditions_count_17",
                    lambda: len(HARD_BLOCK_CONDITIONS) == 17)
        self._check("hard_block_has_real_order",
                    lambda: "real_order_requested" in HARD_BLOCK_CONDITIONS)
        self._check("hard_block_has_production_mutation",
                    lambda: "production_strategy_mutation_attempted" in HARD_BLOCK_CONDITIONS)

        # ── allowed / forbidden actions (4) ───────────────────────────────────
        self._check("allowed_actions_count_16",
                    lambda: len(ALLOWED_TUNING_ACTIONS) == 16)
        self._check("forbidden_actions_count_9",
                    lambda: len(FORBIDDEN_TUNING_ACTIONS) == 9)
        self._check("allowed_action_tune",
                    lambda: is_allowed_action("TUNE") is True)
        self._check("forbidden_action_buy",
                    lambda: is_forbidden_action("BUY") is True)

        # ── GUI panel check (1) ───────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._check("gui_panel_version_191", lambda: PANEL_VERSION == "1.9.1")

        # ── backward compat (2) ───────────────────────────────────────────────
        self._check("backward_compat_v190_known",
                    lambda: is_known_release(
                        "Paper Trading Performance Review & Strategy Improvement Lab v1.9.0"))
        self._check("backward_compat_v189_known",
                    lambda: is_known_release("Paper Decision Journal & Review Loop v1.8.9"))

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)
        return RuleTuningHealthSummary(
            status="PASS" if failed == 0 else "FAIL",
            passed=passed,
            failed=failed,
            total=total,
            checks=list(self._checks),
            all_passed=(failed == 0),
        )


def run_health_check() -> "RuleTuningHealthSummary":
    """Run the strategy tuning health check and return summary."""
    return StrategyTuningHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Strategy Tuning Health v1.9.1: {result.status} ({result.passed}/{result.total})")
    if result.failed:
        for c in result.checks:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
