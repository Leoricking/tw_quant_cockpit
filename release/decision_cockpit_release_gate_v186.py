"""
release/decision_cockpit_release_gate_v186.py
Release gate for End-to-End Small Capital Decision Cockpit v1.8.6. 60+ gate checks.
gate_passed=True required for release.
[!] Research Only. Paper Only. Decision Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.8.6"
MIN_CHECKS   = 60


class DecisionCockpitReleaseGate:
    """Release gate for End-to-End Small Capital Decision Cockpit v1.8.6."""

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
        """Run all gate checks and return result dict."""
        self._checks = []

        # ── Health PASS (4) ──────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_health_v186 import run_health_check
        self._check("health_all_passed",           lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",          lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",          lambda: run_health_check().failed == 0)
        self._check("health_total_ge_60",          lambda: run_health_check().total >= 60)

        # ── Version Identity (5) ─────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_version_v186 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
        )
        self._check("gate_version_1_8_6",          lambda: VERSION == "1.8.6")
        self._check("gate_release_name",           lambda: RELEASE_NAME == "End-to-End Small Capital Decision Cockpit")
        self._check("gate_schema_version_186",     lambda: SCHEMA_VERSION == "186")
        self._check("gate_verify_version",         verify_version)
        self._check("gate_known_release_v185",     lambda: is_known_release("Portfolio Construction & Rebalancing Lab v1.8.5"))

        # ── Safety (10) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_safety_v186 import (
            run_safety_audit, assert_safe, SAFETY_FLAGS,
        )
        self._check("safety_audit_all_safe",       lambda: run_safety_audit()["all_safe"])
        self._check("safety_paper_only",           lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_research_only",        lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("safety_decision_only",        lambda: SAFETY_FLAGS["decision_only"] is True)
        self._check("safety_no_real_orders",       lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_no_broker",            lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_no_margin",            lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("safety_no_leverage",          lambda: SAFETY_FLAGS["no_leverage"] is True)
        self._check("safety_production_blocked",   lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_broker_exec_false",    lambda: SAFETY_FLAGS["broker_execution"] is False)

        # ── Models (5) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import (
            DecisionCockpitInput, DecisionCockpitResult,
            DecisionDashboard, DecisionReport, get_all_model_names,
        )
        self._check("model_cockpit_input",         lambda: DecisionCockpitInput().paper_only is True)
        self._check("model_cockpit_result",        lambda: DecisionCockpitResult().paper_only is True)
        self._check("model_dashboard",             lambda: DecisionDashboard().paper_only is True)
        self._check("model_report",                lambda: DecisionReport().paper_only is True)
        self._check("model_count_22",              lambda: len(get_all_model_names()) == 22)

        # ── Engine (10) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_engine_v186 import (
            ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_COCKPIT_GRADES,
            CAPITAL_STAGES, DECISION_CYCLES, CANDIDATE_EVALUATION_CRITERIA,
            validate_action, validate_grade, run_decision_cockpit,
            build_decision_dashboard, get_engine_info,
        )
        self._check("engine_actions_17",           lambda: len(ALLOWED_OUTPUT_ACTIONS) == 17)
        self._check("engine_forbidden_9",          lambda: len(FORBIDDEN_OUTPUT_WORDS) == 9)
        self._check("engine_grades_6",             lambda: len(VALID_COCKPIT_GRADES) == 6)
        self._check("engine_cycles_8",             lambda: len(DECISION_CYCLES) == 8)
        self._check("engine_criteria_14",          lambda: len(CANDIDATE_EVALUATION_CRITERIA) == 14)
        self._check("engine_validate_action",      lambda: validate_action("DECISION_ONLY"))
        self._check("engine_validate_grade",       lambda: validate_grade("READY"))
        _inp = DecisionCockpitInput(capital=300000.0, market_regime="BULL")
        self._check("engine_run_callable",         lambda: run_decision_cockpit(_inp).paper_only is True)
        self._check("engine_info_dict",            lambda: isinstance(get_engine_info(), dict))
        self._check("engine_dashboard_callable",   lambda: build_decision_dashboard(_inp).paper_only is True)

        # ── Decision cockpit results (5) ─────────────────────────────────
        self._check("result_empty_wait",           lambda: run_decision_cockpit(
            DecisionCockpitInput(capital=300000.0)).final_cockpit_grade in ("WAIT", "WATCH", "READY"))
        self._check("result_blocked_regime",       lambda: run_decision_cockpit(
            DecisionCockpitInput(capital=300000.0, market_regime="BLOCKED")).final_cockpit_grade == "BLOCKED")
        self._check("result_high_ruin_blocked",    lambda: run_decision_cockpit(
            DecisionCockpitInput(capital=300000.0, monte_carlo_ruin_risk_pct=25.0)).final_cockpit_grade == "BLOCKED")
        self._check("result_paper_only",           lambda: run_decision_cockpit(_inp).paper_only is True)
        self._check("result_decision_only",        lambda: run_decision_cockpit(_inp).decision_only is True)

        # ── Report (4) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_report_v186 import (
            build_report, get_report_sections, REPORT_SECTIONS,
        )
        _dash = build_decision_dashboard(_inp)
        _rpt = build_report(_dash)
        self._check("report_paper_only",           lambda: _rpt.paper_only is True)
        self._check("report_sections_20",          lambda: len(REPORT_SECTIONS) == 20)
        self._check("report_sections_fn",          lambda: len(get_report_sections()) == 20)
        self._check("report_version_186",          lambda: _rpt.version == "1.8.6")

        # ── CLI (3) ──────────────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        _dc_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("decision-cockpit")]
        self._check("cli_dc_cmds_ge_22",           lambda: len(_dc_cmds) >= 22)
        self._check("cli_version_exists",          lambda: any(c.name == "decision-cockpit-version" for c in PROVIDER_COMMANDS))
        self._check("cli_gate_exists",             lambda: any(c.name == "decision-cockpit-gate" for c in PROVIDER_COMMANDS))

        # ── GUI (4) ──────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION, _TABS
        self._check("gui_panel_version_186",       lambda: PANEL_VERSION in ("1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0"))
        self._check("gui_tabs_ge_141",             lambda: len(_TABS) >= 141)
        self._check("gui_daily_decision_tab",      lambda: "daily_decision_cockpit" in _TABS)
        self._check("gui_weekly_review_tab",       lambda: "weekly_decision_review" in _TABS)

        # ── Scenarios & Fixtures (4) ─────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_scenarios_v186 import (
            count_scenarios, get_scenarios,
        )
        self._check("scenarios_ge_75",             lambda: count_scenarios() >= 75)
        self._check("scenarios_all_paper",         lambda: all(s["paper_only"] for s in get_scenarios()))
        from paper_trading.small_capital_strategy.decision_cockpit_fixtures_v186 import (
            get_fixture_count,
        )
        self._check("fixtures_ge_75",              lambda: get_fixture_count() >= 75)
        self._check("fixture_info_dict",           lambda: isinstance(
            __import__("paper_trading.small_capital_strategy.decision_cockpit_fixtures_v186",
                       fromlist=["get_fixture_info"]).get_fixture_info(), dict))

        # ── Forbidden output words (5) ───────────────────────────────────
        self._check("forbidden_BUY",               lambda: "BUY" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_SELL",              lambda: "SELL" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_ORDER",             lambda: "ORDER" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_EXECUTE",           lambda: "EXECUTE" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_BROKER_ORDER",      lambda: "BROKER_ORDER" in FORBIDDEN_OUTPUT_WORDS)

        # ── Backward compat (5) ──────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_version_v186 import (
            is_known_release as ikr,
        )
        self._check("compat_v170",                 lambda: ikr("Small Capital Strategy v1.7.0"))
        self._check("compat_v180",                 lambda: ikr("Paper Simulation & Performance Lab v1.8.0"))
        self._check("compat_v182",                 lambda: ikr("Parameter Optimization & Walk-Forward Validation Lab v1.8.2"))
        self._check("compat_v183",                 lambda: ikr("Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3"))
        self._check("compat_v185",                 lambda: ikr("Portfolio Construction & Rebalancing Lab v1.8.5"))

        # ── No forbidden action in allowed output (3) ────────────────────
        self._check("no_buy_in_actions",           lambda: "BUY" not in ALLOWED_OUTPUT_ACTIONS)
        self._check("no_sell_in_actions",          lambda: "SELL" not in ALLOWED_OUTPUT_ACTIONS)
        self._check("decision_only_in_actions",    lambda: "DECISION_ONLY" in ALLOWED_OUTPUT_ACTIONS)

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)
        gate_passed = failed == 0 and total >= MIN_CHECKS

        return {
            "gate_version": GATE_VERSION,
            "total": total,
            "passed": passed,
            "failed": failed,
            "gate_passed": gate_passed,
            "min_checks": MIN_CHECKS,
            "checks": self._checks,
            "paper_only": True,
            "decision_only": True,
            "no_real_orders": True,
        }


def run_release_gate() -> Dict[str, Any]:
    """Run decision cockpit release gate."""
    return DecisionCockpitReleaseGate().run()


if __name__ == "__main__":
    result = run_release_gate()
    status = "PASS" if result["gate_passed"] else "FAIL"
    print(f"Release Gate v1.8.6: {status} {result['passed']}/{result['total']}")
    if not result["gate_passed"]:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
