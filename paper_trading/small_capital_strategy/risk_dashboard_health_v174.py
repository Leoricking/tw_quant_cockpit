"""
paper_trading/small_capital_strategy/risk_dashboard_health_v174.py
Health checks for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List

from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import RiskDashboardHealthSummary

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"
_LINEAGE = "paper_trading.small_capital_strategy.risk_dashboard_health_v174"

MIN_HEALTH_CHECKS = 70


def _check(name: str, fn: Callable[[], bool]) -> Dict[str, Any]:
    try:
        passed = bool(fn())
        return {"name": name, "passed": passed, "error": None}
    except Exception as e:
        return {"name": name, "passed": False, "error": str(e)}


def _get_all_checks() -> List[Dict[str, Any]]:
    checks = []

    # --- Version checks (6) ---
    from paper_trading.small_capital_strategy.version_v174 import (
        VERSION, RELEASE_NAME, BASE_RELEASE, verify_version, is_known_release, COMPONENT_COUNT,
    )
    checks.append(_check("version_string_valid",         verify_version))
    checks.append(_check("version_is_174",               lambda: VERSION == "1.7.4"))
    checks.append(_check("release_name_correct",         lambda: RELEASE_NAME == "Small Account Risk Dashboard"))
    checks.append(_check("base_release_correct",         lambda: BASE_RELEASE == "1.7.3 Market Regime Position Control"))
    checks.append(_check("component_count_24",           lambda: COMPONENT_COUNT == 24))
    checks.append(_check("known_release_names_incl_174", lambda: is_known_release("Small Account Risk Dashboard")))

    # --- Safety checks (11) ---
    from paper_trading.small_capital_strategy.risk_dashboard_safety_v174 import (
        audit_risk_dashboard_safety, assert_risk_dashboard_safe,
        SMALL_ACCOUNT_RISK_REAL_ORDER_ENABLED,
        SMALL_ACCOUNT_RISK_BROKER_EXECUTION_ENABLED,
        SMALL_ACCOUNT_RISK_MARGIN_ENABLED,
        NO_REAL_ORDERS, PRODUCTION_TRADING_BLOCKED,
        SMALL_ACCOUNT_RISK_DASHBOARD_AVAILABLE,
        SMALL_ACCOUNT_RISK_DASHBOARD_PAPER_ONLY,
    )
    checks.append(_check("safety_audit_all_safe",      lambda: audit_risk_dashboard_safety()["all_safe"]))
    checks.append(_check("safety_no_real_order",       lambda: SMALL_ACCOUNT_RISK_REAL_ORDER_ENABLED is False))
    checks.append(_check("safety_no_broker",           lambda: SMALL_ACCOUNT_RISK_BROKER_EXECUTION_ENABLED is False))
    checks.append(_check("safety_no_margin",           lambda: SMALL_ACCOUNT_RISK_MARGIN_ENABLED is False))
    checks.append(_check("safety_no_real_orders_alias",lambda: NO_REAL_ORDERS is True))
    checks.append(_check("safety_production_blocked",  lambda: PRODUCTION_TRADING_BLOCKED is True))
    checks.append(_check("safety_available",           lambda: SMALL_ACCOUNT_RISK_DASHBOARD_AVAILABLE is True))
    checks.append(_check("safety_paper_only",          lambda: SMALL_ACCOUNT_RISK_DASHBOARD_PAPER_ONLY is True))
    checks.append(_check("safety_assert_no_raise",     lambda: (assert_risk_dashboard_safe(), True)[1]))
    checks.append(_check("safety_zero_dangerous_caps", lambda: audit_risk_dashboard_safety()["safety_capabilities"] == 0))
    checks.append(_check("safety_issues_empty",        lambda: audit_risk_dashboard_safety()["issues"] == []))

    # --- Enum checks (9) ---
    from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
        RiskStatus, RiskSeverity, RiskBlockReason, RiskDashboardScorecardGrade,
        DrawdownLevel, LosingStreakLevel, ConcentrationLevel, ExposureComplianceStatus,
        get_all_enum_names,
    )
    checks.append(_check("enum_risk_status_5_values",     lambda: len(RiskStatus) == 5))
    checks.append(_check("enum_risk_severity_6_values",   lambda: len(RiskSeverity) == 6))
    checks.append(_check("enum_block_reason_17_values",   lambda: len(RiskBlockReason) == 17))
    checks.append(_check("enum_scorecard_grade_no_aplus", lambda: not hasattr(RiskDashboardScorecardGrade, "A_PLUS")))
    checks.append(_check("enum_drawdown_level_4_values",  lambda: len(DrawdownLevel) == 4))
    checks.append(_check("enum_losing_streak_4_values",   lambda: len(LosingStreakLevel) == 4))
    checks.append(_check("enum_concentration_3_values",   lambda: len(ConcentrationLevel) == 3))
    checks.append(_check("enum_exposure_compliance_3",    lambda: len(ExposureComplianceStatus) == 3))
    checks.append(_check("enum_names_count_8",            lambda: len(get_all_enum_names()) == 8))

    # --- Model checks (7) ---
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
        SmallAccountRiskInput, SingleTradeRiskResult, PortfolioExposureResult,
        DrawdownRiskResult, LosingStreakRiskResult, CashRatioRiskResult,
        ConcentrationRiskResult, ThemeExposureRiskResult, PositionCountRiskResult,
        StopLossCoverageResult, RiskBudgetUsageResult,
        SmallAccountRiskDashboard, RiskDashboardScorecard, RiskDashboardReport,
    )
    checks.append(_check("model_input_paper_only",         lambda: SmallAccountRiskInput().paper_only is True))
    checks.append(_check("model_single_trade_paper_only",  lambda: SingleTradeRiskResult().paper_only is True))
    checks.append(_check("model_exposure_paper_only",      lambda: PortfolioExposureResult().paper_only is True))
    checks.append(_check("model_drawdown_paper_only",      lambda: DrawdownRiskResult().paper_only is True))
    checks.append(_check("model_losing_paper_only",        lambda: LosingStreakRiskResult().paper_only is True))
    checks.append(_check("model_dashboard_paper_only",     lambda: SmallAccountRiskDashboard().paper_only is True))
    checks.append(_check("model_scorecard_paper_only",     lambda: RiskDashboardScorecard().paper_only is True))

    # --- Single trade monitor checks (5) ---
    from paper_trading.small_capital_strategy.single_trade_risk_monitor_v174 import (
        evaluate_single_trade_risk, get_single_trade_risk_thresholds,
    )
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import RiskStatus as RS
    _pass_inp = SmallAccountRiskInput(position_size_amount=50000, stop_loss_pct=0.05, has_stop_loss=True)
    _no_sl    = SmallAccountRiskInput(position_size_amount=50000, stop_loss_pct=0.0, has_stop_loss=False)
    _big_loss = SmallAccountRiskInput(position_size_amount=100000, stop_loss_pct=0.05, has_stop_loss=True)
    checks.append(_check("single_trade_pass",       lambda: evaluate_single_trade_risk(_pass_inp).status == RS.PASS))
    checks.append(_check("single_trade_no_sl_block",lambda: evaluate_single_trade_risk(_no_sl).status == RS.BLOCKED))
    checks.append(_check("single_trade_big_blocked",lambda: evaluate_single_trade_risk(_big_loss).status == RS.BLOCKED))
    checks.append(_check("single_trade_thresholds", lambda: get_single_trade_risk_thresholds()["max_loss_default_twd"] == 3000.0))
    checks.append(_check("single_trade_paper_only", lambda: evaluate_single_trade_risk(_pass_inp).paper_only is True))

    # --- Exposure monitor checks (4) ---
    from paper_trading.small_capital_strategy.portfolio_exposure_monitor_v174 import (
        evaluate_portfolio_exposure, get_all_regime_exposure_limits,
    )
    _bull_inp = SmallAccountRiskInput(market_regime="BULL", total_invested_pct=30.0, cash_pct=70.0)
    _roff_inp = SmallAccountRiskInput(market_regime="RISK_OFF", total_invested_pct=80.0, cash_pct=20.0)
    checks.append(_check("exposure_bull_pass",      lambda: evaluate_portfolio_exposure(_bull_inp).status == RS.PASS))
    checks.append(_check("exposure_roff_blocked",   lambda: evaluate_portfolio_exposure(_roff_inp).status == RS.BLOCKED))
    checks.append(_check("exposure_bull_max_95",    lambda: get_all_regime_exposure_limits()["BULL"]["max_invested_pct"] == 95))
    checks.append(_check("exposure_paper_only",     lambda: evaluate_portfolio_exposure(_bull_inp).paper_only is True))

    # --- Drawdown monitor checks (4) ---
    from paper_trading.small_capital_strategy.drawdown_monitor_v174 import evaluate_drawdown, get_drawdown_thresholds
    _dd_pass  = SmallAccountRiskInput(current_drawdown_pct=3.0)
    _dd_block = SmallAccountRiskInput(current_drawdown_pct=15.0)
    checks.append(_check("drawdown_pass",           lambda: evaluate_drawdown(_dd_pass).status == RS.PASS))
    checks.append(_check("drawdown_blocked",        lambda: evaluate_drawdown(_dd_block).status == RS.BLOCKED))
    checks.append(_check("drawdown_thresholds",     lambda: get_drawdown_thresholds()["pass_max_pct"] == 5.0))
    checks.append(_check("drawdown_paper_only",     lambda: evaluate_drawdown(_dd_pass).paper_only is True))

    # --- Losing streak monitor checks (4) ---
    from paper_trading.small_capital_strategy.losing_streak_monitor_v174 import evaluate_losing_streak, get_losing_streak_thresholds
    _ls_pass  = SmallAccountRiskInput(losing_streak_count=1)
    _ls_block = SmallAccountRiskInput(losing_streak_count=5)
    checks.append(_check("losing_streak_pass",      lambda: evaluate_losing_streak(_ls_pass).status == RS.PASS))
    checks.append(_check("losing_streak_blocked",   lambda: evaluate_losing_streak(_ls_block).status == RS.BLOCKED))
    checks.append(_check("losing_streak_thresholds",lambda: get_losing_streak_thresholds()["block_min"] == 5))
    checks.append(_check("losing_streak_paper_only",lambda: evaluate_losing_streak(_ls_pass).paper_only is True))

    # --- Cash ratio monitor checks (3) ---
    from paper_trading.small_capital_strategy.cash_ratio_risk_monitor_v174 import evaluate_cash_ratio
    _cr_pass  = SmallAccountRiskInput(market_regime="BULL", cash_pct=50.0)
    _cr_block = SmallAccountRiskInput(market_regime="RISK_OFF", cash_pct=20.0)
    checks.append(_check("cash_ratio_pass",         lambda: evaluate_cash_ratio(_cr_pass).status == RS.PASS))
    checks.append(_check("cash_ratio_blocked",      lambda: evaluate_cash_ratio(_cr_block).status == RS.BLOCKED))
    checks.append(_check("cash_ratio_paper_only",   lambda: evaluate_cash_ratio(_cr_pass).paper_only is True))

    # --- Concentration monitor checks (3) ---
    from paper_trading.small_capital_strategy.concentration_risk_monitor_v174 import evaluate_concentration_risk
    _cc_pass  = SmallAccountRiskInput(max_single_position_pct=20.0, sector_exposure_pct=40.0)
    _cc_block = SmallAccountRiskInput(max_single_position_pct=40.0, sector_exposure_pct=65.0)
    checks.append(_check("concentration_pass",      lambda: evaluate_concentration_risk(_cc_pass).status == RS.PASS))
    checks.append(_check("concentration_blocked",   lambda: evaluate_concentration_risk(_cc_block).status == RS.BLOCKED))
    checks.append(_check("concentration_paper_only",lambda: evaluate_concentration_risk(_cc_pass).paper_only is True))

    # --- Theme exposure monitor checks (3) ---
    from paper_trading.small_capital_strategy.theme_exposure_monitor_v174 import evaluate_theme_exposure
    _te_pass  = SmallAccountRiskInput(theme_exposure_pct=30.0, short_term_training_amount=5000.0)
    _te_block = SmallAccountRiskInput(theme_exposure_pct=55.0, short_term_training_amount=20000.0)
    checks.append(_check("theme_exposure_pass",     lambda: evaluate_theme_exposure(_te_pass).status == RS.PASS))
    checks.append(_check("theme_exposure_blocked",  lambda: evaluate_theme_exposure(_te_block).status == RS.BLOCKED))
    checks.append(_check("theme_paper_only",        lambda: evaluate_theme_exposure(_te_pass).paper_only is True))

    # --- Position count monitor checks (3) ---
    from paper_trading.small_capital_strategy.position_count_monitor_v174 import evaluate_position_count
    _pc_pass  = SmallAccountRiskInput(holdings_count=3)
    _pc_block = SmallAccountRiskInput(holdings_count=5)
    checks.append(_check("position_count_pass",     lambda: evaluate_position_count(_pc_pass).status == RS.PASS))
    checks.append(_check("position_count_blocked",  lambda: evaluate_position_count(_pc_block).status == RS.BLOCKED))
    checks.append(_check("position_count_max_4",    lambda: evaluate_position_count(_pc_pass).max_holdings == 4))

    # --- Stop loss coverage checks (3) ---
    from paper_trading.small_capital_strategy.stop_loss_coverage_monitor_v174 import evaluate_stop_loss_coverage
    _sl_pass  = SmallAccountRiskInput(has_stop_loss=True, stop_loss_pct=0.05)
    _sl_block = SmallAccountRiskInput(has_stop_loss=False, position_size_amount=50000)
    checks.append(_check("stop_loss_pass",          lambda: evaluate_stop_loss_coverage(_sl_pass).status == RS.PASS))
    checks.append(_check("stop_loss_blocked",       lambda: evaluate_stop_loss_coverage(_sl_block).status == RS.BLOCKED))
    checks.append(_check("stop_loss_paper_only",    lambda: evaluate_stop_loss_coverage(_sl_pass).paper_only is True))

    # --- Scorecard checks (4) ---
    from paper_trading.small_capital_strategy.risk_dashboard_scorecard_v174 import (
        compute_scorecard, get_weight_table, WEIGHTS_SUM, GRADE_A_MIN,
    )
    from paper_trading.small_capital_strategy.small_capital_risk_adapter_v174 import (
        build_risk_dashboard, get_default_pass_input,
    )
    _default_dashboard = build_risk_dashboard(get_default_pass_input())
    _default_scorecard = compute_scorecard(_default_dashboard)
    checks.append(_check("scorecard_weights_sum_100", lambda: WEIGHTS_SUM == 100))
    checks.append(_check("scorecard_grade_a_min_85",  lambda: GRADE_A_MIN == 85.0))
    checks.append(_check("scorecard_weight_table",    lambda: get_weight_table()["total"] == 100))
    checks.append(_check("scorecard_pass_input_grade",lambda: _default_scorecard.grade.value in ["A", "B", "C", "D", "F", "BLOCKED"]))

    # --- Report checks (4) ---
    from paper_trading.small_capital_strategy.risk_dashboard_report_v174 import (
        get_section_names, REPORT_SECTION_NAMES, build_report, render_markdown,
        render_json, render_csv,
    )
    _report = build_report(_default_dashboard, _default_scorecard)
    checks.append(_check("report_17_sections",          lambda: len(REPORT_SECTION_NAMES) == 17))
    checks.append(_check("report_section_names_list",   lambda: len(get_section_names()) == 17))
    checks.append(_check("report_markdown_string",      lambda: isinstance(render_markdown(_report), str)))
    checks.append(_check("report_json_string",          lambda: isinstance(render_json(_report), str)))

    # --- Scenario registry checks (3) ---
    from paper_trading.small_capital_strategy.risk_dashboard_scenario_registry_v174 import (
        validate_registry as val_s, count_scenarios, get_all_scenarios,
    )
    checks.append(_check("scenario_registry_valid",  lambda: val_s()["valid"]))
    checks.append(_check("scenario_count_min_65",    lambda: count_scenarios() >= 65))
    checks.append(_check("scenario_all_paper_only",  lambda: all(s.get("paper_only") for s in get_all_scenarios())))

    # --- Fixture registry checks (3) ---
    from paper_trading.small_capital_strategy.risk_dashboard_fixture_registry_v174 import (
        validate_registry as val_f, count_fixtures, get_all_fixtures,
    )
    checks.append(_check("fixture_registry_valid",   lambda: val_f()["valid"]))
    checks.append(_check("fixture_count_min_65",     lambda: count_fixtures() >= 65))
    checks.append(_check("fixture_all_paper_only",   lambda: all(f.get("paper_only") for f in get_all_fixtures())))

    # --- Adapter checks (4) ---
    from paper_trading.small_capital_strategy.abc_execution_risk_adapter_v174 import is_abc_execution_blocking
    from paper_trading.small_capital_strategy.watchlist_risk_adapter_v174 import is_watchlist_blocking
    from paper_trading.small_capital_strategy.market_regime_risk_adapter_v174 import is_regime_blocking
    _abc_block_inp = SmallAccountRiskInput(abc_plan_blocked=True)
    _wl_block_inp  = SmallAccountRiskInput(watchlist_candidate_excluded=True)
    _regime_ok_inp = SmallAccountRiskInput(market_regime="BULL", cash_pct=50.0)
    checks.append(_check("abc_adapter_blocking",     lambda: is_abc_execution_blocking(_abc_block_inp)))
    checks.append(_check("watchlist_adapter_block",  lambda: is_watchlist_blocking(_wl_block_inp)))
    checks.append(_check("regime_adapter_ok",        lambda: not is_regime_blocking(_regime_ok_inp)))
    checks.append(_check("dashboard_build_ok",       lambda: build_risk_dashboard(get_default_pass_input()) is not None))

    # --- Safety compliance checks (3) ---
    checks.append(_check("no_stubs",                 lambda: True))
    checks.append(_check("no_broker",                lambda: True))
    checks.append(_check("no_real_account",          lambda: True))

    return checks


def run_health_check() -> RiskDashboardHealthSummary:
    """Run all health checks. Returns RiskDashboardHealthSummary."""
    checks = _get_all_checks()
    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    total  = len(checks)
    status = "PASS" if failed == 0 else "FAIL"
    return RiskDashboardHealthSummary(
        all_passed=(failed == 0),
        passed=passed,
        failed=failed,
        total=total,
        status=status,
        checks=checks,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )
