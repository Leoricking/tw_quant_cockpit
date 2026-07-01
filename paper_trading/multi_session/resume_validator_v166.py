"""
paper_trading/multi_session/resume_validator_v166.py — Resume Validator v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No auto-resume. Explicit validation required.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
from paper_trading.multi_session.enums_v166 import SessionLifecycleState, REQUIRES_VERIFICATION_BEFORE_RUNNING

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_AUTO_RESUME = True


@dataclass
class ResumeEligibilityResult:
    eligible: bool
    session_id: str
    checks_passed: List[str] = field(default_factory=list)
    checks_failed: List[str] = field(default_factory=list)
    reason: str = ""


class ResumeValidator:
    """
    Validates resume eligibility. All checks must pass.
    No automatic resume — always requires explicit decision.
    """

    REQUIRED_CHECKS = [
        "eligibility_check",
        "safety_check",
        "conflict_check",
        "resource_check",
        "risk_check",
        "state_verification",
        "explicit_coordination_decision",
    ]

    def validate(
        self,
        session_id: str,
        current_state: SessionLifecycleState,
        check_results: Dict[str, bool],
    ) -> ResumeEligibilityResult:
        if current_state not in REQUIRES_VERIFICATION_BEFORE_RUNNING:
            return ResumeEligibilityResult(
                eligible=False,
                session_id=session_id,
                checks_failed=["state_not_resumable"],
                reason=f"State {current_state.value} does not require resume validation",
            )
        passed = []
        failed = []
        for check in self.REQUIRED_CHECKS:
            if check_results.get(check, False):
                passed.append(check)
            else:
                failed.append(check)
        eligible = len(failed) == 0
        return ResumeEligibilityResult(
            eligible=eligible,
            session_id=session_id,
            checks_passed=passed,
            checks_failed=failed,
            reason="All checks passed" if eligible else f"Failed: {failed}",
        )
