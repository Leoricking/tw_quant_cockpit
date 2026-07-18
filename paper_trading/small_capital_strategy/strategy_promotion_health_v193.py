"""
paper_trading/small_capital_strategy/strategy_promotion_health_v193.py
Health check for Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3.
[!] Research Only. Paper Only. Promotion Package Only. Rollback Plan Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List


class StrategyPromotionHealthCheck:
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

    def run(self) -> "PromotionHealthSummary":
        from paper_trading.small_capital_strategy.strategy_promotion_models_v193 import PromotionHealthSummary
        self._checks = []

        # ── version (6) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_version_v193 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_promotion_approval_states, get_promotion_recommendations,
            get_rollback_triggers, get_forbidden_promotion_actions,
            get_allowed_promotion_actions, get_hard_block_conditions,
        )
        self._check("version_is_193", lambda: VERSION == "1.9.3")
        self._check("release_name_correct",
                    lambda: RELEASE_NAME == "Paper Strategy Promotion Package & Rollback Plan Lab")
        self._check("schema_version_193", lambda: SCHEMA_VERSION == "193")
        self._check("verify_version_returns_true", lambda: verify_version() is True)
        self._check("is_known_release_v193",
                    lambda: is_known_release("Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3"))
        self._check("version_info_paper_only", lambda: get_version_info()["paper_only"] is True)

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_safety_v193 import (
            SAFETY_FLAGS, run_safety_audit, is_safe_output_path, is_forbidden_action,
            is_allowed_action, validate_promotion_action,
            FORBIDDEN_PROMOTION_ACTIONS, ALLOWED_PROMOTION_ACTIONS,
            HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_flag_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_flag_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_flag_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_flag_promotion_package_only",
                    lambda: SAFETY_FLAGS["promotion_package_only"] is True)
        self._check("safety_flag_rollback_plan_only",
                    lambda: SAFETY_FLAGS["rollback_plan_only"] is True)
        self._check("safety_flag_not_investment_advice",
                    lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._check("safety_flag_no_production_mutation",
                    lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._check("safety_flag_broker_execution_false",
                    lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_flag_live_strategy_activation_false",
                    lambda: SAFETY_FLAGS["live_strategy_activation"] is False)

        # ── approval states (2) ───────────────────────────────────────────────
        self._check("approval_states_count_8", lambda: len(get_promotion_approval_states()) == 8)
        self._check("approval_states_has_paper_promotion_ready",
                    lambda: "PAPER_PROMOTION_READY" in get_promotion_approval_states())

        # ── recommendations (2) ───────────────────────────────────────────────
        self._check("recommendations_count_11", lambda: len(get_promotion_recommendations()) == 11)
        self._check("recommendations_has_promote",
                    lambda: "PROMOTE_TO_PAPER_PACKAGE" in get_promotion_recommendations())

        # ── rollback triggers (2) ─────────────────────────────────────────────
        self._check("rollback_triggers_count_12", lambda: len(get_rollback_triggers()) == 12)
        self._check("rollback_triggers_has_drawdown",
                    lambda: "DRAWDOWN_INCREASED" in get_rollback_triggers())

        # ── models (25) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_models_v193 import (
            StrategyPromotionInput, StrategyPromotionResult, PromotionPackage,
            PromotionCandidateRule, PromotionEvidenceLink, PromotionValidationSummary,
            PromotionRiskSummary, PromotionImpactSummary, PromotionApprovalChecklist,
            PromotionApprovalState, RollbackPlan, RollbackTrigger, RollbackStep,
            RollbackValidationResult, PromotionBlockReason, PromotionFinding,
            PromotionRecommendation, PromotionExportManifest, PromotionEvidencePack,
            PromotionAuditTrail, PromotionDashboard,
            PromotionHealthSummary as PHS,
            get_all_model_names,
        )
        self._check("model_promotion_input_paper_only",
                    lambda: StrategyPromotionInput().paper_only is True)
        self._check("model_promotion_result_no_real_orders",
                    lambda: StrategyPromotionResult().no_real_orders is True)
        self._check("model_promotion_package_promotion_package_only",
                    lambda: PromotionPackage().promotion_package_only is True)
        self._check("model_candidate_rule_rollback_plan_only",
                    lambda: PromotionCandidateRule().rollback_plan_only is True)
        self._check("model_evidence_link_no_broker",
                    lambda: PromotionEvidenceLink().no_broker is True)
        self._check("model_validation_summary_no_margin",
                    lambda: PromotionValidationSummary().no_margin is True)
        self._check("model_risk_summary_no_leverage",
                    lambda: PromotionRiskSummary().no_leverage is True)
        self._check("model_impact_summary_not_investment_advice",
                    lambda: PromotionImpactSummary().not_investment_advice is True)
        self._check("model_approval_checklist_demo_only",
                    lambda: PromotionApprovalChecklist().demo_only is True)
        self._check("model_approval_state_not_for_production",
                    lambda: PromotionApprovalState().not_for_production is True)
        self._check("model_rollback_plan_production_blocked",
                    lambda: RollbackPlan().production_trading_blocked is True)
        self._check("model_rollback_trigger_no_real_orders",
                    lambda: RollbackTrigger().no_real_orders is True)
        self._check("model_rollback_step_paper_only",
                    lambda: RollbackStep().paper_only is True)
        self._check("model_rollback_validation_result_research_only",
                    lambda: RollbackValidationResult().research_only is True)
        self._check("model_block_reason_simulate_only",
                    lambda: PromotionBlockReason().simulate_only is True)
        self._check("model_finding_validation_only",
                    lambda: PromotionFinding().validation_only is True)
        self._check("model_recommendation_review_only",
                    lambda: PromotionRecommendation().review_only is True)
        self._check("model_export_manifest_report_only",
                    lambda: PromotionExportManifest().report_only is True)
        self._check("model_evidence_pack_audit_only",
                    lambda: PromotionEvidencePack().audit_only is True)
        self._check("model_audit_trail_promotion_package_only",
                    lambda: PromotionAuditTrail().promotion_package_only is True)
        self._check("model_dashboard_rollback_plan_only",
                    lambda: PromotionDashboard().rollback_plan_only is True)
        self._check("model_health_summary_no_production_mutation",
                    lambda: PHS().no_production_strategy_mutation is True)
        self._check("models_count_22", lambda: len(get_all_model_names()) == 22)
        self._check("models_schema_193",
                    lambda: StrategyPromotionInput().schema_version == "193")
        self._check("models_no_live_activation",
                    lambda: PromotionPackage().no_live_strategy_activation is True)

        # ── engine (8) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_engine_v193 import (
            build_promotion_package, build_rollback_plan, validate_rollback_plan,
            build_promotion_approval_checklist, build_promotion_recommendation,
            build_promotion_evidence_pack, build_promotion_audit_trail,
            build_promotion_dashboard, build_promotion_export_manifest,
            validate_promotion_action, validate_promotion_approval_state,
            get_engine_info,
        )
        self._check("engine_blocked_missing_sandbox_source",
                    lambda: build_promotion_package("p1", "", "shadow_001", "cand_001", "base_001")["blocked"] is True)
        self._check("engine_blocked_missing_shadow_source",
                    lambda: build_promotion_package("p1", "sandbox_001", "", "cand_001", "base_001")["blocked"] is True)
        self._check("engine_blocked_missing_baseline",
                    lambda: build_promotion_package("p1", "sandbox_001", "shadow_001", "cand_001", "")["blocked"] is True)
        self._check("engine_passes_with_all_inputs",
                    lambda: build_promotion_package("p1", "sandbox_001", "shadow_001", "cand_001", "base_001")["blocked"] is False)
        self._check("engine_rollback_blocked_no_baseline",
                    lambda: build_rollback_plan("r1", "pkg1", "")["blocked"] is True)
        self._check("engine_rollback_passes_with_baseline",
                    lambda: build_rollback_plan("r1", "pkg1", "base_001", ["WIN_RATE_DETERIORATION"], ["step1"])["blocked"] is False)
        self._check("engine_recommendation_blocked_no_evidence",
                    lambda: build_promotion_recommendation("rec1", "pkg1", "NO_CHANGE", "test", [])["blocked"] is True)
        self._check("engine_checklist_blocked_no_rollback",
                    lambda: build_promotion_approval_checklist("cl1", "pkg1", rollback_plan_present=False)["blocked"] is True)

        # ── report (5) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_report_v193 import (
            export_promotion_summary_as_json, export_rollback_plan_as_json,
            export_promotion_recommendations_as_json, export_promotion_dashboard_as_json,
            get_report_info,
        )
        self._check("report_summary_json_paper_only",
                    lambda: '"paper_only": true' in export_promotion_summary_as_json({}))
        self._check("report_rollback_plan_json_no_real_orders",
                    lambda: '"no_real_orders": true' in export_rollback_plan_as_json({}))
        self._check("report_recommendations_json_schema",
                    lambda: '"schema_version"' in export_promotion_recommendations_as_json([]))
        self._check("report_dashboard_json_promotion_only",
                    lambda: '"promotion_package_only": true' in export_promotion_dashboard_as_json({}))
        self._check("report_info_paper_only",
                    lambda: get_report_info()["paper_only"] is True)

        # ── scenarios (3) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_scenarios_v193 import (
            get_all_scenarios, get_scenarios_by_type, get_scenario_by_id,
        )
        self._check("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._check("scenarios_all_paper_only",
                    lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._check("scenarios_have_complete_promotion",
                    lambda: len(get_scenarios_by_type("complete_promotion_package")) >= 1)

        # ── fixtures (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_fixtures_v193 import (
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
        self._check("safety_promotion_only_all_fixtures",
                    lambda: all(f["promotion_package_only"] is True for f in get_all_fixtures()))
        self._check("safety_safe_export_path",
                    lambda: is_safe_output_path("reports/") is True)
        self._check("safety_unsafe_export_blocked",
                    lambda: is_safe_output_path("production_strategy/") is False)

        # ── hard block conditions (3) ─────────────────────────────────────────
        self._check("hard_block_conditions_count_19",
                    lambda: len(HARD_BLOCK_CONDITIONS) == 19)
        self._check("hard_block_has_real_order",
                    lambda: "real_order_requested" in HARD_BLOCK_CONDITIONS)
        self._check("hard_block_has_missing_rollback_plan",
                    lambda: "missing_rollback_plan" in HARD_BLOCK_CONDITIONS)

        # ── allowed / forbidden actions (4) ───────────────────────────────────
        self._check("allowed_actions_count_16",
                    lambda: len(ALLOWED_PROMOTION_ACTIONS) == 16)
        self._check("forbidden_actions_count_9",
                    lambda: len(FORBIDDEN_PROMOTION_ACTIONS) == 9)
        self._check("allowed_action_promotion_build",
                    lambda: is_allowed_action("PROMOTION_BUILD") is True)
        self._check("forbidden_action_buy",
                    lambda: is_forbidden_action("BUY") is True)

        # ── GUI panel check (1) ───────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._check("gui_panel_version_193", lambda: PANEL_VERSION in ("1.9.3", "1.9.4", "1.9.5"))

        # ── backward compat (2) ───────────────────────────────────────────────
        self._check("backward_compat_v192_known",
                    lambda: is_known_release(
                        "Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2"))
        self._check("backward_compat_v191_known",
                    lambda: is_known_release(
                        "Paper Strategy Rule Tuning & Guardrail Lab v1.9.1"))

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)
        return PromotionHealthSummary(
            status="PASS" if failed == 0 else "FAIL",
            passed=passed,
            failed=failed,
            total=total,
            checks=list(self._checks),
            all_passed=(failed == 0),
        )


def run_health_check() -> "PromotionHealthSummary":
    """Run the strategy promotion health check and return summary."""
    return StrategyPromotionHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Strategy Promotion Health v1.9.3: {result.status} ({result.passed}/{result.total})")
    if result.failed:
        for c in result.checks:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
