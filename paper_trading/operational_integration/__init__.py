"""
paper_trading/operational_integration/__init__.py
Operational Integration Hardening v1.6.8.
[!] OPERATIONAL INTEGRATION ONLY. RESEARCH ONLY. NO REAL ORDERS. NO BROKER.
[!] DETERMINISTIC. READ-ONLY. NOT FOR PRODUCTION. NOT INVESTMENT ADVICE.
[!] Paper trading, simulated trading, historical replay, research portfolio only.
[!] All integration is SIMULATION_ONLY. NOT_A_REAL_INTEGRATION_RECORD.
[!] NO_BROKER_CALL. NO_REAL_ACCOUNT. NO_FORMAL_LEDGER_WRITE.
"""
from __future__ import annotations

VERSION = "1.6.8"
RELEASE_NAME = "Operational Integration Hardening"
BASE_RELEASE = "1.6.7 Paper Performance Attribution"

# ── Safety flags ─────────────────────────────────────────────────────────────
OPERATIONAL_INTEGRATION_AVAILABLE          = True
OPERATIONAL_INTEGRATION_RESEARCH_ONLY      = True
OPERATIONAL_INTEGRATION_PAPER_ONLY         = True
OPERATIONAL_INTEGRATION_READ_ONLY          = True
OPERATIONAL_INTEGRATION_DETERMINISTIC      = True

REAL_OPERATIONAL_INTEGRATION_ENABLED       = False
BROKER_INTEGRATION_ENABLED                 = False
REAL_ACCOUNT_INTEGRATION_ENABLED           = False
REAL_ORDER_INTEGRATION_ENABLED             = False
PRODUCTION_LEDGER_INTEGRATION_ENABLED      = False
LIVE_EXECUTION_INTEGRATION_ENABLED         = False
AUTO_PROCESS_CONTROL_ENABLED               = False
AUTO_SERVICE_CONTROL_ENABLED               = False
AUTO_SESSION_CONTROL_ENABLED               = False
AUTO_CAPITAL_REALLOCATION_ENABLED          = False
AUTO_RISK_OVERRIDE_ENABLED                 = False
EXTERNAL_COORDINATION_ENABLED              = False
EXTERNAL_MESSAGE_BROKER_ENABLED            = False
EXTERNAL_LOCK_SERVICE_ENABLED              = False
NETWORK_INTEGRATION_ENABLED                = False

# ── Preserved safety flags from paper_trading foundation ─────────────────────
NO_REAL_ORDERS                             = True
BROKER_EXECUTION_ENABLED                   = False
PRODUCTION_TRADING_BLOCKED                 = True
