"""
data/governance/quality/quarantine_v146.py — Provider Quarantine Manager v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] auto_release_allowed = False always.
[!] No auto-release of blocking quarantine.
[!] History preserved (append-only).
"""
from __future__ import annotations

import datetime
import uuid
from typing import Any, Dict, List, Optional

from data.governance.quality.models_v146 import (
    ProviderQualityState, QuarantineRecord,
)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
AUTO_QUARANTINE_RELEASE_ENABLED = False


class ProviderQuarantineManager:
    """
    Manages provider quarantine state.
    auto_release_allowed = False always.
    History is append-only.
    """

    def __init__(self) -> None:
        self._records: Dict[str, QuarantineRecord] = {}  # provider_id → record
        self._all_records: List[QuarantineRecord] = []   # append-only history

    def quarantine(self, provider_id: str, reason: str,
                   triggered_by_gate: str,
                   blocking_failures: Optional[List[str]] = None,
                   evidence: str = "") -> QuarantineRecord:
        """Quarantine a provider. auto_release_allowed always False."""
        now = datetime.datetime.utcnow().isoformat() + "Z"
        qid = str(uuid.uuid4())
        record = QuarantineRecord(
            quarantine_id=qid,
            provider_id=provider_id,
            reason=reason,
            triggered_by_gate=triggered_by_gate,
            quarantined_at=now,
            quality_state=ProviderQualityState.QUARANTINED.value,
            auto_release_allowed=False,
            released=False,
            blocking_failures=blocking_failures or [],
            evidence=evidence,
        )
        self._records[provider_id] = record
        self._all_records.append(record)
        return record

    def restrict(self, provider_id: str, reason: str,
                 triggered_by_gate: str) -> QuarantineRecord:
        """Restrict a provider (RESTRICTED state)."""
        now = datetime.datetime.utcnow().isoformat() + "Z"
        qid = str(uuid.uuid4())
        record = QuarantineRecord(
            quarantine_id=qid,
            provider_id=provider_id,
            reason=reason,
            triggered_by_gate=triggered_by_gate,
            quarantined_at=now,
            quality_state=ProviderQualityState.RESTRICTED.value,
            auto_release_allowed=False,
            released=False,
        )
        self._records[provider_id] = record
        self._all_records.append(record)
        return record

    def block(self, provider_id: str, reason: str,
              triggered_by_gate: str,
              blocking_failures: Optional[List[str]] = None) -> QuarantineRecord:
        """Block a provider (BLOCKED state)."""
        now = datetime.datetime.utcnow().isoformat() + "Z"
        qid = str(uuid.uuid4())
        record = QuarantineRecord(
            quarantine_id=qid,
            provider_id=provider_id,
            reason=reason,
            triggered_by_gate=triggered_by_gate,
            quarantined_at=now,
            quality_state=ProviderQualityState.BLOCKED.value,
            auto_release_allowed=False,
            released=False,
            blocking_failures=blocking_failures or [],
        )
        self._records[provider_id] = record
        self._all_records.append(record)
        return record

    def release(self, provider_id: str, released_by: str,
                release_reason: str) -> Optional[QuarantineRecord]:
        """
        Manual release only — auto_release_allowed is always False.
        Records history entry but does NOT delete the quarantine record.
        """
        record = self._records.get(provider_id)
        if record is None:
            return None
        now = datetime.datetime.utcnow().isoformat() + "Z"
        # Create new record with released=True (append-only — old record preserved in history)
        new_record = QuarantineRecord(
            quarantine_id=record.quarantine_id,
            provider_id=record.provider_id,
            reason=record.reason,
            triggered_by_gate=record.triggered_by_gate,
            quarantined_at=record.quarantined_at,
            quality_state=ProviderQualityState.ACTIVE.value,
            auto_release_allowed=False,
            released=True,
            released_at=now,
            released_by=released_by,
            release_reason=release_reason,
            blocking_failures=record.blocking_failures,
            evidence=record.evidence,
            history=record.history + [record.to_dict()],
        )
        self._records[provider_id] = new_record
        self._all_records.append(new_record)
        return new_record

    def list_quarantined(self) -> List[QuarantineRecord]:
        return [
            r for r in self._records.values()
            if not r.released and r.quality_state in (
                ProviderQualityState.QUARANTINED.value,
                ProviderQualityState.BLOCKED.value,
                ProviderQualityState.RESTRICTED.value,
            )
        ]

    def get_record(self, provider_id: str) -> Optional[QuarantineRecord]:
        return self._records.get(provider_id)

    def evaluate_release_readiness(self, provider_id: str) -> Dict[str, Any]:
        """
        Evaluate if a provider is ready for manual release.
        auto_release_allowed is always False — human action required.
        """
        record = self._records.get(provider_id)
        if record is None:
            return {"provider_id": provider_id, "ready": False, "reason": "No quarantine record"}
        if record.released:
            return {"provider_id": provider_id, "ready": False, "reason": "Already released"}
        return {
            "provider_id": provider_id,
            "ready": False,  # always requires manual human action
            "auto_release_allowed": False,
            "blocking_failures": record.blocking_failures,
            "reason": "Manual human review required before release",
            "quality_state": record.quality_state,
        }
