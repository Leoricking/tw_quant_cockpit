"""
data/providers/twse/provider_v140.py — TWSE Provider v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, Optional, Tuple

from data.providers.twse.models_v140 import TWSEFetchStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
TWSE_REALTIME_AVAILABLE = False
TWSE_BROKER_EXECUTION_AVAILABLE = False
TWSE_AUTO_DOWNLOAD_ENABLED = False
TWSE_MOCK_FALLBACK_ENABLED = False


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class _ProviderMetadata:
    """Simple metadata holder (compatible with ProviderMetadata interface)."""

    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}


class TWSEProviderV140:
    """
    TWSE Official Public Data Provider v1.4.0.

    Implements the RealDataProviderAdapter interface contract.
    [!] Not a broker. No order execution. Historical data only.
    """

    provider_id = "twse_official"
    provider_name = "Taiwan Stock Exchange Official Public Data"
    market = "TWSE"
    official = True
    requires_auth = False
    supports_real_mode = True
    supports_mock_mode = True  # For testing only
    mock_formal_conclusion_allowed = False
    broker_provider = False
    order_execution_supported = False
    TWSE_REALTIME_AVAILABLE = False
    TWSE_BROKER_EXECUTION_AVAILABLE = False
    TWSE_AUTO_DOWNLOAD_ENABLED = False
    TWSE_MOCK_FALLBACK_ENABLED = False

    def get_metadata(self) -> _ProviderMetadata:
        return _ProviderMetadata(
            provider_id=self.provider_id,
            provider_name=self.provider_name,
            market=self.market,
            official=self.official,
            requires_auth=self.requires_auth,
            supports_real_mode=self.supports_real_mode,
            supports_mock_mode=self.supports_mock_mode,
            mock_formal_conclusion_allowed=self.mock_formal_conclusion_allowed,
            broker_provider=self.broker_provider,
            order_execution_supported=self.order_execution_supported,
            realtime_available=self.TWSE_REALTIME_AVAILABLE,
            no_real_orders=True,
            broker_execution_enabled=False,
            production_trading_blocked=True,
        )

    def get_capability_matrix(self) -> Dict[str, Any]:
        from data.providers.twse.capabilities_v140 import TWSECapabilityMatrix
        return TWSECapabilityMatrix().build_summary()

    def get_endpoint_registry(self):
        from data.providers.twse.endpoints_v140 import TWSEEndpointRegistry
        return TWSEEndpointRegistry()

    def is_capability_supported(self, capability: str) -> bool:
        from data.providers.twse.capabilities_v140 import TWSECapabilityMatrix
        return TWSECapabilityMatrix().is_supported(capability)

    def health_check(self) -> Dict[str, Any]:
        from data.providers.twse.health_v140 import TWSEProviderHealthCheck
        return TWSEProviderHealthCheck().get_health_summary()

    def fetch_with_transport(
        self,
        endpoint_id: str,
        params: Dict[str, Any],
        transport: Optional[Callable] = None,
    ) -> Tuple[TWSEFetchStatus, Any, Dict[str, Any]]:
        """
        Fetch data from a TWSE endpoint.
        transport is injectable for offline testing.
        NEVER falls back to mock.
        """
        from data.providers.twse.endpoints_v140 import TWSEEndpointRegistry
        from data.providers.twse.client_v140 import TWSEHttpClient

        reg = TWSEEndpointRegistry()
        ep = reg.get(endpoint_id)
        if ep is None:
            return (
                TWSEFetchStatus.UNAVAILABLE,
                None,
                {"error": f"Unknown endpoint: {endpoint_id}", "request_id": None, "warnings": []},
            )
        if not ep.enabled:
            return (
                TWSEFetchStatus.BLOCKED,
                None,
                {"error": f"Endpoint {endpoint_id} is disabled", "request_id": None, "warnings": []},
            )

        client = TWSEHttpClient(transport=transport)
        return client.get(ep.path, params)
