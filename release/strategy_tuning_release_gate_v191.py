"""
release/strategy_tuning_release_gate_v191.py
Release gate for Paper Strategy Rule Tuning & Guardrail Lab v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List


class StrategyTuningReleaseGate:
    VERSION = "1.9.1"
    RELEASE_NAME = "Paper Strategy Rule Tuning & Guardrail Lab"
    MIN_SCENARIOS = 75
    MIN_FIXTURES = 75
    MIN_CLI = 18
    MIN_HEALTH_CHECKS = 60
    BASELINE_TESTS = 26649
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
        from paper_trading.small_capital_strategy.strategy_tuning_version_v191 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version,
            get_rule_categories, get_guardrail_triggers,
            get_tuning_recommendations, get_approval_states,
            get_forbidden_tuning_actions, get_allowed_tuning_actions,
            get_hard_block_conditions, is_known_release,
        )
        self._gate("version_191", lambda: VERSION == "1.9.1")
        self._gate("release_name_tuning_guardrail",
                   lambda: RELEASE_NAME == "Paper Strategy Rule Tuning & Guardrail Lab")
        self._gate("schema_191", lambda: SCHEMA_VERSION == "191")
        self._gate("verify_version_true", lambda: verify_version() is True)
        self._gate("rule_categories_count_14", lambda: len(get_rule_categories()) == 14)
        self._gate("guardrail_triggers_count_16",
                   lambda: len(get_guardrail_triggers()) == 16)
        self._gate("tuning_recommendations_count_15",
                   lambda: len(get_tuning_recommendations()) == 15)
        self._gate("approval_states_count_6", lambda: len(get_approval_states()) == 6)
        self._gate("hard_block_conditions_count_17",
                   lambda: len(get_hard_block_conditions()) == 17)

        # ── safety (13) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_safety_v191 import (
            SAFETY_FLAGS, run_safety_audit, is_forbidden_action, is_allowed_action,
            is_safe_output_path, FORBIDDEN_TUNING_ACTIONS,
            ALLOWED_TUNING_ACTIONS, HARD_BLOCK_CONDITIONS,
            get_safety_flags, get_hard_block_conditions as s_get_hbc,
        )
        self._gate("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._gate("safety_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._gate("safety_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._gate("safety_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._gate("safety_tuning_only", lambda: SAFETY_FLAGS["tuning_only"] is True)
        self._gate("safety_guardrail_only", lambda: SAFETY_FLAGS["guardrail_only"] is True)
        self._gate("safety_not_investment_advice",
                   lambda: SAFETY_FLAGS["not_investment_advice"] is True)
        self._gate("safety_no_production_mutation",
                   lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._gate("safety_broker_execution_false",
                   lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._gate("safety_production_mutation_false",
                   lambda: SAFETY_FLAGS["production_strategy_mutation"] is False)
        self._gate("safety_forbidden_buy", lambda: is_forbidden_action("BUY") is True)
        self._gate("safety_forbidden_actions_count_9",
                   lambda: len(FORBIDDEN_TUNING_ACTIONS) == 9)
        self._gate("safety_allowed_actions_count_16",
                   lambda: len(ALLOWED_TUNING_ACTIONS) == 16)

        # ── models (22) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_models_v191 import (
            StrategyRuleTuningInput, StrategyRuleTuningResult,
            StrategyRuleCandidate, StrategyRuleAdjustment,
            StrategyGuardrail, GuardrailTrigger, GuardrailSeverity, GuardrailAction,
            RuleTuningEvidence, RuleTuningFinding, RuleTuningRecommendation,
            RuleTuningBacktestSnapshot, RuleTuningReviewChecklist,
            RuleTuningApprovalState, RuleTuningExportManifest,
            RuleTuningEvidencePack, RuleTuningAuditTrail, RuleTuningDashboard,
            RuleTuningHealthSummary, RuleTuningValidationResult, get_all_model_names,
        )
        self._gate("models_count_20", lambda: len(get_all_model_names()) == 20)
        self._gate("model_tuning_input_paper_only",
                   lambda: StrategyRuleTuningInput().paper_only is True)
        self._gate("model_tuning_result_no_real_orders",
                   lambda: StrategyRuleTuningResult().no_real_orders is True)
        self._gate("model_rule_candidate_tuning_only",
                   lambda: StrategyRuleCandidate().tuning_only is True)
        self._gate("model_rule_adjustment_no_production_mutation",
                   lambda: StrategyRuleAdjustment().no_production_strategy_mutation is True)
        self._gate("model_guardrail_guardrail_only",
                   lambda: StrategyGuardrail().guardrail_only is True)
        self._gate("model_guardrail_trigger_paper_only",
                   lambda: GuardrailTrigger().paper_only is True)
        self._gate("model_guardrail_severity_no_broker",
                   lambda: GuardrailSeverity().no_broker is True)
        self._gate("model_guardrail_action_not_investment_advice",
                   lambda: GuardrailAction().not_investment_advice is True)
        self._gate("model_evidence_production_blocked",
                   lambda: RuleTuningEvidence().production_trading_blocked is True)
        self._gate("model_finding_demo_only",
                   lambda: RuleTuningFinding().demo_only is True)
        self._gate("model_recommendation_not_for_production",
                   lambda: RuleTuningRecommendation().not_for_production is True)
        self._gate("model_backtest_snapshot_no_margin",
                   lambda: RuleTuningBacktestSnapshot().no_margin is True)
        self._gate("model_review_checklist_no_leverage",
                   lambda: RuleTuningReviewChecklist().no_leverage is True)
        self._gate("model_approval_state_simulate_only",
                   lambda: RuleTuningApprovalState().simulate_only is True)
        self._gate("model_export_manifest_report_only",
                   lambda: RuleTuningExportManifest().report_only is True)
        self._gate("model_evidence_pack_audit_only",
                   lambda: RuleTuningEvidencePack().audit_only is True)
        self._gate("model_audit_trail_review_only",
                   lambda: RuleTuningAuditTrail().review_only is True)
        self._gate("model_dashboard_validation_only",
                   lambda: RuleTuningDashboard().validation_only is True)
        self._gate("model_health_summary_research_only",
                   lambda: RuleTuningHealthSummary().research_only is True)
        self._gate("model_validation_result_tuning_only",
                   lambda: RuleTuningValidationResult().tuning_only is True)
        self._gate("model_schema_191",
                   lambda: StrategyRuleTuningInput().schema_version == "191")

        # ── engine (16) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_engine_v191 import (
            run_tuning_review, build_rule_candidate, build_rule_adjustment,
            build_guardrail, evaluate_guardrail_triggers,
            build_tuning_recommendation, build_backtest_snapshot,
            build_dashboard, build_evidence_pack, build_audit_trail,
            build_export_manifest, get_engine_info,
            validate_rule_category, validate_guardrail_trigger,
            validate_tuning_recommendation, validate_approval_state,
        )
        self._gate("engine_tuning_blocked_missing_perf",
                   lambda: run_tuning_review("t1", "", "j1")["blocked"] is True)
        self._gate("engine_tuning_blocked_missing_journal",
                   lambda: run_tuning_review("t2", "p1", "")["blocked"] is True)
        self._gate("engine_tuning_passes_with_sources",
                   lambda: run_tuning_review("t3", "p1", "j1")["blocked"] is False)
        self._gate("engine_candidate_keep_rule",
                   lambda: build_rule_candidate("r1", "A", "ABC_BUY_POINT",
                                                0.65, 0.6, 0.05)["recommendation"] == "KEEP_RULE")
        self._gate("engine_candidate_tighten_rule",
                   lambda: build_rule_candidate("r2", "B", "ABC_BUY_POINT",
                                                0.28, -0.1, 0.1)["recommendation"] == "TIGHTEN_RULE")
        self._gate("engine_adjustment_blocked_no_evidence",
                   lambda: build_rule_adjustment("a1", "r1", "ABC_BUY_POINT",
                                                 "TIGHTEN_RULE", "test", [])["blocked"] is True)
        self._gate("engine_adjustment_passes_with_evidence",
                   lambda: build_rule_adjustment("a2", "r1", "ABC_BUY_POINT",
                                                 "TIGHTEN_RULE", "test", ["e1"])["blocked"] is False)
        self._gate("engine_guardrail_blocked_no_trigger",
                   lambda: build_guardrail("g1", "test", "", "WARNING",
                                           "LOG_ONLY")["blocked"] is True)
        self._gate("engine_guardrail_passes_with_trigger",
                   lambda: build_guardrail("g2", "test", "EXPECTANCY_NEGATIVE",
                                           "WARNING", "LOG_ONLY")["blocked"] is False)
        self._gate("engine_triggers_list_length",
                   lambda: len(evaluate_guardrail_triggers({})) == 16)
        self._gate("engine_expectancy_trigger_fires",
                   lambda: any(t["triggered"] for t in
                               evaluate_guardrail_triggers({"expectancy_r": -0.3})))
        self._gate("engine_validate_rule_category",
                   lambda: validate_rule_category("ABC_BUY_POINT") is True)
        self._gate("engine_validate_rule_category_invalid",
                   lambda: validate_rule_category("REAL_TRADE") is False)
        self._gate("engine_validate_guardrail_trigger",
                   lambda: validate_guardrail_trigger("EXPECTANCY_NEGATIVE") is True)
        self._gate("engine_export_manifest_safe",
                   lambda: build_export_manifest("m1", "period")["safe_path"] is True)
        self._gate("engine_export_manifest_unsafe_redirected",
                   lambda: build_export_manifest("m2", "period",
                                                 "production_strategy/")["export_path"] == "reports/")

        # ── report (6) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_report_v191 import (
            export_tuning_summary_as_json, export_guardrail_report_as_json,
            export_recommendations_as_json, export_recommendations_as_markdown,
            export_dashboard_as_json, get_report_info,
        )
        self._gate("report_tuning_summary_paper_only",
                   lambda: '"paper_only": true' in export_tuning_summary_as_json({}))
        self._gate("report_guardrail_no_real_orders",
                   lambda: '"no_real_orders": true' in export_guardrail_report_as_json([]))
        self._gate("report_recommendations_markdown_header",
                   lambda: "Rule Tuning Recommendations" in export_recommendations_as_markdown([]))
        self._gate("report_dashboard_schema",
                   lambda: '"schema_version"' in export_dashboard_as_json({}))
        self._gate("report_info_tuning_only",
                   lambda: get_report_info()["tuning_only"] is True)
        self._gate("report_info_functions_count",
                   lambda: len(get_report_info()["functions"]) >= 10)

        # ── scenarios (5) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_scenarios_v191 import (
            get_all_scenarios, get_scenarios_by_type, get_scenario_by_id,
        )
        self._gate("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._gate("scenarios_min_75",
                   lambda: len(get_all_scenarios()) >= self.MIN_SCENARIOS)
        self._gate("scenarios_all_paper_only",
                   lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._gate("scenarios_no_real_orders",
                   lambda: all(s["no_real_orders"] is True for s in get_all_scenarios()))
        self._gate("scenarios_no_forbidden_words",
                   lambda: all(
                       not any(word in s.get("description", "").upper()
                               for word in ["SUBMIT_ORDER", "BROKER_ORDER", "AUTO_TRADE"])
                       for s in get_all_scenarios()
                   ))

        # ── fixtures (5) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_fixtures_v191 import (
            get_all_fixtures, get_fixture_by_id, get_fixtures_by_recommendation,
        )
        self._gate("fixtures_count_75", lambda: len(get_all_fixtures()) == 75)
        self._gate("fixtures_min_75",
                   lambda: len(get_all_fixtures()) >= self.MIN_FIXTURES)
        self._gate("fixtures_all_paper_only",
                   lambda: all(f["paper_only"] is True for f in get_all_fixtures()))
        self._gate("fixtures_all_no_real_orders",
                   lambda: all(f["no_real_orders"] is True for f in get_all_fixtures()))
        self._gate("fixtures_all_tuning_only",
                   lambda: all(f["tuning_only"] is True for f in get_all_fixtures()))

        # ── health (3) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_tuning_health_v191 import (
            run_health_check,
        )
        h = run_health_check()
        self._gate("health_all_passed", lambda: h.all_passed is True)
        self._gate("health_status_pass", lambda: h.status == "PASS")
        self._gate("health_checks_count_ge_60", lambda: h.total >= self.MIN_HEALTH_CHECKS)

        # ── backward compatibility (3) ────────────────────────────────────────
        self._gate("backward_compat_v190_known",
                   lambda: is_known_release(
                       "Paper Trading Performance Review & Strategy Improvement Lab v1.9.0"))
        self._gate("backward_compat_v189_known",
                   lambda: is_known_release("Paper Decision Journal & Review Loop v1.8.9"))
        self._gate("backward_compat_v188_known",
                   lambda: is_known_release("Paper Decision Workflow Runner v1.8.8"))

        # ── no forbidden words in version module (1) ──────────────────────────
        self._gate("version_module_no_forbidden_words",
                   lambda: not any(
                       word in str(get_rule_categories()).upper()
                       for word in ["BUY_SIGNAL", "SUBMIT_ORDER", "BROKER_ORDER"]
                   ))

        # ── GUI panel version (1) ─────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._gate("gui_panel_version_191", lambda: PANEL_VERSION in ("1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8"))

        # ── CLI check (1) ────────────────────────────────────────────────────
        from cli.command_registry import get_commands_by_group
        st_cmds = [c for c in get_commands_by_group("strategy_tuning")
                   if c.introduced_in == "1.9.1"]
        self._gate("cli_strategy_tuning_count_18",
                   lambda: len(st_cmds) >= self.MIN_CLI)

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
            "tuning_only": True,
            "guardrail_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "no_production_strategy_mutation": True,
            "not_investment_advice": True,
            "production_trading_blocked": True,
            "review_only": True,
            "audit_only": True,
        }


def run_release_gate() -> Dict[str, Any]:
    """Run the strategy tuning release gate and return result dict."""
    return StrategyTuningReleaseGate().run()


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Strategy Tuning Release Gate v1.9.1: {result['status']} "
          f"({result['passed']}/{result['total']})")
    if result["failed"]:
        for r in result["results"]:
            if not r["passed"]:
                print(f"  [FAIL] {r['name']}: {r['error']}")
