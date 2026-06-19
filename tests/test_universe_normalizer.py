"""
tests/test_universe_normalizer.py — Symbol normalizer tests for v1.3.1.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import pytest
from universe.symbol_normalizer import SymbolNormalizer
from universe.models import UniverseMarket


class TestSymbolNormalizer:
    """9 normalizer tests (v1.3.1)."""

    def setup_method(self):
        self.norm = SymbolNormalizer()

    def test_plain_twse_symbol(self):
        result = self.norm.normalize("2330")
        assert result.is_valid
        assert result.normalized_symbol == "2330"
        assert result.detected_market == UniverseMarket.TWSE.value

    def test_dotTW_suffix(self):
        result = self.norm.normalize("2330.TW")
        assert result.is_valid
        assert result.normalized_symbol == "2330"
        assert result.detected_market == UniverseMarket.TWSE.value

    def test_TWSE_prefix(self):
        result = self.norm.normalize("TWSE:2330")
        assert result.is_valid
        assert result.normalized_symbol == "2330"
        assert result.detected_market == UniverseMarket.TWSE.value

    def test_dotTWO_suffix_tpex(self):
        result = self.norm.normalize("6488.TWO")
        assert result.is_valid
        assert result.normalized_symbol == "6488"
        assert result.detected_market == UniverseMarket.TPEX.value

    def test_TPEx_prefix(self):
        result = self.norm.normalize("TPEx:6488")
        assert result.is_valid
        assert result.normalized_symbol == "6488"
        assert result.detected_market == UniverseMarket.TPEX.value

    def test_lowercase_suffix(self):
        result = self.norm.normalize("2330.tw")
        assert result.is_valid
        assert result.normalized_symbol == "2330"
        assert result.detected_market == UniverseMarket.TWSE.value

    def test_invalid_symbol(self):
        result = self.norm.normalize("")
        assert not result.is_valid

    def test_unsupported_foreign_symbol(self):
        result = self.norm.normalize("AAPL")
        assert not result.is_valid
        assert "UNSUPPORTED" in result.warning or "unsupported" in result.warning.lower()

    def test_unknown_market_does_not_guess(self):
        # "7777" — prefix 7 is not in our known TWSE or TPEx prefixes
        result = self.norm.normalize("7777")
        # Should be valid code format but market should be UNKNOWN
        assert result.is_valid
        assert result.detected_market == UniverseMarket.UNKNOWN.value

    def test_leading_zeros_preserved(self):
        result = self.norm.normalize("0050")
        assert result.is_valid
        assert result.normalized_symbol == "0050"

    def test_chinese_name_is_not_symbol(self):
        result = self.norm.normalize("台積電")
        assert not result.is_valid
        assert "name" in result.warning.lower() or "symbol" in result.warning.lower()
