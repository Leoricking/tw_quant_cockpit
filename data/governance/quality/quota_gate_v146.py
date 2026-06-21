"""
data/governance/quality/quota_gate_v146.py — Quota Readiness Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] QUOTA_EXHAUSTED blocks new fetch but doesn't invalidate existing data.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.quality.models_v146 import GateStatus, OperationalReadiness, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class QuotaReadinessGate:
    """
    Quota readiness gate.
    QUOTA_EXHAUSTED blocks new fetch; does NOT invalidate existing data.
    Stale quota evidence → WARN, not BLOCK.
    """

    POLICY_VERSION = "1.4.6"

    def evaluate(self, subject_id: str,
                 context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        ctx = context or {}
        now = datetime.datetime.utcnow().isoformat() + "Z"

        quota_known = ctx.get("quota_known", False)
        quota_sufficient = ctx.get("quota_sufficient", True)
        quota_exhausted = ctx.get("quota_exhausted", False)
        evidence_stale = ctx.get("evidence_stale", False)
        reserve_ok = ctx.get("reserve_ok", True)

        if quota_exhausted:
            return QualityGateResult(
                gate_id="quota_readiness", gate_name="Quota Readiness Gate",
                scope="ENDPOINT", subject_id=subject_id,
                status=GateStatus.BLOCKED.value, passed=False, blocking=True,
                evidence=(
                    "QUOTA_EXHAUSTED: new fetch blocked. "
                    "Existing data is NOT invalidated by quota exhaustion."
                ),
                evaluated_at=now, policy_version=self.POLICY_VERSION,
            )

        warnings = []
        if not quota_known:
            warnings.append("Quota unknown — proceeding with caution")
        if evidence_stale:
            warnings.append("Quota evidence is stale — may not be accurate")
        if not reserve_ok:
            warnings.append("Quota reserve is low")

        if not quota_sufficient and quota_known:
            return QualityGateResult(
                gate_id="quota_readiness", gate_name="Quota Readiness Gate",
                scope="ENDPOINT", subject_id=subject_id,
                status=GateStatus.WARN.value, passed=False, blocking=False,
                evidence="Quota insufficient for requested operation",
                warnings=warnings,
                evaluated_at=now, policy_version=self.POLICY_VERSION,
            )

        return QualityGateResult(
            gate_id="quota_readiness", gate_name="Quota Readiness Gate",
            scope="ENDPOINT", subject_id=subject_id,
            status=GateStatus.PASS.value if not warnings else GateStatus.WARN.value,
            passed=True, blocking=False,
            evidence="Quota available" if not warnings else "Quota available (with warnings)",
            warnings=warnings,
            evaluated_at=now, policy_version=self.POLICY_VERSION,
        )
