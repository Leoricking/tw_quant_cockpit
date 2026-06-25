"""
paper_trading/market_data/models_v161.py — Market Data Session Adapter models v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
All canonical events carry safety markers. Decimal-safe pricing. Timezone-aware timestamps.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Dict, Any

from paper_trading.market_data.enums_v161 import (
    MarketDataEventType, MarketDataSessionStatus, SourceClass,
    FreshnessStatus, SequenceStatus, DataQualityStatus,
    ReconnectPolicy, FailoverPolicy,
)

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


@dataclass
class MarketDataAdapterConfig:
    adapter_id: str
    source_class: SourceClass
    provider_name: str
    symbols: List[str]
    reconnect_policy: ReconnectPolicy = ReconnectPolicy.NO_RECONNECT
    failover_policy: FailoverPolicy = FailoverPolicy.PAUSE_ON_FAILURE
    max_reconnect_attempts: int = 0
    reconnect_interval_seconds: int = 30
    heartbeat_interval_seconds: int = 10
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Safety
    no_real_orders: bool = True
    no_broker_api: bool = True
    market_data_only: bool = True

    def __post_init__(self):
        assert self.no_real_orders is True, "no_real_orders must be True"
        assert self.no_broker_api is True, "no_broker_api must be True"
        assert self.market_data_only is True, "market_data_only must be True"
        if self.source_class == SourceClass.UNKNOWN:
            raise ValueError("UNKNOWN source class is not trusted as LIVE — set explicit source_class")


@dataclass
class RawMarketDataEvent:
    event_id: str
    adapter_id: str
    source_class: SourceClass
    event_type: MarketDataEventType
    symbol: str
    timestamp_utc: str        # ISO-8601 UTC
    raw_payload: Dict[str, Any] = field(default_factory=dict)
    sequence_number: Optional[int] = None
    received_at_utc: Optional[str] = None
    # Safety markers
    research_only: bool = True
    market_data_only: bool = True
    no_broker_call: bool = True

    def __post_init__(self):
        assert self.research_only is True
        assert self.market_data_only is True
        assert self.no_broker_call is True


@dataclass
class CanonicalQuoteEvent:
    event_id: str
    raw_event_id: str
    adapter_id: str
    source_class: SourceClass
    symbol: str
    timestamp_utc: str
    bid_price: Decimal
    ask_price: Decimal
    bid_size: int
    ask_size: int
    mid_price: Decimal
    freshness_status: FreshnessStatus
    sequence_status: SequenceStatus
    quality_status: DataQualityStatus
    delay_ms: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Safety markers
    research_only: bool = True
    market_data_only: bool = True
    no_broker_call: bool = True
    no_real_order: bool = True
    source_classified: bool = True
    data_mode_disclosed: bool = True

    def __post_init__(self):
        assert self.research_only is True
        assert self.market_data_only is True
        assert self.no_broker_call is True
        assert self.no_real_order is True
        assert self.source_classified is True
        assert self.data_mode_disclosed is True
        if self.bid_price > self.ask_price:
            raise ValueError(
                f"bid_price ({self.bid_price}) > ask_price ({self.ask_price}): bid<=ask enforced"
            )


@dataclass
class CanonicalTradeEvent:
    event_id: str
    raw_event_id: str
    adapter_id: str
    source_class: SourceClass
    symbol: str
    timestamp_utc: str
    price: Decimal
    volume: int
    freshness_status: FreshnessStatus
    sequence_status: SequenceStatus
    quality_status: DataQualityStatus
    delay_ms: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Safety markers
    research_only: bool = True
    market_data_only: bool = True
    no_broker_call: bool = True
    no_real_order: bool = True
    source_classified: bool = True
    data_mode_disclosed: bool = True

    def __post_init__(self):
        assert self.research_only is True
        assert self.market_data_only is True
        assert self.no_broker_call is True
        assert self.no_real_order is True
        assert self.source_classified is True
        assert self.data_mode_disclosed is True
        if self.price <= Decimal("0"):
            raise ValueError(f"trade price must be > 0, got {self.price}")


@dataclass
class MarketDataSessionConfig:
    session_id: str
    adapter_id: str
    symbols: List[str]
    source_class: SourceClass
    paper_session_as_of: Optional[str] = None  # PIT enforcement
    timezone: str = "Asia/Taipei"
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Safety
    no_real_orders: bool = True
    no_broker_api: bool = True

    def __post_init__(self):
        assert self.no_real_orders is True
        assert self.no_broker_api is True


@dataclass
class MarketDataCheckpoint:
    checkpoint_id: str
    session_id: str
    adapter_id: str
    created_at_utc: str
    sequence_number: Optional[int]
    last_event_id: Optional[str]
    adapter_state: Dict[str, Any] = field(default_factory=dict)
    checkpoint_hash: str = ""
    # Safety
    research_only: bool = True
    market_data_only: bool = True

    def __post_init__(self):
        assert self.research_only is True
        assert self.market_data_only is True
