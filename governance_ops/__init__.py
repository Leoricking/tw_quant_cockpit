"""
governance_ops — TW Quant Cockpit v1.1.6 Data Governance Operations Dashboard

Unified governance operations package integrating universe, onboarding, repair,
freshness, quality gates, enforcement, audit, module health, symbol status,
prioritized action queues, daily snapshots, and reports.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Data Governance Dashboard does NOT auto-repair, auto-download, override gates,
    or enable trading. Dashboard actions are metadata-only.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level safety constants — must remain True at all times
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True
PRODUCTION_TRADING_BLOCKED = True

# Feature flags
DATA_GOVERNANCE_DASHBOARD_AVAILABLE = True
GOVERNANCE_ACTION_QUEUE_AVAILABLE = True
GOVERNANCE_DAILY_SUMMARY_AVAILABLE = True

# Disabled actions
GOVERNANCE_AUTO_REPAIR_ENABLED = False
GOVERNANCE_AUTO_DOWNLOAD_ENABLED = False
GOVERNANCE_GATE_OVERRIDE_ENABLED = False
GOVERNANCE_TRADE_EXECUTION_ENABLED = False

__version__ = "1.1.6"
__all__ = [
    "NO_REAL_ORDERS",
    "BROKER_DISABLED",
    "RESEARCH_ONLY",
    "PRODUCTION_TRADING_BLOCKED",
    "DATA_GOVERNANCE_DASHBOARD_AVAILABLE",
    "GOVERNANCE_ACTION_QUEUE_AVAILABLE",
    "GOVERNANCE_DAILY_SUMMARY_AVAILABLE",
    "GOVERNANCE_AUTO_REPAIR_ENABLED",
    "GOVERNANCE_AUTO_DOWNLOAD_ENABLED",
    "GOVERNANCE_GATE_OVERRIDE_ENABLED",
    "GOVERNANCE_TRADE_EXECUTION_ENABLED",
]
