"""
paper_trading/multi_session/metrics_v166.py — Coordination Metrics v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List
from paper_trading.multi_session.models_v166 import CoordinationResult

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True


class CoordinationMetrics:
    """Computes aggregate coordination metrics."""

    def compute(self, results: List[CoordinationResult]) -> Dict[str, Any]:
        if not results:
            return {"total_coordinations": 0}
        total = len(results)
        total_admitted = sum(len(r.sessions_admitted) for r in results)
        total_blocked = sum(len(r.sessions_blocked) for r in results)
        total_conflicts = sum(r.conflicts_detected for r in results)
        total_unresolved = sum(r.conflicts_unresolved for r in results)
        total_warnings = sum(len(r.warnings) for r in results)
        return {
            "total_coordinations": total,
            "total_admitted": total_admitted,
            "total_blocked": total_blocked,
            "total_conflicts_detected": total_conflicts,
            "total_conflicts_unresolved": total_unresolved,
            "total_warnings": total_warnings,
            "avg_admitted_per_coord": total_admitted / total,
            "admission_rate": total_admitted / (total_admitted + total_blocked) if (total_admitted + total_blocked) > 0 else 0.0,
        }
