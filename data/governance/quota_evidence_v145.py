"""
data/governance/quota_evidence_v145.py — Quota Evidence Service v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Allowlisted headers only: X-RateLimit-*, X-Quota-*, RateLimit-*, Retry-After.
[!] Never store auth headers, cookies.
[!] FinMind status=402 → QUOTA_EXCEEDED evidence.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Dict, List, Optional

from data.governance.models_v145 import QuotaEvidence

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_ALLOWED_HEADER_PREFIXES = (
    "x-ratelimit-",
    "x-quota-",
    "ratelimit-",
    "retry-after",
)

_SECRET_HEADER_PREFIXES = (
    "authorization",
    "cookie",
    "x-auth",
    "token",
    "apikey",
    "api-key",
)

_PAYLOAD_MESSAGE_CLASSES = {
    "quota_exceeded": "QUOTA_EXCEEDED",
    "rate limited": "RATE_LIMITED",
    "auth invalid": "AUTH_INVALID",
    "auth required": "AUTH_REQUIRED",
    "invalid token": "AUTH_INVALID",
    "429": "RATE_LIMITED",
    "402": "QUOTA_EXCEEDED",
}


class QuotaEvidenceService:
    """
    Service for tracking quota evidence from providers.
    [!] Only allowlisted headers stored. No auth headers. No cookies.
    """

    def __init__(self) -> None:
        self._evidence: Dict[str, QuotaEvidence] = {}
        self._by_provider: Dict[str, List[str]] = {}
        self._order: List[str] = []

    def record_evidence(self, evidence: QuotaEvidence) -> str:
        if not evidence.evidence_id:
            evidence.evidence_id = str(uuid.uuid4())
        # Ensure no secret headers stored
        evidence.HTTP_headers = self._filter_headers(evidence.HTTP_headers)
        self._evidence[evidence.evidence_id] = evidence
        key = f"{evidence.provider_id}::{evidence.host}"
        self._by_provider.setdefault(key, []).append(evidence.evidence_id)
        if evidence.evidence_id not in self._order:
            self._order.append(evidence.evidence_id)
        return evidence.evidence_id

    def get_latest(self, provider_id: str, host: str) -> Optional[QuotaEvidence]:
        key = f"{provider_id}::{host}"
        ids = self._by_provider.get(key, [])
        if not ids:
            return None
        return self._evidence.get(ids[-1])

    def is_stale(self, evidence_id: str, max_age_seconds: int = 3600) -> bool:
        ev = self._evidence.get(evidence_id)
        if ev is None:
            return True
        try:
            captured = datetime.fromisoformat(ev.captured_at.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            age = (now - captured).total_seconds()
            return age > max_age_seconds
        except Exception:
            return True

    def _filter_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Keep only allowlisted headers, reject any auth/secret headers."""
        filtered = {}
        for k, v in headers.items():
            kl = k.lower()
            if any(kl.startswith(p) for p in _SECRET_HEADER_PREFIXES):
                continue  # Never store auth headers
            if any(kl.startswith(p) for p in _ALLOWED_HEADER_PREFIXES):
                filtered[k] = v
        return filtered

    def extract_from_headers(
        self,
        provider_id: str,
        host: str,
        headers: Dict[str, str],
    ) -> Optional[QuotaEvidence]:
        """Extract quota evidence from response headers (allowlisted only)."""
        safe = self._filter_headers(headers)
        if not safe:
            return None
        evidence_id = str(uuid.uuid4())
        ev = QuotaEvidence(
            evidence_id=evidence_id,
            provider_id=provider_id,
            host=host,
            source="RESPONSE_HEADERS",
            captured_at=datetime.now(timezone.utc).isoformat(),
            HTTP_headers=safe,
            confidence="MEDIUM",
        )
        # Parse known header values
        for k, v in safe.items():
            kl = k.lower()
            if "remaining" in kl:
                try:
                    ev.remaining = int(v)
                except ValueError:
                    pass
            elif "limit" in kl and "ratelimit" in kl:
                try:
                    ev.limit = int(v)
                except ValueError:
                    pass
            elif "reset" in kl:
                ev.reset_at = v
        return ev

    def extract_from_payload(
        self,
        provider_id: str,
        payload_status: Optional[int],
        payload_msg: Optional[str],
    ) -> Optional[QuotaEvidence]:
        """
        Extract quota evidence from payload.
        FinMind status=402 → QUOTA_EXCEEDED.
        """
        if payload_status is None:
            return None
        msg_class = self.classify_payload_message(str(payload_msg or ""))
        if payload_status == 402:
            msg_class = "QUOTA_EXCEEDED"
        elif payload_status == 429:
            msg_class = "RATE_LIMITED"

        if msg_class in ("QUOTA_EXCEEDED", "RATE_LIMITED"):
            evidence_id = str(uuid.uuid4())
            return QuotaEvidence(
                evidence_id=evidence_id,
                provider_id=provider_id,
                host="",
                source="PAYLOAD",
                captured_at=datetime.now(timezone.utc).isoformat(),
                payload_status=payload_status,
                payload_message_class=msg_class,
                confidence="HIGH" if payload_status in (402, 429) else "LOW",
            )
        return None

    def classify_payload_message(self, msg: str) -> str:
        """Classify a payload message string."""
        ml = msg.lower()
        for pattern, cls in _PAYLOAD_MESSAGE_CLASSES.items():
            if pattern.lower() in ml:
                return cls
        return "UNKNOWN"
