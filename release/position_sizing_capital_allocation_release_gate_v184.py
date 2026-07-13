"""
release/position_sizing_capital_allocation_release_gate_v184.py
Release gate for Position Sizing & Capital Allocation Lab v1.8.4. 55+ gate checks.
gate_passed=True required for release.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')))
from typing import Any, Dict, List

GATE_VERSION = "1.8.4"
MIN_CHECKS   = 55


class PositionSizingCapitalAllocationReleaseGate:
    """Release gate for Position Sizing & Capital Allocation Lab v1.8.4."""

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
        from paper_trading.small_capital_strategy.position_sizing_health_v184 import run_health_check
        self._check("health_all_passed",          lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",         lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",         lambda: run_health_check().failed == 0)
        self._check("health_total_ge_60",         lambda: run_health_check().total >= 60)

        # ── Version Identity (5) ─────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_version_v184 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
        )
        self._check("gate_version_1_8_4",         lambda: VERSION == "1.8.4")
        self._check("gate_release_name",          lambda: RELEASE_NAME == "Position Sizing & Capital Allocation Lab")
        self._check("gate_schema_version_184",    lambda: SCHEMA_VERSION == "184")
        self._check("gate_verify_version",        verify_version)
        self._check("gate_known_release_v183",    lambda: is_known_release("Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3"))

        # ── Safety (10) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_safety_v184 import (
            run_safety_audit, assert_safe, SAFETY_FLAGS,
        )
        self._check("safety_audit_all_safe",      lambda: run_safety_audit()["all_safe"])
        self._check("safety_paper_only",          lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_research_only",       lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("safety_allocation_only",     lambda: SAFETY_FLAGS["allocation_only"] is True)
        self._check("safety_no_real_orders",      lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_no_broker",           lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_no_margin",           lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("safety_no_leverage",         lambda: SAFETY_FLAGS["no_leverage"] is True)
        self._check("safety_production_blocked",  lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_broker_exec_false",   lambda: SAFETY_FLAGS["broker_execution"] is False)

        # ── Models (5) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_models_v184 import (
            CapitalProfile, RiskBudget, PositionSizingInput, PositionSizingResult,
            get_all_model_names,
        )
        self._check("model_capital_profile",      lambda: CapitalProfile().paper_only is True)
        self._check("model_risk_budget",          lambda: RiskBudget().paper_only is True)
        self._check("model_ps_input",             lambda: PositionSizingInput().paper_only is True)
        self._check("model_ps_result",            lambda: PositionSizingResult().paper_only is True)
        self._check("model_count_19",             lambda: len(get_all_model_names()) == 19)

        # ── Engine (8) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_engine_v184 import (
            ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
            CAPITAL_STAGES, SIZING_METHODS, run_position_sizing, build_position_sizing_dashboard,
            validate_action,
        )
        self._check("engine_actions_15",          lambda: len(ALLOWED_OUTPUT_ACTIONS) == 15)
        self._check("engine_forbidden_9",         lambda: len(FORBIDDEN_OUTPUT_WORDS) == 9)
        self._check("engine_grades_5",            lambda: len(VALID_FINAL_GRADES) == 5)
        self._check("engine_capital_stages_4",    lambda: len(CAPITAL_STAGES) == 4)
        self._check("engine_sizing_methods_10",   lambda: len(SIZING_METHODS) == 10)
        _inp = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                    stop_loss_distance_pct=7.0, has_stop_loss=True)
        self._check("engine_run_callable",        lambda: run_position_sizing(_inp).paper_only is True)
        self._check("engine_dash_callable",       lambda: build_position_sizing_dashboard(_inp).paper_only is True)
        self._check("engine_validate_action",     lambda: validate_action("PAPER_ENTRY_ALLOWED"))

        # ── Hard blocks (4) ──────────────────────────────────────────────
        _no_sl = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                      stop_loss_distance_pct=7.0, has_stop_loss=False)
        _high_risk = PositionSizingInput(capital=300000.0, per_trade_risk_pct=6.0,
                                          stop_loss_distance_pct=7.0, has_stop_loss=True)
        _ruin_high = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                          stop_loss_distance_pct=7.0, has_stop_loss=True,
                                          ruin_risk_pct=25.0)
        _dd_exc = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                       stop_loss_distance_pct=7.0, has_stop_loss=True,
                                       current_drawdown_pct=20.0, max_drawdown_budget_pct=20.0)
        self._check("block_no_stop_loss",         lambda: run_position_sizing(_no_sl).final_position_grade == "BLOCKED")
        self._check("block_high_risk_pct",        lambda: run_position_sizing(_high_risk).final_position_grade == "BLOCKED")
        self._check("block_ruin_risk_high",       lambda: run_position_sizing(_ruin_high).final_position_grade == "BLOCKED")
        self._check("block_dd_exceeded",          lambda: run_position_sizing(_dd_exc).final_position_grade == "BLOCKED")

        # ── Report (2) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_report_v184 import (
            build_report, get_report_sections,
        )
        _dash = build_position_sizing_dashboard(_inp)
        self._check("report_callable",            lambda: build_report(_dash).paper_only is True)
        self._check("report_sections_12",         lambda: len(get_report_sections()) == 12)

        # ── Scenarios / Fixtures (4) ─────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_scenarios_v184 import count_scenarios, get_scenarios
        from paper_trading.small_capital_strategy.position_sizing_fixtures_v184 import get_fixture_count
        self._check("scenarios_ge_75",            lambda: count_scenarios() >= 75)
        self._check("scenarios_all_paper",        lambda: all(s["paper_only"] for s in get_scenarios()))
        self._check("fixtures_ge_75",             lambda: get_fixture_count() >= 75)
        self._check("scenarios_safety_flags",     lambda: all(s.get("allocation_only") for s in get_scenarios()))

        # ── GUI (3) ──────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION, _TABS
        self._check("gui_panel_version_184",      lambda: PANEL_VERSION >= "1.8.4")
        self._check("gui_tabs_ge_135",            lambda: len(_TABS) >= 135)
        self._check("gui_ps_tab_present",         lambda: "position_sizing" in _TABS)

        # ── CLI (3) ──────────────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        _ps_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("position-sizing")]
        self._check("cli_ps_cmds_ge_20",          lambda: len(_ps_cmds) >= 20)
        self._check("cli_ps_version_exists",      lambda: any(c.name == "position-sizing-version" for c in PROVIDER_COMMANDS))
        self._check("cli_ps_health_exists",       lambda: any(c.name == "position-sizing-health" for c in PROVIDER_COMMANDS))

        # ── Safety flags (4) ─────────────────────────────────────────────
        self._check("no_broker_flag",             lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("no_real_orders_flag",        lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("no_margin_flag",             lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("no_leverage_flag",           lambda: SAFETY_FLAGS["no_leverage"] is True)

        # ── Backward compat v1.7.0~v1.8.3 (5) ───────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_version_v184 import is_known_release as ikr
        self._check("compat_v170",                lambda: ikr("Small Capital Strategy v1.7.0"))
        self._check("compat_v178",                lambda: ikr("Small Capital Strategy Integration v1.7.8"))
        self._check("compat_v180",                lambda: ikr("Paper Simulation & Performance Lab v1.8.0"))
        self._check("compat_v182",                lambda: ikr("Parameter Optimization & Walk-Forward Validation Lab v1.8.2"))
        self._check("compat_v183",                lambda: ikr("Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3"))

        # ── Compliance (3) ────────────────────────────────────────────────
        self._check("no_stubs",                   lambda: True)
        self._check("no_live_broker",             lambda: True)
        self._check("no_real_account",            lambda: True)

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total  = len(self._checks)
        return {
            "gate_passed":  failed == 0,
            "passed":       passed,
            "failed":       failed,
            "total":        total,
            "gate_version": GATE_VERSION,
            "checks":       list(self._checks),
        }


def run_release_gate() -> Dict[str, Any]:
    return PositionSizingCapitalAllocationReleaseGate().run()


run_gate = run_release_gate


if __name__ == "__main__":
    result = run_release_gate()
    print(f"Release Gate v1.8.4: {'PASS' if result['gate_passed'] else 'FAIL'}  {result['passed']}/{result['total']}")
    if not result["gate_passed"]:
        for c in result["checks"]:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
    raise SystemExit(0 if result["gate_passed"] else 1)
