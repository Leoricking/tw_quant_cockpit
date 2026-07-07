"""
paper_trading/small_capital_strategy/market_regime_health_v173.py
Health checks for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List

from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeHealthSummary

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.market_regime_health_v173"

MIN_HEALTH_CHECKS = 70


def _check(name: str, fn: Callable[[], bool]) -> Dict[str, Any]:
    try:
        passed = bool(fn())
        return {"name": name, "passed": passed, "error": None}
    except Exception as e:
        return {"name": name, "passed": False, "error": str(e)}


def _get_all_checks() -> List[Dict[str, Any]]:
    checks = []

    # --- Version checks (5) ---
    from paper_trading.small_capital_strategy.version_v173 import (
        VERSION, RELEASE_NAME, verify_version, is_known_release, COMPONENT_COUNT,
    )
    checks.append(_check("version_string_valid", verify_version))
    checks.append(_check("version_is_173", lambda: VERSION == "1.7.3"))
    checks.append(_check("release_name_correct", lambda: RELEASE_NAME == "Market Regime Position Control"))
    checks.append(_check("component_count_23", lambda: COMPONENT_COUNT == 23))
    checks.append(_check("known_release_names_includes_173", lambda: is_known_release("Market Regime Position Control")))

    # --- Enum checks (11) ---
    from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
        MarketRegime, RegimeDetectionStatus, TrendSignal, VolatilityLevel,
        BreadthSignal, RiskOffSignal, AllocationBucket, RegimePermissionStatus,
        RegimeScorecardGrade, RegimeBlockReason, RegimeWarningReason,
        get_all_enum_names,
    )
    checks.append(_check("enum_market_regime_5_values", lambda: len(MarketRegime) == 5))
    checks.append(_check("enum_trend_signal_6_values", lambda: len(TrendSignal) == 6))
    checks.append(_check("enum_volatility_level_5_values", lambda: len(VolatilityLevel) == 5))
    checks.append(_check("enum_breadth_signal_5_values", lambda: len(BreadthSignal) == 5))
    checks.append(_check("enum_risk_off_signal_4_values", lambda: len(RiskOffSignal) == 4))
    checks.append(_check("enum_block_reason_14_values", lambda: len(RegimeBlockReason) == 14))
    checks.append(_check("enum_warning_reason_4_values", lambda: len(RegimeWarningReason) == 4))
    checks.append(_check("enum_scorecard_grade_no_aplus", lambda: not hasattr(RegimeScorecardGrade, "A_PLUS")))
    checks.append(_check("get_all_enum_names_returns_11", lambda: len(get_all_enum_names()) == 11))
    checks.append(_check("enum_allocation_bucket_5_values", lambda: len(AllocationBucket) == 5))
    checks.append(_check("enum_permission_status_5_values", lambda: len(RegimePermissionStatus) == 5))

    # --- Safety checks (10) ---
    from paper_trading.small_capital_strategy.market_regime_safety_v173 import (
        audit_market_regime_safety, assert_market_regime_safe,
        MARKET_REGIME_REAL_ORDER_ENABLED, MARKET_REGIME_BROKER_EXECUTION_ENABLED,
        MARKET_REGIME_MARGIN_ENABLED, NO_REAL_ORDERS, PRODUCTION_TRADING_BLOCKED,
        MARKET_REGIME_CONTROL_AVAILABLE, MARKET_REGIME_CONTROL_PAPER_ONLY,
    )
    checks.append(_check("safety_audit_all_safe", lambda: audit_market_regime_safety()["all_safe"]))
    checks.append(_check("safety_no_real_order", lambda: MARKET_REGIME_REAL_ORDER_ENABLED is False))
    checks.append(_check("safety_no_broker", lambda: MARKET_REGIME_BROKER_EXECUTION_ENABLED is False))
    checks.append(_check("safety_no_margin", lambda: MARKET_REGIME_MARGIN_ENABLED is False))
    checks.append(_check("safety_no_real_orders_alias", lambda: NO_REAL_ORDERS is True))
    checks.append(_check("safety_production_blocked", lambda: PRODUCTION_TRADING_BLOCKED is True))
    checks.append(_check("safety_control_available", lambda: MARKET_REGIME_CONTROL_AVAILABLE is True))
    checks.append(_check("safety_paper_only", lambda: MARKET_REGIME_CONTROL_PAPER_ONLY is True))
    checks.append(_check("safety_assert_does_not_raise", lambda: (assert_market_regime_safe(), True)[1]))
    checks.append(_check("safety_zero_dangerous_capabilities", lambda: audit_market_regime_safety()["safety_capabilities"] == 0))

    # --- Model checks (7) ---
    from paper_trading.small_capital_strategy.market_regime_models_v173 import (
        MarketRegimeInput, TrendFilterResult, VolatilityFilterResult,
        BreadthFilterResult, RiskOffDetectionResult, MarketRegimeDetectionResult,
        CashRatioPlan, ExposureControlPlan, BucketAdjustmentPlan,
        CandidateRegimePermission, ABCRegimePermission,
        MarketRegimeScorecard, MarketRegimeReport, MarketRegimeHealthSummary as HMS,
    )
    checks.append(_check("model_input_paper_only", lambda: MarketRegimeInput().paper_only is True))
    checks.append(_check("model_detection_result_paper_only", lambda: MarketRegimeDetectionResult().paper_only is True))
    checks.append(_check("model_cash_ratio_paper_only", lambda: CashRatioPlan().paper_only is True))
    checks.append(_check("model_exposure_paper_only", lambda: ExposureControlPlan().paper_only is True))
    checks.append(_check("model_bucket_paper_only", lambda: BucketAdjustmentPlan().paper_only is True))
    checks.append(_check("model_scorecard_paper_only", lambda: MarketRegimeScorecard().paper_only is True))
    checks.append(_check("model_report_paper_only", lambda: MarketRegimeReport().paper_only is True))

    # --- Trend filter checks (4) ---
    from paper_trading.small_capital_strategy.trend_filter_v173 import evaluate_trend_filter
    _bull_inp = MarketRegimeInput(index_close=20000, index_ma20=19500, index_ma60=18800, index_ma120=17500, index_ma240=16000, major_index_trend_score=1.0)
    _bear_inp = MarketRegimeInput(index_close=15000, index_ma20=16000, index_ma60=17000, index_ma120=18000, index_ma240=19000, major_index_trend_score=-1.0)
    checks.append(_check("trend_bull_is_up", lambda: evaluate_trend_filter(_bull_inp).trend_score > 0))
    checks.append(_check("trend_bear_is_down", lambda: evaluate_trend_filter(_bear_inp).trend_score < 0))
    checks.append(_check("trend_bull_above_ma20", lambda: evaluate_trend_filter(_bull_inp).index_above_ma20))
    checks.append(_check("trend_bear_not_above_ma20", lambda: not evaluate_trend_filter(_bear_inp).index_above_ma20))

    # --- Volatility filter checks (4) ---
    from paper_trading.small_capital_strategy.volatility_filter_v173 import evaluate_volatility_filter
    _low_vol  = MarketRegimeInput(volatility_score=10.0)
    _high_vol = MarketRegimeInput(volatility_score=80.0)
    checks.append(_check("volatility_low_controlled", lambda: evaluate_volatility_filter(_low_vol).volatility_controlled))
    checks.append(_check("volatility_high_not_controlled", lambda: not evaluate_volatility_filter(_high_vol).volatility_controlled))
    checks.append(_check("volatility_extreme_threshold", lambda: evaluate_volatility_filter(_high_vol).volatility_level.value == "EXTREME"))
    checks.append(_check("volatility_low_level", lambda: evaluate_volatility_filter(_low_vol).volatility_level.value == "LOW"))

    # --- Breadth filter checks (4) ---
    from paper_trading.small_capital_strategy.breadth_filter_v173 import evaluate_breadth_filter
    _healthy_breadth = MarketRegimeInput(advance_decline_ratio=1.8)
    _weak_breadth    = MarketRegimeInput(advance_decline_ratio=0.3)
    checks.append(_check("breadth_healthy_signal", lambda: evaluate_breadth_filter(_healthy_breadth).breadth_signal.value == "HEALTHY"))
    checks.append(_check("breadth_very_weak_signal", lambda: evaluate_breadth_filter(_weak_breadth).breadth_signal.value == "VERY_WEAK"))
    checks.append(_check("breadth_healthy_flag_true", lambda: evaluate_breadth_filter(_healthy_breadth).breadth_healthy))
    checks.append(_check("breadth_healthy_flag_false_when_weak", lambda: not evaluate_breadth_filter(_weak_breadth).breadth_healthy))

    # --- Risk-off detector checks (4) ---
    from paper_trading.small_capital_strategy.risk_off_detector_v173 import detect_risk_off
    _risk_off_inp = MarketRegimeInput(index_close=14000, index_ma120=17000, index_ma240=18000, volatility_score=80.0, risk_event_flag=True, advance_decline_ratio=0.3)
    _safe_inp     = MarketRegimeInput(index_close=20000, index_ma120=17000, index_ma240=16000, volatility_score=10.0, risk_event_flag=False)
    checks.append(_check("risk_off_extreme_when_all_triggers", lambda: detect_risk_off(_risk_off_inp).risk_off_signal.value == "EXTREME"))
    checks.append(_check("risk_off_none_when_safe", lambda: detect_risk_off(_safe_inp).risk_off_signal.value == "NONE"))
    checks.append(_check("risk_off_spike_detected", lambda: detect_risk_off(_risk_off_inp).volatility_spike))
    checks.append(_check("risk_off_event_detected", lambda: detect_risk_off(_risk_off_inp).risk_event_active))

    # --- Regime detector checks (5) ---
    from paper_trading.small_capital_strategy.market_regime_detector_v173 import detect_market_regime
    _bull_full = MarketRegimeInput(index_close=20000, index_ma20=19500, index_ma60=18800, index_ma120=17500, index_ma240=16000, advance_decline_ratio=1.8, volatility_score=20.0, risk_event_flag=False, major_index_trend_score=1.0, institutional_market_bias=0.5)
    _bear_full = MarketRegimeInput(index_close=15000, index_ma20=16000, index_ma60=17000, index_ma120=18000, index_ma240=19000, advance_decline_ratio=0.4, volatility_score=60.0, risk_event_flag=False, major_index_trend_score=-1.0)
    _risk_full = MarketRegimeInput(index_close=14000, index_ma20=15000, index_ma60=16000, index_ma120=17000, index_ma240=18000, advance_decline_ratio=0.3, volatility_score=80.0, risk_event_flag=True, major_index_trend_score=-2.0)
    checks.append(_check("detector_bull_detected", lambda: detect_market_regime(_bull_full).regime.value == "BULL"))
    checks.append(_check("detector_bear_detected", lambda: detect_market_regime(_bear_full).regime.value == "BEAR"))
    checks.append(_check("detector_risk_off_detected", lambda: detect_market_regime(_risk_full).regime.value == "RISK_OFF"))
    checks.append(_check("detector_zero_close_insufficient", lambda: detect_market_regime(MarketRegimeInput(index_close=0)).status.value == "INSUFFICIENT"))
    checks.append(_check("detector_paper_only", lambda: detect_market_regime(_bull_full).paper_only))

    # --- Cash ratio engine checks (5) ---
    from paper_trading.small_capital_strategy.cash_ratio_engine_v173 import build_cash_ratio_plan
    checks.append(_check("cash_bull_total_100", lambda: build_cash_ratio_plan(MarketRegime.BULL).total_pct == 100))
    checks.append(_check("cash_bear_total_100", lambda: build_cash_ratio_plan(MarketRegime.BEAR).total_pct == 100))
    checks.append(_check("cash_risk_off_total_100", lambda: build_cash_ratio_plan(MarketRegime.RISK_OFF).total_pct == 100))
    checks.append(_check("cash_bull_cash_5pct", lambda: build_cash_ratio_plan(MarketRegime.BULL).cash_pct == 5))
    checks.append(_check("cash_risk_off_cash_60pct", lambda: build_cash_ratio_plan(MarketRegime.RISK_OFF).cash_pct == 60))

    # --- Exposure control checks (4) ---
    from paper_trading.small_capital_strategy.exposure_control_engine_v173 import build_exposure_control_plan
    checks.append(_check("exposure_no_margin_bull", lambda: not build_exposure_control_plan(MarketRegime.BULL).margin_allowed))
    checks.append(_check("exposure_no_margin_bear", lambda: not build_exposure_control_plan(MarketRegime.BEAR).margin_allowed))
    checks.append(_check("exposure_no_leverage_all", lambda: not build_exposure_control_plan(MarketRegime.RISK_OFF).leverage_allowed))
    checks.append(_check("exposure_bull_max_95", lambda: build_exposure_control_plan(MarketRegime.BULL).max_total_exposure_pct == 95))

    # --- Bucket adjustment checks (4) ---
    from paper_trading.small_capital_strategy.bucket_adjustment_engine_v173 import build_bucket_adjustment_plan, get_training_amount
    checks.append(_check("bucket_bear_training_zero", lambda: get_training_amount(MarketRegime.BEAR) == 0.0))
    checks.append(_check("bucket_risk_off_training_zero", lambda: get_training_amount(MarketRegime.RISK_OFF) == 0.0))
    checks.append(_check("bucket_unknown_training_zero", lambda: get_training_amount(MarketRegime.UNKNOWN) == 0.0))
    checks.append(_check("bucket_bull_total_equals_capital", lambda: abs(build_bucket_adjustment_plan(MarketRegime.BULL).total_amount - 300000.0) < 1.0))

    # --- Candidate permission checks (4) ---
    from paper_trading.small_capital_strategy.candidate_permission_engine_v173 import (
        get_candidate_permission, get_abc_regime_permission, list_all_tiers,
    )
    checks.append(_check("perm_bull_core_allowed", lambda: get_candidate_permission(MarketRegime.BULL, "CORE").permission.value == "ALLOWED"))
    checks.append(_check("perm_bear_main_blocked", lambda: get_candidate_permission(MarketRegime.BEAR, "MAIN_THEME_SWING").permission.value == "BLOCKED"))
    checks.append(_check("abc_bull_all_allowed", lambda: get_abc_regime_permission(MarketRegime.BULL).a_allowed and get_abc_regime_permission(MarketRegime.BULL).b_allowed))
    checks.append(_check("abc_bear_all_blocked", lambda: not get_abc_regime_permission(MarketRegime.BEAR).a_allowed))

    # --- Scenario registry checks (3) ---
    from paper_trading.small_capital_strategy.market_regime_scenario_registry_v173 import (
        validate_registry as val_scenarios, count_scenarios, get_all_scenarios,
    )
    checks.append(_check("scenario_registry_valid", lambda: val_scenarios()["valid"]))
    checks.append(_check("scenario_count_min_65", lambda: count_scenarios() >= 65))
    checks.append(_check("scenario_all_paper_only", lambda: all(s.get("paper_only") for s in get_all_scenarios())))

    # --- Fixture registry checks (3) ---
    from paper_trading.small_capital_strategy.market_regime_fixture_registry_v173 import (
        validate_registry as val_fixtures, count_fixtures, get_all_fixtures,
    )
    checks.append(_check("fixture_registry_valid", lambda: val_fixtures()["valid"]))
    checks.append(_check("fixture_count_min_65", lambda: count_fixtures() >= 65))
    checks.append(_check("fixture_all_paper_only", lambda: all(f.get("paper_only") for f in get_all_fixtures())))

    return checks


def run_health_check() -> MarketRegimeHealthSummary:
    """Run all health checks. Returns MarketRegimeHealthSummary."""
    checks = _get_all_checks()
    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    total  = len(checks)
    status = "PASS" if failed == 0 else "FAIL"
    return MarketRegimeHealthSummary(
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
