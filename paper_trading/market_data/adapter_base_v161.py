"""
paper_trading/market_data/adapter_base_v161.py — Abstract adapter interface v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
No broker API. No credential storage. No real order submission.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

from paper_trading.market_data.enums_v161 import MarketDataSessionStatus, FeedFailureType
from paper_trading.market_data.models_v161 import (
    MarketDataAdapterConfig, RawMarketDataEvent, MarketDataCheckpoint,
)

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
NO_BROKER_API: bool = True


class AbstractMarketDataAdapter(ABC):
    """
    Abstract base class for all market data adapters.
    No broker API. No credential storage. No real order submission.
    All implementations must maintain research-only invariants.
    """

    def __init__(self, config: MarketDataAdapterConfig) -> None:
        assert config.no_real_orders is True, "Adapter config must have no_real_orders=True"
        assert config.no_broker_api is True, "Adapter config must have no_broker_api=True"
        assert config.market_data_only is True, "Adapter config must have market_data_only=True"
        self._config = config
        self._status: MarketDataSessionStatus = MarketDataSessionStatus.CREATED
        self._last_failure: Optional[FeedFailureType] = None

    @property
    def adapter_id(self) -> str:
        return self._config.adapter_id

    @property
    def status(self) -> MarketDataSessionStatus:
        return self._status

    @property
    def source_class(self):
        return self._config.source_class

    @abstractmethod
    def validate_config(self) -> Dict[str, Any]:
        """Validate adapter configuration. Returns {"valid": bool, "errors": [...]}."""

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to data source. Returns True on success."""

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from data source. Returns True on success."""

    @abstractmethod
    def subscribe(self, symbols: List[str]) -> Dict[str, bool]:
        """Subscribe to symbols. Returns {symbol: success}."""

    @abstractmethod
    def unsubscribe(self, symbols: List[str]) -> Dict[str, bool]:
        """Unsubscribe from symbols. Returns {symbol: success}."""

    @abstractmethod
    def poll(self) -> List[RawMarketDataEvent]:
        """Poll for new events. Returns list of raw events."""

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Return adapter status dict."""

    @abstractmethod
    def get_heartbeat(self) -> Dict[str, Any]:
        """Return heartbeat info dict."""

    @abstractmethod
    def normalize_event(self, raw: RawMarketDataEvent) -> Optional[Any]:
        """Normalize a raw event to canonical form."""

    @abstractmethod
    def checkpoint_state(self) -> MarketDataCheckpoint:
        """Capture current adapter state as a checkpoint."""

    @abstractmethod
    def restore_state(self, checkpoint: MarketDataCheckpoint) -> bool:
        """Restore adapter state from checkpoint. Always resumes to PAUSED."""

    def submit_real_order(self, *args, **kwargs):
        raise NotImplementedError(
            "submit_real_order is FORBIDDEN — PRODUCTION_TRADING_BLOCKED=True. "
            "This adapter is MARKET_DATA_ONLY."
        )

    def connect_broker(self, *args, **kwargs):
        raise NotImplementedError(
            "connect_broker is FORBIDDEN — NO_BROKER_API=True. "
            "This adapter is MARKET_DATA_ONLY."
        )

    def get_credentials(self, *args, **kwargs):
        raise NotImplementedError(
            "get_credentials is FORBIDDEN — NO_CREDENTIAL_STORAGE=True."
        )
