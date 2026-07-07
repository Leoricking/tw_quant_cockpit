"""tests/test_theme_rotation_v171.py — theme rotation signal tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    ThemeStrength, ThemeCategory,
)
from paper_trading.small_capital_strategy.theme_rotation_v171 import (
    determine_rotation_phase, build_theme_rotation_signal,
    rank_themes_by_strength, get_leading_themes, get_sample_theme_signals,
    ROTATION_PHASES,
)


def test_rotation_phases_tuple():
    assert isinstance(ROTATION_PHASES, tuple)
    assert "EARLY" in ROTATION_PHASES
    assert "COOLING" in ROTATION_PHASES


def test_phase_early():
    assert determine_rotation_phase(85.0, 0.70, 6) == "EARLY"


def test_phase_mid():
    assert determine_rotation_phase(65.0, 0.55, 3) == "MID"


def test_phase_late():
    assert determine_rotation_phase(45.0, 0.30, 1) == "LATE"


def test_phase_cooling():
    assert determine_rotation_phase(20.0, 0.15, 0) == "COOLING"


def test_build_signal_paper_only():
    sig = build_theme_rotation_signal("AI", ThemeCategory.AI_SEMICONDUCTOR, 6, 0.80, 90.0)
    assert sig.paper_only is True


def test_build_signal_not_investment_advice():
    sig = build_theme_rotation_signal("AI", ThemeCategory.AI_SEMICONDUCTOR, 6, 0.80, 90.0)
    assert sig.not_investment_advice is True


def test_build_signal_theme_name():
    sig = build_theme_rotation_signal("AI", ThemeCategory.AI_SEMICONDUCTOR, 6, 0.80, 90.0)
    assert sig.theme == "AI"


def test_build_signal_strong():
    sig = build_theme_rotation_signal("EV", ThemeCategory.EV_BATTERY, 3, 0.55, 65.0)
    assert sig.theme_strength == ThemeStrength.STRONG


def test_build_signal_leading():
    sig = build_theme_rotation_signal("AI", ThemeCategory.AI_SEMICONDUCTOR, 6, 0.80, 90.0)
    assert sig.theme_strength == ThemeStrength.LEADING


def test_build_signal_rotation_phase():
    sig = build_theme_rotation_signal("AI", ThemeCategory.AI_SEMICONDUCTOR, 6, 0.80, 90.0)
    assert sig.rotation_phase in ROTATION_PHASES


def test_rank_themes_by_strength_order():
    signals = get_sample_theme_signals()
    ranked = rank_themes_by_strength(signals)
    # First should be stronger than last
    strength_order = {
        ThemeStrength.LEADING: 4,
        ThemeStrength.STRONG: 3,
        ThemeStrength.MODERATE: 2,
        ThemeStrength.WEAK: 1,
        ThemeStrength.UNKNOWN: 0,
    }
    for i in range(len(ranked) - 1):
        assert (
            strength_order.get(ranked[i].theme_strength, 0)
            >= strength_order.get(ranked[i + 1].theme_strength, 0)
        )


def test_get_leading_themes_filters():
    signals = get_sample_theme_signals()
    leading = get_leading_themes(signals)
    for sig in leading:
        assert sig.theme_strength in (ThemeStrength.LEADING, ThemeStrength.STRONG)


def test_get_sample_signals_returns_list():
    signals = get_sample_theme_signals()
    assert isinstance(signals, list)
    assert len(signals) > 0


def test_get_sample_signals_count():
    signals = get_sample_theme_signals()
    assert len(signals) == 5


def test_get_sample_signals_paper_only():
    for sig in get_sample_theme_signals():
        assert sig.paper_only is True


def test_rank_empty_list():
    ranked = rank_themes_by_strength([])
    assert ranked == []


def test_leading_themes_empty_list():
    assert get_leading_themes([]) == []
