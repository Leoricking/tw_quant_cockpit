"""
tests/test_risk_dashboard_models_v174.py
Tests for Small Account Risk Dashboard models v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskInput,
    SingleTradeRiskResult,
    PortfolioExposureResult,
    DrawdownRiskResult,
    LosingStreakRiskResult,
    CashRatioRiskResult,
    ConcentrationRiskResult,
    ThemeExposureRiskResult,
    PositionCountRiskResult,
    StopLossCoverageResult,
    RiskBudgetUsageResult,
    SmallAccountRiskDashboard,
    RiskDashboardScorecard,
    RiskDashboardReport,
    RiskDashboardHealthSummary,
)

_SCHEMA = "174"


class TestSmallAccountRiskInput:
    def test_default_capital(self):
        assert SmallAccountRiskInput().capital_twd == 300_000.0

    def test_paper_only_true(self):
        assert SmallAccountRiskInput().paper_only is True

    def test_research_only_true(self):
        assert SmallAccountRiskInput().research_only is True

    def test_no_real_orders_true(self):
        assert SmallAccountRiskInput().no_real_orders is True

    def test_not_investment_advice_true(self):
        assert SmallAccountRiskInput().not_investment_advice is True

    def test_schema_version(self):
        assert SmallAccountRiskInput().schema_version == _SCHEMA

    def test_created_at_not_empty(self):
        assert SmallAccountRiskInput().created_at != ""

    def test_default_real_order_false(self):
        assert SmallAccountRiskInput().real_order_requested is False

    def test_default_broker_false(self):
        assert SmallAccountRiskInput().broker_requested is False

    def test_default_margin_false(self):
        assert SmallAccountRiskInput().margin_requested is False


class TestSingleTradeRiskResult:
    def test_paper_only(self):
        assert SingleTradeRiskResult().paper_only is True

    def test_no_real_orders(self):
        assert SingleTradeRiskResult().no_real_orders is True

    def test_schema_version(self):
        assert SingleTradeRiskResult().schema_version == _SCHEMA

    def test_default_has_stop_loss_false(self):
        assert SingleTradeRiskResult().has_stop_loss is False


class TestPortfolioExposureResult:
    def test_paper_only(self):
        assert PortfolioExposureResult().paper_only is True

    def test_no_real_orders(self):
        assert PortfolioExposureResult().no_real_orders is True

    def test_schema_version(self):
        assert PortfolioExposureResult().schema_version == _SCHEMA


class TestDrawdownRiskResult:
    def test_paper_only(self):
        assert DrawdownRiskResult().paper_only is True

    def test_default_drawdown_zero(self):
        assert DrawdownRiskResult().drawdown_pct == 0.0

    def test_schema_version(self):
        assert DrawdownRiskResult().schema_version == _SCHEMA


class TestLosingStreakRiskResult:
    def test_paper_only(self):
        assert LosingStreakRiskResult().paper_only is True

    def test_default_streak_zero(self):
        assert LosingStreakRiskResult().losing_streak_count == 0

    def test_schema_version(self):
        assert LosingStreakRiskResult().schema_version == _SCHEMA


class TestCashRatioRiskResult:
    def test_paper_only(self):
        assert CashRatioRiskResult().paper_only is True

    def test_default_cash_100(self):
        assert CashRatioRiskResult().cash_pct == 100.0

    def test_schema_version(self):
        assert CashRatioRiskResult().schema_version == _SCHEMA


class TestConcentrationRiskResult:
    def test_paper_only(self):
        assert ConcentrationRiskResult().paper_only is True

    def test_schema_version(self):
        assert ConcentrationRiskResult().schema_version == _SCHEMA


class TestThemeExposureRiskResult:
    def test_paper_only(self):
        assert ThemeExposureRiskResult().paper_only is True

    def test_schema_version(self):
        assert ThemeExposureRiskResult().schema_version == _SCHEMA


class TestPositionCountRiskResult:
    def test_paper_only(self):
        assert PositionCountRiskResult().paper_only is True

    def test_default_count_zero(self):
        assert PositionCountRiskResult().holdings_count == 0

    def test_default_max_4(self):
        assert PositionCountRiskResult().max_holdings == 4


class TestStopLossCoverageResult:
    def test_paper_only(self):
        assert StopLossCoverageResult().paper_only is True

    def test_default_covered_true(self):
        assert StopLossCoverageResult().all_positions_covered is True

    def test_schema_version(self):
        assert StopLossCoverageResult().schema_version == _SCHEMA


class TestRiskBudgetUsageResult:
    def test_paper_only(self):
        assert RiskBudgetUsageResult().paper_only is True

    def test_default_budget_3000(self):
        assert RiskBudgetUsageResult().max_risk_twd == 3000.0

    def test_schema_version(self):
        assert RiskBudgetUsageResult().schema_version == _SCHEMA


class TestSmallAccountRiskDashboard:
    def test_paper_only(self):
        assert SmallAccountRiskDashboard().paper_only is True

    def test_no_real_orders(self):
        assert SmallAccountRiskDashboard().no_real_orders is True

    def test_not_investment_advice(self):
        assert SmallAccountRiskDashboard().not_investment_advice is True

    def test_schema_version(self):
        assert SmallAccountRiskDashboard().schema_version == _SCHEMA

    def test_default_block_reasons_empty(self):
        assert SmallAccountRiskDashboard().all_block_reasons == []


class TestRiskDashboardScorecard:
    def test_paper_only(self):
        assert RiskDashboardScorecard().paper_only is True

    def test_weights_sum_100(self):
        assert RiskDashboardScorecard().weights_sum == 100

    def test_schema_version(self):
        assert RiskDashboardScorecard().schema_version == _SCHEMA


class TestRiskDashboardHealthSummary:
    def test_paper_only(self):
        assert RiskDashboardHealthSummary().paper_only is True

    def test_default_status_fail(self):
        assert RiskDashboardHealthSummary().status == "FAIL"

    def test_schema_version(self):
        assert RiskDashboardHealthSummary().schema_version == _SCHEMA
