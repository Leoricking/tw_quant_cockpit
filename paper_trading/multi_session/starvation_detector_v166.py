"""
paper_trading/multi_session/starvation_detector_v166.py — Starvation Detector v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No auto-production priority escalation.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_AUTO_PRODUCTION_PRIORITY_ESCALATION = True


@dataclass
class StarvationRecord:
    session_id: str
    wait_rounds: int
    denial_count: int
    fairness_score: float
    priority_value: int
    starved: bool
    escalation_recommended: bool


class StarvationDetector:
    """Detects session starvation. Recommends correction. No auto-escalation to production."""

    STARVATION_THRESHOLD = 10

    def analyze(
        self,
        session_id: str,
        wait_rounds: int,
        denial_count: int,
        priority_value: int,
    ) -> StarvationRecord:
        starved = wait_rounds >= self.STARVATION_THRESHOLD
        fairness_score = max(0.0, 1.0 - wait_rounds / (self.STARVATION_THRESHOLD * 2))
        return StarvationRecord(
            session_id=session_id,
            wait_rounds=wait_rounds,
            denial_count=denial_count,
            fairness_score=fairness_score,
            priority_value=priority_value,
            starved=starved,
            escalation_recommended=starved,
        )

    def detect_all(
        self,
        wait_records: Dict[str, Dict[str, Any]],
    ) -> List[StarvationRecord]:
        results = []
        for sid, rec in wait_records.items():
            result = self.analyze(
                session_id=sid,
                wait_rounds=rec.get("wait_rounds", 0),
                denial_count=rec.get("denial_count", 0),
                priority_value=rec.get("priority_value", 50),
            )
            results.append(result)
        return results

    def starved_sessions(self, wait_records: Dict[str, Dict[str, Any]]) -> List[str]:
        return [r.session_id for r in self.detect_all(wait_records) if r.starved]
