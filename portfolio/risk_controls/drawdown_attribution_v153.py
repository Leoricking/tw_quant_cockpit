"""
portfolio/risk_controls/drawdown_attribution_v153.py — Drawdown Attribution v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from portfolio.risk_controls.enums_v153 import AttributionType
from portfolio.risk_controls.models_v153 import DrawdownAttribution

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class DrawdownAttributionCalculator:
    """Attributes drawdown across positions, industries, themes, clusters."""

    RESEARCH_ONLY = True

    def attribute_by_position(
        self,
        weights: Dict[str, float],
        pnl_by_symbol: Dict[str, float],
        total_portfolio_value: float,
    ) -> List[DrawdownAttribution]:
        """Attribute drawdown contribution to each symbol position."""
        results: List[DrawdownAttribution] = []
        if total_portfolio_value <= 0:
            return results

        for symbol, weight in weights.items():
            pnl = pnl_by_symbol.get(symbol, 0.0)
            dd_contrib = pnl / total_portfolio_value if total_portfolio_value else 0.0
            results.append(DrawdownAttribution(
                attribution_id=f"ATTR_POS_{symbol}_{uuid.uuid4().hex[:4]}",
                attribution_type=AttributionType.POSITION,
                key=symbol,
                drawdown_contribution_pct=dd_contrib,
                weight=weight,
                pnl_contribution=pnl,
            ))

        # Sort by drawdown contribution ascending (worst first)
        results.sort(key=lambda a: a.drawdown_contribution_pct)
        return results

    def attribute_by_industry(
        self,
        industry_map: Dict[str, str],
        weights: Dict[str, float],
        pnl_by_symbol: Dict[str, float],
        total_portfolio_value: float,
    ) -> List[DrawdownAttribution]:
        """Attribute drawdown by industry."""
        industry_pnl: Dict[str, float] = {}
        industry_weight: Dict[str, float] = {}

        for symbol, weight in weights.items():
            industry = industry_map.get(symbol, "UNKNOWN")
            industry_pnl[industry] = industry_pnl.get(industry, 0.0) + pnl_by_symbol.get(symbol, 0.0)
            industry_weight[industry] = industry_weight.get(industry, 0.0) + weight

        results: List[DrawdownAttribution] = []
        for industry, pnl in industry_pnl.items():
            dd_contrib = pnl / total_portfolio_value if total_portfolio_value else 0.0
            results.append(DrawdownAttribution(
                attribution_id=f"ATTR_IND_{industry}_{uuid.uuid4().hex[:4]}",
                attribution_type=AttributionType.INDUSTRY,
                key=industry,
                drawdown_contribution_pct=dd_contrib,
                weight=industry_weight.get(industry, 0.0),
                pnl_contribution=pnl,
            ))

        results.sort(key=lambda a: a.drawdown_contribution_pct)
        return results

    def attribute_by_theme(
        self,
        theme_map: Dict[str, List[str]],
        weights: Dict[str, float],
        pnl_by_symbol: Dict[str, float],
        total_portfolio_value: float,
    ) -> List[DrawdownAttribution]:
        """Attribute drawdown by theme."""
        theme_pnl: Dict[str, float] = {}
        theme_weight: Dict[str, float] = {}

        for symbol, weight in weights.items():
            for theme in theme_map.get(symbol, ["UNKNOWN"]):
                theme_pnl[theme] = theme_pnl.get(theme, 0.0) + pnl_by_symbol.get(symbol, 0.0)
                theme_weight[theme] = theme_weight.get(theme, 0.0) + weight

        results: List[DrawdownAttribution] = []
        for theme, pnl in theme_pnl.items():
            dd_contrib = pnl / total_portfolio_value if total_portfolio_value else 0.0
            results.append(DrawdownAttribution(
                attribution_id=f"ATTR_THM_{theme}_{uuid.uuid4().hex[:4]}",
                attribution_type=AttributionType.THEME,
                key=theme,
                drawdown_contribution_pct=dd_contrib,
                weight=theme_weight.get(theme, 0.0),
                pnl_contribution=pnl,
            ))

        results.sort(key=lambda a: a.drawdown_contribution_pct)
        return results

    def attribute_by_cluster(
        self,
        cluster_map: Dict[str, List[str]],
        weights: Dict[str, float],
        pnl_by_symbol: Dict[str, float],
        total_portfolio_value: float,
    ) -> List[DrawdownAttribution]:
        """Attribute drawdown by correlation cluster."""
        cluster_pnl: Dict[str, float] = {}
        cluster_weight: Dict[str, float] = {}

        for cluster_id, symbols in cluster_map.items():
            for symbol in symbols:
                cluster_pnl[cluster_id] = cluster_pnl.get(cluster_id, 0.0) + pnl_by_symbol.get(symbol, 0.0)
                cluster_weight[cluster_id] = cluster_weight.get(cluster_id, 0.0) + weights.get(symbol, 0.0)

        results: List[DrawdownAttribution] = []
        for cluster_id, pnl in cluster_pnl.items():
            dd_contrib = pnl / total_portfolio_value if total_portfolio_value else 0.0
            results.append(DrawdownAttribution(
                attribution_id=f"ATTR_CLU_{cluster_id}_{uuid.uuid4().hex[:4]}",
                attribution_type=AttributionType.CLUSTER,
                key=cluster_id,
                drawdown_contribution_pct=dd_contrib,
                weight=cluster_weight.get(cluster_id, 0.0),
                pnl_contribution=pnl,
            ))

        results.sort(key=lambda a: a.drawdown_contribution_pct)
        return results
