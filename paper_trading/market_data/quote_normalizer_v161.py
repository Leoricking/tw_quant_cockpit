"""
paper_trading/market_data/quote_normalizer_v161.py — Quote Normalizer v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
bid<=ask enforced. Decimal-safe. Timezone-aware. Source disclosed.
"""
from __future__ import annotations
import uuid
from decimal import Decimal, InvalidOperation
from typing import Optional

from paper_trading.market_data.enums_v161 import (
    FreshnessStatus, SequenceStatus, DataQualityStatus,
)
from paper_trading.market_data.models_v161 import RawMarketDataEvent, CanonicalQuoteEvent

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
BID_ASK_INVARIANT_ENFORCED: bool = True


class QuoteNormalizerError(Exception):
    pass


class QuoteNormalizer:
    """
    Normalizes raw quote events to CanonicalQuoteEvent.
    Enforces bid <= ask. Decimal-safe pricing. Source classified on output.
    """

    def normalize(self, raw: RawMarketDataEvent) -> Optional[CanonicalQuoteEvent]:
        payload = raw.raw_payload
        try:
            bid = Decimal(str(payload.get("bid", payload.get("bid_price", "0"))))
            ask = Decimal(str(payload.get("ask", payload.get("ask_price", "0"))))
        except (InvalidOperation, TypeError) as e:
            return None  # non-numeric: drop

        if bid <= Decimal("0") or ask <= Decimal("0"):
            return None

        if bid > ask:
            # bid>ask: drop (invariant violated)
            return None

        mid = (bid + ask) / Decimal("2")
        bid_size = int(payload.get("bid_size", payload.get("bid_vol", 0)))
        ask_size = int(payload.get("ask_size", payload.get("ask_vol", 0)))

        return CanonicalQuoteEvent(
            event_id=str(uuid.uuid4()),
            raw_event_id=raw.event_id,
            adapter_id=raw.adapter_id,
            source_class=raw.source_class,
            symbol=raw.symbol,
            timestamp_utc=raw.timestamp_utc,
            bid_price=bid,
            ask_price=ask,
            bid_size=bid_size,
            ask_size=ask_size,
            mid_price=mid,
            freshness_status=FreshnessStatus.UNKNOWN,
            sequence_status=SequenceStatus.UNKNOWN,
            quality_status=DataQualityStatus.PASS,
        )
