"""
data/providers/tpex/capabilities_v141.py — TPEx capability matrix v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
"""
from __future__ import annotations

from typing import Any, Dict

from data.providers.tpex.models_v141 import TPExCapability

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_SUPPORTED = {
    TPExCapability.SECURITY_MASTER,
    TPExCapability.DAILY_OHLCV,
    TPExCapability.DAILY_TRADING_SUMMARY,
    TPExCapability.INSTITUTIONAL,
    TPExCapability.MARGIN,
    TPExCapability.MARKET_INDEX,
    TPExCapability.TRADING_CALENDAR,
    TPExCapability.SUSPENSION_RESUMPTION,
    TPExCapability.CORPORATE_ACTIONS,
    TPExCapability.VALUATION,
}

_UNSUPPORTED = {
    "REALTIME_QUOTE",
    "ORDER_BOOK",
    "TICK",
    "BROKER_ACCOUNT",
    "ORDER_EXECUTION",
}


class TPExCapabilityMatrix:
    """Capability matrix for the TPEx provider."""

    def get_capability_status(self, capability: Any) -> Dict[str, Any]:
        if isinstance(capability, str):
            try:
                capability = TPExCapability(capability)
            except ValueError:
                return {"status": "UNSUPPORTED", "supported": False, "broker": False, "reason": "Not a TPEx capability"}
        if capability in _SUPPORTED:
            return {"status": "SUPPORTED", "supported": True, "broker": False}
        return {"status": "UNSUPPORTED", "supported": False, "broker": False}

    def is_supported(self, capability: Any) -> bool:
        if isinstance(capability, str):
            try:
                capability = TPExCapability(capability)
            except ValueError:
                return False
        return capability in _SUPPORTED

    def is_broker_capability(self, capability: Any) -> bool:
        """Always False for TPEx — TPEx is data-only, never broker."""
        return False

    def build_summary(self) -> Dict[str, Any]:
        caps: Dict[str, Any] = {}
        for cap in TPExCapability:
            caps[cap.value] = self.get_capability_status(cap)
        for cap in _UNSUPPORTED:
            caps[cap] = {"status": "UNSUPPORTED", "supported": False, "broker": False}
        return {
            "provider": "tpex_official",
            "official_source": True,
            "no_real_orders": True,
            "broker_execution_enabled": False,
            "realtime_available": False,
            "board_scope": "MAINBOARD",
            "capabilities": caps,
            "supported_count": len(_SUPPORTED),
            "unsupported_count": len(_UNSUPPORTED),
        }
