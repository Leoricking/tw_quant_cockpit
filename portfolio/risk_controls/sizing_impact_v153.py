"""
portfolio/risk_controls/sizing_impact_v153.py — Position Sizing Risk Impact v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

from portfolio.risk_controls.models_v153 import SizingRiskImpact

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class SizingRiskImpactAnalyzer:
    """Analyzes hypothetical risk impact of a sizing proposal. Research-only."""

    RESEARCH_ONLY = True

    def analyze(
        self,
        proposal_id: str,
        portfolio_id: str,
        symbol: str,
        before_drawdown_pct: float,
        after_drawdown_pct: float,
        before_volatility: float,
        after_volatility: float,
        before_checks: List[str] = None,
        after_checks: List[str] = None,
        risk_budget_consumed_pct: float = 0.0,
        binding_constraint: str = "",
    ) -> SizingRiskImpact:
        """Compute hypothetical risk impact. Never creates orders."""
        before_checks = before_checks or []
        after_checks  = after_checks or []

        breaches_added   = [c for c in after_checks if c not in before_checks]
        breaches_removed = [c for c in before_checks if c not in after_checks]

        return SizingRiskImpact(
            proposal_id=proposal_id,
            portfolio_id=portfolio_id,
            symbol=symbol,
            before_drawdown_pct=before_drawdown_pct,
            after_drawdown_pct=after_drawdown_pct,
            before_volatility=before_volatility,
            after_volatility=after_volatility,
            control_breaches_added=breaches_added,
            control_breaches_removed=breaches_removed,
            risk_budget_consumed_pct=risk_budget_consumed_pct,
            binding_constraint=binding_constraint,
        )

    def build_demo(self, proposal_id: str = "demo_proposal") -> SizingRiskImpact:
        """Build a demo sizing risk impact for fixture/demo use."""
        return self.analyze(
            proposal_id=proposal_id,
            portfolio_id="demo_portfolio",
            symbol="2330",
            before_drawdown_pct=-0.05,
            after_drawdown_pct=-0.07,
            before_volatility=0.18,
            after_volatility=0.20,
            before_checks=[],
            after_checks=[],
            risk_budget_consumed_pct=0.35,
            binding_constraint="VOLATILITY_LIMIT",
        )
