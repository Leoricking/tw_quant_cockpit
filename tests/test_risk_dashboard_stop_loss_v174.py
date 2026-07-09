"""
tests/test_risk_dashboard_stop_loss_v174.py
Tests for stop loss coverage monitor v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import RiskStatus, RiskBlockReason
from paper_trading.small_capital_strategy.stop_loss_coverage_monitor_v174 import evaluate_stop_loss_coverage


def _inp(**kw):
    return SmallAccountRiskInput(**kw)


class TestPassCases:
    def test_has_stop_loss_pass(self):
        r = evaluate_stop_loss_coverage(_inp(has_stop_loss=True, stop_loss_pct=0.05))
        assert r.status == RiskStatus.PASS

    def test_covered_true_when_pass(self):
        r = evaluate_stop_loss_coverage(_inp(has_stop_loss=True, stop_loss_pct=0.05))
        assert r.all_positions_covered is True

    def test_missing_count_zero_when_pass(self):
        r = evaluate_stop_loss_coverage(_inp(has_stop_loss=True, stop_loss_pct=0.05))
        assert r.missing_stop_loss_count == 0

    def test_paper_only(self):
        r = evaluate_stop_loss_coverage(_inp(has_stop_loss=True, stop_loss_pct=0.05))
        assert r.paper_only is True


class TestBlockedCases:
    def test_no_stop_loss_blocked(self):
        r = evaluate_stop_loss_coverage(_inp(has_stop_loss=False, position_size_amount=50000))
        assert r.status == RiskStatus.BLOCKED

    def test_no_stop_loss_has_reason(self):
        r = evaluate_stop_loss_coverage(_inp(has_stop_loss=False, position_size_amount=50000))
        assert RiskBlockReason.NO_STOP_LOSS in r.block_reasons

    def test_abc_plan_blocked_cascades(self):
        r = evaluate_stop_loss_coverage(_inp(has_stop_loss=True, abc_plan_blocked=True))
        assert r.status == RiskStatus.BLOCKED
        assert RiskBlockReason.STOP_LOSS_COVERAGE_INCOMPLETE in r.block_reasons

    def test_no_stop_loss_coverage_incomplete(self):
        r = evaluate_stop_loss_coverage(_inp(has_stop_loss=False, position_size_amount=50000))
        assert r.all_positions_covered is False


class TestResultFields:
    def test_has_stop_loss_stored(self):
        r = evaluate_stop_loss_coverage(_inp(has_stop_loss=True))
        assert r.has_stop_loss is True

    def test_detail_not_empty(self):
        r = evaluate_stop_loss_coverage(_inp(has_stop_loss=True))
        assert len(r.detail) > 0

    def test_no_real_orders(self):
        assert evaluate_stop_loss_coverage(_inp()).no_real_orders is True

    def test_not_investment_advice(self):
        assert evaluate_stop_loss_coverage(_inp()).not_investment_advice is True
