"""
paper_trading/performance_attribution/__init__.py
Paper Performance Attribution v1.6.7.
[!] PAPER ATTRIBUTION ONLY. RESEARCH ONLY. NO REAL ORDERS. NO BROKER.
[!] DETERMINISTIC. READ-ONLY. NOT FOR PRODUCTION. NOT INVESTMENT ADVICE.
[!] Paper trading, simulated trading, historical replay, research portfolio only.
[!] All attribution is SIMULATION_ONLY. NOT_A_REAL_PERFORMANCE_RECORD.
[!] NO_BROKER_CALL. NO_REAL_ACCOUNT. NO_FORMAL_LEDGER_WRITE.
"""
from __future__ import annotations

VERSION = "1.6.7"
RELEASE_NAME = "Paper Performance Attribution"
BASE_RELEASE = "1.6.6.2 Replay Session Lineage Handler Integrity Hotfix"

# ── Safety flags ─────────────────────────────────────────────────────────────
PAPER_ATTRIBUTION_AVAILABLE             = True
PAPER_ATTRIBUTION_RESEARCH_ONLY        = True
PAPER_ATTRIBUTION_PAPER_ONLY           = True
PAPER_ATTRIBUTION_DETERMINISTIC        = True
PAPER_ATTRIBUTION_READ_ONLY            = True

REAL_PERFORMANCE_ATTRIBUTION_ENABLED   = False
BROKER_ATTRIBUTION_ENABLED             = False
REAL_ACCOUNT_ATTRIBUTION_ENABLED       = False
REAL_ORDER_ATTRIBUTION_ENABLED         = False
PRODUCTION_LEDGER_ATTRIBUTION_ENABLED  = False
LIVE_EXECUTION_ATTRIBUTION_ENABLED     = False
PRODUCTION_PORTFOLIO_ATTRIBUTION_ENABLED = False
AUTO_CAPITAL_REALLOCATION_ENABLED      = False
AUTO_RISK_OVERRIDE_ENABLED             = False
AUTO_SESSION_CONTROL_ENABLED           = False
EXTERNAL_ATTRIBUTION_SERVICE_ENABLED   = False
EXTERNAL_ATTRIBUTION_DB_ENABLED        = False
NETWORK_ATTRIBUTION_ENABLED            = False

# ── Preserved safety flags from paper_trading foundation ─────────────────────
NO_REAL_ORDERS                         = True
BROKER_EXECUTION_ENABLED               = False
PRODUCTION_TRADING_BLOCKED             = True
