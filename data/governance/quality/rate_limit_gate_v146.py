"""
data/governance/quality/rate_limit_gate_v146.py — Rate Limit Readiness Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] POLICY_UNKNOWN → blocks large batch, not small queries.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.quality.models_v146 import GateStatus, OperationalReadiness, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_LARGE_BATCH_THRESHOLD = 50  # requests


class RateLimitReadinessGate:
    """
    Checks host policy, provider budget, endpoint policy, cooldown, Retry-After.
    POLICY_UNKNOWN → blocks large batch, not small queries.
    """

    POLICY_VERSION = "1.4.6"

    def evaluate(self, subject_id: str,
                 context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        ctx = context or {}
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

        host_policy_exists = ctx.get("host_policy_exists", False)
        in_cooldown = ctx.get("in_cooldown", False)
        retry_after_active = ctx.get("retry_after_active", False)
        request_count = ctx.get("request_count", 1)
        is_large_batch = request_count >= _LARGE_BATCH_THRESHOLD or ctx.get("is_large_batch", False)

        warnings = []

        if in_cooldown or retry_after_active:
            return QualityGateResult(
                gate_id="rate_limit_readiness", gate_name="Rate Limit Readiness Gate",
                scope="ENDPOINT", subject_id=subject_id,
                status=GateStatus.WARN.value, passed=False, blocking=False,
                evidence=f"In cooldown={in_cooldown}, retry_after={retry_after_active}",
                warnings=["Rate limited — wait before retrying"],
                evaluated_at=now, policy_version=self.POLICY_VERSION,
            )

        if not host_policy_exists:
            if is_large_batch:
                return QualityGateResult(
                    gate_id="rate_limit_readiness", gate_name="Rate Limit Readiness Gate",
                    scope="ENDPOINT", subject_id=subject_id,
                    status=GateStatus.BLOCKED.value, passed=False, blocking=True,
                    evidence=(
                        f"POLICY_UNKNOWN blocks large batch (request_count={request_count})"
                    ),
                    evaluated_at=now, policy_version=self.POLICY_VERSION,
                )
            else:
                warnings.append("Host rate limit policy unknown — small query allowed")
                return QualityGateResult(
                    gate_id="rate_limit_readiness", gate_name="Rate Limit Readiness Gate",
                    scope="ENDPOINT", subject_id=subject_id,
                    status=GateStatus.WARN.value, passed=False, blocking=False,
                    evidence="POLICY_UNKNOWN: small query allowed, large batch blocked",
                    warnings=warnings,
                    evaluated_at=now, policy_version=self.POLICY_VERSION,
                )

        return QualityGateResult(
            gate_id="rate_limit_readiness", gate_name="Rate Limit Readiness Gate",
            scope="ENDPOINT", subject_id=subject_id,
            status=GateStatus.PASS.value, passed=True, blocking=False,
            evidence="Rate limit policy exists, no cooldown",
            evaluated_at=now, policy_version=self.POLICY_VERSION,
        )
