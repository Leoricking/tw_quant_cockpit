"""
tests/test_trade_journal_risk_review_v175.py
Tests for Trade Journal risk review v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeDirection, ABCPattern, ReviewStatus,
)
from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeDecisionSnapshot, RiskViolationReview,
)
from paper_trading.small_capital_strategy.trade_journal_risk_review_v175 import (
    review_risk_violations, detect_violations,
)


def _compliant_entry():
    return create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                580.0, 50000.0, 552.0, 0.05,
                                ABCPattern.B_BREAKOUT, "BULL", 1)


def _no_stop_loss_entry():
    return create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                580.0, 50000.0, 0.0, 0.0,
                                ABCPattern.UNKNOWN, "BULL", 1)


def _oversize_entry():
    return create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                580.0, 100000.0, 552.0, 0.05,
                                ABCPattern.B_BREAKOUT, "BULL", 1)


def _bear_entry():
    return create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                580.0, 50000.0, 552.0, 0.05,
                                ABCPattern.UNKNOWN, "BEAR", 1)


class TestDetectViolations:
    def test_compliant_no_violations(self):
        assert detect_violations(_compliant_entry()) == []

    def test_no_stop_loss_detected(self):
        assert "NO_STOP_LOSS" in detect_violations(_no_stop_loss_entry())

    def test_oversize_detected(self):
        assert "OVERSIZE" in detect_violations(_oversize_entry())

    def test_regime_mismatch_detected(self):
        assert "REGIME_MISMATCH" in detect_violations(_bear_entry())

    def test_risk_off_mismatch_detected(self):
        e = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                 580.0, 50000.0, 552.0, 0.05,
                                 ABCPattern.UNKNOWN, "RISK_OFF", 1)
        assert "REGIME_MISMATCH" in detect_violations(e)


class TestReviewRiskViolations:
    def test_returns_risk_violation_review(self):
        assert isinstance(review_risk_violations(_compliant_entry()), RiskViolationReview)

    def test_compliant_entry_pass_status(self):
        r = review_risk_violations(_compliant_entry())
        assert r.review_status == ReviewStatus.PASS

    def test_no_stop_loss_warn_or_fail(self):
        r = review_risk_violations(_no_stop_loss_entry())
        assert r.review_status in (ReviewStatus.WARN, ReviewStatus.FAIL)

    def test_no_stop_loss_detected_flag(self):
        r = review_risk_violations(_no_stop_loss_entry())
        assert r.no_stop_loss_detected is True

    def test_oversize_detected_flag(self):
        r = review_risk_violations(_oversize_entry())
        assert r.oversize_detected is True

    def test_regime_mismatch_detected_flag(self):
        r = review_risk_violations(_bear_entry())
        assert r.regime_mismatch_detected is True

    def test_paper_only_true(self):
        assert review_risk_violations(_compliant_entry()).paper_only is True

    def test_no_broker_true(self):
        assert review_risk_violations(_compliant_entry()).no_broker is True

    def test_not_investment_advice_true(self):
        assert review_risk_violations(_compliant_entry()).not_investment_advice is True

    def test_symbol_preserved(self):
        r = review_risk_violations(_compliant_entry())
        assert r.symbol == "2330"

    def test_violation_date_set(self):
        r = review_risk_violations(_compliant_entry())
        assert r.violation_date == "2026-01-05"

    def test_multiple_violations_fail_status(self):
        e = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                 580.0, 100000.0, 0.0, 0.0,
                                 ABCPattern.UNKNOWN, "BEAR", 0)
        r = review_risk_violations(e)
        assert r.review_status == ReviewStatus.FAIL

    def test_schema_version(self):
        r = review_risk_violations(_compliant_entry())
        assert r.schema_version == "175"

    def test_severity_none_for_compliant(self):
        r = review_risk_violations(_compliant_entry())
        assert r.severity == "NONE"
