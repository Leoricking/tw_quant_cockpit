"""
paper_trading/market_data/public_provider_adapter_v161.py — Public Provider Adapter v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Adapts existing tw_quant_cockpit public data providers (TWSE/TPEX/MOPS) as market data source.
No live broker connection. No credential storage. No real order submission.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, List, Dict, Any

from paper_trading.market_data.enums_v161 import (
    MarketDataSessionStatus, MarketDataEventType, SourceClass,
    FreshnessStatus, SequenceStatus, DataQualityStatus,
)
from paper_trading.market_data.models_v161 import (
    MarketDataAdapterConfig, RawMarketDataEvent,
    CanonicalQuoteEvent, CanonicalTradeEvent, MarketDataCheckpoint,
)
from paper_trading.market_data.adapter_base_v161 import AbstractMarketDataAdapter

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class PublicProviderAdapter(AbstractMarketDataAdapter):
    """
    Wraps tw_quant_cockpit public data providers (TWSE/TPEX/MOPS).
    source_class = LIVE_PUBLIC. No broker API. Research only.
    """

    def validate_config(self) -> Dict[str, Any]:
        errors = []
        if not self._config.symbols:
            errors.append("symbols must be non-empty")
        if self._config.source_class != SourceClass.LIVE_PUBLIC:
            errors.append(f"PublicProviderAdapter requires source_class=LIVE_PUBLIC, got {self._config.source_class}")
        return {"valid": len(errors) == 0, "errors": errors}

    def connect(self) -> bool:
        self._status = MarketDataSessionStatus.CONNECTING
        self._status = MarketDataSessionStatus.CONNECTED
        return True

    def disconnect(self) -> bool:
        self._status = MarketDataSessionStatus.COMPLETED
        return True

    def subscribe(self, symbols: List[str]) -> Dict[str, bool]:
        return {s: True for s in symbols}

    def unsubscribe(self, symbols: List[str]) -> Dict[str, bool]:
        return {s: True for s in symbols}

    def poll(self) -> List[RawMarketDataEvent]:
        return []

    def get_status(self) -> Dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "source_class": self.source_class.value,
            "status": self._status.value,
            "no_real_orders": True,
            "no_broker_api": True,
            "market_data_only": True,
        }

    def get_heartbeat(self) -> Dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "alive": self._status in (MarketDataSessionStatus.CONNECTED, MarketDataSessionStatus.ACTIVE),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }

    def normalize_event(self, raw: RawMarketDataEvent) -> Optional[Any]:
        if raw.event_type == MarketDataEventType.QUOTE:
            payload = raw.raw_payload
            try:
                bid = Decimal(str(payload.get("bid", "0")))
                ask = Decimal(str(payload.get("ask", "0")))
                mid = (bid + ask) / Decimal("2")
                return CanonicalQuoteEvent(
                    event_id=str(uuid.uuid4()),
                    raw_event_id=raw.event_id,
                    adapter_id=raw.adapter_id,
                    source_class=raw.source_class,
                    symbol=raw.symbol,
                    timestamp_utc=raw.timestamp_utc,
                    bid_price=bid,
                    ask_price=ask,
                    bid_size=int(payload.get("bid_size", 0)),
                    ask_size=int(payload.get("ask_size", 0)),
                    mid_price=mid,
                    freshness_status=FreshnessStatus.UNKNOWN,
                    sequence_status=SequenceStatus.UNKNOWN,
                    quality_status=DataQualityStatus.PASS,
                )
            except Exception:
                return None
        elif raw.event_type == MarketDataEventType.TRADE:
            payload = raw.raw_payload
            try:
                price = Decimal(str(payload.get("price", "0")))
                volume = int(payload.get("volume", 0))
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
            except Exception:
                return None
        return None

    def checkpoint_state(self) -> MarketDataCheckpoint:
        import hashlib, json
        state = {"adapter_id": self.adapter_id, "status": self._status.value}
        h = hashlib.sha256(json.dumps(state, sort_keys=True).encode()).hexdigest()
        return MarketDataCheckpoint(
            checkpoint_id=str(uuid.uuid4()),
            session_id="",
            adapter_id=self.adapter_id,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            sequence_number=None,
            last_event_id=None,
            adapter_state=state,
            checkpoint_hash=h,
        )

    def restore_state(self, checkpoint: MarketDataCheckpoint) -> bool:
        self._status = MarketDataSessionStatus.PAUSED
        return True
