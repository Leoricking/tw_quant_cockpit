"""
data/providers/tpex — TPEx Official Public Data Provider v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
"""
from __future__ import annotations

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
TPEX_REALTIME_AVAILABLE = False
TPEX_BROKER_EXECUTION_AVAILABLE = False
TPEX_AUTO_DOWNLOAD_ENABLED = False
TPEX_MOCK_FALLBACK_ENABLED = False
OFFICIAL_SOURCE_ONLY = True
BOARD_SCOPE = "MAINBOARD"
