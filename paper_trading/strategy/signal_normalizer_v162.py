"""
paper_trading/strategy/signal_normalizer_v162.py — Signal normalization for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
import math
from typing import List, Optional

from paper_trading.strategy.enums_v162 import SignalStrength, SignalType
from paper_trading.strategy.models_v162 import PaperSignal

logger = logging.getLogger(__name__)

# Strength → normalized value mapping
_STRENGTH_TO_NORMALIZED = {
    SignalStrength.STRONG.value:   1.0,
    SignalStrength.MODERATE.value: 0.65,
    SignalStrength.WEAK.value:     0.35,
    SignalStrength.NEUTRAL.value:  0.0,
}

# Signal type polarity for normalization
_SIGNAL_POLARITY = {
    SignalType.ENTRY_LONG.value:      +1.0,
    SignalType.EXIT_LONG.value:       -1.0,
    SignalType.HOLD.value:             0.0,
    SignalType.REDUCE_RESEARCH.value: -0.5,
    SignalType.BLOCK.value:           -1.0,
    SignalType.ALERT.value:            0.0,
}


class SignalNormalizer:
    """
    Normalizes raw signal values to [-1.0, 1.0] range.

    Normalization formula:
      normalized = polarity * strength_base * confidence

    Where:
      - polarity: +1 for long, -1 for exit/block, 0 for hold/alert
      - strength_base: [0.0, 1.0] from SignalStrength
      - confidence: [0.0, 1.0] from signal
    """

    def normalize(self, signal: PaperSignal) -> PaperSignal:
        """
        Compute normalized_value for a signal in-place. Returns the signal.
        Does NOT mutate signal_type, strength, or confidence.
        """
        polarity = _SIGNAL_POLARITY.get(signal.signal_type, 0.0)
        strength_base = _STRENGTH_TO_NORMALIZED.get(signal.strength, 0.0)
        normalized = polarity * strength_base * signal.confidence

        # Clamp to [-1.0, 1.0] to handle float edge cases
        normalized = max(-1.0, min(1.0, normalized))

        # Round to 6 dp for stability
        signal.normalized_value = round(normalized, 6)

        logger.debug(
            "[v1.6.2][normalizer] %s/%s normalized=%.4f (polarity=%.1f str=%.2f conf=%.2f)",
            signal.ticker, signal.signal_type,
            signal.normalized_value, polarity, strength_base, signal.confidence,
        )
        return signal

    def normalize_batch(self, signals: List[PaperSignal]) -> List[PaperSignal]:
        """Normalize a list of signals. Returns the same list (mutated in-place)."""
        for sig in signals:
            self.normalize(sig)
        return signals

    @staticmethod
    def normalized_to_strength(value: float) -> str:
        """Convert a normalized value back to a SignalStrength label."""
        abs_val = abs(value)
        if abs_val >= 0.8:
            return SignalStrength.STRONG.value
        if abs_val >= 0.5:
            return SignalStrength.MODERATE.value
        if abs_val >= 0.2:
            return SignalStrength.WEAK.value
        return SignalStrength.NEUTRAL.value
