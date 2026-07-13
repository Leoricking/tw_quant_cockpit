"""
release/portfolio_construction_rebalancing_release_gate_v185.py
Release gate for Portfolio Construction & Rebalancing Lab v1.8.5. 60+ gate checks.
gate_passed=True required for release.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.8.5"
MIN_CHECKS   = 60


class PortfolioConstructionRebalancingReleaseGate:
    """Release gate for Portfolio Construction & Rebalancing Lab v1.8.5."""

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
        from paper_trading.small_capital_strategy.portfolio_construction_health_v185 import run_health_check
        self._check("health_all_passed",           lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",          lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",          lambda: run_health_check().failed == 0)
        self._check("health_total_ge_60",          lambda: run_health_check().total >= 60)

        # ── Version Identity (5) ─────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_version_v185 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
        )
        self._check("gate_version_1_8_5",          lambda: VERSION == "1.8.5")
        self._check("gate_release_name",           lambda: RELEASE_NAME == "Portfolio Construction & Rebalancing Lab")
        self._check("gate_schema_version_185",     lambda: SCHEMA_VERSION == "185")
        self._check("gate_verify_version",         verify_version)
        self._check("gate_known_release_v184",     lambda: is_known_release("Position Sizing & Capital Allocation Lab v1.8.4"))

        # ── Safety (10) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_safety_v185 import (
            run_safety_audit, assert_safe, SAFETY_FLAGS,
        )
        self._check("safety_audit_all_safe",       lambda: run_safety_audit()["all_safe"])
        self._check("safety_paper_only",           lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_research_only",        lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("safety_portfolio_only",       lambda: SAFETY_FLAGS["portfolio_only"] is True)
        self._check("safety_no_real_orders",       lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_no_broker",            lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_no_margin",            lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("safety_no_leverage",          lambda: SAFETY_FLAGS["no_leverage"] is True)
        self._check("safety_production_blocked",   lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_broker_exec_false",    lambda: SAFETY_FLAGS["broker_execution"] is False)

        # ── Models (5) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_models_v185 import (
            PortfolioProfile, PortfolioHolding, PortfolioConstructionInput,
            PortfolioConstructionResult, get_all_model_names,
        )
        self._check("model_portfolio_profile",     lambda: PortfolioProfile().paper_only is True)
        self._check("model_portfolio_holding",     lambda: PortfolioHolding().paper_only is True)
        self._check("model_construction_input",    lambda: PortfolioConstructionInput().paper_only is True)
        self._check("model_construction_result",   lambda: PortfolioConstructionResult().paper_only is True)
        self._check("model_count_20",              lambda: len(get_all_model_names()) == 20)

        # ── Engine (8) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_engine_v185 import (
            ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
            validate_action, validate_grade, run_portfolio_construction,
            get_engine_info, build_portfolio_dashboard,
        )
        self._check("engine_actions_16",           lambda: len(ALLOWED_OUTPUT_ACTIONS) == 16)
        self._check("engine_forbidden_9",          lambda: len(FORBIDDEN_OUTPUT_WORDS) == 9)
        self._check("engine_grades_6",             lambda: len(VALID_FINAL_GRADES) == 6)
        self._check("engine_validate_action",      lambda: validate_action("PORTFOLIO_ONLY"))
        self._check("engine_validate_grade",       lambda: validate_grade("BALANCED"))
        _inp = PortfolioConstructionInput(capital=300000.0, market_regime="BULL")
        self._check("engine_run_callable",         lambda: run_portfolio_construction(_inp).paper_only is True)
        self._check("engine_info_dict",            lambda: isinstance(get_engine_info(), dict))
        self._check("engine_dashboard_callable",   lambda: build_portfolio_dashboard(_inp).paper_only is True)

        # ── Portfolio construction results (5) ───────────────────────────
        self._check("result_empty_balanced",       lambda: run_portfolio_construction(
            PortfolioConstructionInput(capital=300000.0)).final_portfolio_grade == "BALANCED")
        self._check("result_blocked_regime",       lambda: run_portfolio_construction(
            PortfolioConstructionInput(capital=300000.0, market_regime="BLOCKED")).final_portfolio_grade == "BLOCKED")
        self._check("result_high_ruin_blocked",    lambda: run_portfolio_construction(
            PortfolioConstructionInput(capital=300000.0, monte_carlo_ruin_risk_pct=25.0)).final_portfolio_grade == "BLOCKED")
        self._check("result_paper_only",           lambda: run_portfolio_construction(_inp).paper_only is True)
        self._check("result_portfolio_only",       lambda: run_portfolio_construction(_inp).portfolio_only is True)

        # ── Report (4) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_report_v185 import (
            build_report, get_report_sections, REPORT_SECTIONS,
        )
        _dash = build_portfolio_dashboard(_inp)
        _rpt = build_report(_dash)
        self._check("report_paper_only",           lambda: _rpt.paper_only is True)
        self._check("report_sections_15",          lambda: len(REPORT_SECTIONS) == 15)
        self._check("report_sections_fn",          lambda: len(get_report_sections()) == 15)
        self._check("report_version_185",          lambda: _rpt.version == "1.8.5")

        # ── CLI (3) ──────────────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        _pc_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("portfolio-construction")]
        self._check("cli_pc_cmds_ge_22",           lambda: len(_pc_cmds) >= 22)
        self._check("cli_version_exists",          lambda: any(c.name == "portfolio-construction-version" for c in PROVIDER_COMMANDS))
        self._check("cli_gate_exists",             lambda: any(c.name == "portfolio-construction-gate" for c in PROVIDER_COMMANDS))

        # ── GUI (4) ──────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION, _TABS
        self._check("gui_panel_version_185",       lambda: PANEL_VERSION == "1.8.5")
        self._check("gui_tabs_ge_138",             lambda: len(_TABS) >= 138)
        self._check("gui_portfolio_construction",  lambda: "portfolio_construction_lab" in _TABS)
        self._check("gui_rebalancing_tab",         lambda: "portfolio_rebalancing" in _TABS)

        # ── Scenarios & Fixtures (4) ─────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_scenarios_v185 import (
            count_scenarios, get_scenarios,
        )
        self._check("scenarios_ge_75",             lambda: count_scenarios() >= 75)
        self._check("scenarios_all_paper",         lambda: all(s["paper_only"] for s in get_scenarios()))
        from paper_trading.small_capital_strategy.portfolio_construction_fixtures_v185 import (
            get_fixture_count,
        )
        self._check("fixtures_ge_75",              lambda: get_fixture_count() >= 75)
        self._check("fixture_info_dict",           lambda: isinstance(
            __import__("paper_trading.small_capital_strategy.portfolio_construction_fixtures_v185",
                       fromlist=["get_fixture_info"]).get_fixture_info(), dict))

        # ── Forbidden output words (5) ───────────────────────────────────
        self._check("forbidden_BUY",               lambda: "BUY" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_SELL",              lambda: "SELL" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_ORDER",             lambda: "ORDER" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_EXECUTE",           lambda: "EXECUTE" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_BROKER_ORDER",      lambda: "BROKER_ORDER" in FORBIDDEN_OUTPUT_WORDS)

        # ── Backward compat (5) ──────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_version_v185 import (
            is_known_release as ikr,
        )
        self._check("compat_v170",                 lambda: ikr("Small Capital Strategy v1.7.0"))
        self._check("compat_v180",                 lambda: ikr("Paper Simulation & Performance Lab v1.8.0"))
        self._check("compat_v182",                 lambda: ikr("Parameter Optimization & Walk-Forward Validation Lab v1.8.2"))
        self._check("compat_v183",                 lambda: ikr("Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3"))
        self._check("compat_v184",                 lambda: ikr("Position Sizing & Capital Allocation Lab v1.8.4"))

        # ── No forbidden action in allowed output (3) ────────────────────
        self._check("no_buy_in_actions",           lambda: "BUY" not in ALLOWED_OUTPUT_ACTIONS)
        self._check("no_sell_in_actions",          lambda: "SELL" not in ALLOWED_OUTPUT_ACTIONS)
        self._check("portfolio_only_in_actions",   lambda: "PORTFOLIO_ONLY" in ALLOWED_OUTPUT_ACTIONS)

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
            "portfolio_only": True,
            "no_real_orders": True,
        }


def run_release_gate() -> Dict[str, Any]:
    """Run portfolio construction release gate."""
    return PortfolioConstructionRebalancingReleaseGate().run()


if __name__ == "__main__":
    result = run_release_gate()
    status = "PASS" if result["gate_passed"] else "FAIL"
    print(f"Release Gate v1.8.5: {status} {result['passed']}/{result['total']}")
    if not result["gate_passed"]:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
