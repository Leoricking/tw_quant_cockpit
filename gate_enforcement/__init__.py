"""
gate_enforcement — TW Quant Cockpit v1.1.5 Quality Gate Enforcement & Audit

Research-only package. Enforces quality gate decisions at run time, filters
symbols, builds immutable audit events, run snapshots, and reproducibility
hashes. No broker connectivity. No order placement.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Quality Gate Enforcement does NOT enable trading.
[!] VALIDATED does not mean tradable.
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
QUALITY_GATE_ENFORCEMENT_RELEASE = True
QUALITY_GATE_ENFORCEMENT_AVAILABLE = True
QUALITY_GATE_AUDIT_AVAILABLE = True
RUN_GATE_SNAPSHOT_AVAILABLE = True
RUN_REPRODUCIBILITY_HASH_AVAILABLE = True

# Override policy
QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT = True
QUALITY_GATE_BYPASS_ALLOWED = False

# Mock / blocked guards
MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED = False
BLOCKED_DATA_FORMAL_ENFORCEMENT_ALLOWED = False

__version__ = "1.1.5"
__all__ = [
    "NO_REAL_ORDERS",
    "BROKER_DISABLED",
    "RESEARCH_ONLY",
    "PRODUCTION_TRADING_BLOCKED",
    "QUALITY_GATE_ENFORCEMENT_RELEASE",
    "QUALITY_GATE_ENFORCEMENT_AVAILABLE",
    "QUALITY_GATE_AUDIT_AVAILABLE",
    "RUN_GATE_SNAPSHOT_AVAILABLE",
    "RUN_REPRODUCIBILITY_HASH_AVAILABLE",
    "QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT",
    "QUALITY_GATE_BYPASS_ALLOWED",
    "MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED",
    "BLOCKED_DATA_FORMAL_ENFORCEMENT_ALLOWED",
]
