"""
data/governance/quality/__init__.py — Provider Quality Gates package v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Quality gates do NOT enable trading. Gate failure does NOT trigger auto-repair.
[!] QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False (always).
[!] AUTO_PROVIDER_PROMOTION_ENABLED = False (always).
[!] AUTO_QUARANTINE_RELEASE_ENABLED = False (always).
[!] MOCK_FALLBACK_ENABLED = False (always).
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Safety invariants — module-level constants (never modify)
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False
AUTO_PROVIDER_PROMOTION_ENABLED = False
AUTO_PRIMARY_OVERRIDE_ENABLED = False
SILENT_PROVIDER_FALLBACK_ENABLED = False
AUTO_QUARANTINE_RELEASE_ENABLED = False
MOCK_FALLBACK_ENABLED = False
AUTO_RATE_LIMIT_BYPASS_ENABLED = False
