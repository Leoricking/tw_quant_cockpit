"""
data/providers/data_gov_tw/provider_v143.py — data.gov.tw Provider v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] DATA_GOV_TW_REALTIME_AVAILABLE = False.
[!] DATA_GOV_TW_BROKER_EXECUTION_AVAILABLE = False.
[!] DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED = False.
[!] DATA_GOV_TW_MOCK_FALLBACK_ENABLED = False.
[!] Cannot override TWSE/TPEx/MOPS as primary providers.
[!] Official data.gov.tw Public Open Data only.
[!] Research supplement only. Not market price data.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, Optional, Tuple

from data.providers.data_gov_tw.models_v143 import FetchStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
DATA_GOV_TW_REALTIME_AVAILABLE = False
DATA_GOV_TW_BROKER_EXECUTION_AVAILABLE = False
DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED = False
DATA_GOV_TW_MOCK_FALLBACK_ENABLED = False
DATA_GOV_TW_OFFICIAL_SOURCE_ONLY = True
DATA_GOV_TW_CAN_OVERRIDE_PRIMARY_PROVIDER = False
DATA_GOV_TW_ALLOWLIST_REQUIRED = True
DATA_GOV_TW_FORMAL_USE_REQUIRES_APPROVAL = True
DATA_GOV_TW_AUTO_DISCOVERY_ENABLED = False


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class _ProviderMetadata:
    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}


class DataGovTwProviderV143:
    """
    Official Taiwan Government Open Data Platform Provider v1.4.3.

    Scope:
    - Government open data catalog and metadata
    - Research supplement for macro, trade, industry, energy, policy domains
    - Dataset allowlist, license validation, schema contracts
    - NOT a broker. NOT market price data. NOT financial statements.
    - Cannot override TWSE/TPEx/MOPS as primary providers.
    - No realtime. No mock fallback. No auto-download. No auto-discovery.
    """

    provider_id = "data_gov_tw_official"
    provider_name = "Taiwan Government Open Data Platform"
    data_domain = "government_open_data"
    official = True
    requires_auth = False
    supports_real_mode = True
    supports_mock_mode = True  # For testing only
    mock_formal_conclusion_allowed = False
    broker_provider = False
    order_execution_supported = False
    realtime_supported = False
    auto_discovery_supported = False
    auto_download_default = False
    can_override_primary_provider = False

    # Safety flags
    DATA_GOV_TW_REALTIME_AVAILABLE = False
    DATA_GOV_TW_BROKER_EXECUTION_AVAILABLE = False
    DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED = False
    DATA_GOV_TW_MOCK_FALLBACK_ENABLED = False
    DATA_GOV_TW_CAN_OVERRIDE_PRIMARY_PROVIDER = False
    DATA_GOV_TW_AUTO_DISCOVERY_ENABLED = False

    def get_metadata(self) -> _ProviderMetadata:
        return _ProviderMetadata(
            provider_id=self.provider_id,
            provider_name=self.provider_name,
            data_domain=self.data_domain,
            official=self.official,
            requires_auth=self.requires_auth,
            supports_real_mode=self.supports_real_mode,
            supports_mock_mode=self.supports_mock_mode,
            mock_formal_conclusion_allowed=self.mock_formal_conclusion_allowed,
            broker_provider=self.broker_provider,
            order_execution_supported=self.order_execution_supported,
            realtime_supported=self.realtime_supported,
            can_override_primary_provider=self.can_override_primary_provider,
            no_real_orders=True,
            broker_execution_enabled=False,
            production_trading_blocked=True,
            mock_fallback_enabled=False,
            auto_download_enabled=False,
            auto_discovery_enabled=False,
        )

    def get_capability_matrix(self) -> Dict[str, Any]:
        from data.providers.data_gov_tw.capabilities_v143 import DataGovTwCapabilityMatrix
        return DataGovTwCapabilityMatrix().build_summary()

    def get_endpoint_registry(self):
        from data.providers.data_gov_tw.endpoints_v143 import DataGovTwEndpointRegistry
        return DataGovTwEndpointRegistry()

    def is_capability_supported(self, capability: str) -> bool:
        from data.providers.data_gov_tw.capabilities_v143 import DataGovTwCapabilityMatrix
        return DataGovTwCapabilityMatrix().is_supported(capability)

    def health_check(self) -> Dict[str, Any]:
        from data.providers.data_gov_tw.health_v143 import DataGovTwProviderHealthCheck
        return DataGovTwProviderHealthCheck().get_health_summary()

    def fetch_dataset_metadata(
        self,
        dataset_id: str,
        transport: Optional[Callable] = None,
        dry_run: bool = True,
    ) -> Tuple[FetchStatus, Optional[Dict[str, Any]], Dict[str, Any]]:
        """
        Fetch metadata for a dataset from data.gov.tw.
        dry_run=True by default — does not write to database.
        NEVER falls back to mock.
        """
        from data.providers.data_gov_tw.allowlist_v143 import DataGovTwAllowlist
        from data.providers.data_gov_tw.client_v143 import DataGovTwHttpClient
        from data.providers.data_gov_tw.endpoints_v143 import DataGovTwEndpointRegistry

        allowlist = DataGovTwAllowlist()
        if not allowlist.is_allowlisted(dataset_id):
            return (
                FetchStatus.NOT_ALLOWLISTED,
                None,
                {
                    "dataset_id": dataset_id,
                    "result": "DATASET_NOT_ALLOWLISTED",
                    "dry_run": dry_run,
                    "warnings": ["Dataset not in allowlist. Metadata inspection only."],
                },
            )

        reg = DataGovTwEndpointRegistry()
        ep = reg.get("dataset_metadata")
        if ep is None or not ep.enabled:
            return (
                FetchStatus.BLOCKED,
                None,
                {"error": "Dataset metadata endpoint not available", "dry_run": dry_run},
            )

        url = ep.path.replace("{dataset_id}", dataset_id)
        client = DataGovTwHttpClient(transport=transport)
        status, data, prov = client.get_json(url)
        prov["dry_run"] = dry_run
        prov["dataset_id"] = dataset_id
        return status, data, prov
