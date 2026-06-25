"""
data/governance/quality/audit_v146.py — Quality Decision Audit Service v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Append-only, immutable, deterministic evidence hash.
[!] No credentials stored.
"""
from __future__ import annotations

import datetime
import uuid
from typing import Any, Dict, List, Optional

from data.governance.quality.models_v146 import QualityDecision, QualityDecisionAudit

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class QualityDecisionAuditService:
    """
    Append-only audit service for quality decisions.
    Records are immutable once created.
    No credentials or sensitive data stored.
    """

    def __init__(self) -> None:
        self._audits: List[QualityDecisionAudit] = []

    def record(self, decision: QualityDecision, provider_id: str = "") -> QualityDecisionAudit:
        """Record a quality decision. Append-only."""
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
        audit_id = str(uuid.uuid4())

        gate_results_summary = [
            f"{r.get('gate_id', '?')}:{r.get('status', '?')}"
            for r in decision.gate_results
        ]

        evidence_hash = QualityDecisionAudit.compute_evidence_hash(
            decision_id=decision.decision_id,
            decision=decision.decision,
            blocking_failures=decision.blocking_failures,
            audited_at=now,
        )

        audit = QualityDecisionAudit(
            audit_id=audit_id,
            decision_id=decision.decision_id,
            provider_id=provider_id or decision.subject_id,
            scope=decision.scope,
            subject_id=decision.subject_id,
            decision=decision.decision,
            quality_state=decision.quality_state,
            gate_results_summary=gate_results_summary,
            blocking_failures=decision.blocking_failures,
            evidence_hash=evidence_hash,
            audited_at=now,
            policy_version=decision.policy_version,
        )
        self._audits.append(audit)
        return audit

    def get_by_decision_id(self, decision_id: str) -> List[QualityDecisionAudit]:
        return [a for a in self._audits if a.decision_id == decision_id]

    def get_by_provider(self, provider_id: str) -> List[QualityDecisionAudit]:
        return [a for a in self._audits if a.provider_id == provider_id]

    def get_by_scope(self, scope: str) -> List[QualityDecisionAudit]:
        return [a for a in self._audits if a.scope == scope]

    def get_by_time_range(self, start: str, end: str) -> List[QualityDecisionAudit]:
        return [a for a in self._audits if start <= a.audited_at <= end]

    def list_all(self) -> List[QualityDecisionAudit]:
        return list(self._audits)

    def summary(self) -> Dict[str, Any]:
        return {
            "total_audits": len(self._audits),
            "no_credentials_stored": True,
            "append_only": True,
            "policy_version": "1.4.6",
        }
