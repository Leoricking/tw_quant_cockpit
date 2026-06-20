"""
data/providers/mops/provider_v142.py — MOPS Provider v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, Optional, Tuple

from data.providers.mops.models_v142 import MOPSFetchStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
MOPS_REALTIME_AVAILABLE = False
MOPS_BROKER_EXECUTION_AVAILABLE = False
MOPS_AUTO_DOWNLOAD_ENABLED = False
MOPS_MOCK_FALLBACK_ENABLED = False


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class _ProviderMetadata:
    """Simple metadata holder."""

    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}


class MOPSProviderV142:
    """
    MOPS Official Public Disclosure Provider v1.4.2.

    Implements the RealDataProviderAdapter interface contract.
    [!] Not a broker. No order execution. Financial disclosure data only.
    [!] No realtime. No mock fallback. No auto-download.
    """

    provider_id = "mops_official"
    provider_name = "Market Observation Post System Official Public Disclosure"
    market = "MOPS"
    data_domain = "financial_disclosure"
    official = True
    requires_auth = False
    supports_real_mode = True
    supports_mock_mode = True  # For testing only
    mock_formal_conclusion_allowed = False
    broker_provider = False
    order_execution_supported = False
    realtime_supported = False
    MOPS_REALTIME_AVAILABLE = False
    MOPS_BROKER_EXECUTION_AVAILABLE = False
    MOPS_AUTO_DOWNLOAD_ENABLED = False
    MOPS_MOCK_FALLBACK_ENABLED = False

    def get_metadata(self) -> _ProviderMetadata:
        return _ProviderMetadata(
            provider_id=self.provider_id,
            provider_name=self.provider_name,
            market=self.market,
            data_domain=self.data_domain,
            official=self.official,
            requires_auth=self.requires_auth,
            supports_real_mode=self.supports_real_mode,
            supports_mock_mode=self.supports_mock_mode,
            mock_formal_conclusion_allowed=self.mock_formal_conclusion_allowed,
            broker_provider=self.broker_provider,
            order_execution_supported=self.order_execution_supported,
            realtime_available=self.MOPS_REALTIME_AVAILABLE,
            no_real_orders=True,
            broker_execution_enabled=False,
            production_trading_blocked=True,
        )

    def get_capability_matrix(self) -> Dict[str, Any]:
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        return MOPSCapabilityMatrix().build_summary()

    def get_endpoint_registry(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        return MOPSEndpointRegistry()

    def is_capability_supported(self, capability: str) -> bool:
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        return MOPSCapabilityMatrix().is_supported(capability)

    def health_check(self) -> Dict[str, Any]:
        from data.providers.mops.health_v142 import MOPSProviderHealthCheck
        return MOPSProviderHealthCheck().get_health_summary()

    def fetch_with_transport(
        self,
        endpoint_id: str,
        params: Dict[str, Any],
        transport: Optional[Callable] = None,
    ) -> Tuple[MOPSFetchStatus, Any, Dict[str, Any]]:
        """
        Fetch data from a MOPS endpoint.
        transport is injectable for offline testing.
        NEVER falls back to mock.
        """
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        from data.providers.mops.client_v142 import MOPSHttpClient

        reg = MOPSEndpointRegistry()
        ep = reg.get(endpoint_id)
        if ep is None:
            return (
                MOPSFetchStatus.UNAVAILABLE,
                None,
                {"error": f"Unknown endpoint: {endpoint_id}", "request_id": None, "warnings": []},
            )
        if not ep.enabled:
            return (
                MOPSFetchStatus.BLOCKED,
                None,
                {"error": f"Endpoint {endpoint_id} is disabled", "request_id": None, "warnings": []},
            )

        client = MOPSHttpClient(transport=transport)
        if ep.method == "POST" and ep.requires_form_params:
            form_data = {**ep.form_params, **params}
            return client.post_form(ep.path, form_data)
        else:
            return client.get(ep.path, params)
