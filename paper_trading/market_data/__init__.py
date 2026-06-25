"""
paper_trading/market_data/__init__.py — Market Data Session Adapter v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
[!] MARKET_DATA_ONLY. No broker API. No credential storage.
"""
from __future__ import annotations

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
NO_BROKER_API: bool = True
NO_CREDENTIAL_STORAGE: bool = True
LIVE_TO_FIXTURE_FALLBACK_DISABLED: bool = True
LIVE_TO_OFFLINE_FALLBACK_DISABLED: bool = True
UNKNOWN_SOURCE_AS_LIVE_DISABLED: bool = True
SILENT_FIXTURE_FALLBACK_DISABLED: bool = True
RESEARCH_ONLY: bool = True
SIMULATION_ONLY: bool = True
MARKET_DATA_SESSION_RELEASE: bool = True
MARKET_DATA_SESSION_AVAILABLE: bool = True
MARKET_DATA_SESSION_VERSION: str = "1.6.1"

assert NO_REAL_ORDERS is True
assert BROKER_EXECUTION_ENABLED is False
assert PRODUCTION_TRADING_BLOCKED is True
assert MARKET_DATA_ONLY is True
assert NO_BROKER_API is True
assert LIVE_TO_FIXTURE_FALLBACK_DISABLED is True
assert LIVE_TO_OFFLINE_FALLBACK_DISABLED is True
assert UNKNOWN_SOURCE_AS_LIVE_DISABLED is True
assert SILENT_FIXTURE_FALLBACK_DISABLED is True
