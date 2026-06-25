"""
paper_trading/strategy/replay_v162.py — Signal replay for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Optional

from paper_trading.strategy.enums_v162 import SignalType, TriggerType
from paper_trading.strategy.models_v162 import PaperSignal, _new_id, _now_iso

logger = logging.getLogger(__name__)


class ReplaySession:
    """
    Replays a recorded sequence of paper signals through the strategy pipeline.

    Use cases:
      - Reproduce a past decision for debugging
      - Validate determinism of the decision pipeline
      - Stress-test the pipeline with historical signal sequences

    [!] All replayed signals are paper-only. No real orders are placed.
    [!] Replay does NOT connect to any broker or live data feed.
    """

    def __init__(
        self,
        strategy_id: str,
        signals: List[PaperSignal],
        replay_handler: Optional[Callable[[PaperSignal], Any]] = None,
    ) -> None:
        self.session_id = _new_id()
        self.strategy_id = strategy_id
        self._signals = [self._validate_signal(s) for s in signals]
        self._handler = replay_handler
        self._cursor: int = 0
        self._replayed: int = 0
        self._errors: int = 0
        self._started_at: Optional[str] = None
        self._completed_at: Optional[str] = None
        self._complete: bool = False

    @staticmethod
    def _validate_signal(signal: PaperSignal) -> PaperSignal:
        """Ensure replayed signal has correct safety flags and trigger type."""
        assert signal.paper_only is True, "Replay signal must be paper_only"
        assert signal.not_a_real_order is True, "Replay signal must be not_a_real_order"
        forbidden = {"ENTRY_SHORT", "SELL_SHORT", "MARGIN_LONG", "MARGIN_SHORT"}
        assert signal.signal_type not in forbidden, f"Forbidden signal type: {signal.signal_type}"
        # Override trigger type to REPLAY for audit clarity
        signal.trigger_type = TriggerType.REPLAY.value
        return signal

    def has_next(self) -> bool:
        return self._cursor < len(self._signals)

    def next(self) -> Optional[PaperSignal]:
        """Return the next signal in the replay sequence, or None if exhausted."""
        if not self.has_next():
            return None
        signal = self._signals[self._cursor]
        self._cursor += 1
        return signal

    def run_all(self) -> Dict[str, Any]:
        """
        Run all signals through the registered handler.
        Returns a summary dict.
        """
        self._started_at = _now_iso()
        self._cursor = 0
        self._replayed = 0
        self._errors = 0

        if self._handler is None:
            logger.warning("[v1.6.2][replay] No handler registered — dry run")

        while self.has_next():
            signal = self.next()
            if signal is None:
                break
            try:
                if self._handler:
                    self._handler(signal)
                self._replayed += 1
            except Exception as exc:
                self._errors += 1
                logger.error(
                    "[v1.6.2][replay] Error on signal %s: %s",
                    signal.signal_id[:8], exc
                )

        self._complete = True
        self._completed_at = _now_iso()
        logger.info(
            "[v1.6.2][replay] Session %s complete: %d/%d replayed, %d errors",
            self.session_id[:8], self._replayed, len(self._signals), self._errors
        )
        return self.summary()

    def summary(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "strategy_id": self.strategy_id,
            "total_signals": len(self._signals),
            "replayed": self._replayed,
            "errors": self._errors,
            "cursor": self._cursor,
            "complete": self._complete,
            "started_at": self._started_at,
            "completed_at": self._completed_at,
            "paper_only": True,
            "research_only": True,
            "no_broker_call": True,
        }


def build_replay_session(
    strategy_id: str,
    raw_signal_dicts: List[Dict[str, Any]],
    handler: Optional[Callable[[PaperSignal], Any]] = None,
) -> ReplaySession:
    """
    Build a ReplaySession from a list of raw signal dicts (e.g. from journal).
    """
    from paper_trading.strategy.enums_v162 import SignalStrength
    signals: List[PaperSignal] = []
    for d in raw_signal_dicts:
        try:
            sig = PaperSignal(
                signal_id=d.get("signal_id", _new_id()),
                strategy_id=strategy_id,
                ticker=d.get("ticker", ""),
                signal_type=d.get("signal_type", SignalType.HOLD.value),
                strength=d.get("strength", SignalStrength.NEUTRAL.value),
                confidence=float(d.get("confidence", 0.5)),
                raw_value=d.get("raw_value"),
                normalized_value=d.get("normalized_value"),
                generated_at=d.get("generated_at", _now_iso()),
                trigger_type=TriggerType.REPLAY.value,
                metadata=d.get("metadata", {}),
                is_duplicate=False,
                dedup_key=d.get("dedup_key", ""),
                paper_only=True,
                research_only=True,
                not_a_real_order=True,
            )
            signals.append(sig)
        except Exception as exc:
            logger.warning("[v1.6.2][replay] Skipping invalid signal dict: %s", exc)
    return ReplaySession(strategy_id=strategy_id, signals=signals, replay_handler=handler)
