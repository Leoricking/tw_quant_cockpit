"""
portfolio/risk_controls/explain_v153.py — Drawdown Risk Controls Explainer v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"

_SAFETY_TEXT = (
    "This is a research-only risk controls analysis. "
    "No automated action has been taken. "
    "Results are descriptive only and do not constitute investment advice. "
    "No orders have been created. No broker has been contacted. "
    "No ledger entry has been written."
)

_LIMITATIONS = [
    "Historical drawdown is not predictive of future drawdown.",
    "Risk controls are advisory only — never auto-executed.",
    "Equity curve is based on demo/fixture data — not real portfolio.",
    "Stress scenarios use simplified shock models.",
    "Attribution uses simplified decomposition — not marginal contribution.",
]


class DrawdownRiskControlsExplainer:
    """Generates human-readable explanations for risk controls evaluations."""

    RESEARCH_ONLY = True

    def explain(
        self,
        evaluation,
        drawdown_summary=None,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Generate explanation dict for an evaluation."""
        context = context or {}

        overall = getattr(evaluation, "overall_status", "UNKNOWN")
        overall_str = overall.value if hasattr(overall, "value") else str(overall)

        breach_count = getattr(evaluation, "breach_count", 0)
        warn_count   = getattr(evaluation, "warn_count", 0)
        pass_count   = getattr(evaluation, "pass_count", 0)

        check_summaries: List[Dict[str, Any]] = []
        for check in getattr(evaluation, "checks", []):
            check_summaries.append({
                "check_id":    check.check_id,
                "type":        check.control_type.value if hasattr(check.control_type, "value") else str(check.control_type),
                "status":      check.status.value if hasattr(check.status, "value") else str(check.status),
                "detail":      check.detail,
                "action":      check.recommended_action.value if hasattr(check.recommended_action, "value") else str(check.recommended_action),
            })

        dd_pct = None
        if drawdown_summary is not None:
            dd_pct = getattr(drawdown_summary, "current_drawdown_pct", None)

        return {
            "research_only":       True,
            "executable":          False,
            "order_created":       False,
            "safety_text":         _SAFETY_TEXT,
            "limitations":         _LIMITATIONS,
            "overall_status":      overall_str,
            "breach_count":        breach_count,
            "warn_count":          warn_count,
            "pass_count":          pass_count,
            "current_drawdown_pct": dd_pct,
            "check_summaries":     check_summaries,
            "labels": [
                "RESEARCH_ONLY",
                "NOT_AN_ORDER",
                "NO_BROKER_CALL",
                "NO_LEDGER_WRITE",
            ],
        }
