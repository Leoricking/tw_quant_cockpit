"""
paper_trading/strategy/strategy_lifecycle_v162.py — Lifecycle manager for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple

from paper_trading.strategy.enums_v162 import (
    JournalEventType,
    StrategyStatus,
)
from paper_trading.strategy.models_v162 import JournalEntry, StrategyConfig, _now_iso
from paper_trading.strategy.strategy_base_v162 import PaperStrategyBase
from paper_trading.strategy.strategy_registry_v162 import StrategyRegistry
from paper_trading.strategy.strategy_state_v162 import StrategyState

logger = logging.getLogger(__name__)


class StrategyLifecycleManager:
    """
    Manages the lifecycle of paper strategies: register → start → pause → halt → complete.

    Maintains per-strategy StrategyState instances.
    All strategies are research-only paper simulations.
    """

    def __init__(self, registry: StrategyRegistry) -> None:
        self._registry = registry
        self._states: Dict[str, StrategyState] = {}
        self._journal: List[JournalEntry] = []

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, strategy: PaperStrategyBase) -> str:
        """Register a strategy and create its runtime state. Returns strategy_id."""
        sid = self._registry.register(strategy)
        cfg = strategy.config
        state = StrategyState(
            strategy_id=sid,
            max_signals_per_minute=cfg.max_signals_per_minute,
            cooldown_seconds=cfg.cooldown_seconds,
            max_open_proposals=cfg.max_open_proposals,
        )
        self._states[sid] = state
        self._journal_event(
            sid, JournalEventType.STRATEGY_REGISTERED,
            f"Strategy '{strategy.strategy_name}' registered (PAPER_ONLY)"
        )
        logger.info("[v1.6.2][lifecycle] Registered strategy %s (%s)", sid, strategy.strategy_name)
        return sid

    # ------------------------------------------------------------------
    # Lifecycle transitions
    # ------------------------------------------------------------------

    def start(self, strategy_id: str) -> Tuple[bool, str]:
        """Start a registered strategy. Returns (ok, reason)."""
        strategy = self._registry.get(strategy_id)
        if strategy is None:
            return False, f"Strategy not found: {strategy_id}"
        state = self._states.get(strategy_id)
        if state is None:
            return False, f"State not found for: {strategy_id}"
        if strategy.status == StrategyStatus.RUNNING:
            return False, "Strategy already running"
        if strategy.status in (StrategyStatus.HALTED, StrategyStatus.COMPLETED,
                                StrategyStatus.RETIRED, StrategyStatus.FAILED):
            return False, f"Cannot start strategy in status: {strategy.status.value}"

        strategy.start()
        state.set_status(StrategyStatus.RUNNING)
        self._journal_event(strategy_id, JournalEventType.STRATEGY_STARTED,
                            "Strategy started (PAPER_ONLY. NO REAL ORDERS.)")
        return True, "started"

    def pause(self, strategy_id: str) -> Tuple[bool, str]:
        """Pause a running strategy."""
        strategy = self._registry.get(strategy_id)
        if strategy is None:
            return False, f"Strategy not found: {strategy_id}"
        if strategy.status != StrategyStatus.RUNNING:
            return False, f"Cannot pause strategy in status: {strategy.status.value}"
        strategy.pause()
        if strategy_id in self._states:
            self._states[strategy_id].set_status(StrategyStatus.PAUSED)
        self._journal_event(strategy_id, JournalEventType.STRATEGY_PAUSED, "Strategy paused")
        return True, "paused"

    def halt(self, strategy_id: str) -> Tuple[bool, str]:
        """Halt a strategy (irreversible without recovery)."""
        strategy = self._registry.get(strategy_id)
        if strategy is None:
            return False, f"Strategy not found: {strategy_id}"
        strategy.halt()
        if strategy_id in self._states:
            self._states[strategy_id].set_status(StrategyStatus.HALTED)
        self._journal_event(strategy_id, JournalEventType.STRATEGY_HALTED, "Strategy halted")
        return True, "halted"

    def complete(self, strategy_id: str) -> Tuple[bool, str]:
        """Mark a strategy as completed."""
        strategy = self._registry.get(strategy_id)
        if strategy is None:
            return False, f"Strategy not found: {strategy_id}"
        strategy.complete()
        if strategy_id in self._states:
            self._states[strategy_id].set_status(StrategyStatus.COMPLETED)
        self._journal_event(strategy_id, JournalEventType.STRATEGY_COMPLETED,
                            "Strategy completed")
        return True, "completed"

    def halt_all(self) -> int:
        """Halt all running strategies. Returns count halted."""
        count = self._registry.halt_all()
        for state in self._states.values():
            if state.status == StrategyStatus.RUNNING:
                state.set_status(StrategyStatus.HALTED)
        logger.info("[v1.6.2][lifecycle] Halted %d strategies", count)
        return count

    # ------------------------------------------------------------------
    # State access
    # ------------------------------------------------------------------

    def get_state(self, strategy_id: str) -> Optional[StrategyState]:
        return self._states.get(strategy_id)

    def list_states(self) -> List[Dict]:
        return [state.summary() for state in self._states.values()]

    # ------------------------------------------------------------------
    # Journal
    # ------------------------------------------------------------------

    def _journal_event(
        self,
        strategy_id: str,
        event_type: JournalEventType,
        summary: str,
        detail: Optional[Dict] = None,
    ) -> None:
        entry = JournalEntry(
            strategy_id=strategy_id,
            event_type=event_type.value,
            summary=summary,
            detail=detail or {},
        )
        self._journal.append(entry)

    def get_journal(self, strategy_id: Optional[str] = None) -> List[JournalEntry]:
        if strategy_id is None:
            return list(self._journal)
        return [e for e in self._journal if e.strategy_id == strategy_id]

    def journal_count(self) -> int:
        return len(self._journal)
