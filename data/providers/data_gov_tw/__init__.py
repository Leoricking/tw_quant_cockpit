"""
data/providers/data_gov_tw — Taiwan Government Open Data Platform Provider v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] DATA_GOV_TW_REALTIME_AVAILABLE = False.
[!] DATA_GOV_TW_BROKER_EXECUTION_AVAILABLE = False.
[!] DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED = False.
[!] DATA_GOV_TW_MOCK_FALLBACK_ENABLED = False.
[!] Official data.gov.tw Public Data Only. Research supplement. No broker.
[!] Cannot override TWSE/TPEx/MOPS as primary providers.
"""
from __future__ import annotations

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
DATA_GOV_TW_MOCK_FALLBACK_ENABLED = False
DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED = False
DATA_GOV_TW_REALTIME_AVAILABLE = False
DATA_GOV_TW_BROKER_EXECUTION_AVAILABLE = False
DATA_GOV_TW_OFFICIAL_SOURCE_ONLY = True
DATA_GOV_TW_CAN_OVERRIDE_PRIMARY_PROVIDER = False
DATA_GOV_TW_ALLOWLIST_REQUIRED = True
