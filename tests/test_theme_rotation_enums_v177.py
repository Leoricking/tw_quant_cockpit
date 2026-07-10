"""tests/test_theme_rotation_enums_v177.py — v1.7.7 enum tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import (
    ThemeCategory, ThemeGrade, ThemeSignalType,
    get_all_enum_names, get_all_theme_categories, get_all_grades, get_all_signal_types,
)


class TestThemeCategoryEnum:
    def test_count_ge_18(self):
        assert len(ThemeCategory) >= 18

    def test_ai_server_exists(self):
        assert ThemeCategory.AI_SERVER.value == "AI_SERVER"

    def test_asic_exists(self):
        assert ThemeCategory.ASIC.value == "ASIC"

    def test_gpu_server_exists(self):
        assert ThemeCategory.GPU_SERVER.value == "GPU_SERVER"

    def test_cooling_exists(self):
        assert ThemeCategory.COOLING.value == "COOLING"

    def test_power_supply_exists(self):
        assert ThemeCategory.POWER_SUPPLY.value == "POWER_SUPPLY"

    def test_pcb_exists(self):
        assert ThemeCategory.PCB.value == "PCB"

    def test_ccl_exists(self):
        assert ThemeCategory.CCL.value == "CCL"

    def test_high_speed_transmission_exists(self):
        assert ThemeCategory.HIGH_SPEED_TRANSMISSION.value == "HIGH_SPEED_TRANSMISSION"

    def test_semiconductor_exists(self):
        assert ThemeCategory.SEMICONDUCTOR.value == "SEMICONDUCTOR"

    def test_advanced_packaging_exists(self):
        assert ThemeCategory.ADVANCED_PACKAGING.value == "ADVANCED_PACKAGING"

    def test_robotics_exists(self):
        assert ThemeCategory.ROBOTICS.value == "ROBOTICS"

    def test_edge_ai_exists(self):
        assert ThemeCategory.EDGE_AI.value == "EDGE_AI"

    def test_ev_exists(self):
        assert ThemeCategory.EV.value == "EV"

    def test_energy_storage_exists(self):
        assert ThemeCategory.ENERGY_STORAGE.value == "ENERGY_STORAGE"

    def test_financial_exists(self):
        assert ThemeCategory.FINANCIAL.value == "FINANCIAL"

    def test_shipping_exists(self):
        assert ThemeCategory.SHIPPING.value == "SHIPPING"

    def test_biotech_exists(self):
        assert ThemeCategory.BIOTECH.value == "BIOTECH"

    def test_unknown_exists(self):
        assert ThemeCategory.UNKNOWN.value == "UNKNOWN"


class TestThemeGradeEnum:
    def test_count_5(self):
        assert len(ThemeGrade) == 5

    def test_leader_exists(self):
        assert ThemeGrade.LEADER.value == "LEADER"

    def test_strong_exists(self):
        assert ThemeGrade.STRONG.value == "STRONG"

    def test_watch_exists(self):
        assert ThemeGrade.WATCH.value == "WATCH"

    def test_weak_exists(self):
        assert ThemeGrade.WEAK.value == "WEAK"

    def test_excluded_exists(self):
        assert ThemeGrade.EXCLUDED.value == "EXCLUDED"


class TestThemeSignalTypeEnum:
    def test_count_7(self):
        assert len(ThemeSignalType) == 7

    def test_breadth_exists(self):
        assert ThemeSignalType.BREADTH.value == "BREADTH"

    def test_momentum_exists(self):
        assert ThemeSignalType.MOMENTUM.value == "MOMENTUM"

    def test_continuation_exists(self):
        assert ThemeSignalType.CONTINUATION.value == "CONTINUATION"

    def test_risk_exists(self):
        assert ThemeSignalType.RISK.value == "RISK"

    def test_volume_exists(self):
        assert ThemeSignalType.VOLUME.value == "VOLUME"

    def test_institutional_exists(self):
        assert ThemeSignalType.INSTITUTIONAL.value == "INSTITUTIONAL"

    def test_margin_exists(self):
        assert ThemeSignalType.MARGIN.value == "MARGIN"


class TestEnumHelpers:
    def test_get_all_enum_names_count_3(self):
        assert len(get_all_enum_names()) == 3

    def test_get_all_enum_names_contains_category(self):
        assert "ThemeCategory" in get_all_enum_names()

    def test_get_all_enum_names_contains_grade(self):
        assert "ThemeGrade" in get_all_enum_names()

    def test_get_all_enum_names_contains_signal(self):
        assert "ThemeSignalType" in get_all_enum_names()

    def test_get_all_theme_categories_ge_18(self):
        cats = get_all_theme_categories()
        assert len(cats) >= 18

    def test_get_all_theme_categories_contains_ai_server(self):
        cats = get_all_theme_categories()
        assert ThemeCategory.AI_SERVER in cats

    def test_get_all_grades_count_5(self):
        grades = get_all_grades()
        assert len(grades) == 5

    def test_get_all_grades_contains_leader(self):
        grades = get_all_grades()
        assert ThemeGrade.LEADER in grades

    def test_get_all_signal_types_count_7(self):
        types = get_all_signal_types()
        assert len(types) == 7
