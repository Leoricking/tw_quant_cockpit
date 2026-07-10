"""
paper_trading/small_capital_strategy/theme_rotation_classifier_v177.py
Theme classifier for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List, Optional

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"


def get_default_theme_mapping() -> Dict[str, object]:
    """Return {symbol: ThemeCategory} example mapping for Taiwan stocks."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory
    return {
        "2330": ThemeCategory.SEMICONDUCTOR,
        "2317": ThemeCategory.AI_SERVER,
        "2382": ThemeCategory.GPU_SERVER,
        "2454": ThemeCategory.SEMICONDUCTOR,
        "3711": ThemeCategory.AI_SERVER,
        "2308": ThemeCategory.GPU_SERVER,
        "2412": ThemeCategory.HIGH_SPEED_TRANSMISSION,
        "3034": ThemeCategory.ADVANCED_PACKAGING,
        "6669": ThemeCategory.COOLING,
        "2395": ThemeCategory.PCB,
        "3008": ThemeCategory.HIGH_SPEED_TRANSMISSION,
        "2345": ThemeCategory.CCL,
        "6770": ThemeCategory.POWER_SUPPLY,
        "2376": ThemeCategory.GPU_SERVER,
        "4938": ThemeCategory.AI_SERVER,
        "2379": ThemeCategory.ASIC,
        "5274": ThemeCategory.EDGE_AI,
        "3045": ThemeCategory.HIGH_SPEED_TRANSMISSION,
        "2049": ThemeCategory.ROBOTICS,
        "1590": ThemeCategory.ROBOTICS,
    }


def get_all_theme_categories() -> List[object]:
    """Return all ThemeCategory members."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory
    return list(ThemeCategory)


def classify_theme(signals: List[object]) -> object:
    """Classify dominant theme from a list of ThemeSignal objects."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory
    if not signals:
        return ThemeCategory.UNKNOWN
    # Return the theme of the signal with the highest value
    best = max(signals, key=lambda s: getattr(s, "value", 0.0))
    return getattr(best, "theme", ThemeCategory.UNKNOWN)


def get_theme_for_symbol(symbol: str, mapping: Optional[Dict[str, object]] = None) -> object:
    """Return ThemeCategory for a symbol. Falls back to UNKNOWN if not found."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory
    if mapping is None:
        mapping = get_default_theme_mapping()
    return mapping.get(symbol, ThemeCategory.UNKNOWN)
