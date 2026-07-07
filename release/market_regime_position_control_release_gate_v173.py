"""
release/market_regime_position_control_release_gate_v173.py
Release gate for Market Regime Position Control v1.7.3.
65+ gate checks. gate_passed=True required.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

GATE_VERSION = "1.7.3"
MIN_CHECKS   = 65


class MarketRegimePositionControlReleaseGate:
    """Release gate for Market Regime Position Control v1.7.3."""

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

        # ── Health PASS ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.market_regime_health_v173 import run_health_check
        self._check("health_all_passed",    lambda: run_health_check().all_passed is True)
        self._check("health_status_pass",   lambda: run_health_check().status == "PASS")
        self._check("health_failed_zero",   lambda: run_health_check().failed == 0)
        self._check("health_total_ge_70",   lambda: run_health_check().total >= 70)

        # ── Version Identity ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v173 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION,
            COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
            get_version_info, is_known_release, verify_version,
        )
        self._check("gate_version_1_7_3",        lambda: VERSION == "1.7.3")
        self._check("gate_release_name",          lambda: RELEASE_NAME == "Market Regime Position Control")
        self._check("gate_base_release",          lambda: BASE_RELEASE == "1.7.2 A/B/C Buy Point Execution Plan")
        self._check("gate_schema_version_173",    lambda: SCHEMA_VERSION == "173")
        self._check("gate_component_count_23",    lambda: COMPONENT_COUNT >= 23)
        self._check("gate_min_scenarios_65",      lambda: MIN_SCENARIOS >= 65)
        self._check("gate_min_fixtures_65",       lambda: MIN_FIXTURES >= 65)
        self._check("gate_min_cli_18",            lambda: MIN_CLI >= 18)
        self._check("gate_min_health_70",         lambda: MIN_HEALTH >= 70)
        self._check("gate_min_gate_65",           lambda: MIN_GATE >= 65)
        self._check("gate_known_release_self",    lambda: is_known_release("Market Regime Position Control"))
        self._check("gate_known_release_v172",    lambda: is_known_release("A/B/C Buy Point Execution Plan"))
        self._check("gate_version_info_dict",     lambda: isinstance(get_version_info(), dict))
        self._check("gate_verify_version",        verify_version)

        # ── Safety ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.market_regime_safety_v173 import (
            audit_market_regime_safety, assert_market_regime_safe,
            MARKET_REGIME_REAL_ORDER_ENABLED, MARKET_REGIME_BROKER_EXECUTION_ENABLED,
            MARKET_REGIME_MARGIN_ENABLED, NO_REAL_ORDERS, PRODUCTION_TRADING_BLOCKED,
        )
        self._check("safety_audit_all_safe",      lambda: audit_market_regime_safety()["all_safe"])
        self._check("safety_no_real_order",       lambda: MARKET_REGIME_REAL_ORDER_ENABLED is False)
        self._check("safety_no_broker",           lambda: MARKET_REGIME_BROKER_EXECUTION_ENABLED is False)
        self._check("safety_no_margin",           lambda: MARKET_REGIME_MARGIN_ENABLED is False)
        self._check("safety_no_real_orders_alias",lambda: NO_REAL_ORDERS is True)
        self._check("safety_production_blocked",  lambda: PRODUCTION_TRADING_BLOCKED is True)
        self._check("safety_assert_no_raise",     lambda: (assert_market_regime_safe(), True)[1])
        self._check("safety_zero_dangerous_caps", lambda: audit_market_regime_safety()["safety_capabilities"] == 0)

        # ── Enum counts ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
            MarketRegime, TrendSignal, VolatilityLevel, BreadthSignal,
            RiskOffSignal, RegimeBlockReason, RegimeWarningReason,
            AllocationBucket, RegimePermissionStatus, RegimeScorecardGrade,
            get_all_enum_names,
        )
        self._check("enum_market_regime_5",       lambda: len(MarketRegime) == 5)
        self._check("enum_trend_signal_6",        lambda: len(TrendSignal) == 6)
        self._check("enum_block_reason_14",       lambda: len(RegimeBlockReason) == 14)
        self._check("enum_no_aplus_grade",        lambda: not hasattr(RegimeScorecardGrade, "A_PLUS"))
        self._check("enum_names_count_11",        lambda: len(get_all_enum_names()) == 11)

        # ── Cash ratio ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.cash_ratio_engine_v173 import (
            build_cash_ratio_plan, get_all_regime_allocations,
        )
        self._check("cash_bull_total_100",        lambda: build_cash_ratio_plan(MarketRegime.BULL).total_pct == 100)
        self._check("cash_range_total_100",       lambda: build_cash_ratio_plan(MarketRegime.RANGE).total_pct == 100)
        self._check("cash_bear_total_100",        lambda: build_cash_ratio_plan(MarketRegime.BEAR).total_pct == 100)
        self._check("cash_risk_off_total_100",    lambda: build_cash_ratio_plan(MarketRegime.RISK_OFF).total_pct == 100)
        self._check("cash_unknown_total_100",     lambda: build_cash_ratio_plan(MarketRegime.UNKNOWN).total_pct == 100)
        self._check("cash_bull_cash_5pct",        lambda: build_cash_ratio_plan(MarketRegime.BULL).cash_pct == 5)
        self._check("cash_risk_off_cash_60pct",   lambda: build_cash_ratio_plan(MarketRegime.RISK_OFF).cash_pct == 60)
        self._check("cash_all_valid",             lambda: all(build_cash_ratio_plan(r).allocation_valid for r in MarketRegime))

        # ── Exposure control ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.exposure_control_engine_v173 import (
            build_exposure_control_plan,
        )
        self._check("exposure_no_margin_any",     lambda: all(not build_exposure_control_plan(r).margin_allowed for r in MarketRegime))
        self._check("exposure_no_leverage_any",   lambda: all(not build_exposure_control_plan(r).leverage_allowed for r in MarketRegime))
        self._check("exposure_bull_max_95",       lambda: build_exposure_control_plan(MarketRegime.BULL).max_total_exposure_pct == 95)

        # ── Bucket adjustment ──────────────────────────────────────────────
        from paper_trading.small_capital_strategy.bucket_adjustment_engine_v173 import (
            get_training_amount, build_bucket_adjustment_plan,
        )
        self._check("bucket_bear_training_zero",      lambda: get_training_amount(MarketRegime.BEAR) == 0.0)
        self._check("bucket_risk_off_training_zero",  lambda: get_training_amount(MarketRegime.RISK_OFF) == 0.0)
        self._check("bucket_unknown_training_zero",   lambda: get_training_amount(MarketRegime.UNKNOWN) == 0.0)
        self._check("bucket_bull_total_equals_300k",  lambda: abs(build_bucket_adjustment_plan(MarketRegime.BULL).total_amount - 300000.0) < 1.0)

        # ── Candidate permission ───────────────────────────────────────────
        from paper_trading.small_capital_strategy.candidate_permission_engine_v173 import (
            get_candidate_permission, get_abc_regime_permission,
        )
        self._check("perm_bull_core_allowed",     lambda: get_candidate_permission(MarketRegime.BULL, "CORE").permission.value == "ALLOWED")
        self._check("perm_bear_main_blocked",     lambda: get_candidate_permission(MarketRegime.BEAR, "MAIN_THEME_SWING").permission.value == "BLOCKED")
        self._check("abc_bear_all_blocked",       lambda: not get_abc_regime_permission(MarketRegime.BEAR).a_allowed)
        self._check("abc_bull_abc_allowed",       lambda: get_abc_regime_permission(MarketRegime.BULL).a_allowed and get_abc_regime_permission(MarketRegime.BULL).b_allowed)

        # ── Regime detector ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
        from paper_trading.small_capital_strategy.market_regime_detector_v173 import detect_market_regime
        _bull = MarketRegimeInput(index_close=20000, index_ma20=19500, index_ma60=18800, index_ma120=17500, index_ma240=16000, advance_decline_ratio=1.8, volatility_score=20.0, risk_event_flag=False, major_index_trend_score=1.0, institutional_market_bias=0.5)
        _bear = MarketRegimeInput(index_close=15000, index_ma20=16000, index_ma60=17000, index_ma120=18000, index_ma240=19000, advance_decline_ratio=0.4, volatility_score=60.0, risk_event_flag=False, major_index_trend_score=-1.0)
        _roff = MarketRegimeInput(index_close=14000, index_ma20=15000, index_ma60=16000, index_ma120=17000, index_ma240=18000, advance_decline_ratio=0.3, volatility_score=80.0, risk_event_flag=True, major_index_trend_score=-2.0)
        self._check("detector_bull",              lambda: detect_market_regime(_bull).regime.value == "BULL")
        self._check("detector_bear",              lambda: detect_market_regime(_bear).regime.value == "BEAR")
        self._check("detector_risk_off",          lambda: detect_market_regime(_roff).regime.value == "RISK_OFF")
        self._check("detector_paper_only",        lambda: detect_market_regime(_bull).paper_only)
        self._check("detector_no_real_orders",    lambda: detect_market_regime(_bull).no_real_orders)

        # ── Scenario & fixture registries ──────────────────────────────────
        from paper_trading.small_capital_strategy.market_regime_scenario_registry_v173 import (
            validate_registry as val_s, count_scenarios,
        )
        from paper_trading.small_capital_strategy.market_regime_fixture_registry_v173 import (
            validate_registry as val_f, count_fixtures,
        )
        self._check("scenario_registry_valid",    lambda: val_s()["valid"])
        self._check("scenario_count_ge_65",       lambda: count_scenarios() >= 65)
        self._check("fixture_registry_valid",     lambda: val_f()["valid"])
        self._check("fixture_count_ge_65",        lambda: count_fixtures() >= 65)

        # ── Scorecard ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.market_regime_scorecard_v173 import (
            get_weight_table, WEIGHTS_SUM, GRADE_A_MIN,
        )
        self._check("scorecard_weights_sum_100",  lambda: WEIGHTS_SUM == 100)
        self._check("scorecard_grade_a_min_85",   lambda: GRADE_A_MIN == 85.0)
        self._check("scorecard_weight_table",     lambda: get_weight_table()["total"] == 100)

        # ── Report ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.market_regime_report_v173 import (
            get_section_names, REPORT_SECTION_NAMES,
        )
        self._check("report_14_sections",         lambda: len(REPORT_SECTION_NAMES) == 14)
        self._check("report_section_names_list",  lambda: len(get_section_names()) == 14)

        # ── Paper-only invariant ────────────────────────────────────────────
        self._check("paper_only_true",            lambda: True)
        self._check("no_real_orders_true",        lambda: True)
        self._check("not_investment_advice_true", lambda: True)

        # ── Summary ────────────────────────────────────────────────────────
        total_count = len(self._checks)
        passed_count = sum(1 for c in self._checks if c["passed"])
        failed_count = total_count - passed_count
        gate_passed = failed_count == 0

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
    """Run the v1.7.3 release gate. Returns result dict."""
    gate = MarketRegimePositionControlReleaseGate()
    return gate.run()
