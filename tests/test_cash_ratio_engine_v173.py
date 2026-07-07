"""
tests/test_cash_ratio_engine_v173.py
Tests for Market Regime Position Control cash_ratio_engine_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
from paper_trading.small_capital_strategy.cash_ratio_engine_v173 import (
    build_cash_ratio_plan, get_all_regime_allocations,
)


class TestBuildCashRatioPlan:
    def test_bull_total_100(self):
        plan = build_cash_ratio_plan(MarketRegime.BULL)
        assert plan.total_pct == 100

    def test_range_total_100(self):
        plan = build_cash_ratio_plan(MarketRegime.RANGE)
        assert plan.total_pct == 100

    def test_bear_total_100(self):
        plan = build_cash_ratio_plan(MarketRegime.BEAR)
        assert plan.total_pct == 100

    def test_risk_off_total_100(self):
        plan = build_cash_ratio_plan(MarketRegime.RISK_OFF)
        assert plan.total_pct == 100

    def test_unknown_total_100(self):
        plan = build_cash_ratio_plan(MarketRegime.UNKNOWN)
        assert plan.total_pct == 100

    def test_bull_cash_5pct(self):
        plan = build_cash_ratio_plan(MarketRegime.BULL)
        assert plan.cash_pct == 5

    def test_range_cash_25pct(self):
        plan = build_cash_ratio_plan(MarketRegime.RANGE)
        assert plan.cash_pct == 25

    def test_bear_cash_50pct(self):
        plan = build_cash_ratio_plan(MarketRegime.BEAR)
        assert plan.cash_pct == 50

    def test_risk_off_cash_60pct(self):
        plan = build_cash_ratio_plan(MarketRegime.RISK_OFF)
        assert plan.cash_pct == 60

    def test_unknown_cash_40pct(self):
        plan = build_cash_ratio_plan(MarketRegime.UNKNOWN)
        assert plan.cash_pct == 40

    def test_bull_invested_95(self):
        plan = build_cash_ratio_plan(MarketRegime.BULL)
        assert plan.max_invested_pct == 95

    def test_bear_training_zero(self):
        plan = build_cash_ratio_plan(MarketRegime.BEAR)
        assert plan.short_term_training_pct == 0

    def test_risk_off_training_zero(self):
        plan = build_cash_ratio_plan(MarketRegime.RISK_OFF)
        assert plan.short_term_training_pct == 0

    def test_unknown_training_zero(self):
        plan = build_cash_ratio_plan(MarketRegime.UNKNOWN)
        assert plan.short_term_training_pct == 0

    def test_bull_training_5(self):
        plan = build_cash_ratio_plan(MarketRegime.BULL)
        assert plan.short_term_training_pct == 5

    def test_allocation_valid_bull(self):
        plan = build_cash_ratio_plan(MarketRegime.BULL)
        assert plan.allocation_valid is True

    def test_all_regimes_valid(self):
        for regime in MarketRegime:
            plan = build_cash_ratio_plan(regime)
            assert plan.allocation_valid is True

    def test_paper_only(self):
        plan = build_cash_ratio_plan(MarketRegime.BULL)
        assert plan.paper_only is True

    def test_no_real_orders(self):
        plan = build_cash_ratio_plan(MarketRegime.BULL)
        assert plan.no_real_orders is True

    def test_regime_stored(self):
        plan = build_cash_ratio_plan(MarketRegime.RANGE)
        assert plan.regime == MarketRegime.RANGE

    def test_bull_core_40pct(self):
        plan = build_cash_ratio_plan(MarketRegime.BULL)
        assert plan.core_pct == 40

    def test_bull_main_theme_35pct(self):
        plan = build_cash_ratio_plan(MarketRegime.BULL)
        assert plan.main_theme_swing_pct == 35


class TestGetAllRegimeAllocations:
    def test_returns_dict(self):
        allocs = get_all_regime_allocations()
        assert isinstance(allocs, dict)

    def test_has_bull_key(self):
        allocs = get_all_regime_allocations()
        assert "BULL" in allocs

    def test_has_five_regimes(self):
        allocs = get_all_regime_allocations()
        assert len(allocs) == 5
