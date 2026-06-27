"""
paper_trading/failure_validation/cascading_v165.py — Cascading failure simulation v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] Deterministic, bounded, in-memory cascading simulation only.
"""
from __future__ import annotations

import random
from typing import Any, Dict, List, Optional

from paper_trading.failure_validation.enums_v165 import (
    ExpectedOutcome,
    FailureDomain,
    FailureSeverity,
    FailureType,
    RecoveryState,
)
from paper_trading.failure_validation.models_v165 import (
    FailureInjectionRequest,
    FailureInjectionResult,
    FailureScenario,
)
from paper_trading.failure_validation.injector_v165 import DeterministicFailureInjector

PAPER_ONLY = True
RESEARCH_ONLY = True
REAL_FAILURE_INJECTION_ENABLED = False


def simulate_cascading_failure(
    scenario: FailureScenario,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Simulate a cascading failure chain from a primary scenario.
    Returns dict with chain results for each domain in cascading_targets.
    """
    injector = DeterministicFailureInjector()
    rng = random.Random(seed)

    primary_request = FailureInjectionRequest(
        scenario=scenario,
        requested_by="cascading_test_harness",
        target_component=scenario.domain.value,
    )
    primary_result = injector.inject(primary_request)

    chain: List[Dict[str, Any]] = [{
        "step": 0,
        "domain": scenario.domain.value,
        "failure_type": scenario.failure_type.value,
        "status": primary_result.status.value,
        "detected": primary_result.detection_confirmed,
        "contained": primary_result.containment_confirmed,
    }]

    # Propagate cascading effects
    previous_contained = primary_result.containment_confirmed
    for step_idx, target_domain_str in enumerate(scenario.cascading_targets, start=1):
        try:
            target_domain = FailureDomain(target_domain_str)
        except ValueError:
            chain.append({
                "step": step_idx,
                "domain": target_domain_str,
                "status": "SKIPPED",
                "reason": f"Unknown domain: {target_domain_str}",
            })
            continue

        # If primary not contained, cascade propagates with higher probability
        propagation_probability = 0.85 if not previous_contained else 0.30
        propagates = rng.random() < propagation_probability

        if not propagates:
            chain.append({
                "step": step_idx,
                "domain": target_domain_str,
                "status": "NO_PROPAGATION",
                "detected": False,
                "contained": True,
            })
            continue

        # Pick a plausible cascading failure type
        cascade_type = _cascading_failure_type(target_domain, rng)
        cascade_scenario = FailureScenario(
            name=f"cascade_step_{step_idx}_{target_domain_str.lower()}",
            description=f"Cascading failure in {target_domain_str} (step {step_idx})",
            domain=target_domain,
            failure_type=cascade_type,
            severity=scenario.severity,
            expected_outcomes=[ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED],
            seed=seed + step_idx,
            max_duration_ms=5000,
            reversible=True,
            bounded=True,
            fixture_only=True,
            research_only=True,
            paper_only=True,
            no_broker=True,
            no_real_account=True,
            no_real_order=True,
            not_for_production=True,
            not_live=True,
            failure_injection_only=True,
            demo_only=True,
        )

        cascade_request = FailureInjectionRequest(
            scenario=cascade_scenario,
            requested_by="cascading_test_harness",
            target_component=target_domain_str,
        )
        cascade_result = injector.inject(cascade_request)
        previous_contained = cascade_result.containment_confirmed

        chain.append({
            "step": step_idx,
            "domain": target_domain_str,
            "failure_type": cascade_type.value,
            "status": cascade_result.status.value,
            "detected": cascade_result.detection_confirmed,
            "contained": cascade_result.containment_confirmed,
            "state_after": cascade_result.state_after.value if cascade_result.state_after else None,
        })

    final_state = RecoveryState.HEALTHY
    if chain:
        last = chain[-1]
        if not last.get("contained", True):
            final_state = RecoveryState.DEGRADED
        elif last.get("status") == "BLOCKED_BY_SAFETY":
            final_state = RecoveryState.BLOCKED

    return {
        "scenario_id": scenario.scenario_id,
        "scenario_name": scenario.name,
        "chain_length": len(chain),
        "chain": chain,
        "final_state": final_state.value,
        "primary_detected": primary_result.detection_confirmed,
        "primary_contained": primary_result.containment_confirmed,
        "all_contained": all(step.get("contained", True) for step in chain),
    }


def _cascading_failure_type(domain: FailureDomain, rng: random.Random) -> FailureType:
    """Pick a plausible cascading failure type for a domain."""
    domain_to_types: Dict[FailureDomain, List[FailureType]] = {
        FailureDomain.MARKET_DATA:      [FailureType.STALE_DATA, FailureType.MISSING_DATA],
        FailureDomain.SESSION_STATE:    [FailureType.STATE_DIVERGENCE, FailureType.DEGRADED_MODE],
        FailureDomain.STRATEGY_SIGNAL:  [FailureType.MISSING_DATA, FailureType.INVALID_PAYLOAD],
        FailureDomain.PAPER_ORDER:      [FailureType.WRITE_FAILURE, FailureType.TIMEOUT],
        FailureDomain.PAPER_FILL:       [FailureType.MISSING_DATA, FailureType.PARTIAL_WRITE],
        FailureDomain.EVENT_STREAM:     [FailureType.EVENT_LOSS, FailureType.EVENT_STORM],
        FailureDomain.CHECKPOINT:       [FailureType.CHECKPOINT_CORRUPTION, FailureType.HASH_MISMATCH],
        FailureDomain.STORE:            [FailureType.WRITE_FAILURE, FailureType.READ_FAILURE],
        FailureDomain.QUERY:            [FailureType.TIMEOUT, FailureType.MISSING_DATA],
        FailureDomain.ALERT:            [FailureType.ALERT_LOSS, FailureType.INCIDENT_CREATION_FAILURE],
        FailureDomain.INCIDENT:         [FailureType.INCIDENT_CREATION_FAILURE],
        FailureDomain.RECOVERY:         [FailureType.RECOVERY_FAILURE, FailureType.REPLAY_MISMATCH],
        FailureDomain.ANALYTICS:        [FailureType.MISSING_DATA, FailureType.STALE_DATA],
        FailureDomain.REPORT:           [FailureType.MISSING_DATA, FailureType.TIMEOUT],
        FailureDomain.DEPENDENCY:       [FailureType.DEPENDENCY_UNAVAILABLE, FailureType.CIRCUIT_OPEN],
        FailureDomain.TIME:             [FailureType.CLOCK_SKEW, FailureType.DELAY],
        FailureDomain.CONFIGURATION:    [FailureType.CONFIG_DRIFT, FailureType.INVALID_PAYLOAD],
    }
    choices = domain_to_types.get(domain, [FailureType.TIMEOUT])
    return rng.choice(choices)
