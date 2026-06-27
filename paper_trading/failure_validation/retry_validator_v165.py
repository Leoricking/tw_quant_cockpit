"""
paper_trading/failure_validation/retry_validator_v165.py — Retry validation v1.6.5.
[!] Research Only. No Real Orders. No Real Network Calls. Not Investment Advice.
[!] Virtual clock only. No real sleep. Idempotency key validated.
"""
from __future__ import annotations

import uuid
from typing import Any, Callable, Dict, List, Optional

from paper_trading.failure_validation.models_v165 import RetryRecord

PAPER_ONLY = True
RESEARCH_ONLY = True


def simulate_retry_sequence(
    max_attempts: int = 3,
    backoff_ms: int = 100,
    succeed_on_attempt: Optional[int] = None,
    idempotency_key: Optional[str] = None,
    seed: int = 42,
) -> RetryRecord:
    """
    Simulate a retry sequence with virtual clock. No real sleep.
    Returns a RetryRecord with all attempt details.
    """
    import random
    rng = random.Random(seed)

    key = idempotency_key or str(uuid.uuid4())
    record = RetryRecord(
        idempotency_key=key,
        max_attempts=max_attempts,
        backoff_ms=backoff_ms,
    )

    for attempt_num in range(1, max_attempts + 1):
        if succeed_on_attempt is not None:
            success = (attempt_num == succeed_on_attempt)
        else:
            success = rng.random() > 0.5

        record.record_attempt(success, detail=f"attempt_{attempt_num}_seed_{seed}")

        if success or record.exhausted:
            break

    return record


def validate_idempotency(
    key: str,
    seen_keys: set,
) -> Dict[str, Any]:
    """
    Validate that an idempotency key has not been seen before.
    Returns {"duplicate": bool, "key": str}.
    """
    is_duplicate = key in seen_keys
    if not is_duplicate:
        seen_keys.add(key)
    return {"duplicate": is_duplicate, "key": key}
