"""
local_assistant/__init__.py — Local Research Assistant package for TW Quant Cockpit v1.0.8.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Local Research Assistant. No external API. No broker execution.
[!] Local assistant does not enable trading.
"""
from __future__ import annotations

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True
LOCAL_ONLY = True
EXTERNAL_API_DISABLED = True
ASSISTANT_DOES_NOT_ENABLE_TRADING = True
PRODUCTION_TRADING_BLOCKED = True

__all__ = [
    "NO_REAL_ORDERS", "BROKER_DISABLED", "RESEARCH_ONLY",
    "LOCAL_ONLY", "EXTERNAL_API_DISABLED",
    "ASSISTANT_DOES_NOT_ENABLE_TRADING", "PRODUCTION_TRADING_BLOCKED",
]
