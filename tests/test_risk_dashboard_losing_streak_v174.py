"""
tests/test_risk_dashboard_losing_streak_v174.py
Tests for losing streak monitor v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import RiskStatus, LosingStreakLevel, RiskBlockReason
from paper_trading.small_capital_strategy.losing_streak_monitor_v174 import (
    evaluate_losing_streak, get_losing_streak_thresholds,
    STREAK_PASS_MAX, STREAK_WATCH_MAX, STREAK_WARNING_MAX, STREAK_BLOCK_MIN,
)


def _inp(streak=0):
    return SmallAccountRiskInput(losing_streak_count=streak)


class TestThresholds:
    def test_pass_max_2(self):
        assert STREAK_PASS_MAX == 2

    def test_watch_value_3(self):
        assert STREAK_WATCH_MAX == 3

    def test_warning_value_4(self):
        assert STREAK_WARNING_MAX == 4

    def test_block_min_5(self):
        assert STREAK_BLOCK_MIN == 5

    def test_thresholds_dict(self):
        t = get_losing_streak_thresholds()
        assert t["pass_max"] == 2
        assert t["block_min"] == 5

    def test_thresholds_paper_only(self):
        assert get_losing_streak_thresholds()["paper_only"] is True


class TestPassCases:
    def test_0_pass(self):
        assert evaluate_losing_streak(_inp(0)).status == RiskStatus.PASS

    def test_1_pass(self):
        assert evaluate_losing_streak(_inp(1)).status == RiskStatus.PASS

    def test_2_pass(self):
        assert evaluate_losing_streak(_inp(2)).status == RiskStatus.PASS

    def test_pass_level(self):
        assert evaluate_losing_streak(_inp(1)).level == LosingStreakLevel.PASS


class TestWatchCases:
    def test_3_watch(self):
        assert evaluate_losing_streak(_inp(3)).status == RiskStatus.WATCH

    def test_watch_level(self):
        assert evaluate_losing_streak(_inp(3)).level == LosingStreakLevel.WATCH


class TestWarningCases:
    def test_4_warning(self):
        assert evaluate_losing_streak(_inp(4)).status == RiskStatus.WARNING

    def test_warning_level(self):
        assert evaluate_losing_streak(_inp(4)).level == LosingStreakLevel.WARNING


class TestBlockedCases:
    def test_5_blocked(self):
        assert evaluate_losing_streak(_inp(5)).status == RiskStatus.BLOCKED

    def test_6_blocked(self):
        assert evaluate_losing_streak(_inp(6)).status == RiskStatus.BLOCKED

    def test_10_blocked(self):
        assert evaluate_losing_streak(_inp(10)).status == RiskStatus.BLOCKED

    def test_blocked_level(self):
        assert evaluate_losing_streak(_inp(5)).level == LosingStreakLevel.BLOCKED

    def test_blocked_has_reason(self):
        r = evaluate_losing_streak(_inp(5))
        assert RiskBlockReason.LOSING_STREAK_LIMIT_BREACHED in r.block_reasons


class TestResultFields:
    def test_paper_only(self):
        assert evaluate_losing_streak(_inp(0)).paper_only is True

    def test_streak_stored(self):
        r = evaluate_losing_streak(_inp(3))
        assert r.losing_streak_count == 3

    def test_detail_not_empty(self):
        assert len(evaluate_losing_streak(_inp(0)).detail) > 0

    def test_block_reasons_empty_when_pass(self):
        assert evaluate_losing_streak(_inp(1)).block_reasons == []
