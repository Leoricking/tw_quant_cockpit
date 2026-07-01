"""
paper_trading/multi_session/reconciliation_v166.py — Reconciliation v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Unknown state cannot be treated as healthy.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_UNKNOWN_AS_HEALTHY = True


@dataclass
class ReconciliationResult:
    passed: bool
    mismatches: List[str] = field(default_factory=list)
    unknown_states: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class CoordinationReconciler:
    """Reconciles coordination state. Unknown != healthy."""

    def reconcile(
        self,
        expected: Dict[str, Any],
        actual: Dict[str, Any],
        domains: List[str] = None,
    ) -> ReconciliationResult:
        if domains is None:
            domains = ["registry", "lifecycle_state", "resources", "locks", "leases",
                       "leader", "event_cursor", "risk", "capital", "checkpoints",
                       "alerts", "incidents"]
        mismatches: List[str] = []
        unknown: List[str] = []
        warnings: List[str] = []

        for domain in domains:
            exp_val = expected.get(domain)
            act_val = actual.get(domain)
            if exp_val is None and act_val is None:
                continue
            if act_val is None:
                unknown.append(domain)
                warnings.append(f"Domain '{domain}' actual state unknown — not treated as healthy")
            elif exp_val != act_val:
                mismatches.append(f"{domain}: expected={exp_val!r} actual={act_val!r}")

        return ReconciliationResult(
            passed=len(mismatches) == 0 and len(unknown) == 0,
            mismatches=mismatches,
            unknown_states=unknown,
            warnings=warnings,
        )
