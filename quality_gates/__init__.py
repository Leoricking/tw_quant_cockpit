"""
quality_gates — TW Quant Cockpit v1.1.4 Coverage Quality Gates

Research-only package. All trading execution is blocked.
This package evaluates data quality and coverage eligibility for backtesting
and analysis workflows. No broker connectivity. No order placement.
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
COVERAGE_QUALITY_GATES_RELEASE = True
FORMAL_BACKTEST_GATE_AVAILABLE = True
FORMAL_VALIDATION_GATE_AVAILABLE = True

# Override policy
QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT = True

# Data-source guards for formal gate eligibility
MOCK_DATA_FORMAL_GATE_ALLOWED = False
STALE_DATA_FORMAL_GATE_ALLOWED = False
CONFLICT_DATA_FORMAL_GATE_ALLOWED = False
INVALID_DATA_FORMAL_GATE_ALLOWED = False

__version__ = "1.1.4"
__all__ = [
    "NO_REAL_ORDERS",
    "BROKER_DISABLED",
    "RESEARCH_ONLY",
    "PRODUCTION_TRADING_BLOCKED",
    "COVERAGE_QUALITY_GATES_RELEASE",
    "FORMAL_BACKTEST_GATE_AVAILABLE",
    "FORMAL_VALIDATION_GATE_AVAILABLE",
    "QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT",
    "MOCK_DATA_FORMAL_GATE_ALLOWED",
    "STALE_DATA_FORMAL_GATE_ALLOWED",
    "CONFLICT_DATA_FORMAL_GATE_ALLOWED",
    "INVALID_DATA_FORMAL_GATE_ALLOWED",
]
