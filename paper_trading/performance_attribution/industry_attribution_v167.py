"""
paper_trading/performance_attribution/industry_attribution_v167.py
Industry attribution for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .sector_attribution_v167 import SectorAttributionEngine

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class IndustryAttributionEngine(SectorAttributionEngine):
    """
    Industry-level attribution (same Brinson-Fachler as sector, finer granularity).
    Inherits SectorAttributionEngine logic, overrides entity name.
    """

    def compute_industry(
        self,
        industry: str,
        portfolio_weight: float,
        benchmark_weight: float,
        portfolio_return: float,
        benchmark_return: float,
        risk_contribution: float,
        drawdown_contribution: float,
        concentration: float,
        residual: float = 0.0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> Dict[str, Any]:
        """Compute industry attribution."""
        result = self.compute(
            sector=industry,
            portfolio_weight=portfolio_weight,
            benchmark_weight=benchmark_weight,
            portfolio_return=portfolio_return,
            benchmark_return=benchmark_return,
            risk_contribution=risk_contribution,
            drawdown_contribution=drawdown_contribution,
            concentration=concentration,
            residual=residual,
            period_start=period_start,
            period_end=period_end,
            source_lineage=source_lineage,
        )
        result["industry"] = result.pop("sector")
        return result
