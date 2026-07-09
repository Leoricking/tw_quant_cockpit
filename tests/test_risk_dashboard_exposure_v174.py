"""
tests/test_risk_dashboard_exposure_v174.py
Tests for portfolio exposure monitor v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import RiskStatus, RiskBlockReason
from paper_trading.small_capital_strategy.portfolio_exposure_monitor_v174 import (
    evaluate_portfolio_exposure, get_all_regime_exposure_limits, get_regime_limits,
)


def _inp(regime="BULL", invested=30.0, cash=70.0, **kw):
    return SmallAccountRiskInput(
        market_regime=regime,
        total_invested_pct=invested,
        cash_pct=cash,
        **kw,
    )


class TestRegimeLimits:
    def test_bull_max_95(self):
        assert get_regime_limits("BULL")["max_invested_pct"] == 95

    def test_bull_min_cash_5(self):
        assert get_regime_limits("BULL")["min_cash_pct"] == 5

    def test_range_max_75(self):
        assert get_regime_limits("RANGE")["max_invested_pct"] == 75

    def test_range_min_cash_25(self):
        assert get_regime_limits("RANGE")["min_cash_pct"] == 25

    def test_bear_max_50(self):
        assert get_regime_limits("BEAR")["max_invested_pct"] == 50

    def test_bear_min_cash_50(self):
        assert get_regime_limits("BEAR")["min_cash_pct"] == 50

    def test_risk_off_max_40(self):
        assert get_regime_limits("RISK_OFF")["max_invested_pct"] == 40

    def test_risk_off_min_cash_60(self):
        assert get_regime_limits("RISK_OFF")["min_cash_pct"] == 60

    def test_unknown_max_60(self):
        assert get_regime_limits("UNKNOWN")["max_invested_pct"] == 60

    def test_all_regimes_in_dict(self):
        limits = get_all_regime_exposure_limits()
        for r in ["BULL", "RANGE", "BEAR", "RISK_OFF", "UNKNOWN"]:
            assert r in limits


class TestBullRegime:
    def test_bull_30pct_pass(self):
        assert evaluate_portfolio_exposure(_inp("BULL", 30.0, 70.0)).status == RiskStatus.PASS

    def test_bull_95pct_pass(self):
        assert evaluate_portfolio_exposure(_inp("BULL", 95.0, 5.0)).status == RiskStatus.PASS

    def test_bull_96pct_blocked(self):
        assert evaluate_portfolio_exposure(_inp("BULL", 96.0, 4.0)).status == RiskStatus.BLOCKED

    def test_bull_low_cash_blocked(self):
        assert evaluate_portfolio_exposure(_inp("BULL", 98.0, 2.0)).status == RiskStatus.BLOCKED


class TestRangeRegime:
    def test_range_75pct_pass(self):
        assert evaluate_portfolio_exposure(_inp("RANGE", 75.0, 25.0)).status == RiskStatus.PASS

    def test_range_76pct_blocked(self):
        assert evaluate_portfolio_exposure(_inp("RANGE", 76.0, 24.0)).status == RiskStatus.BLOCKED


class TestBearRegime:
    def test_bear_50pct_pass(self):
        assert evaluate_portfolio_exposure(_inp("BEAR", 50.0, 50.0)).status == RiskStatus.PASS

    def test_bear_51pct_blocked(self):
        assert evaluate_portfolio_exposure(_inp("BEAR", 51.0, 49.0)).status == RiskStatus.BLOCKED


class TestRiskOffRegime:
    def test_risk_off_40pct_pass(self):
        assert evaluate_portfolio_exposure(_inp("RISK_OFF", 40.0, 60.0)).status == RiskStatus.PASS

    def test_risk_off_41pct_blocked(self):
        assert evaluate_portfolio_exposure(_inp("RISK_OFF", 41.0, 59.0)).status == RiskStatus.BLOCKED

    def test_risk_off_low_cash_blocked(self):
        assert evaluate_portfolio_exposure(_inp("RISK_OFF", 80.0, 20.0)).status == RiskStatus.BLOCKED


class TestUnknownRegime:
    def test_unknown_60pct_pass(self):
        assert evaluate_portfolio_exposure(_inp("UNKNOWN", 60.0, 40.0)).status == RiskStatus.PASS

    def test_unknown_61pct_blocked(self):
        assert evaluate_portfolio_exposure(_inp("UNKNOWN", 61.0, 39.0)).status == RiskStatus.BLOCKED


class TestSafetyBlocks:
    def test_real_order_blocked(self):
        r = evaluate_portfolio_exposure(_inp(real_order_requested=True))
        assert r.status == RiskStatus.BLOCKED

    def test_broker_blocked(self):
        r = evaluate_portfolio_exposure(_inp(broker_requested=True))
        assert r.status == RiskStatus.BLOCKED


class TestResultFields:
    def test_paper_only(self):
        assert evaluate_portfolio_exposure(_inp()).paper_only is True

    def test_block_reasons_list(self):
        r = evaluate_portfolio_exposure(_inp())
        assert isinstance(r.block_reasons, list)

    def test_regime_in_result(self):
        r = evaluate_portfolio_exposure(_inp("BULL"))
        assert r.market_regime == "BULL"
