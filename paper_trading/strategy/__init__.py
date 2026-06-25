"""
paper_trading/strategy/__init__.py — Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

PAPER_STRATEGY_ORCHESTRATION_VERSION       = "1.6.2"
PAPER_STRATEGY_ORCHESTRATION_STAGE         = "FOUNDATION"

# Safety flags — all real execution permanently disabled
PAPER_STRATEGY_RESEARCH_ONLY               = True
PAPER_SIGNAL_EVALUATION_ENABLED            = True
PAPER_DECISION_PIPELINE_ENABLED            = True
PAPER_ORDER_PROPOSAL_ENABLED               = True
PAPER_POLICY_APPROVAL_ENABLED              = True
PAPER_ORDER_SUBMISSION_ENABLED             = True   # to paper order machine only

REAL_STRATEGY_EXECUTION_ENABLED            = False
REAL_ORDER_CREATION_ENABLED                = False
REAL_ORDER_EXECUTION_ENABLED               = False
BROKER_CONNECTION_ENABLED                  = False
LIVE_ACCOUNT_SYNC_ENABLED                  = False
PRODUCTION_TRADING_ENABLED                 = False
REAL_PORTFOLIO_LEDGER_WRITE_ENABLED        = False
AUTONOMOUS_PRODUCTION_STRATEGY_ENABLED     = False
REAL_AUTO_REBALANCE_ENABLED                = False
REAL_HEDGING_EXECUTION_ENABLED             = False
MARGIN_ENABLED                             = False
SHORT_SELLING_ENABLED                      = False

# Canonical safety aliases (match paper_trading/__init__.py)
NO_REAL_ORDERS                             = True
BROKER_EXECUTION_ENABLED                   = False
PRODUCTION_TRADING_BLOCKED                 = True
AUTO_PAPER_ONLY_ENABLED_BY_DEFAULT         = False
AUTO_RESUME_RUNNING                        = False
