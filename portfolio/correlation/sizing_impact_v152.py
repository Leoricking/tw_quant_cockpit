"""
portfolio/correlation/sizing_impact_v152.py — Sizing Exposure Impact Analyzer v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] HYPOTHETICAL_ONLY. NO_LEDGER_WRITE. NO_ORDER_CREATED. NO_BROKER_CALL. NO_AUTO_APPLY.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from portfolio.correlation.models_v152 import (
    CorrelationCluster,
    ExposureBucket,
    SizingExposureImpact,
)

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"

SIZING_IMPACT_LABELS = [
    "HYPOTHETICAL_ONLY",
    "NO_LEDGER_WRITE",
    "NO_ORDER_CREATED",
    "NO_BROKER_CALL",
    "NO_AUTO_APPLY",
    "RESEARCH_ONLY",
]


class SizingExposureImpactAnalyzer:
    """
    Computes the hypothetical impact of adding a position on portfolio exposure metrics.
    NEVER modifies the proposal quantity.
    ALWAYS: research_only=True, order_created=False, ledger_persisted=False.
    """

    RESEARCH_ONLY   = True
    NO_LEDGER_WRITE = True
    NO_ORDER_CREATED = True
    NO_BROKER_CALL  = True

    def analyze(
        self,
        portfolio_id: str,
        proposal_id: str,
        symbol: str,
        hypothetical_quantity: float,
        entry_price: float,
        portfolio_snapshot: Dict[str, Any],
        before_portfolio_volatility: float,
        after_portfolio_volatility: float,
        before_clusters: List[CorrelationCluster],
        after_clusters: List[CorrelationCluster],
        before_industry_exposure: List[ExposureBucket],
        after_industry_exposure: List[ExposureBucket],
        before_theme_exposure: List[ExposureBucket],
        after_theme_exposure: List[ExposureBucket],
    ) -> SizingExposureImpact:
        """
        Analyse the hypothetical exposure impact of adding `symbol` to the portfolio.
        Does NOT modify the proposal quantity.
        """
        portfolio_value = portfolio_snapshot.get("portfolio_value", 0.0) or 0.0
        hypothetical_value  = hypothetical_quantity * entry_price
        hypothetical_weight = hypothetical_value / portfolio_value if portfolio_value > 0 else 0.0

        before_snapshot_id = portfolio_snapshot.get("snapshot_id", "")

        # Volatility delta
        vol_delta = after_portfolio_volatility - before_portfolio_volatility

        # Cluster weight for this symbol — before and after
        def _cluster_weight_for_symbol(clusters: List[CorrelationCluster], sym: str) -> float:
            for c in clusters:
                if sym in c.symbols:
                    return c.portfolio_weight
            return 0.0

        before_cw = _cluster_weight_for_symbol(before_clusters, symbol)
        after_cw  = _cluster_weight_for_symbol(after_clusters, symbol)
        cw_delta  = after_cw - before_cw

        # Industry exposure dicts
        def _exposure_dict(buckets: List[ExposureBucket]) -> Dict[str, float]:
            return {b.key: b.gross_weight for b in buckets}

        before_ind = _exposure_dict(before_industry_exposure)
        after_ind  = _exposure_dict(after_industry_exposure)
        before_thm = _exposure_dict(before_theme_exposure)
        after_thm  = _exposure_dict(after_theme_exposure)

        # Binding constraint (largest industry exposure delta)
        binding = ""
        max_delta = 0.0
        for key in after_ind:
            delta = after_ind[key] - before_ind.get(key, 0.0)
            if abs(delta) > max_delta:
                max_delta = abs(delta)
                binding = f"INDUSTRY:{key}"

        return SizingExposureImpact(
            proposal_id=proposal_id,
            portfolio_id=portfolio_id,
            symbol=symbol,
            before_snapshot_id=before_snapshot_id,
            hypothetical_weight=hypothetical_weight,
            before_portfolio_volatility=before_portfolio_volatility,
            after_portfolio_volatility=after_portfolio_volatility,
            volatility_delta=vol_delta,
            before_cluster_weight=before_cw,
            after_cluster_weight=after_cw,
            cluster_weight_delta=cw_delta,
            before_industry_exposure=before_ind,
            after_industry_exposure=after_ind,
            before_theme_exposure=before_thm,
            after_theme_exposure=after_thm,
            binding_exposure_constraint=binding,
            status="VALID",
            research_only=True,
            order_created=False,
            ledger_persisted=False,
            metadata={"labels": SIZING_IMPACT_LABELS},
        )
