"""tests/test_theme_rotation_stock_map_v177.py — v1.7.7 stock map tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory
from paper_trading.small_capital_strategy.theme_rotation_stock_map_v177 import (
    build_stock_mapping, get_theme_leaders, filter_by_theme,
)


class TestBuildStockMapping:
    def test_returns_stock_mapping(self):
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeStockMapping
        result = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
        assert isinstance(result, ThemeStockMapping)

    def test_symbol_preserved(self):
        result = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
        assert result.symbol == "2330"

    def test_theme_preserved(self):
        result = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
        assert result.theme == ThemeCategory.SEMICONDUCTOR

    def test_is_leader_true(self):
        result = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
        assert result.is_leader is True

    def test_is_leader_false(self):
        result = build_stock_mapping("2317", ThemeCategory.AI_SERVER, False, 2)
        assert result.is_leader is False

    def test_strength_rank_preserved(self):
        result = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 3)
        assert result.strength_rank == 3

    def test_paper_only_true(self):
        result = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
        assert result.paper_only is True

    def test_no_broker_true(self):
        result = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
        assert result.no_broker is True


class TestGetThemeLeaders:
    def test_empty_list(self):
        result = get_theme_leaders([])
        assert result == []

    def test_filters_leaders(self):
        m1 = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
        m2 = build_stock_mapping("2317", ThemeCategory.AI_SERVER, False, 2)
        result = get_theme_leaders([m1, m2])
        assert len(result) == 1
        assert result[0].symbol == "2330"

    def test_no_leaders(self):
        m1 = build_stock_mapping("2317", ThemeCategory.AI_SERVER, False, 1)
        result = get_theme_leaders([m1])
        assert result == []

    def test_multiple_leaders(self):
        m1 = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
        m2 = build_stock_mapping("2317", ThemeCategory.AI_SERVER, True, 2)
        result = get_theme_leaders([m1, m2])
        assert len(result) == 2


class TestFilterByTheme:
    def test_filters_by_theme(self):
        m1 = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
        m2 = build_stock_mapping("2317", ThemeCategory.AI_SERVER, False, 2)
        result = filter_by_theme([m1, m2], ThemeCategory.SEMICONDUCTOR)
        assert len(result) == 1
        assert result[0].symbol == "2330"

    def test_no_match_returns_empty(self):
        m1 = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
        result = filter_by_theme([m1], ThemeCategory.AI_SERVER)
        assert result == []

    def test_multiple_matches(self):
        m1 = build_stock_mapping("2330", ThemeCategory.SEMICONDUCTOR, True, 1)
        m2 = build_stock_mapping("2454", ThemeCategory.SEMICONDUCTOR, False, 2)
        result = filter_by_theme([m1, m2], ThemeCategory.SEMICONDUCTOR)
        assert len(result) == 2
