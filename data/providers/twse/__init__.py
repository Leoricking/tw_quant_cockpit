"""
data/providers/twse — TWSE Official Public Data Provider v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only.
"""
from __future__ import annotations

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
TWSE_REALTIME_AVAILABLE = False
TWSE_BROKER_EXECUTION_AVAILABLE = False
TWSE_AUTO_DOWNLOAD_ENABLED = False
TWSE_MOCK_FALLBACK_ENABLED = False
OFFICIAL_SOURCE_ONLY = True
