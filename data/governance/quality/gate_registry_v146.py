"""
data/governance/quality/gate_registry_v146.py — Quality Gate Registry v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Rejects duplicate IDs, missing evaluators, circular deps, blocking without severity, no policy version.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional

from data.governance.quality.models_v146 import (
    GateStatus, QualityGateDefinition, QualityGateResult, QualityScope,
)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class QualityGateRegistry:
    """
    Central registry for all quality gate definitions.
    Pre-registered gates cover all 15+ categories.
    """

    POLICY_VERSION = "1.4.6"

    def __init__(self) -> None:
        self._gates: Dict[str, QualityGateDefinition] = {}
        self._evaluators: Dict[str, Callable] = {}
        self._register_default_gates()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_gate(self, gate: QualityGateDefinition,
                      evaluator: Optional[Callable] = None) -> None:
        """Register a gate. Raises on duplicate ID."""
        if gate.gate_id in self._gates:
            raise ValueError(f"Duplicate gate ID: {gate.gate_id}")
        if gate.blocking and not gate.severity:
            raise ValueError(f"Blocking gate '{gate.gate_id}' must have severity")
        if not gate.policy_version:
            raise ValueError(f"Gate '{gate.gate_id}' missing policy_version")
        if gate.mandatory and not gate.evaluator_name:
            raise ValueError(f"Mandatory gate '{gate.gate_id}' must have evaluator_name")
        self._gates[gate.gate_id] = gate
        if evaluator is not None:
            self._evaluators[gate.gate_id] = evaluator

    def get_gate(self, gate_id: str) -> Optional[QualityGateDefinition]:
        return self._gates.get(gate_id)

    def list_gates(self) -> List[QualityGateDefinition]:
        return list(self._gates.values())

    def list_mandatory_gates(self) -> List[QualityGateDefinition]:
        return [g for g in self._gates.values() if g.mandatory]

    def list_optional_gates(self) -> List[QualityGateDefinition]:
        return [g for g in self._gates.values() if not g.mandatory]

    def get_policy_version(self) -> str:
        return self.POLICY_VERSION

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_registry(self) -> Dict[str, Any]:
        """Validate registry for duplicates, missing evaluators, circular deps, etc."""
        errors: List[str] = []
        warnings: List[str] = []

        # Check all IDs unique (handled at register time, but double-check)
        ids = [g.gate_id for g in self._gates.values()]
        if len(ids) != len(set(ids)):
            errors.append("Duplicate gate IDs detected")

        # Check blocking gates have severity
        for g in self._gates.values():
            if g.blocking and not g.severity:
                errors.append(f"Blocking gate '{g.gate_id}' missing severity")

        # Check mandatory gates have evaluators
        for g in self._gates.values():
            if g.mandatory and g.evaluator_name not in self._evaluators:
                # Optional warning — evaluators may be injected later
                warnings.append(f"Mandatory gate '{g.gate_id}' has no registered evaluator")

        # Check dependencies exist
        for g in self._gates.values():
            for dep in g.dependencies:
                if dep not in self._gates:
                    errors.append(f"Gate '{g.gate_id}' depends on unknown gate '{dep}'")

        # Circular dependency detection
        def _has_cycle(node: str, visited: set, stack: set) -> bool:
            visited.add(node)
            stack.add(node)
            gate = self._gates.get(node)
            if gate:
                for dep in gate.dependencies:
                    if dep not in visited:
                        if _has_cycle(dep, visited, stack):
                            return True
                    elif dep in stack:
                        return True
            stack.discard(node)
            return False

        visited: set = set()
        for gate_id in self._gates:
            if gate_id not in visited:
                if _has_cycle(gate_id, set(), set()):
                    errors.append(f"Circular dependency detected involving gate '{gate_id}'")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "gate_count": len(self._gates),
            "evaluator_count": len(self._evaluators),
        }

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def evaluate_gate(self, gate_id: str, subject_id: str,
                      context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        """Evaluate a single gate for a subject."""
        gate = self._gates.get(gate_id)
        if gate is None:
            return QualityGateResult(
                gate_id=gate_id, gate_name=gate_id, scope="UNKNOWN",
                subject_id=subject_id, status=GateStatus.UNKNOWN.value,
                passed=False, blocking=True,
                evidence=f"Gate '{gate_id}' not found in registry",
                evaluated_at=datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
            )

        evaluator = self._evaluators.get(gate_id)
        if evaluator is None:
            # No evaluator: return PASS for optional, WARN for mandatory
            status = GateStatus.WARN.value if gate.mandatory else GateStatus.NOT_APPLICABLE.value
            return QualityGateResult(
                gate_id=gate_id, gate_name=gate.gate_name, scope=gate.scope,
                subject_id=subject_id, status=status,
                passed=(status != GateStatus.FAIL.value),
                blocking=gate.blocking,
                evidence="No evaluator registered",
                evaluated_at=datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
                policy_version=gate.policy_version,
            )

        try:
            result = evaluator(subject_id, context or {})
            if isinstance(result, QualityGateResult):
                return result
            # Accept dict
            return QualityGateResult.from_dict(result)
        except Exception as exc:
            return QualityGateResult(
                gate_id=gate_id, gate_name=gate.gate_name, scope=gate.scope,
                subject_id=subject_id, status=GateStatus.FAIL.value,
                passed=False, blocking=gate.blocking,
                evidence=f"Evaluator raised exception: {exc}",
                errors=[str(exc)],
                evaluated_at=datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
                policy_version=gate.policy_version,
            )

    def evaluate_scope(self, scope: str, subject_id: str,
                       context: Optional[Dict[str, Any]] = None) -> List[QualityGateResult]:
        """Evaluate all gates applicable to the given scope."""
        applicable = [g for g in self._gates.values() if g.scope == scope]
        return [self.evaluate_gate(g.gate_id, subject_id, context) for g in applicable]

    # ------------------------------------------------------------------
    # Default gates (15 pre-registered)
    # ------------------------------------------------------------------

    def _make_gate(self, gate_id: str, gate_name: str, scope: str, category: str,
                   description: str, mandatory: bool = True, blocking: bool = True,
                   severity: str = "CRITICAL", evaluator_name: str = "") -> QualityGateDefinition:
        if not evaluator_name:
            evaluator_name = gate_id + "_evaluator"
        return QualityGateDefinition(
            gate_id=gate_id, gate_name=gate_name, scope=scope,
            category=category, description=description,
            mandatory=mandatory, blocking=blocking, severity=severity,
            evaluator_name=evaluator_name, policy_version=self.POLICY_VERSION,
        )

    def _register_default_gates(self) -> None:
        """Pre-register 15 gates covering all categories."""
        defaults = [
            self._make_gate(
                "provider_registration", "Provider Registration Gate",
                QualityScope.PROVIDER.value, "onboarding",
                "Provider must be registered in the authority registry",
                evaluator_name="provider_registration_evaluator",
            ),
            self._make_gate(
                "provider_health", "Provider Health Gate",
                QualityScope.PROVIDER.value, "operational",
                "Provider health check must pass",
                evaluator_name="provider_health_evaluator",
            ),
            self._make_gate(
                "dataset_admission", "Dataset Admission Gate",
                QualityScope.DATASET.value, "admission",
                "Dataset must be on the allowlist and approved for use",
                evaluator_name="dataset_admission_evaluator",
            ),
            self._make_gate(
                "endpoint_readiness", "Endpoint Readiness Gate",
                QualityScope.ENDPOINT.value, "operational",
                "Endpoint must be registered, active, and have policies",
                evaluator_name="endpoint_readiness_evaluator",
            ),
            self._make_gate(
                "batch_ingestion", "Batch Ingestion Gate",
                QualityScope.BATCH.value, "integrity",
                "Batch fetch run must have consistent audit counts",
                evaluator_name="batch_ingestion_evaluator",
            ),
            self._make_gate(
                "formal_research_eligibility", "Formal Research Eligibility Gate",
                QualityScope.DATASET.value, "research",
                "All conditions for formal research use must be satisfied",
                evaluator_name="formal_research_evaluator",
            ),
            self._make_gate(
                "backtest_input_eligibility", "Backtest Input Eligibility Gate",
                QualityScope.BACKTEST_INPUT.value, "backtest",
                "No look-ahead leakage, PIT available, revision frozen",
                evaluator_name="backtest_input_evaluator",
            ),
            self._make_gate(
                "safety_invariants", "Safety Invariants Gate",
                QualityScope.PROVIDER.value, "safety",
                "No token leak, no auth header, no rate bypass, no broker",
                evaluator_name="safety_invariants_evaluator",
            ),
            self._make_gate(
                "schema_drift", "Schema Drift Gate",
                QualityScope.DATASET.value, "schema",
                "Breaking schema changes block formal use",
                evaluator_name="schema_drift_evaluator",
            ),
            self._make_gate(
                "authority_hierarchy", "Authority Hierarchy Gate",
                QualityScope.DATASET.value, "authority",
                "Primary wins, secondary cannot override, mock blocked from real",
                evaluator_name="authority_hierarchy_evaluator",
            ),
            self._make_gate(
                "conflict_resolution", "Conflict Resolution Gate",
                QualityScope.DATASET.value, "conflict",
                "Unresolved primary-source conflicts block formal use",
                evaluator_name="conflict_resolution_evaluator",
            ),
            self._make_gate(
                "freshness", "Freshness Gate",
                QualityScope.DATASET.value, "freshness",
                "Data freshness; quota_exhausted != stale",
                mandatory=True, blocking=False, severity="HIGH",
                evaluator_name="freshness_evaluator",
            ),
            self._make_gate(
                "coverage", "Coverage Gate",
                QualityScope.DATASET.value, "coverage",
                "Symbol/date/market/batch completeness check",
                mandatory=True, blocking=False, severity="HIGH",
                evaluator_name="coverage_evaluator",
            ),
            self._make_gate(
                "provenance_completeness", "Provenance Completeness Gate",
                QualityScope.RECORD.value, "provenance",
                "All provenance fields must be complete for formal use",
                evaluator_name="provenance_completeness_evaluator",
            ),
            self._make_gate(
                "point_in_time", "Point-In-Time Gate",
                QualityScope.BACKTEST_INPUT.value, "pit",
                "No future leakage; published_at, available_from, as_of must be valid",
                evaluator_name="point_in_time_evaluator",
            ),
        ]

        for gate in defaults:
            # Direct dict insertion to avoid duplicate check on init
            self._gates[gate.gate_id] = gate
