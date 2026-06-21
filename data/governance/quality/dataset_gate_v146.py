"""
data/governance/quality/dataset_gate_v146.py — Dataset Admission Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Not-allowlisted dataset → BLOCKED immediately. No auto-admission.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from data.governance.quality.models_v146 import (
    DatasetQualityProfile, GateStatus, ProviderQualityState, QualityGateResult,
)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Built-in dataset allowlist
_DATASET_ALLOWLIST = {
    "twse:daily_ohlcv", "twse:security_master", "twse:institutional",
    "twse:margin", "twse:index", "twse:calendar", "twse:corporate_action",
    "tpex:daily_ohlcv", "tpex:security_master", "tpex:institutional",
    "tpex:margin", "tpex:index", "tpex:calendar", "tpex:valuation",
    "mops:company_profile", "mops:monthly_revenue", "mops:financial_report",
    "mops:balance_sheet", "mops:income_statement", "mops:cash_flow",
    "finmind:daily_ohlcv", "finmind:institutional", "finmind:margin",
    "data_gov_tw:approved_dataset",
}


class DatasetAdmissionGate:
    """
    Gate for dataset admission.
    Not-allowlisted → BLOCKED immediately.
    """

    POLICY_VERSION = "1.4.6"

    def evaluate(self, dataset_id: str, provider_id: str,
                 context: Optional[Dict[str, Any]] = None) -> DatasetQualityProfile:
        ctx = context or {}
        now = datetime.datetime.utcnow().isoformat() + "Z"
        results: List[QualityGateResult] = []

        full_key = f"{provider_id}:{dataset_id}"
        allowlisted = full_key in _DATASET_ALLOWLIST or ctx.get("allowlisted", False)

        # Gate 1: Allowlist check — blocking if not allowlisted
        if allowlisted:
            results.append(self._make_result(
                "dataset_allowlist", "Dataset Allowlist Gate", dataset_id,
                GateStatus.PASS.value, f"Dataset '{full_key}' on allowlist",
            ))
        else:
            results.append(self._make_result(
                "dataset_allowlist", "Dataset Allowlist Gate", dataset_id,
                GateStatus.BLOCKED.value, f"Dataset '{full_key}' NOT on allowlist — BLOCKED",
            ))

        # Gate 2: Schema contract
        schema_valid = ctx.get("schema_valid", allowlisted)
        results.append(self._make_result(
            "schema_contract", "Schema Contract Gate", dataset_id,
            GateStatus.PASS.value if schema_valid else GateStatus.FAIL.value,
            "Schema contract valid" if schema_valid else "Schema contract violation",
        ))

        # Gate 3: PIT policy
        pit_ok = ctx.get("pit_policy", True)
        results.append(self._make_result(
            "pit_policy", "Point-In-Time Policy Gate", dataset_id,
            GateStatus.PASS.value if pit_ok else GateStatus.WARN.value,
            "PIT policy compliant" if pit_ok else "PIT policy unclear",
            blocking=False,
        ))

        blocking_failures = [
            r.gate_id for r in results
            if r.blocking and r.status in (GateStatus.BLOCKED.value, GateStatus.FAIL.value)
        ]
        warnings = [w for r in results for w in r.warnings]

        if blocking_failures:
            quality_state = ProviderQualityState.BLOCKED.value
            admitted = False
        elif any(r.status == GateStatus.FAIL.value for r in results):
            quality_state = ProviderQualityState.RESTRICTED.value
            admitted = False
        else:
            quality_state = ProviderQualityState.ACTIVE.value
            admitted = True

        return DatasetQualityProfile(
            dataset_id=dataset_id,
            provider_id=provider_id,
            quality_state=quality_state,
            admitted=admitted,
            allowlisted=allowlisted,
            schema_valid=schema_valid,
            pit_compliant=pit_ok,
            formal_use_allowed=admitted and not blocking_failures,
            gate_results=[r.to_dict() for r in results],
            blocking_failures=blocking_failures,
            warnings=warnings,
            evaluated_at=now,
            policy_version=self.POLICY_VERSION,
        )

    def _make_result(self, gate_id: str, gate_name: str, dataset_id: str,
                     status: str, evidence: str, blocking: bool = True,
                     warnings: Optional[List[str]] = None) -> QualityGateResult:
        return QualityGateResult(
            gate_id=gate_id, gate_name=gate_name, scope="DATASET",
            subject_id=dataset_id, status=status,
            passed=(status == GateStatus.PASS.value),
            blocking=blocking, evidence=evidence,
            warnings=warnings or [],
            evaluated_at=datetime.datetime.utcnow().isoformat() + "Z",
            policy_version=self.POLICY_VERSION,
        )
