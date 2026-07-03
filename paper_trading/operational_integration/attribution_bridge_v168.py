"""
paper_trading/operational_integration/attribution_bridge_v168.py
Attribution Bridge for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class AttributionBridge:
    """Validates attribution run results and linkages. Research only."""

    def check_run_linkage(self, attribution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Check attribution result has valid run linkage."""
        has_run_id = bool(attribution_result.get("run_id"))
        has_session = bool(attribution_result.get("session_id"))
        has_period = bool(attribution_result.get("period_start") and attribution_result.get("period_end"))
        return {
            "has_run_id": has_run_id,
            "has_session_id": has_session,
            "has_period": has_period,
            "valid": has_run_id and has_session and has_period,
            "paper_only": True,
        }

    def check_residual_linkage(self, attribution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Check that residual is linked to total return."""
        total_return = attribution_result.get("total_return", None)
        residual = attribution_result.get("residual", None)
        explained = attribution_result.get("explained_return", None)
        if total_return is None or residual is None:
            return {
                "has_residual": False,
                "valid": False,
                "paper_only": True,
            }
        computed_residual = total_return - (explained or 0)
        tolerance = abs(total_return) * 0.001 + 1e-8
        consistent = abs(residual - computed_residual) <= tolerance
        return {
            "has_residual": True,
            "residual": residual,
            "computed_residual": computed_residual,
            "consistent": consistent,
            "valid": consistent,
            "paper_only": True,
        }

    def check_benchmark_linkage(self, attribution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Check benchmark linkage in attribution result."""
        has_benchmark = bool(attribution_result.get("benchmark_return") is not None)
        benchmark_source = attribution_result.get("benchmark_source", "")
        return {
            "has_benchmark": has_benchmark,
            "benchmark_source": benchmark_source,
            "missing_benchmark": not has_benchmark,
            "paper_only": True,
        }

    def check_reconciliation_status(self, attribution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Check reconciliation status of attribution result."""
        recon_status = attribution_result.get("reconciliation_status", "UNKNOWN")
        valid_statuses = {"RECONCILED", "RECONCILED_WITH_ROUNDING", "DEGRADED", "FAILED", "UNKNOWN"}
        return {
            "reconciliation_status": recon_status,
            "valid_status": recon_status in valid_statuses,
            "is_reconciled": recon_status in ("RECONCILED", "RECONCILED_WITH_ROUNDING"),
            "paper_only": True,
        }

    def summarize(self, attribution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Return summary of attribution result."""
        return {
            "run_id": attribution_result.get("run_id", ""),
            "session_id": attribution_result.get("session_id", ""),
            "status": attribution_result.get("status", "UNKNOWN"),
            "reconciliation_status": attribution_result.get("reconciliation_status", "UNKNOWN"),
            "has_benchmark": attribution_result.get("benchmark_return") is not None,
            "paper_only": True,
        }
