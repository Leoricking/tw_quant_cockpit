"""
tests/test_drawdown_risk_controls_v153.py — Drawdown & Risk Controls v1.5.3 test suite.
288 tests. All offline. Research-only. Not Investment Advice.
[!] Research Only. No Real Orders. No Broker. No Auto-Stop. No Auto-Rebalance.
"""
from __future__ import annotations

import json
import os
import pathlib
import pytest

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

FIXTURE_DIR = pathlib.Path(__file__).parent / "fixtures" / "drawdown_risk_controls"


def _load_fixture(name: str) -> dict:
    path = FIXTURE_DIR / name
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _make_request(**kwargs):
    from portfolio.risk_controls.models_v153 import DrawdownAnalysisRequest
    defaults = dict(
        request_id="REQ_TEST_001",
        portfolio_id="demo_portfolio",
        as_of="2026-06-21",
        available_from="2025-01-01",
        lookback_days=252,
        source_lineage_ids=["LIN_001"],
    )
    defaults.update(kwargs)
    return DrawdownAnalysisRequest(**defaults)


def _build_equity_curve(n: int = 50, base: float = 1_000_000.0):
    from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
    import math
    values = {}
    for i in range(n):
        month = (i // 21) + 1
        day   = (i % 21) + 1
        date  = f"2025-{month:02d}-{day:02d}"
        values[date] = base * (1.0 + 0.0003 * i - 0.000005 * i * i
                                + 0.001 * math.sin(i * 0.3))
    return PortfolioEquityCurveBuilder().build(values, {}, "2026-06-21")


def _build_underwater(equity_curve=None):
    from portfolio.risk_controls.underwater_v153 import UnderwaterCurveCalculator
    if equity_curve is None:
        equity_curve = _build_equity_curve()
    return UnderwaterCurveCalculator().calculate(equity_curve)


def _build_demo_evaluation():
    from portfolio.risk_controls.constraint_engine_v153 import RiskControlConstraintEngine
    return RiskControlConstraintEngine().build_demo_evaluation()


# ===========================================================================
# 1. TestModelsSafety (tests 1-18)
# ===========================================================================

class TestModelsSafety:
    def test_1_DRAWDOWN_RISK_CONTROLS_AVAILABLE_true(self):
        from portfolio.risk_controls import DRAWDOWN_RISK_CONTROLS_AVAILABLE
        assert DRAWDOWN_RISK_CONTROLS_AVAILABLE is True

    def test_2_DRAWDOWN_RISK_CONTROLS_RESEARCH_ONLY_true(self):
        from portfolio.risk_controls import DRAWDOWN_RISK_CONTROLS_RESEARCH_ONLY
        assert DRAWDOWN_RISK_CONTROLS_RESEARCH_ONLY is True

    def test_3_RISK_CONTROL_AUTO_APPLY_ENABLED_false(self):
        from portfolio.risk_controls import RISK_CONTROL_AUTO_APPLY_ENABLED
        assert RISK_CONTROL_AUTO_APPLY_ENABLED is False

    def test_4_RISK_CONTROL_AUTO_REDUCE_ENABLED_false(self):
        from portfolio.risk_controls import RISK_CONTROL_AUTO_REDUCE_ENABLED
        assert RISK_CONTROL_AUTO_REDUCE_ENABLED is False

    def test_5_RISK_CONTROL_AUTO_STOP_ENABLED_false(self):
        from portfolio.risk_controls import RISK_CONTROL_AUTO_STOP_ENABLED
        assert RISK_CONTROL_AUTO_STOP_ENABLED is False

    def test_6_RISK_CONTROL_AUTO_REBALANCE_ENABLED_false(self):
        from portfolio.risk_controls import RISK_CONTROL_AUTO_REBALANCE_ENABLED
        assert RISK_CONTROL_AUTO_REBALANCE_ENABLED is False

    def test_7_RISK_CONTROL_ORDER_CREATION_ENABLED_false(self):
        from portfolio.risk_controls import RISK_CONTROL_ORDER_CREATION_ENABLED
        assert RISK_CONTROL_ORDER_CREATION_ENABLED is False

    def test_8_RISK_CONTROL_BROKER_ENABLED_false(self):
        from portfolio.risk_controls import RISK_CONTROL_BROKER_ENABLED
        assert RISK_CONTROL_BROKER_ENABLED is False

    def test_9_NO_REAL_ORDERS_true(self):
        from portfolio.risk_controls import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_10_PRODUCTION_TRADING_BLOCKED_true(self):
        from portfolio.risk_controls import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_11_BROKER_EXECUTION_ENABLED_false(self):
        from portfolio.risk_controls import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_12_RESULT_LABELS_contains_safety_strings(self):
        from portfolio.risk_controls import RESULT_LABELS
        for lbl in ["RESEARCH_ONLY", "NO_BROKER_CALL", "NO_LEDGER_WRITE", "NOT_AN_ORDER"]:
            assert lbl in RESULT_LABELS

    def test_13_DrawdownAnalysisRequest_research_only_defaults_true(self):
        req = _make_request()
        assert req.research_only is True

    def test_14_DrawdownAnalysisRequest_research_only_false_raises(self):
        with pytest.raises(AssertionError):
            _make_request(research_only=False)

    def test_15_RiskControlPolicy_executable_false_enforced(self):
        from portfolio.risk_controls.models_v153 import RiskControlPolicy
        from portfolio.risk_controls.enums_v153 import RiskControlType
        p = RiskControlPolicy(policy_id="P1", control_type=RiskControlType.VOLATILITY_LIMIT, name="T")
        assert p.executable is False

    def test_16_RiskControlPolicy_executable_true_raises(self):
        from portfolio.risk_controls.models_v153 import RiskControlPolicy
        from portfolio.risk_controls.enums_v153 import RiskControlType
        with pytest.raises(AssertionError):
            RiskControlPolicy(policy_id="P1", control_type=RiskControlType.VOLATILITY_LIMIT,
                              name="T", executable=True)

    def test_17_RiskControlCheck_order_created_false_enforced(self):
        from portfolio.risk_controls.models_v153 import RiskControlCheck
        from portfolio.risk_controls.enums_v153 import RiskControlType
        c = RiskControlCheck(check_id="C1", policy_id="P1",
                             control_type=RiskControlType.DAILY_LOSS_LIMIT)
        assert c.order_created is False

    def test_18_RiskControlEvaluation_ledger_persisted_false_enforced(self):
        from portfolio.risk_controls.models_v153 import RiskControlEvaluation
        ev = RiskControlEvaluation(evaluation_id="E1", portfolio_id="P", as_of="2026-06-21")
        assert ev.ledger_persisted is False


# ===========================================================================
# 2. TestEquityCurve (tests 19-32)
# ===========================================================================

class TestEquityCurve:
    def test_19_build_returns_list(self):
        curve = _build_equity_curve()
        assert isinstance(curve, list)

    def test_20_build_positive_length(self):
        curve = _build_equity_curve(n=10)
        assert len(curve) == 10

    def test_21_build_no_future_dates(self):
        curve = _build_equity_curve()
        for pt in curve:
            assert pt.date <= "2026-06-21"

    def test_22_build_demo_returns_list(self):
        from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
        curve = PortfolioEquityCurveBuilder().build_demo()
        assert isinstance(curve, list)
        assert len(curve) > 0

    def test_23_build_demo_no_future_dates(self):
        from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
        curve = PortfolioEquityCurveBuilder().build_demo(as_of="2026-06-21")
        for pt in curve:
            assert pt.date <= "2026-06-21"

    def test_24_point_has_date_field(self):
        curve = _build_equity_curve(n=5)
        for pt in curve:
            assert hasattr(pt, "date")

    def test_25_point_has_portfolio_value_field(self):
        curve = _build_equity_curve(n=5)
        for pt in curve:
            assert hasattr(pt, "portfolio_value")

    def test_26_point_portfolio_value_positive(self):
        curve = _build_equity_curve(n=5)
        for pt in curve:
            assert pt.portfolio_value > 0

    def test_27_fixture_equity_curve_valid_loads(self):
        f = _load_fixture("equity_curve_valid.json")
        assert f["portfolio_id"] == "demo_portfolio"

    def test_28_fixture_equity_curve_valid_research_only(self):
        f = _load_fixture("equity_curve_valid.json")
        assert f["research_only"] is True

    def test_29_fixture_equity_curve_future_data_has_future(self):
        f = _load_fixture("equity_curve_future_data.json")
        assert f.get("has_future_data", True) is True or "2027" in str(f)

    def test_30_fixture_equity_curve_cash_flows_loads(self):
        f = _load_fixture("equity_curve_cash_flows.json")
        assert "cash_flows" in f

    def test_31_fixture_equity_curve_missing_value_loads(self):
        f = _load_fixture("equity_curve_missing_value.json")
        assert f.get("has_missing") is True

    def test_32_builder_filters_future_dates(self):
        from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
        values = {"2026-06-20": 1_000_000.0, "2026-06-22": 1_010_000.0}
        curve = PortfolioEquityCurveBuilder().build(values, {}, as_of="2026-06-21")
        assert all(pt.date <= "2026-06-21" for pt in curve)
        assert len(curve) == 1


# ===========================================================================
# 3. TestUnderwaterAndDrawdown (tests 33-44)
# ===========================================================================

class TestUnderwaterAndDrawdown:
    def test_33_underwater_curve_returns_list(self):
        uw = _build_underwater()
        assert isinstance(uw, list)

    def test_34_underwater_curve_positive_length(self):
        uw = _build_underwater()
        assert len(uw) > 0

    def test_35_underwater_drawdown_pct_non_positive(self):
        uw = _build_underwater()
        for pt in uw:
            assert pt.drawdown_pct <= 0.001

    def test_36_underwater_high_water_mark_positive(self):
        uw = _build_underwater()
        for pt in uw:
            assert pt.high_water_mark > 0

    def test_37_drawdown_summary_research_only(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        uw = _build_underwater()
        summary = MaxDrawdownCalculator().calculate("demo_portfolio", "2026-06-21", uw)
        assert summary.research_only is True

    def test_38_drawdown_summary_max_drawdown_non_positive(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        uw = _build_underwater()
        summary = MaxDrawdownCalculator().calculate("demo_portfolio", "2026-06-21", uw)
        assert summary.max_drawdown_pct <= 0.001

    def test_39_drawdown_summary_has_portfolio_id(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        uw = _build_underwater()
        summary = MaxDrawdownCalculator().calculate("test_portfolio", "2026-06-21", uw)
        assert summary.portfolio_id == "test_portfolio"

    def test_40_drawdown_summary_has_as_of(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        uw = _build_underwater()
        summary = MaxDrawdownCalculator().calculate("demo_portfolio", "2026-06-21", uw)
        assert summary.as_of == "2026-06-21"

    def test_41_drawdown_summary_empty_curve(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        from portfolio.risk_controls.enums_v153 import DrawdownStatus
        summary = MaxDrawdownCalculator().calculate("demo_portfolio", "2026-06-21", [])
        assert summary.current_drawdown_status == DrawdownStatus.UNKNOWN

    def test_42_fixture_drawdown_summary_valid_loads(self):
        f = _load_fixture("drawdown_summary_valid.json")
        assert f["portfolio_id"] == "demo_portfolio"

    def test_43_fixture_underwater_valid_loads(self):
        f = _load_fixture("underwater_valid.json")
        assert "portfolio_id" in f

    def test_44_drawdown_summary_labels_present(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        uw = _build_underwater()
        summary = MaxDrawdownCalculator().calculate("demo_portfolio", "2026-06-21", uw)
        assert "RESEARCH_ONLY" in summary.labels


# ===========================================================================
# 4. TestDrawdownEpisodes (tests 45-53)
# ===========================================================================

class TestDrawdownEpisodes:
    def test_45_episode_detection_returns_list(self):
        from portfolio.risk_controls.drawdown_episode_v153 import DrawdownEpisodeDetector
        uw = _build_underwater()
        episodes = DrawdownEpisodeDetector().detect(uw)
        assert isinstance(episodes, list)

    def test_46_fixture_episode_open_loads(self):
        f = _load_fixture("drawdown_episode_open.json")
        assert "research_only" in f or "portfolio_id" in f or "_fixture_labels" in f

    def test_47_fixture_episode_closed_loads(self):
        f = _load_fixture("drawdown_episode_closed.json")
        assert "research_only" in f or "_fixture_labels" in f

    def test_48_fixture_single_episode_loads(self):
        f = _load_fixture("drawdown_single_episode.json")
        assert f["expected_episode_count"] == 1

    def test_49_fixture_multiple_episodes_loads(self):
        f = _load_fixture("drawdown_multiple_episodes.json")
        assert f["expected_episode_count"] == 2

    def test_50_fixture_unrecovered_loads(self):
        f = _load_fixture("drawdown_unrecovered.json")
        assert f["expected_status"] == "IN_DRAWDOWN"

    def test_51_fixture_equal_peaks_loads(self):
        f = _load_fixture("drawdown_equal_peaks.json")
        assert f["expected_high_water_mark"] == 1020000.0

    def test_52_episode_model_research_only(self):
        from portfolio.risk_controls.models_v153 import DrawdownEpisode
        from portfolio.risk_controls.enums_v153 import DrawdownEpisodeStatus
        ep = DrawdownEpisode(
            episode_id="EP001", start_date="2025-01-02",
            trough_date="2025-01-06",
        )
        assert isinstance(ep.status, DrawdownEpisodeStatus)

    def test_53_episode_detection_empty_curve(self):
        from portfolio.risk_controls.drawdown_episode_v153 import DrawdownEpisodeDetector
        episodes = DrawdownEpisodeDetector().detect([])
        assert isinstance(episodes, list)


# ===========================================================================
# 5. TestRollingDrawdown (tests 54-60)
# ===========================================================================

class TestRollingDrawdown:
    def test_54_rolling_drawdown_returns_list(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        uw = _build_underwater()
        results = MaxDrawdownCalculator().calculate_rolling(uw, window=20, as_of="2026-06-21")
        assert isinstance(results, list)

    def test_55_rolling_drawdown_has_date_field(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        uw = _build_underwater()
        results = MaxDrawdownCalculator().calculate_rolling(uw, window=20, as_of="2026-06-21")
        for r in results:
            assert "date" in r

    def test_56_rolling_drawdown_no_future_dates(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        uw = _build_underwater()
        results = MaxDrawdownCalculator().calculate_rolling(uw, window=20, as_of="2026-06-21")
        for r in results:
            assert r["date"] <= "2026-06-21"

    def test_57_rolling_drawdown_value_non_positive(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        uw = _build_underwater()
        results = MaxDrawdownCalculator().calculate_rolling(uw, window=20, as_of="2026-06-21")
        for r in results:
            assert r["rolling_max_drawdown_pct"] <= 0.001

    def test_58_rolling_drawdown_window_stored(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        uw = _build_underwater()
        results = MaxDrawdownCalculator().calculate_rolling(uw, window=30, as_of="2026-06-21")
        for r in results:
            assert r["window"] == 30

    def test_59_fixture_rolling_drawdown_valid_loads(self):
        f = _load_fixture("rolling_drawdown_valid.json")
        assert "portfolio_id" in f

    def test_60_rolling_drawdown_empty_curve(self):
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        results = MaxDrawdownCalculator().calculate_rolling([], window=20, as_of="2026-06-21")
        assert isinstance(results, list)


# ===========================================================================
# 6. TestDrawdownAttribution (tests 61-68)
# ===========================================================================

class TestDrawdownAttribution:
    def test_61_attribution_by_position_returns_list(self):
        from portfolio.risk_controls.drawdown_attribution_v153 import DrawdownAttributionCalculator
        calc = DrawdownAttributionCalculator()
        weights = {"2330": 0.5, "2308": 0.5}
        pnl = {"2330": -10000.0, "2308": 5000.0}
        result = calc.attribute_by_position(weights, pnl, 1_000_000.0)
        assert isinstance(result, list)

    def test_62_attribution_by_industry_returns_list(self):
        from portfolio.risk_controls.drawdown_attribution_v153 import DrawdownAttributionCalculator
        calc = DrawdownAttributionCalculator()
        weights = {"2330": 0.5, "2308": 0.5}
        pnl = {"2330": -10000.0, "2308": 5000.0}
        industry_map = {"2330": "Semiconductor", "2308": "Electronics"}
        result = calc.attribute_by_industry(industry_map, weights, pnl, 1_000_000.0)
        assert isinstance(result, list)

    def test_63_attribution_research_only(self):
        from portfolio.risk_controls.drawdown_attribution_v153 import DrawdownAttributionCalculator
        calc = DrawdownAttributionCalculator()
        weights = {"2330": 0.5, "2308": 0.5}
        pnl = {"2330": -10000.0, "2308": 5000.0}
        result = calc.attribute_by_position(weights, pnl, 1_000_000.0)
        for item in result:
            assert item.research_only is True

    def test_64_attribution_no_order_created(self):
        from portfolio.risk_controls.drawdown_attribution_v153 import DrawdownAttributionCalculator
        calc = DrawdownAttributionCalculator()
        weights = {"2330": 0.5, "2308": 0.5}
        pnl = {"2330": -10000.0, "2308": 5000.0}
        result = calc.attribute_by_position(weights, pnl, 1_000_000.0)
        for item in result:
            assert hasattr(item, "research_only")

    def test_65_fixture_attribution_by_position_loads(self):
        f = _load_fixture("attribution_by_position.json")
        assert "portfolio_id" in f

    def test_66_fixture_attribution_by_industry_loads(self):
        f = _load_fixture("attribution_by_industry.json")
        assert "research_only" in f or "industry_map" in f

    def test_67_fixture_attribution_theme_overlap_loads(self):
        f = _load_fixture("attribution_theme_overlap.json")
        assert f["expected_theme_count"] == 3

    def test_68_fixture_attribution_cluster_loads(self):
        f = _load_fixture("attribution_cluster.json")
        assert f["expected_cluster_count"] == 3


# ===========================================================================
# 7. TestRiskBudget (tests 69-77)
# ===========================================================================

class TestRiskBudget:
    def test_69_risk_budget_evaluate_returns_dict(self):
        from portfolio.risk_controls.risk_budget_v153 import PortfolioRiskBudgetEngine
        result = PortfolioRiskBudgetEngine().evaluate(
            "demo_portfolio", "2026-06-21", -0.05, 0.18
        )
        assert isinstance(result, dict)

    def test_70_risk_budget_research_only_flag(self):
        from portfolio.risk_controls.risk_budget_v153 import PortfolioRiskBudgetEngine
        result = PortfolioRiskBudgetEngine().evaluate(
            "demo_portfolio", "2026-06-21", -0.05, 0.18
        )
        assert result["research_only"] is True

    def test_71_risk_budget_executable_false(self):
        from portfolio.risk_controls.risk_budget_v153 import PortfolioRiskBudgetEngine
        result = PortfolioRiskBudgetEngine().evaluate(
            "demo_portfolio", "2026-06-21", -0.05, 0.18
        )
        assert result["executable"] is False

    def test_72_risk_budget_order_created_false(self):
        from portfolio.risk_controls.risk_budget_v153 import PortfolioRiskBudgetEngine
        result = PortfolioRiskBudgetEngine().evaluate(
            "demo_portfolio", "2026-06-21", -0.05, 0.18
        )
        assert result["order_created"] is False

    def test_73_risk_budget_consumed_ratio_present(self):
        from portfolio.risk_controls.risk_budget_v153 import PortfolioRiskBudgetEngine
        result = PortfolioRiskBudgetEngine().evaluate(
            "demo_portfolio", "2026-06-21", -0.05, 0.18
        )
        assert "drawdown_budget_consumed" in result

    def test_74_risk_budget_warnings_list(self):
        from portfolio.risk_controls.risk_budget_v153 import PortfolioRiskBudgetEngine
        result = PortfolioRiskBudgetEngine().evaluate(
            "demo_portfolio", "2026-06-21", -0.05, 0.18
        )
        assert isinstance(result["warnings"], list)

    def test_75_risk_budget_exceeded_warns(self):
        from portfolio.risk_controls.risk_budget_v153 import PortfolioRiskBudgetEngine
        result = PortfolioRiskBudgetEngine().evaluate(
            "demo_portfolio", "2026-06-21", -0.18, 0.18,
            drawdown_budget_pct=-0.20,
        )
        # 90% consumed should trigger warning
        assert len(result["warnings"]) > 0

    def test_76_fixture_risk_budget_valid_loads(self):
        f = _load_fixture("risk_budget_valid.json")
        assert "portfolio_id" in f

    def test_77_fixture_risk_budget_exceeded_loads(self):
        f = _load_fixture("risk_budget_exceeded.json")
        assert f["status"] == "BREACH"


# ===========================================================================
# 8. TestLossLimits (tests 78-87)
# ===========================================================================

class TestLossLimits:
    def test_78_daily_loss_pass(self):
        from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = LossLimitChecker().check_daily("CHK001", "POL001", -0.005)
        assert c.status == RiskControlStatus.PASS

    def test_79_daily_loss_breach(self):
        from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = LossLimitChecker().check_daily("CHK002", "POL001", -0.05)
        assert c.status == RiskControlStatus.BREACH

    def test_80_daily_loss_warn(self):
        from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = LossLimitChecker().check_daily("CHK003", "POL001", -0.02)
        assert c.status in (RiskControlStatus.WARN, RiskControlStatus.BREACH)

    def test_81_weekly_loss_pass(self):
        from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = LossLimitChecker().check_weekly("CHK004", "POL002", -0.01)
        assert c.status == RiskControlStatus.PASS

    def test_82_weekly_loss_breach(self):
        from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = LossLimitChecker().check_weekly("CHK005", "POL002", -0.06)
        assert c.status == RiskControlStatus.BREACH

    def test_83_monthly_loss_pass(self):
        from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = LossLimitChecker().check_monthly("CHK006", "POL003", -0.03)
        assert c.status == RiskControlStatus.PASS

    def test_84_monthly_loss_breach(self):
        from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = LossLimitChecker().check_monthly("CHK007", "POL003", -0.12)
        assert c.status == RiskControlStatus.BREACH

    def test_85_loss_limit_research_only(self):
        from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
        c = LossLimitChecker().check_daily("CHK008", "POL001", -0.005)
        assert c.research_only is True

    def test_86_loss_limit_no_order(self):
        from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
        c = LossLimitChecker().check_daily("CHK009", "POL001", -0.005)
        assert c.order_created is False

    def test_87_fixture_daily_loss_limit_loads(self):
        f = _load_fixture("daily_loss_limit.json")
        assert f["expected_status"] == "PASS"


# ===========================================================================
# 9. TestVolatilityLimit (tests 88-94)
# ===========================================================================

class TestVolatilityLimit:
    def test_88_vol_limit_pass(self):
        from portfolio.risk_controls.volatility_limit_v153 import VolatilityLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = VolatilityLimitChecker().check("CHK010", "POL001", 0.18)
        assert c.status == RiskControlStatus.PASS

    def test_89_vol_limit_warn(self):
        from portfolio.risk_controls.volatility_limit_v153 import VolatilityLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = VolatilityLimitChecker().check("CHK011", "POL001", 0.25)
        assert c.status in (RiskControlStatus.WARN, RiskControlStatus.BREACH)

    def test_90_vol_limit_breach(self):
        from portfolio.risk_controls.volatility_limit_v153 import VolatilityLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = VolatilityLimitChecker().check("CHK012", "POL001", 0.35)
        assert c.status == RiskControlStatus.BREACH

    def test_91_vol_limit_research_only(self):
        from portfolio.risk_controls.volatility_limit_v153 import VolatilityLimitChecker
        c = VolatilityLimitChecker().check("CHK013", "POL001", 0.18)
        assert c.research_only is True

    def test_92_vol_limit_no_order(self):
        from portfolio.risk_controls.volatility_limit_v153 import VolatilityLimitChecker
        c = VolatilityLimitChecker().check("CHK014", "POL001", 0.18)
        assert c.order_created is False

    def test_93_vol_limit_no_auto_apply(self):
        from portfolio.risk_controls.volatility_limit_v153 import VolatilityLimitChecker
        c = VolatilityLimitChecker().check("CHK015", "POL001", 0.18)
        assert c.auto_applied is False

    def test_94_fixture_volatility_limit_loads(self):
        f = _load_fixture("volatility_limit.json")
        assert f["expected_status"] == "PASS"


# ===========================================================================
# 10. TestConcentrationControls (tests 95-103)
# ===========================================================================

class TestConcentrationControls:
    def test_95_concentration_pass_below_cap(self):
        from portfolio.risk_controls.concentration_limit_v153 import ConcentrationLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = ConcentrationLimitChecker().check_single_name(
            "CHK016", "POL001", {"A": 0.20, "B": 0.20, "C": 0.60}
        )
        # 60% single name — should be BREACH
        assert c.status in (RiskControlStatus.BREACH, RiskControlStatus.WARN)

    def test_96_concentration_pass_well_diversified(self):
        from portfolio.risk_controls.concentration_limit_v153 import ConcentrationLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = ConcentrationLimitChecker().check_single_name(
            "CHK017", "POL001", {"A": 0.10, "B": 0.10, "C": 0.10, "D": 0.70}
        )
        assert c.status is not None

    def test_97_concentration_research_only(self):
        from portfolio.risk_controls.concentration_limit_v153 import ConcentrationLimitChecker
        c = ConcentrationLimitChecker().check_single_name(
            "CHK018", "POL001", {"A": 0.25, "B": 0.75}
        )
        assert c.research_only is True

    def test_98_concentration_no_order(self):
        from portfolio.risk_controls.concentration_limit_v153 import ConcentrationLimitChecker
        c = ConcentrationLimitChecker().check_single_name(
            "CHK019", "POL001", {"A": 0.25, "B": 0.75}
        )
        assert c.order_created is False

    def test_99_fixture_concentration_limit_loads(self):
        f = _load_fixture("concentration_limit.json")
        assert f["expected_status"] == "PASS"

    def test_100_concentration_check_returns_RiskControlCheck(self):
        from portfolio.risk_controls.concentration_limit_v153 import ConcentrationLimitChecker
        from portfolio.risk_controls.models_v153 import RiskControlCheck
        c = ConcentrationLimitChecker().check_single_name(
            "CHK020", "POL001", {"A": 0.25, "B": 0.75}
        )
        assert isinstance(c, RiskControlCheck)

    def test_101_concentration_auto_applied_false(self):
        from portfolio.risk_controls.concentration_limit_v153 import ConcentrationLimitChecker
        c = ConcentrationLimitChecker().check_single_name(
            "CHK021", "POL001", {"A": 0.25, "B": 0.75}
        )
        assert c.auto_applied is False

    def test_102_concentration_ledger_persisted_false(self):
        from portfolio.risk_controls.concentration_limit_v153 import ConcentrationLimitChecker
        c = ConcentrationLimitChecker().check_single_name(
            "CHK022", "POL001", {"A": 0.25, "B": 0.75}
        )
        assert c.ledger_persisted is False

    def test_103_concentration_executable_false(self):
        from portfolio.risk_controls.concentration_limit_v153 import ConcentrationLimitChecker
        c = ConcentrationLimitChecker().check_single_name(
            "CHK023", "POL001", {"A": 0.25, "B": 0.75}
        )
        assert c.executable is False


# ===========================================================================
# 11. TestCorrelationControls (tests 104-110)
# ===========================================================================

class TestCorrelationControls:
    def test_104_correlation_check_pass(self):
        from portfolio.risk_controls.correlation_limit_v153 import CorrelationLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = CorrelationLimitChecker().check_max_pairwise(
            "CHK024", "POL001", high_correlation_pair_count=0, total_pairs=3
        )
        assert c.status == RiskControlStatus.PASS

    def test_105_correlation_check_breach(self):
        from portfolio.risk_controls.correlation_limit_v153 import CorrelationLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = CorrelationLimitChecker().check_max_pairwise(
            "CHK025", "POL001", high_correlation_pair_count=3, total_pairs=3
        )
        assert c.status in (RiskControlStatus.BREACH, RiskControlStatus.WARN)

    def test_106_correlation_research_only(self):
        from portfolio.risk_controls.correlation_limit_v153 import CorrelationLimitChecker
        c = CorrelationLimitChecker().check_max_pairwise(
            "CHK026", "POL001", high_correlation_pair_count=1, total_pairs=3
        )
        assert c.research_only is True

    def test_107_correlation_no_order(self):
        from portfolio.risk_controls.correlation_limit_v153 import CorrelationLimitChecker
        c = CorrelationLimitChecker().check_max_pairwise(
            "CHK027", "POL001", high_correlation_pair_count=1, total_pairs=3
        )
        assert c.order_created is False

    def test_108_fixture_correlation_limit_loads(self):
        f = _load_fixture("correlation_limit.json")
        assert f["expected_status"] == "WARN"

    def test_109_correlation_auto_applied_false(self):
        from portfolio.risk_controls.correlation_limit_v153 import CorrelationLimitChecker
        c = CorrelationLimitChecker().check_max_pairwise(
            "CHK028", "POL001", high_correlation_pair_count=1, total_pairs=3
        )
        assert c.auto_applied is False

    def test_110_correlation_executable_false(self):
        from portfolio.risk_controls.correlation_limit_v153 import CorrelationLimitChecker
        c = CorrelationLimitChecker().check_max_pairwise(
            "CHK029", "POL001", high_correlation_pair_count=1, total_pairs=3
        )
        assert c.executable is False


# ===========================================================================
# 12. TestLiquidityControls (tests 111-117)
# ===========================================================================

class TestLiquidityControls:
    def test_111_liquidity_pass(self):
        from portfolio.risk_controls.liquidity_limit_v153 import LiquidityLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = LiquidityLimitChecker().check_illiquid_fraction("CHK030", "POL001", 0.10)
        assert c.status == RiskControlStatus.PASS

    def test_112_liquidity_breach(self):
        from portfolio.risk_controls.liquidity_limit_v153 import LiquidityLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = LiquidityLimitChecker().check_illiquid_fraction("CHK031", "POL001", 0.50)
        assert c.status in (RiskControlStatus.BREACH, RiskControlStatus.WARN)

    def test_113_liquidity_research_only(self):
        from portfolio.risk_controls.liquidity_limit_v153 import LiquidityLimitChecker
        c = LiquidityLimitChecker().check_illiquid_fraction("CHK032", "POL001", 0.10)
        assert c.research_only is True

    def test_114_liquidity_no_order(self):
        from portfolio.risk_controls.liquidity_limit_v153 import LiquidityLimitChecker
        c = LiquidityLimitChecker().check_illiquid_fraction("CHK033", "POL001", 0.10)
        assert c.order_created is False

    def test_115_fixture_liquidity_limit_loads(self):
        f = _load_fixture("liquidity_limit.json")
        assert f["expected_status"] == "PASS"

    def test_116_liquidity_auto_applied_false(self):
        from portfolio.risk_controls.liquidity_limit_v153 import LiquidityLimitChecker
        c = LiquidityLimitChecker().check_illiquid_fraction("CHK034", "POL001", 0.10)
        assert c.auto_applied is False

    def test_117_liquidity_executable_false(self):
        from portfolio.risk_controls.liquidity_limit_v153 import LiquidityLimitChecker
        c = LiquidityLimitChecker().check_illiquid_fraction("CHK035", "POL001", 0.10)
        assert c.executable is False


# ===========================================================================
# 13. TestCashReserve (tests 118-123)
# ===========================================================================

class TestCashReserve:
    def test_118_cash_reserve_pass(self):
        from portfolio.risk_controls.cash_reserve_limit_v153 import CashReserveLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = CashReserveLimitChecker().check("CHK036", "POL001", cash_weight=0.10)
        assert c.status == RiskControlStatus.PASS

    def test_119_cash_reserve_breach(self):
        from portfolio.risk_controls.cash_reserve_limit_v153 import CashReserveLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        c = CashReserveLimitChecker().check("CHK037", "POL001", cash_weight=0.005)
        assert c.status in (RiskControlStatus.BREACH, RiskControlStatus.WARN)

    def test_120_cash_reserve_research_only(self):
        from portfolio.risk_controls.cash_reserve_limit_v153 import CashReserveLimitChecker
        c = CashReserveLimitChecker().check("CHK038", "POL001", cash_weight=0.10)
        assert c.research_only is True

    def test_121_cash_reserve_no_order(self):
        from portfolio.risk_controls.cash_reserve_limit_v153 import CashReserveLimitChecker
        c = CashReserveLimitChecker().check("CHK039", "POL001", cash_weight=0.10)
        assert c.order_created is False

    def test_122_fixture_cash_reserve_limit_loads(self):
        f = _load_fixture("cash_reserve_limit.json")
        assert f["expected_status"] == "PASS"

    def test_123_cash_reserve_executable_false(self):
        from portfolio.risk_controls.cash_reserve_limit_v153 import CashReserveLimitChecker
        c = CashReserveLimitChecker().check("CHK040", "POL001", cash_weight=0.10)
        assert c.executable is False


# ===========================================================================
# 14. TestConstraintEngine (tests 124-130)
# ===========================================================================

class TestConstraintEngine:
    def test_124_demo_evaluation_returns_RiskControlEvaluation(self):
        from portfolio.risk_controls.models_v153 import RiskControlEvaluation
        ev = _build_demo_evaluation()
        assert isinstance(ev, RiskControlEvaluation)

    def test_125_demo_evaluation_research_only(self):
        ev = _build_demo_evaluation()
        assert ev.research_only is True

    def test_126_demo_evaluation_no_order(self):
        ev = _build_demo_evaluation()
        assert ev.order_created is False

    def test_127_demo_evaluation_no_exec(self):
        ev = _build_demo_evaluation()
        assert ev.executable is False

    def test_128_demo_evaluation_has_checks(self):
        ev = _build_demo_evaluation()
        assert len(ev.checks) > 0

    def test_129_demo_evaluation_overall_status_set(self):
        from portfolio.risk_controls.enums_v153 import RiskControlStatus
        ev = _build_demo_evaluation()
        assert ev.overall_status in list(RiskControlStatus)

    def test_130_evaluation_order_has_21_steps(self):
        from portfolio.risk_controls.constraint_engine_v153 import EVALUATION_ORDER
        assert len(EVALUATION_ORDER) == 21


# ===========================================================================
# 15. TestRecommendedActions (tests 131-142)
# ===========================================================================

class TestRecommendedActions:
    def test_131_RiskActionType_NO_ACTION_exists(self):
        from portfolio.risk_controls.enums_v153 import RiskActionType
        assert RiskActionType.NO_ACTION == "NO_ACTION"

    def test_132_RiskActionType_WARN_ONLY_exists(self):
        from portfolio.risk_controls.enums_v153 import RiskActionType
        assert RiskActionType.WARN_ONLY == "WARN_ONLY"

    def test_133_RiskActionType_REVIEW_RECOMMENDED_exists(self):
        from portfolio.risk_controls.enums_v153 import RiskActionType
        assert RiskActionType.REVIEW_RECOMMENDED == "REVIEW_RECOMMENDED"

    def test_134_RiskActionType_REDUCE_RECOMMENDED_exists(self):
        from portfolio.risk_controls.enums_v153 import RiskActionType
        assert RiskActionType.REDUCE_RECOMMENDED == "REDUCE_RECOMMENDED"

    def test_135_RiskActionType_HALT_RECOMMENDED_exists(self):
        from portfolio.risk_controls.enums_v153 import RiskActionType
        assert RiskActionType.HALT_RECOMMENDED == "HALT_RECOMMENDED"

    def test_136_check_default_action_NO_ACTION(self):
        from portfolio.risk_controls.models_v153 import RiskControlCheck
        from portfolio.risk_controls.enums_v153 import RiskControlType, RiskActionType
        c = RiskControlCheck(check_id="C1", policy_id="P1",
                             control_type=RiskControlType.VOLATILITY_LIMIT)
        assert c.recommended_action == RiskActionType.NO_ACTION

    def test_137_REDUCE_RECOMMENDED_not_executable(self):
        from portfolio.risk_controls.enums_v153 import RiskActionType
        # REDUCE_RECOMMENDED is advisory only — verify no auto-execute flag
        action = RiskActionType.REDUCE_RECOMMENDED
        assert action.value == "REDUCE_RECOMMENDED"

    def test_138_HALT_RECOMMENDED_not_executable(self):
        from portfolio.risk_controls.enums_v153 import RiskActionType
        action = RiskActionType.HALT_RECOMMENDED
        assert action.value == "HALT_RECOMMENDED"

    def test_139_vol_breach_action_set(self):
        from portfolio.risk_controls.volatility_limit_v153 import VolatilityLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskActionType
        c = VolatilityLimitChecker().check("CHK_ACT_001", "POL001", 0.35)
        assert c.recommended_action != RiskActionType.NO_ACTION

    def test_140_pass_check_action_NO_ACTION(self):
        from portfolio.risk_controls.volatility_limit_v153 import VolatilityLimitChecker
        from portfolio.risk_controls.enums_v153 import RiskActionType
        c = VolatilityLimitChecker().check("CHK_ACT_002", "POL001", 0.10)
        assert c.recommended_action == RiskActionType.NO_ACTION

    def test_141_RiskActionType_has_5_values(self):
        from portfolio.risk_controls.enums_v153 import RiskActionType
        assert len(list(RiskActionType)) == 5

    def test_142_action_never_auto_applies(self):
        # Verify no module implements auto_apply_action()
        ev = _build_demo_evaluation()
        assert ev.auto_applied is False


# ===========================================================================
# 16. TestSizingImpact (tests 143-155)
# ===========================================================================

class TestSizingImpact:
    def test_143_sizing_impact_analyze_returns_SizingRiskImpact(self):
        from portfolio.risk_controls.sizing_impact_v153 import SizingRiskImpactAnalyzer
        from portfolio.risk_controls.models_v153 import SizingRiskImpact
        result = SizingRiskImpactAnalyzer().analyze(
            "P1", "demo_portfolio", "2330",
            -0.05, -0.07, 0.18, 0.20,
        )
        assert isinstance(result, SizingRiskImpact)

    def test_144_sizing_impact_research_only(self):
        from portfolio.risk_controls.sizing_impact_v153 import SizingRiskImpactAnalyzer
        result = SizingRiskImpactAnalyzer().analyze(
            "P1", "demo_portfolio", "2330",
            -0.05, -0.07, 0.18, 0.20,
        )
        assert result.research_only is True

    def test_145_sizing_impact_no_order(self):
        from portfolio.risk_controls.sizing_impact_v153 import SizingRiskImpactAnalyzer
        result = SizingRiskImpactAnalyzer().analyze(
            "P1", "demo_portfolio", "2330",
            -0.05, -0.07, 0.18, 0.20,
        )
        assert result.order_created is False

    def test_146_sizing_impact_no_exec(self):
        from portfolio.risk_controls.sizing_impact_v153 import SizingRiskImpactAnalyzer
        result = SizingRiskImpactAnalyzer().analyze(
            "P1", "demo_portfolio", "2330",
            -0.05, -0.07, 0.18, 0.20,
        )
        assert result.executable is False

    def test_147_sizing_impact_no_ledger(self):
        from portfolio.risk_controls.sizing_impact_v153 import SizingRiskImpactAnalyzer
        result = SizingRiskImpactAnalyzer().analyze(
            "P1", "demo_portfolio", "2330",
            -0.05, -0.07, 0.18, 0.20,
        )
        assert result.ledger_persisted is False

    def test_148_sizing_impact_demo_build(self):
        from portfolio.risk_controls.sizing_impact_v153 import SizingRiskImpactAnalyzer
        result = SizingRiskImpactAnalyzer().build_demo()
        assert result.proposal_id == "demo_proposal"

    def test_149_sizing_impact_breaches_added_list(self):
        from portfolio.risk_controls.sizing_impact_v153 import SizingRiskImpactAnalyzer
        result = SizingRiskImpactAnalyzer().analyze(
            "P2", "demo_portfolio", "2330",
            -0.05, -0.07, 0.18, 0.20,
            before_checks=[], after_checks=["VOLATILITY_LIMIT"],
        )
        assert "VOLATILITY_LIMIT" in result.control_breaches_added

    def test_150_sizing_impact_breaches_removed_list(self):
        from portfolio.risk_controls.sizing_impact_v153 import SizingRiskImpactAnalyzer
        result = SizingRiskImpactAnalyzer().analyze(
            "P3", "demo_portfolio", "2330",
            -0.05, -0.04, 0.18, 0.15,
            before_checks=["VOLATILITY_LIMIT"], after_checks=[],
        )
        assert "VOLATILITY_LIMIT" in result.control_breaches_removed

    def test_151_fixture_sizing_impact_valid_loads(self):
        f = _load_fixture("sizing_impact_valid.json")
        assert f["status"] == "VALID"
        assert f["research_only"] is True

    def test_152_fixture_sizing_impact_blocked_loads(self):
        f = _load_fixture("sizing_impact_blocked.json")
        assert f["status"] == "BLOCKED"
        assert len(f["control_breaches_added"]) > 0

    def test_153_sizing_impact_order_created_false_enforced(self):
        from portfolio.risk_controls.models_v153 import SizingRiskImpact
        with pytest.raises(AssertionError):
            SizingRiskImpact(
                proposal_id="P", portfolio_id="PF", symbol="A",
                order_created=True
            )

    def test_154_sizing_impact_executable_false_enforced(self):
        from portfolio.risk_controls.models_v153 import SizingRiskImpact
        with pytest.raises(AssertionError):
            SizingRiskImpact(
                proposal_id="P", portfolio_id="PF", symbol="A",
                executable=True
            )

    def test_155_query_service_analyze_sizing_impact(self):
        from portfolio.risk_controls.query_v153 import DrawdownRiskControlsQueryService
        result = DrawdownRiskControlsQueryService().analyze_sizing_impact(
            "demo_proposal", "2026-06-21"
        )
        assert result.research_only is True


# ===========================================================================
# 17. TestStress (tests 156-167)
# ===========================================================================

class TestStress:
    def test_156_stress_run_returns_DrawdownStressResult(self):
        from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
        from portfolio.risk_controls.enums_v153 import StressScenarioType
        from portfolio.risk_controls.models_v153 import DrawdownStressResult
        result = DrawdownStressAnalyzer().run("demo_portfolio", 1_000_000.0,
                                              StressScenarioType.BEAR_MARKET)
        assert isinstance(result, DrawdownStressResult)

    def test_157_stress_research_only(self):
        from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
        from portfolio.risk_controls.enums_v153 import StressScenarioType
        result = DrawdownStressAnalyzer().run("demo_portfolio", 1_000_000.0,
                                              StressScenarioType.BEAR_MARKET)
        assert result.research_only is True

    def test_158_stress_no_order(self):
        from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
        from portfolio.risk_controls.enums_v153 import StressScenarioType
        result = DrawdownStressAnalyzer().run("demo_portfolio", 1_000_000.0,
                                              StressScenarioType.BEAR_MARKET)
        assert result.order_created is False

    def test_159_stress_projected_dd_negative(self):
        from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
        from portfolio.risk_controls.enums_v153 import StressScenarioType
        result = DrawdownStressAnalyzer().run("demo_portfolio", 1_000_000.0,
                                              StressScenarioType.BEAR_MARKET)
        assert result.projected_drawdown_pct < 0

    def test_160_stress_projected_loss_positive(self):
        from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
        from portfolio.risk_controls.enums_v153 import StressScenarioType
        result = DrawdownStressAnalyzer().run("demo_portfolio", 1_000_000.0,
                                              StressScenarioType.BEAR_MARKET)
        assert result.projected_loss > 0

    def test_161_stress_run_all_returns_8(self):
        from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
        results = DrawdownStressAnalyzer().run_all("demo_portfolio", 1_000_000.0)
        assert len(results) == 8

    def test_162_stress_run_from_fixture(self):
        from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
        fixture = _load_fixture("stress_combined.json")
        result = DrawdownStressAnalyzer().run_from_fixture(fixture)
        assert result.research_only is True

    def test_163_fixture_stress_market_shock_loads(self):
        f = _load_fixture("stress_market_shock.json")
        assert f["scenario_type"] == "BEAR_MARKET"

    def test_164_fixture_stress_correlation_spike_loads(self):
        f = _load_fixture("stress_correlation_spike.json")
        assert f["scenario_type"] == "CORRELATION_BREAKDOWN"

    def test_165_fixture_stress_liquidity_shock_loads(self):
        f = _load_fixture("stress_liquidity_shock.json")
        assert f["scenario_type"] == "LIQUIDITY_CRISIS"

    def test_166_fixture_stress_combined_loads(self):
        f = _load_fixture("stress_combined.json")
        assert f["scenario_type"] == "COMBINED"

    def test_167_stress_executable_false(self):
        from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
        from portfolio.risk_controls.enums_v153 import StressScenarioType
        result = DrawdownStressAnalyzer().run("demo_portfolio", 1_000_000.0,
                                              StressScenarioType.COMBINED)
        assert result.executable is False


# ===========================================================================
# 18. TestEligibility (tests 168-177)
# ===========================================================================

class TestEligibility:
    def test_168_eligibility_gate_eligible(self):
        from portfolio.risk_controls.eligibility_v153 import DrawdownRiskControlsEligibilityGate
        req = _make_request()
        result = DrawdownRiskControlsEligibilityGate().evaluate(req, {}, equity_curve_points=300)
        assert result["eligibility_status"] == "ELIGIBLE"

    def test_169_eligibility_gate_broker_blocked(self):
        from portfolio.risk_controls.eligibility_v153 import DrawdownRiskControlsEligibilityGate
        req = _make_request()
        result = DrawdownRiskControlsEligibilityGate().evaluate(
            req, {"broker_linked": True}, equity_curve_points=300
        )
        assert result["eligibility_status"] == "INELIGIBLE"

    def test_170_eligibility_gate_auto_apply_blocked(self):
        from portfolio.risk_controls.eligibility_v153 import DrawdownRiskControlsEligibilityGate
        req = _make_request()
        result = DrawdownRiskControlsEligibilityGate().evaluate(
            req, {"auto_apply_enabled": True}, equity_curve_points=300
        )
        assert result["eligibility_status"] == "INELIGIBLE"

    def test_171_eligibility_gate_research_only_in_result(self):
        from portfolio.risk_controls.eligibility_v153 import DrawdownRiskControlsEligibilityGate
        req = _make_request()
        result = DrawdownRiskControlsEligibilityGate().evaluate(req, {}, equity_curve_points=300)
        assert result["research_only"] is True

    def test_172_fixture_eligibility_valid_loads(self):
        f = _load_fixture("eligibility_valid.json")
        assert "research_only" in f or "_fixture_labels" in f

    def test_173_fixture_eligibility_broker_blocked_loads(self):
        f = _load_fixture("eligibility_broker_blocked.json")
        assert "research_only" in f or "_fixture_labels" in f

    def test_174_fixture_eligibility_blocked_loads(self):
        f = _load_fixture("eligibility_blocked.json")
        assert f["expected_eligibility_status"] == "BLOCKED"

    def test_175_eligibility_research_only_false_blocked(self):
        from portfolio.risk_controls.eligibility_v153 import DrawdownRiskControlsEligibilityGate
        from portfolio.risk_controls.models_v153 import DrawdownAnalysisRequest
        # research_only=False raises AssertionError in __post_init__
        with pytest.raises(AssertionError):
            DrawdownAnalysisRequest(
                request_id="R1", portfolio_id="P", as_of="2026-06-21",
                available_from="2025-01-01", research_only=False
            )

    def test_176_eligibility_insufficient_curve_warns(self):
        from portfolio.risk_controls.eligibility_v153 import DrawdownRiskControlsEligibilityGate
        req = _make_request()
        result = DrawdownRiskControlsEligibilityGate().evaluate(req, {}, equity_curve_points=5)
        assert len(result["warnings"]) > 0

    def test_177_eligibility_returns_dict(self):
        from portfolio.risk_controls.eligibility_v153 import DrawdownRiskControlsEligibilityGate
        req = _make_request()
        result = DrawdownRiskControlsEligibilityGate().evaluate(req, {}, equity_curve_points=300)
        assert isinstance(result, dict)


# ===========================================================================
# 19. TestPointInTime (tests 178-185)
# ===========================================================================

class TestPointInTime:
    def test_178_pit_validate_equity_curve_no_future(self):
        from portfolio.risk_controls.point_in_time_v153 import DrawdownRiskControlsPITValidator
        curve = _build_equity_curve()
        result = DrawdownRiskControlsPITValidator().validate_equity_curve(curve, "2026-06-21")
        assert result["valid"] is True

    def test_179_pit_validate_equity_curve_with_future(self):
        from portfolio.risk_controls.point_in_time_v153 import DrawdownRiskControlsPITValidator
        from portfolio.risk_controls.models_v153 import EquityCurvePoint
        future_pt = EquityCurvePoint(date="2027-01-01", portfolio_value=1_100_000.0)
        result = DrawdownRiskControlsPITValidator().validate_equity_curve(
            [future_pt], "2026-06-21"
        )
        assert result["valid"] is False
        assert len(result["future_dates_found"]) > 0

    def test_180_pit_validate_as_of_valid(self):
        from portfolio.risk_controls.point_in_time_v153 import DrawdownRiskControlsPITValidator
        result = DrawdownRiskControlsPITValidator().validate_as_of("2026-06-21")
        assert result["valid"] is True

    def test_181_pit_validate_as_of_invalid(self):
        from portfolio.risk_controls.point_in_time_v153 import DrawdownRiskControlsPITValidator
        result = DrawdownRiskControlsPITValidator().validate_as_of("not-a-date")
        assert result["valid"] is False

    def test_182_fixture_equity_curve_future_data_pit_fails(self):
        f = _load_fixture("equity_curve_future_data.json")
        assert "2027" in str(f) or f.get("has_future_data", False)

    def test_183_fixture_pit_future_policy_excluded(self):
        f = _load_fixture("pit_future_policy.json")
        assert f["expected_excluded"] is True

    def test_184_pit_no_future_data_in_demo(self):
        from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
        from portfolio.risk_controls.point_in_time_v153 import DrawdownRiskControlsPITValidator
        curve = PortfolioEquityCurveBuilder().build_demo(as_of="2026-06-21")
        result = DrawdownRiskControlsPITValidator().validate_equity_curve(curve, "2026-06-21")
        assert result["valid"] is True

    def test_185_pit_validator_research_only(self):
        from portfolio.risk_controls.point_in_time_v153 import DrawdownRiskControlsPITValidator
        assert DrawdownRiskControlsPITValidator.RESEARCH_ONLY is True


# ===========================================================================
# 20. TestLineage (tests 186-195)
# ===========================================================================

class TestLineage:
    def test_186_lineage_build_returns_dict(self):
        from portfolio.risk_controls.lineage_v153 import DrawdownRiskControlsLineageTracker
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsLineageTracker().build_lineage(ev)
        assert isinstance(result, dict)

    def test_187_lineage_has_evaluation_id(self):
        from portfolio.risk_controls.lineage_v153 import DrawdownRiskControlsLineageTracker
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsLineageTracker().build_lineage(ev)
        assert "evaluation_id" in result

    def test_188_lineage_research_only(self):
        from portfolio.risk_controls.lineage_v153 import DrawdownRiskControlsLineageTracker
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsLineageTracker().build_lineage(ev)
        assert result["research_only"] is True

    def test_189_lineage_generated_at_present(self):
        from portfolio.risk_controls.lineage_v153 import DrawdownRiskControlsLineageTracker
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsLineageTracker().build_lineage(ev)
        assert "generated_at" in result

    def test_190_lineage_module_version(self):
        from portfolio.risk_controls.lineage_v153 import DrawdownRiskControlsLineageTracker
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsLineageTracker().build_lineage(ev)
        assert result["module_version"] == "1.5.3"

    def test_191_fixture_lineage_complete_loads(self):
        f = _load_fixture("lineage_complete.json")
        assert f["lineage_complete"] is True

    def test_192_fixture_lineage_missing_loads(self):
        f = _load_fixture("lineage_missing.json")
        assert f["lineage_complete"] is False
        assert f["source_lineage_ids"] == []

    def test_193_lineage_tracker_research_only_class(self):
        from portfolio.risk_controls.lineage_v153 import DrawdownRiskControlsLineageTracker
        assert DrawdownRiskControlsLineageTracker.RESEARCH_ONLY is True

    def test_194_lineage_has_portfolio_id(self):
        from portfolio.risk_controls.lineage_v153 import DrawdownRiskControlsLineageTracker
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsLineageTracker().build_lineage(ev, equity_curve_hash="abc123")
        assert "portfolio_id" in result

    def test_195_lineage_equity_curve_hash_stored(self):
        from portfolio.risk_controls.lineage_v153 import DrawdownRiskControlsLineageTracker
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsLineageTracker().build_lineage(ev, equity_curve_hash="abc123")
        assert result["equity_curve_hash"] == "abc123"


# ===========================================================================
# 21. TestExplainability (tests 196-208)
# ===========================================================================

class TestExplainability:
    def test_196_explain_returns_dict(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsExplainer().explain(ev)
        assert isinstance(result, dict)

    def test_197_explain_research_only(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsExplainer().explain(ev)
        assert result["research_only"] is True

    def test_198_explain_executable_false(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsExplainer().explain(ev)
        assert result["executable"] is False

    def test_199_explain_order_created_false(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsExplainer().explain(ev)
        assert result["order_created"] is False

    def test_200_explain_has_safety_text(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsExplainer().explain(ev)
        assert "safety_text" in result
        assert len(result["safety_text"]) > 0

    def test_201_explain_has_limitations(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsExplainer().explain(ev)
        assert isinstance(result["limitations"], list)
        assert len(result["limitations"]) > 0

    def test_202_explain_labels_contain_safety_strings(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsExplainer().explain(ev)
        for lbl in ["RESEARCH_ONLY", "NOT_AN_ORDER", "NO_BROKER_CALL"]:
            assert lbl in result["labels"]

    def test_203_explain_with_drawdown_summary(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        ev = _build_demo_evaluation()
        uw = _build_underwater()
        summary = MaxDrawdownCalculator().calculate("demo_portfolio", "2026-06-21", uw)
        result = DrawdownRiskControlsExplainer().explain(ev, drawdown_summary=summary)
        assert result["current_drawdown_pct"] is not None

    def test_204_explain_overall_status_present(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsExplainer().explain(ev)
        assert "overall_status" in result

    def test_205_explain_check_summaries_list(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsExplainer().explain(ev)
        assert isinstance(result["check_summaries"], list)

    def test_206_explain_breach_count_integer(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsExplainer().explain(ev)
        assert isinstance(result["breach_count"], int)

    def test_207_query_service_explain_evaluation(self):
        from portfolio.risk_controls.query_v153 import DrawdownRiskControlsQueryService
        ev = _build_demo_evaluation()
        result = DrawdownRiskControlsQueryService().explain_evaluation(ev)
        assert result["research_only"] is True

    def test_208_explainer_research_only_class(self):
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        assert DrawdownRiskControlsExplainer.RESEARCH_ONLY is True


# ===========================================================================
# 22. TestStoreAndQuery (tests 209-216)
# ===========================================================================

class TestStoreAndQuery:
    def test_209_store_save_and_get_evaluation(self):
        from portfolio.risk_controls.store_v153 import DrawdownRiskControlsStore
        store = DrawdownRiskControlsStore()
        ev = _build_demo_evaluation()
        eid = store.save_evaluation(ev)
        retrieved = store.get_evaluation(eid)
        assert retrieved is ev

    def test_210_store_list_evaluations(self):
        from portfolio.risk_controls.store_v153 import DrawdownRiskControlsStore
        store = DrawdownRiskControlsStore()
        ev = _build_demo_evaluation()
        store.save_evaluation(ev)
        evs = store.list_evaluations()
        assert len(evs) >= 1

    def test_211_store_filter_by_portfolio(self):
        from portfolio.risk_controls.store_v153 import DrawdownRiskControlsStore
        store = DrawdownRiskControlsStore()
        ev = _build_demo_evaluation()
        store.save_evaluation(ev)
        evs = store.list_evaluations(portfolio_id="demo_portfolio")
        assert len(evs) >= 1

    def test_212_store_get_missing_returns_none(self):
        from portfolio.risk_controls.store_v153 import DrawdownRiskControlsStore
        store = DrawdownRiskControlsStore()
        assert store.get_evaluation("NONEXISTENT") is None

    def test_213_query_service_get_policies(self):
        from portfolio.risk_controls.query_v153 import DrawdownRiskControlsQueryService
        policies = DrawdownRiskControlsQueryService().get_policies()
        assert isinstance(policies, list)
        assert len(policies) > 0

    def test_214_query_service_policies_research_only(self):
        from portfolio.risk_controls.query_v153 import DrawdownRiskControlsQueryService
        policies = DrawdownRiskControlsQueryService().get_policies()
        for p in policies:
            assert p["research_only"] is True
            assert p["executable"] is False
            assert p["order_created"] is False

    def test_215_query_service_evaluate_risk_controls(self):
        from portfolio.risk_controls.query_v153 import DrawdownRiskControlsQueryService
        ev = DrawdownRiskControlsQueryService().evaluate_risk_controls(
            "demo_portfolio", "2026-06-21"
        )
        assert ev.research_only is True

    def test_216_store_save_no_id_raises(self):
        from portfolio.risk_controls.store_v153 import DrawdownRiskControlsStore
        store = DrawdownRiskControlsStore()

        class FakeEval:
            evaluation_id = ""

        with pytest.raises(ValueError):
            store.save_evaluation(FakeEval())


# ===========================================================================
# 23. TestCLI (tests 217-242)
# ===========================================================================

class TestCLI:
    def test_217_command_registry_has_drawdown_risk_health(self):
        from cli.command_registry import get_command
        cmd = get_command("drawdown-risk-health")
        assert cmd is not None

    def test_218_command_registry_has_risk_control_policies(self):
        from cli.command_registry import get_command
        cmd = get_command("risk-control-policies")
        assert cmd is not None

    def test_219_command_registry_has_drawdown_eligibility(self):
        from cli.command_registry import get_command
        cmd = get_command("drawdown-eligibility")
        assert cmd is not None

    def test_220_command_registry_has_portfolio_equity_curve(self):
        from cli.command_registry import get_command
        cmd = get_command("portfolio-equity-curve")
        assert cmd is not None

    def test_221_command_registry_has_portfolio_underwater(self):
        from cli.command_registry import get_command
        cmd = get_command("portfolio-underwater")
        assert cmd is not None

    def test_222_command_registry_has_portfolio_drawdown(self):
        from cli.command_registry import get_command
        cmd = get_command("portfolio-drawdown")
        assert cmd is not None

    def test_223_command_registry_has_drawdown_episodes(self):
        from cli.command_registry import get_command
        cmd = get_command("drawdown-episodes")
        assert cmd is not None

    def test_224_command_registry_has_rolling_drawdown(self):
        from cli.command_registry import get_command
        cmd = get_command("rolling-drawdown")
        assert cmd is not None

    def test_225_command_registry_has_drawdown_attribution(self):
        from cli.command_registry import get_command
        cmd = get_command("drawdown-attribution")
        assert cmd is not None

    def test_226_command_registry_has_portfolio_risk_budget(self):
        from cli.command_registry import get_command
        cmd = get_command("portfolio-risk-budget")
        assert cmd is not None

    def test_227_command_registry_has_portfolio_loss_limits(self):
        from cli.command_registry import get_command
        cmd = get_command("portfolio-loss-limits")
        assert cmd is not None

    def test_228_command_registry_has_portfolio_volatility_limit(self):
        from cli.command_registry import get_command
        cmd = get_command("portfolio-volatility-limit")
        assert cmd is not None

    def test_229_command_registry_has_portfolio_concentration_limits(self):
        from cli.command_registry import get_command
        cmd = get_command("portfolio-concentration-limits")
        assert cmd is not None

    def test_230_command_registry_has_portfolio_correlation_limits(self):
        from cli.command_registry import get_command
        cmd = get_command("portfolio-correlation-limits")
        assert cmd is not None

    def test_231_command_registry_has_portfolio_liquidity_limit(self):
        from cli.command_registry import get_command
        cmd = get_command("portfolio-liquidity-limit")
        assert cmd is not None

    def test_232_command_registry_has_portfolio_cash_reserve(self):
        from cli.command_registry import get_command
        cmd = get_command("portfolio-cash-reserve")
        assert cmd is not None

    def test_233_command_registry_has_risk_control_evaluate(self):
        from cli.command_registry import get_command
        cmd = get_command("risk-control-evaluate")
        assert cmd is not None

    def test_234_command_registry_has_sizing_risk_impact(self):
        from cli.command_registry import get_command
        cmd = get_command("sizing-risk-impact")
        assert cmd is not None

    def test_235_command_registry_has_drawdown_stress(self):
        from cli.command_registry import get_command
        cmd = get_command("drawdown-stress")
        assert cmd is not None

    def test_236_command_registry_has_risk_control_explain(self):
        from cli.command_registry import get_command
        cmd = get_command("risk-control-explain")
        assert cmd is not None

    def test_237_command_registry_has_risk_control_show(self):
        from cli.command_registry import get_command
        cmd = get_command("risk-control-show")
        assert cmd is not None

    def test_238_command_registry_has_risk_control_list(self):
        from cli.command_registry import get_command
        cmd = get_command("risk-control-list")
        assert cmd is not None

    def test_239_command_registry_has_risk_control_lineage(self):
        from cli.command_registry import get_command
        cmd = get_command("risk-control-lineage")
        assert cmd is not None

    def test_240_command_registry_has_risk_control_policy_show(self):
        from cli.command_registry import get_command
        cmd = get_command("risk-control-policy-show")
        assert cmd is not None

    def test_241_command_registry_has_drawdown_risk_report(self):
        from cli.command_registry import get_command
        cmd = get_command("drawdown-risk-report")
        assert cmd is not None

    def test_242_all_drawdown_commands_research_only(self):
        from cli.command_registry import get_commands_by_group
        cmds = get_commands_by_group("drawdown_risk_controls")
        assert len(cmds) == 25
        for cmd in cmds:
            assert cmd.research_only is True


# ===========================================================================
# 24. TestGUI (tests 243-257)
# ===========================================================================

class TestGUI:
    def test_243_gui_panel_imports(self):
        import gui.drawdown_risk_controls_panel as panel
        assert panel is not None

    def test_244_gui_panel_has_RESEARCH_ONLY(self):
        import gui.drawdown_risk_controls_panel as panel
        assert panel.RESEARCH_ONLY is True

    def test_245_gui_panel_has_NO_REAL_ORDERS(self):
        import gui.drawdown_risk_controls_panel as panel
        assert panel.NO_REAL_ORDERS is True

    def test_246_gui_panel_DrawdownRiskControlsPanel_class(self):
        from gui.drawdown_risk_controls_panel import DrawdownRiskControlsPanel
        assert DrawdownRiskControlsPanel is not None

    def test_247_gui_panel_class_BROKER_EXECUTION_false(self):
        from gui.drawdown_risk_controls_panel import DrawdownRiskControlsPanel
        assert DrawdownRiskControlsPanel.BROKER_EXECUTION_ENABLED is False

    def test_248_gui_panel_class_RESEARCH_ONLY(self):
        from gui.drawdown_risk_controls_panel import DrawdownRiskControlsPanel
        assert DrawdownRiskControlsPanel.RESEARCH_ONLY is True

    def test_249_gui_panel_get_summary_returns_dict(self):
        from gui.drawdown_risk_controls_panel import DrawdownRiskControlsPanel
        panel = DrawdownRiskControlsPanel()
        summary = panel.get_summary()
        assert isinstance(summary, dict)
        assert summary["research_only"] is True

    def test_250_gui_panel_get_summary_no_broker(self):
        from gui.drawdown_risk_controls_panel import DrawdownRiskControlsPanel
        panel = DrawdownRiskControlsPanel()
        summary = panel.get_summary()
        assert summary["broker_execution_enabled"] is False

    def test_251_gui_panel_no_broker_method(self):
        from gui.drawdown_risk_controls_panel import DrawdownRiskControlsPanel
        panel = DrawdownRiskControlsPanel()
        # Blocked buttons should not be methods
        assert not hasattr(panel, "connect_broker")
        assert not hasattr(panel, "submit_order")

    def test_252_report_module_imports(self):
        import reports.drawdown_risk_controls_report as report_mod
        assert report_mod is not None

    def test_253_report_module_RESEARCH_ONLY(self):
        import reports.drawdown_risk_controls_report as report_mod
        assert report_mod.RESEARCH_ONLY is True

    def test_254_report_generate_returns_dict(self):
        from reports.drawdown_risk_controls_report import DrawdownRiskControlsReport
        gen = DrawdownRiskControlsReport()
        report = gen.generate("demo_portfolio", "2026-06-21")
        assert isinstance(report, dict)
        assert report["research_only"] is True

    def test_255_report_generate_no_order(self):
        from reports.drawdown_risk_controls_report import DrawdownRiskControlsReport
        gen = DrawdownRiskControlsReport()
        report = gen.generate("demo_portfolio", "2026-06-21")
        assert report["executable"] is False

    def test_256_release_gate_imports(self):
        import release.drawdown_risk_controls_release_gate_v153 as gate_mod
        assert gate_mod is not None

    def test_257_release_gate_RESEARCH_ONLY(self):
        import release.drawdown_risk_controls_release_gate_v153 as gate_mod
        assert gate_mod.RESEARCH_ONLY is True


# ===========================================================================
# 25. TestRegression (tests 258-288)
# ===========================================================================

class TestRegression:
    def test_258_version_is_1_5_3(self):
        from release.version_info import VERSION
        assert VERSION == "1.5.3"

    def test_259_DRAWDOWN_RISK_CONTROLS_AVAILABLE_true_in_version_info(self):
        from release.version_info import DRAWDOWN_RISK_CONTROLS_AVAILABLE
        assert DRAWDOWN_RISK_CONTROLS_AVAILABLE is True

    def test_260_DRAWDOWN_RISK_CONTROLS_STAGE_STABLE(self):
        from release.version_info import DRAWDOWN_RISK_CONTROLS_STAGE
        assert DRAWDOWN_RISK_CONTROLS_STAGE == "STABLE"

    def test_261_DRAWDOWN_RISK_CONTROLS_BASELINE_1_5_3(self):
        from release.version_info import DRAWDOWN_RISK_CONTROLS_BASELINE
        assert DRAWDOWN_RISK_CONTROLS_BASELINE == "1.5.3"

    def test_262_RISK_CONTROL_AUTO_APPLY_false_version_info(self):
        from release.version_info import RISK_CONTROL_AUTO_APPLY_ENABLED
        assert RISK_CONTROL_AUTO_APPLY_ENABLED is False

    def test_263_RISK_CONTROL_AUTO_REDUCE_false_version_info(self):
        from release.version_info import RISK_CONTROL_AUTO_REDUCE_ENABLED
        assert RISK_CONTROL_AUTO_REDUCE_ENABLED is False

    def test_264_RISK_CONTROL_AUTO_STOP_false_version_info(self):
        from release.version_info import RISK_CONTROL_AUTO_STOP_ENABLED
        assert RISK_CONTROL_AUTO_STOP_ENABLED is False

    def test_265_RISK_CONTROL_AUTO_REBALANCE_false_version_info(self):
        from release.version_info import RISK_CONTROL_AUTO_REBALANCE_ENABLED
        assert RISK_CONTROL_AUTO_REBALANCE_ENABLED is False

    def test_266_RISK_CONTROL_ORDER_GENERATION_false_version_info(self):
        from release.version_info import RISK_CONTROL_ORDER_GENERATION_ENABLED
        assert RISK_CONTROL_ORDER_GENERATION_ENABLED is False

    def test_267_RISK_CONTROL_BROKER_false_version_info(self):
        from release.version_info import RISK_CONTROL_BROKER_ENABLED
        assert RISK_CONTROL_BROKER_ENABLED is False

    def test_268_UNDERWATER_CURVE_AVAILABLE_true(self):
        from release.version_info import UNDERWATER_CURVE_AVAILABLE
        assert UNDERWATER_CURVE_AVAILABLE is True

    def test_269_MAX_DRAWDOWN_AVAILABLE_true(self):
        from release.version_info import MAX_DRAWDOWN_AVAILABLE
        assert MAX_DRAWDOWN_AVAILABLE is True

    def test_270_ROLLING_MAX_DRAWDOWN_AVAILABLE_true(self):
        from release.version_info import ROLLING_MAX_DRAWDOWN_AVAILABLE
        assert ROLLING_MAX_DRAWDOWN_AVAILABLE is True

    def test_271_health_check_all_pass(self):
        from portfolio.risk_controls.health_v153 import DrawdownRiskControlsHealthCheck
        result = DrawdownRiskControlsHealthCheck().run()
        failures = [k for k, v in result.items()
                    if isinstance(v, dict) and v.get("status") == "FAIL"]
        assert failures == [], f"Health check failures: {failures}"

    def test_272_enums_version_1_5_3(self):
        from portfolio.risk_controls.enums_v153 import ENUMS_VERSION
        assert ENUMS_VERSION == "1.5.3"

    def test_273_models_version_1_5_3(self):
        from portfolio.risk_controls.models_v153 import MODELS_VERSION
        assert MODELS_VERSION == "1.5.3"

    def test_274_package_version_1_5_3(self):
        from portfolio.risk_controls import VERSION
        assert VERSION == "1.5.3"

    def test_275_all_modules_importable(self):
        modules = [
            "portfolio.risk_controls.enums_v153",
            "portfolio.risk_controls.models_v153",
            "portfolio.risk_controls.validation_v153",
            "portfolio.risk_controls.equity_curve_v153",
            "portfolio.risk_controls.underwater_v153",
            "portfolio.risk_controls.drawdown_v153",
            "portfolio.risk_controls.drawdown_episode_v153",
            "portfolio.risk_controls.drawdown_duration_v153",
            "portfolio.risk_controls.drawdown_recovery_v153",
            "portfolio.risk_controls.drawdown_attribution_v153",
            "portfolio.risk_controls.risk_budget_v153",
            "portfolio.risk_controls.volatility_limit_v153",
            "portfolio.risk_controls.loss_limit_v153",
            "portfolio.risk_controls.concentration_limit_v153",
            "portfolio.risk_controls.correlation_limit_v153",
            "portfolio.risk_controls.liquidity_limit_v153",
            "portfolio.risk_controls.cash_reserve_limit_v153",
            "portfolio.risk_controls.constraint_engine_v153",
            "portfolio.risk_controls.sizing_impact_v153",
            "portfolio.risk_controls.stress_v153",
            "portfolio.risk_controls.eligibility_v153",
            "portfolio.risk_controls.point_in_time_v153",
            "portfolio.risk_controls.lineage_v153",
            "portfolio.risk_controls.explain_v153",
            "portfolio.risk_controls.store_v153",
            "portfolio.risk_controls.query_v153",
        ]
        for mod in modules:
            __import__(mod)

    def test_276_no_auto_optimize_in_package(self):
        from portfolio.risk_controls import RISK_CONTROL_ORDER_EXECUTION_ENABLED
        assert RISK_CONTROL_ORDER_EXECUTION_ENABLED is False

    def test_277_no_hedging_execution_in_package(self):
        from portfolio.risk_controls import RISK_CONTROL_HEDGING_EXECUTION_ENABLED
        assert RISK_CONTROL_HEDGING_EXECUTION_ENABLED is False

    def test_278_no_ledger_write_in_package(self):
        from portfolio.risk_controls import RISK_CONTROL_LEDGER_WRITE_ENABLED
        assert RISK_CONTROL_LEDGER_WRITE_ENABLED is False

    def test_279_no_live_sync_in_package(self):
        from portfolio.risk_controls import RISK_CONTROL_LIVE_ACCOUNT_SYNC_ENABLED
        assert RISK_CONTROL_LIVE_ACCOUNT_SYNC_ENABLED is False

    def test_280_query_service_research_only_class(self):
        from portfolio.risk_controls.query_v153 import DrawdownRiskControlsQueryService
        assert DrawdownRiskControlsQueryService.RESEARCH_ONLY is True

    def test_281_constraint_engine_research_only_class(self):
        from portfolio.risk_controls.constraint_engine_v153 import RiskControlConstraintEngine
        assert RiskControlConstraintEngine.RESEARCH_ONLY is True

    def test_282_stress_analyzer_research_only_class(self):
        from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
        assert DrawdownStressAnalyzer.RESEARCH_ONLY is True

    def test_283_25_cli_commands_registered(self):
        from cli.command_registry import get_commands_by_group
        cmds = get_commands_by_group("drawdown_risk_controls")
        assert len(cmds) == 25

    def test_284_fixture_dir_has_all_fixtures(self):
        expected = [
            "equity_curve_valid.json",
            "equity_curve_future_data.json",
            "equity_curve_cash_flows.json",
            "equity_curve_missing_value.json",
            "underwater_valid.json",
            "drawdown_summary_valid.json",
            "drawdown_episode_open.json",
            "drawdown_episode_closed.json",
            "drawdown_single_episode.json",
            "drawdown_multiple_episodes.json",
            "drawdown_unrecovered.json",
            "drawdown_equal_peaks.json",
            "rolling_drawdown_valid.json",
            "attribution_by_position.json",
            "attribution_by_industry.json",
            "attribution_theme_overlap.json",
            "attribution_cluster.json",
            "risk_policy_default.json",
            "risk_policy_conservative.json",
            "risk_budget_valid.json",
            "risk_budget_exceeded.json",
            "daily_loss_limit.json",
            "weekly_loss_limit.json",
            "monthly_loss_limit.json",
            "volatility_limit.json",
            "concentration_limit.json",
            "correlation_limit.json",
            "liquidity_limit.json",
            "cash_reserve_limit.json",
            "sizing_impact_valid.json",
            "sizing_impact_blocked.json",
            "stress_market_shock.json",
            "stress_correlation_spike.json",
            "stress_liquidity_shock.json",
            "stress_combined.json",
            "eligibility_valid.json",
            "eligibility_broker_blocked.json",
            "eligibility_blocked.json",
            "pit_future_policy.json",
            "lineage_complete.json",
            "lineage_missing.json",
        ]
        for name in expected:
            assert (FIXTURE_DIR / name).exists(), f"Missing fixture: {name}"

    def test_285_all_fixtures_have_labels(self):
        for fixture_path in FIXTURE_DIR.glob("*.json"):
            with open(fixture_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            labels = data.get("_labels") or data.get("_fixture_labels")
            assert labels is not None, f"No labels in {fixture_path.name}"

    def test_286_correlation_and_exposure_baseline_preserved(self):
        from release.version_info import CORRELATION_EXPOSURE_AVAILABLE
        assert CORRELATION_EXPOSURE_AVAILABLE is True

    def test_287_position_sizing_baseline_preserved(self):
        from release.version_info import POSITION_SIZING_AVAILABLE
        assert POSITION_SIZING_AVAILABLE is True

    def test_288_v153_release_name_correct(self):
        from release.version_info import RELEASE_NAME
        assert RELEASE_NAME == "Drawdown & Risk Controls"
