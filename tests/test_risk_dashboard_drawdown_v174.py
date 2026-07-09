"""
tests/test_risk_dashboard_drawdown_v174.py
Tests for drawdown monitor v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import RiskStatus, DrawdownLevel, RiskBlockReason
from paper_trading.small_capital_strategy.drawdown_monitor_v174 import (
    evaluate_drawdown, get_drawdown_thresholds,
    DRAWDOWN_PASS_MAX, DRAWDOWN_WATCH_MAX, DRAWDOWN_WARNING_MAX,
)


def _inp(dd=0.0):
    return SmallAccountRiskInput(current_drawdown_pct=dd)


class TestThresholds:
    def test_pass_max_5(self):
        assert DRAWDOWN_PASS_MAX == 5.0

    def test_watch_max_8(self):
        assert DRAWDOWN_WATCH_MAX == 8.0

    def test_warning_max_12(self):
        assert DRAWDOWN_WARNING_MAX == 12.0

    def test_thresholds_dict(self):
        t = get_drawdown_thresholds()
        assert t["pass_max_pct"] == 5.0
        assert t["watch_max_pct"] == 8.0
        assert t["warning_max_pct"] == 12.0

    def test_thresholds_paper_only(self):
        assert get_drawdown_thresholds()["paper_only"] is True


class TestPassCases:
    def test_zero_pass(self):
        assert evaluate_drawdown(_inp(0.0)).status == RiskStatus.PASS

    def test_2pct_pass(self):
        assert evaluate_drawdown(_inp(2.0)).status == RiskStatus.PASS

    def test_5pct_pass(self):
        assert evaluate_drawdown(_inp(5.0)).status == RiskStatus.PASS

    def test_pass_level(self):
        assert evaluate_drawdown(_inp(2.0)).level == DrawdownLevel.PASS

    def test_negative_value_abs(self):
        # Negative drawdown values should be treated as absolute
        assert evaluate_drawdown(_inp(-3.0)).status == RiskStatus.PASS


class TestWatchCases:
    def test_6pct_watch(self):
        assert evaluate_drawdown(_inp(6.0)).status == RiskStatus.WATCH

    def test_8pct_watch(self):
        assert evaluate_drawdown(_inp(8.0)).status == RiskStatus.WATCH

    def test_watch_level(self):
        assert evaluate_drawdown(_inp(6.0)).level == DrawdownLevel.WATCH


class TestWarningCases:
    def test_9pct_warning(self):
        assert evaluate_drawdown(_inp(9.0)).status == RiskStatus.WARNING

    def test_12pct_warning(self):
        assert evaluate_drawdown(_inp(12.0)).status == RiskStatus.WARNING

    def test_warning_level(self):
        assert evaluate_drawdown(_inp(10.0)).level == DrawdownLevel.WARNING


class TestBlockedCases:
    def test_13pct_blocked(self):
        assert evaluate_drawdown(_inp(13.0)).status == RiskStatus.BLOCKED

    def test_20pct_blocked(self):
        assert evaluate_drawdown(_inp(20.0)).status == RiskStatus.BLOCKED

    def test_blocked_level(self):
        assert evaluate_drawdown(_inp(15.0)).level == DrawdownLevel.BLOCKED

    def test_blocked_has_block_reason(self):
        r = evaluate_drawdown(_inp(15.0))
        assert RiskBlockReason.DRAWDOWN_LIMIT_BREACHED in r.block_reasons


class TestResultFields:
    def test_paper_only(self):
        assert evaluate_drawdown(_inp(2.0)).paper_only is True

    def test_drawdown_pct_stored(self):
        r = evaluate_drawdown(_inp(3.0))
        assert r.drawdown_pct == 3.0

    def test_detail_not_empty(self):
        assert len(evaluate_drawdown(_inp(2.0)).detail) > 0

    def test_block_reasons_empty_when_pass(self):
        assert evaluate_drawdown(_inp(2.0)).block_reasons == []
