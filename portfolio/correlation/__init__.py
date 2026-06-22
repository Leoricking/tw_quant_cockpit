"""
portfolio/correlation/__init__.py — Correlation & Exposure module v1.5.2.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No Broker Connection. No Auto Rebalance. No Optimization.
[!] CORRELATION_EXPOSURE_RESEARCH_ONLY = True. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.5.2"
RELEASE_NAME = "Correlation & Exposure"
RESEARCH_ONLY = True

# ---------------------------------------------------------------------------
# Feature availability flags
# ---------------------------------------------------------------------------
CORRELATION_EXPOSURE_AVAILABLE           = True
CORRELATION_EXPOSURE_RESEARCH_ONLY       = True

# ---------------------------------------------------------------------------
# Explicitly disabled features — FIXED, never negotiable
# ---------------------------------------------------------------------------
PORTFOLIO_OPTIMIZATION_AVAILABLE         = False
EFFICIENT_FRONTIER_AVAILABLE             = False
BLACK_LITTERMAN_AVAILABLE                = False
RISK_PARITY_AUTO_ALLOCATION_AVAILABLE    = False

CORRELATION_AUTO_REBALANCE_ENABLED       = False
CORRELATION_AUTO_REDUCTION_ENABLED       = False
CORRELATION_ORDER_CREATION_ENABLED       = False
CORRELATION_ORDER_EXECUTION_ENABLED      = False
CORRELATION_BROKER_ENABLED               = False
CORRELATION_LIVE_ACCOUNT_SYNC_ENABLED    = False
CORRELATION_HEDGING_EXECUTION_ENABLED    = False

NO_REAL_ORDERS                           = True
BROKER_EXECUTION_ENABLED                 = False
PRODUCTION_TRADING_BLOCKED               = True

# Every analysis result must carry these labels
RESULT_LABELS = [
    "RESEARCH_ONLY",
    "DESCRIPTIVE_ANALYTICS_ONLY",
    "NOT_AN_OPTIMIZATION",
    "NOT_A_REBALANCE_INSTRUCTION",
    "NOT_AN_ORDER",
    "NO_BROKER_CALL",
    "NO_LEDGER_WRITE",
]
