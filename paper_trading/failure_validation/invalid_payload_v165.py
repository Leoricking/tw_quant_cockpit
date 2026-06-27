"""
paper_trading/failure_validation/invalid_payload_v165.py — Invalid payload failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class InvalidPayloadResult:
    component: str = ""
    validation_errors: List[str] = field(default_factory=list)
    rejected: bool = False
    downstream_blocked: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "validation_errors": self.validation_errors,
            "rejected": self.rejected,
            "downstream_blocked": self.downstream_blocked,
        }


def simulate_invalid_payload(component: str, errors: List[str],
                              seed: int = 42) -> InvalidPayloadResult:
    import random
    rng = random.Random(seed)
    result = InvalidPayloadResult(component=component, validation_errors=errors)
    if errors:
        result.rejected = True
        result.downstream_blocked = True
    return result
