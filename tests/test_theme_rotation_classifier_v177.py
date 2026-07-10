"""tests/test_theme_rotation_classifier_v177.py — v1.7.7 classifier tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory, ThemeSignalType
from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeSignal
from paper_trading.small_capital_strategy.theme_rotation_classifier_v177 import (
    get_default_theme_mapping, get_all_theme_categories,
    classify_theme, get_theme_for_symbol,
)


class TestGetDefaultThemeMapping:
    def test_returns_dict(self):
        mapping = get_default_theme_mapping()
        assert isinstance(mapping, dict)

    def test_ge_10_entries(self):
        mapping = get_default_theme_mapping()
        assert len(mapping) >= 10

    def test_2330_is_semiconductor(self):
        mapping = get_default_theme_mapping()
        assert mapping["2330"] == ThemeCategory.SEMICONDUCTOR

    def test_2317_is_ai_server(self):
        mapping = get_default_theme_mapping()
        assert mapping["2317"] == ThemeCategory.AI_SERVER

    def test_all_values_are_theme_category(self):
        mapping = get_default_theme_mapping()
        for v in mapping.values():
            assert isinstance(v, ThemeCategory)


class TestGetAllThemeCategories:
    def test_returns_list(self):
        cats = get_all_theme_categories()
        assert isinstance(cats, list)

    def test_ge_18_categories(self):
        cats = get_all_theme_categories()
        assert len(cats) >= 18

    def test_contains_ai_server(self):
        cats = get_all_theme_categories()
        assert ThemeCategory.AI_SERVER in cats

    def test_contains_unknown(self):
        cats = get_all_theme_categories()
        assert ThemeCategory.UNKNOWN in cats


class TestClassifyTheme:
    def test_empty_signals_returns_unknown(self):
        result = classify_theme([])
        assert result == ThemeCategory.UNKNOWN

    def test_single_signal_returns_its_theme(self):
        sig = ThemeSignal(theme=ThemeCategory.AI_SERVER, value=0.9)
        result = classify_theme([sig])
        assert result == ThemeCategory.AI_SERVER

    def test_highest_value_wins(self):
        sig1 = ThemeSignal(theme=ThemeCategory.AI_SERVER, value=0.9)
        sig2 = ThemeSignal(theme=ThemeCategory.SEMICONDUCTOR, value=0.5)
        result = classify_theme([sig1, sig2])
        assert result == ThemeCategory.AI_SERVER


class TestGetThemeForSymbol:
    def test_known_symbol_2330(self):
        result = get_theme_for_symbol("2330")
        assert result == ThemeCategory.SEMICONDUCTOR

    def test_known_symbol_2317(self):
        result = get_theme_for_symbol("2317")
        assert result == ThemeCategory.AI_SERVER

    def test_unknown_symbol_returns_unknown(self):
        result = get_theme_for_symbol("NOTFOUND")
        assert result == ThemeCategory.UNKNOWN

    def test_custom_mapping(self):
        mapping = {"9999": ThemeCategory.ROBOTICS}
        result = get_theme_for_symbol("9999", mapping)
        assert result == ThemeCategory.ROBOTICS

    def test_custom_mapping_miss(self):
        mapping = {"9999": ThemeCategory.ROBOTICS}
        result = get_theme_for_symbol("0000", mapping)
        assert result == ThemeCategory.UNKNOWN
