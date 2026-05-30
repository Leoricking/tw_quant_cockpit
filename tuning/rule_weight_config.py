"""
tuning/rule_weight_config.py - Scoring weight configuration dataclass (v0.3.15).

Maps each scoring component to a configurable weight so that different
portfolio_rank_score formulas can be tested without touching production code.

portfolio_rank_score (baseline) =
    0.30 * bull_stock_score
  + 0.20 * buy_point_score
  + 0.20 * strategy_knowledge_score
  + 0.15 * fundamental_quality_score
  + 0.10 * microstructure_score
  + 0.05 * sector_strength_score
  - warnings_penalty

[!] Advisory only. Never auto-applied to production strategy.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class RuleWeightConfig:
    """
    Configurable scoring weights for portfolio_rank_score.

    Weights do not have to sum to exactly 1.0 — the scoring formula
    multiplies each sub-score (0-100 scale) by its weight, so the
    practical range of scores scales with the sum of weights.
    Baseline sum = 1.00.
    """

    name: str = "custom"
    description: str = ""

    # ── Signal weights ────────────────────────────────────────────────────
    bull_stock_weight: float = 0.30          # Screener / bull_stock_score
    buy_point_weight: float = 0.20           # Buy-point A/B/C grade
    strategy_knowledge_weight: float = 0.20  # Strategy Knowledge Engine
    fundamental_weight: float = 0.15         # Fundamental quality
    intraday_weight: float = 0.10            # Microstructure / intraday
    sector_strength_weight: float = 0.05     # Sector rotation signal

    # ── Penalty weights (subtracted from score; must be >= 0) ─────────────
    penalty_no_chase: float = 8.0
    penalty_fake_breakout: float = 8.0
    penalty_fundamental_warn: float = 6.0
    penalty_overvalued: float = 6.0
    penalty_timing_estimated: float = 3.0
    penalty_sector_conc: float = 4.0

    # ── Metadata ─────────────────────────────────────────────────────────
    source: str = "manual"           # 'manual' | 'signal_quality_csv' | 'preset'
    version: str = "v0.3.15"

    def weight_sum(self) -> float:
        """Sum of all signal weights (baseline = 1.0)."""
        return round(
            self.bull_stock_weight
            + self.buy_point_weight
            + self.strategy_knowledge_weight
            + self.fundamental_weight
            + self.intraday_weight
            + self.sector_strength_weight,
            6,
        )

    def to_dict(self) -> Dict:
        return {
            "name":                        self.name,
            "description":                 self.description,
            "bull_stock_weight":           self.bull_stock_weight,
            "buy_point_weight":            self.buy_point_weight,
            "strategy_knowledge_weight":   self.strategy_knowledge_weight,
            "fundamental_weight":          self.fundamental_weight,
            "intraday_weight":             self.intraday_weight,
            "sector_strength_weight":      self.sector_strength_weight,
            "penalty_no_chase":            self.penalty_no_chase,
            "penalty_fake_breakout":       self.penalty_fake_breakout,
            "penalty_fundamental_warn":    self.penalty_fundamental_warn,
            "penalty_overvalued":          self.penalty_overvalued,
            "penalty_timing_estimated":    self.penalty_timing_estimated,
            "penalty_sector_conc":         self.penalty_sector_conc,
            "source":                      self.source,
            "version":                     self.version,
            "weight_sum":                  self.weight_sum(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RuleWeightConfig":
        valid = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in valid})
