"""
data/governance/quality/backtest_gate_v146.py — Backtest Input Eligibility Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Future leakage → BLOCK. No auto-patch. Look-ahead leakage → BLOCK.
[!] No latest-value backfill.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.quality.models_v146 import BacktestInputEligibility, GateStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_BACKTEST_ALLOWED_AUTHORITIES = {
    "PRIMARY_OFFICIAL", "PRIMARY_DOMAIN_OFFICIAL", "SECONDARY_OFFICIAL",
}


class BacktestInputEligibilityGate:
    """
    Full backtest input eligibility check.
    Future leakage → BLOCK (no exceptions).
    """

    POLICY_VERSION = "1.4.6"

    def evaluate(self, provider_id: str, dataset_id: str,
                 context: Optional[Dict[str, Any]] = None) -> BacktestInputEligibility:
        ctx = context or {}
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

        pit_available = ctx.get("pit_available", False)
        lookahead_leakage = ctx.get("lookahead_leakage", False)
        future_leakage = ctx.get("future_leakage", False)
        revision_frozen = ctx.get("revision_frozen", False)
        timestamp_aligned = ctx.get("timestamp_aligned", False)
        survivorship_ok = ctx.get("survivorship_bias_policy_ok", False)
        authority_level = ctx.get("authority_level", "UNKNOWN")
        coverage_sufficient = ctx.get("coverage_sufficient", False)

        authority_sufficient = authority_level in _BACKTEST_ALLOWED_AUTHORITIES

        blocking_failures = []
        warnings = []

        # HARD BLOCKS (no exceptions)
        if future_leakage:
            blocking_failures.append("future_leakage_detected: BLOCKED, no auto-patch")

        if lookahead_leakage:
            blocking_failures.append("lookahead_leakage_detected: BLOCKED")

        if not pit_available:
            blocking_failures.append("pit_not_available: required for backtest")

        if not revision_frozen:
            blocking_failures.append("revision_not_frozen: backtest requires frozen data")

        if not authority_sufficient:
            blocking_failures.append(
                f"authority_insufficient: {authority_level} not allowed for backtest"
            )

        # Warnings (non-blocking)
        if not timestamp_aligned:
            warnings.append("timestamp_alignment not confirmed")

        if not survivorship_ok:
            warnings.append("survivorship bias policy not confirmed")

        if not coverage_sufficient:
            warnings.append("coverage may be insufficient for full backtest")

        eligible = len(blocking_failures) == 0

        return BacktestInputEligibility(
            provider_id=provider_id,
            dataset_id=dataset_id,
            eligible=eligible,
            blocking_failures=blocking_failures,
            warnings=warnings,
            pit_available=pit_available,
            no_lookahead_leakage=not lookahead_leakage and not future_leakage,
            revision_frozen=revision_frozen,
            timestamp_aligned=timestamp_aligned,
            survivorship_bias_policy_ok=survivorship_ok,
            source_authority_sufficient=authority_sufficient,
            coverage_sufficient=coverage_sufficient,
            evaluated_at=now,
            policy_version=self.POLICY_VERSION,
        )
