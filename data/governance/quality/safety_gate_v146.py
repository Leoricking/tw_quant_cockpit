"""
data/governance/quality/safety_gate_v146.py — Safety Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No token leak, no auth header, no rate bypass, no token rotation,
[!] no proxy rotation, no primary override, no mock fallback, no broker, no orders.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.quality.models_v146 import GateStatus, QualityGateResult
from data.governance.quality import (
    NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE, AUTO_PROVIDER_PROMOTION_ENABLED,
    AUTO_PRIMARY_OVERRIDE_ENABLED, SILENT_PROVIDER_FALLBACK_ENABLED,
    AUTO_QUARANTINE_RELEASE_ENABLED, MOCK_FALLBACK_ENABLED,
    AUTO_RATE_LIMIT_BYPASS_ENABLED,
)


class SafetyGate:
    """
    Safety invariants gate. Checks all safety flags.
    Any violation → BLOCKED.
    """

    POLICY_VERSION = "1.4.6"

    def evaluate(self, subject_id: str,
                 context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        ctx = context or {}
        now = datetime.datetime.utcnow().isoformat() + "Z"
        violations = []

        # Module-level safety invariants
        if not NO_REAL_ORDERS:
            violations.append("NO_REAL_ORDERS is False")
        if BROKER_EXECUTION_ENABLED:
            violations.append("BROKER_EXECUTION_ENABLED is True")
        if not PRODUCTION_TRADING_BLOCKED:
            violations.append("PRODUCTION_TRADING_BLOCKED is False")
        if QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE:
            violations.append("QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE is True")
        if AUTO_PROVIDER_PROMOTION_ENABLED:
            violations.append("AUTO_PROVIDER_PROMOTION_ENABLED is True")
        if AUTO_PRIMARY_OVERRIDE_ENABLED:
            violations.append("AUTO_PRIMARY_OVERRIDE_ENABLED is True")
        if SILENT_PROVIDER_FALLBACK_ENABLED:
            violations.append("SILENT_PROVIDER_FALLBACK_ENABLED is True")
        if AUTO_QUARANTINE_RELEASE_ENABLED:
            violations.append("AUTO_QUARANTINE_RELEASE_ENABLED is True")
        if MOCK_FALLBACK_ENABLED:
            violations.append("MOCK_FALLBACK_ENABLED is True")
        if AUTO_RATE_LIMIT_BYPASS_ENABLED:
            violations.append("AUTO_RATE_LIMIT_BYPASS_ENABLED is True")

        # Context-level checks
        if ctx.get("token_in_plaintext"):
            violations.append("token_in_plaintext detected")
        if ctx.get("auth_header_stored"):
            violations.append("auth_header_stored detected")
        if ctx.get("rate_bypass"):
            violations.append("rate_bypass detected")
        if ctx.get("has_broker"):
            violations.append("broker connection detected")
        if ctx.get("has_orders"):
            violations.append("order execution detected")

        if violations:
            return QualityGateResult(
                gate_id="safety_invariants", gate_name="Safety Invariants Gate",
                scope="PROVIDER", subject_id=subject_id,
                status=GateStatus.BLOCKED.value, passed=False, blocking=True,
                evidence=f"SAFETY VIOLATIONS: {violations}",
                errors=violations,
                evaluated_at=now, policy_version=self.POLICY_VERSION,
            )

        return QualityGateResult(
            gate_id="safety_invariants", gate_name="Safety Invariants Gate",
            scope="PROVIDER", subject_id=subject_id,
            status=GateStatus.PASS.value, passed=True, blocking=False,
            evidence="All safety invariants confirmed",
            evaluated_at=now, policy_version=self.POLICY_VERSION,
        )
