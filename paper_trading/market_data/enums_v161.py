"""
paper_trading/market_data/enums_v161.py — Market Data Session Adapter enums v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
"""
from __future__ import annotations
from enum import Enum

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class MarketDataEventType(str, Enum):
    QUOTE = "QUOTE"
    TRADE = "TRADE"
    ORDER_BOOK = "ORDER_BOOK"
    SESSION_OPEN = "SESSION_OPEN"
    SESSION_CLOSE = "SESSION_CLOSE"
    HALT = "HALT"
    RESUME = "RESUME"
    HEARTBEAT = "HEARTBEAT"
    ERROR = "ERROR"


class MarketDataSessionStatus(str, Enum):
    CREATED = "CREATED"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    SUBSCRIBING = "SUBSCRIBING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    RECONNECTING = "RECONNECTING"
    FAILING_OVER = "FAILING_OVER"
    CHECKPOINTING = "CHECKPOINTING"
    HALTED = "HALTED"
    COMPLETED = "COMPLETED"


class SourceClass(str, Enum):
    LIVE_PUBLIC = "LIVE_PUBLIC"
    REPLAY = "REPLAY"
    FIXTURE = "FIXTURE"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"
    SIMULATION = "SIMULATION"


class FreshnessStatus(str, Enum):
    FRESH = "FRESH"
    STALE = "STALE"
    DELAYED = "DELAYED"
    UNKNOWN = "UNKNOWN"
    EXPIRED = "EXPIRED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class SequenceStatus(str, Enum):
    IN_ORDER = "IN_ORDER"
    GAP_DETECTED = "GAP_DETECTED"
    DUPLICATE = "DUPLICATE"
    OUT_OF_ORDER = "OUT_OF_ORDER"
    RESET = "RESET"
    UNKNOWN = "UNKNOWN"


class DataQualityStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"


class FeedFailureType(str, Enum):
    CONNECTION_LOST = "CONNECTION_LOST"
    TIMEOUT = "TIMEOUT"
    AUTH_FAILED = "AUTH_FAILED"
    RATE_LIMITED = "RATE_LIMITED"
    BAD_DATA = "BAD_DATA"
    SYMBOL_NOT_FOUND = "SYMBOL_NOT_FOUND"
    SESSION_EXPIRED = "SESSION_EXPIRED"
    PROVIDER_ERROR = "PROVIDER_ERROR"
    UNKNOWN = "UNKNOWN"


class ReconnectPolicy(str, Enum):
    NO_RECONNECT = "NO_RECONNECT"
    FIXED_INTERVAL = "FIXED_INTERVAL"
    BOUNDED_EXPONENTIAL_BACKOFF = "BOUNDED_EXPONENTIAL_BACKOFF"


class FailoverPolicy(str, Enum):
    NO_FAILOVER = "NO_FAILOVER"
    PAUSE_ON_FAILURE = "PAUSE_ON_FAILURE"
    HALT_ON_FAILURE = "HALT_ON_FAILURE"
