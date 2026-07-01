"""
paper_trading/multi_session/fairness_engine_v166.py — Fairness Engine v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.models_v166 import SessionDescriptor

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True
NO_INFINITE_STARVATION = True


@dataclass
class FairnessRecord:
    session_id: str
    grant_count: int = 0
    denial_count: int = 0
    wait_rounds: int = 0
    consecutive_grants: int = 0
    fairness_score: float = 1.0
    starvation_flag: bool = False


class FairnessEngine:
    """
    Aging-weighted FIFO fairness.
    Prevents starvation. No infinite denial. No hidden preference.
    Deterministic tie-break.
    """

    STARVATION_THRESHOLD = 10

    def __init__(self) -> None:
        self._records: Dict[str, FairnessRecord] = {}

    def get_record(self, session_id: str) -> FairnessRecord:
        if session_id not in self._records:
            self._records[session_id] = FairnessRecord(session_id=session_id)
        return self._records[session_id]

    def record_grant(self, session_id: str) -> None:
        r = self.get_record(session_id)
        r.grant_count += 1
        r.consecutive_grants += 1
        r.wait_rounds = 0
        r.denial_count = 0
        r.starvation_flag = False

    def record_denial(self, session_id: str) -> None:
        r = self.get_record(session_id)
        r.denial_count += 1
        r.wait_rounds += 1
        r.consecutive_grants = 0
        if r.wait_rounds >= self.STARVATION_THRESHOLD:
            r.starvation_flag = True

    def compute_aging_bonus(self, session_id: str) -> float:
        r = self.get_record(session_id)
        return r.wait_rounds * 0.1

    def detect_starvation(self) -> List[str]:
        return [sid for sid, r in self._records.items() if r.starvation_flag]

    def max_consecutive_grants_exceeded(self, session_id: str, max_grants: int = 5) -> bool:
        return self.get_record(session_id).consecutive_grants >= max_grants

    def fairness_summary(self) -> Dict[str, Any]:
        return {
            sid: {
                "grants": r.grant_count,
                "denials": r.denial_count,
                "wait_rounds": r.wait_rounds,
                "starvation": r.starvation_flag,
            }
            for sid, r in self._records.items()
        }
