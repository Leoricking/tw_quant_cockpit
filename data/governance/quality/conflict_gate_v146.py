"""
data/governance/quality/conflict_gate_v146.py — Conflict Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Uses v1.4.5 ConflictLineage.
[!] Unresolved primary-source conflict → BLOCK.
[!] Tolerance conflict → WARN. Date/unit conflict → FAIL.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from data.governance.models_v145 import ConflictLineage, ConflictType
from data.governance.quality.models_v146 import GateStatus, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class ConflictGate:
    """
    Evaluates conflict records.
    Unresolved primary-source conflict → BLOCK.
    Within-tolerance → WARN. Date/unit conflict → FAIL.
    """

    POLICY_VERSION = "1.4.6"

    def evaluate(self, subject_id: str,
                 context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        ctx = context or {}
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

        conflicts: List[Dict[str, Any]] = ctx.get("conflicts", [])
        if not conflicts:
            return QualityGateResult(
                gate_id="conflict_resolution", gate_name="Conflict Resolution Gate",
                scope="DATASET", subject_id=subject_id,
                status=GateStatus.PASS.value, passed=True, blocking=False,
                evidence="No conflicts detected",
                evaluated_at=now, policy_version=self.POLICY_VERSION,
            )

        worst_status = GateStatus.PASS.value
        blocking_reasons = []
        warnings = []

        for c_dict in conflicts:
            try:
                conflict = ConflictLineage.from_dict(c_dict)
            except Exception:
                conflict = None
                conflict_type = c_dict.get("conflict_type", "VALUE_CONFLICT")
                reviewed = c_dict.get("reviewed", False)
                formal_use_blocked = c_dict.get("formal_use_blocked", True)
            else:
                conflict_type = conflict.conflict_type
                reviewed = conflict.reviewed
                formal_use_blocked = conflict.formal_use_blocked

            # Unresolved primary-source conflict → BLOCK
            if formal_use_blocked and not reviewed:
                if conflict_type == ConflictType.VALUE_CONFLICT.value:
                    worst_status = GateStatus.BLOCKED.value
                    blocking_reasons.append(
                        f"Unresolved primary-source conflict: {c_dict.get('conflict_id', '?')}"
                    )
                elif conflict_type in (
                    ConflictType.DATE_CONFLICT.value, ConflictType.UNIT_CONFLICT.value
                ):
                    if worst_status != GateStatus.BLOCKED.value:
                        worst_status = GateStatus.FAIL.value
                    blocking_reasons.append(f"Date/unit conflict: {conflict_type}")
                elif conflict_type == ConflictType.WITHIN_TOLERANCE.value:
                    if worst_status not in (GateStatus.BLOCKED.value, GateStatus.FAIL.value):
                        worst_status = GateStatus.WARN.value
                    warnings.append(f"Within-tolerance conflict detected")
                else:
                    if worst_status not in (GateStatus.BLOCKED.value, GateStatus.FAIL.value):
                        worst_status = GateStatus.WARN.value

        evidence = (
            f"Conflicts: {len(conflicts)} total, "
            f"blocking={len(blocking_reasons)}, warnings={len(warnings)}"
        )

        return QualityGateResult(
            gate_id="conflict_resolution", gate_name="Conflict Resolution Gate",
            scope="DATASET", subject_id=subject_id,
            status=worst_status, passed=(worst_status == GateStatus.PASS.value),
            blocking=(worst_status == GateStatus.BLOCKED.value),
            evidence=evidence, warnings=warnings, errors=blocking_reasons,
            evaluated_at=now, policy_version=self.POLICY_VERSION,
        )
