"""
paper_trading/failure_validation/safety_precheck_v165.py — Safety precheck for failure injection v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] Any injection blocked (BLOCKED_BY_SAFETY) if any of 20+ conditions fail.
[!] This precheck is the FIRST gate in the injection pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from paper_trading.failure_validation.enums_v165 import (
    FORBIDDEN_DOMAINS,
    PERMITTED_DOMAINS,
    InjectionStatus,
    FailureDomain,
)
from paper_trading.failure_validation.models_v165 import (
    FailureInjectionRequest,
    FailureInjectionResult,
    FailureScenario,
)

REAL_FAILURE_INJECTION_ENABLED = False
PRODUCTION_CHAOS_ENABLED = False
PRODUCTION_RECOVERY_ENABLED = False
AUTO_RECOVERY_EXECUTION_ENABLED = False
AUTO_FAILOVER_ENABLED = False
AUTO_RESTART_ENABLED = False
AUTO_RESUME_RUNNING = False
BROKER_FAILURE_INJECTION_ENABLED = False
NETWORK_FAILURE_INJECTION_ENABLED = False
EXTERNAL_SYSTEM_MUTATION_ENABLED = False


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class SafetyPrecheckResult:
    """Result of the safety precheck gate."""
    passed: bool = False
    blocked_reason: Optional[str] = None
    violations: List[str] = field(default_factory=list)
    checked_at: datetime = field(default_factory=_utcnow)


def run_safety_precheck(request: FailureInjectionRequest) -> SafetyPrecheckResult:
    """
    Run all 20+ safety checks. Returns BLOCKED_BY_SAFETY if any fail.
    All conditions must pass for injection to proceed.
    """
    violations: List[str] = []

    # --- Module-level global safety flags ---
    if REAL_FAILURE_INJECTION_ENABLED:
        violations.append("REAL_FAILURE_INJECTION_ENABLED is True — injection blocked globally")
    if PRODUCTION_CHAOS_ENABLED:
        violations.append("PRODUCTION_CHAOS_ENABLED is True — injection blocked globally")
    if PRODUCTION_RECOVERY_ENABLED:
        violations.append("PRODUCTION_RECOVERY_ENABLED is True — injection blocked globally")
    if AUTO_RECOVERY_EXECUTION_ENABLED:
        violations.append("AUTO_RECOVERY_EXECUTION_ENABLED is True — injection blocked globally")
    if AUTO_FAILOVER_ENABLED:
        violations.append("AUTO_FAILOVER_ENABLED is True — injection blocked globally")
    if AUTO_RESTART_ENABLED:
        violations.append("AUTO_RESTART_ENABLED is True — injection blocked globally")
    if AUTO_RESUME_RUNNING:
        violations.append("AUTO_RESUME_RUNNING is True — injection blocked globally")
    if BROKER_FAILURE_INJECTION_ENABLED:
        violations.append("BROKER_FAILURE_INJECTION_ENABLED is True — injection blocked globally")
    if NETWORK_FAILURE_INJECTION_ENABLED:
        violations.append("NETWORK_FAILURE_INJECTION_ENABLED is True — injection blocked globally")
    if EXTERNAL_SYSTEM_MUTATION_ENABLED:
        violations.append("EXTERNAL_SYSTEM_MUTATION_ENABLED is True — injection blocked globally")

    # --- Request-level safety markers ---
    if not request.fixture_only:
        violations.append("request.fixture_only must be True")
    if not request.research_only:
        violations.append("request.research_only must be True")
    if not request.paper_only:
        violations.append("request.paper_only must be True")
    if not request.no_broker:
        violations.append("request.no_broker must be True")
    if not request.no_real_account:
        violations.append("request.no_real_account must be True")
    if not request.no_real_order:
        violations.append("request.no_real_order must be True")
    if not request.not_for_production:
        violations.append("request.not_for_production must be True")
    if not request.not_live:
        violations.append("request.not_live must be True")
    if not request.failure_injection_only:
        violations.append("request.failure_injection_only must be True")
    if not request.demo_only:
        violations.append("request.demo_only must be True")

    # --- Scenario-level checks ---
    scenario = request.scenario
    if scenario is None:
        violations.append("request.scenario must not be None")
    else:
        if not scenario.fixture_only:
            violations.append("scenario.fixture_only must be True")
        if not scenario.research_only:
            violations.append("scenario.research_only must be True")
        if not scenario.paper_only:
            violations.append("scenario.paper_only must be True")
        if not scenario.no_broker:
            violations.append("scenario.no_broker must be True")
        if not scenario.no_real_account:
            violations.append("scenario.no_real_account must be True")
        if not scenario.no_real_order:
            violations.append("scenario.no_real_order must be True")
        if not scenario.not_for_production:
            violations.append("scenario.not_for_production must be True")
        if not scenario.not_live:
            violations.append("scenario.not_live must be True")
        if not scenario.reversible:
            violations.append("scenario.reversible must be True")
        if not scenario.bounded:
            violations.append("scenario.bounded must be True")
        if scenario.max_duration_ms <= 0:
            violations.append("scenario.max_duration_ms must be > 0")
        if scenario.max_duration_ms > 60000:
            violations.append("scenario.max_duration_ms must be <= 60000 ms (bounded)")

        # --- Domain checks ---
        domain_value = scenario.domain.value if isinstance(scenario.domain, FailureDomain) else str(scenario.domain)
        if domain_value in FORBIDDEN_DOMAINS:
            violations.append(f"Domain '{domain_value}' is FORBIDDEN — no injection allowed in this domain")
        if domain_value not in PERMITTED_DOMAINS:
            violations.append(f"Domain '{domain_value}' is not in PERMITTED_DOMAINS")

    if violations:
        return SafetyPrecheckResult(
            passed=False,
            blocked_reason=f"BLOCKED_BY_SAFETY: {len(violations)} violation(s): {violations[0]}",
            violations=violations,
        )

    return SafetyPrecheckResult(passed=True)


def block_result(request: FailureInjectionRequest, precheck: SafetyPrecheckResult) -> FailureInjectionResult:
    """Build a BLOCKED_BY_SAFETY result from a failed precheck."""
    result = FailureInjectionResult(
        request_id=request.request_id,
        scenario_id=request.scenario.scenario_id if request.scenario else "",
        status=InjectionStatus.BLOCKED_BY_SAFETY,
        blocked_reason=precheck.blocked_reason,
    )
    return result
