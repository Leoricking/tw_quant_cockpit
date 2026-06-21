"""
data/governance/quality/quality_gate_v146.py — Data Quality Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Maps existing Data Quality results to gate evidence.
[!] PASS/PARTIAL/DEGRADED/FAIL/BLOCKED mapping (versioned).
[!] Critical datasets get stricter mapping.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from data.governance.quality.models_v146 import GateStatus, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Score thresholds (versioned)
_POLICY_VERSION = "1.4.6"
_PASS_THRESHOLD = 80
_DEGRADED_THRESHOLD = 60
_FAIL_THRESHOLD = 49
_CRITICAL_PASS_THRESHOLD = 90
_CRITICAL_DEGRADED_THRESHOLD = 75

_CRITICAL_DATASETS = {
    "twse:daily_ohlcv", "tpex:daily_ohlcv",
    "mops:financial_report", "mops:balance_sheet",
    "mops:income_statement",
}


class DataQualityGate:
    """Maps Data Quality scores to gate results."""

    POLICY_VERSION = _POLICY_VERSION

    def evaluate(self, subject_id: str,
                 context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        ctx = context or {}
        now = datetime.datetime.utcnow().isoformat() + "Z"

        quality_score = ctx.get("quality_score", None)
        quality_status = ctx.get("quality_status", "UNKNOWN")
        is_critical = ctx.get("is_critical", subject_id in _CRITICAL_DATASETS)

        if quality_score is None and quality_status == "UNKNOWN":
            return QualityGateResult(
                gate_id="data_quality", gate_name="Data Quality Gate",
                scope="DATASET", subject_id=subject_id,
                status=GateStatus.UNKNOWN.value, passed=False,
                blocking=True, evidence="No quality score or status available",
                evaluated_at=now, policy_version=self.POLICY_VERSION,
            )

        # Determine thresholds
        pass_thresh = _CRITICAL_PASS_THRESHOLD if is_critical else _PASS_THRESHOLD
        degraded_thresh = _CRITICAL_DEGRADED_THRESHOLD if is_critical else _DEGRADED_THRESHOLD

        # Map status string
        if quality_status == "BLOCKED":
            status = GateStatus.BLOCKED.value
            evidence = f"Quality status: BLOCKED (score={quality_score})"
        elif quality_status == "FAIL" or (quality_score is not None and quality_score <= _FAIL_THRESHOLD):
            status = GateStatus.FAIL.value
            evidence = f"Quality FAIL: score={quality_score} <= {_FAIL_THRESHOLD}"
        elif quality_score is not None and quality_score < degraded_thresh:
            status = GateStatus.WARN.value
            evidence = f"Quality DEGRADED: score={quality_score} < {degraded_thresh}"
        elif quality_score is not None and quality_score >= pass_thresh:
            status = GateStatus.PASS.value
            evidence = f"Quality PASS: score={quality_score} >= {pass_thresh}"
        elif quality_status in ("PASS", "PARTIAL"):
            status = GateStatus.PASS.value if quality_status == "PASS" else GateStatus.WARN.value
            evidence = f"Quality status: {quality_status}"
        else:
            status = GateStatus.WARN.value
            evidence = f"Quality partial: score={quality_score}, status={quality_status}"

        return QualityGateResult(
            gate_id="data_quality", gate_name="Data Quality Gate",
            scope="DATASET", subject_id=subject_id,
            status=status, passed=(status == GateStatus.PASS.value),
            blocking=(status in (GateStatus.BLOCKED.value, GateStatus.FAIL.value)),
            evidence=evidence,
            evaluated_at=now, policy_version=self.POLICY_VERSION,
        )
