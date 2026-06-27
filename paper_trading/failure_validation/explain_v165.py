"""
paper_trading/failure_validation/explain_v165.py — Failure injection explanation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.failure_validation.enums_v165 import (
    FailureDomain, FailureType, FailureSeverity, ExpectedOutcome, RecoveryState
)
from paper_trading.failure_validation.models_v165 import FailureScenario, FailureInjectionResult

PAPER_ONLY = True
RESEARCH_ONLY = True


def explain_scenario(scenario: FailureScenario) -> Dict[str, Any]:
    """Return a human-readable explanation of a failure scenario."""
    return {
        "scenario_id": scenario.scenario_id,
        "name": scenario.name,
        "description": scenario.description,
        "domain": scenario.domain.value,
        "failure_type": scenario.failure_type.value,
        "severity": scenario.severity.value,
        "expected_outcomes": [o.value for o in scenario.expected_outcomes],
        "safety_markers": scenario.safety_markers(),
        "all_safety_markers_set": scenario.all_safety_markers_set(),
        "reversible": scenario.reversible,
        "bounded": scenario.bounded,
        "max_duration_ms": scenario.max_duration_ms,
        "cascading_targets": scenario.cascading_targets,
        "note": "This is a simulation-only scenario for research and paper trading only.",
    }


def explain_injection_result(result: FailureInjectionResult) -> Dict[str, Any]:
    """Return a human-readable explanation of an injection result."""
    return {
        "result_id": result.result_id,
        "status": result.status.value,
        "blocked_reason": result.blocked_reason,
        "detection_confirmed": result.detection_confirmed,
        "alert_generated": result.alert_generated,
        "incident_created": result.incident_created,
        "containment_confirmed": result.containment_confirmed,
        "recovery_triggered": result.recovery_triggered,
        "state_after": result.state_after.value if result.state_after else None,
        "hash_matches": result.hash_matches,
        "events_injected": result.events_injected,
        "events_reverted": result.events_reverted,
        "phases": len(result.phase_log),
    }
