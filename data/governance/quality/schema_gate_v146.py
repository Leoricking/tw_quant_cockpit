"""
data/governance/quality/schema_gate_v146.py — Schema Drift Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] NO_CHANGE→PASS, ADDITIVE→WARN, COMPATIBLE_ALIAS→PASS/WARN.
[!] BREAKING_MISSING_FIELD→BLOCKED, BREAKING_TYPE_CHANGE→BLOCKED, BREAKING_KEY_CHANGE→BLOCKED.
[!] UNKNOWN→FAIL.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.models_v145 import SchemaDriftStatus
from data.governance.quality.models_v146 import GateStatus, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Mapping from SchemaDriftStatus → GateStatus
_DRIFT_TO_GATE = {
    SchemaDriftStatus.NO_CHANGE.value: GateStatus.PASS.value,
    SchemaDriftStatus.ADDITIVE.value: GateStatus.WARN.value,
    SchemaDriftStatus.COMPATIBLE_ALIAS.value: GateStatus.WARN.value,
    SchemaDriftStatus.BREAKING_MISSING_FIELD.value: GateStatus.BLOCKED.value,
    SchemaDriftStatus.BREAKING_TYPE_CHANGE.value: GateStatus.BLOCKED.value,
    SchemaDriftStatus.BREAKING_KEY_CHANGE.value: GateStatus.BLOCKED.value,
    SchemaDriftStatus.UNKNOWN.value: GateStatus.FAIL.value,
}


class SchemaDriftGate:
    """Maps SchemaDriftStatus to gate result. Breaking changes → BLOCKED."""

    POLICY_VERSION = "1.4.6"

    def evaluate(self, subject_id: str,
                 context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        ctx = context or {}
        now = datetime.datetime.utcnow().isoformat() + "Z"

        drift_status = ctx.get("schema_drift_status", SchemaDriftStatus.UNKNOWN.value)
        gate_status = _DRIFT_TO_GATE.get(drift_status, GateStatus.FAIL.value)

        blocking = gate_status == GateStatus.BLOCKED.value
        evidence = f"Schema drift: {drift_status} → gate: {gate_status}"

        warnings = []
        if gate_status == GateStatus.WARN.value:
            warnings.append(f"Schema drift: {drift_status}")

        return QualityGateResult(
            gate_id="schema_drift", gate_name="Schema Drift Gate",
            scope="DATASET", subject_id=subject_id,
            status=gate_status, passed=(gate_status == GateStatus.PASS.value),
            blocking=blocking, evidence=evidence, warnings=warnings,
            evaluated_at=now, policy_version=self.POLICY_VERSION,
        )
