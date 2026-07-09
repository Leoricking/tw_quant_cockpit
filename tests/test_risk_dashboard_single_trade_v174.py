"""
tests/test_risk_dashboard_single_trade_v174.py
Tests for single trade risk monitor v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import RiskStatus, RiskBlockReason
from paper_trading.small_capital_strategy.single_trade_risk_monitor_v174 import (
    evaluate_single_trade_risk,
    get_single_trade_risk_thresholds,
    MAX_SINGLE_TRADE_LOSS_DEFAULT,
    MAX_SINGLE_TRADE_LOSS_WARNING,
    MAX_SINGLE_TRADE_RISK_PCT,
)


def _inp(**kw):
    defaults = {
        "capital_twd": 300_000.0,
        "position_size_amount": 50_000.0,
        "stop_loss_pct": 0.05,
        "has_stop_loss": True,
    }
    defaults.update(kw)
    return SmallAccountRiskInput(**defaults)


class TestThresholds:
    def test_default_loss_3000(self):
        assert MAX_SINGLE_TRADE_LOSS_DEFAULT == 3000.0

    def test_warning_loss_4500(self):
        assert MAX_SINGLE_TRADE_LOSS_WARNING == 4500.0

    def test_max_risk_pct_1_5(self):
        assert MAX_SINGLE_TRADE_RISK_PCT == 1.5

    def test_thresholds_dict(self):
        t = get_single_trade_risk_thresholds()
        assert t["max_loss_default_twd"] == 3000.0
        assert t["max_loss_warning_twd"] == 4500.0
        assert t["max_risk_pct"] == 1.5

    def test_thresholds_paper_only(self):
        assert get_single_trade_risk_thresholds()["paper_only"] is True


class TestPassCases:
    def test_loss_exactly_3000_pass(self):
        # 60000 * 0.05 = 3000
        result = evaluate_single_trade_risk(_inp(position_size_amount=60_000.0, stop_loss_pct=0.05))
        assert result.status == RiskStatus.PASS

    def test_loss_below_3000_pass(self):
        result = evaluate_single_trade_risk(_inp(position_size_amount=40_000.0, stop_loss_pct=0.05))
        assert result.status == RiskStatus.PASS

    def test_loss_2400_pass(self):
        result = evaluate_single_trade_risk(_inp(position_size_amount=48_000.0, stop_loss_pct=0.05))
        assert result.status == RiskStatus.PASS

    def test_result_paper_only(self):
        result = evaluate_single_trade_risk(_inp())
        assert result.paper_only is True

    def test_result_no_real_orders(self):
        result = evaluate_single_trade_risk(_inp())
        assert result.no_real_orders is True

    def test_result_not_investment_advice(self):
        result = evaluate_single_trade_risk(_inp())
        assert result.not_investment_advice is True

    def test_pass_has_stop_loss_true(self):
        result = evaluate_single_trade_risk(_inp())
        assert result.has_stop_loss is True


class TestWarningCases:
    def test_loss_4000_warning(self):
        # 80000 * 0.05 = 4000
        result = evaluate_single_trade_risk(_inp(position_size_amount=80_000.0, stop_loss_pct=0.05))
        assert result.status == RiskStatus.WARNING

    def test_loss_4499_warning(self):
        result = evaluate_single_trade_risk(_inp(position_size_amount=89_980.0, stop_loss_pct=0.05))
        assert result.status == RiskStatus.WARNING


class TestBlockedCases:
    def test_no_stop_loss_blocked(self):
        result = evaluate_single_trade_risk(_inp(has_stop_loss=False, stop_loss_pct=0.0))
        assert result.status == RiskStatus.BLOCKED

    def test_stop_loss_pct_zero_blocked(self):
        result = evaluate_single_trade_risk(_inp(stop_loss_pct=0.0))
        assert result.status == RiskStatus.BLOCKED

    def test_loss_5000_blocked(self):
        # 100000 * 0.05 = 5000
        result = evaluate_single_trade_risk(_inp(position_size_amount=100_000.0, stop_loss_pct=0.05))
        assert result.status == RiskStatus.BLOCKED

    def test_risk_pct_1_6_blocked(self):
        # 100000 * 0.048 = 4800 (>4500) and 4800/300000 = 1.6% (>1.5%)
        result = evaluate_single_trade_risk(_inp(position_size_amount=100_000.0, stop_loss_pct=0.048))
        assert result.status == RiskStatus.BLOCKED

    def test_real_order_blocked(self):
        result = evaluate_single_trade_risk(_inp(real_order_requested=True))
        assert result.status == RiskStatus.BLOCKED
        assert RiskBlockReason.REAL_ORDER_REQUESTED in result.block_reasons

    def test_broker_blocked(self):
        result = evaluate_single_trade_risk(_inp(broker_requested=True))
        assert result.status == RiskStatus.BLOCKED
        assert RiskBlockReason.BROKER_REQUESTED in result.block_reasons

    def test_margin_blocked(self):
        result = evaluate_single_trade_risk(_inp(margin_requested=True))
        assert result.status == RiskStatus.BLOCKED
        assert RiskBlockReason.MARGIN_NOT_ALLOWED in result.block_reasons


class TestResultFields:
    def test_loss_amount_computed(self):
        result = evaluate_single_trade_risk(_inp(position_size_amount=60_000.0, stop_loss_pct=0.05))
        assert abs(result.single_trade_loss_amount - 3000.0) < 0.01

    def test_risk_pct_computed(self):
        result = evaluate_single_trade_risk(_inp(position_size_amount=60_000.0, stop_loss_pct=0.05))
        assert abs(result.risk_pct - 1.0) < 0.01

    def test_detail_not_empty(self):
        result = evaluate_single_trade_risk(_inp())
        assert isinstance(result.detail, str) and len(result.detail) > 0

    def test_block_reasons_list(self):
        result = evaluate_single_trade_risk(_inp())
        assert isinstance(result.block_reasons, list)

    def test_no_stop_loss_reason(self):
        result = evaluate_single_trade_risk(_inp(has_stop_loss=False, stop_loss_pct=0.0))
        assert RiskBlockReason.NO_STOP_LOSS in result.block_reasons
