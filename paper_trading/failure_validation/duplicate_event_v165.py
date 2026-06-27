"""
paper_trading/failure_validation/duplicate_event_v165.py — Duplicate event failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class DuplicateEventResult:
    component: str = ""
    original_event_id: str = ""
    duplicates_injected: int = 0
    duplicates_detected: int = 0
    duplicates_suppressed: int = 0

    @property
    def detection_rate(self) -> float:
        if self.duplicates_injected == 0:
            return 1.0
        return self.duplicates_detected / self.duplicates_injected

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "original_event_id": self.original_event_id,
            "duplicates_injected": self.duplicates_injected,
            "duplicates_detected": self.duplicates_detected,
            "duplicates_suppressed": self.duplicates_suppressed,
            "detection_rate": self.detection_rate,
        }


def simulate_duplicate_events(component: str, event_id: str, count: int = 3,
                               seed: int = 42) -> DuplicateEventResult:
    import random
    rng = random.Random(seed)
    result = DuplicateEventResult(
        component=component,
        original_event_id=event_id,
        duplicates_injected=count,
    )
    for _ in range(count):
        if rng.random() > 0.1:
            result.duplicates_detected += 1
            result.duplicates_suppressed += 1
    return result
