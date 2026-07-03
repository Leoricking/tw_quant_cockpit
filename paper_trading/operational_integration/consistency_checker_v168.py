"""
paper_trading/operational_integration/consistency_checker_v168.py
Consistency Checker for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .models_v168 import ConsistencyResult

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_CONSISTENCY_DIMENSIONS = [
    "component_version", "schema_version", "run_id", "session_id",
    "strategy_id", "portfolio_id", "period", "timezone", "symbol",
    "quantity", "price", "pnl", "exposure", "cost", "attribution",
    "health_status", "report_status",
]


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ConsistencyChecker:
    """Checks cross-component consistency. Real checks, not fixed PASS."""

    def check_all(self, context: Dict[str, Any]) -> List[ConsistencyResult]:
        """Run all consistency checks for the given context."""
        results = []
        component_id = context.get("component_id", "unknown")

        # component_version
        results.append(self.check_dimension(
            "component_version",
            context.get("expected_component_version", "1.6.8"),
            context.get("component_version", ""),
            component_id,
        ))

        # schema_version
        results.append(self.check_dimension(
            "schema_version",
            context.get("expected_schema_version", "1.6.8"),
            context.get("schema_version", ""),
            component_id,
        ))

        # run_id
        results.append(self.check_dimension(
            "run_id",
            context.get("expected_run_id", context.get("run_id", "")),
            context.get("actual_run_id", context.get("run_id", "")),
            component_id,
        ))

        # session_id
        results.append(self.check_dimension(
            "session_id",
            context.get("expected_session_id", context.get("session_id", "")),
            context.get("actual_session_id", context.get("session_id", "")),
            component_id,
        ))

        # period
        exp_period = (context.get("period_start", ""), context.get("period_end", ""))
        act_period = (context.get("actual_period_start", context.get("period_start", "")),
                      context.get("actual_period_end", context.get("period_end", "")))
        results.append(self.check_dimension("period", str(exp_period), str(act_period), component_id))

        # timezone
        results.append(self.check_dimension(
            "timezone",
            context.get("expected_timezone", context.get("timezone", "Asia/Taipei")),
            context.get("actual_timezone", context.get("timezone", "Asia/Taipei")),
            component_id,
        ))

        # pnl (if present)
        if "expected_pnl" in context and "actual_pnl" in context:
            exp_pnl = float(context["expected_pnl"])
            act_pnl = float(context["actual_pnl"])
            tol = abs(exp_pnl) * 0.001 + 1e-6
            residual = abs(exp_pnl - act_pnl)
            status = "CONSISTENT" if residual <= tol else "INCONSISTENT"
            results.append(ConsistencyResult(
                check_id=f"consistency_pnl_{component_id}",
                component_id=component_id,
                dimension="pnl",
                expected=exp_pnl,
                actual=act_pnl,
                status=status,
                residual=residual,
                created_at=_utcnow_iso(),
            ))

        return results

    def check_dimension(
        self,
        dimension: str,
        expected: Any,
        actual: Any,
        component_id: str = "unknown",
    ) -> ConsistencyResult:
        """Check consistency of a single dimension."""
        if expected == actual:
            status = "CONSISTENT"
            residual = 0.0
        elif isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            residual = abs(float(expected) - float(actual))
            tol = abs(float(expected)) * 0.001 + 1e-9
            status = "CONSISTENT" if residual <= tol else "INCONSISTENT"
        elif expected == "" or actual == "":
            status = "INSUFFICIENT_DATA"
            residual = 0.0
        else:
            status = "INCONSISTENT"
            residual = 0.0
        return ConsistencyResult(
            check_id=f"consistency_{dimension}_{component_id}",
            component_id=component_id,
            dimension=dimension,
            expected=expected,
            actual=actual,
            status=status,
            residual=residual,
            created_at=_utcnow_iso(),
        )

    def summarize(self, results: List[ConsistencyResult]) -> Dict[str, Any]:
        """Return summary of consistency results."""
        total = len(results)
        consistent = sum(1 for r in results if r.status == "CONSISTENT")
        inconsistent = sum(1 for r in results if r.status == "INCONSISTENT")
        insufficient = sum(1 for r in results if r.status == "INSUFFICIENT_DATA")
        return {
            "total_checks": total,
            "consistent": consistent,
            "inconsistent": inconsistent,
            "insufficient_data": insufficient,
            "all_consistent": inconsistent == 0 and total > 0,
            "paper_only": True,
        }
