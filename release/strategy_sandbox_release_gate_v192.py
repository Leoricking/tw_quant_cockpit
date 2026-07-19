"""
release/strategy_sandbox_release_gate_v192.py
Release gate for Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List


class StrategySandboxReleaseGate:
    VERSION = "1.9.2"
    RELEASE_NAME = "Paper Strategy Rule Sandbox & Shadow Validation Lab"
    MIN_SCENARIOS = 75
    MIN_FIXTURES = 75
    MIN_CLI = 20
    MIN_HEALTH_CHECKS = 60
    BASELINE_TESTS = 27267
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

        # ── version (9) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_version_v192 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version,
            get_sandbox_modes, get_validation_dimensions,
            get_sandbox_approval_states, get_sandbox_recommendations,
            get_forbidden_sandbox_actions, get_allowed_sandbox_actions,
            get_hard_block_conditions, is_known_release,
        )
        self._gate("version_192", lambda: VERSION == "1.9.2")
        self._gate("release_name_sandbox",
                   lambda: RELEASE_NAME == "Paper Strategy Rule Sandbox & Shadow Validation Lab")
        self._gate("schema_192", lambda: SCHEMA_VERSION == "192")
        self._gate("verify_version_true", lambda: verify_version() is True)
        self._gate("sandbox_modes_count_11", lambda: len(get_sandbox_modes()) == 11)
        self._gate("validation_dimensions_count_20",
                   lambda: len(get_validation_dimensions()) == 20)
        self._gate("approval_states_count_6", lambda: len(get_sandbox_approval_states()) == 6)
        self._gate("recommendations_count_13", lambda: len(get_sandbox_recommendations()) == 13)
        self._gate("hard_block_conditions_count_17",
                   lambda: len(get_hard_block_conditions()) == 17)

        # ── safety (13) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_safety_v192 import (
            SAFETY_FLAGS, run_safety_audit, is_forbidden_action, is_allowed_action,
            is_safe_output_path, FORBIDDEN_SANDBOX_ACTIONS,
            ALLOWED_SANDBOX_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._gate("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._gate("safety_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._gate("safety_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._gate("safety_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._gate("safety_sandbox_only", lambda: SAFETY_FLAGS["sandbox_only"] is True)
        self._gate("safety_shadow_only", lambda: SAFETY_FLAGS["shadow_only"] is True)
        self._gate("safety_not_investment_advice",
                   lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._gate("safety_no_production_mutation",
                   lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._gate("safety_no_live_activation",
                   lambda: SAFETY_FLAGS["no_live_strategy_activation"] is True)
        self._gate("safety_broker_execution_false",
                   lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._gate("safety_live_strategy_activation_false",
                   lambda: SAFETY_FLAGS["live_strategy_activation"] is False)
        self._gate("safety_forbidden_buy", lambda: is_forbidden_action("BUY") is True)
        self._gate("safety_forbidden_actions_count_9",
                   lambda: len(FORBIDDEN_SANDBOX_ACTIONS) == 9)

        # ── models (25) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_models_v192 import (
            StrategySandboxInput, StrategySandboxResult, ShadowValidationInput,
            ShadowValidationResult, SandboxRuleSet, SandboxRuleChange,
            SandboxGuardrailSet, ShadowComparisonResult, BaselineStrategySnapshot,
            CandidateStrategySnapshot, SandboxPerformanceDelta, SandboxRiskDelta,
            SandboxSignalDelta, SandboxApprovalState, SandboxBlockReason,
            SandboxValidationFinding, SandboxRecommendation, SandboxExportManifest,
            SandboxEvidencePack, SandboxAuditTrail, SandboxDashboard,
            SandboxHealthSummary, SandboxValidationResult, get_all_model_names,
        )
        self._gate("models_count_23", lambda: len(get_all_model_names()) == 23)
        self._gate("model_sandbox_input_paper_only",
                   lambda: StrategySandboxInput().paper_only is True)
        self._gate("model_sandbox_result_no_real_orders",
                   lambda: StrategySandboxResult().no_real_orders is True)
        self._gate("model_shadow_validation_input_sandbox_only",
                   lambda: ShadowValidationInput().sandbox_only is True)
        self._gate("model_shadow_validation_result_shadow_only",
                   lambda: ShadowValidationResult().shadow_only is True)
        self._gate("model_sandbox_ruleset_no_broker",
                   lambda: SandboxRuleSet().no_broker is True)
        self._gate("model_sandbox_rule_change_paper_only",
                   lambda: SandboxRuleChange().paper_only is True)
        self._gate("model_sandbox_guardrail_set_no_margin",
                   lambda: SandboxGuardrailSet().no_margin is True)
        self._gate("model_shadow_comparison_result_no_leverage",
                   lambda: ShadowComparisonResult().no_leverage is True)
        self._gate("model_baseline_snapshot_no_production_mutation",
                   lambda: BaselineStrategySnapshot().no_production_strategy_mutation is True)
        self._gate("model_candidate_snapshot_no_live_activation",
                   lambda: CandidateStrategySnapshot().no_live_strategy_activation is True)
        self._gate("model_performance_delta_not_investment_advice",
                   lambda: SandboxPerformanceDelta().not_investment_advice is True)
        self._gate("model_risk_delta_demo_only",
                   lambda: SandboxRiskDelta().demo_only is True)
        self._gate("model_signal_delta_not_for_production",
                   lambda: SandboxSignalDelta().not_for_production is True)
        self._gate("model_approval_state_production_blocked",
                   lambda: SandboxApprovalState().production_trading_blocked is True)
        self._gate("model_block_reason_research_only",
                   lambda: SandboxBlockReason().research_only is True)
        self._gate("model_validation_finding_simulate_only",
                   lambda: SandboxValidationFinding().simulate_only is True)
        self._gate("model_recommendation_validation_only",
                   lambda: SandboxRecommendation().validation_only is True)
        self._gate("model_export_manifest_review_only",
                   lambda: SandboxExportManifest().review_only is True)
        self._gate("model_evidence_pack_report_only",
                   lambda: SandboxEvidencePack().report_only is True)
        self._gate("model_audit_trail_audit_only",
                   lambda: SandboxAuditTrail().audit_only is True)
        self._gate("model_dashboard_sandbox_only",
                   lambda: SandboxDashboard().sandbox_only is True)
        self._gate("model_health_summary_shadow_only",
                   lambda: SandboxHealthSummary().shadow_only is True)
        self._gate("model_validation_result_sandbox_only",
                   lambda: SandboxValidationResult().sandbox_only is True)
        self._gate("model_schema_192",
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
        self._gate("engine_sandbox_blocked_missing_proposal",
                   lambda: run_sandbox_validation("s1", "", "b1", "c1")["blocked"] is True)
        self._gate("engine_sandbox_blocked_missing_baseline",
                   lambda: run_sandbox_validation("s2", "p1", "", "c1")["blocked"] is True)
        self._gate("engine_sandbox_blocked_missing_candidate",
                   lambda: run_sandbox_validation("s3", "p1", "b1", "")["blocked"] is True)
        self._gate("engine_sandbox_passes_with_all_inputs",
                   lambda: run_sandbox_validation("s4", "p1", "b1", "c1")["blocked"] is False)
        self._gate("engine_recommendation_blocked_no_evidence",
                   lambda: build_sandbox_recommendation("r1", "s1", "NO_CHANGE",
                                                        "test", [])["blocked"] is True)
        self._gate("engine_recommendation_passes_with_evidence",
                   lambda: build_sandbox_recommendation("r2", "s1", "KEEP_BASELINE",
                                                        "test", ["e1"])["blocked"] is False)
        self._gate("engine_validate_sandbox_mode",
                   lambda: validate_sandbox_mode("SHADOW_COMPARE") is True)
        self._gate("engine_shadow_compare_blocked_no_baseline",
                   lambda: run_shadow_comparison("c1", "", "cand1")["blocked"] is True)

        # ── report (5) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_report_v192 import (
            export_sandbox_summary_as_json, export_shadow_comparison_as_json,
            export_sandbox_recommendations_as_json, export_sandbox_dashboard_as_json,
            get_report_info,
        )
        self._gate("report_sandbox_summary_paper_only",
                   lambda: '"paper_only": true' in export_sandbox_summary_as_json({}))
        self._gate("report_shadow_comparison_no_real_orders",
                   lambda: '"no_real_orders": true' in export_shadow_comparison_as_json({}))
        self._gate("report_recommendations_schema",
                   lambda: '"schema_version"' in export_sandbox_recommendations_as_json([]))
        self._gate("report_dashboard_sandbox_only",
                   lambda: '"sandbox_only": true' in export_sandbox_dashboard_as_json({}))
        self._gate("report_info_paper_only",
                   lambda: get_report_info()["paper_only"] is True)

        # ── scenarios (5) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_scenarios_v192 import (
            get_all_scenarios, get_scenarios_by_type, get_scenario_by_id,
        )
        self._gate("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._gate("scenarios_min_75",
                   lambda: len(get_all_scenarios()) >= self.MIN_SCENARIOS)
        self._gate("scenarios_all_paper_only",
                   lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._gate("scenarios_have_complete_sandbox_validation",
                   lambda: len(get_scenarios_by_type("complete_sandbox_validation")) >= 1)
        self._gate("scenarios_have_shadow_compare",
                   lambda: len(get_scenarios_by_type("shadow_compare_baseline_vs_candidate")) >= 1)

        # ── fixtures (5) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_fixtures_v192 import (
            get_all_fixtures, get_fixture_by_id,
        )
        self._gate("fixtures_count_75", lambda: len(get_all_fixtures()) == 75)
        self._gate("fixtures_min_75",
                   lambda: len(get_all_fixtures()) >= self.MIN_FIXTURES)
        self._gate("fixtures_all_paper_only",
                   lambda: all(f["paper_only"] is True for f in get_all_fixtures()))
        self._gate("fixtures_all_no_real_orders",
                   lambda: all(f["no_real_orders"] is True for f in get_all_fixtures()))
        self._gate("fixtures_all_sandbox_only",
                   lambda: all(f["sandbox_only"] is True for f in get_all_fixtures()))

        # ── safety extras (4) ────────────────────────────────────────────────
        self._gate("safety_safe_export_path",
                   lambda: is_safe_output_path("reports/") is True)
        self._gate("safety_unsafe_export_blocked",
                   lambda: is_safe_output_path("production_strategy/") is False)
        self._gate("hard_block_has_real_order",
                   lambda: "real_order_requested" in HARD_BLOCK_CONDITIONS)
        self._gate("hard_block_has_live_activation",
                   lambda: "live_strategy_activation_attempted" in HARD_BLOCK_CONDITIONS)

        # ── health (3) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_sandbox_health_v192 import (
            run_health_check,
        )
        h = run_health_check()
        self._gate("health_all_passed", lambda: h.all_passed is True)
        self._gate("health_status_pass", lambda: h.status == "PASS")
        self._gate("health_checks_count_ge_60", lambda: h.total >= self.MIN_HEALTH_CHECKS)

        # ── GUI panel version (1) ─────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._gate("gui_panel_version_192", lambda: PANEL_VERSION in ("1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10", "2.0.0"))

        # ── CLI check (1) ────────────────────────────────────────────────────
        from cli.command_registry import get_commands_by_group
        sb_cmds = [c for c in get_commands_by_group("strategy_sandbox")
                   if c.introduced_in == "1.9.2"]
        self._gate("cli_strategy_sandbox_count_20",
                   lambda: len(sb_cmds) >= self.MIN_CLI)

        # ── backward compatibility (5) ────────────────────────────────────────
        self._gate("backward_compat_v191_known",
                   lambda: is_known_release(
                       "Paper Strategy Rule Tuning & Guardrail Lab v1.9.1"))
        self._gate("backward_compat_v190_known",
                   lambda: is_known_release(
                       "Paper Trading Performance Review & Strategy Improvement Lab v1.9.0"))
        self._gate("backward_compat_v189_known",
                   lambda: is_known_release("Paper Decision Journal & Review Loop v1.8.9"))
        self._gate("backward_compat_v188_known",
                   lambda: is_known_release("Paper Decision Workflow Runner v1.8.8"))
        self._gate("backward_compat_v170_known",
                   lambda: is_known_release("Small Capital Strategy v1.7.0"))

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
            "sandbox_only": True,
            "shadow_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
            "production_trading_blocked": True,
            "schema_version": "192",
            "research_only": True,
            "no_broker": True,
            "no_production_strategy_mutation": True,
            "review_only": True,
            "audit_only": True,
        }


def run_release_gate() -> Dict[str, Any]:
    """Run the strategy sandbox release gate."""
    return StrategySandboxReleaseGate().run()


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Strategy Sandbox Release Gate v1.9.2: {result['status']} ({result['passed']}/{result['total']})")
    if result["failed"]:
        for r in result["results"]:
            if not r["passed"]:
                print(f"  [FAIL] {r['name']}: {r['error']}")
