"""
paper_trading/small_capital_strategy/theme_rotation_v171.py
Theme rotation signal engine for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    ThemeCategory, ThemeStrength,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import ThemeRotationSignal
from paper_trading.small_capital_strategy.theme_strength_model_v171 import assess_theme_strength

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

ROTATION_PHASES = ("EARLY", "MID", "LATE", "COOLING")


def determine_rotation_phase(
    momentum_score: float,
    breadth_score: float,
    leader_count: int,
) -> str:
    """Determine theme rotation phase from momentum, breadth, and leader count."""
    if momentum_score >= 80 and breadth_score >= 0.65 and leader_count >= 5:
        return "EARLY"
    if momentum_score >= 60 and breadth_score >= 0.50:
        return "MID"
    if momentum_score >= 40:
        return "LATE"
    return "COOLING"


def build_theme_rotation_signal(
    theme: str,
    theme_category: ThemeCategory,
    leader_count: int,
    breadth_pct: float,
    momentum_score: float,
) -> ThemeRotationSignal:
    """Build a ThemeRotationSignal for a given theme."""
    strength = assess_theme_strength(theme, leader_count, breadth_pct, momentum_score)
    phase = determine_rotation_phase(momentum_score, breadth_pct, leader_count)
    return ThemeRotationSignal(
        theme=theme,
        theme_category=theme_category,
        theme_strength=strength,
        momentum_score=float(momentum_score),
        leader_count=int(leader_count),
        breadth_score=float(breadth_pct),
        rotation_phase=phase,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def rank_themes_by_strength(signals: List[ThemeRotationSignal]) -> List[ThemeRotationSignal]:
    """Return theme signals sorted by momentum_score descending."""
    strength_order = {
        ThemeStrength.LEADING: 4,
        ThemeStrength.STRONG:  3,
        ThemeStrength.MODERATE: 2,
        ThemeStrength.WEAK:    1,
        ThemeStrength.UNKNOWN: 0,
    }
    return sorted(
        signals,
        key=lambda s: (strength_order.get(s.theme_strength, 0), s.momentum_score),
        reverse=True,
    )


def get_leading_themes(signals: List[ThemeRotationSignal]) -> List[ThemeRotationSignal]:
    """Return only LEADING or STRONG theme signals."""
    return [s for s in signals if s.theme_strength in (ThemeStrength.LEADING, ThemeStrength.STRONG)]


def get_sample_theme_signals() -> List[ThemeRotationSignal]:
    """Return sample theme rotation signals for demo/testing. Deterministic."""
    samples = [
        ("AI_SEMICONDUCTOR", ThemeCategory.AI_SEMICONDUCTOR, 6, 0.80, 90.0),
        ("EV_BATTERY",       ThemeCategory.EV_BATTERY,       3, 0.55, 65.0),
        ("GREEN_ENERGY",     ThemeCategory.GREEN_ENERGY,      2, 0.45, 50.0),
        ("DEFENSE",          ThemeCategory.DEFENSE,           1, 0.30, 40.0),
        ("BIOTECH",          ThemeCategory.BIOTECH,           0, 0.20, 20.0),
    ]
    return [
        build_theme_rotation_signal(name, cat, ldr, brd, mom)
        for name, cat, ldr, brd, mom in samples
    ]
