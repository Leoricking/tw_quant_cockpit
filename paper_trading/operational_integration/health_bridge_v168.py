"""
paper_trading/operational_integration/health_bridge_v168.py
Health Bridge for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class HealthBridge:
    """Aggregates component health and identifies severity. Research only."""

    def aggregate_component_health(self, health_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate health results from multiple components."""
        total = len(health_results)
        if total == 0:
            return {
                "aggregate_status": "UNKNOWN",
                "total": 0,
                "passed": 0,
                "failed": 0,
                "degraded": 0,
                "paper_only": True,
            }
        passed = sum(1 for r in health_results if r.get("status") in ("PASS", "COMPLETE"))
        failed = sum(1 for r in health_results if r.get("status") == "FAIL")
        degraded = sum(1 for r in health_results if r.get("status") == "DEGRADED")

        if failed > 0:
            agg_status = "FAIL"
        elif degraded > 0:
            agg_status = "DEGRADED"
        elif passed == total:
            agg_status = "PASS"
        else:
            agg_status = "DEGRADED"

        avg_score = sum(r.get("health_score", 1.0) for r in health_results) / total

        return {
            "aggregate_status": agg_status,
            "total": total,
            "passed": passed,
            "failed": failed,
            "degraded": degraded,
            "average_health_score": avg_score,
            "paper_only": True,
        }

    def check_failure_severity(self, health_result: Dict[str, Any]) -> str:
        """Return severity string for a health result."""
        status = health_result.get("status", "UNKNOWN")
        failed_checks = [c for c in health_result.get("checks", []) if c.get("status") == "FAIL"]
        if status == "FAIL" and len(failed_checks) >= 5:
            return "CRITICAL"
        elif status == "FAIL":
            return "HIGH"
        elif status == "DEGRADED":
            return "MEDIUM"
        elif status == "PASS":
            return "INFO"
        return "UNKNOWN"

    def check_degraded_status(self, health_result: Dict[str, Any]) -> Dict[str, Any]:
        """Check and return detailed degraded status info."""
        status = health_result.get("status", "UNKNOWN")
        is_degraded = status == "DEGRADED"
        degraded_reasons = health_result.get("degraded_reasons", [])
        return {
            "is_degraded": is_degraded,
            "status": status,
            "degraded_reasons": degraded_reasons,
            "can_operate": status not in ("FAIL", "CRITICAL"),
            "paper_only": True,
        }

    def summarize(self, health_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Return full summary of health check results."""
        agg = self.aggregate_component_health(health_results)
        severities = [self.check_failure_severity(r) for r in health_results]
        critical_count = sum(1 for s in severities if s == "CRITICAL")
        return {
            **agg,
            "critical_count": critical_count,
            "severity_distribution": {
                s: sum(1 for x in severities if x == s)
                for s in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "UNKNOWN"]
            },
            "paper_only": True,
        }
