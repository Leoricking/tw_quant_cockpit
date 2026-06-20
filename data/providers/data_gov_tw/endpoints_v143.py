"""
data/providers/data_gov_tw/endpoints_v143.py — data.gov.tw endpoint registry v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official data.gov.tw API endpoints only. No third-party mirrors.
[!] DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED = False.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_DATA_GOV_TW_BASE = "https://data.gov.tw"
_DATA_GOV_TW_API_BASE = "https://data.gov.tw/api/v2"


@dataclass
class DataGovTwEndpoint:
    """Definition of a single data.gov.tw API endpoint."""
    endpoint_id: str
    official_name: str
    path: str
    method: str  # GET or POST
    response_format: str  # JSON, CSV, XML
    description: str = ""
    query_params: List[str] = field(default_factory=list)
    pagination_supported: bool = False
    auth_required: bool = False
    rate_limit_per_minute: int = 30
    cache_ttl_seconds: int = 3600
    enabled: bool = True
    official: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class DataGovTwEndpointRegistry:
    """Registry of all data.gov.tw API endpoints."""

    def __init__(self) -> None:
        self._endpoints: Dict[str, DataGovTwEndpoint] = {}
        self._register_all()

    def _register_all(self) -> None:
        endpoints = [
            DataGovTwEndpoint(
                endpoint_id="dataset_catalog",
                official_name="data.gov.tw Dataset Catalog",
                path=f"{_DATA_GOV_TW_API_BASE}/dataset",
                method="GET",
                response_format="JSON",
                description="List datasets from data.gov.tw catalog",
                query_params=["keyword", "size", "page", "categoryId", "organizationId"],
                pagination_supported=True,
                auth_required=False,
                rate_limit_per_minute=30,
                cache_ttl_seconds=3600,
            ),
            DataGovTwEndpoint(
                endpoint_id="dataset_metadata",
                official_name="data.gov.tw Dataset Metadata",
                path=f"{_DATA_GOV_TW_API_BASE}/dataset/{{dataset_id}}",
                method="GET",
                response_format="JSON",
                description="Get metadata for a single dataset",
                query_params=["dataset_id"],
                pagination_supported=False,
                auth_required=False,
                rate_limit_per_minute=30,
                cache_ttl_seconds=3600,
            ),
            DataGovTwEndpoint(
                endpoint_id="resource_list",
                official_name="data.gov.tw Dataset Resources",
                path=f"{_DATA_GOV_TW_API_BASE}/dataset/{{dataset_id}}/resource",
                method="GET",
                response_format="JSON",
                description="List downloadable resources for a dataset",
                query_params=["dataset_id"],
                pagination_supported=False,
                auth_required=False,
                rate_limit_per_minute=30,
                cache_ttl_seconds=3600,
            ),
            DataGovTwEndpoint(
                endpoint_id="organization_list",
                official_name="data.gov.tw Organization List",
                path=f"{_DATA_GOV_TW_API_BASE}/organization",
                method="GET",
                response_format="JSON",
                description="List provider agencies/organizations",
                query_params=["size", "page"],
                pagination_supported=True,
                auth_required=False,
                rate_limit_per_minute=30,
                cache_ttl_seconds=86400,
            ),
            DataGovTwEndpoint(
                endpoint_id="category_list",
                official_name="data.gov.tw Category List",
                path=f"{_DATA_GOV_TW_API_BASE}/category",
                method="GET",
                response_format="JSON",
                description="List dataset categories",
                query_params=[],
                pagination_supported=False,
                auth_required=False,
                rate_limit_per_minute=30,
                cache_ttl_seconds=86400,
            ),
        ]
        for ep in endpoints:
            self._endpoints[ep.endpoint_id] = ep

    def get(self, endpoint_id: str) -> Optional[DataGovTwEndpoint]:
        return self._endpoints.get(endpoint_id)

    def list_all(self) -> List[DataGovTwEndpoint]:
        return list(self._endpoints.values())

    def list_enabled(self) -> List[DataGovTwEndpoint]:
        return [ep for ep in self._endpoints.values() if ep.enabled]
