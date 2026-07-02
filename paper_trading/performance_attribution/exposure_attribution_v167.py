"""
paper_trading/performance_attribution/exposure_attribution_v167.py
Exposure attribution for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionLevel, AttributionStatus, ConfidenceLevel
from .models_v167 import ExposureContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den != 0.0 else default


class ExposureAttributionEngine:
    """Exposure attribution: beta, gross/net, concentration, leverage, sectors."""

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        positions: List[Dict[str, Any]],
        portfolio_value: float,
        beta_map: Optional[Dict[str, float]] = None,
        sector_map: Optional[Dict[str, str]] = None,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> ExposureContribution:
        """Compute exposure attribution from position list."""
        if not positions or portfolio_value <= 0:
            return ExposureContribution(
                entity_id=entity_id,
                level=level,
                market_exposure=0.0,
                beta_exposure=0.0,
                gross_exposure=0.0,
                net_exposure=0.0,
                long_exposure=0.0,
                short_exposure=0.0,
                concentration=0.0,
                leverage=0.0,
                confidence=ConfidenceLevel.UNKNOWN,
                status=AttributionStatus.INSUFFICIENT_DATA,
                source_lineage=source_lineage,
                period_start=period_start,
                period_end=period_end,
                paper_only=True,
                research_only=True,
                no_real_orders=True,
                not_for_production=True,
            )

        betas = beta_map or {}
        sectors = sector_map or {}

        long_val = sum(
            p.get("market_value", 0.0)
            for p in positions
            if p.get("direction", "LONG") in ("LONG", 1)
        )
        short_val = sum(
            abs(p.get("market_value", 0.0))
            for p in positions
            if p.get("direction", "LONG") in ("SHORT", -1)
        )
        gross_exp = (long_val + short_val) / portfolio_value
        net_exp = (long_val - short_val) / portfolio_value
        market_exp = gross_exp

        # Beta-weighted exposure
        beta_exp = 0.0
        for p in positions:
            sym = p.get("symbol", "")
            mv = p.get("market_value", 0.0)
            beta = betas.get(sym, 1.0)
            direction_sign = 1 if p.get("direction", "LONG") in ("LONG", 1) else -1
            beta_exp += beta * mv * direction_sign / portfolio_value

        # Concentration: largest single position as pct
        weights = [
            abs(p.get("market_value", 0.0)) / portfolio_value
            for p in positions if portfolio_value > 0
        ]
        concentration = max(weights) if weights else 0.0
        leverage = gross_exp

        # Sector exposures
        sector_exp: Dict[str, float] = {}
        for p in positions:
            sym = p.get("symbol", "")
            sector = sectors.get(sym, "UNKNOWN")
            mv = p.get("market_value", 0.0)
            weight = mv / portfolio_value
            sector_exp[sector] = sector_exp.get(sector, 0.0) + weight

        confidence = ConfidenceLevel.HIGH if len(positions) >= 2 else ConfidenceLevel.MEDIUM

        return ExposureContribution(
            entity_id=entity_id,
            level=level,
            market_exposure=market_exp,
            beta_exposure=beta_exp,
            gross_exposure=gross_exp,
            net_exposure=net_exp,
            long_exposure=long_val / portfolio_value,
            short_exposure=short_val / portfolio_value,
            concentration=concentration,
            leverage=leverage,
            sector_exposures=sector_exp,
            confidence=confidence,
            status=AttributionStatus.COMPLETE,
            source_lineage=source_lineage,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )
