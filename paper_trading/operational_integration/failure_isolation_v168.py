"""
paper_trading/operational_integration/failure_isolation_v168.py
Failure Isolator for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from .models_v168 import IntegrationFailure
from .enums_v168 import FailureSeverity, FailureDomain

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_CRITICAL_DOMAINS = {FailureDomain.SAFETY, FailureDomain.CONTRACT}


class FailureIsolator:
    """Isolates failures to prevent cascading. Research only."""

    def isolate(self, failure: IntegrationFailure) -> Dict[str, Any]:
        """
        Isolate a failure and return isolation result.
        Returns {isolated, domain, affects_downstream, critical}.
        """
        is_critical = self.check_is_critical(failure)
        domain = self.get_failure_domain(failure)
        affects_downstream = failure.downstream_blocked or is_critical
        return {
            "isolated": True,
            "failure_id": failure.failure_id,
            "domain": domain.value,
            "affects_downstream": affects_downstream,
            "critical": is_critical,
            "recoverable": failure.recoverable,
            "paper_only": True,
        }

    def check_is_critical(self, failure: IntegrationFailure) -> bool:
        """Return True if failure is critical severity or safety domain."""
        return (
            failure.severity == FailureSeverity.CRITICAL
            or failure.domain in _CRITICAL_DOMAINS
            or failure.safety_related
        )

    def block_downstream(
        self, failure: IntegrationFailure, downstream: List[str]
    ) -> List[str]:
        """Return list of downstream components to block due to failure."""
        if not self.check_is_critical(failure) and not failure.downstream_blocked:
            return []
        return list(downstream)

    def get_failure_domain(self, failure: IntegrationFailure) -> FailureDomain:
        """Return the failure domain."""
        return failure.domain

    def summarize(self, failures: List[IntegrationFailure]) -> Dict[str, Any]:
        """Return summary of failure isolation."""
        total = len(failures)
        critical = sum(1 for f in failures if self.check_is_critical(f))
        isolated = total  # all failures are isolated
        blocking = sum(1 for f in failures if f.downstream_blocked)
        domain_dist: Dict[str, int] = {}
        for f in failures:
            d = f.domain.value
            domain_dist[d] = domain_dist.get(d, 0) + 1
        return {
            "total_failures": total,
            "critical_count": critical,
            "isolated_count": isolated,
            "blocking_count": blocking,
            "domain_distribution": domain_dist,
            "paper_only": True,
        }
