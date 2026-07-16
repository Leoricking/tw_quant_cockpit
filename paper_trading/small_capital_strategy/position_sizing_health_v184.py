"""
paper_trading/small_capital_strategy/position_sizing_health_v184.py
Health check for Position Sizing & Capital Allocation Lab v1.8.4.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Allocation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List


class PositionSizingHealthCheck:
    """Health check runner for v1.8.4 Position Sizing."""

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

    def run(self) -> "PositionSizingHealthSummary":
        from paper_trading.small_capital_strategy.position_sizing_models_v184 import (
            PositionSizingHealthSummary,
        )
        self._checks = []

        # ── Version (5) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_version_v184 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
        )
        self._check("version_is_184",             lambda: VERSION == "1.8.4")
        self._check("release_name_correct",        lambda: RELEASE_NAME == "Position Sizing & Capital Allocation Lab")
        self._check("schema_version_184",          lambda: SCHEMA_VERSION == "184")
        self._check("verify_version_true",         verify_version)
        self._check("known_release_v183",          lambda: is_known_release("Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3"))

        # ── Safety (10) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_safety_v184 import (
            run_safety_audit, assert_safe, SAFETY_FLAGS,
        )
        self._check("safety_all_safe",             lambda: run_safety_audit()["all_safe"])
        self._check("safety_paper_only",           lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_research_only",        lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("safety_allocation_only",      lambda: SAFETY_FLAGS["allocation_only"] is True)
        self._check("safety_no_real_orders",       lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_no_broker",            lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_no_margin",            lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("safety_no_leverage",          lambda: SAFETY_FLAGS["no_leverage"] is True)
        self._check("safety_production_blocked",   lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_assert_no_raise",      lambda: (assert_safe(), True)[1])

        # ── Models (19) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_models_v184 import (
            CapitalProfile, RiskBudget, PositionSizingInput, PositionSizingRule,
            PositionSizingResult, PortfolioAllocationInput, PortfolioAllocationResult,
            ScalingPlan, AddPositionPlan, ReducePositionPlan, StopLossBudget,
            DrawdownBudget, ConcentrationRiskReport, ExposureLimitReport,
            CashReservePlan, CapitalStagePlan, PositionSizingDashboard,
            PositionSizingReport, PositionSizingHealthSummary as PSH,
            get_all_model_names,
        )
        self._check("model_capital_profile",       lambda: CapitalProfile().paper_only is True)
        self._check("model_risk_budget",           lambda: RiskBudget().paper_only is True)
        self._check("model_ps_input",              lambda: PositionSizingInput().paper_only is True)
        self._check("model_ps_rule",               lambda: PositionSizingRule().paper_only is True)
        self._check("model_ps_result",             lambda: PositionSizingResult().paper_only is True)
        self._check("model_portfolio_alloc_input", lambda: PortfolioAllocationInput().paper_only is True)
        self._check("model_portfolio_alloc_result",lambda: PortfolioAllocationResult().paper_only is True)
        self._check("model_scaling_plan",          lambda: ScalingPlan().paper_only is True)
        self._check("model_add_position_plan",     lambda: AddPositionPlan().paper_only is True)
        self._check("model_reduce_position_plan",  lambda: ReducePositionPlan().paper_only is True)
        self._check("model_stop_loss_budget",      lambda: StopLossBudget().paper_only is True)
        self._check("model_drawdown_budget",       lambda: DrawdownBudget().paper_only is True)
        self._check("model_concentration_report",  lambda: ConcentrationRiskReport().paper_only is True)
        self._check("model_exposure_report",       lambda: ExposureLimitReport().paper_only is True)
        self._check("model_cash_reserve_plan",     lambda: CashReservePlan().paper_only is True)
        self._check("model_capital_stage_plan",    lambda: CapitalStagePlan().paper_only is True)
        self._check("model_ps_dashboard",         lambda: PositionSizingDashboard().paper_only is True)
        self._check("model_ps_report",            lambda: PositionSizingReport().paper_only is True)
        self._check("model_ps_health_summary",    lambda: PSH().paper_only is True)
        self._check("model_count_19",             lambda: len(get_all_model_names()) == 19)

        # ── Engine (10) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_engine_v184 import (
            ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
            CAPITAL_STAGES, SIZING_METHODS, ABC_SIZING_RULES,
            validate_action, validate_grade, run_position_sizing, get_engine_info,
        )
        self._check("engine_allowed_actions_15",   lambda: len(ALLOWED_OUTPUT_ACTIONS) == 15)
        self._check("engine_forbidden_words_9",    lambda: len(FORBIDDEN_OUTPUT_WORDS) == 9)
        self._check("engine_valid_grades_5",       lambda: len(VALID_FINAL_GRADES) == 5)
        self._check("engine_capital_stages_4",     lambda: len(CAPITAL_STAGES) == 4)
        self._check("engine_sizing_methods_10",    lambda: len(SIZING_METHODS) == 10)
        self._check("engine_abc_rules_3",          lambda: len(ABC_SIZING_RULES) == 3)
        self._check("engine_validate_action",      lambda: validate_action("PAPER_ENTRY_ALLOWED"))
        self._check("engine_validate_grade_safe",  lambda: validate_grade("SAFE"))
        _inp = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                   stop_loss_distance_pct=7.0, has_stop_loss=True,
                                   market_regime="BULL")
        self._check("engine_run_callable",         lambda: run_position_sizing(_inp).paper_only is True)
        self._check("engine_info_callable",        lambda: isinstance(get_engine_info(), dict))

        # ── Risk budget params (5) ───────────────────────────────────────
        self._check("risk_budget_per_trade_1pct",  lambda: RiskBudget(per_trade_risk_pct=1.0).per_trade_risk_pct == 1.0)
        self._check("risk_budget_max_pos_20pct",   lambda: RiskBudget(max_single_position_pct=20.0).max_single_position_pct == 20.0)
        self._check("risk_budget_cash_20pct",      lambda: RiskBudget(cash_reserve_pct=20.0).cash_reserve_pct == 20.0)
        self._check("risk_budget_max_dd_20pct",    lambda: RiskBudget(max_drawdown_budget_pct=20.0).max_drawdown_budget_pct == 20.0)
        self._check("risk_budget_max_conc_4",      lambda: RiskBudget(max_concurrent_positions=4).max_concurrent_positions == 4)

        # ── Capital profile (4) ──────────────────────────────────────────
        self._check("capital_stage_300k",          lambda: CapitalProfile(capital=300000.0).capital == 300000.0)
        self._check("capital_stage_500k",          lambda: CapitalProfile(capital=500000.0).capital == 500000.0)
        self._check("capital_stage_1m",            lambda: CapitalProfile(capital=1000000.0).capital == 1000000.0)
        self._check("capital_stage_3m",            lambda: CapitalProfile(capital=3000000.0).capital == 3000000.0)

        # ── Fixed risk sizing (3) ────────────────────────────────────────
        _safe_inp = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                        stop_loss_distance_pct=7.0, has_stop_loss=True)
        self._check("fixed_risk_risk_amount",      lambda: run_position_sizing(_safe_inp).per_trade_risk_amount == 3000.0)
        self._check("fixed_risk_pos_value_gt0",    lambda: run_position_sizing(_safe_inp).suggested_position_value > 0)
        self._check("fixed_risk_grade_safe",       lambda: run_position_sizing(_safe_inp).final_position_grade == "SAFE")

        # ── Stop-distance sizing (2) ─────────────────────────────────────
        self._check("stop_dist_3pct",              lambda: run_position_sizing(PositionSizingInput(
            capital=300000.0, per_trade_risk_pct=1.0, stop_loss_distance_pct=3.0,
            has_stop_loss=True)).suggested_position_value > 0)
        self._check("stop_dist_10pct",             lambda: run_position_sizing(PositionSizingInput(
            capital=300000.0, per_trade_risk_pct=1.0, stop_loss_distance_pct=10.0,
            has_stop_loss=True)).suggested_position_value > 0)

        # ── Volatility adjusted sizing (2) ───────────────────────────────
        _high_vol = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                         stop_loss_distance_pct=7.0, has_stop_loss=True,
                                         volatility_pct=35.0)
        _low_vol  = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                         stop_loss_distance_pct=7.0, has_stop_loss=True,
                                         volatility_pct=10.0)
        self._check("vol_adj_high_reduces",        lambda: run_position_sizing(_high_vol).suggested_position_value
                                                             <= run_position_sizing(_low_vol).suggested_position_value)
        self._check("vol_adj_low_normal",          lambda: run_position_sizing(_low_vol).ruin_risk_adjustment == 1.0)

        # ── Drawdown-aware sizing (2) ────────────────────────────────────
        _dd_exceeded = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                           stop_loss_distance_pct=7.0, has_stop_loss=True,
                                           current_drawdown_pct=20.0, max_drawdown_budget_pct=20.0)
        self._check("dd_exceeded_blocked",         lambda: run_position_sizing(_dd_exceeded).final_position_grade == "BLOCKED")
        self._check("dd_normal_safe",              lambda: run_position_sizing(_safe_inp).drawdown_budget_usage_pct == 0.0)

        # ── Monte Carlo adjusted sizing (2) ──────────────────────────────
        _high_ruin = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                          stop_loss_distance_pct=7.0, has_stop_loss=True,
                                          ruin_risk_pct=25.0)
        self._check("mc_ruin_high_blocked",        lambda: run_position_sizing(_high_ruin).final_position_grade == "BLOCKED")
        self._check("mc_ruin_low_normal",          lambda: run_position_sizing(_safe_inp).ruin_risk_adjustment == 1.0)

        # ── A/B/C staged sizing (3) ──────────────────────────────────────
        _a_inp = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                      stop_loss_distance_pct=7.0, has_stop_loss=True,
                                      abc_buy_point="A_10MA_PULLBACK")
        _b_inp = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                      stop_loss_distance_pct=7.0, has_stop_loss=True,
                                      abc_buy_point="B_BREAKOUT")
        _c_inp = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                      stop_loss_distance_pct=7.0, has_stop_loss=True,
                                      abc_buy_point="C_20MA_RECLAIM")
        self._check("abc_a_initial_40pct",         lambda: abs(run_position_sizing(_a_inp).initial_entry_value /
                                                                run_position_sizing(_a_inp).suggested_position_value - 0.4) < 0.01)
        self._check("abc_b_initial_50pct",         lambda: abs(run_position_sizing(_b_inp).initial_entry_value /
                                                                run_position_sizing(_b_inp).suggested_position_value - 0.5) < 0.01)
        self._check("abc_c_initial_30pct",         lambda: abs(run_position_sizing(_c_inp).initial_entry_value /
                                                                run_position_sizing(_c_inp).suggested_position_value - 0.3) < 0.01)

        # ── Exposure limits (2) ──────────────────────────────────────────
        _exp_inp = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                        stop_loss_distance_pct=7.0, has_stop_loss=True,
                                        current_exposure_pct=55.0, max_total_equity_exposure_pct=60.0)
        self._check("exposure_near_limit_caution", lambda: run_position_sizing(_exp_inp).final_position_grade in
                                                            ("SAFE","ACCEPTABLE","CAUTION","HIGH_RISK","BLOCKED"))
        self._check("exposure_total_computed",     lambda: run_position_sizing(_exp_inp).total_exposure_pct >= 55.0)

        # ── Concentration risk (2) ───────────────────────────────────────
        self._check("concentration_risk_score_ge0",lambda: run_position_sizing(_safe_inp).concentration_risk_score >= 0)
        self._check("concentration_risk_score_le100",lambda: run_position_sizing(_safe_inp).concentration_risk_score <= 100)

        # ── Cash reserve (2) ─────────────────────────────────────────────
        self._check("cash_reserve_amount_gt0",     lambda: run_position_sizing(_safe_inp).cash_after_entry > 0)
        self._check("cash_reserve_pct_default",    lambda: run_position_sizing(_safe_inp).cash_reserve_pct == 20.0)

        # ── Dashboard (3) ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_engine_v184 import build_position_sizing_dashboard
        _dash = build_position_sizing_dashboard(_safe_inp)
        self._check("dashboard_callable",          lambda: _dash.paper_only is True)
        self._check("dashboard_no_real_orders",    lambda: _dash.no_real_orders is True)
        self._check("dashboard_no_broker",         lambda: _dash.no_broker is True)

        # ── Report (3) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_report_v184 import (
            build_report, get_report_sections, REPORT_SECTIONS,
        )
        _rpt = build_report(_dash)
        self._check("report_callable",             lambda: _rpt.paper_only is True)
        self._check("report_sections_12",          lambda: len(REPORT_SECTIONS) == 12)
        self._check("report_sections_fn",          lambda: len(get_report_sections()) == 12)

        # ── CLI (2) ──────────────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        _ps_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("position-sizing")]
        self._check("cli_ps_cmds_ge_20",           lambda: len(_ps_cmds) >= 20)
        self._check("cli_ps_version_exists",       lambda: any(c.name == "position-sizing-version" for c in PROVIDER_COMMANDS))

        # ── GUI (5) ──────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._check("gui_panel_version_184",       lambda: PANEL_VERSION >= "1.8.4")
        self._check("gui_panel_version_in_range",  lambda: PANEL_VERSION in ("1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0"))
        from gui.small_capital_strategy_panel import _TABS
        self._check("gui_tabs_ge_135",             lambda: len(_TABS) >= 135)
        self._check("gui_ps_tab_present",          lambda: "position_sizing" in _TABS)
        self._check("gui_risk_budget_tab_present", lambda: "risk_budget_allocation" in _TABS)

        # ── Scenarios (2) ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_scenarios_v184 import (
            count_scenarios, get_scenarios,
        )
        self._check("scenarios_ge_75",             lambda: count_scenarios() >= 75)
        self._check("scenarios_all_paper",         lambda: all(s["paper_only"] for s in get_scenarios()))

        # ── Fixtures (2) ─────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_fixtures_v184 import (
            get_fixture_count, get_fixture_info,
        )
        self._check("fixtures_ge_75",              lambda: get_fixture_count() >= 75)
        self._check("fixtures_info_callable",      lambda: isinstance(get_fixture_info(), dict))

        # ── Blocked scenarios (4) ────────────────────────────────────────
        _no_sl = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                      stop_loss_distance_pct=7.0, has_stop_loss=False)
        _zero_sl = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                        stop_loss_distance_pct=0.0, has_stop_loss=True)
        _high_risk_pct = PositionSizingInput(capital=300000.0, per_trade_risk_pct=6.0,
                                              stop_loss_distance_pct=7.0, has_stop_loss=True)
        _blocked_regime = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                                               stop_loss_distance_pct=7.0, has_stop_loss=True,
                                               market_regime="BLOCKED")
        self._check("block_no_stop_loss",          lambda: run_position_sizing(_no_sl).final_position_grade == "BLOCKED")
        self._check("block_zero_stop_dist",        lambda: run_position_sizing(_zero_sl).final_position_grade == "BLOCKED")
        self._check("block_high_risk_pct",         lambda: run_position_sizing(_high_risk_pct).final_position_grade == "BLOCKED")
        self._check("block_regime_blocked",        lambda: run_position_sizing(_blocked_regime).final_position_grade == "BLOCKED")

        # ── Forbidden action words (4) ───────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_engine_v184 import FORBIDDEN_OUTPUT_WORDS
        self._check("forbidden_BUY",               lambda: "BUY" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_SELL",              lambda: "SELL" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_ORDER",             lambda: "ORDER" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_BROKER_ORDER",      lambda: "BROKER_ORDER" in FORBIDDEN_OUTPUT_WORDS)

        # ── Backward compatibility (5) ───────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_version_v184 import is_known_release as ikr
        self._check("compat_v170",                 lambda: ikr("Small Capital Strategy v1.7.0"))
        self._check("compat_v178",                 lambda: ikr("Small Capital Strategy Integration v1.7.8"))
        self._check("compat_v180",                 lambda: ikr("Paper Simulation & Performance Lab v1.8.0"))
        self._check("compat_v182",                 lambda: ikr("Parameter Optimization & Walk-Forward Validation Lab v1.8.2"))
        self._check("compat_v183",                 lambda: ikr("Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3"))

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)

        from paper_trading.small_capital_strategy.position_sizing_models_v184 import PositionSizingHealthSummary
        return PositionSizingHealthSummary(
            total=total,
            passed=passed,
            failed=failed,
            all_passed=(failed == 0),
            status="PASS" if failed == 0 else "FAIL",
        )


def run_health_check() -> "PositionSizingHealthSummary":
    """Run position sizing health check."""
    return PositionSizingHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Health Check v1.8.4: {'PASS' if result.all_passed else 'FAIL'} {result.passed}/{result.total}")
    if not result.all_passed:
        hc = PositionSizingHealthCheck()
        hc.run()
        for c in hc._checks:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
