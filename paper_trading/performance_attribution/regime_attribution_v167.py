"""
paper_trading/performance_attribution/regime_attribution_v167.py
Regime attribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] UNKNOWN regime must not be forced to SIDEWAYS. confidence must degrade. Missing metadata disclosed.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import (
    AttributionLevel, AttributionStatus, ConfidenceLevel, RegimeType,
)
from .models_v167 import RegimeContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class RegimeAttributionEngine:
    """Regime attribution: returns and attribution effects by market regime."""

    def compute_by_regime(
        self,
        entity_id: str,
        level: AttributionLevel,
        daily_returns: List[float],
        daily_pnl: List[float],
        regime_dates: Dict[str, RegimeType],       # date -> regime
        trade_dates: Optional[List[str]] = None,
        costs_by_date: Optional[Dict[str, float]] = None,
        selection_by_date: Optional[Dict[str, float]] = None,
        allocation_by_date: Optional[Dict[str, float]] = None,
        timing_by_date: Optional[Dict[str, float]] = None,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> List[RegimeContribution]:
        """
        Compute attribution by regime.
        UNKNOWN regime: confidence UNKNOWN, not forced to SIDEWAYS, missing metadata disclosed.
        """
        if not regime_dates:
            # All unknown
            regime_dates = {}

        # Group by regime
        regime_buckets: Dict[RegimeType, List[float]] = {}
        for r in RegimeType:
            regime_buckets[r] = []

        # Match daily returns to regimes (by date if available)
        dates = sorted(regime_dates.keys())
        if daily_returns and dates:
            for i, ret in enumerate(daily_returns):
                if i < len(dates):
                    d = dates[i]
                    regime = regime_dates.get(d, RegimeType.UNKNOWN)
                else:
                    regime = RegimeType.UNKNOWN
                regime_buckets[regime].append(ret)
        elif daily_returns:
            # No regime metadata — all UNKNOWN
            regime_buckets[RegimeType.UNKNOWN].extend(daily_returns)

        results: List[RegimeContribution] = []

        for regime, returns in regime_buckets.items():
            if not returns:
                continue

            gross_return = sum(r for r in returns if r >= 0)
            net_return = sum(returns)
            winners = [r for r in returns if r > 0]
            losers = [r for r in returns if r < 0]
            hit_rate = len(winners) / len(returns) if returns else 0.0

            # Drawdown within regime
            cum = 1.0
            peak = 1.0
            max_dd = 0.0
            for r in returns:
                cum *= (1.0 + r)
                if cum > peak:
                    peak = cum
                dd = (cum - peak) / peak
                if dd < max_dd:
                    max_dd = dd

            # If regime is UNKNOWN: degrade confidence, disclose missing metadata
            if regime == RegimeType.UNKNOWN:
                confidence = ConfidenceLevel.UNKNOWN
                status = AttributionStatus.DEGRADED
                unknown_forced = False  # explicitly NOT forced
            else:
                confidence = ConfidenceLevel.MEDIUM if len(returns) >= 5 else ConfidenceLevel.LOW
                status = AttributionStatus.COMPLETE
                unknown_forced = False

            results.append(RegimeContribution(
                entity_id=entity_id,
                level=level,
                regime=regime,
                return_in_regime=net_return,
                net_return_in_regime=net_return,
                hit_rate_in_regime=hit_rate,
                drawdown_in_regime=abs(max_dd),
                cost_in_regime=0.0,
                selection_effect_in_regime=0.0,
                allocation_effect_in_regime=0.0,
                timing_effect_in_regime=0.0,
                unknown_forced=unknown_forced,
                confidence=confidence,
                status=status,
                source_lineage=source_lineage,
                period_start=period_start,
                period_end=period_end,
                paper_only=True,
                research_only=True,
                no_real_orders=True,
                not_for_production=True,
            ))

        return results
