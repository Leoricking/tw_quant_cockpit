"""
data/governance/quality/pit_gate_v146.py — Point-In-Time Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Future leakage → BLOCK. No latest-value backfill.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.quality.models_v146 import GateStatus, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class PointInTimeGate:
    """
    PIT compliance gate.
    Future leakage → BLOCK.
    No latest-value backfill.
    """

    POLICY_VERSION = "1.4.6"

    def evaluate(self, subject_id: str,
                 context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        ctx = context or {}
        now = datetime.datetime.utcnow().isoformat() + "Z"

        published_at = ctx.get("published_at")
        available_from = ctx.get("available_from")
        as_of = ctx.get("as_of")
        revision_frozen = ctx.get("revision_frozen", False)
        future_leakage = ctx.get("future_leakage", False)
        pit_status = ctx.get("pit_status", "UNKNOWN")

        blocking_failures = []
        warnings = []

        # Future leakage → BLOCK (no exceptions)
        if future_leakage:
            blocking_failures.append("future_leakage_detected")

        # Check available_from is not in the future (crude check)
        if available_from and as_of:
            # Both are ISO strings — just compare lexicographically as approximation
            if available_from > as_of:
                warnings.append(
                    f"available_from ({available_from}) > as_of ({as_of}): "
                    "data may not have been available at as_of time"
                )

        if pit_status == "UNKNOWN":
            warnings.append("PIT status is UNKNOWN — not confirmed compliant")

        if not revision_frozen:
            warnings.append("revision not frozen — data may change retroactively")

        if blocking_failures:
            status = GateStatus.BLOCKED.value
            evidence = f"PIT BLOCKED: {', '.join(blocking_failures)}"
        elif warnings:
            status = GateStatus.WARN.value
            evidence = f"PIT warnings: {', '.join(warnings)}"
        elif pit_status == "PASS":
            status = GateStatus.PASS.value
            evidence = "PIT compliant"
        else:
            status = GateStatus.WARN.value
            evidence = f"PIT status: {pit_status}"

        return QualityGateResult(
            gate_id="point_in_time", gate_name="Point-In-Time Gate",
            scope="BACKTEST_INPUT", subject_id=subject_id,
            status=status, passed=(status == GateStatus.PASS.value),
            blocking=(status == GateStatus.BLOCKED.value),
            evidence=evidence, warnings=warnings,
            evaluated_at=now, policy_version=self.POLICY_VERSION,
        )
