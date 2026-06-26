"""
paper_trading/analytics/explain_v164.py — Analytics Explain v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Explains analytics results in human-readable form. No auto actions.
"""
from __future__ import annotations
from typing import Any, Dict, Optional

NO_REAL_ORDERS = True
PAPER_ONLY = True
AUTO_ACTION_ENABLED = False


def explain_analytics_result(
    analytics_result: Any,
    verbosity: str = "standard",
    *,
    include_lineage: bool = True,
    include_attributions: bool = True,
    include_anomalies: bool = True,
    safety_blocked: bool = False,
) -> Dict[str, Any]:
    """
    Explain an analytics result in structured dict form.
    verbosity: 'brief' | 'standard' | 'detailed'
    No auto-actions. Research only.
    """
    session_id = getattr(analytics_result, "session_id", "UNKNOWN")
    scope = getattr(analytics_result, "scope", "UNKNOWN")
    as_of = getattr(analytics_result, "as_of", None)
    metrics = getattr(analytics_result, "metrics", {})
    data_quality = getattr(analytics_result, "data_quality", "UNKNOWN")
    attributions = getattr(analytics_result, "attributions", [])
    anomalies = getattr(analytics_result, "anomalies", [])
    lineage = getattr(analytics_result, "lineage", {})

    explanation: Dict[str, Any] = {
        "session_id": session_id,
        "scope": str(scope),
        "as_of": as_of.isoformat() if as_of else None,
        "data_quality": str(data_quality),
        "paper_only": True,
        "research_only": True,
        "safety_blocked": safety_blocked,
        "auto_actions": False,
        "not_investment_advice": True,
    }

    if verbosity in ("standard", "detailed"):
        explanation["metrics_summary"] = {
            k: str(getattr(v, "value", v)) for k, v in metrics.items()
        } if metrics else {}
        if include_attributions:
            explanation["attribution_count"] = len(attributions)
        if include_anomalies:
            explanation["anomaly_count"] = len(anomalies)
            if anomalies:
                explanation["anomaly_severities"] = list(set(
                    str(getattr(a, "severity", "UNKNOWN")) for a in anomalies
                ))

    if verbosity == "detailed" and include_lineage:
        explanation["lineage"] = lineage

    return explanation


__all__ = ["explain_analytics_result"]
