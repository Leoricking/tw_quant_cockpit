"""
paper_trading/small_capital_strategy/strategy_sandbox_health_v192.py
Health check for Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List


class StrategySandboxHealthCheck:
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

    def run(self) -> "SandboxHealthSummary":
        from paper_trading.small_capital_strategy.strategy_sandbox_models_v192 import SandboxHealthSummary
        self._checks = []

        # ── version (6) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_version_v192 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_sandbox_modes, get_validation_dimensions,
            get_sandbox_approval_states, get_sandbox_recommendations,
            get_forbidden_sandbox_actions, get_allowed_sandbox_actions,
            get_hard_block_conditions,
        )
        self._check("version_is_192", lambda: VERSION == "1.9.2")
        self._check("release_name_correct",
                    lambda: RELEASE_NAME == "Paper Strategy Rule Sandbox & Shadow Validation Lab")
        self._check("schema_version_192", lambda: SCHEMA_VERSION == "192")
        self._check("verify_version_returns_true", lambda: verify_version() is True)
        self._check("is_known_release_v192",
                    lambda: is_known_release("Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2"))
        self._check("version_info_paper_only", lambda: get_version_info()["paper_only"] is True)

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_safety_v192 import (
            SAFETY_FLAGS, run_safety_audit, is_safe_output_path, is_forbidden_action,
            is_allowed_action, validate_sandbox_action,
            FORBIDDEN_SANDBOX_ACTIONS, ALLOWED_SANDBOX_ACTIONS,
            HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_flag_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_flag_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_flag_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_flag_sandbox_only", lambda: SAFETY_FLAGS["sandbox_only"] is True)
        self._check("safety_flag_shadow_only", lambda: SAFETY_FLAGS["shadow_only"] is True)
        self._check("safety_flag_not_investment_advice",
                    lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._check("safety_flag_no_production_mutation",
                    lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._check("safety_flag_broker_execution_false",
                    lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_flag_live_strategy_activation_false",
                    lambda: SAFETY_FLAGS["live_strategy_activation"] is False)

        # ── sandbox modes (3) ────────────────────────────────────────────────
        self._check("sandbox_modes_count_11", lambda: len(get_sandbox_modes()) == 11)
        self._check("sandbox_modes_has_shadow_compare",
                    lambda: "SHADOW_COMPARE" in get_sandbox_modes())
        self._check("sandbox_modes_has_full_ruleset",
                    lambda: "FULL_RULESET_COMPARE" in get_sandbox_modes())

        # ── validation dimensions (3) ─────────────────────────────────────────
        self._check("validation_dimensions_count_20",
                    lambda: len(get_validation_dimensions()) == 20)
        self._check("validation_dimensions_has_win_rate_delta",
                    lambda: "win_rate_delta" in get_validation_dimensions())
        self._check("validation_dimensions_has_shadow_score",
                    lambda: "shadow_validation_score" in get_validation_dimensions())

        # ── approval states (2) ───────────────────────────────────────────────
        self._check("approval_states_count_6", lambda: len(get_sandbox_approval_states()) == 6)
        self._check("approval_states_has_shadow_only",
                    lambda: "SHADOW_ONLY" in get_sandbox_approval_states())

        # ── recommendations (2) ───────────────────────────────────────────────
        self._check("recommendations_count_13", lambda: len(get_sandbox_recommendations()) == 13)
        self._check("recommendations_has_keep_baseline",
                    lambda: "KEEP_BASELINE" in get_sandbox_recommendations())

        # ── models (25) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_models_v192 import (
            StrategySandboxInput, StrategySandboxResult, ShadowValidationInput,
            ShadowValidationResult, SandboxRuleSet, SandboxRuleChange,
            SandboxGuardrailSet, ShadowComparisonResult, BaselineStrategySnapshot,
            CandidateStrategySnapshot, SandboxPerformanceDelta, SandboxRiskDelta,
            SandboxSignalDelta, SandboxApprovalState, SandboxBlockReason,
            SandboxValidationFinding, SandboxRecommendation, SandboxExportManifest,
            SandboxEvidencePack, SandboxAuditTrail, SandboxDashboard,
            SandboxHealthSummary as SMS, SandboxValidationResult as SVR,
            get_all_model_names,
        )
        self._check("model_sandbox_input_paper_only",
                    lambda: StrategySandboxInput().paper_only is True)
        self._check("model_sandbox_result_no_real_orders",
                    lambda: StrategySandboxResult().no_real_orders is True)
        self._check("model_shadow_validation_input_sandbox_only",
                    lambda: ShadowValidationInput().sandbox_only is True)
        self._check("model_shadow_validation_result_shadow_only",
                    lambda: ShadowValidationResult().shadow_only is True)
        self._check("model_sandbox_ruleset_no_broker",
                    lambda: SandboxRuleSet().no_broker is True)
        self._check("model_sandbox_rule_change_paper_only",
                    lambda: SandboxRuleChange().paper_only is True)
        self._check("model_sandbox_guardrail_set_no_margin",
                    lambda: SandboxGuardrailSet().no_margin is True)
        self._check("model_shadow_comparison_result_no_leverage",
                    lambda: ShadowComparisonResult().no_leverage is True)
        self._check("model_baseline_snapshot_no_production_mutation",
                    lambda: BaselineStrategySnapshot().no_production_strategy_mutation is True)
        self._check("model_candidate_snapshot_no_live_activation",
                    lambda: CandidateStrategySnapshot().no_live_strategy_activation is True)
        self._check("model_performance_delta_not_investment_advice",
                    lambda: SandboxPerformanceDelta().not_investment_advice is True)
        self._check("model_risk_delta_demo_only",
                    lambda: SandboxRiskDelta().demo_only is True)
        self._check("model_signal_delta_not_for_production",
                    lambda: SandboxSignalDelta().not_for_production is True)
        self._check("model_approval_state_production_blocked",
                    lambda: SandboxApprovalState().production_trading_blocked is True)
        self._check("model_block_reason_research_only",
                    lambda: SandboxBlockReason().research_only is True)
        self._check("model_validation_finding_simulate_only",
                    lambda: SandboxValidationFinding().simulate_only is True)
        self._check("model_recommendation_validation_only",
                    lambda: SandboxRecommendation().validation_only is True)
        self._check("model_export_manifest_review_only",
                    lambda: SandboxExportManifest().review_only is True)
        self._check("model_evidence_pack_report_only",
                    lambda: SandboxEvidencePack().report_only is True)
        self._check("model_audit_trail_audit_only",
                    lambda: SandboxAuditTrail().audit_only is True)
        self._check("model_dashboard_sandbox_only",
                    lambda: SandboxDashboard().sandbox_only is True)
        self._check("model_health_summary_shadow_only",
                    lambda: SMS().shadow_only is True)
        self._check("model_validation_result_sandbox_only",
                    lambda: SVR().sandbox_only is True)
        self._check("models_count_23", lambda: len(get_all_model_names()) == 23)
        self._check("models_schema_192",
                    lambda: StrategySandboxInput().schema_version == "192")

        # ── engine (8) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_engine_v192 import (
            run_sandbox_validation, build_baseline_snapshot, build_candidate_snapshot,
            run_shadow_comparison, compute_performance_delta, compute_risk_delta,
            build_sandbox_recommendation, build_sandbox_evidence_pack,
            build_sandbox_audit_trail, build_sandbox_dashboard,
            build_sandbox_export_manifest, get_engine_info,
            validate_sandbox_action, validate_sandbox_mode, validate_sandbox_approval_state,
        )
        self._check("engine_sandbox_blocked_missing_proposal",
                    lambda: run_sandbox_validation("s1", "", "b1", "c1")["blocked"] is True)
        self._check("engine_sandbox_blocked_missing_baseline",
                    lambda: run_sandbox_validation("s2", "p1", "", "c1")["blocked"] is True)
        self._check("engine_sandbox_blocked_missing_candidate",
                    lambda: run_sandbox_validation("s3", "p1", "b1", "")["blocked"] is True)
        self._check("engine_sandbox_passes_with_all_inputs",
                    lambda: run_sandbox_validation("s4", "p1", "b1", "c1")["blocked"] is False)
        self._check("engine_recommendation_blocked_no_evidence",
                    lambda: build_sandbox_recommendation("r1", "s1", "NO_CHANGE",
                                                         "test", [])["blocked"] is True)
        self._check("engine_recommendation_passes_with_evidence",
                    lambda: build_sandbox_recommendation("r2", "s1", "KEEP_BASELINE",
                                                         "test", ["e1"])["blocked"] is False)
        self._check("engine_validate_sandbox_mode",
                    lambda: validate_sandbox_mode("SHADOW_COMPARE") is True)
        self._check("engine_shadow_compare_blocked_no_baseline",
                    lambda: run_shadow_comparison("c1", "", "cand1")["blocked"] is True)

        # ── report (5) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_report_v192 import (
            export_sandbox_summary_as_json, export_shadow_comparison_as_json,
            export_sandbox_recommendations_as_json, export_sandbox_dashboard_as_json,
            get_report_info,
        )
        self._check("report_sandbox_summary_json_paper_only",
                    lambda: '"paper_only": true' in export_sandbox_summary_as_json({}))
        self._check("report_shadow_comparison_json_no_real_orders",
                    lambda: '"no_real_orders": true' in export_shadow_comparison_as_json({}))
        self._check("report_recommendations_json_schema",
                    lambda: '"schema_version"' in export_sandbox_recommendations_as_json([]))
        self._check("report_dashboard_json_sandbox_only",
                    lambda: '"sandbox_only": true' in export_sandbox_dashboard_as_json({}))
        self._check("report_info_paper_only",
                    lambda: get_report_info()["paper_only"] is True)

        # ── scenarios (3) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_scenarios_v192 import (
            get_all_scenarios, get_scenarios_by_type, get_scenario_by_id,
        )
        self._check("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._check("scenarios_all_paper_only",
                    lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._check("scenarios_have_complete_sandbox_validation",
                    lambda: len(get_scenarios_by_type("complete_sandbox_validation")) >= 1)

        # ── fixtures (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_fixtures_v192 import (
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
        self._check("safety_sandbox_only_all_fixtures",
                    lambda: all(f["sandbox_only"] is True for f in get_all_fixtures()))
        self._check("safety_safe_export_path",
                    lambda: is_safe_output_path("reports/") is True)
        self._check("safety_unsafe_export_blocked",
                    lambda: is_safe_output_path("production_strategy/") is False)

        # ── hard block conditions (3) ─────────────────────────────────────────
        self._check("hard_block_conditions_count_17",
                    lambda: len(HARD_BLOCK_CONDITIONS) == 17)
        self._check("hard_block_has_real_order",
                    lambda: "real_order_requested" in HARD_BLOCK_CONDITIONS)
        self._check("hard_block_has_live_activation",
                    lambda: "live_strategy_activation_attempted" in HARD_BLOCK_CONDITIONS)

        # ── allowed / forbidden actions (4) ───────────────────────────────────
        self._check("allowed_actions_count_16",
                    lambda: len(ALLOWED_SANDBOX_ACTIONS) == 16)
        self._check("forbidden_actions_count_9",
                    lambda: len(FORBIDDEN_SANDBOX_ACTIONS) == 9)
        self._check("allowed_action_sandbox_run",
                    lambda: is_allowed_action("SANDBOX_RUN") is True)
        self._check("forbidden_action_buy",
                    lambda: is_forbidden_action("BUY") is True)

        # ── GUI panel check (1) ───────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._check("gui_panel_version_192", lambda: PANEL_VERSION == "1.9.2")

        # ── backward compat (2) ───────────────────────────────────────────────
        self._check("backward_compat_v191_known",
                    lambda: is_known_release(
                        "Paper Strategy Rule Tuning & Guardrail Lab v1.9.1"))
        self._check("backward_compat_v190_known",
                    lambda: is_known_release(
                        "Paper Trading Performance Review & Strategy Improvement Lab v1.9.0"))

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)
        return SandboxHealthSummary(
            status="PASS" if failed == 0 else "FAIL",
            passed=passed,
            failed=failed,
            total=total,
            checks=list(self._checks),
            all_passed=(failed == 0),
        )


def run_health_check() -> "SandboxHealthSummary":
    """Run the strategy sandbox health check and return summary."""
    return StrategySandboxHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Strategy Sandbox Health v1.9.2: {result.status} ({result.passed}/{result.total})")
    if result.failed:
        for c in result.checks:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
