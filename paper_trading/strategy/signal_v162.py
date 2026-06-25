"""
paper_trading/strategy/signal_v162.py — Signal creation helpers for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, Dict, Optional

from paper_trading.strategy.enums_v162 import SignalStrength, SignalType, TriggerType
from paper_trading.strategy.models_v162 import PaperSignal, _new_id, _now_iso

logger = logging.getLogger(__name__)

_FORBIDDEN_SIGNAL_TYPES = {"ENTRY_SHORT", "SELL_SHORT", "MARGIN_LONG", "MARGIN_SHORT"}


def make_signal(
    strategy_id: str,
    ticker: str,
    signal_type: SignalType,
    confidence: float = 0.5,
    strength: SignalStrength = SignalStrength.NEUTRAL,
    raw_value: Optional[float] = None,
    trigger_type: TriggerType = TriggerType.MANUAL,
    metadata: Optional[Dict[str, Any]] = None,
) -> PaperSignal:
    """
    Create a validated PaperSignal.
    Raises ValueError for forbidden signal types (SHORT/MARGIN).
    """
    if signal_type.value in _FORBIDDEN_SIGNAL_TYPES:
        raise ValueError(f"Signal type permanently forbidden: {signal_type.value}")
    if not (0.0 <= confidence <= 1.0):
        raise ValueError(f"confidence must be in [0.0, 1.0], got {confidence}")

    sig_id = _new_id()
    dedup_key = _compute_dedup_key(strategy_id, ticker, signal_type.value)

    return PaperSignal(
        signal_id=sig_id,
        strategy_id=strategy_id,
        ticker=ticker,
        signal_type=signal_type.value,
        strength=strength.value,
        confidence=confidence,
        raw_value=raw_value,
        normalized_value=None,   # set by normalizer
        generated_at=_now_iso(),
        trigger_type=trigger_type.value,
        metadata=metadata or {},
        is_duplicate=False,
        dedup_key=dedup_key,
        paper_only=True,
        research_only=True,
        not_a_real_order=True,
    )


def make_entry_long(
    strategy_id: str,
    ticker: str,
    confidence: float = 0.5,
    strength: SignalStrength = SignalStrength.MODERATE,
    raw_value: Optional[float] = None,
    trigger_type: TriggerType = TriggerType.MANUAL,
    metadata: Optional[Dict[str, Any]] = None,
) -> PaperSignal:
    return make_signal(
        strategy_id=strategy_id,
        ticker=ticker,
        signal_type=SignalType.ENTRY_LONG,
        confidence=confidence,
        strength=strength,
        raw_value=raw_value,
        trigger_type=trigger_type,
        metadata=metadata,
    )


def make_exit_long(
    strategy_id: str,
    ticker: str,
    confidence: float = 0.7,
    strength: SignalStrength = SignalStrength.MODERATE,
    raw_value: Optional[float] = None,
    trigger_type: TriggerType = TriggerType.MANUAL,
    metadata: Optional[Dict[str, Any]] = None,
) -> PaperSignal:
    return make_signal(
        strategy_id=strategy_id,
        ticker=ticker,
        signal_type=SignalType.EXIT_LONG,
        confidence=confidence,
        strength=strength,
        raw_value=raw_value,
        trigger_type=trigger_type,
        metadata=metadata,
    )


def make_hold(
    strategy_id: str,
    ticker: str,
    trigger_type: TriggerType = TriggerType.MANUAL,
) -> PaperSignal:
    return make_signal(
        strategy_id=strategy_id,
        ticker=ticker,
        signal_type=SignalType.HOLD,
        confidence=0.5,
        strength=SignalStrength.NEUTRAL,
        trigger_type=trigger_type,
    )


def make_block(
    strategy_id: str,
    ticker: str,
    reason: str = "",
    trigger_type: TriggerType = TriggerType.MANUAL,
) -> PaperSignal:
    return make_signal(
        strategy_id=strategy_id,
        ticker=ticker,
        signal_type=SignalType.BLOCK,
        confidence=1.0,
        strength=SignalStrength.STRONG,
        trigger_type=trigger_type,
        metadata={"reason": reason},
    )


def make_alert(
    strategy_id: str,
    ticker: str,
    message: str = "",
    trigger_type: TriggerType = TriggerType.MANUAL,
) -> PaperSignal:
    return make_signal(
        strategy_id=strategy_id,
        ticker=ticker,
        signal_type=SignalType.ALERT,
        confidence=0.5,
        strength=SignalStrength.NEUTRAL,
        trigger_type=trigger_type,
        metadata={"message": message},
    )


def _compute_dedup_key(strategy_id: str, ticker: str, signal_type: str) -> str:
    """Compute a deduplication key for a signal (strategy + ticker + type)."""
    raw = json.dumps({"s": strategy_id, "t": ticker, "st": signal_type}, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def signal_to_dict(signal: PaperSignal) -> Dict[str, Any]:
    """Serialize a PaperSignal to a plain dict."""
    return {
        "signal_id": signal.signal_id,
        "strategy_id": signal.strategy_id,
        "ticker": signal.ticker,
        "signal_type": signal.signal_type,
        "strength": signal.strength,
        "confidence": signal.confidence,
        "raw_value": signal.raw_value,
        "normalized_value": signal.normalized_value,
        "generated_at": signal.generated_at,
        "trigger_type": signal.trigger_type,
        "metadata": signal.metadata,
        "is_duplicate": signal.is_duplicate,
        "dedup_key": signal.dedup_key,
        "paper_only": signal.paper_only,
        "research_only": signal.research_only,
        "not_a_real_order": signal.not_a_real_order,
    }
