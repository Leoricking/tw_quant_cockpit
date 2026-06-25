"""
data/governance/quality/provenance_gate_v146.py — Provenance Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Wraps v1.4.5 ProvenanceCompletenessGate directly — does NOT rewrite a weaker version.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.quality.models_v146 import GateStatus, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class ProvenanceGate:
    """
    Wraps v1.4.5 ProvenanceCompletenessGate.
    Does NOT rewrite — imports and delegates directly.
    """

    POLICY_VERSION = "1.4.6"

    def __init__(self) -> None:
        from data.governance.provenance_v145 import ProvenanceCompletenessGate
        self._v145_gate = ProvenanceCompletenessGate()

    def evaluate(self, subject_id: str,
                 context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        ctx = context or {}
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

        lineage = ctx.get("lineage_record")
        mode = ctx.get("mode", "real")
        pit_required = ctx.get("pit_required", False)

        if lineage is None:
            return QualityGateResult(
                gate_id="provenance_completeness", gate_name="Provenance Completeness Gate",
                scope="RECORD", subject_id=subject_id,
                status=GateStatus.FAIL.value, passed=False, blocking=True,
                evidence="No lineage record provided",
                evaluated_at=now, policy_version=self.POLICY_VERSION,
            )

        try:
            result = self._v145_gate.check(lineage, mode=mode, pit_required=pit_required)
        except Exception as exc:
            return QualityGateResult(
                gate_id="provenance_completeness", gate_name="Provenance Completeness Gate",
                scope="RECORD", subject_id=subject_id,
                status=GateStatus.FAIL.value, passed=False, blocking=True,
                evidence=f"ProvenanceCompletenessGate error: {exc}",
                evaluated_at=now, policy_version=self.POLICY_VERSION,
            )

        gate_result = result.get("result", "FAIL")
        missing = result.get("missing_fields", [])
        blocking_reasons = result.get("blocking_reasons", [])
        warnings = result.get("warnings", [])

        if gate_result == "PASS":
            status = GateStatus.PASS.value
        elif gate_result == "PARTIAL":
            status = GateStatus.WARN.value
        elif gate_result == "BLOCKED":
            status = GateStatus.BLOCKED.value
        else:
            status = GateStatus.FAIL.value

        evidence = f"v1.4.5 result={gate_result}, missing={missing}, blocking={blocking_reasons}"

        return QualityGateResult(
            gate_id="provenance_completeness", gate_name="Provenance Completeness Gate",
            scope="RECORD", subject_id=subject_id,
            status=status, passed=(status == GateStatus.PASS.value),
            blocking=(status in (GateStatus.BLOCKED.value, GateStatus.FAIL.value)),
            evidence=evidence, warnings=warnings,
            errors=blocking_reasons,
            evaluated_at=now, policy_version=self.POLICY_VERSION,
        )
