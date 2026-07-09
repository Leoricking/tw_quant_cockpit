"""
tests/test_trade_journal_regime_review_v175.py
Tests for Trade Journal regime review v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeDirection, ABCPattern, ReviewStatus, TradeOutcome,
)
from paper_trading.small_capital_strategy.trade_journal_entry_v175 import (
    create_journal_entry, close_journal_entry,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import RegimeOutcomeReview
from paper_trading.small_capital_strategy.trade_journal_regime_review_v175 import (
    review_regime_outcome, calculate_regime_alignment_score,
)


def _bull_win():
    e = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                             580.0, 50000.0, 552.0, 0.05,
                             ABCPattern.B_BREAKOUT, "BULL", 1)
    return close_journal_entry(e, "2026-01-20", 638.0)


def _bull_loss():
    e = create_journal_entry("2317", TradeDirection.LONG, "2026-01-06",
                             100.0, 50000.0, 95.0, 0.05,
                             ABCPattern.UNKNOWN, "BULL", 1)
    return close_journal_entry(e, "2026-01-20", 90.0)


def _bear_loss():
    e = create_journal_entry("2454", TradeDirection.LONG, "2026-01-07",
                             180.0, 50000.0, 170.0, 0.05,
                             ABCPattern.UNKNOWN, "BEAR", 0)
    return close_journal_entry(e, "2026-01-21", 160.0)


class TestCalculateRegimeAlignmentScore:
    def test_all_bull_100pct(self):
        entries = [_bull_win(), _bull_win()]
        assert calculate_regime_alignment_score(entries) == 100.0

    def test_all_bear_0pct(self):
        entries = [_bear_loss(), _bear_loss()]
        assert calculate_regime_alignment_score(entries) == 0.0

    def test_empty_list_zero(self):
        assert calculate_regime_alignment_score([]) == 0.0

    def test_mixed_partial_score(self):
        entries = [_bull_win(), _bear_loss()]
        score = calculate_regime_alignment_score(entries)
        assert 0 < score < 100


class TestReviewRegimeOutcome:
    def test_returns_regime_outcome_review(self):
        r = review_regime_outcome("BULL", [_bull_win()])
        assert isinstance(r, RegimeOutcomeReview)

    def test_regime_set(self):
        r = review_regime_outcome("BULL", [_bull_win()])
        assert r.regime == "BULL"

    def test_trade_count_correct(self):
        r = review_regime_outcome("BULL", [_bull_win(), _bull_loss()])
        assert r.trade_count == 2

    def test_win_count_correct(self):
        r = review_regime_outcome("BULL", [_bull_win(), _bull_loss()])
        assert r.win_count == 1

    def test_loss_count_correct(self):
        r = review_regime_outcome("BULL", [_bull_win(), _bull_loss()])
        assert r.loss_count == 1

    def test_win_rate_50pct(self):
        r = review_regime_outcome("BULL", [_bull_win(), _bull_loss()])
        assert r.win_rate_pct == 50.0

    def test_empty_regime_pending_status(self):
        r = review_regime_outcome("BULL", [])
        assert r.review_status == ReviewStatus.PENDING

    def test_paper_only_true(self):
        r = review_regime_outcome("BULL", [_bull_win()])
        assert r.paper_only is True

    def test_no_broker_true(self):
        r = review_regime_outcome("BULL", [_bull_win()])
        assert r.no_broker is True

    def test_not_investment_advice_true(self):
        r = review_regime_outcome("BULL", [_bull_win()])
        assert r.not_investment_advice is True

    def test_schema_version(self):
        r = review_regime_outcome("BULL", [_bull_win()])
        assert r.schema_version == "175"

    def test_bear_regime_alignment_score_zero(self):
        r = review_regime_outcome("BEAR", [_bear_loss()])
        assert r.regime_alignment_score == 0.0

    def test_bull_regime_alignment_score_100(self):
        r = review_regime_outcome("BULL", [_bull_win()])
        assert r.regime_alignment_score == 100.0

    def test_period_start_set(self):
        r = review_regime_outcome("BULL", [_bull_win()])
        assert r.period_start != ""

    def test_no_match_for_wrong_regime(self):
        r = review_regime_outcome("RANGE", [_bull_win()])
        assert r.trade_count == 0
