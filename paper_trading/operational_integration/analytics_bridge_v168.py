"""
paper_trading/operational_integration/analytics_bridge_v168.py
Analytics Bridge for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class AnalyticsBridge:
    """Validates analytics metrics and propagates degraded status. Research only."""

    def check_metric_identity(self, metric: Dict[str, Any]) -> Dict[str, Any]:
        """Validate metric has required identity fields."""
        required = ["metric_id", "run_id", "session_id", "metric_name", "period_start", "period_end"]
        missing = [f for f in required if f not in metric]
        return {
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "metric_id": metric.get("metric_id", ""),
            "paper_only": True,
        }

    def check_period_alignment(
        self, metric: Dict[str, Any], expected_period: tuple
    ) -> bool:
        """Return True if metric period aligns with expected_period (start, end)."""
        expected_start, expected_end = expected_period
        metric_start = metric.get("period_start", "")
        metric_end = metric.get("period_end", "")
        if not metric_start or not metric_end:
            return False
        return metric_start == expected_start and metric_end == expected_end

    def check_confidence(self, metric: Dict[str, Any]) -> Dict[str, Any]:
        """Return confidence level for a metric."""
        confidence = metric.get("confidence", metric.get("confidence_level", "UNKNOWN"))
        known_levels = {"HIGH", "MEDIUM", "LOW", "VERY_LOW", "UNKNOWN"}
        if confidence not in known_levels:
            confidence = "UNKNOWN"
        return {
            "confidence": confidence,
            "is_high_confidence": confidence == "HIGH",
            "metric_id": metric.get("metric_id", ""),
            "paper_only": True,
        }

    def propagate_degraded(
        self, metric: Dict[str, Any], upstream_status: str
    ) -> Dict[str, Any]:
        """Propagate degraded status from upstream to metric."""
        if upstream_status in ("DEGRADED", "FAILED", "INSUFFICIENT_DATA"):
            return {
                **metric,
                "status": "DEGRADED",
                "degraded_reason": f"upstream_{upstream_status.lower()}",
                "paper_only": True,
            }
        return {**metric, "paper_only": True}

    def summarize(self, metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Return summary of analytics metrics."""
        total = len(metrics)
        complete = sum(1 for m in metrics if m.get("status", "COMPLETE") == "COMPLETE")
        degraded = sum(1 for m in metrics if m.get("status") == "DEGRADED")
        return {
            "total_metrics": total,
            "complete_metrics": complete,
            "degraded_metrics": degraded,
            "failed_metrics": total - complete - degraded,
            "paper_only": True,
        }
