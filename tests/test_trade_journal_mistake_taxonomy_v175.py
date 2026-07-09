"""
tests/test_trade_journal_mistake_taxonomy_v175.py
Tests for Trade Journal mistake taxonomy v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeDirection, ABCPattern, MistakeCategory, ReviewStatus, TradeOutcome,
)
from paper_trading.small_capital_strategy.trade_journal_entry_v175 import (
    create_journal_entry, close_journal_entry,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    EntryReviewResult, MistakeTaxonomyResult,
)
from paper_trading.small_capital_strategy.trade_journal_mistake_taxonomy_v175 import (
    classify_mistakes, get_primary_mistake,
)


def _compliant():
    return create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                580.0, 50000.0, 552.0, 0.05,
                                ABCPattern.B_BREAKOUT, "BULL", 1)


def _no_stop_loss():
    return create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                580.0, 50000.0, 0.0, 0.0,
                                ABCPattern.UNKNOWN, "BULL", 1)


def _oversize():
    return create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                580.0, 100000.0, 552.0, 0.05,
                                ABCPattern.B_BREAKOUT, "BULL", 1)


def _bear_regime():
    return create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                580.0, 50000.0, 552.0, 0.05,
                                ABCPattern.UNKNOWN, "BEAR", 0)


class TestGetPrimaryMistake:
    def test_empty_list_returns_none(self):
        assert get_primary_mistake([]) == MistakeCategory.NONE

    def test_none_returns_none(self):
        assert get_primary_mistake([MistakeCategory.NONE]) == MistakeCategory.NONE

    def test_no_stop_loss_highest_severity(self):
        categories = [MistakeCategory.FOMO, MistakeCategory.NO_STOP_LOSS]
        assert get_primary_mistake(categories) == MistakeCategory.NO_STOP_LOSS

    def test_oversize_higher_than_fomo(self):
        categories = [MistakeCategory.FOMO, MistakeCategory.OVERSIZE]
        assert get_primary_mistake(categories) == MistakeCategory.OVERSIZE

    def test_single_mistake_returns_itself(self):
        assert get_primary_mistake([MistakeCategory.REVENGE]) == MistakeCategory.REVENGE


class TestClassifyMistakes:
    def test_returns_mistake_taxonomy_result(self):
        assert isinstance(classify_mistakes(_compliant()), MistakeTaxonomyResult)

    def test_compliant_primary_none(self):
        r = classify_mistakes(_compliant())
        assert r.primary_mistake == MistakeCategory.NONE

    def test_no_stop_loss_detected(self):
        r = classify_mistakes(_no_stop_loss())
        assert MistakeCategory.NO_STOP_LOSS in r.mistake_categories

    def test_oversize_detected(self):
        r = classify_mistakes(_oversize())
        assert MistakeCategory.OVERSIZE in r.mistake_categories

    def test_regime_mismatch_detected(self):
        r = classify_mistakes(_bear_regime())
        assert MistakeCategory.REGIME_MISMATCH in r.mistake_categories

    def test_watchlist_miss_when_tier_0(self):
        e = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                 580.0, 50000.0, 552.0, 0.05,
                                 ABCPattern.B_BREAKOUT, "BULL", 0)
        r = classify_mistakes(e)
        assert MistakeCategory.WATCHLIST_MISS in r.mistake_categories

    def test_paper_only_true(self):
        assert classify_mistakes(_compliant()).paper_only is True

    def test_no_broker_true(self):
        assert classify_mistakes(_compliant()).no_broker is True

    def test_not_investment_advice_true(self):
        assert classify_mistakes(_compliant()).not_investment_advice is True

    def test_symbol_preserved(self):
        r = classify_mistakes(_compliant())
        assert r.symbol == "2330"

    def test_trade_date_preserved(self):
        r = classify_mistakes(_compliant())
        assert r.trade_date == "2026-01-05"

    def test_severity_zero_for_none(self):
        r = classify_mistakes(_compliant())
        assert r.severity_score == 0.0

    def test_severity_positive_for_mistake(self):
        r = classify_mistakes(_no_stop_loss())
        assert r.severity_score > 0

    def test_corrective_action_not_empty_for_mistake(self):
        r = classify_mistakes(_no_stop_loss())
        assert r.corrective_action != ""

    def test_fomo_detected_via_review(self):
        e = _compliant()
        fake_review = EntryReviewResult(trigger_met=False)
        r = classify_mistakes(e, fake_review)
        assert MistakeCategory.FOMO in r.mistake_categories

    def test_schema_version(self):
        r = classify_mistakes(_compliant())
        assert r.schema_version == "175"
