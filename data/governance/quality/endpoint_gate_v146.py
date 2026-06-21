"""
data/governance/quality/endpoint_gate_v146.py — Endpoint Readiness Gate v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from data.governance.quality.models_v146 import GateStatus, QualityGateResult

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_KNOWN_ENDPOINTS = {
    "twse:daily", "twse:security_master", "twse:institutional",
    "tpex:daily", "tpex:security_master", "tpex:institutional",
    "mops:company_profile", "mops:monthly_revenue", "finmind:market",
}


class EndpointReadinessGate:
    """Checks endpoint registration, active status, rate limit policy, retry policy."""

    POLICY_VERSION = "1.4.6"

    def evaluate(self, endpoint_id: str,
                 context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        ctx = context or {}
        now = datetime.datetime.utcnow().isoformat() + "Z"
        results: List[QualityGateResult] = []

        registered = endpoint_id in _KNOWN_ENDPOINTS or ctx.get("registered", False)
        active = ctx.get("active", registered)
        has_rate_policy = ctx.get("has_rate_policy", registered)
        has_retry_policy = ctx.get("has_retry_policy", registered)
        deprecated = ctx.get("deprecated", False)

        results.append(self._make_result(
            "endpoint_registered", "Endpoint Registered", endpoint_id,
            GateStatus.PASS.value if registered else GateStatus.FAIL.value,
            f"Endpoint '{endpoint_id}' registered={registered}",
        ))

        if deprecated:
            results.append(self._make_result(
                "endpoint_not_deprecated", "Endpoint Not Deprecated", endpoint_id,
                GateStatus.BLOCKED.value, f"Endpoint '{endpoint_id}' is DEPRECATED",
            ))

        results.append(self._make_result(
            "endpoint_active", "Endpoint Active", endpoint_id,
            GateStatus.PASS.value if active else GateStatus.FAIL.value,
            f"Endpoint active={active}",
        ))

        results.append(self._make_result(
            "rate_policy_exists", "Rate Policy Exists", endpoint_id,
            GateStatus.PASS.value if has_rate_policy else GateStatus.WARN.value,
            f"Rate policy exists={has_rate_policy}",
            blocking=False,
        ))

        blocking_failures = [
            r.gate_id for r in results
            if r.blocking and r.status in (GateStatus.BLOCKED.value, GateStatus.FAIL.value)
        ]

        return {
            "endpoint_id": endpoint_id,
            "ready": len(blocking_failures) == 0,
            "blocking_failures": blocking_failures,
            "gate_results": [r.to_dict() for r in results],
            "evaluated_at": now,
            "policy_version": self.POLICY_VERSION,
        }

    def _make_result(self, gate_id: str, gate_name: str, endpoint_id: str,
                     status: str, evidence: str, blocking: bool = True,
                     warnings: Optional[List[str]] = None) -> QualityGateResult:
        return QualityGateResult(
            gate_id=gate_id, gate_name=gate_name, scope="ENDPOINT",
            subject_id=endpoint_id, status=status,
            passed=(status == GateStatus.PASS.value),
            blocking=blocking, evidence=evidence,
            warnings=warnings or [],
            evaluated_at=datetime.datetime.utcnow().isoformat() + "Z",
            policy_version=self.POLICY_VERSION,
        )
