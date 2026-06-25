"""paper_trading/event_v160.py — Paper Trading Event Model v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .enums_v160 import PaperEventType


@dataclass
class PaperEvent:
    event_id: str
    sequence: int
    event_type: PaperEventType
    session_id: str
    idempotency_key: str
    timestamp: str
    payload: Dict[str, Any] = field(default_factory=dict)
    content_hash: str = ""
    previous_hash: str = ""
    paper_only: bool = True

    def __post_init__(self) -> None:
        if not self.content_hash:
            self.content_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        payload_str = json.dumps(self.payload, sort_keys=True, default=str)
        data = f"{self.event_id}|{self.sequence}|{self.event_type.value}|{self.session_id}|{self.timestamp}|{payload_str}|{self.previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()[:32]

    def verify_hash(self) -> bool:
        return self.content_hash == self._compute_hash()
