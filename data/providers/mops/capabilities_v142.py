"""
data/providers/mops/capabilities_v142.py — MOPS capability matrix v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

from typing import Any, Dict

from data.providers.mops.models_v142 import MOPSCapability

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_SUPPORTED = {
    MOPSCapability.COMPANY_PROFILE,
    MOPSCapability.MONTHLY_REVENUE,
    MOPSCapability.FINANCIAL_REPORT_ANNOUNCEMENT,
    MOPSCapability.BALANCE_SHEET,
    MOPSCapability.INCOME_STATEMENT,
    MOPSCapability.CASH_FLOW,
    MOPSCapability.EQUITY_STATEMENT_INDEX,
    MOPSCapability.MATERIAL_INFORMATION,
    MOPSCapability.INVESTOR_CONFERENCE,
    MOPSCapability.XBRL_DOCUMENT_INDEX,
    MOPSCapability.REVISION_LINEAGE,
    MOPSCapability.POINT_IN_TIME_AVAILABILITY,
    MOPSCapability.DERIVED_FINANCIAL_METRICS,
}

_UNSUPPORTED = {
    "REALTIME_QUOTE",
    "ORDER_BOOK",
    "TICK",
    "BROKER_ACCOUNT",
    "ORDER_EXECUTION",
    "DAILY_OHLCV",
    "MARGIN",
}


class MOPSCapabilityMatrix:
    """Capability matrix for the MOPS provider."""

    def get_capability_status(self, capability: Any) -> Dict[str, Any]:
        if isinstance(capability, str):
            try:
                capability = MOPSCapability(capability)
            except ValueError:
                return {"status": "UNSUPPORTED", "supported": False, "broker": False, "reason": "Not a MOPS capability"}
        if capability in _SUPPORTED:
            return {"status": "SUPPORTED", "supported": True, "broker": False}
        return {"status": "UNSUPPORTED", "supported": False, "broker": False}

    def is_supported(self, capability: Any) -> bool:
        if isinstance(capability, str):
            try:
                capability = MOPSCapability(capability)
            except ValueError:
                return False
        return capability in _SUPPORTED

    def is_broker_capability(self, capability: Any) -> bool:
        """Always False for MOPS — MOPS is data-only, never broker."""
        return False

    def build_summary(self) -> Dict[str, Any]:
        # Only include MOPSCapability enum values — not-applicable market-data capabilities
        # (DAILY_OHLCV, MARGIN, etc.) are excluded because MOPS is financial disclosure only.
        caps: Dict[str, Any] = {}
        for cap in MOPSCapability:
            caps[cap.value] = self.get_capability_status(cap)
        return {
            "provider": "mops_official",
            "official_source": True,
            "no_real_orders": True,
            "broker_execution_enabled": False,
            "realtime_available": False,
            "data_type": "financial_disclosure",
            "capabilities": caps,
            "not_applicable": sorted(_UNSUPPORTED),
            "supported_count": len(_SUPPORTED),
            "unsupported_count": len(_UNSUPPORTED),
        }
