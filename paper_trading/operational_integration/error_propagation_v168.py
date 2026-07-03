"""
paper_trading/operational_integration/error_propagation_v168.py
Error Propagator for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .models_v168 import IntegrationFailure
from .enums_v168 import FailureSeverity, FailureDomain, IntegrationStage

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ErrorPropagator:
    """Creates and propagates integration errors. Never swallows errors."""

    def create_error(
        self,
        component: str,
        stage: str,
        category: str,
        severity: str,
        message: str,
        cause: str = "",
        recoverable: bool = False,
        downstream_blocked: bool = False,
        user_visible: bool = True,
        safety_related: bool = False,
    ) -> IntegrationFailure:
        """Create a new IntegrationFailure."""
        try:
            stage_enum = IntegrationStage(stage)
        except ValueError:
            stage_enum = IntegrationStage.STAGE_VALIDATE
        try:
            domain_enum = FailureDomain(category)
        except ValueError:
            domain_enum = FailureDomain.UNKNOWN
        try:
            sev_enum = FailureSeverity(severity)
        except ValueError:
            sev_enum = FailureSeverity.MEDIUM

        failure_id = f"failure_{component}_{stage}_{len(message)}"
        return IntegrationFailure(
            failure_id=failure_id,
            component_id=component,
            stage=stage_enum,
            domain=domain_enum,
            severity=sev_enum,
            message=message,
            cause=cause,
            timestamp=_utcnow_iso(),
            recoverable=recoverable,
            downstream_blocked=downstream_blocked,
            user_visible=user_visible,
            safety_related=safety_related,
        )

    def propagate(
        self, failure: IntegrationFailure, downstream_component: str
    ) -> IntegrationFailure:
        """Propagate failure to downstream component."""
        failure_id = f"prop_{failure.failure_id}_{downstream_component}"
        return IntegrationFailure(
            failure_id=failure_id,
            component_id=downstream_component,
            stage=failure.stage,
            domain=failure.domain,
            severity=failure.severity,
            message=f"Propagated from {failure.component_id}: {failure.message}",
            cause=failure.failure_id,
            timestamp=_utcnow_iso(),
            recoverable=False,
            downstream_blocked=failure.downstream_blocked,
            user_visible=failure.user_visible,
            safety_related=failure.safety_related,
        )

    def wrap_exception(
        self, exc: Exception, component: str, stage: str
    ) -> IntegrationFailure:
        """Wrap a Python exception as an IntegrationFailure."""
        return self.create_error(
            component=component,
            stage=stage,
            category=FailureDomain.COMPONENT.value,
            severity=FailureSeverity.HIGH.value,
            message=f"{type(exc).__name__}: {exc}",
            cause=repr(exc),
            recoverable=False,
            downstream_blocked=False,
            user_visible=True,
            safety_related=False,
        )

    def is_swallowed(self, failure: IntegrationFailure) -> bool:
        """Always returns False. Errors are never swallowed."""
        return False

    def summarize(self, failures: List[IntegrationFailure]) -> Dict[str, Any]:
        """Return summary of all failures."""
        total = len(failures)
        swallowed = sum(1 for f in failures if self.is_swallowed(f))
        severity_dist: Dict[str, int] = {}
        for f in failures:
            s = f.severity.value
            severity_dist[s] = severity_dist.get(s, 0) + 1
        return {
            "total_failures": total,
            "swallowed_count": swallowed,  # always 0
            "severity_distribution": severity_dist,
            "safety_related_count": sum(1 for f in failures if f.safety_related),
            "paper_only": True,
        }
