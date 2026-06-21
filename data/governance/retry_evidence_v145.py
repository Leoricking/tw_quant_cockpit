"""
data/governance/retry_evidence_v145.py — Retry Evidence Service v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Injectable clock for tests. No real sleep in tests.
"""
from __future__ import annotations

import math
import random
import uuid
from email.utils import parsedate_to_datetime
from typing import Any, Callable, Dict, List, Optional

from data.governance.models_v145 import RetryEvidence

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class RetryEvidenceService:
    """
    Service for tracking retry evidence.
    [!] Injectable clock for deterministic tests. No real sleep.
    """

    def __init__(self, clock: Optional[Callable[[], float]] = None) -> None:
        import time
        self._clock = clock or time.time
        self._evidence: Dict[str, RetryEvidence] = {}
        self._by_request: Dict[str, List[str]] = {}
        self._order: List[str] = []

    def record_retry(self, evidence: RetryEvidence) -> str:
        if not evidence.retry_id:
            evidence.retry_id = str(uuid.uuid4())
        self._evidence[evidence.retry_id] = evidence
        self._by_request.setdefault(evidence.request_id, []).append(evidence.retry_id)
        if evidence.retry_id not in self._order:
            self._order.append(evidence.retry_id)
        return evidence.retry_id

    def get_retry(self, retry_id: str) -> Optional[RetryEvidence]:
        return self._evidence.get(retry_id)

    def list_by_request(self, request_id: str) -> List[Dict[str, Any]]:
        ids = self._by_request.get(request_id, [])
        return [self._evidence[rid].to_dict() for rid in ids if rid in self._evidence]

    def parse_retry_after_header(self, value: str) -> float:
        """
        Parse Retry-After header value.
        Handles both integer seconds and HTTP-date format.
        """
        value = value.strip()
        try:
            return float(value)
        except ValueError:
            pass
        # Try HTTP-date format
        try:
            dt = parsedate_to_datetime(value)
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc)
            delta = (dt - now).total_seconds()
            return max(0.0, delta)
        except Exception:
            return 0.0

    def calculate_backoff(
        self,
        attempt: int,
        base_seconds: float = 1.0,
        max_seconds: float = 60.0,
        jitter: bool = True,
        clock: Optional[Callable[[], float]] = None,
    ) -> float:
        """
        Exponential backoff with optional jitter.
        Injectable clock for tests — no real sleep.
        """
        raw = min(base_seconds * (2 ** (attempt - 1)), max_seconds)
        if jitter:
            # Use deterministic jitter based on clock if provided
            rng = random.Random(int((clock or self._clock)() * 1000) % 10000)
            raw = raw * (0.5 + rng.random() * 0.5)
        return round(raw, 3)
