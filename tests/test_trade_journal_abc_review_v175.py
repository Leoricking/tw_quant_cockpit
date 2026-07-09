"""
tests/test_trade_journal_abc_review_v175.py
Tests for Trade Journal ABC review v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeDirection, ABCPattern, ReviewStatus,
)
from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeDecisionSnapshot, ABCExecutionReview,
)
from paper_trading.small_capital_strategy.trade_journal_abc_review_v175 import (
    review_abc_execution, score_abc_execution,
)


def _entry(abc=ABCPattern.C_RECLAIM, regime="BULL", tier=1):
    return create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                580.0, 50000.0, 552.0, 0.05, abc, regime, tier)


def _snap(sl_pct=0.05, size=50000.0):
    return TradeDecisionSnapshot(stop_loss_pct=sl_pct, position_size_twd=size)


class TestScoreABCExecution:
    def test_c_reclaim_with_snap_max_score(self):
        e = _entry(abc=ABCPattern.C_RECLAIM)
        s = _snap(sl_pct=0.05, size=50000.0)
        assert score_abc_execution(e, s) == 100.0

    def test_unknown_pattern_low_score(self):
        e = _entry(abc=ABCPattern.UNKNOWN)
        assert score_abc_execution(e) == 0.0

    def test_b_breakout_no_snap_partial_score(self):
        e = _entry(abc=ABCPattern.B_BREAKOUT)
        score = score_abc_execution(e, None)
        assert 0 < score < 100

    def test_score_range_0_100(self):
        e = _entry()
        s = score_abc_execution(e, _snap())
        assert 0 <= s <= 100


class TestReviewABCExecution:
    def _full_review(self):
        return review_abc_execution(_entry(abc=ABCPattern.C_RECLAIM), _snap())

    def test_returns_abc_execution_review(self):
        assert isinstance(self._full_review(), ABCExecutionReview)

    def test_c_reclaim_a_point_valid(self):
        assert self._full_review().a_point_valid is True

    def test_c_reclaim_b_breakout_clean(self):
        assert self._full_review().b_breakout_clean is True

    def test_c_reclaim_confirmed(self):
        assert self._full_review().c_reclaim_confirmed is True

    def test_position_sized_correctly_with_snap(self):
        assert self._full_review().position_sized_correctly is True

    def test_pass_status_for_full_compliance(self):
        assert self._full_review().review_status == ReviewStatus.PASS

    def test_paper_only_true(self):
        assert self._full_review().paper_only is True

    def test_no_broker_true(self):
        assert self._full_review().no_broker is True

    def test_not_investment_advice_true(self):
        assert self._full_review().not_investment_advice is True

    def test_symbol_preserved(self):
        assert self._full_review().symbol == "2330"

    def test_unknown_pattern_fail_status(self):
        r = review_abc_execution(_entry(abc=ABCPattern.UNKNOWN), None)
        assert r.review_status == ReviewStatus.FAIL

    def test_a_pullback_no_c_confirm(self):
        r = review_abc_execution(_entry(abc=ABCPattern.A_PULLBACK), None)
        assert r.c_reclaim_confirmed is False

    def test_schema_version(self):
        assert self._full_review().schema_version == "175"

    def test_execution_score_positive_for_c_reclaim(self):
        assert self._full_review().execution_score > 0
