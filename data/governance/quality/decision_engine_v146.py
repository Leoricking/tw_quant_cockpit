"""
data/governance/quality/decision_engine_v146.py — Quality Decision Engine v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Blocking rules ALWAYS override score — never the reverse.
[!] QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False (always).
"""
from __future__ import annotations

import datetime
import uuid
from typing import Any, Dict, List, Optional

from data.governance.quality.models_v146 import (
    GateStatus, ProviderQualityState, QualityDecision,
    QualityDecisionResult, QualityGateResult, QualityScope,
)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False


class QualityDecisionEngine:
    """
    Evaluates all applicable gates for a scope and returns a QualityDecision.
    Blocking rules ALWAYS take strict precedence over quality score.
    Score CANNOT override blocking failures.
    """

    POLICY_VERSION = "1.4.6"

    def __init__(self, gate_registry=None) -> None:
        self._registry = gate_registry

    def decide(
        self,
        scope: str,
        subject_id: str,
        gate_results: List[QualityGateResult],
        quality_score: Optional[float] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> QualityDecision:
        """
        Make a quality decision based on gate results.
        Blocking failures always override score.
        """
        now = datetime.datetime.utcnow().isoformat() + "Z"
        decision_id = str(uuid.uuid4())

        blocking_failures = [
            r.gate_id for r in gate_results
            if r.blocking and r.status in (GateStatus.BLOCKED.value, GateStatus.FAIL.value)
        ]
        warnings = []
        for r in gate_results:
            warnings.extend(r.warnings)
            if r.status == GateStatus.WARN.value:
                warnings.append(f"Gate '{r.gate_id}' returned WARN: {r.evidence}")

        # Safety: score CANNOT override blocking failures
        if blocking_failures:
            decision = QualityDecisionResult.BLOCK.value
            quality_state = ProviderQualityState.BLOCKED.value
            formal_research_allowed = False
            backtest_allowed = False
            report_allowed = False
            ingestion_allowed = False
        elif any(r.status == GateStatus.FAIL.value for r in gate_results):
            decision = QualityDecisionResult.RESTRICT.value
            quality_state = ProviderQualityState.RESTRICTED.value
            formal_research_allowed = False
            backtest_allowed = False
            report_allowed = False
            ingestion_allowed = True
        elif warnings:
            decision = QualityDecisionResult.ALLOW_WITH_WARNING.value
            quality_state = ProviderQualityState.DEGRADED.value
            formal_research_allowed = True
            backtest_allowed = True
            report_allowed = True
            ingestion_allowed = True
        else:
            decision = QualityDecisionResult.ALLOW.value
            quality_state = ProviderQualityState.ACTIVE.value
            formal_research_allowed = True
            backtest_allowed = True
            report_allowed = True
            ingestion_allowed = True

        return QualityDecision(
            decision_id=decision_id,
            scope=scope,
            subject_id=subject_id,
            decision=decision,
            quality_state=quality_state,
            formal_research_allowed=formal_research_allowed,
            backtest_allowed=backtest_allowed,
            report_allowed=report_allowed,
            ingestion_allowed=ingestion_allowed,
            blocking_failures=blocking_failures,
            warnings=warnings,
            gate_results=[r.to_dict() for r in gate_results],
            quality_score=quality_score,
            decided_at=now,
            policy_version=self.POLICY_VERSION,
            score_overrode_blocking=False,  # always False
        )

    def evaluate_provider(
        self, provider_id: str, context: Optional[Dict[str, Any]] = None
    ) -> QualityDecision:
        """Evaluate all PROVIDER-scope gates for a provider."""
        results = []
        if self._registry:
            results = self._registry.evaluate_scope(
                QualityScope.PROVIDER.value, provider_id, context
            )
        return self.decide(QualityScope.PROVIDER.value, provider_id, results)

    def evaluate_dataset(
        self, dataset_id: str, context: Optional[Dict[str, Any]] = None
    ) -> QualityDecision:
        """Evaluate all DATASET-scope gates for a dataset."""
        results = []
        if self._registry:
            results = self._registry.evaluate_scope(
                QualityScope.DATASET.value, dataset_id, context
            )
        return self.decide(QualityScope.DATASET.value, dataset_id, results)

    def evaluate_endpoint(
        self, endpoint_id: str, context: Optional[Dict[str, Any]] = None
    ) -> QualityDecision:
        """Evaluate all ENDPOINT-scope gates for an endpoint."""
        results = []
        if self._registry:
            results = self._registry.evaluate_scope(
                QualityScope.ENDPOINT.value, endpoint_id, context
            )
        return self.decide(QualityScope.ENDPOINT.value, endpoint_id, results)

    def evaluate_fetch_run(
        self, fetch_run_id: str, context: Optional[Dict[str, Any]] = None
    ) -> QualityDecision:
        """Evaluate FETCH_RUN-scope gates."""
        results = []
        if self._registry:
            results = self._registry.evaluate_scope(
                QualityScope.FETCH_RUN.value, fetch_run_id, context
            )
        return self.decide(QualityScope.FETCH_RUN.value, fetch_run_id, results)
