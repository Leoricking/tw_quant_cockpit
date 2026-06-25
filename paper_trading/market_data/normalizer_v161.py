"""
paper_trading/market_data/normalizer_v161.py — Normalizer coordinator v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Orchestrates quote and trade normalization. Decimal-safe. TZ-aware.
"""
from __future__ import annotations
from typing import Optional, Any

from paper_trading.market_data.enums_v161 import MarketDataEventType, SourceClass
from paper_trading.market_data.models_v161 import RawMarketDataEvent

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class MarketDataNormalizer:
    """
    Dispatches raw events to quote or trade normalizers.
    Ensures source_class is disclosed on every canonical event.
    """

    def __init__(self) -> None:
        from paper_trading.market_data.quote_normalizer_v161 import QuoteNormalizer
        from paper_trading.market_data.trade_normalizer_v161 import TradeNormalizer
        self._quote_normalizer = QuoteNormalizer()
        self._trade_normalizer = TradeNormalizer()

    def normalize(self, raw: RawMarketDataEvent) -> Optional[Any]:
        """Normalize a raw event. Returns canonical event or None if unsupported/invalid."""
        if raw.source_class == SourceClass.UNKNOWN:
            return None  # UNKNOWN source never trusted

        if raw.event_type == MarketDataEventType.QUOTE:
            return self._quote_normalizer.normalize(raw)
        elif raw.event_type == MarketDataEventType.TRADE:
            return self._trade_normalizer.normalize(raw)
        return None

    def normalize_batch(self, raw_events: list) -> list:
        """Normalize a batch of raw events, skipping None results."""
        results = []
        for raw in raw_events:
            canonical = self.normalize(raw)
            if canonical is not None:
                results.append(canonical)
        return results
