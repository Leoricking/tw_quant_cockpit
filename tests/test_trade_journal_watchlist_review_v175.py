"""
tests/test_trade_journal_watchlist_review_v175.py
Tests for Trade Journal watchlist review v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import ReviewStatus
from paper_trading.small_capital_strategy.trade_journal_models_v175 import WatchlistConversionReview
from paper_trading.small_capital_strategy.trade_journal_watchlist_review_v175 import (
    review_watchlist_conversion, calculate_conversion_rate,
)


class TestCalculateConversionRate:
    def test_50pct_rate(self):
        assert calculate_conversion_rate(5, 5, 5) == 50.0

    def test_100pct_rate(self):
        assert calculate_conversion_rate(5, 5, 10) == 100.0

    def test_zero_rate_no_candidates(self):
        assert calculate_conversion_rate(0, 0, 0) == 0.0

    def test_partial_rate(self):
        assert calculate_conversion_rate(5, 3, 4) == 50.0

    def test_rounding(self):
        r = calculate_conversion_rate(3, 1, 1)
        assert isinstance(r, float)


class TestReviewWatchlistConversion:
    def _tier1_converted(self):
        return review_watchlist_conversion("2330", 1, True, "", 5, 3, 4)

    def test_returns_watchlist_conversion_review(self):
        assert isinstance(self._tier1_converted(), WatchlistConversionReview)

    def test_symbol_preserved(self):
        assert self._tier1_converted().symbol == "2330"

    def test_tier_set(self):
        assert self._tier1_converted().watchlist_tier == 1

    def test_converted_true(self):
        assert self._tier1_converted().converted_to_trade is True

    def test_tier1_converted_high_score(self):
        assert self._tier1_converted().conversion_score >= 80.0

    def test_tier1_converted_pass_status(self):
        assert self._tier1_converted().review_status == ReviewStatus.PASS

    def test_tier0_not_converted_fail(self):
        r = review_watchlist_conversion("2330", 0, False, "no trigger", 0, 0, 0)
        assert r.review_status == ReviewStatus.FAIL

    def test_paper_only_true(self):
        assert self._tier1_converted().paper_only is True

    def test_no_broker_true(self):
        assert self._tier1_converted().no_broker is True

    def test_not_investment_advice_true(self):
        assert self._tier1_converted().not_investment_advice is True

    def test_conversion_rate_pct_set(self):
        r = self._tier1_converted()
        assert r.conversion_rate_pct >= 0.0

    def test_tier1_not_converted_warn_status(self):
        r = review_watchlist_conversion("2330", 1, False, "regime mismatch", 5, 3, 0)
        assert r.review_status in (ReviewStatus.WARN, ReviewStatus.FAIL)

    def test_schema_version(self):
        assert self._tier1_converted().schema_version == "175"

    def test_exclusion_reason_set(self):
        r = review_watchlist_conversion("2330", 1, False, "bear regime", 5, 3, 0)
        assert r.exclusion_reason == "bear regime"
