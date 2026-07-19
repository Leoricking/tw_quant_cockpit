"""
release/strategy_promotion_release_gate_v193.py
Release gate for Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3.
[!] Research Only. Paper Only. Promotion Package Only. Rollback Plan Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List


class StrategyPromotionReleaseGate:
    VERSION = "1.9.3"
    RELEASE_NAME = "Paper Strategy Promotion Package & Rollback Plan Lab"
    MIN_SCENARIOS = 75
    MIN_FIXTURES = 75
    MIN_CLI = 18
    MIN_HEALTH_CHECKS = 60
    BASELINE_TESTS = 27847
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
        from paper_trading.small_capital_strategy.strategy_promotion_version_v193 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version,
            get_promotion_approval_states, get_promotion_recommendations,
            get_rollback_triggers, get_forbidden_promotion_actions,
            get_allowed_promotion_actions, get_hard_block_conditions,
            is_known_release,
        )
        self._gate("version_193", lambda: VERSION == "1.9.3")
        self._gate("release_name_promotion",
                   lambda: RELEASE_NAME == "Paper Strategy Promotion Package & Rollback Plan Lab")
        self._gate("schema_193", lambda: SCHEMA_VERSION == "193")
        self._gate("verify_version_true", lambda: verify_version() is True)
        self._gate("approval_states_count_8", lambda: len(get_promotion_approval_states()) == 8)
        self._gate("recommendations_count_11", lambda: len(get_promotion_recommendations()) == 11)
        self._gate("rollback_triggers_count_12", lambda: len(get_rollback_triggers()) == 12)
        self._gate("hard_block_conditions_count_19",
                   lambda: len(get_hard_block_conditions()) == 19)

        # ── safety (13) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_safety_v193 import (
            SAFETY_FLAGS, run_safety_audit, is_forbidden_action, is_allowed_action,
            is_safe_output_path, FORBIDDEN_PROMOTION_ACTIONS,
            ALLOWED_PROMOTION_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._gate("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._gate("safety_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._gate("safety_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._gate("safety_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._gate("safety_promotion_package_only",
                   lambda: SAFETY_FLAGS["promotion_package_only"] is True)
        self._gate("safety_rollback_plan_only",
                   lambda: SAFETY_FLAGS["rollback_plan_only"] is True)
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
        self._gate("safety_safe_export_path",
                   lambda: is_safe_output_path("reports/") is True)
        self._gate("safety_forbidden_action_buy",
                   lambda: is_forbidden_action("BUY") is True)

        # ── models (10) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_models_v193 import (
            StrategyPromotionInput, StrategyPromotionResult, PromotionPackage,
            RollbackPlan, RollbackTrigger, PromotionApprovalChecklist,
            PromotionEvidencePack, PromotionAuditTrail, PromotionDashboard,
            get_all_model_names,
        )
        self._gate("model_promotion_input_paper_only",
                   lambda: StrategyPromotionInput().paper_only is True)
        self._gate("model_promotion_result_no_real_orders",
                   lambda: StrategyPromotionResult().no_real_orders is True)
        self._gate("model_promotion_package_promotion_only",
                   lambda: PromotionPackage().promotion_package_only is True)
        self._gate("model_rollback_plan_rollback_only",
                   lambda: RollbackPlan().rollback_plan_only is True)
        self._gate("model_rollback_trigger_paper_only",
                   lambda: RollbackTrigger().paper_only is True)
        self._gate("model_approval_checklist_no_broker",
                   lambda: PromotionApprovalChecklist().no_broker is True)
        self._gate("model_evidence_pack_no_margin",
                   lambda: PromotionEvidencePack().no_margin is True)
        self._gate("model_audit_trail_no_leverage",
                   lambda: PromotionAuditTrail().no_leverage is True)
        self._gate("model_dashboard_not_investment_advice",
                   lambda: PromotionDashboard().not_investment_advice is True)
        self._gate("models_count_22", lambda: len(get_all_model_names()) == 22)

        # ── engine (6) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_engine_v193 import (
            build_promotion_package, build_rollback_plan, validate_rollback_plan,
            build_promotion_approval_checklist, build_promotion_recommendation,
            get_engine_info,
        )
        self._gate("engine_blocked_missing_sandbox_source",
                   lambda: build_promotion_package("p1", "", "shadow_001", "c1", "b1")["blocked"] is True)
        self._gate("engine_blocked_missing_shadow_source",
                   lambda: build_promotion_package("p1", "sandbox_001", "", "c1", "b1")["blocked"] is True)
        self._gate("engine_passes_all_inputs",
                   lambda: build_promotion_package("p1", "s1", "sh1", "c1", "b1")["blocked"] is False)
        self._gate("engine_rollback_blocked_no_baseline",
                   lambda: build_rollback_plan("r1", "pkg1", "")["blocked"] is True)
        self._gate("engine_recommendation_blocked_no_evidence",
                   lambda: build_promotion_recommendation("rec1", "pkg1", "NO_CHANGE", "test", [])["blocked"] is True)
        self._gate("engine_checklist_blocked_no_rollback",
                   lambda: build_promotion_approval_checklist("cl1", "pkg1", rollback_plan_present=False)["blocked"] is True)

        # ── report (4) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_report_v193 import (
            export_promotion_summary_as_json, export_rollback_plan_as_json,
            export_promotion_dashboard_as_json, get_report_info,
        )
        self._gate("report_summary_paper_only",
                   lambda: '"paper_only": true' in export_promotion_summary_as_json({}))
        self._gate("report_rollback_no_real_orders",
                   lambda: '"no_real_orders": true' in export_rollback_plan_as_json({}))
        self._gate("report_dashboard_promotion_only",
                   lambda: '"promotion_package_only": true' in export_promotion_dashboard_as_json({}))
        self._gate("report_info_paper_only", lambda: get_report_info()["paper_only"] is True)

        # ── scenarios (4) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_scenarios_v193 import (
            get_all_scenarios, get_scenarios_by_type,
        )
        self._gate("scenarios_count_75", lambda: len(get_all_scenarios()) == 75)
        self._gate("scenarios_all_paper_only",
                   lambda: all(s["paper_only"] is True for s in get_all_scenarios()))
        self._gate("scenarios_have_complete_promotion",
                   lambda: len(get_scenarios_by_type("complete_promotion_package")) >= 1)
        self._gate("scenarios_have_rollback",
                   lambda: len(get_scenarios_by_type("rollback_to_baseline")) >= 1)

        # ── fixtures (4) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_fixtures_v193 import (
            get_all_fixtures,
        )
        self._gate("fixtures_count_75", lambda: len(get_all_fixtures()) == 75)
        self._gate("fixtures_all_paper_only",
                   lambda: all(f["paper_only"] is True for f in get_all_fixtures()))
        self._gate("fixtures_all_no_real_orders",
                   lambda: all(f["no_real_orders"] is True for f in get_all_fixtures()))
        self._gate("fixtures_all_promotion_package_only",
                   lambda: all(f["promotion_package_only"] is True for f in get_all_fixtures()))

        # ── health check (3) ─────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_promotion_health_v193 import (
            run_health_check,
        )
        health = run_health_check()
        self._gate("health_check_pass", lambda: health.status == "PASS")
        self._gate("health_check_min_60", lambda: health.total >= 60)
        self._gate("health_check_no_failures", lambda: health.failed == 0)

        # ── GUI (2) ──────────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._gate("gui_panel_version_193", lambda: PANEL_VERSION in ("1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10", "2.0.0"))
        from gui.small_capital_strategy_panel import get_promotion_tab_names
        self._gate("gui_promotion_tabs_count_3",
                   lambda: len(get_promotion_tab_names()) == 3)

        # ── CLI (4) ──────────────────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        self._gate("cli_promotion_version",
                   lambda: any(c.name == "strategy-promotion-version" for c in PROVIDER_COMMANDS))
        self._gate("cli_promotion_build",
                   lambda: any(c.name == "strategy-promotion-build" for c in PROVIDER_COMMANDS))
        self._gate("cli_promotion_rollback",
                   lambda: any(c.name == "strategy-promotion-rollback" for c in PROVIDER_COMMANDS))
        self._gate("cli_promotion_gate",
                   lambda: any(c.name == "strategy-promotion-gate" for c in PROVIDER_COMMANDS))

        # ── backward compat (4) ──────────────────────────────────────────────
        self._gate("backward_compat_v192_known",
                   lambda: is_known_release(
                       "Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2"))
        self._gate("backward_compat_v191_known",
                   lambda: is_known_release(
                       "Paper Strategy Rule Tuning & Guardrail Lab v1.9.1"))
        self._gate("backward_compat_v190_known",
                   lambda: is_known_release(
                       "Paper Trading Performance Review & Strategy Improvement Lab v1.9.0"))
        self._gate("backward_compat_v179_known",
                   lambda: is_known_release(
                       "Small Capital Strategy Stable Rollup v1.7.9"))

        # ── forbidden actions (3) ─────────────────────────────────────────────
        self._gate("forbidden_buy", lambda: is_forbidden_action("BUY") is True)
        self._gate("forbidden_sell", lambda: is_forbidden_action("SELL") is True)
        self._gate("forbidden_broker_order",
                   lambda: is_forbidden_action("BROKER_ORDER") is True)

        passed = sum(1 for r in self._results if r["passed"])
        failed = sum(1 for r in self._results if not r["passed"])
        total = len(self._results)
        gate_passed = failed == 0
        return {
            "gate_passed": gate_passed,
            "version": self.VERSION,
            "release_name": self.RELEASE_NAME,
            "passed": passed,
            "failed": failed,
            "total": total,
            "results": list(self._results),
            "paper_only": True,
            "research_only": True,
            "promotion_package_only": True,
            "rollback_plan_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
            "schema_version": "193",
        }


def run_release_gate() -> Dict[str, Any]:
    """Run the strategy promotion release gate and return result."""
    return StrategyPromotionReleaseGate().run()


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Strategy Promotion Release Gate v1.9.3: {'PASS' if result['gate_passed'] else 'FAIL'} ({result['passed']}/{result['total']})")
    if result["failed"]:
        for r in result["results"]:
            if not r["passed"]:
                print(f"  [FAIL] {r['name']}: {r['error']}")
