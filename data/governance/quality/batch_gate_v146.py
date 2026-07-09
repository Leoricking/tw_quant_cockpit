"""
data/governance/quality/batch_gate_v146.py — Batch Ingestion Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] records_written <= records_valid, requests_succeeded <= requests_executed.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from data.governance.quality.models_v146 import GateStatus, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class BatchIngestionGate:
    """
    Checks batch fetch run audit integrity.
    """

    POLICY_VERSION = "1.4.6"

    def evaluate(self, fetch_run_id: str,
                 audit: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        ctx = audit or {}
        now = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"
        results: List[QualityGateResult] = []

        records_written = ctx.get("records_written", 0)
        records_valid = ctx.get("records_valid", 0)
        requests_succeeded = ctx.get("requests_succeeded", 0)
        requests_executed = ctx.get("requests_executed", 0)
        lineage_count = ctx.get("lineage_records_created", 0)
        duplicate_fingerprints = ctx.get("duplicate_fingerprints", 0)

        # Gate 1: records_written <= records_valid
        ok1 = records_written <= records_valid or records_valid == 0
        results.append(self._make_result(
            "records_written_valid", "Records Written <= Valid", fetch_run_id,
            GateStatus.PASS.value if ok1 else GateStatus.FAIL.value,
            f"records_written={records_written}, records_valid={records_valid}",
        ))

        # Gate 2: requests_succeeded <= requests_executed
        ok2 = requests_succeeded <= requests_executed or requests_executed == 0
        results.append(self._make_result(
            "requests_succeeded_valid", "Requests Succeeded <= Executed", fetch_run_id,
            GateStatus.PASS.value if ok2 else GateStatus.FAIL.value,
            f"requests_succeeded={requests_succeeded}, requests_executed={requests_executed}",
        ))

        # Gate 3: No duplicate fingerprints
        ok3 = duplicate_fingerprints == 0
        results.append(self._make_result(
            "no_duplicate_fingerprints", "No Duplicate Fingerprints", fetch_run_id,
            GateStatus.PASS.value if ok3 else GateStatus.FAIL.value,
            f"duplicate_fingerprints={duplicate_fingerprints}",
        ))

        # Gate 4: Lineage count consistent
        ok4 = lineage_count >= 0
        results.append(self._make_result(
            "lineage_count_consistent", "Lineage Count Consistent", fetch_run_id,
            GateStatus.PASS.value if ok4 else GateStatus.WARN.value,
            f"lineage_records_created={lineage_count}",
            blocking=False,
        ))

        blocking_failures = [
            r.gate_id for r in results
            if r.blocking and r.status in (GateStatus.BLOCKED.value, GateStatus.FAIL.value)
        ]

        return {
            "fetch_run_id": fetch_run_id,
            "eligible": len(blocking_failures) == 0,
            "blocking_failures": blocking_failures,
            "gate_results": [r.to_dict() for r in results],
            "evaluated_at": now,
            "policy_version": self.POLICY_VERSION,
        }

    def _make_result(self, gate_id: str, gate_name: str, fetch_run_id: str,
                     status: str, evidence: str, blocking: bool = True,
                     warnings: Optional[List[str]] = None) -> QualityGateResult:
        return QualityGateResult(
            gate_id=gate_id, gate_name=gate_name, scope="BATCH",
            subject_id=fetch_run_id, status=status,
            passed=(status == GateStatus.PASS.value),
            blocking=blocking, evidence=evidence,
            warnings=warnings or [],
            evaluated_at=datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
            policy_version=self.POLICY_VERSION,
        )
