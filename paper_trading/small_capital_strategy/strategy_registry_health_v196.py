"""
paper_trading/small_capital_strategy/strategy_registry_health_v196.py
Health check for Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List

MIN_CHECKS = 60


class StrategyRegistryHealthCheck:
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

    def run(self) -> Dict[str, Any]:
        self._checks = []

        # ── version (7) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_version_v196 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
            get_version_info, get_decision_sources, get_decision_types,
            get_decision_states, get_governance_checks, get_hard_block_conditions,
            get_forbidden_registry_actions, get_allowed_registry_actions,
        )
        self._check("version_is_196", lambda: VERSION == "1.9.6")
        self._check("release_name_correct",
                    lambda: RELEASE_NAME == "Paper Strategy Decision Registry & Governance Lab")
        self._check("schema_version_196", lambda: SCHEMA_VERSION == "196")
        self._check("verify_version_returns_true", lambda: verify_version() is True)
        self._check("is_known_release_v196",
                    lambda: is_known_release("Paper Strategy Decision Registry & Governance Lab v1.9.6"))
        self._check("version_info_paper_only", lambda: get_version_info()["paper_only"] is True)
        self._check("version_info_governance_only", lambda: get_version_info()["governance_only"] is True)

        # ── decision sources (3) ──────────────────────────────────────────────
        self._check("decision_sources_count_10", lambda: len(get_decision_sources()) == 10)
        self._check("decision_sources_has_tuning_proposal",
                    lambda: "TUNING_PROPOSAL" in get_decision_sources())
        self._check("decision_sources_has_human_approval_request",
                    lambda: "HUMAN_APPROVAL_REQUEST" in get_decision_sources())

        # ── decision types (3) ────────────────────────────────────────────────
        self._check("decision_types_count_10", lambda: len(get_decision_types()) == 10)
        self._check("decision_types_has_approve_for_paper_only",
                    lambda: "APPROVE_FOR_PAPER_ONLY" in get_decision_types())
        self._check("decision_types_has_no_change",
                    lambda: "NO_CHANGE" in get_decision_types())

        # ── decision states (3) ───────────────────────────────────────────────
        self._check("decision_states_count_12", lambda: len(get_decision_states()) == 12)
        self._check("decision_states_has_recorded",
                    lambda: "RECORDED" in get_decision_states())
        self._check("decision_states_has_archived",
                    lambda: "ARCHIVED" in get_decision_states())

        # ── governance checks (3) ────────────────────────────────────────────
        self._check("governance_checks_count_19", lambda: len(get_governance_checks()) == 19)
        self._check("governance_checks_has_decision_id_present",
                    lambda: "decision_id_present" in get_governance_checks())
        self._check("governance_checks_has_audit_trail_present",
                    lambda: "audit_trail_present" in get_governance_checks())

        # ── hard block conditions (3) ─────────────────────────────────────────
        self._check("hard_block_conditions_count_20",
                    lambda: len(get_hard_block_conditions()) == 20)
        self._check("hard_block_has_real_order_requested",
                    lambda: "real_order_requested" in get_hard_block_conditions())
        self._check("hard_block_has_duplicate_decision_id",
                    lambda: "duplicate_decision_id" in get_hard_block_conditions())

        # ── forbidden / allowed actions (4) ──────────────────────────────────
        self._check("forbidden_registry_actions_count_9",
                    lambda: len(get_forbidden_registry_actions()) == 9)
        self._check("allowed_registry_actions_count_18",
                    lambda: len(get_allowed_registry_actions()) == 18)
        self._check("forbidden_has_broker_order",
                    lambda: "BROKER_ORDER" in get_forbidden_registry_actions())
        self._check("allowed_has_governance_check",
                    lambda: "GOVERNANCE_CHECK" in get_allowed_registry_actions())

        # ── safety (10) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_safety_v196 import (
            SAFETY_FLAGS, run_safety_audit, assert_safe,
            is_forbidden_action, is_allowed_action, validate_registry_action,
            FORBIDDEN_REGISTRY_ACTIONS, ALLOWED_REGISTRY_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_flag_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_flag_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_flag_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_flag_governance_only", lambda: SAFETY_FLAGS["governance_only"] is True)
        self._check("safety_flag_registry_only", lambda: SAFETY_FLAGS["registry_only"] is True)
        self._check("safety_flag_no_production_mutation",
                    lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._check("safety_flag_no_automatic_rollback",
                    lambda: SAFETY_FLAGS["no_automatic_rollback"] is True)
        self._check("safety_flag_no_live_activation",
                    lambda: SAFETY_FLAGS["no_live_strategy_activation"] is True)
        self._check("safety_assert_no_raise", lambda: (assert_safe(), True)[1])

        # ── models (8) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_models_v196 import (
            StrategyDecisionRegistryInput, StrategyDecisionRegistryResult,
            StrategyDecisionRecord, StrategyDecisionId, StrategyDecisionSource,
            StrategyDecisionType, StrategyDecisionState, StrategyDecisionOwner,
            StrategyDecisionRationale, StrategyDecisionEvidenceLink,
            StrategyDecisionEvidencePack, StrategyDecisionLineage,
            StrategyDecisionGovernancePolicy, StrategyDecisionGovernanceResult,
            StrategyDecisionChecklist, StrategyDecisionViolation,
            StrategyDecisionRiskSummary, StrategyDecisionImpactSummary,
            StrategyDecisionExportManifest, StrategyDecisionAuditTrail,
            StrategyDecisionDashboard, StrategyDecisionQueue,
            StrategyDecisionQueueSummary, StrategyDecisionHealthSummary,
            StrategyDecisionValidationResult, StrategyDecisionRetentionPolicy,
        )
        self._check("model_registry_input_paper_only",
                    lambda: StrategyDecisionRegistryInput().paper_only is True)
        self._check("model_registry_result_paper_only",
                    lambda: StrategyDecisionRegistryResult().paper_only is True)
        self._check("model_decision_record_paper_only",
                    lambda: StrategyDecisionRecord().paper_only is True)
        self._check("model_decision_record_immutable",
                    lambda: StrategyDecisionRecord().immutable is True)
        self._check("model_decision_queue_no_auto_processing",
                    lambda: StrategyDecisionQueue().auto_processing is False)
        self._check("model_decision_queue_requires_human_review",
                    lambda: StrategyDecisionQueue().requires_human_review is True)
        self._check("model_governance_result_paper_only",
                    lambda: StrategyDecisionGovernanceResult().paper_only is True)
        self._check("model_retention_no_auto_deletion",
                    lambda: StrategyDecisionRetentionPolicy().auto_deletion is False)

        # ── engine (6) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_engine_v196 import (
            validate_registry_action, validate_decision_source, validate_decision_type,
            validate_decision_state, build_decision_record, build_governance_check,
            build_decision_queue, build_evidence_pack, build_audit_trail,
            build_registry_dashboard, build_export_manifest, build_decision_lineage,
            build_registry_report, get_engine_info,
        )
        self._check("engine_info_paper_only",
                    lambda: get_engine_info()["paper_only"] is True)
        self._check("engine_validate_action_buy_blocked",
                    lambda: validate_registry_action("BUY")["blocked"] is True)
        self._check("engine_validate_action_governance_check_valid",
                    lambda: validate_registry_action("GOVERNANCE_CHECK")["valid"] is True)
        self._check("engine_build_record_missing_id_blocked",
                    lambda: build_decision_record("", "TUNING_PROPOSAL", "APPROVE_FOR_PAPER_ONLY",
                                                   "rationale")["blocked"] is True)
        self._check("engine_build_governance_check_blocked_missing_evidence",
                    lambda: build_governance_check("DEC-001", [], "rationale")["blocked"] is True)
        self._check("engine_build_evidence_pack_blocked_missing_id",
                    lambda: build_evidence_pack("", ["ev1"])["blocked"] is True)

        # ── report (4) ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_report_v196 import (
            export_decision_record_report, export_governance_report,
            export_full_registry_pack, get_report_section_names,
            export_audit_trail_report, export_lineage_report,
        )
        self._check("report_sections_count_ge_10",
                    lambda: len(get_report_section_names()) >= 10)
        self._check("report_export_record_blocked_missing_id",
                    lambda: export_decision_record_report("")["blocked"] is True)
        self._check("report_full_pack_paper_only",
                    lambda: export_full_registry_pack("DEC-001")["paper_only"] is True)
        self._check("report_full_pack_auto_rollback_false",
                    lambda: export_full_registry_pack("DEC-001")["auto_rollback"] is False)

        # ── scenarios (3) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_scenarios_v196 import (
            get_all_scenarios, get_scenario_count, get_scenario_by_id,
        )
        self._check("scenarios_count_75", lambda: get_scenario_count() == 75)
        self._check("scenarios_all_paper_only",
                    lambda: all(s["paper_only"] for s in get_all_scenarios()))
        self._check("scenario_by_id_found",
                    lambda: get_scenario_by_id("SP196-001").get("scenario_id") == "SP196-001")

        # ── fixtures (3) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_fixtures_v196 import (
            get_all_fixtures, get_fixture_count, get_fixture_by_id,
        )
        self._check("fixtures_count_75", lambda: get_fixture_count() == 75)
        self._check("fixtures_all_paper_only",
                    lambda: all(f["paper_only"] for f in get_all_fixtures()))
        self._check("fixture_by_id_found",
                    lambda: get_fixture_by_id("SMF196-001") is not None)

        # ── CLI (2) ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_version_v196 import MIN_CLI
        self._check("min_cli_18", lambda: MIN_CLI >= 18)
        self._check("allowed_actions_covers_cli",
                    lambda: len(get_allowed_registry_actions()) >= MIN_CLI)

        # ── backward compat (4) ──────────────────────────────────────────────
        self._check("backward_compat_v195",
                    lambda: is_known_release("Paper Strategy Review Alert & Human Approval Lab v1.9.5"))
        self._check("backward_compat_v194",
                    lambda: is_known_release("Paper Strategy Monitoring & Drift Detection Lab v1.9.4"))
        self._check("backward_compat_v193",
                    lambda: is_known_release("Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3"))
        self._check("backward_compat_v190",
                    lambda: is_known_release("Paper Trading Performance Review & Strategy Improvement Lab v1.9.0"))

        # ── forbidden action words (3) ────────────────────────────────────────
        self._check("forbidden_buy_blocked",
                    lambda: is_forbidden_action("BUY") is True)
        self._check("forbidden_sell_blocked",
                    lambda: is_forbidden_action("SELL") is True)
        self._check("forbidden_broker_order_blocked",
                    lambda: is_forbidden_action("BROKER_ORDER") is True)

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)
        return {
            "all_passed": failed == 0,
            "status": "PASS" if failed == 0 else "FAIL",
            "passed": passed,
            "failed": failed,
            "total": total,
            "checks": list(self._checks),
            "paper_only": True,
            "governance_only": True,
            "registry_only": True,
            "no_real_orders": True,
            "schema_version": "196",
        }


def run_health_check() -> Dict[str, Any]:
    return StrategyRegistryHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Strategy Registry Health v1.9.6: {'PASS' if result['all_passed'] else 'FAIL'}  "
          f"{result['passed']}/{result['total']}")
    if not result["all_passed"]:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
