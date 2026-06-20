"""
data/providers/data_gov_tw/capabilities_v143.py — data.gov.tw capability matrix v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] DATA_GOV_TW_REALTIME_AVAILABLE = False.
[!] DATA_GOV_TW_BROKER_EXECUTION_AVAILABLE = False.
[!] Cannot override TWSE/TPEx/MOPS as primary providers.
"""
from __future__ import annotations

from typing import Any, Dict

from data.providers.data_gov_tw.models_v143 import DataGovTwCapability

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_SUPPORTED = {
    DataGovTwCapability.DATASET_CATALOG,
    DataGovTwCapability.DATASET_METADATA,
    DataGovTwCapability.DATASET_RESOURCE,
    DataGovTwCapability.JSON_RESOURCE,
    DataGovTwCapability.CSV_RESOURCE,
    DataGovTwCapability.XML_RESOURCE,
    DataGovTwCapability.ZIP_RESOURCE,
    DataGovTwCapability.OAS_API_RESOURCE,
    DataGovTwCapability.LICENSE_VALIDATION,
    DataGovTwCapability.SCHEMA_CONTRACT,
    DataGovTwCapability.DATASET_REVISION,
    DataGovTwCapability.SOURCE_LINEAGE,
    DataGovTwCapability.UPDATE_FREQUENCY,
    DataGovTwCapability.MACRO_DATA,
    DataGovTwCapability.INDUSTRY_DATA,
    DataGovTwCapability.TRADE_DATA,
    DataGovTwCapability.ENERGY_DATA,
    DataGovTwCapability.POLICY_DATA,
    DataGovTwCapability.CORPORATE_REGISTRY_SUPPLEMENT,
}

# These are explicitly not supported — declared to make the matrix complete
_NOT_DECLARED = {
    "MARKET_PRICE",
    "OFFICIAL_STOCK_PRICE",
    "FINANCIAL_STATEMENTS",
    "REALTIME_QUOTE",
    "ORDER_BOOK",
    "TICK",
    "BROKER_ACCOUNT",
    "ORDER_EXECUTION",
    "DAILY_OHLCV",
    "MARGIN",
    "INSTITUTIONAL",
}


class DataGovTwCapabilityMatrix:
    """Capability matrix for the data.gov.tw provider."""

    def get_capability_status(self, capability: Any) -> Dict[str, Any]:
        if isinstance(capability, str):
            try:
                capability = DataGovTwCapability(capability)
            except ValueError:
                if capability in _NOT_DECLARED:
                    return {
                        "status": "NOT_APPLICABLE",
                        "supported": False,
                        "broker": False,
                        "reason": "data.gov.tw does not provide market/broker data",
                    }
                return {
                    "status": "UNSUPPORTED",
                    "supported": False,
                    "broker": False,
                    "reason": "Not a data.gov.tw capability",
                }
        if capability in _SUPPORTED:
            return {"status": "SUPPORTED", "supported": True, "broker": False}
        return {"status": "UNSUPPORTED", "supported": False, "broker": False}

    def is_supported(self, capability: Any) -> bool:
        if isinstance(capability, str):
            try:
                capability = DataGovTwCapability(capability)
            except ValueError:
                return False
        return capability in _SUPPORTED

    def is_broker_capability(self, capability: Any) -> bool:
        """Always False — data.gov.tw is open-data only, never broker."""
        return False

    def build_summary(self) -> Dict[str, Any]:
        caps: Dict[str, Any] = {}
        for cap in DataGovTwCapability:
            caps[cap.value] = self.get_capability_status(cap)
        return {
            "provider": "data_gov_tw_official",
            "official_source": True,
            "no_real_orders": True,
            "broker_execution_enabled": False,
            "realtime_available": False,
            "can_override_primary_provider": False,
            "data_type": "government_open_data",
            "capabilities": caps,
            "not_applicable": sorted(_NOT_DECLARED),
            "supported_count": len(_SUPPORTED),
            "not_applicable_count": len(_NOT_DECLARED),
        }
