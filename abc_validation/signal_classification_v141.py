"""
abc_validation/signal_classification_v141.py — Signal classification for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class ABCSignalClassification:
    """Signal classification constants for A/B/C buy points."""

    # A Buy Point (MA10 pullback)
    A_STRICT            = "A_STRICT"
    A_RELAXED           = "A_RELAXED"
    A_FAILED_SUPPORT    = "A_FAILED_SUPPORT"
    A_INSUFFICIENT_DATA = "A_INSUFFICIENT_DATA"

    # B Buy Point (MA5 + VWAP)
    B_STRICT             = "B_STRICT"
    B_RELAXED            = "B_RELAXED"
    B_OVEREXTENDED       = "B_OVEREXTENDED"
    B_FAILED_SUPPORT     = "B_FAILED_SUPPORT"
    B_INSUFFICIENT_DATA  = "B_INSUFFICIENT_DATA"

    # C Buy Point (MA20 reclaim)
    C_STRICT_RECLAIM    = "C_STRICT_RECLAIM"
    C_WEAK_RECLAIM      = "C_WEAK_RECLAIM"
    C_FALSE_RECLAIM     = "C_FALSE_RECLAIM"
    C_NO_CONFIRMATION   = "C_NO_CONFIRMATION"
    C_INSUFFICIENT_DATA = "C_INSUFFICIENT_DATA"

    # Blocked
    BLOCKED = "BLOCKED"

    @classmethod
    def all_a(cls) -> List[str]:
        return [cls.A_STRICT, cls.A_RELAXED, cls.A_FAILED_SUPPORT, cls.A_INSUFFICIENT_DATA]

    @classmethod
    def all_b(cls) -> List[str]:
        return [cls.B_STRICT, cls.B_RELAXED, cls.B_OVEREXTENDED, cls.B_FAILED_SUPPORT, cls.B_INSUFFICIENT_DATA]

    @classmethod
    def all_c(cls) -> List[str]:
        return [cls.C_STRICT_RECLAIM, cls.C_WEAK_RECLAIM, cls.C_FALSE_RECLAIM,
                cls.C_NO_CONFIRMATION, cls.C_INSUFFICIENT_DATA]

    @classmethod
    def is_valid_for_type(cls, signal_type: str, buy_point_type: str) -> bool:
        if buy_point_type == "A":
            return signal_type in cls.all_a()
        if buy_point_type == "B":
            return signal_type in cls.all_b()
        if buy_point_type == "C":
            return signal_type in cls.all_c()
        return False


@dataclass
class ABCSignalRecord:
    """Record of a detected A/B/C buy point signal."""
    signal_id: str
    buy_point_type: str                  # "A", "B", "C"
    classification: str                  # ABCSignalClassification constant
    symbol: str
    signal_date: str
    decision_date: str
    execution_date: str
    entry_price: Optional[float] = None
    stop_loss_price: Optional[float] = None
    target_price: Optional[float] = None
    support_ma_value: Optional[float] = None
    volume_ratio: Optional[float] = None
    kd_value: Optional[float] = None
    rsi_value: Optional[float] = None
    macd_value: Optional[float] = None
    foreign_net: Optional[float] = None
    trust_net: Optional[float] = None
    margin_balance: Optional[float] = None
    regime: Optional[str] = None
    is_second_wave: bool = False
    data_quality: str = "UNKNOWN"
    lookahead_safe: bool = True
    corporate_action_clean: bool = True
    fixture_data: bool = False
    formal_conclusion_allowed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def validate_fixture_mode(self, mode: str) -> None:
        """Block fixture data in real mode."""
        if mode == 'real' and self.fixture_data:
            raise ValueError(
                f"BLOCKED: fixture data cannot be used in real mode for signal {self.signal_id}"
            )
