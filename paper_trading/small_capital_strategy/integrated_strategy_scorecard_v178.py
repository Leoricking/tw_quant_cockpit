"""
paper_trading/small_capital_strategy/integrated_strategy_scorecard_v178.py
Scorecard computation for Small Capital Strategy Integration v1.7.8.
Scores: theme, watchlist, abc, regime, risk, behavior, journal_quality, final (0–100).
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Optional

from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedScoreGrade, IntegratedRegimeStatus, IntegratedWatchlistStatus,
    IntegratedABCStatus, IntegratedThemeStatus, IntegratedRiskLevel,
    IntegratedBehaviorStatus, score_to_grade,
)
from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
    IntegratedStrategyInput, IntegratedScorecard,
)

_SCHEMA  = "178"
_POLICY  = "1.7.8-small-capital-strategy-integration"
_LINEAGE = "paper_trading.small_capital_strategy.integrated_strategy_scorecard_v178"

# Score weights (sum to 1.0)
_WEIGHT_THEME     = 0.20
_WEIGHT_WATCHLIST = 0.15
_WEIGHT_ABC       = 0.20
_WEIGHT_REGIME    = 0.15
_WEIGHT_RISK      = 0.15
_WEIGHT_BEHAVIOR  = 0.10
_WEIGHT_JOURNAL   = 0.05


def _regime_base_score(status: IntegratedRegimeStatus) -> float:
    _map = {
        IntegratedRegimeStatus.BULL:      85.0,
        IntegratedRegimeStatus.BULL_SOFT: 65.0,
        IntegratedRegimeStatus.NEUTRAL:   50.0,
        IntegratedRegimeStatus.RISK_OFF:  10.0,
        IntegratedRegimeStatus.BEAR:       5.0,
        IntegratedRegimeStatus.UNKNOWN:   20.0,
    }
    return _map.get(status, 20.0)


def _watchlist_base_score(status: IntegratedWatchlistStatus) -> float:
    _map = {
        IntegratedWatchlistStatus.FOCUS:    90.0,
        IntegratedWatchlistStatus.WATCH:    60.0,
        IntegratedWatchlistStatus.EXCLUDED:  0.0,
        IntegratedWatchlistStatus.UNKNOWN:  20.0,
    }
    return _map.get(status, 20.0)


def _abc_base_score(status: IntegratedABCStatus) -> float:
    _map = {
        IntegratedABCStatus.A_READY:   90.0,
        IntegratedABCStatus.B_READY:   85.0,
        IntegratedABCStatus.C_READY:   75.0,
        IntegratedABCStatus.NOT_READY: 20.0,
        IntegratedABCStatus.BLOCKED:    0.0,
    }
    return _map.get(status, 20.0)


def _theme_base_score(status: IntegratedThemeStatus) -> float:
    _map = {
        IntegratedThemeStatus.LEADER:   95.0,
        IntegratedThemeStatus.STRONG:   75.0,
        IntegratedThemeStatus.WATCH:    50.0,
        IntegratedThemeStatus.WEAK:     20.0,
        IntegratedThemeStatus.EXCLUDED:  0.0,
        IntegratedThemeStatus.UNKNOWN:  15.0,
    }
    return _map.get(status, 15.0)


def _risk_base_score(level: IntegratedRiskLevel) -> float:
    _map = {
        IntegratedRiskLevel.SAFE:      85.0,
        IntegratedRiskLevel.MODERATE:  60.0,
        IntegratedRiskLevel.HIGH:      25.0,
        IntegratedRiskLevel.BLOCKED:    0.0,
    }
    return _map.get(level, 0.0)


def _behavior_base_score(status: IntegratedBehaviorStatus) -> float:
    _map = {
        IntegratedBehaviorStatus.CLEAN:    90.0,
        IntegratedBehaviorStatus.CAUTION:  60.0,
        IntegratedBehaviorStatus.WARNING:  30.0,
        IntegratedBehaviorStatus.BLOCKED:   0.0,
    }
    return _map.get(status, 0.0)


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def compute_scorecard(inp: IntegratedStrategyInput) -> IntegratedScorecard:
    """Compute integrated scorecard from all subsystem inputs."""
    # Use provided scores if non-zero, else derive from status enums
    theme_s    = _clamp(inp.theme_score    if inp.theme_score    > 0 else _theme_base_score(inp.theme_status))
    watchlist_s = _clamp(inp.watchlist_score if inp.watchlist_score > 0 else _watchlist_base_score(inp.watchlist_status))
    abc_s      = _clamp(inp.abc_score      if inp.abc_score      > 0 else _abc_base_score(inp.abc_status))
    regime_s   = _clamp(inp.regime_score   if inp.regime_score   > 0 else _regime_base_score(inp.regime_status))
    risk_s     = _clamp(inp.risk_score     if inp.risk_score     > 0 else _risk_base_score(inp.risk_level))
    behavior_s = _clamp(inp.behavior_score if inp.behavior_score > 0 else _behavior_base_score(inp.behavior_status))
    journal_s  = _clamp(inp.journal_quality_score)

    # Hard overrides
    if inp.watchlist_status == IntegratedWatchlistStatus.EXCLUDED:
        watchlist_s = 0.0
    if inp.theme_status == IntegratedThemeStatus.EXCLUDED:
        theme_s = 0.0
    if inp.abc_status == IntegratedABCStatus.BLOCKED:
        abc_s = 0.0
    if inp.risk_level == IntegratedRiskLevel.BLOCKED:
        risk_s = 0.0
    if inp.behavior_status == IntegratedBehaviorStatus.BLOCKED:
        behavior_s = 0.0
    if inp.regime_status == IntegratedRegimeStatus.RISK_OFF and not inp.regime_safety_override:
        regime_s = min(regime_s, 10.0)

    final_s = (
        theme_s    * _WEIGHT_THEME
        + watchlist_s * _WEIGHT_WATCHLIST
        + abc_s      * _WEIGHT_ABC
        + regime_s   * _WEIGHT_REGIME
        + risk_s     * _WEIGHT_RISK
        + behavior_s * _WEIGHT_BEHAVIOR
        + journal_s  * _WEIGHT_JOURNAL
    )
    final_s = _clamp(final_s)
    grade = score_to_grade(final_s)

    return IntegratedScorecard(
        symbol=inp.symbol,
        date=inp.date,
        theme_score=round(theme_s, 2),
        watchlist_score=round(watchlist_s, 2),
        abc_score=round(abc_s, 2),
        regime_score=round(regime_s, 2),
        risk_score=round(risk_s, 2),
        behavior_score=round(behavior_s, 2),
        journal_quality_score=round(journal_s, 2),
        final_score=round(final_s, 2),
        grade=grade,
    )
