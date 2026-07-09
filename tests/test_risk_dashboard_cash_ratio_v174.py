"""
tests/test_risk_dashboard_cash_ratio_v174.py
Tests for cash ratio risk monitor v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import RiskStatus, RiskBlockReason
from paper_trading.small_capital_strategy.cash_ratio_risk_monitor_v174 import (
    evaluate_cash_ratio, get_cash_ratio_thresholds,
)


def _inp(**kw):
    return SmallAccountRiskInput(**kw)


class TestThresholds:
    def test_bull_min_cash_5(self):
        t = get_cash_ratio_thresholds()
        assert t["BULL"]["min_cash_pct"] == 5

    def test_range_min_cash_25(self):
        t = get_cash_ratio_thresholds()
        assert t["RANGE"]["min_cash_pct"] == 25

    def test_bear_min_cash_50(self):
        t = get_cash_ratio_thresholds()
        assert t["BEAR"]["min_cash_pct"] == 50

    def test_risk_off_min_cash_60(self):
        t = get_cash_ratio_thresholds()
        assert t["RISK_OFF"]["min_cash_pct"] == 60

    def test_unknown_min_cash_40(self):
        t = get_cash_ratio_thresholds()
        assert t["UNKNOWN"]["min_cash_pct"] == 40

    def test_thresholds_paper_only(self):
        assert get_cash_ratio_thresholds()["paper_only"] is True


class TestPassCases:
    def test_bull_cash_50_pass(self):
        r = evaluate_cash_ratio(_inp(market_regime="BULL", cash_pct=50.0))
        assert r.status == RiskStatus.PASS

    def test_bull_cash_10_pass(self):
        # min_cash=5, warning tier is [5,5.5), pass is >=5.5
        r = evaluate_cash_ratio(_inp(market_regime="BULL", cash_pct=10.0))
        assert r.status == RiskStatus.PASS

    def test_range_cash_30_pass(self):
        # min_cash=25, warning tier is [25,27.5), pass is >=27.5
        r = evaluate_cash_ratio(_inp(market_regime="RANGE", cash_pct=30.0))
        assert r.status == RiskStatus.PASS

    def test_bear_cash_60_pass(self):
        # min_cash=50, warning tier is [50,55), pass is >=55
        r = evaluate_cash_ratio(_inp(market_regime="BEAR", cash_pct=60.0))
        assert r.status == RiskStatus.PASS

    def test_risk_off_cash_70_pass(self):
        # min_cash=60, warning tier is [60,66), pass is >=66
        r = evaluate_cash_ratio(_inp(market_regime="RISK_OFF", cash_pct=70.0))
        assert r.status == RiskStatus.PASS

    def test_unknown_cash_50_pass(self):
        # min_cash=40, warning tier is [40,44), pass is >=44
        r = evaluate_cash_ratio(_inp(market_regime="UNKNOWN", cash_pct=50.0))
        assert r.status == RiskStatus.PASS


class TestBlockedCases:
    def test_bull_cash_1_blocked(self):
        r = evaluate_cash_ratio(_inp(market_regime="BULL", cash_pct=1.0))
        assert r.status == RiskStatus.BLOCKED

    def test_range_cash_10_blocked(self):
        r = evaluate_cash_ratio(_inp(market_regime="RANGE", cash_pct=10.0))
        assert r.status == RiskStatus.BLOCKED

    def test_risk_off_cash_20_blocked(self):
        r = evaluate_cash_ratio(_inp(market_regime="RISK_OFF", cash_pct=20.0))
        assert r.status == RiskStatus.BLOCKED

    def test_blocked_has_reason(self):
        r = evaluate_cash_ratio(_inp(market_regime="RISK_OFF", cash_pct=20.0))
        assert RiskBlockReason.CASH_RATIO_TOO_LOW in r.block_reasons

    def test_bear_cash_10_blocked(self):
        r = evaluate_cash_ratio(_inp(market_regime="BEAR", cash_pct=10.0))
        assert r.status == RiskStatus.BLOCKED


class TestWarningCases:
    def test_range_near_min_warning(self):
        r = evaluate_cash_ratio(_inp(market_regime="RANGE", cash_pct=26.0))
        assert r.status == RiskStatus.WARNING


class TestResultFields:
    def test_paper_only(self):
        assert evaluate_cash_ratio(_inp(market_regime="BULL", cash_pct=50.0)).paper_only is True

    def test_no_real_orders(self):
        assert evaluate_cash_ratio(_inp()).no_real_orders is True

    def test_not_investment_advice(self):
        assert evaluate_cash_ratio(_inp()).not_investment_advice is True

    def test_cash_pct_stored(self):
        r = evaluate_cash_ratio(_inp(market_regime="BULL", cash_pct=30.0))
        assert r.cash_pct == 30.0

    def test_min_cash_pct_stored(self):
        r = evaluate_cash_ratio(_inp(market_regime="BULL", cash_pct=30.0))
        assert r.min_cash_pct == 5

    def test_market_regime_stored(self):
        r = evaluate_cash_ratio(_inp(market_regime="BEAR", cash_pct=55.0))
        assert r.market_regime == "BEAR"

    def test_detail_not_empty(self):
        r = evaluate_cash_ratio(_inp(market_regime="BULL", cash_pct=30.0))
        assert len(r.detail) > 0

    def test_block_reasons_empty_when_pass(self):
        r = evaluate_cash_ratio(_inp(market_regime="BULL", cash_pct=50.0))
        assert r.block_reasons == []
