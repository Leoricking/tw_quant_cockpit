"""paper_trading/idempotency_v160.py — Idempotent Event Processing v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
"""
from __future__ import annotations
from typing import Dict, Optional, Set


class IdempotencyRegistry:
    """Tracks processed idempotency keys to prevent duplicate event processing."""

    def __init__(self) -> None:
        self._seen: Dict[str, int] = {}  # key -> sequence

    def is_duplicate(self, idempotency_key: str) -> bool:
        return idempotency_key in self._seen

    def register(self, idempotency_key: str, sequence: int) -> None:
        if idempotency_key in self._seen:
            raise ValueError(f"Duplicate idempotency key: {idempotency_key}")
        self._seen[idempotency_key] = sequence

    def get_sequence(self, idempotency_key: str) -> Optional[int]:
        return self._seen.get(idempotency_key)

    def count(self) -> int:
        return len(self._seen)

    def reset(self) -> None:
        self._seen.clear()
