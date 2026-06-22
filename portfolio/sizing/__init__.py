"""
portfolio/sizing/__init__.py — Position Sizing module v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No Broker Connection. No Auto Apply. No Auto Rebalance.
[!] POSITION_SIZING_RESEARCH_ONLY = True. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.5.1"
RELEASE_NAME = "Position Sizing"

# ---------------------------------------------------------------------------
# Safety constants — FIXED, never negotiable
# ---------------------------------------------------------------------------
POSITION_SIZING_AVAILABLE              = True
POSITION_SIZING_RESEARCH_ONLY         = True
POSITION_SIZING_ORDER_CREATION_ENABLED = False
POSITION_SIZING_ORDER_EXECUTION_ENABLED = False
POSITION_SIZING_BROKER_ENABLED        = False
POSITION_SIZING_AUTO_REBALANCE_ENABLED = False
POSITION_SIZING_AUTO_APPLY_ENABLED    = False
POSITION_SIZING_LIVE_ACCOUNT_SYNC_ENABLED = False
POSITION_SIZING_MARGIN_ENABLED        = False
POSITION_SIZING_SHORT_SELL_ENABLED    = False
POSITION_SIZING_LEVERAGE_ENABLED      = False
POSITION_SIZING_KELLY_FULL_ENABLED    = False

NO_REAL_ORDERS                        = True
BROKER_EXECUTION_ENABLED              = False
PRODUCTION_TRADING_BLOCKED            = True

# Every sizing result must carry these labels
RESULT_LABELS = [
    "RESEARCH_ONLY",
    "NOT_AN_ORDER",
    "NOT_EXECUTABLE",
    "NO_BROKER_CALL",
    "NO_LEDGER_WRITE",
    "NO_AUTO_REBALANCE",
]
