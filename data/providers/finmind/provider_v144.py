"""
data/providers/finmind/provider_v144.py — FinMind Adapter v1.4.4 main provider.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SECONDARY_AGGREGATOR. official=False. can_override_primary_provider=False.
[!] silent_fallback_enabled=False. mock_fallback_enabled=False.
[!] No broker. No order execution. No formal realtime.
[!] Token optional. No token in logs.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FINMIND_SILENT_FALLBACK_ENABLED = False
FINMIND_MOCK_FALLBACK_ENABLED = False
FINMIND_AUTO_DOWNLOAD_ENABLED = False
FINMIND_AUTO_DISCOVERY_ENABLED = False
FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER = False
FINMIND_REALTIME_FORMAL_USE_ALLOWED = False
FINMIND_BROKER_EXECUTION_AVAILABLE = False
FINMIND_TOKEN_OPTIONAL = True
FINMIND_DATASET_ALLOWLIST_REQUIRED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class FinMindAdapterV144:
    """
    FinMind Secondary Financial Data Aggregator v1.4.4.

    Scope:
    - Secondary supplement for daily OHLCV, institutional, margin, revenue, financials
    - API v4, quota tracking, schema drift detection, conflict detection, PIT guards
    - NOT a broker. NOT a primary source. Cannot override TWSE/TPEx/MOPS.
    - No realtime formal use. No silent/mock fallback. No auto-download.
    - Token optional (anonymous mode supported).
    """

    provider_id = "finmind"
    provider_name = "FinMind Secondary Financial Data Aggregator"
    authoritative_level = "SECONDARY_AGGREGATOR"
    official = False
    aggregator = True
    requires_auth = False
    supports_real_mode = True
    supports_mock_mode = True
    mock_formal_conclusion_allowed = False
    can_override_primary_provider = False
    silent_fallback_enabled = False
    broker_provider = False
    order_execution_supported = False
    formal_realtime_supported = False

    # Safety flags (accessible as class attributes for tests)
    FINMIND_SILENT_FALLBACK_ENABLED = False
    FINMIND_MOCK_FALLBACK_ENABLED = False
    FINMIND_AUTO_DOWNLOAD_ENABLED = False
    FINMIND_AUTO_DISCOVERY_ENABLED = False
    FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER = False
    FINMIND_REALTIME_FORMAL_USE_ALLOWED = False
    FINMIND_BROKER_EXECUTION_AVAILABLE = False

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._transport = transport
        self._query: Any = None

    def _get_query(self):
        if self._query is None:
            from data.providers.finmind.query_v144 import FinMindQueryService
            self._query = FinMindQueryService(transport=self._transport)
        return self._query

    def health_check(self) -> Dict[str, Any]:
        from data.providers.finmind.health_v144 import FinMindAdapterHealthCheck
        return FinMindAdapterHealthCheck().get_health_summary()

    def get_capabilities(self) -> List[Dict[str, Any]]:
        from data.providers.finmind.capabilities_v144 import get_capabilities
        return get_capabilities()

    def get_allowlist_summary(self) -> Dict[str, Any]:
        from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist
        return FinMindDatasetAllowlist().summary()

    def get_auth_summary(self) -> Dict[str, Any]:
        from data.providers.finmind.auth_v144 import FinMindAuthManager
        return FinMindAuthManager().get_auth_summary()

    def get_quota_status(self) -> Dict[str, Any]:
        return self._get_query().get_quota_status()

    def get_schema(self, dataset: str) -> Optional[Dict[str, Any]]:
        return self._get_query().get_dataset_schema(dataset)

    def get_schema_drift(self, dataset: str) -> Dict[str, Any]:
        return self._get_query().get_schema_drift_status(dataset)

    def fetch_price(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self._get_query().get_price(symbol, start_date, end_date)

    def fetch_institutional(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self._get_query().get_institutional(symbol, start_date, end_date)

    def fetch_margin(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self._get_query().get_margin(symbol, start_date, end_date)

    def fetch_records(
        self,
        dataset: str,
        data_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self._get_query().get_records(dataset, data_id, start_date, end_date)

    def compare_with_primary(
        self,
        dataset: str,
        symbol: str,
        primary_records: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        return self._get_query().compare_with_primary(dataset, symbol, primary_records)

    def get_conflicts(self) -> List[Dict[str, Any]]:
        return self._get_query().get_conflicts()

    def get_provider_lineage(self) -> Dict[str, Any]:
        return self._get_query().get_provider_lineage()

    def summarize_coverage(self) -> Dict[str, Any]:
        return self._get_query().summarize_coverage()

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "provider_name": self.provider_name,
            "authoritative_level": self.authoritative_level,
            "official": self.official,
            "aggregator": self.aggregator,
            "requires_auth": self.requires_auth,
            "supports_real_mode": self.supports_real_mode,
            "supports_mock_mode": self.supports_mock_mode,
            "mock_formal_conclusion_allowed": self.mock_formal_conclusion_allowed,
            "can_override_primary_provider": self.can_override_primary_provider,
            "silent_fallback_enabled": self.silent_fallback_enabled,
            "broker_provider": self.broker_provider,
            "order_execution_supported": self.order_execution_supported,
            "formal_realtime_supported": self.formal_realtime_supported,
            "no_real_orders": True,
            "broker_execution_enabled": False,
            "production_trading_blocked": True,
        }
