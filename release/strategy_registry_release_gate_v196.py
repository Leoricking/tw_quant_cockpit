"""
release/strategy_registry_release_gate_v196.py
Release gate for Paper Strategy Decision Registry & Governance Lab v1.9.6.
gate_passed=True required for release.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.9.6"
MIN_CHECKS = 50
BASELINE_TESTS = 29358
MIN_NEW_TESTS = 400
MIN_SCENARIOS = 75
MIN_FIXTURES = 75
MIN_CLI = 18


class StrategyRegistryReleaseGate:
    """Release gate for Paper Strategy Decision Registry & Governance Lab v1.9.6."""

    GATE_VERSION = "1.9.6"
    MIN_SCENARIOS = 75
    MIN_FIXTURES = 75
    MIN_CLI = 18
    BASELINE_TESTS = 29358
    MIN_NEW_TESTS = 400

    def __init__(self) -> None:
        self._checks: List[Dict[str, Any]] = []

    def _check(self, name: str, fn) -> None:
        try:
            result = fn()
            ok = bool(result)
        except Exception as exc:
            ok = False
            result = str(exc)
        self._checks.append({
            "name": name,
            "passed": ok,
            "error": None if ok else str(result),
        })

    def run(self) -> Dict[str, Any]:
        """Run all gate checks and return result dict."""
        self._checks = []

        # ── Health PASS (4) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_health_v196 import run_health_check
        self._check("health_all_passed", lambda: run_health_check()["all_passed"] is True)
        self._check("health_status_pass", lambda: run_health_check()["status"] == "PASS")
        self._check("health_failed_zero", lambda: run_health_check()["failed"] == 0)
        self._check("health_total_ge_60", lambda: run_health_check()["total"] >= 60)

        # ── Version Identity (8) ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_version_v196 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
            verify_version, is_known_release,
            get_decision_sources, get_decision_types, get_decision_states,
            get_governance_checks, get_hard_block_conditions,
            get_forbidden_registry_actions, get_allowed_registry_actions,
        )
        self._check("gate_version_1_9_6", lambda: VERSION == "1.9.6")
        self._check("gate_release_name",
                    lambda: RELEASE_NAME == "Paper Strategy Decision Registry & Governance Lab")
        self._check("gate_schema_version_196", lambda: SCHEMA_VERSION == "196")
        self._check("gate_policy_version",
                    lambda: POLICY_VERSION == "1.9.6-small-capital-strategy-paper-strategy-decision-registry-governance-lab")
        self._check("gate_known_release_self",
                    lambda: is_known_release("Paper Strategy Decision Registry & Governance Lab v1.9.6"))
        self._check("gate_verify_version", verify_version)
        self._check("gate_decision_sources_count_10", lambda: len(get_decision_sources()) == 10)
        self._check("gate_decision_types_count_10", lambda: len(get_decision_types()) == 10)

        # ── Governance & States (4) ──────────────────────────────────────────
        self._check("gate_decision_states_count_12", lambda: len(get_decision_states()) == 12)
        self._check("gate_governance_checks_count_19", lambda: len(get_governance_checks()) == 19)
        self._check("gate_hard_block_conditions_count_20",
                    lambda: len(get_hard_block_conditions()) == 20)
        self._check("gate_allowed_registry_actions_count_18",
                    lambda: len(get_allowed_registry_actions()) == 18)

        # ── Safety (10) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_safety_v196 import (
            SAFETY_FLAGS, run_safety_audit, assert_safe,
            FORBIDDEN_REGISTRY_ACTIONS, ALLOWED_REGISTRY_ACTIONS, HARD_BLOCK_CONDITIONS,
        )
        self._check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"] is True)
        self._check("safety_no_real_order", lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("safety_no_broker_exec", lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_governance_only", lambda: SAFETY_FLAGS["governance_only"] is True)
        self._check("safety_no_production_mutation",
                    lambda: SAFETY_FLAGS["no_production_strategy_mutation"] is True)
        self._check("safety_no_automatic_rollback",
                    lambda: SAFETY_FLAGS["no_automatic_rollback"] is True)
        self._check("safety_no_live_activation",
                    lambda: SAFETY_FLAGS["no_live_strategy_activation"] is True)
        self._check("safety_immutable_decision_record",
                    lambda: SAFETY_FLAGS["immutable_decision_record"] is True)
        self._check("safety_assert_no_raise", lambda: (assert_safe(), True)[1])

        # ── Models (6) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_models_v196 import (
            StrategyDecisionRegistryInput, StrategyDecisionRegistryResult,
            StrategyDecisionRecord, StrategyDecisionQueue, StrategyDecisionHealthSummary,
            StrategyDecisionRetentionPolicy,
        )
        self._check("model_registry_input_paper_only",
                    lambda: StrategyDecisionRegistryInput().paper_only is True)
        self._check("model_registry_result_paper_only",
                    lambda: StrategyDecisionRegistryResult().paper_only is True)
        self._check("model_decision_record_immutable",
                    lambda: StrategyDecisionRecord().immutable is True)
        self._check("model_decision_queue_no_auto_processing",
                    lambda: StrategyDecisionQueue().auto_processing is False)
        self._check("model_health_summary_schema_196",
                    lambda: StrategyDecisionHealthSummary().schema_version == "196")
        self._check("model_retention_no_auto_deletion",
                    lambda: StrategyDecisionRetentionPolicy().auto_deletion is False)

        # ── Engine (6) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_engine_v196 import (
            validate_registry_action, build_decision_record, build_governance_check,
            build_evidence_pack, build_audit_trail, get_engine_info,
        )
        self._check("engine_info_paper_only",
                    lambda: get_engine_info()["paper_only"] is True)
        self._check("engine_buy_blocked",
                    lambda: validate_registry_action("BUY")["blocked"] is True)
        self._check("engine_governance_check_valid",
                    lambda: validate_registry_action("GOVERNANCE_CHECK")["valid"] is True)
        self._check("engine_record_missing_id_blocked",
                    lambda: build_decision_record("", "TUNING_PROPOSAL",
                                                   "APPROVE_FOR_PAPER_ONLY", "r")["blocked"] is True)
        self._check("engine_governance_blocked_empty_evidence",
                    lambda: build_governance_check("DEC-001", [], "rationale")["blocked"] is True)
        self._check("engine_evidence_pack_blocked_missing_id",
                    lambda: build_evidence_pack("", ["e1"])["blocked"] is True)

        # ── Report (4) ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_report_v196 import (
            export_decision_record_report, export_full_registry_pack,
            get_report_section_names, export_governance_report,
        )
        self._check("report_sections_ge_10",
                    lambda: len(get_report_section_names()) >= 10)
        self._check("report_record_blocked_empty",
                    lambda: export_decision_record_report("")["blocked"] is True)
        self._check("report_full_pack_valid",
                    lambda: export_full_registry_pack("DEC-001")["valid"] is True)
        self._check("report_governance_report_valid",
                    lambda: export_governance_report("DEC-001")["valid"] is True)

        # ── Scenarios (4) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_scenarios_v196 import (
            get_all_scenarios, get_scenario_count, get_scenario_by_id,
        )
        self._check("scenarios_count_75", lambda: get_scenario_count() == 75)
        self._check("scenarios_ge_min", lambda: get_scenario_count() >= MIN_SCENARIOS)
        self._check("scenarios_all_paper_only",
                    lambda: all(s["paper_only"] for s in get_all_scenarios()))
        self._check("scenario_by_id_found",
                    lambda: get_scenario_by_id("SP196-001").get("scenario_id") == "SP196-001")

        # ── Fixtures (4) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_fixtures_v196 import (
            get_all_fixtures, get_fixture_count, get_fixture_by_id,
        )
        self._check("fixtures_count_75", lambda: get_fixture_count() == 75)
        self._check("fixtures_ge_min", lambda: get_fixture_count() >= MIN_FIXTURES)
        self._check("fixtures_all_paper_only",
                    lambda: all(f["paper_only"] for f in get_all_fixtures()))
        self._check("fixture_by_id_found",
                    lambda: get_fixture_by_id("SMF196-001") is not None)

        # ── GUI (3) ──────────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION, get_registry_tab_names
        self._check("gui_panel_version_196",
                    lambda: PANEL_VERSION in ("1.9.6",))
        self._check("gui_registry_tabs_present",
                    lambda: "decision_registry" in get_registry_tab_names())
        self._check("gui_registry_tab_count_3",
                    lambda: len(get_registry_tab_names()) == 3)

        # ── CLI (3) ──────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_registry_version_v196 import MIN_CLI
        self._check("min_cli_18", lambda: MIN_CLI >= 18)
        self._check("allowed_actions_covers_min_cli",
                    lambda: len(get_allowed_registry_actions()) >= MIN_CLI)
        self._check("cli_registry_version_in_allowed",
                    lambda: "REGISTRY_VERSION" in get_allowed_registry_actions())

        # ── Baseline test count (2) ───────────────────────────────────────────
        self._check("baseline_tests_29358", lambda: BASELINE_TESTS == 29358)
        self._check("min_new_tests_400", lambda: MIN_NEW_TESTS >= 400)

        # ── Backward compat (4) ──────────────────────────────────────────────
        self._check("backward_compat_v195",
                    lambda: is_known_release("Paper Strategy Review Alert & Human Approval Lab v1.9.5"))
        self._check("backward_compat_v194",
                    lambda: is_known_release("Paper Strategy Monitoring & Drift Detection Lab v1.9.4"))
        self._check("backward_compat_v193",
                    lambda: is_known_release("Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3"))
        self._check("backward_compat_panel_version",
                    lambda: PANEL_VERSION in ("1.9.6",))

        # ── Panel version check (1) ───────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION as _PV
        self._check("gui_panel_version_match", lambda: _PV in ("1.9.6",))

        passed_count = sum(1 for c in self._checks if c["passed"])
        failed_count = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)
        return {
            "gate_passed": failed_count == 0,
            "passed": passed_count,
            "failed": failed_count,
            "passed_count": passed_count,
            "failed_count": failed_count,
            "total": total,
            "gate_version": GATE_VERSION,
            "checks": list(self._checks),
            "paper_only": True,
            "no_real_orders": True,
            "governance_only": True,
            "registry_only": True,
            "decision_record_only": True,
            "not_investment_advice": True,
            "schema_version": "196",
        }


def run_release_gate() -> Dict[str, Any]:
    return StrategyRegistryReleaseGate().run()


run_gate = run_release_gate


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Strategy Registry Release Gate v1.9.6: {'PASS' if result['gate_passed'] else 'FAIL'}  "
          f"{result['passed_count']}/{result['total']}")
    if not result["gate_passed"]:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
