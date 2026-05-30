"""
backtest/portfolio_rules.py - Portfolio rule engine for position management (v0.3.12).

Handles:
  - Position limits (max_positions)
  - Sector exposure limits (max_sector_exposure_pct)
  - Entry conditions (rank_score, entry_allowed, cash)
  - Stop loss (fixed)
  - Half take-profit
  - Trailing stop
  - Candidate ranking / scoring

Weights for portfolio_rank_score:
  0.30 * bull_stock_score
  0.20 * buy_point_score
  0.20 * strategy_knowledge_score
  0.15 * fundamental_quality_score
  0.10 * microstructure_score
  0.05 * sector_strength_score
  - warnings_penalty

Penalties:
  no_chase_warning       -8
  fake_breakout_risk     -8
  fundamental_warning    -6
  overvalued_warning     -6
  timing_estimated       -3
  sector_concentration   -4
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class PortfolioRules:
    """Encapsulates all portfolio entry/exit/sizing rules."""

    # Penalty weights
    PENALTY_NO_CHASE         = 8
    PENALTY_FAKE_BREAKOUT    = 8
    PENALTY_FUNDAMENTAL_WARN = 6
    PENALTY_OVERVALUED       = 6
    PENALTY_TIMING_ESTIMATED = 3
    PENALTY_SECTOR_CONC      = 4

    # Minimum rank score to consider entry
    ENTRY_SCORE_THRESHOLD = 40.0

    def __init__(
        self,
        max_positions: int = 5,
        position_size_pct: float = 0.20,
        max_sector_exposure_pct: float = 0.50,
        stop_loss_pct: float = 0.08,
        take_profit_pct: float = 0.20,
        trailing_stop_pct: float = 0.10,
        use_half_take_profit: bool = True,
        use_score_ranking: bool = True,
        use_fundamental_filter: bool = True,
        use_strategy_knowledge_filter: bool = True,
        rule_weight_config: Optional[Any] = None,  # v0.3.15: RuleWeightConfig or None
    ):
        self.max_positions            = max_positions
        self.position_size_pct        = position_size_pct
        self.max_sector_exposure_pct  = max_sector_exposure_pct
        self.stop_loss_pct            = stop_loss_pct
        self.take_profit_pct          = take_profit_pct
        self.trailing_stop_pct        = trailing_stop_pct
        self.use_half_take_profit     = use_half_take_profit
        self.use_score_ranking        = use_score_ranking
        self.use_fundamental_filter   = use_fundamental_filter
        self.use_strategy_knowledge_filter = use_strategy_knowledge_filter
        self.rule_weight_config       = rule_weight_config  # v0.3.15

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def score_candidate(self, candidate: dict) -> float:
        """
        Compute portfolio_rank_score for a candidate signal dict.

        Expects keys (all optional, default 50):
          bull_stock_score, buy_point_score, strategy_knowledge_score,
          fundamental_quality_score, microstructure_score, sector_strength_score,
          no_chase_warning, fake_breakout_risk, fundamental_warning,
          overvalued_warning, timing_estimated, sector_concentration_warning
        """
        def _g(key, default=50.0):
            v = candidate.get(key)
            try:
                return float(v) if v is not None else default
            except (TypeError, ValueError):
                return default

        # v0.3.15: use configurable weights when rule_weight_config is provided
        cfg = self.rule_weight_config
        if cfg is not None:
            score = (
                cfg.bull_stock_weight          * _g('bull_stock_score')
                + cfg.buy_point_weight         * _g('buy_point_score')
                + cfg.strategy_knowledge_weight * _g('strategy_knowledge_score')
                + cfg.fundamental_weight       * _g('fundamental_quality_score')
                + cfg.intraday_weight          * _g('microstructure_score')
                + cfg.sector_strength_weight   * _g('sector_strength_score')
            )
        else:
            score = (
                0.30 * _g('bull_stock_score')
                + 0.20 * _g('buy_point_score')
                + 0.20 * _g('strategy_knowledge_score')
                + 0.15 * _g('fundamental_quality_score')
                + 0.10 * _g('microstructure_score')
                + 0.05 * _g('sector_strength_score')
            )

        # Penalties — use config values if available, else class-level constants
        p_no_chase    = cfg.penalty_no_chase         if cfg is not None else self.PENALTY_NO_CHASE
        p_fake        = cfg.penalty_fake_breakout    if cfg is not None else self.PENALTY_FAKE_BREAKOUT
        p_fund        = cfg.penalty_fundamental_warn if cfg is not None else self.PENALTY_FUNDAMENTAL_WARN
        p_ov          = cfg.penalty_overvalued       if cfg is not None else self.PENALTY_OVERVALUED
        p_timing      = cfg.penalty_timing_estimated if cfg is not None else self.PENALTY_TIMING_ESTIMATED
        p_sector      = cfg.penalty_sector_conc      if cfg is not None else self.PENALTY_SECTOR_CONC

        if candidate.get('no_chase_warning'):
            score -= p_no_chase
        if candidate.get('fake_breakout_risk'):
            score -= p_fake
        if candidate.get('fundamental_warning'):
            score -= p_fund
        if candidate.get('overvalued_warning'):
            score -= p_ov
        if candidate.get('timing_estimated'):
            score -= p_timing
        if candidate.get('sector_concentration_warning'):
            score -= p_sector

        return round(score, 2)

    def rank_candidates(self, candidates: list) -> list:
        """
        Assign portfolio_rank_score to each candidate, sort descending.
        Candidates without an existing rank_score get it computed here.
        """
        for c in candidates:
            if 'portfolio_rank_score' not in c or c.get('portfolio_rank_score') is None:
                c['portfolio_rank_score'] = self.score_candidate(c)
        return sorted(candidates, key=lambda x: x.get('portfolio_rank_score', 0), reverse=True)

    # ------------------------------------------------------------------
    # Entry conditions
    # ------------------------------------------------------------------

    def can_enter_position(
        self,
        candidate: dict,
        current_positions: Dict[str, dict],
        portfolio_equity: float,
        cash: float,
    ) -> tuple:
        """
        Evaluate whether a new position can be opened.

        Returns (allowed: bool, reasons: list[str]).
        """
        reasons = []
        sym = candidate.get('symbol', '?')

        # Already in position
        if sym in current_positions:
            return False, ['already_in_position']

        # Position limit
        if self.check_position_limit(current_positions):
            reasons.append(f'max_positions_reached ({self.max_positions})')
            return False, reasons

        # Score threshold
        score = candidate.get('portfolio_rank_score', 0)
        if score < self.ENTRY_SCORE_THRESHOLD:
            reasons.append(f'rank_score_too_low ({score:.1f} < {self.ENTRY_SCORE_THRESHOLD})')
            return False, reasons

        # Entry allowed flag
        if not candidate.get('entry_allowed', True):
            reasons.append('entry_allowed=False')
            return False, reasons

        # No-chase filter
        if self.use_strategy_knowledge_filter and candidate.get('no_chase_warning'):
            reasons.append('no_chase_warning')
            return False, reasons

        # Cash check
        required = portfolio_equity * self.position_size_pct
        if cash < required * 0.9:  # 10% tolerance
            reasons.append(f'insufficient_cash ({cash:.0f} < {required:.0f})')
            return False, reasons

        # Sector limit
        sector = candidate.get('sector', 'GENERAL')
        if self.check_sector_limit(sector, current_positions, portfolio_equity):
            reasons.append(f'sector_exposure_exceeded ({sector})')
            return False, reasons

        return True, []

    def check_position_limit(self, current_positions: dict) -> bool:
        """True if max positions already reached."""
        return len(current_positions) >= self.max_positions

    def check_sector_limit(
        self,
        sector: str,
        current_positions: Dict[str, dict],
        portfolio_equity: float,
    ) -> bool:
        """
        True if adding a new position in `sector` would exceed max_sector_exposure_pct.
        """
        if portfolio_equity <= 0:
            return False
        sector_value = sum(
            p.get('current_value', p.get('entry_value', 0))
            for p in current_positions.values()
            if p.get('sector', 'GENERAL') == sector
        )
        # Adding position_size_pct worth
        new_exposure = (sector_value + portfolio_equity * self.position_size_pct) / portfolio_equity
        return new_exposure > self.max_sector_exposure_pct

    # ------------------------------------------------------------------
    # Exit conditions
    # ------------------------------------------------------------------

    def should_exit_position(
        self,
        position: dict,
        current_price: float,
    ) -> tuple:
        """
        Check fixed stop loss for the position.

        Returns (should_exit: bool, reason: str).
        """
        entry_price = position.get('entry_price', 0)
        if entry_price <= 0 or current_price <= 0:
            return False, ''

        # Fixed stop loss
        stop_price = entry_price * (1 - self.stop_loss_pct)
        if current_price <= stop_price:
            return True, 'STOP_LOSS'

        # Trailing stop (if half already taken)
        if position.get('half_taken'):
            trailing_stop = position.get('trailing_stop_price', 0)
            if trailing_stop > 0 and current_price <= trailing_stop:
                return True, 'TRAILING_STOP'

        return False, ''

    def should_take_profit_half(
        self,
        position: dict,
        current_price: float,
    ) -> bool:
        """
        True if price has reached take-profit level AND we haven't taken half yet.
        """
        if not self.use_half_take_profit:
            return False
        if position.get('half_taken'):
            return False
        entry_price = position.get('entry_price', 0)
        if entry_price <= 0:
            return False
        return current_price >= entry_price * (1 + self.take_profit_pct)

    def update_trailing_stop(
        self,
        position: dict,
        current_price: float,
    ) -> dict:
        """
        Update peak_price and trailing_stop_price for a position with half_taken=True.
        Returns the updated position dict.
        """
        if not position.get('half_taken'):
            return position
        position = position.copy()
        peak = position.get('peak_price', position.get('entry_price', current_price))
        if current_price > peak:
            peak = current_price
            position['peak_price'] = peak
            position['trailing_stop_price'] = round(peak * (1 - self.trailing_stop_pct), 4)
        return position
