"""
portfolio/correlation/etf_overlap_v152.py — ETF Overlap Analyzer v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from portfolio.correlation.models_v152 import ETFOverlapResult

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


class ETFOverlapAnalyzer:
    """
    Identifies direct + indirect exposure from ETF holdings in a portfolio.

    Missing holdings: NOT assumed zero overlap → status="UNKNOWN".
    Stale holdings (available_from > as_of): status="STALE".
    """

    RESEARCH_ONLY = True

    def analyze(
        self,
        portfolio_weights: Dict[str, float],
        etf_holdings: Dict[str, Dict[str, float]],
        holdings_as_of: Dict[str, str],
        holdings_available_from: Dict[str, str],
        as_of: str,
    ) -> List[ETFOverlapResult]:
        """
        Args:
            portfolio_weights: {symbol: weight}
            etf_holdings: {etf_symbol: {constituent_symbol: constituent_weight}}
                          constituent_weight is the ETF's internal weight (should sum ~1.0)
            holdings_as_of: {etf_symbol: date_str}
            holdings_available_from: {etf_symbol: date_str}
            as_of: reference date

        Returns:
            List of ETFOverlapResult, one per ETF present in portfolio_weights.
        """
        results: List[ETFOverlapResult] = []
        non_etf_symbols = set(portfolio_weights.keys())

        for etf_symbol, etf_weight in portfolio_weights.items():
            # Only process if we have holdings data for this symbol
            if etf_symbol not in etf_holdings:
                # Missing holdings — cannot assume zero
                results.append(ETFOverlapResult(
                    etf_symbol=etf_symbol,
                    portfolio_symbols=list(non_etf_symbols - {etf_symbol}),
                    direct_weight=etf_weight,
                    status="UNKNOWN",
                    metadata={"reason": "NO_HOLDINGS_DATA"},
                ))
                continue

            constituents = etf_holdings[etf_symbol]
            h_as_of = holdings_as_of.get(etf_symbol, "")
            h_avail = holdings_available_from.get(etf_symbol, "")

            # Stale check
            if h_avail and h_avail > as_of:
                results.append(ETFOverlapResult(
                    etf_symbol=etf_symbol,
                    holdings_as_of=h_as_of,
                    holdings_available_from=h_avail,
                    direct_weight=etf_weight,
                    status="STALE",
                    metadata={"reason": f"STALE_HOLDINGS: available_from={h_avail} > as_of={as_of}"},
                ))
                continue

            # Validate holdings sum ≈ 1.0
            holdings_sum = sum(constituents.values())
            holdings_ok = abs(holdings_sum - 1.0) <= 0.02

            # Find overlapping constituents (symbols also held directly in portfolio)
            other_portfolio_syms = {s for s in portfolio_weights if s != etf_symbol}
            overlapping = [s for s in constituents if s in other_portfolio_syms]

            # indirect_weight: ETF weight × sum of constituent weights for overlapping symbols
            indirect_weight = etf_weight * sum(constituents.get(s, 0.0) for s in overlapping)
            direct_weight = etf_weight
            combined = direct_weight + indirect_weight

            metadata: Dict[str, Any] = {}
            if not holdings_ok:
                metadata["warning"] = f"ETF_HOLDINGS_SUM={holdings_sum:.4f} (expected ~1.0)"

            results.append(ETFOverlapResult(
                etf_symbol=etf_symbol,
                portfolio_symbols=sorted(other_portfolio_syms),
                overlapping_constituents=sorted(overlapping),
                direct_weight=direct_weight,
                indirect_weight=indirect_weight,
                combined_effective_exposure=combined,
                holdings_as_of=h_as_of,
                holdings_available_from=h_avail,
                status="VALID",
                metadata=metadata,
            ))

        return results
