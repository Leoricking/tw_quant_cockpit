"""
paper_trading/market_data/store_v161.py — Market Data Store v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
In-memory store for canonical events and session metadata.
"""
from __future__ import annotations
from typing import Dict, List, Optional, Any
from collections import deque

from paper_trading.market_data.enums_v161 import SourceClass

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True

DEFAULT_MAX_EVENTS_PER_SYMBOL: int = 1_000


class MarketDataStore:
    """
    In-memory store for canonical market data events.
    Bounded per-symbol queues. Research only.
    """

    def __init__(self, max_events_per_symbol: int = DEFAULT_MAX_EVENTS_PER_SYMBOL) -> None:
        self._max_per_symbol = max_events_per_symbol
        # symbol → deque of canonical event dicts
        self._quote_store: Dict[str, deque] = {}
        self._trade_store: Dict[str, deque] = {}
        self._session_metadata: Dict[str, Dict[str, Any]] = {}
        self._total_stored: int = 0

    def store_quote(self, symbol: str, event_dict: Dict[str, Any]) -> None:
        q = self._quote_store.setdefault(symbol, deque(maxlen=self._max_per_symbol))
        q.append(event_dict)
        self._total_stored += 1

    def store_trade(self, symbol: str, event_dict: Dict[str, Any]) -> None:
        q = self._trade_store.setdefault(symbol, deque(maxlen=self._max_per_symbol))
        q.append(event_dict)
        self._total_stored += 1

    def get_quotes(self, symbol: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        events = list(self._quote_store.get(symbol, []))
        if limit:
            events = events[-limit:]
        return events

    def get_trades(self, symbol: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        events = list(self._trade_store.get(symbol, []))
        if limit:
            events = events[-limit:]
        return events

    def get_latest_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        q = self._quote_store.get(symbol)
        if q:
            return q[-1]
        return None

    def get_latest_trade(self, symbol: str) -> Optional[Dict[str, Any]]:
        q = self._trade_store.get(symbol)
        if q:
            return q[-1]
        return None

    def store_session_metadata(self, session_id: str, metadata: Dict[str, Any]) -> None:
        self._session_metadata[session_id] = metadata

    def get_session_metadata(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._session_metadata.get(session_id)

    def list_symbols_with_quotes(self) -> List[str]:
        return [s for s, q in self._quote_store.items() if q]

    def list_symbols_with_trades(self) -> List[str]:
        return [s for s, q in self._trade_store.items() if q]

    @property
    def total_stored(self) -> int:
        return self._total_stored

    def reset(self) -> None:
        self._quote_store.clear()
        self._trade_store.clear()
        self._session_metadata.clear()
        self._total_stored = 0
