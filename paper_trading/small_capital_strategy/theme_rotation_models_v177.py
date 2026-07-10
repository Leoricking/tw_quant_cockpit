"""
paper_trading/small_capital_strategy/theme_rotation_models_v177.py
Data models for Theme Rotation Scanner v1.7.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import (
    ThemeCategory, ThemeGrade, ThemeSignalType,
)

_SCHEMA  = "177"
_POLICY  = "1.7.7-theme-rotation-scanner"
_LINEAGE = "paper_trading.small_capital_strategy.theme_rotation_models_v177"


@dataclass
class ThemeSignal:
    """A single theme signal value."""
    theme: ThemeCategory = ThemeCategory.UNKNOWN
    signal_type: ThemeSignalType = ThemeSignalType.BREADTH
    value: float = 0.0
    date: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class ThemeStrengthScore:
    """Comprehensive strength score for a theme."""
    theme: ThemeCategory = ThemeCategory.UNKNOWN
    score: float = 0.0
    grade: ThemeGrade = ThemeGrade.WATCH
    strong_ratio: float = 0.0
    new_high_ratio: float = 0.0
    above_ma5_ratio: float = 0.0
    above_ma10_ratio: float = 0.0
    above_ma20_ratio: float = 0.0
    above_ma60_ratio: float = 0.0
    volume_expand_ratio: float = 0.0
    institutional_buy_ratio: float = 0.0
    investment_trust_buy_ratio: float = 0.0
    margin_risk: bool = False
    overheated: bool = False
    resonance_count: int = 0
    single_stock_only: bool = False
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class ThemeMomentumScore:
    """Momentum score for a theme."""
    theme: ThemeCategory = ThemeCategory.UNKNOWN
    score: float = 0.0
    week_change_pct: float = 0.0
    month_change_pct: float = 0.0
    relative_strength: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class ThemeBreadthScore:
    """Breadth score for a theme."""
    theme: ThemeCategory = ThemeCategory.UNKNOWN
    score: float = 0.0
    advancing: int = 0
    declining: int = 0
    total: int = 0
    advance_decline_ratio: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class ThemeContinuationScore:
    """Continuation score for a theme."""
    theme: ThemeCategory = ThemeCategory.UNKNOWN
    score: float = 0.0
    consecutive_up_days: int = 0
    pullback_shallow: bool = False
    holding_gain: bool = False
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class ThemeRiskScore:
    """Risk score for a theme (higher = more dangerous)."""
    theme: ThemeCategory = ThemeCategory.UNKNOWN
    score: float = 0.0
    margin_expansion_rate: float = 0.0
    institutional_selling: bool = False
    volume_spike: bool = False
    overheated: bool = False
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class ThemeRotationRank:
    """Ranking entry for a theme."""
    theme: ThemeCategory = ThemeCategory.UNKNOWN
    rank: int = 0
    strength_score: float = 0.0
    grade: ThemeGrade = ThemeGrade.WATCH
    momentum_score: float = 0.0
    breadth_score: float = 0.0
    continuation_score: float = 0.0
    risk_score: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class ThemeStockMapping:
    """Maps a stock symbol to a theme."""
    symbol: str = ""
    theme: ThemeCategory = ThemeCategory.UNKNOWN
    is_leader: bool = False
    strength_rank: int = 0
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class ThemeWatchlistCandidate:
    """A watchlist candidate from theme rotation."""
    symbol: str = ""
    theme: ThemeCategory = ThemeCategory.UNKNOWN
    grade: ThemeGrade = ThemeGrade.WATCH
    reason: str = ""
    eligible: bool = False
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class ThemeRotationDashboard:
    """Comprehensive theme rotation dashboard."""
    date: str = ""
    top_themes: list = field(default_factory=list)
    market_regime: str = "BULL"
    total_themes: int = 0
    leader_count: int = 0
    strong_count: int = 0
    sections: list = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class ThemeRotationReport:
    """Theme rotation report."""
    date: str = ""
    sections: list = field(default_factory=list)
    top_theme: ThemeCategory = ThemeCategory.UNKNOWN
    report_format: str = "text"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY


@dataclass
class ThemeRotationHealthSummary:
    """Health check summary for the theme rotation scanner."""
    status: str = "PASS"
    passed: int = 0
    failed: int = 0
    total: int = 0
    checks: list = field(default_factory=list)
    all_passed: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True
