"""
paper_trading/market_data/trade_normalizer_v161.py — Trade Normalizer v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
price>0 enforced. volume>=0 enforced. Decimal-safe. TZ-aware.
"""
from __future__ import annotations
import uuid
from decimal import Decimal, InvalidOperation
from typing import Optional

from paper_trading.market_data.enums_v161 import (
    FreshnessStatus, SequenceStatus, DataQualityStatus,
)
from paper_trading.market_data.models_v161 import RawMarketDataEvent, CanonicalTradeEvent

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class TradeNormalizer:
    """
    Normalizes raw trade events to CanonicalTradeEvent.
    price>0 enforced. volume>=0. Decimal-safe. Source classified on output.
    """

    def normalize(self, raw: RawMarketDataEvent) -> Optional[CanonicalTradeEvent]:
        payload = raw.raw_payload
        try:
            price = Decimal(str(payload.get("price", payload.get("last_price", "0"))))
        except (InvalidOperation, TypeError):
            return None

        if price <= Decimal("0"):
            return None

        try:
            volume = int(payload.get("volume", payload.get("qty", 0)))
        except (ValueError, TypeError):
            return None

        if volume < 0:
            return None

        return CanonicalTradeEvent(
            event_id=str(uuid.uuid4()),
            raw_event_id=raw.event_id,
            adapter_id=raw.adapter_id,
            source_class=raw.source_class,
            symbol=raw.symbol,
            timestamp_utc=raw.timestamp_utc,
            price=price,
            volume=volume,
            freshness_status=FreshnessStatus.UNKNOWN,
            sequence_status=SequenceStatus.UNKNOWN,
            quality_status=DataQualityStatus.PASS,
        )
