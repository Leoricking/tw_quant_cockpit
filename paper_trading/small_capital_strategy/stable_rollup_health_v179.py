"""
paper_trading/small_capital_strategy/stable_rollup_health_v179.py
Health checks for Small Capital Strategy Stable Rollup v1.7.9. 50+ checks.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Callable, Dict, List

_SCHEMA  = "179"
_POLICY  = "1.7.9-small-capital-strategy-stable-rollup"
_LINEAGE = "paper_trading.small_capital_strategy.stable_rollup_health_v179"

MIN_HEALTH_CHECKS = 50


def _check(name: str, fn: Callable[[], bool]) -> Dict[str, Any]:
    try:
        passed = bool(fn())
        return {"name": name, "passed": passed, "error": None}
    except Exception as e:
        return {"name": name, "passed": False, "error": str(e)}


def _get_all_checks() -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []

    # ── Version checks (8) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.stable_rollup_version_v179 import (
        VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
        get_version_info, verify_version, is_known_release, INCLUDED_RELEASES,
    )
    checks.append(_check("version_179",              lambda: VERSION == "1.7.9"))
    checks.append(_check("release_name_179",         lambda: RELEASE_NAME == "Small Capital Strategy Stable Rollup"))
    checks.append(_check("schema_version_179",       lambda: SCHEMA_VERSION == "179"))
    checks.append(_check("policy_version_179",       lambda: POLICY_VERSION == "1.7.9-small-capital-strategy-stable-rollup"))
    checks.append(_check("verify_version_true",      verify_version))
    checks.append(_check("known_release_v179",       lambda: is_known_release("Small Capital Strategy Stable Rollup")))
    checks.append(_check("known_release_v178",       lambda: is_known_release("Small Capital Strategy Integration")))
    checks.append(_check("included_releases_9",      lambda: len(INCLUDED_RELEASES) == 9))

    # ── Safety checks (10) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.stable_rollup_safety_v179 import (
        run_safety_audit, assert_safe, get_safety_flags, SAFETY_FLAGS,
    )
    checks.append(_check("safety_audit_all_safe",        lambda: run_safety_audit()["all_safe"]))
    checks.append(_check("safety_no_real_order",         lambda: SAFETY_FLAGS["real_order"] is False))
    checks.append(_check("safety_no_broker_exec",        lambda: SAFETY_FLAGS["broker_execution"] is False))
    checks.append(_check("safety_paper_only",            lambda: SAFETY_FLAGS["paper_only"] is True))
    checks.append(_check("safety_research_only",         lambda: SAFETY_FLAGS["research_only"] is True))
    checks.append(_check("safety_no_real_orders",        lambda: SAFETY_FLAGS["no_real_orders"] is True))
    checks.append(_check("safety_no_broker",             lambda: SAFETY_FLAGS["no_broker"] is True))
    checks.append(_check("safety_no_margin",             lambda: SAFETY_FLAGS["no_margin"] is True))
    checks.append(_check("safety_assert_no_raise",       lambda: (assert_safe(), True)[1]))
    checks.append(_check("safety_production_blocked",    lambda: SAFETY_FLAGS["production_trading_blocked"] is True))

    # ── Manifest checks (5) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.stable_rollup_manifest_v179 import (
        get_manifest, validate_manifest, REQUIRED_CLI_COMMANDS, REQUIRED_GUI_TABS,
    )
    checks.append(_check("manifest_valid",               validate_manifest))
    checks.append(_check("manifest_cli_12",              lambda: len(REQUIRED_CLI_COMMANDS) >= 12))
    checks.append(_check("manifest_gui_tabs_3",          lambda: len(REQUIRED_GUI_TABS) >= 3))
    checks.append(_check("manifest_dict",                lambda: isinstance(get_manifest(), dict)))
    checks.append(_check("manifest_no_real_orders",      lambda: get_manifest()["no_real_orders"] is True))

    # ── Model checks (5) ─────────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.stable_rollup_models_v179 import (
        StableRollupVersionEntry, StableRollupCompatResult,
        StableRollupAuditResult, StableRollupHealthSummary, StableRollupReport,
        get_all_model_names,
    )
    checks.append(_check("model_version_entry",          lambda: StableRollupVersionEntry().paper_only is True))
    checks.append(_check("model_compat_result",          lambda: StableRollupCompatResult().no_real_orders is True))
    checks.append(_check("model_audit_result",           lambda: StableRollupAuditResult().no_broker is True))
    checks.append(_check("model_health_summary",         lambda: StableRollupHealthSummary().not_investment_advice is True))
    checks.append(_check("model_names_5",                lambda: len(get_all_model_names()) == 5))

    # ── Compatibility checks (10) ─────────────────────────────────────────────
    from paper_trading.small_capital_strategy.stable_rollup_compatibility_v179 import (
        run_compatibility_check, is_backward_compatible,
    )
    checks.append(_check("compat_all_9_pass",            lambda: run_compatibility_check()["all_compatible"]))
    checks.append(_check("compat_v170",                  lambda: is_backward_compatible("v1.7.0")))
    checks.append(_check("compat_v171",                  lambda: is_backward_compatible("v1.7.1")))
    checks.append(_check("compat_v172",                  lambda: is_backward_compatible("v1.7.2")))
    checks.append(_check("compat_v173",                  lambda: is_backward_compatible("v1.7.3")))
    checks.append(_check("compat_v174",                  lambda: is_backward_compatible("v1.7.4")))
    checks.append(_check("compat_v175",                  lambda: is_backward_compatible("v1.7.5")))
    checks.append(_check("compat_v176",                  lambda: is_backward_compatible("v1.7.6")))
    checks.append(_check("compat_v177",                  lambda: is_backward_compatible("v1.7.7")))
    checks.append(_check("compat_v178",                  lambda: is_backward_compatible("v1.7.8")))

    # ── CLI audit checks (3) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.stable_rollup_cli_audit_v179 import (
        run_cli_audit, get_required_stable_commands,
    )
    checks.append(_check("cli_all_registered",           lambda: run_cli_audit()["all_registered"]))
    checks.append(_check("cli_count_ge_12",              lambda: run_cli_audit()["registered_count"] >= 12))
    checks.append(_check("cli_required_12",              lambda: len(get_required_stable_commands()) == 12))

    # ── GUI audit checks (4) ──────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.stable_rollup_gui_audit_v179 import (
        run_gui_audit, get_required_stable_tabs,
    )
    checks.append(_check("gui_stable_tabs_present",      lambda: run_gui_audit()["all_tabs_present"]))
    checks.append(_check("gui_render_clean",             lambda: run_gui_audit()["render_clean"]))
    checks.append(_check("gui_panel_version_179",        lambda: run_gui_audit()["panel_version"] in ("1.7.9", "1.8.0", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4")))
    checks.append(_check("gui_required_tabs_3",          lambda: len(get_required_stable_tabs()) == 3))

    # ── Fixture audit checks (3) ──────────────────────────────────────────────
    from paper_trading.small_capital_strategy.stable_rollup_fixture_audit_v179 import run_fixture_audit
    checks.append(_check("fixture_audit_all_safe",       lambda: run_fixture_audit()["all_safe"]))
    checks.append(_check("fixture_total_ge_50",          lambda: run_fixture_audit()["total_fixtures"] >= 50))
    checks.append(_check("fixture_no_violations",        lambda: run_fixture_audit()["violation_count"] == 0))

    # ── Scenario audit checks (3) ─────────────────────────────────────────────
    from paper_trading.small_capital_strategy.stable_rollup_scenario_audit_v179 import run_scenario_audit
    checks.append(_check("scenario_audit_all_clean",     lambda: run_scenario_audit()["all_clean"]))
    checks.append(_check("scenario_total_ge_50",         lambda: run_scenario_audit()["total_scenarios"] >= 50))
    checks.append(_check("scenario_no_forbidden",        lambda: run_scenario_audit()["forbidden_count"] == 0))

    # ── Regression audit checks (3) ───────────────────────────────────────────
    from paper_trading.small_capital_strategy.stable_rollup_regression_audit_v179 import run_regression_audit
    checks.append(_check("regression_audit_clean",       lambda: run_regression_audit()["all_clean"]))
    checks.append(_check("regression_no_issues",         lambda: run_regression_audit()["issue_count"] == 0))
    checks.append(_check("regression_safety_required",   lambda: run_regression_audit()["all_clean"] is True))

    # ── No-real-orders checks (3) ─────────────────────────────────────────────
    checks.append(_check("no_broker_flag",               lambda: SAFETY_FLAGS["no_broker"] is True))
    checks.append(_check("no_real_orders_flag",          lambda: SAFETY_FLAGS["no_real_orders"] is True))
    checks.append(_check("no_margin_flag",               lambda: SAFETY_FLAGS["no_margin"] is True))

    # ── Report checks (2) ─────────────────────────────────────────────────────
    from paper_trading.small_capital_strategy.stable_rollup_report_v179 import build_report, get_report_sections
    checks.append(_check("report_sections_11",           lambda: len(get_report_sections()) == 11))
    checks.append(_check("report_paper_only",            lambda: build_report()["paper_only"] is True))

    return checks


def run_health_check():
    """Run all health checks and return StableRollupHealthSummary."""
    from paper_trading.small_capital_strategy.stable_rollup_models_v179 import StableRollupHealthSummary
    checks = _get_all_checks()
    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    total  = len(checks)
    all_passed = failed == 0
    return StableRollupHealthSummary(
        status="PASS" if all_passed else "FAIL",
        passed=passed,
        failed=failed,
        total=total,
        all_passed=all_passed,
        checks=checks,
    )


if __name__ == "__main__":
    result = run_health_check()
    print(f"Stable Rollup Health v1.7.9: {result.status}  {result.passed}/{result.total}")
    if result.failed:
        for c in result.checks:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
