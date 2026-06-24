"""
portfolio/risk_controls/risk_budget_v153.py — Portfolio Risk Budget Engine v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class PortfolioRiskBudgetEngine:
    """Tracks and reports on portfolio risk budget consumption. Research-only."""

    RESEARCH_ONLY = True

    def evaluate(
        self,
        portfolio_id: str,
        as_of: str,
        current_drawdown_pct: float,
        annualized_volatility: float,
        drawdown_budget_pct: float = -0.20,
        volatility_budget_pct: float = 0.25,
    ) -> Dict[str, Any]:
        """
        Evaluate risk budget utilization.
        Returns consumption ratios and advisory flags (research-only).
        """
        dd_ratio = (current_drawdown_pct / drawdown_budget_pct
                    if drawdown_budget_pct != 0 else 0.0)
        vol_ratio = (annualized_volatility / volatility_budget_pct
                     if volatility_budget_pct != 0 else 0.0)

        dd_pct_used = min(dd_ratio, 1.0) if dd_ratio >= 0 else dd_ratio
        vol_pct_used = min(vol_ratio, 1.0)

        warnings: List[str] = []
        if dd_ratio > 0.75:
            warnings.append(f"Drawdown budget {dd_ratio:.0%} consumed — review recommended")
        if vol_ratio > 0.90:
            warnings.append(f"Volatility budget {vol_ratio:.0%} consumed — review recommended")

        return {
            "portfolio_id":               portfolio_id,
            "as_of":                      as_of,
            "current_drawdown_pct":       current_drawdown_pct,
            "drawdown_budget_pct":        drawdown_budget_pct,
            "drawdown_budget_consumed":   dd_pct_used,
            "annualized_volatility":      annualized_volatility,
            "volatility_budget_pct":      volatility_budget_pct,
            "volatility_budget_consumed": vol_pct_used,
            "warnings":                   warnings,
            "research_only":              True,
            "executable":                 False,
            "order_created":              False,
        }
