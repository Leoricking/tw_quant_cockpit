"""
paper_trading/failure_validation/degraded_mode_v165.py — Degraded mode simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
[!] AUTO_RESUME_RUNNING_ENABLED = False. DEGRADED never auto-resumes RUNNING.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from paper_trading.failure_validation.enums_v165 import RecoveryState, AUTO_RESUME_RUNNING_ENABLED

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class DegradedModeResult:
    component: str = ""
    entered_degraded: bool = False
    auto_resume_attempted: bool = False
    auto_resume_blocked: bool = True
    manual_resume_required: bool = True
    capabilities_disabled: List[str] = field(default_factory=list)
    state: RecoveryState = RecoveryState.DEGRADED

    def as_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "entered_degraded": self.entered_degraded,
            "auto_resume_attempted": self.auto_resume_attempted,
            "auto_resume_blocked": self.auto_resume_blocked,
            "manual_resume_required": self.manual_resume_required,
            "capabilities_disabled": self.capabilities_disabled,
            "state": self.state.value,
        }


def simulate_degraded_mode(component: str, capabilities_to_disable: List[str],
                            seed: int = 42) -> DegradedModeResult:
    assert not AUTO_RESUME_RUNNING_ENABLED, "Auto resume must never be enabled"
    result = DegradedModeResult(
        component=component,
        entered_degraded=True,
        auto_resume_attempted=False,  # Never attempted
        auto_resume_blocked=True,  # Always blocked
        manual_resume_required=True,
        capabilities_disabled=capabilities_to_disable,
        state=RecoveryState.DEGRADED,
    )
    return result
