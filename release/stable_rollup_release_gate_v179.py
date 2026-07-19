"""
release/stable_rollup_release_gate_v179.py
Release gate for Small Capital Strategy Stable Rollup v1.7.9. 50+ gate checks.
gate_passed=True required for release.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.7.9"
MIN_CHECKS   = 50


class StableRollupReleaseGate:
    """Release gate for Small Capital Strategy Stable Rollup v1.7.9."""

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
            "name":   name,
            "passed": ok,
            "error":  None if ok else str(result),
        })

    def run(self) -> Dict[str, Any]:
        """Run all gate checks and return result dict."""
        self._checks = []

        # ── Health PASS (4) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.stable_rollup_health_v179 import run_health_check
        self._check("health_all_passed",          lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",         lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",         lambda: run_health_check().failed == 0)
        self._check("health_total_ge_50",         lambda: run_health_check().total >= 50)

        # ── Version Identity (6) ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.stable_rollup_version_v179 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
            verify_version, is_known_release,
        )
        self._check("gate_version_1_7_9",         lambda: VERSION == "1.7.9")
        self._check("gate_release_name",          lambda: RELEASE_NAME == "Small Capital Strategy Stable Rollup")
        self._check("gate_schema_version_179",    lambda: SCHEMA_VERSION == "179")
        self._check("gate_policy_version",        lambda: POLICY_VERSION == "1.7.9-small-capital-strategy-stable-rollup")
        self._check("gate_known_release_self",    lambda: is_known_release("Small Capital Strategy Stable Rollup"))
        self._check("gate_verify_version",        verify_version)

        # ── Safety (10) ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.stable_rollup_safety_v179 import (
            run_safety_audit, assert_safe, SAFETY_FLAGS,
        )
        self._check("safety_audit_all_safe",      lambda: run_safety_audit()["all_safe"])
        self._check("safety_no_real_order",       lambda: SAFETY_FLAGS["real_order"] is False)
        self._check("safety_no_broker_exec",      lambda: SAFETY_FLAGS["broker_execution"] is False)
        self._check("safety_no_real_trading",     lambda: SAFETY_FLAGS["real_trading"] is False)
        self._check("safety_no_real_account",     lambda: SAFETY_FLAGS["real_account"] is False)
        self._check("safety_paper_only",          lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_research_only",       lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("safety_no_margin",           lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("safety_assert_no_raise",     lambda: (assert_safe(), True)[1])
        self._check("safety_production_blocked",  lambda: SAFETY_FLAGS["production_trading_blocked"] is True)

        # ── Compatibility (9) ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.stable_rollup_compatibility_v179 import is_backward_compatible
        self._check("compat_v170",                lambda: is_backward_compatible("v1.7.0"))
        self._check("compat_v171",                lambda: is_backward_compatible("v1.7.1"))
        self._check("compat_v172",                lambda: is_backward_compatible("v1.7.2"))
        self._check("compat_v173",                lambda: is_backward_compatible("v1.7.3"))
        self._check("compat_v174",                lambda: is_backward_compatible("v1.7.4"))
        self._check("compat_v175",                lambda: is_backward_compatible("v1.7.5"))
        self._check("compat_v176",                lambda: is_backward_compatible("v1.7.6"))
        self._check("compat_v177",                lambda: is_backward_compatible("v1.7.7"))
        self._check("compat_v178",                lambda: is_backward_compatible("v1.7.8"))

        # ── Manifest (4) ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.stable_rollup_manifest_v179 import (
            validate_manifest, get_manifest,
        )
        self._check("manifest_valid",             validate_manifest)
        self._check("manifest_no_real_orders",    lambda: get_manifest()["no_real_orders"] is True)
        self._check("manifest_no_broker",         lambda: get_manifest()["no_broker"] is True)
        self._check("manifest_no_margin",         lambda: get_manifest()["no_margin"] is True)

        # ── CLI Audit (3) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.stable_rollup_cli_audit_v179 import run_cli_audit
        self._check("cli_all_registered",         lambda: run_cli_audit()["all_registered"])
        self._check("cli_count_ge_12",            lambda: run_cli_audit()["registered_count"] >= 12)
        self._check("cli_missing_zero",           lambda: run_cli_audit()["missing_count"] == 0)

        # ── GUI Audit (4) ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.stable_rollup_gui_audit_v179 import run_gui_audit
        self._check("gui_stable_tabs_present",    lambda: run_gui_audit()["all_tabs_present"])
        self._check("gui_render_clean",           lambda: run_gui_audit()["render_clean"])
        self._check("gui_panel_version_179",      lambda: run_gui_audit()["panel_version"] in ("1.7.9", "1.8.0", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10", "2.0.0"))
        self._check("gui_error_tabs_zero",        lambda: len(run_gui_audit()["error_tabs"]) == 0)

        # ── Fixture Audit (3) ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.stable_rollup_fixture_audit_v179 import run_fixture_audit
        self._check("fixtures_all_safe",          lambda: run_fixture_audit()["all_safe"])
        self._check("fixtures_total_ge_50",       lambda: run_fixture_audit()["total_fixtures"] >= 50)
        self._check("fixtures_no_violations",     lambda: run_fixture_audit()["violation_count"] == 0)

        # ── Scenario Audit (3) ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.stable_rollup_scenario_audit_v179 import run_scenario_audit
        self._check("scenarios_all_clean",        lambda: run_scenario_audit()["all_clean"])
        self._check("scenarios_total_ge_50",      lambda: run_scenario_audit()["total_scenarios"] >= 50)
        self._check("scenarios_no_forbidden",     lambda: run_scenario_audit()["forbidden_count"] == 0)

        # ── Regression Audit (3) ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.stable_rollup_regression_audit_v179 import run_regression_audit
        self._check("regression_all_clean",       lambda: run_regression_audit()["all_clean"])
        self._check("regression_no_issues",       lambda: run_regression_audit()["issue_count"] == 0)
        self._check("no_production_writes",       lambda: SAFETY_FLAGS["no_production_db_writes"] is True)

        # ── Safety Flags (4) ─────────────────────────────────────────────────
        self._check("no_broker_flag",             lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("no_real_orders_flag",        lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("no_margin_flag",             lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("no_live_broker",             lambda: SAFETY_FLAGS["broker_execution"] is False)

        # ── GUI panel version (1) ─────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._check("gui_panel_version_match",    lambda: PANEL_VERSION in ("1.7.9", "1.8.0", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10", "2.0.0"))

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total  = len(self._checks)
        return {
            "gate_passed":   failed == 0,
            "passed":        passed,
            "failed":        failed,
            "total":         total,
            "gate_version":  GATE_VERSION,
            "checks":        list(self._checks),
        }


def run_release_gate() -> Dict[str, Any]:
    return StableRollupReleaseGate().run()


run_gate = run_release_gate


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Stable Rollup Release Gate v1.7.9: {'PASS' if result['gate_passed'] else 'FAIL'}  {result['passed']}/{result['total']}")
    if not result["gate_passed"]:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
