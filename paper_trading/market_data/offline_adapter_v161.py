"""
paper_trading/market_data/offline_adapter_v161.py — Offline Adapter v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Serves events from local cached/stored data. source_class = OFFLINE.
LIVE→OFFLINE failover is DISABLED. Offline cannot substitute for LIVE.
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
LIVE_TO_OFFLINE_FAILOVER_DISABLED: bool = True
OFFLINE_IS_NOT_LIVE: bool = True


class OfflineAdapter(AbstractMarketDataAdapter):
    """
    Serves market data from local cached/stored snapshots.
    source_class = OFFLINE. Cannot be silently used as LIVE substitute.
    No broker API. Research only.
    """

    def __init__(
        self,
        config: MarketDataAdapterConfig,
        stored_events: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        super().__init__(config)
        self._stored_events: List[Dict[str, Any]] = stored_events or []
        self._cursor: int = 0

    def validate_config(self) -> Dict[str, Any]:
        errors = []
        if self._config.source_class != SourceClass.OFFLINE:
            errors.append(f"OfflineAdapter requires source_class=OFFLINE, got {self._config.source_class}")
        return {"valid": len(errors) == 0, "errors": errors}

    def connect(self) -> bool:
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
        events = []
        while self._cursor < len(self._stored_events):
            entry = self._stored_events[self._cursor]
            event = RawMarketDataEvent(
                event_id=entry.get("event_id", str(uuid.uuid4())),
                adapter_id=self.adapter_id,
                source_class=SourceClass.OFFLINE,
                event_type=MarketDataEventType(entry.get("event_type", "TRADE")),
                symbol=entry.get("symbol", ""),
                timestamp_utc=entry.get("timestamp_utc", ""),
                raw_payload=entry.get("payload", {}),
                sequence_number=entry.get("sequence_number"),
            )
            events.append(event)
            self._cursor += 1
        return events

    def get_status(self) -> Dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "source_class": SourceClass.OFFLINE.value,
            "status": self._status.value,
            "cursor": self._cursor,
            "total_stored_events": len(self._stored_events),
            "no_real_orders": True,
            "live_to_offline_failover_disabled": True,
        }

    def get_heartbeat(self) -> Dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "alive": self._status == MarketDataSessionStatus.CONNECTED,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }

    def normalize_event(self, raw: RawMarketDataEvent) -> Optional[Any]:
        payload = raw.raw_payload
        if raw.event_type == MarketDataEventType.QUOTE:
            try:
                bid = Decimal(str(payload.get("bid", "0")))
                ask = Decimal(str(payload.get("ask", "0")))
                mid = (bid + ask) / Decimal("2")
                return CanonicalQuoteEvent(
                    event_id=str(uuid.uuid4()),
                    raw_event_id=raw.event_id,
                    adapter_id=raw.adapter_id,
                    source_class=SourceClass.OFFLINE,
                    symbol=raw.symbol,
                    timestamp_utc=raw.timestamp_utc,
                    bid_price=bid, ask_price=ask, mid_price=mid,
                    bid_size=int(payload.get("bid_size", 0)),
                    ask_size=int(payload.get("ask_size", 0)),
                    freshness_status=FreshnessStatus.STALE,
                    sequence_status=SequenceStatus.UNKNOWN,
                    quality_status=DataQualityStatus.PASS,
                )
            except Exception:
                return None
        elif raw.event_type == MarketDataEventType.TRADE:
            try:
                price = Decimal(str(payload.get("price", "0")))
                volume = int(payload.get("volume", 0))
                return CanonicalTradeEvent(
                    event_id=str(uuid.uuid4()),
                    raw_event_id=raw.event_id,
                    adapter_id=raw.adapter_id,
                    source_class=SourceClass.OFFLINE,
                    symbol=raw.symbol,
                    timestamp_utc=raw.timestamp_utc,
                    price=price, volume=volume,
                    freshness_status=FreshnessStatus.STALE,
                    sequence_status=SequenceStatus.UNKNOWN,
                    quality_status=DataQualityStatus.PASS,
                )
            except Exception:
                return None
        return None

    def checkpoint_state(self) -> MarketDataCheckpoint:
        import hashlib, json
        state = {"adapter_id": self.adapter_id, "cursor": self._cursor}
        h = hashlib.sha256(json.dumps(state, sort_keys=True).encode()).hexdigest()
        return MarketDataCheckpoint(
            checkpoint_id=str(uuid.uuid4()),
            session_id="",
            adapter_id=self.adapter_id,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            sequence_number=self._cursor,
            last_event_id=None,
            adapter_state=state,
            checkpoint_hash=h,
        )

    def restore_state(self, checkpoint: MarketDataCheckpoint) -> bool:
        self._cursor = checkpoint.adapter_state.get("cursor", 0)
        self._status = MarketDataSessionStatus.PAUSED
        return True
