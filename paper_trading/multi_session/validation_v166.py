"""
paper_trading/multi_session/validation_v166.py — Multi-session Coordination validation v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import (
    SessionType, SessionLifecycleState, VALID_LIFECYCLE_TRANSITIONS,
    REQUIRES_VERIFICATION_BEFORE_RUNNING, FORBIDDEN_SESSION_TYPES,
)

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True


@dataclass
class ValidationResult:
    valid: bool
    violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_violation(self, msg: str) -> None:
        self.valid = False
        self.violations.append(msg)

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)


def validate_session_descriptor(desc: Any) -> ValidationResult:
    result = ValidationResult(valid=True)
    if not desc.session_id:
        result.add_violation("session_id is required")
    if not desc.owner:
        result.add_violation("owner is required")
    if desc.session_type is None:
        result.add_violation("session_type is required")
    elif hasattr(desc.session_type, 'value') and desc.session_type.value in FORBIDDEN_SESSION_TYPES:
        result.add_violation(f"Forbidden session type: {desc.session_type.value}")
    if not desc.policy_version:
        result.add_violation("policy_version is required")
    if not desc.code_version:
        result.add_violation("code_version is required")
    if not desc.capabilities:
        result.add_warning("No capabilities declared; may be BLOCKED_BY_CAPABILITY")
    if desc.risk_budget < 0:
        result.add_violation("risk_budget cannot be negative")
    if desc.capital_budget < 0:
        result.add_violation("capital_budget cannot be negative")
    return result


def validate_lifecycle_transition(
    from_state: SessionLifecycleState,
    to_state: SessionLifecycleState,
    verified: bool = False,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    allowed = VALID_LIFECYCLE_TRANSITIONS.get(from_state, set())
    if to_state not in allowed:
        result.add_violation(
            f"Invalid transition {from_state.value} -> {to_state.value}"
        )
    if to_state == SessionLifecycleState.RUNNING and from_state in REQUIRES_VERIFICATION_BEFORE_RUNNING:
        if not verified:
            result.add_violation(
                f"Transition to RUNNING from {from_state.value} requires explicit verification"
            )
    return result


def validate_capability_required(
    session_capabilities: List[str],
    required_capability: str,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    if required_capability not in session_capabilities:
        result.add_violation(
            f"BLOCKED_BY_CAPABILITY: {required_capability} not declared"
        )
    return result


def validate_no_duplicate_session(
    existing_ids: List[str],
    new_id: str,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    if new_id in existing_ids:
        result.add_violation(f"Duplicate session_id: {new_id}")
    return result


def validate_policy(policy: Any) -> ValidationResult:
    result = ValidationResult(valid=True)
    if not policy.policy_id:
        result.add_violation("policy_id is required")
    if not policy.version:
        result.add_violation("version is required")
    if policy.max_concurrent_sessions < 1:
        result.add_violation("max_concurrent_sessions must be >= 1")
    return result


def validate_reservation(reservation: Any) -> ValidationResult:
    result = ValidationResult(valid=True)
    if not reservation.reservation_id:
        result.add_violation("reservation_id is required")
    if not reservation.session_id:
        result.add_violation("session_id is required")
    if reservation.quantity <= 0:
        result.add_violation("quantity must be positive")
    if reservation.expires_at and reservation.expires_at <= reservation.reserved_at:
        result.add_violation("expires_at must be after reserved_at")
    return result
