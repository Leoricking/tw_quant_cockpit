"""
paper_trading/failure_validation/idempotency_v165.py — Idempotency validation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, Set
import uuid

PAPER_ONLY = True
RESEARCH_ONLY = True


class IdempotencyValidator:
    """Validates that operations are idempotent via key tracking."""

    def __init__(self) -> None:
        self._seen_keys: Set[str] = set()
        self._duplicate_count: int = 0

    def check(self, key: str) -> Dict[str, Any]:
        is_dup = key in self._seen_keys
        if is_dup:
            self._duplicate_count += 1
        else:
            self._seen_keys.add(key)
        return {"key": key, "duplicate": is_dup, "total_seen": len(self._seen_keys)}

    def duplicate_count(self) -> int:
        return self._duplicate_count

    def unique_count(self) -> int:
        return len(self._seen_keys)

    def reset(self) -> None:
        self._seen_keys.clear()
        self._duplicate_count = 0
