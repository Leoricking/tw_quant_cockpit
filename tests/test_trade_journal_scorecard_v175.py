"""
tests/test_trade_journal_scorecard_v175.py
Tests for Trade Journal scorecard v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection
from paper_trading.small_capital_strategy.trade_journal_entry_v175 import (
    create_journal_entry, close_journal_entry,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import ReviewScorecard
from paper_trading.small_capital_strategy.trade_journal_scorecard_v175 import (
    build_scorecard, grade_scorecard, get_weight_table, WEIGHTS_SUM, GRADE_A_MIN,
)


def _win():
    e = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                             580.0, 50000.0, 552.0, 0.05)
    return close_journal_entry(e, "2026-01-20", 638.0)


def _loss():
    e = create_journal_entry("2317", TradeDirection.LONG, "2026-01-06",
                             100.0, 50000.0, 95.0, 0.05)
    return close_journal_entry(e, "2026-01-20", 90.0)


class TestGradeScorecard:
    def test_grade_a_at_85(self):
        assert grade_scorecard(85.0) == "A"

    def test_grade_a_at_100(self):
        assert grade_scorecard(100.0) == "A"

    def test_grade_b_at_70(self):
        assert grade_scorecard(70.0) == "B"

    def test_grade_c_at_55(self):
        assert grade_scorecard(55.0) == "C"

    def test_grade_d_at_40(self):
        assert grade_scorecard(40.0) == "D"

    def test_grade_f_at_0(self):
        assert grade_scorecard(0.0) == "F"

    def test_no_aplus_grade(self):
        assert grade_scorecard(100.0) != "A+"

    def test_no_aplus_constant(self):
        assert GRADE_A_MIN == 85.0


class TestWeightTable:
    def test_total_100(self):
        assert get_weight_table()["total"] == WEIGHTS_SUM

    def test_weights_sum_100(self):
        assert WEIGHTS_SUM == 100

    def test_weight_table_has_all_keys(self):
        wt = get_weight_table()
        assert "entry_quality" in wt
        assert "exit_quality" in wt
        assert "abc_execution" in wt
        assert "watchlist_conversion" in wt
        assert "risk_compliance" in wt
        assert "regime_alignment" in wt


class TestBuildScorecard:
    def test_returns_review_scorecard(self):
        assert isinstance(build_scorecard([_win()]), ReviewScorecard)

    def test_empty_entries_grade_f(self):
        sc = build_scorecard([])
        assert sc.grade == "F"
        assert sc.total_score == 0.0

    def test_win_entries_positive_score(self):
        sc = build_scorecard([_win()])
        assert sc.total_score > 0

    def test_win_rate_100pct_for_all_wins(self):
        sc = build_scorecard([_win(), _win()])
        assert sc.win_rate_pct == 100.0

    def test_win_rate_50pct_mixed(self):
        sc = build_scorecard([_win(), _loss()])
        assert sc.win_rate_pct == 50.0

    def test_paper_only_true(self):
        sc = build_scorecard([_win()])
        assert sc.paper_only is True

    def test_no_broker_true(self):
        sc = build_scorecard([_win()])
        assert sc.no_broker is True

    def test_weights_sum_100(self):
        sc = build_scorecard([_win()])
        assert sc.weights_sum == 100

    def test_grade_not_aplus(self):
        sc = build_scorecard([_win(), _win()])
        assert sc.grade != "A+"

    def test_schema_version(self):
        sc = build_scorecard([_win()])
        assert sc.schema_version == "175"
