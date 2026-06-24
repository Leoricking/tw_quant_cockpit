"""
portfolio/risk_controls/eligibility_v153.py — Drawdown Risk Controls Eligibility Gate v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class DrawdownRiskControlsEligibilityGate:
    """Eligibility gate for drawdown & risk controls analysis."""

    RESEARCH_ONLY = True

    def evaluate(
        self,
        request,
        portfolio_context: Dict[str, Any] = None,
        equity_curve_points: int = 0,
    ) -> Dict[str, Any]:
        """
        Evaluate eligibility for drawdown & risk controls analysis.
        Returns eligibility status dict.
        """
        portfolio_context = portfolio_context or {}
        blockers: List[str] = []
        warnings: List[str] = []

        # Safety guard: never allow broker-linked auto-apply
        if portfolio_context.get("broker_linked", False):
            blockers.append("BROKER_LINKED_TRUE — risk controls are research-only")

        if portfolio_context.get("auto_apply_enabled", False):
            blockers.append("AUTO_APPLY_ENABLED — permanently blocked")

        # Minimum equity curve requirement
        min_points = getattr(request, "lookback_days", 60)
        if equity_curve_points < min_points:
            warnings.append(
                f"Equity curve has {equity_curve_points} points, "
                f"fewer than minimum {min_points} — statistics may be unreliable"
            )

        research_only = getattr(request, "research_only", False)
        if not research_only:
            blockers.append("research_only must be True")

        eligible = len(blockers) == 0

        return {
            "eligibility_status": "ELIGIBLE" if eligible else "INELIGIBLE",
            "risk_controls_allowed": eligible,
            "drawdown_analysis_allowed": eligible,
            "blockers": blockers,
            "warnings": warnings,
            "research_only": True,
        }
