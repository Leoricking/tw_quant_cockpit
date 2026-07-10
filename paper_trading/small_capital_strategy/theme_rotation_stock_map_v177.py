"""
paper_trading/small_capital_strategy/theme_rotation_stock_map_v177.py
Stock mapping functions for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"


def build_stock_mapping(
    symbol: str,
    theme: object,
    is_leader: bool,
    strength_rank: int,
) -> object:
    """Build a ThemeStockMapping object."""
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeStockMapping

    return ThemeStockMapping(
        symbol=symbol,
        theme=theme,
        is_leader=is_leader,
        strength_rank=strength_rank,
    )


def get_theme_leaders(mappings: List[object]) -> List[object]:
    """Return all ThemeStockMapping where is_leader=True."""
    return [m for m in mappings if getattr(m, "is_leader", False)]


def filter_by_theme(mappings: List[object], theme: object) -> List[object]:
    """Return all ThemeStockMapping for a specific theme."""
    return [m for m in mappings if getattr(m, "theme", None) == theme]
