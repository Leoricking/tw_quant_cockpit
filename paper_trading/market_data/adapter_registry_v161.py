"""
paper_trading/market_data/adapter_registry_v161.py — Adapter Registry v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Duplicate adapter ID → BLOCKED. Unknown source → BLOCKED. Missing timestamp semantics → BLOCKED.
"""
from __future__ import annotations
from typing import Dict, Optional, List, Any

from paper_trading.market_data.enums_v161 import SourceClass
from paper_trading.market_data.adapter_base_v161 import AbstractMarketDataAdapter

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
DUPLICATE_ADAPTER_ID_BLOCKED: bool = True
UNKNOWN_SOURCE_BLOCKED: bool = True


class AdapterRegistryError(Exception):
    pass


class MarketDataAdapterRegistry:
    """
    Registry for market data adapters.
    - Duplicate adapter_id → BLOCKED (raises AdapterRegistryError)
    - UNKNOWN source_class → BLOCKED
    - Missing timestamp semantics → BLOCKED
    """

    def __init__(self) -> None:
        self._adapters: Dict[str, AbstractMarketDataAdapter] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def register(self, adapter: AbstractMarketDataAdapter, timestamp_semantics: str = "") -> None:
        adapter_id = adapter.adapter_id

        if adapter_id in self._adapters:
            raise AdapterRegistryError(
                f"BLOCKED: Duplicate adapter_id '{adapter_id}'. "
                "Each adapter must have a unique ID. DUPLICATE_ADAPTER_ID_BLOCKED=True."
            )

        if adapter.source_class == SourceClass.UNKNOWN:
            raise AdapterRegistryError(
                f"BLOCKED: adapter '{adapter_id}' has source_class=UNKNOWN. "
                "UNKNOWN source cannot be registered as trusted. UNKNOWN_SOURCE_BLOCKED=True."
            )

        if not timestamp_semantics or not timestamp_semantics.strip():
            raise AdapterRegistryError(
                f"BLOCKED: adapter '{adapter_id}' missing timestamp_semantics. "
                "All adapters must declare timestamp semantics (e.g. 'event_time_utc')."
            )

        self._adapters[adapter_id] = adapter
        self._metadata[adapter_id] = {
            "source_class": adapter.source_class.value,
            "timestamp_semantics": timestamp_semantics,
        }

    def get(self, adapter_id: str) -> Optional[AbstractMarketDataAdapter]:
        return self._adapters.get(adapter_id)

    def list_adapters(self) -> List[str]:
        return list(self._adapters.keys())

    def get_metadata(self, adapter_id: str) -> Optional[Dict[str, Any]]:
        return self._metadata.get(adapter_id)

    def unregister(self, adapter_id: str) -> bool:
        if adapter_id in self._adapters:
            del self._adapters[adapter_id]
            del self._metadata[adapter_id]
            return True
        return False

    def count(self) -> int:
        return len(self._adapters)
