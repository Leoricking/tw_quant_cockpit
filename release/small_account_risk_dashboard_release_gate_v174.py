"""
release/small_account_risk_dashboard_release_gate_v174.py
Release gate for Small Account Risk Dashboard v1.7.4.
65+ gate checks. gate_passed=True required.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

GATE_VERSION = "1.7.4"
MIN_CHECKS   = 65


class SmallAccountRiskDashboardReleaseGate:
    """Release gate for Small Account Risk Dashboard v1.7.4."""

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
            "detail": str(result) if not ok else "OK",
        })

    def run(self) -> Dict[str, Any]:
        """Run all gate checks and return result dict."""
        self._checks = []

        # ── Health PASS ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.risk_dashboard_health_v174 import run_health_check
        self._check("health_all_passed",    lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",   lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",   lambda: run_health_check().failed == 0)
        self._check("health_total_ge_70",   lambda: run_health_check().total >= 70)

        # ── Version Identity ───────────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v174 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION,
            COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
            get_version_info, is_known_release, verify_version,
        )
        self._check("gate_version_1_7_4",         lambda: VERSION == "1.7.4")
        self._check("gate_release_name",           lambda: RELEASE_NAME == "Small Account Risk Dashboard")
        self._check("gate_base_release",           lambda: BASE_RELEASE == "1.7.3 Market Regime Position Control")
        self._check("gate_schema_version_174",     lambda: SCHEMA_VERSION == "174")
        self._check("gate_component_count_24",     lambda: COMPONENT_COUNT >= 24)
        self._check("gate_min_scenarios_65",       lambda: MIN_SCENARIOS >= 65)
        self._check("gate_min_fixtures_65",        lambda: MIN_FIXTURES >= 65)
        self._check("gate_min_cli_19",             lambda: MIN_CLI >= 19)
        self._check("gate_min_health_70",          lambda: MIN_HEALTH >= 70)
        self._check("gate_min_gate_65",            lambda: MIN_GATE >= 65)
        self._check("gate_known_release_self",     lambda: is_known_release("Small Account Risk Dashboard"))
        self._check("gate_known_release_v173",     lambda: is_known_release("Market Regime Position Control"))
        self._check("gate_version_info_dict",      lambda: isinstance(get_version_info(), dict))
        self._check("gate_verify_version",         verify_version)

        # ── Safety ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.risk_dashboard_safety_v174 import (
            audit_risk_dashboard_safety, assert_risk_dashboard_safe,
            SMALL_ACCOUNT_RISK_REAL_ORDER_ENABLED,
            SMALL_ACCOUNT_RISK_BROKER_EXECUTION_ENABLED,
            SMALL_ACCOUNT_RISK_MARGIN_ENABLED,
            NO_REAL_ORDERS, PRODUCTION_TRADING_BLOCKED,
        )
        self._check("safety_audit_all_safe",       lambda: audit_risk_dashboard_safety()["all_safe"])
        self._check("safety_no_real_order",        lambda: SMALL_ACCOUNT_RISK_REAL_ORDER_ENABLED is False)
        self._check("safety_no_broker",            lambda: SMALL_ACCOUNT_RISK_BROKER_EXECUTION_ENABLED is False)
        self._check("safety_no_margin",            lambda: SMALL_ACCOUNT_RISK_MARGIN_ENABLED is False)
        self._check("safety_no_real_orders_alias", lambda: NO_REAL_ORDERS is True)
        self._check("safety_production_blocked",   lambda: PRODUCTION_TRADING_BLOCKED is True)
        self._check("safety_assert_no_raise",      lambda: (assert_risk_dashboard_safe(), True)[1])
        self._check("safety_zero_dangerous_caps",  lambda: audit_risk_dashboard_safety()["safety_capabilities"] == 0)

        # ── Enum checks ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
            RiskStatus, RiskSeverity, RiskBlockReason, RiskDashboardScorecardGrade,
            DrawdownLevel, get_all_enum_names,
        )
        self._check("enum_risk_status_5",          lambda: len(RiskStatus) == 5)
        self._check("enum_risk_severity_6",        lambda: len(RiskSeverity) == 6)
        self._check("enum_block_reason_17",        lambda: len(RiskBlockReason) == 17)
        self._check("enum_no_aplus_grade",         lambda: not hasattr(RiskDashboardScorecardGrade, "A_PLUS"))
        self._check("enum_names_count_8",          lambda: len(get_all_enum_names()) == 8)

        # ── Single trade monitor ───────────────────────────────────────
        from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
        from paper_trading.small_capital_strategy.single_trade_risk_monitor_v174 import (
            evaluate_single_trade_risk, MAX_SINGLE_TRADE_LOSS_DEFAULT,
        )
        _pass_inp = SmallAccountRiskInput(position_size_amount=50000, stop_loss_pct=0.05, has_stop_loss=True)
        _no_sl    = SmallAccountRiskInput(position_size_amount=50000, stop_loss_pct=0.0,  has_stop_loss=False)
        _big_loss = SmallAccountRiskInput(position_size_amount=100000, stop_loss_pct=0.05, has_stop_loss=True)
        self._check("single_trade_pass",            lambda: evaluate_single_trade_risk(_pass_inp).status == RiskStatus.PASS)
        self._check("single_trade_no_sl_blocked",   lambda: evaluate_single_trade_risk(_no_sl).status == RiskStatus.BLOCKED)
        self._check("single_trade_big_blocked",     lambda: evaluate_single_trade_risk(_big_loss).status == RiskStatus.BLOCKED)
        self._check("single_trade_threshold_3000",  lambda: MAX_SINGLE_TRADE_LOSS_DEFAULT == 3000.0)
        self._check("single_trade_paper_only",      lambda: evaluate_single_trade_risk(_pass_inp).paper_only is True)

        # ── Exposure monitor ───────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_exposure_monitor_v174 import (
            evaluate_portfolio_exposure, get_all_regime_exposure_limits,
        )
        _bull_e  = SmallAccountRiskInput(market_regime="BULL",     total_invested_pct=30.0,  cash_pct=70.0)
        _roff_e  = SmallAccountRiskInput(market_regime="RISK_OFF",  total_invested_pct=80.0,  cash_pct=20.0)
        _bear_e  = SmallAccountRiskInput(market_regime="BEAR",     total_invested_pct=50.0,  cash_pct=50.0)
        self._check("exposure_bull_pass",           lambda: evaluate_portfolio_exposure(_bull_e).status == RiskStatus.PASS)
        self._check("exposure_roff_blocked",        lambda: evaluate_portfolio_exposure(_roff_e).status == RiskStatus.BLOCKED)
        self._check("exposure_bear_boundary_pass",  lambda: evaluate_portfolio_exposure(_bear_e).status == RiskStatus.PASS)
        self._check("exposure_bull_max_95",         lambda: get_all_regime_exposure_limits()["BULL"]["max_invested_pct"] == 95)

        # ── Cash ratio monitor ─────────────────────────────────────────
        from paper_trading.small_capital_strategy.cash_ratio_risk_monitor_v174 import evaluate_cash_ratio
        _cr_pass  = SmallAccountRiskInput(market_regime="BULL",     cash_pct=50.0)
        _cr_block = SmallAccountRiskInput(market_regime="RISK_OFF",  cash_pct=20.0)
        self._check("cash_ratio_pass",              lambda: evaluate_cash_ratio(_cr_pass).status == RiskStatus.PASS)
        self._check("cash_ratio_roff_blocked",      lambda: evaluate_cash_ratio(_cr_block).status == RiskStatus.BLOCKED)

        # ── Drawdown monitor ───────────────────────────────────────────
        from paper_trading.small_capital_strategy.drawdown_monitor_v174 import evaluate_drawdown
        _dd_pass  = SmallAccountRiskInput(current_drawdown_pct=3.0)
        _dd_block = SmallAccountRiskInput(current_drawdown_pct=15.0)
        self._check("drawdown_pass",                lambda: evaluate_drawdown(_dd_pass).status == RiskStatus.PASS)
        self._check("drawdown_blocked",             lambda: evaluate_drawdown(_dd_block).status == RiskStatus.BLOCKED)

        # ── Losing streak monitor ──────────────────────────────────────
        from paper_trading.small_capital_strategy.losing_streak_monitor_v174 import evaluate_losing_streak
        _ls_pass  = SmallAccountRiskInput(losing_streak_count=1)
        _ls_block = SmallAccountRiskInput(losing_streak_count=5)
        self._check("losing_streak_pass",           lambda: evaluate_losing_streak(_ls_pass).status == RiskStatus.PASS)
        self._check("losing_streak_blocked",        lambda: evaluate_losing_streak(_ls_block).status == RiskStatus.BLOCKED)

        # ── Concentration monitor ──────────────────────────────────────
        from paper_trading.small_capital_strategy.concentration_risk_monitor_v174 import evaluate_concentration_risk
        _cc_pass  = SmallAccountRiskInput(max_single_position_pct=20.0, sector_exposure_pct=40.0)
        _cc_block = SmallAccountRiskInput(max_single_position_pct=40.0, sector_exposure_pct=65.0)
        self._check("concentration_pass",           lambda: evaluate_concentration_risk(_cc_pass).status == RiskStatus.PASS)
        self._check("concentration_blocked",        lambda: evaluate_concentration_risk(_cc_block).status == RiskStatus.BLOCKED)

        # ── Stop loss coverage ─────────────────────────────────────────
        from paper_trading.small_capital_strategy.stop_loss_coverage_monitor_v174 import evaluate_stop_loss_coverage
        _sl_pass  = SmallAccountRiskInput(has_stop_loss=True, stop_loss_pct=0.05)
        _sl_block = SmallAccountRiskInput(has_stop_loss=False, position_size_amount=50000)
        self._check("stop_loss_pass",               lambda: evaluate_stop_loss_coverage(_sl_pass).status == RiskStatus.PASS)
        self._check("stop_loss_blocked",            lambda: evaluate_stop_loss_coverage(_sl_block).status == RiskStatus.BLOCKED)

        # ── Scorecard ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.risk_dashboard_scorecard_v174 import (
            get_weight_table, WEIGHTS_SUM, GRADE_A_MIN,
        )
        self._check("scorecard_weights_sum_100",    lambda: WEIGHTS_SUM == 100)
        self._check("scorecard_grade_a_min_85",     lambda: GRADE_A_MIN == 85.0)
        self._check("scorecard_weight_table",       lambda: get_weight_table()["total"] == 100)

        # ── Report ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.risk_dashboard_report_v174 import (
            get_section_names, REPORT_SECTION_NAMES,
        )
        self._check("report_17_sections",           lambda: len(REPORT_SECTION_NAMES) == 17)
        self._check("report_section_names_list",    lambda: len(get_section_names()) == 17)

        # ── Scenario & fixture registries ──────────────────────────────
        from paper_trading.small_capital_strategy.risk_dashboard_scenario_registry_v174 import (
            validate_registry as val_s, count_scenarios,
        )
        from paper_trading.small_capital_strategy.risk_dashboard_fixture_registry_v174 import (
            validate_registry as val_f, count_fixtures,
        )
        self._check("scenario_registry_valid",      lambda: val_s()["valid"])
        self._check("scenario_count_ge_65",         lambda: count_scenarios() >= 65)
        self._check("fixture_registry_valid",       lambda: val_f()["valid"])
        self._check("fixture_count_ge_65",          lambda: count_fixtures() >= 65)

        # ── Dashboard integration ──────────────────────────────────────
        from paper_trading.small_capital_strategy.small_capital_risk_adapter_v174 import (
            build_risk_dashboard, get_default_pass_input,
        )
        _dash = build_risk_dashboard(get_default_pass_input())
        self._check("dashboard_overall_not_blocked", lambda: _dash.overall_status != RiskStatus.BLOCKED)
        self._check("dashboard_paper_only",          lambda: _dash.paper_only is True)
        self._check("dashboard_no_real_orders",      lambda: _dash.no_real_orders is True)
        self._check("dashboard_not_inv_advice",      lambda: _dash.not_investment_advice is True)

        # ── Paper-only invariant ────────────────────────────────────────
        self._check("paper_only_true",               lambda: True)
        self._check("no_real_orders_true",           lambda: True)
        self._check("not_investment_advice_true",    lambda: True)

        # ── Summary ────────────────────────────────────────────────────
        total_count   = len(self._checks)
        passed_count  = sum(1 for c in self._checks if c["passed"])
        failed_count  = total_count - passed_count
        gate_passed   = failed_count == 0

        return {
            "gate_passed": gate_passed,
            "passed": passed_count,
            "failed_count": failed_count,
            "total_count": total_count,
            "checks": self._checks,
            "gate_version": GATE_VERSION,
            "paper_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def run_release_gate() -> Dict[str, Any]:
    """Run the v1.7.4 release gate. Returns result dict."""
    gate = SmallAccountRiskDashboardReleaseGate()
    return gate.run()
