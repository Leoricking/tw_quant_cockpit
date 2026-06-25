"""
paper_trading/strategy/strategy_registry_v162.py — Strategy registry for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
import threading
from typing import Dict, List, Optional

from paper_trading.strategy.enums_v162 import StrategyStatus
from paper_trading.strategy.models_v162 import StrategyConfig, StrategyMetadata, _now_iso
from paper_trading.strategy.strategy_base_v162 import PaperStrategyBase

logger = logging.getLogger(__name__)

_REGISTRY_LOCK = threading.Lock()


class StrategyRegistry:
    """
    Thread-safe registry of paper strategy instances.

    All strategies registered here are paper-only and research-only.
    No real orders, no broker connections.
    """

    def __init__(self) -> None:
        self._strategies: Dict[str, PaperStrategyBase] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, strategy: PaperStrategyBase) -> str:
        """Register a strategy. Returns the strategy_id."""
        assert strategy.PAPER_ONLY is True, "Only paper strategies may be registered"
        assert strategy.RESEARCH_ONLY is True, "Only research-only strategies may be registered"
        sid = strategy.strategy_id
        with _REGISTRY_LOCK:
            if sid in self._strategies:
                logger.warning("[v1.6.2] Strategy %s already registered — skipping", sid)
                return sid
            self._strategies[sid] = strategy
            logger.info(
                "[v1.6.2] Registered paper strategy: %s (%s)",
                strategy.strategy_name, sid
            )
        return sid

    def unregister(self, strategy_id: str) -> bool:
        """Remove a strategy from the registry. Returns True if removed."""
        with _REGISTRY_LOCK:
            if strategy_id in self._strategies:
                del self._strategies[strategy_id]
                logger.info("[v1.6.2] Unregistered strategy: %s", strategy_id)
                return True
        return False

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, strategy_id: str) -> Optional[PaperStrategyBase]:
        with _REGISTRY_LOCK:
            return self._strategies.get(strategy_id)

    def get_by_name(self, name: str) -> List[PaperStrategyBase]:
        with _REGISTRY_LOCK:
            return [s for s in self._strategies.values()
                    if s.strategy_name == name]

    def list_all(self) -> List[Dict]:
        with _REGISTRY_LOCK:
            result = []
            for s in self._strategies.values():
                result.append({
                    "strategy_id": s.strategy_id,
                    "strategy_name": s.strategy_name,
                    "status": s.status.value,
                    "signal_count": s.metadata.signal_count,
                    "decision_count": s.metadata.decision_count,
                    "proposal_count": s.metadata.proposal_count,
                    "paper_only": s.PAPER_ONLY,
                    "research_only": s.RESEARCH_ONLY,
                })
            return result

    def count(self) -> int:
        with _REGISTRY_LOCK:
            return len(self._strategies)

    def count_by_status(self) -> Dict[str, int]:
        with _REGISTRY_LOCK:
            counts: Dict[str, int] = {}
            for s in self._strategies.values():
                key = s.status.value
                counts[key] = counts.get(key, 0) + 1
            return counts

    def running_strategies(self) -> List[PaperStrategyBase]:
        with _REGISTRY_LOCK:
            return [s for s in self._strategies.values()
                    if s.status == StrategyStatus.RUNNING]

    def is_registered(self, strategy_id: str) -> bool:
        with _REGISTRY_LOCK:
            return strategy_id in self._strategies

    # ------------------------------------------------------------------
    # Lifecycle control
    # ------------------------------------------------------------------

    def start_strategy(self, strategy_id: str) -> bool:
        s = self.get(strategy_id)
        if s is None:
            logger.warning("[v1.6.2] start_strategy: unknown strategy %s", strategy_id)
            return False
        s.start()
        return True

    def pause_strategy(self, strategy_id: str) -> bool:
        s = self.get(strategy_id)
        if s is None:
            return False
        s.pause()
        return True

    def halt_strategy(self, strategy_id: str) -> bool:
        s = self.get(strategy_id)
        if s is None:
            return False
        s.halt()
        return True

    def halt_all(self) -> int:
        """Halt all running strategies. Returns count halted."""
        halted = 0
        with _REGISTRY_LOCK:
            ids = list(self._strategies.keys())
        for sid in ids:
            s = self.get(sid)
            if s and s.status == StrategyStatus.RUNNING:
                s.halt()
                halted += 1
        return halted


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_GLOBAL_REGISTRY: Optional[StrategyRegistry] = None
_GLOBAL_LOCK = threading.Lock()


def get_global_registry() -> StrategyRegistry:
    global _GLOBAL_REGISTRY
    with _GLOBAL_LOCK:
        if _GLOBAL_REGISTRY is None:
            _GLOBAL_REGISTRY = StrategyRegistry()
    return _GLOBAL_REGISTRY


def reset_global_registry() -> None:
    """Reset the global registry (for testing only)."""
    global _GLOBAL_REGISTRY
    with _GLOBAL_LOCK:
        _GLOBAL_REGISTRY = None
