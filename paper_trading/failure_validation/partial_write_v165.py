"""
paper_trading/failure_validation/partial_write_v165.py — Partial write failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class PartialWriteResult:
    component: str = ""
    total_records: int = 0
    written_records: int = 0
    failed_records: int = 0
    detected: bool = False
    rollback_attempted: bool = False
    rollback_succeeded: bool = False

    @property
    def write_ratio(self) -> float:
        if self.total_records == 0:
            return 0.0
        return self.written_records / self.total_records

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "total_records": self.total_records,
            "written_records": self.written_records,
            "failed_records": self.failed_records,
            "write_ratio": self.write_ratio,
            "detected": self.detected,
            "rollback_attempted": self.rollback_attempted,
            "rollback_succeeded": self.rollback_succeeded,
        }


def simulate_partial_write(component: str, total_records: int = 100,
                            fail_at_record: int = 50, seed: int = 42) -> PartialWriteResult:
    import random
    rng = random.Random(seed)
    written = min(fail_at_record, total_records)
    result = PartialWriteResult(
        component=component,
        total_records=total_records,
        written_records=written,
        failed_records=total_records - written,
    )
    result.detected = result.failed_records > 0 and rng.random() > 0.05
    if result.detected:
        result.rollback_attempted = True
        result.rollback_succeeded = rng.random() > 0.1
    return result
