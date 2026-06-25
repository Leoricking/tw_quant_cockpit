"""
paper_trading/strategy/trigger_v162.py — Trigger engine for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
import threading
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from paper_trading.strategy.enums_v162 import TriggerType
from paper_trading.strategy.models_v162 import _new_id, _now_iso

logger = logging.getLogger(__name__)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TriggerEvent:
    """Represents a trigger event that should cause a strategy to evaluate signals."""

    def __init__(
        self,
        trigger_type: TriggerType,
        strategy_id: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.trigger_id: str = _new_id()
        self.trigger_type: TriggerType = trigger_type
        self.strategy_id: str = strategy_id
        self.payload: Dict[str, Any] = payload or {}
        self.created_at: str = _now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trigger_id": self.trigger_id,
            "trigger_type": self.trigger_type.value,
            "strategy_id": self.strategy_id,
            "payload": self.payload,
            "created_at": self.created_at,
        }


class TriggerHandler:
    """
    A registered handler for a specific trigger type.

    callback(event: TriggerEvent) → None
    """

    def __init__(
        self,
        strategy_id: str,
        trigger_type: TriggerType,
        callback: Callable[[TriggerEvent], None],
        description: str = "",
    ) -> None:
        self.handler_id: str = _new_id()
        self.strategy_id: str = strategy_id
        self.trigger_type: TriggerType = trigger_type
        self.callback: Callable[[TriggerEvent], None] = callback
        self.description: str = description
        self.call_count: int = 0
        self.error_count: int = 0
        self.last_called_at: Optional[str] = None


class TriggerEngine:
    """
    Routes TriggerEvents to registered handlers.

    Paper-only. Triggers cause signal evaluation only — no real orders.
    Thread-safe.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._handlers: Dict[str, TriggerHandler] = {}  # handler_id → handler
        self._event_log: List[Dict[str, Any]] = []

    def register_handler(
        self,
        strategy_id: str,
        trigger_type: TriggerType,
        callback: Callable[[TriggerEvent], None],
        description: str = "",
    ) -> str:
        """Register a trigger handler. Returns handler_id."""
        handler = TriggerHandler(
            strategy_id=strategy_id,
            trigger_type=trigger_type,
            callback=callback,
            description=description,
        )
        with self._lock:
            self._handlers[handler.handler_id] = handler
        logger.debug(
            "[v1.6.2][trigger] Registered handler %s for strategy %s type=%s",
            handler.handler_id[:8], strategy_id, trigger_type.value
        )
        return handler.handler_id

    def unregister_handler(self, handler_id: str) -> bool:
        with self._lock:
            if handler_id in self._handlers:
                del self._handlers[handler_id]
                return True
        return False

    def fire(self, event: TriggerEvent) -> int:
        """
        Fire a trigger event. Calls all matching handlers.
        Returns number of handlers called.
        """
        with self._lock:
            matching = [
                h for h in self._handlers.values()
                if h.strategy_id == event.strategy_id
                and h.trigger_type == event.trigger_type
            ]
            self._event_log.append(event.to_dict())

        called = 0
        for handler in matching:
            try:
                handler.callback(event)
                handler.call_count += 1
                handler.last_called_at = _now_iso()
                called += 1
            except Exception as exc:
                handler.error_count += 1
                logger.error(
                    "[v1.6.2][trigger] Handler %s error on event %s: %s",
                    handler.handler_id[:8], event.trigger_id[:8], exc
                )
        return called

    def fire_manual(self, strategy_id: str, payload: Optional[Dict] = None) -> int:
        """Convenience: fire a MANUAL trigger for a strategy."""
        ev = TriggerEvent(TriggerType.MANUAL, strategy_id, payload)
        return self.fire(ev)

    def fire_replay(self, strategy_id: str, payload: Optional[Dict] = None) -> int:
        """Convenience: fire a REPLAY trigger for a strategy."""
        ev = TriggerEvent(TriggerType.REPLAY, strategy_id, payload)
        return self.fire(ev)

    def handler_count(self, strategy_id: Optional[str] = None) -> int:
        with self._lock:
            if strategy_id is None:
                return len(self._handlers)
            return sum(1 for h in self._handlers.values() if h.strategy_id == strategy_id)

    def event_log(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._event_log)

    def clear_handlers_for_strategy(self, strategy_id: str) -> int:
        with self._lock:
            to_remove = [hid for hid, h in self._handlers.items()
                         if h.strategy_id == strategy_id]
            for hid in to_remove:
                del self._handlers[hid]
        return len(to_remove)

    def list_handlers(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                {
                    "handler_id": h.handler_id,
                    "strategy_id": h.strategy_id,
                    "trigger_type": h.trigger_type.value,
                    "description": h.description,
                    "call_count": h.call_count,
                    "error_count": h.error_count,
                    "last_called_at": h.last_called_at,
                }
                for h in self._handlers.values()
            ]
