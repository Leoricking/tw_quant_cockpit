"""
portfolio/risk_controls/__init__.py — Drawdown & Risk Controls module v1.5.3.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No Broker Connection. No Auto Rebalance. No Optimization.
[!] RISK_CONTROL_RESEARCH_ONLY = True. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.5.3"
RELEASE_NAME = "Drawdown & Risk Controls"
RESEARCH_ONLY = True

# ---------------------------------------------------------------------------
# Feature availability flags
# ---------------------------------------------------------------------------
DRAWDOWN_RISK_CONTROLS_AVAILABLE         = True
DRAWDOWN_RISK_CONTROLS_RESEARCH_ONLY     = True

# ---------------------------------------------------------------------------
# Explicitly disabled features — FIXED, never negotiable
# ---------------------------------------------------------------------------
RISK_CONTROL_RESEARCH_ONLY               = True
RISK_CONTROL_AUTO_APPLY_ENABLED          = False
RISK_CONTROL_AUTO_REDUCE_ENABLED         = False
RISK_CONTROL_AUTO_STOP_ENABLED           = False
RISK_CONTROL_AUTO_REBALANCE_ENABLED      = False
RISK_CONTROL_ORDER_CREATION_ENABLED      = False
RISK_CONTROL_ORDER_EXECUTION_ENABLED     = False
RISK_CONTROL_BROKER_ENABLED              = False
RISK_CONTROL_HEDGING_EXECUTION_ENABLED   = False
RISK_CONTROL_LEDGER_WRITE_ENABLED        = False
RISK_CONTROL_LIVE_ACCOUNT_SYNC_ENABLED   = False

NO_REAL_ORDERS                           = True
BROKER_EXECUTION_ENABLED                 = False
PRODUCTION_TRADING_BLOCKED               = True

# Every analysis result must carry these labels
RESULT_LABELS = [
    "RESEARCH_ONLY",
    "DESCRIPTIVE_ANALYTICS_ONLY",
    "NOT_AN_AUTOMATED_CONTROL",
    "NOT_A_STOP_ORDER",
    "NOT_AN_ORDER",
    "NO_BROKER_CALL",
    "NO_LEDGER_WRITE",
    "NOT_A_REBALANCE_INSTRUCTION",
]
