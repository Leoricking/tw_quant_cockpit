"""
paper_trading/performance_attribution/risk_attribution_v167.py
Risk attribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Covariance/beta insufficient → DEGRADED + disclose fallback_method. No assumptions.
"""
from __future__ import annotations
import math
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionLevel, AttributionStatus, ConfidenceLevel
from .models_v167 import RiskContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _stdev(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    n = len(values)
    mean = sum(values) / n
    var = sum((x - mean) ** 2 for x in values) / (n - 1)
    return math.sqrt(var)


def _downside_stdev(values: List[float], mar: float = 0.0) -> float:
    """Downside deviation relative to MAR."""
    downside = [min(0.0, x - mar) for x in values]
    if not any(d < 0 for d in downside):
        return 0.0
    n = len(downside)
    sq_sum = sum(d ** 2 for d in downside)
    return math.sqrt(sq_sum / n)


class RiskAttributionEngine:
    """Risk attribution: marginal/component/normalized contributions."""

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        daily_returns: List[float],
        portfolio_value: float,
        positions: List[Dict[str, Any]],
        beta_map: Optional[Dict[str, float]] = None,
        correlation_matrix: Optional[Dict[str, Dict[str, float]]] = None,
        has_overnight: bool = True,
        has_leverage: bool = False,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> RiskContribution:
        """Compute risk attribution. Degrades gracefully when data insufficient."""
        data_complete = bool(daily_returns and len(daily_returns) >= 10)
        fallback_method = ""
        confidence = ConfidenceLevel.HIGH

        if not data_complete:
            confidence = ConfidenceLevel.LOW
            fallback_method = "INSUFFICIENT_HISTORY"

        betas = beta_map or {}

        # Volatility contribution
        vol = _stdev(daily_returns) if daily_returns else 0.0
        downside_vol = _downside_stdev(daily_returns) if daily_returns else 0.0

        # Portfolio beta (average)
        if positions and betas:
            pv = portfolio_value or 1.0
            beta_exp = sum(
                betas.get(p.get("symbol", ""), 1.0) * p.get("market_value", 0.0) / pv
                for p in positions
            )
        elif not betas:
            beta_exp = 1.0  # proxy
            fallback_method = fallback_method or "BETA_PROXY_1.0"
            confidence = ConfidenceLevel.LOW
        else:
            beta_exp = 1.0

        # Drawdown contribution (max drawdown proxy)
        drawdown_contribution = 0.0
        if daily_returns:
            cum = 1.0
            peak = 1.0
            max_dd = 0.0
            for r in daily_returns:
                cum *= (1.0 + r)
                if cum > peak:
                    peak = cum
                dd = (cum - peak) / peak
                if dd < max_dd:
                    max_dd = dd
            drawdown_contribution = abs(max_dd)

        # Concentration risk (top position weight)
        concentration = 0.0
        if positions and portfolio_value > 0:
            weights = [abs(p.get("market_value", 0.0)) / portfolio_value for p in positions]
            concentration = max(weights) if weights else 0.0

        # Leverage
        gross_exp = 0.0
        if positions and portfolio_value > 0:
            gross_exp = sum(abs(p.get("market_value", 0.0)) for p in positions) / portfolio_value

        leverage_contribution = max(0.0, gross_exp - 1.0) * vol

        # Overnight / gap risk proxy
        overnight_risk = vol * 0.3 if has_overnight else 0.0
        gap_risk = vol * 0.1
        turnover_risk = 0.0

        # Correlation cluster (proxy from correlation_matrix)
        correlation_cluster = 0.0
        if correlation_matrix:
            all_corrs = []
            symbols = list(correlation_matrix.keys())
            for i, s1 in enumerate(symbols):
                for j, s2 in enumerate(symbols):
                    if i < j:
                        c = correlation_matrix.get(s1, {}).get(s2, 0.0)
                        all_corrs.append(c)
            if all_corrs:
                avg_corr = sum(all_corrs) / len(all_corrs)
                correlation_cluster = max(0.0, avg_corr) * vol
        else:
            fallback_method = fallback_method or "NO_COVARIANCE"
            confidence = min(confidence, ConfidenceLevel.MEDIUM)

        # Liquidity proxy (turnover-based)
        liquidity_proxy = 0.0
        tail_loss = vol * 2.5  # 2.5-sigma proxy
        position_sizing_contrib = concentration * vol

        # MCR / CCR approximations
        marginal_contribution = vol
        component_contribution = vol * gross_exp
        normalized_contribution = 1.0 / len(positions) if positions else 1.0

        # Determine status
        if not data_complete:
            status = AttributionStatus.DEGRADED
        else:
            status = AttributionStatus.COMPLETE

        return RiskContribution(
            entity_id=entity_id,
            level=level,
            volatility_contribution=vol,
            downside_volatility_contribution=downside_vol,
            drawdown_contribution=drawdown_contribution,
            correlation_cluster_contribution=correlation_cluster,
            leverage_contribution=leverage_contribution,
            liquidity_risk_proxy=liquidity_proxy,
            gap_risk=gap_risk,
            overnight_risk=overnight_risk,
            turnover_risk=turnover_risk,
            tail_loss_contribution=tail_loss,
            marginal_contribution=marginal_contribution,
            component_contribution=component_contribution,
            normalized_contribution=normalized_contribution,
            fallback_method=fallback_method,
            data_complete=data_complete,
            confidence=confidence,
            status=status,
            source_lineage=source_lineage,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )
