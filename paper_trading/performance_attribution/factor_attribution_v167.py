"""
paper_trading/performance_attribution/factor_attribution_v167.py
Factor attribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Factor data insufficient → UNAVAILABLE. No auto-fit real alpha claim. proxy confidence != HIGH.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import (
    AttributionLevel, AttributionStatus, ConfidenceLevel,
)
from .models_v167 import FactorContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

# Supported research-only factors
SUPPORTED_FACTORS = [
    "market", "size", "value", "momentum", "volatility",
    "liquidity", "quality", "industry", "sector", "residual_alpha",
]


class FactorAttributionEngine:
    """
    Factor attribution (research-only).
    Returns UNAVAILABLE/INSUFFICIENT_DATA when factor exposure not available.
    Proxy must be marked with proxy_method; proxy confidence != HIGH.
    """

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        factor_name: str,
        factor_exposure: Optional[float],
        factor_return: Optional[float],
        is_proxy: bool = True,
        proxy_method: str = "",
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> FactorContribution:
        """Compute factor contribution for one factor."""
        if factor_name not in SUPPORTED_FACTORS:
            return FactorContribution(
                entity_id=entity_id,
                level=level,
                factor_name=factor_name,
                factor_exposure=0.0,
                factor_return=0.0,
                factor_contribution=0.0,
                is_proxy=True,
                proxy_method="UNSUPPORTED_FACTOR",
                unavailable=True,
                confidence=ConfidenceLevel.UNKNOWN,
                status=AttributionStatus.UNSUPPORTED,
                source_lineage=source_lineage,
                period_start=period_start,
                period_end=period_end,
                paper_only=True,
                research_only=True,
                no_real_orders=True,
                not_for_production=True,
            )

        if factor_exposure is None or factor_return is None:
            return FactorContribution(
                entity_id=entity_id,
                level=level,
                factor_name=factor_name,
                factor_exposure=0.0,
                factor_return=0.0,
                factor_contribution=0.0,
                is_proxy=True,
                proxy_method=proxy_method or "UNAVAILABLE",
                unavailable=True,
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

        contribution = factor_exposure * factor_return

        # Proxy confidence must NOT be HIGH
        if is_proxy:
            confidence = ConfidenceLevel.LOW if not proxy_method else ConfidenceLevel.MEDIUM
        else:
            confidence = ConfidenceLevel.HIGH

        # Residual alpha = factor_return - explained by exposure
        residual_alpha = factor_return - contribution if not is_proxy else 0.0

        return FactorContribution(
            entity_id=entity_id,
            level=level,
            factor_name=factor_name,
            factor_exposure=factor_exposure,
            factor_return=factor_return,
            factor_contribution=contribution,
            is_proxy=is_proxy,
            proxy_method=proxy_method,
            unavailable=False,
            residual_alpha=residual_alpha,
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

    def compute_all_factors(
        self,
        entity_id: str,
        level: AttributionLevel,
        factor_exposures: Dict[str, Optional[float]],
        factor_returns: Dict[str, Optional[float]],
        is_proxy: bool = True,
        proxy_method: str = "",
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> List[FactorContribution]:
        """Compute factor attribution for all supported factors."""
        results = []
        for factor_name in SUPPORTED_FACTORS:
            exposure = factor_exposures.get(factor_name)
            ret = factor_returns.get(factor_name)
            results.append(self.compute(
                entity_id=entity_id,
                level=level,
                factor_name=factor_name,
                factor_exposure=exposure,
                factor_return=ret,
                is_proxy=is_proxy,
                proxy_method=proxy_method,
                period_start=period_start,
                period_end=period_end,
                source_lineage=source_lineage,
            ))
        return results
