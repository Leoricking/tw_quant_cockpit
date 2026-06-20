"""
data/providers/twse/capabilities_v140.py — TWSE capability matrix v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

from typing import Any, Dict

from data.providers.twse.models_v140 import TWSECapability

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_SUPPORTED = {
    TWSECapability.SECURITY_MASTER,
    TWSECapability.DAILY_OHLCV,
    TWSECapability.DAILY_TRADING_SUMMARY,
    TWSECapability.INSTITUTIONAL,
    TWSECapability.MARGIN,
    TWSECapability.MARKET_INDEX,
    TWSECapability.TRADING_CALENDAR,
    TWSECapability.CORPORATE_ACTIONS,
    TWSECapability.VALUATION,
}

_UNSUPPORTED = {
    "REALTIME_QUOTE",
    "ORDER_BOOK",
    "TICK",
    "BROKER_ACCOUNT",
    "ORDER_EXECUTION",
}


class TWSECapabilityMatrix:
    """Capability matrix for the TWSE provider."""

    def get_capability_status(self, capability: Any) -> Dict[str, Any]:
        if isinstance(capability, str):
            try:
                capability = TWSECapability(capability)
            except ValueError:
                return {"status": "UNSUPPORTED", "supported": False, "broker": False, "reason": "Not a TWSE capability"}
        if capability in _SUPPORTED:
            return {"status": "SUPPORTED", "supported": True, "broker": False}
        return {"status": "UNSUPPORTED", "supported": False, "broker": False}

    def is_supported(self, capability: Any) -> bool:
        if isinstance(capability, str):
            try:
                capability = TWSECapability(capability)
            except ValueError:
                return False
        return capability in _SUPPORTED

    def is_broker_capability(self, capability: Any) -> bool:
        """Always False for TWSE — TWSE is data-only, never broker."""
        return False

    def build_summary(self) -> Dict[str, Any]:
        caps: Dict[str, Any] = {}
        for cap in TWSECapability:
            caps[cap.value] = self.get_capability_status(cap)
        for cap in _UNSUPPORTED:
            caps[cap] = {"status": "UNSUPPORTED", "supported": False, "broker": False}
        return {
            "provider": "twse_official",
            "official_source": True,
            "no_real_orders": True,
            "broker_execution_enabled": False,
            "realtime_available": False,
            "capabilities": caps,
            "supported_count": len(_SUPPORTED),
            "unsupported_count": len(_UNSUPPORTED),
        }
