"""
abc_validation/parameters_v141.py — Validation parameters for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
All params have safe defaults, bounds, units, and are snapshot-savable.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional


@dataclass
class APointParameters:
    """Parameters for A buy point (MA10 pullback)."""
    # Bounds and units documented inline
    ma10_touch_tolerance: float = 0.01      # fraction; 0.01 = 1%
    max_breach_pct: float = 0.02            # fraction; max allowed breach below MA10
    recovery_window: int = 3                # trading days
    vol_contraction_ratio: float = 0.7      # ratio vs 20d avg; <1 = contraction
    kd_low_threshold: float = 30.0          # KD stochastic K value
    institutional_sell_limit: float = -2000.0  # net lots; < 0 = net selling
    trend_requirement: str = "MA60_UP"      # "MA60_UP", "ANY", "NONE"

    def validate(self) -> None:
        assert 0 < self.ma10_touch_tolerance < 0.1, "ma10_touch_tolerance out of bounds"
        assert 0 < self.max_breach_pct < 0.1, "max_breach_pct out of bounds"
        assert 1 <= self.recovery_window <= 10, "recovery_window out of bounds"
        assert 0 < self.vol_contraction_ratio < 2.0, "vol_contraction_ratio out of bounds"
        assert 0 <= self.kd_low_threshold <= 100, "kd_low_threshold out of bounds"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BPointParameters:
    """Parameters for B buy point (MA5 + VWAP)."""
    ma5_touch_tolerance: float = 0.005      # fraction
    max_breach_pct: float = 0.01            # fraction
    recovery_window: int = 2                # trading days
    vol_contraction_ratio: float = 0.8      # ratio vs 5d avg
    overextension_limit: float = 0.05       # fraction above MA5; >limit = overextended
    short_term_trend_requirement: str = "MA10_UP"  # "MA10_UP", "MA20_UP", "ANY"

    def validate(self) -> None:
        assert 0 < self.ma5_touch_tolerance < 0.1, "ma5_touch_tolerance out of bounds"
        assert 0 < self.max_breach_pct < 0.1, "max_breach_pct out of bounds"
        assert 1 <= self.recovery_window <= 5, "recovery_window out of bounds"
        assert 0 < self.vol_contraction_ratio < 2.0, "vol_contraction_ratio out of bounds"
        assert 0 < self.overextension_limit < 0.2, "overextension_limit out of bounds"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CPointParameters:
    """Parameters for C buy point (MA20 reclaim)."""
    ma20_reclaim_tolerance: float = 0.005   # fraction
    min_close_above_ma20: int = 1           # consecutive bars closing above MA20
    confirmation_bars: int = 2              # bars to confirm reclaim
    vol_confirmation_ratio: float = 1.2     # ratio vs 20d avg; >1 = expansion
    kd_turn_requirement: bool = True        # KD must turn up
    rsi_recovery_threshold: float = 40.0   # RSI must be >= threshold
    macd_improvement_requirement: bool = True  # MACD histogram must improve

    def validate(self) -> None:
        assert 0 < self.ma20_reclaim_tolerance < 0.1, "ma20_reclaim_tolerance out of bounds"
        assert 1 <= self.min_close_above_ma20 <= 5, "min_close_above_ma20 out of bounds"
        assert 1 <= self.confirmation_bars <= 10, "confirmation_bars out of bounds"
        assert 0 < self.vol_confirmation_ratio < 5.0, "vol_confirmation_ratio out of bounds"
        assert 0 <= self.rsi_recovery_threshold <= 100, "rsi_recovery_threshold out of bounds"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ABCValidationParameters:
    """Combined parameters for A/B/C buy point validation."""
    a_params: APointParameters = field(default_factory=APointParameters)
    b_params: BPointParameters = field(default_factory=BPointParameters)
    c_params: CPointParameters = field(default_factory=CPointParameters)

    def validate(self) -> None:
        self.a_params.validate()
        self.b_params.validate()
        self.c_params.validate()

    def to_dict(self) -> dict:
        return {
            "a_params": self.a_params.to_dict(),
            "b_params": self.b_params.to_dict(),
            "c_params": self.c_params.to_dict(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ABCValidationParameters":
        a = APointParameters(**{k: v for k, v in d.get("a_params", {}).items()
                                if k in APointParameters.__dataclass_fields__})
        b = BPointParameters(**{k: v for k, v in d.get("b_params", {}).items()
                                if k in BPointParameters.__dataclass_fields__})
        c = CPointParameters(**{k: v for k, v in d.get("c_params", {}).items()
                                if k in CPointParameters.__dataclass_fields__})
        return cls(a_params=a, b_params=b, c_params=c)
