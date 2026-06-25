"""
paper_trading/strategy/strategy_base_v162.py — Abstract base class for paper strategies v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import abc
import logging
from typing import List, Optional

from paper_trading.strategy.enums_v162 import StrategyStatus, SignalType
from paper_trading.strategy.models_v162 import (
    PaperSignal,
    StrategyConfig,
    StrategyMetadata,
    _now_iso,
)

logger = logging.getLogger(__name__)


class PaperStrategyBase(abc.ABC):
    """
    Abstract base for all paper strategy implementations.

    Subclasses must implement:
      - generate_signals()      → List[PaperSignal]
      - on_start()              → None
      - on_pause()              → None
      - on_halt()               → None
      - describe()              → str

    Safety contract:
      - All generated signals MUST have paper_only=True, research_only=True,
        not_a_real_order=True, and signal_type in SignalType (no SHORT/MARGIN).
      - Subclasses MUST NOT call any broker API or write to real portfolio ledgers.
    """

    # Class-level safety labels — subclasses must not override these to False
    PAPER_ONLY: bool = True
    RESEARCH_ONLY: bool = True
    SIMULATION_ONLY: bool = True
    NOT_A_REAL_ORDER: bool = True
    NO_BROKER_CALL: bool = True
    NO_REAL_ACCOUNT: bool = True

    def __init__(self, config: StrategyConfig) -> None:
        assert config.paper_only is True, "Config must have paper_only=True"
        assert config.research_only is True, "Config must have research_only=True"
        self._config = config
        self._metadata = StrategyMetadata(strategy_id=config.strategy_id)
        self._status = StrategyStatus.REGISTERED

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def config(self) -> StrategyConfig:
        return self._config

    @property
    def strategy_id(self) -> str:
        return self._config.strategy_id

    @property
    def strategy_name(self) -> str:
        return self._config.strategy_name

    @property
    def status(self) -> StrategyStatus:
        return self._status

    @property
    def metadata(self) -> StrategyMetadata:
        return self._metadata

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        logger.info("[v1.6.2] Strategy %s starting (PAPER_ONLY)", self.strategy_id)
        self._status = StrategyStatus.RUNNING
        self._metadata.status = StrategyStatus.RUNNING
        self._metadata.started_at = _now_iso()
        self.on_start()

    def pause(self) -> None:
        logger.info("[v1.6.2] Strategy %s pausing", self.strategy_id)
        self._status = StrategyStatus.PAUSED
        self._metadata.status = StrategyStatus.PAUSED
        self._metadata.paused_at = _now_iso()
        self.on_pause()

    def halt(self) -> None:
        logger.info("[v1.6.2] Strategy %s halting", self.strategy_id)
        self._status = StrategyStatus.HALTED
        self._metadata.status = StrategyStatus.HALTED
        self._metadata.halted_at = _now_iso()
        self.on_halt()

    def complete(self) -> None:
        self._status = StrategyStatus.COMPLETED
        self._metadata.status = StrategyStatus.COMPLETED
        self._metadata.completed_at = _now_iso()

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abc.abstractmethod
    def generate_signals(self) -> List[PaperSignal]:
        """
        Produce zero or more paper-only trading signals.
        Must never produce ENTRY_SHORT or SELL_SHORT signals.
        """

    @abc.abstractmethod
    def on_start(self) -> None:
        """Called when the strategy transitions to RUNNING."""

    @abc.abstractmethod
    def on_pause(self) -> None:
        """Called when the strategy transitions to PAUSED."""

    @abc.abstractmethod
    def on_halt(self) -> None:
        """Called when the strategy transitions to HALTED."""

    @abc.abstractmethod
    def describe(self) -> str:
        """Return a human-readable description of this strategy."""

    # ------------------------------------------------------------------
    # Safety helpers
    # ------------------------------------------------------------------

    def _assert_signal_safety(self, signal: PaperSignal) -> None:
        """Raise AssertionError if the signal violates safety invariants."""
        assert signal.paper_only is True, "Signal must have paper_only=True"
        assert signal.research_only is True, "Signal must have research_only=True"
        assert signal.not_a_real_order is True, "Signal must have not_a_real_order=True"
        forbidden = {"ENTRY_SHORT", "SELL_SHORT", "MARGIN_LONG", "MARGIN_SHORT"}
        assert signal.signal_type not in forbidden, (
            f"Forbidden signal_type: {signal.signal_type}"
        )
        allowed = {st.value for st in SignalType}
        assert signal.signal_type in allowed, f"Unknown signal_type: {signal.signal_type}"

    def safe_generate_signals(self) -> List[PaperSignal]:
        """
        Calls generate_signals() and validates every produced signal.
        Records signal count. Returns only safe signals.
        """
        raw = self.generate_signals()
        safe: List[PaperSignal] = []
        for sig in raw:
            try:
                self._assert_signal_safety(sig)
                safe.append(sig)
            except AssertionError as exc:
                logger.error(
                    "[v1.6.2] Strategy %s produced unsafe signal %s: %s",
                    self.strategy_id, sig.signal_id, exc
                )
                self._metadata.error_count += 1
        self._metadata.signal_count += len(safe)
        self._metadata.last_signal_at = _now_iso()
        return safe
