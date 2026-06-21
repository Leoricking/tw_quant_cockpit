"""
data/governance/quality/freshness_gate_v146.py — Freshness Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] quota_exhausted != stale. rate_limited != stale. fetch_time != source_freshness.
[!] UNKNOWN → not PASS.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.quality.models_v146 import FreshnessStatus, GateStatus, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class FreshnessGate:
    """
    Per-provider/dataset freshness evaluation.
    quota_exhausted and rate_limited do NOT make data stale.
    fetch_time != source_freshness (source may be published days ago).
    UNKNOWN → not PASS.
    """

    POLICY_VERSION = "1.4.6"

    def evaluate(self, subject_id: str,
                 context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        ctx = context or {}
        now = datetime.datetime.utcnow().isoformat() + "Z"

        freshness_status = ctx.get("freshness_status", FreshnessStatus.UNKNOWN.value)
        quota_exhausted = ctx.get("quota_exhausted", False)
        rate_limited = ctx.get("rate_limited", False)
        source_freshness = ctx.get("source_freshness_status", freshness_status)

        # quota_exhausted and rate_limited do NOT make data stale
        # Use source_freshness, not operational status
        effective_freshness = source_freshness

        warnings = []
        if quota_exhausted:
            warnings.append("quota_exhausted: does not imply stale data")
        if rate_limited:
            warnings.append("rate_limited: does not imply stale data")

        if effective_freshness == FreshnessStatus.FRESH.value:
            status = GateStatus.PASS.value
            evidence = "Data is FRESH"
        elif effective_freshness == FreshnessStatus.NEAR_STALE.value:
            status = GateStatus.WARN.value
            evidence = "Data is NEAR_STALE"
        elif effective_freshness in (FreshnessStatus.STALE.value, FreshnessStatus.DELAYED.value):
            status = GateStatus.FAIL.value
            evidence = f"Data is {effective_freshness}"
        elif effective_freshness == FreshnessStatus.BLOCKED.value:
            status = GateStatus.BLOCKED.value
            evidence = "Freshness status is BLOCKED"
        else:
            # UNKNOWN → not PASS
            status = GateStatus.FAIL.value
            evidence = "Freshness status is UNKNOWN — not PASS"

        return QualityGateResult(
            gate_id="freshness", gate_name="Freshness Gate",
            scope="DATASET", subject_id=subject_id,
            status=status, passed=(status == GateStatus.PASS.value),
            blocking=(status == GateStatus.BLOCKED.value),
            evidence=evidence, warnings=warnings,
            evaluated_at=now, policy_version=self.POLICY_VERSION,
        )
