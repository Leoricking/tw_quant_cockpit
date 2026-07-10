"""
paper_trading/small_capital_strategy/theme_rotation_enums_v177.py
Enums for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum
from typing import List

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"


class ThemeCategory(Enum):
    AI_SERVER               = "AI_SERVER"
    ASIC                    = "ASIC"
    GPU_SERVER              = "GPU_SERVER"
    COOLING                 = "COOLING"
    POWER_SUPPLY            = "POWER_SUPPLY"
    PCB                     = "PCB"
    CCL                     = "CCL"
    HIGH_SPEED_TRANSMISSION = "HIGH_SPEED_TRANSMISSION"
    SEMICONDUCTOR           = "SEMICONDUCTOR"
    ADVANCED_PACKAGING      = "ADVANCED_PACKAGING"
    ROBOTICS                = "ROBOTICS"
    EDGE_AI                 = "EDGE_AI"
    EV                      = "EV"
    ENERGY_STORAGE          = "ENERGY_STORAGE"
    FINANCIAL               = "FINANCIAL"
    SHIPPING                = "SHIPPING"
    BIOTECH                 = "BIOTECH"
    UNKNOWN                 = "UNKNOWN"

ThemeCategory._SCHEMA  = "177"
ThemeCategory._POLICY  = "1.7.7-theme-rotation-scanner"


class ThemeGrade(Enum):
    LEADER   = "LEADER"
    STRONG   = "STRONG"
    WATCH    = "WATCH"
    WEAK     = "WEAK"
    EXCLUDED = "EXCLUDED"

ThemeGrade._SCHEMA  = "177"
ThemeGrade._POLICY  = "1.7.7-theme-rotation-scanner"


class ThemeSignalType(Enum):
    BREADTH       = "BREADTH"
    MOMENTUM      = "MOMENTUM"
    CONTINUATION  = "CONTINUATION"
    RISK          = "RISK"
    VOLUME        = "VOLUME"
    INSTITUTIONAL = "INSTITUTIONAL"
    MARGIN        = "MARGIN"

ThemeSignalType._SCHEMA  = "177"
ThemeSignalType._POLICY  = "1.7.7-theme-rotation-scanner"


def get_all_enum_names() -> List[str]:
    """Return all enum class names defined in this module."""
    return ["ThemeCategory", "ThemeGrade", "ThemeSignalType"]


def get_all_theme_categories() -> List[ThemeCategory]:
    """Return all ThemeCategory members."""
    return list(ThemeCategory)


def get_all_grades() -> List[ThemeGrade]:
    """Return all ThemeGrade members."""
    return list(ThemeGrade)


def get_all_signal_types() -> List[ThemeSignalType]:
    """Return all ThemeSignalType members."""
    return list(ThemeSignalType)
