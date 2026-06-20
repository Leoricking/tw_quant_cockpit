"""
data/providers/tpex/provider_v141.py — TPEx Provider v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, Optional, Tuple

from data.providers.tpex.models_v141 import TPExFetchStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
TPEX_REALTIME_AVAILABLE = False
TPEX_BROKER_EXECUTION_AVAILABLE = False
TPEX_AUTO_DOWNLOAD_ENABLED = False
TPEX_MOCK_FALLBACK_ENABLED = False


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class _ProviderMetadata:
    """Simple metadata holder (compatible with ProviderMetadata interface)."""

    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}


class TPExProviderV141:
    """
    TPEx Official Public Data Provider v1.4.1.

    Implements the RealDataProviderAdapter interface contract.
    [!] Not a broker. No order execution. Historical data only.
    [!] Mainboard Common Stocks only by default.
    """

    provider_id = "tpex_official"
    provider_name = "Taipei Exchange Official Public Data"
    market = "TPEx"
    board_scope = "MAINBOARD"
    official = True
    requires_auth = False
    supports_real_mode = True
    supports_mock_mode = True  # For testing only
    mock_formal_conclusion_allowed = False
    broker_provider = False
    order_execution_supported = False
    realtime_supported = False
    TPEX_REALTIME_AVAILABLE = False
    TPEX_BROKER_EXECUTION_AVAILABLE = False
    TPEX_AUTO_DOWNLOAD_ENABLED = False
    TPEX_MOCK_FALLBACK_ENABLED = False

    def get_metadata(self) -> _ProviderMetadata:
        return _ProviderMetadata(
            provider_id=self.provider_id,
            provider_name=self.provider_name,
            market=self.market,
            board_scope=self.board_scope,
            official=self.official,
            requires_auth=self.requires_auth,
            supports_real_mode=self.supports_real_mode,
            supports_mock_mode=self.supports_mock_mode,
            mock_formal_conclusion_allowed=self.mock_formal_conclusion_allowed,
            broker_provider=self.broker_provider,
            order_execution_supported=self.order_execution_supported,
            realtime_available=self.TPEX_REALTIME_AVAILABLE,
            no_real_orders=True,
            broker_execution_enabled=False,
            production_trading_blocked=True,
        )

    def get_capability_matrix(self) -> Dict[str, Any]:
        from data.providers.tpex.capabilities_v141 import TPExCapabilityMatrix
        return TPExCapabilityMatrix().build_summary()

    def get_endpoint_registry(self):
        from data.providers.tpex.endpoints_v141 import TPExEndpointRegistry
        return TPExEndpointRegistry()

    def is_capability_supported(self, capability: str) -> bool:
        from data.providers.tpex.capabilities_v141 import TPExCapabilityMatrix
        return TPExCapabilityMatrix().is_supported(capability)

    def health_check(self) -> Dict[str, Any]:
        from data.providers.tpex.health_v141 import TPExProviderHealthCheck
        return TPExProviderHealthCheck().get_health_summary()

    def fetch_with_transport(
        self,
        endpoint_id: str,
        params: Dict[str, Any],
        transport: Optional[Callable] = None,
    ) -> Tuple[TPExFetchStatus, Any, Dict[str, Any]]:
        """
        Fetch data from a TPEx endpoint.
        transport is injectable for offline testing.
        NEVER falls back to mock.
        """
        from data.providers.tpex.endpoints_v141 import TPExEndpointRegistry
        from data.providers.tpex.client_v141 import TPExHttpClient

        reg = TPExEndpointRegistry()
        ep = reg.get(endpoint_id)
        if ep is None:
            return (
                TPExFetchStatus.UNAVAILABLE,
                None,
                {"error": f"Unknown endpoint: {endpoint_id}", "request_id": None, "warnings": []},
            )
        if not ep.enabled:
            return (
                TPExFetchStatus.BLOCKED,
                None,
                {"error": f"Endpoint {endpoint_id} is disabled", "request_id": None, "warnings": []},
            )

        client = TPExHttpClient(transport=transport)
        return client.get(ep.path, params)
