"""
Explainability v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from paper_trading.operations.enums_v163 import OperationalStatus, HealthStatus


def explain_operational_state(
    market_data:    OperationalStatus,
    paper_trading:  OperationalStatus,
    paper_strategy: OperationalStatus,
    composite:      OperationalStatus,
    reason:         str,
    *,
    safety_blocked: bool = False,
    incidents:      Optional[List[str]] = None,
    alerts:         Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "composite_status":    str(composite),
        "reason":              reason,
        "layer_statuses": {
            "market_data":    str(market_data),
            "paper_trading":  str(paper_trading),
            "paper_strategy": str(paper_strategy),
        },
        "safety_blocked":      safety_blocked,
        "deterministic":       True,
        "no_optimistic_override": True,
        "incidents":           incidents or [],
        "alerts":              alerts or [],
        "version":             "1.6.3",
        "paper_only":          True,
        "research_only":       True,
    }


def explain_health(
    overall:    HealthStatus,
    components: Dict[str, HealthStatus],
    reasons:    List[str],
) -> Dict[str, Any]:
    return {
        "overall_health":  str(overall),
        "components":      {k: str(v) for k, v in components.items()},
        "reasons":         reasons,
        "priority_rule":   "BLOCKED > CRITICAL > UNHEALTHY > DEGRADED > WARNING > HEALTHY > UNKNOWN",
        "safety_priority": True,
        "version":         "1.6.3",
    }


__all__ = ["explain_operational_state", "explain_health"]
