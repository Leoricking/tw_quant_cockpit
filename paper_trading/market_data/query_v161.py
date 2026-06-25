"""
paper_trading/market_data/query_v161.py — Market Data Query Service v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Read-only query interface. No broker call. No real order.
"""
from __future__ import annotations
from typing import Optional, List, Dict, Any

from paper_trading.market_data.store_v161 import MarketDataStore

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class MarketDataQueryService:
    """
    Read-only query service for market data store.
    Forbidden methods raise NotImplementedError.
    """

    def __init__(self, store: MarketDataStore) -> None:
        self._store = store

    def latest_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        return self._store.get_latest_quote(symbol)

    def latest_trade(self, symbol: str) -> Optional[Dict[str, Any]]:
        return self._store.get_latest_trade(symbol)

    def quote_history(self, symbol: str, limit: int = 50) -> List[Dict[str, Any]]:
        return self._store.get_quotes(symbol, limit=limit)

    def trade_history(self, symbol: str, limit: int = 50) -> List[Dict[str, Any]]:
        return self._store.get_trades(symbol, limit=limit)

    def list_active_symbols(self) -> List[str]:
        quotes = set(self._store.list_symbols_with_quotes())
        trades = set(self._store.list_symbols_with_trades())
        return sorted(quotes | trades)

    def session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._store.get_session_metadata(session_id)

    # Forbidden methods — market data query only, no broker/order actions
    def submit_real_order(self, *args, **kwargs):
        raise NotImplementedError(
            "submit_real_order FORBIDDEN — PRODUCTION_TRADING_BLOCKED=True. "
            "This is MARKET_DATA_ONLY."
        )

    def connect_broker(self, *args, **kwargs):
        raise NotImplementedError(
            "connect_broker FORBIDDEN — NO_BROKER_API=True."
        )

    def execute_real_trade(self, *args, **kwargs):
        raise NotImplementedError(
            "execute_real_trade FORBIDDEN — PRODUCTION_TRADING_BLOCKED=True."
        )
