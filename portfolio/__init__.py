"""
portfolio/__init__.py — Portfolio Research Foundation v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No Broker Connection. No Auto Rebalance. No Position Sizing.
"""
from __future__ import annotations

VERSION = "1.5.0"
RELEASE_NAME = "Portfolio Research Foundation"

# Safety flags — ALWAYS these values
RESEARCH_ONLY                       = True
BROKER_LINKED                       = False
REAL_ORDER_ENABLED                  = False
POSITION_SIZING_AVAILABLE           = False
OPTIMIZATION_AVAILABLE              = False
AUTO_REBALANCE_ENABLED              = False
ORDER_EXECUTION_ENABLED             = False
BROKER_SYNC_ENABLED                 = False
LIVE_ACCOUNT_IMPORT_ENABLED         = False
REAL_TRADING_ENABLED                = False

NO_REAL_ORDERS                      = True
BROKER_EXECUTION_ENABLED            = False
PRODUCTION_TRADING_BLOCKED          = True
