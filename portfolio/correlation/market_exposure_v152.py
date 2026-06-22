"""
portfolio/correlation/market_exposure_v152.py — Market Exposure Calculator v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict, List

from portfolio.correlation.enums_v152 import ExposureType
from portfolio.correlation.models_v152 import ExposureBucket

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"

VALID_MARKET_TYPES = {"LISTED", "OTC", "ETF", "CASH", "UNKNOWN"}


class MarketExposureCalculator:
    """
    Aggregates portfolio weight by market segment.
    No duplicate counting between markets — each symbol contributes to exactly one bucket.
    """

    RESEARCH_ONLY = True

    def calculate(
        self,
        weights: Dict[str, float],
        market_data: Dict[str, str],
    ) -> List[ExposureBucket]:
        """
        Args:
            weights: {symbol: weight}
            market_data: {symbol: market_type}
                         market_type in: LISTED, OTC, ETF, CASH, UNKNOWN

        Returns:
            List of ExposureBucket with exposure_type=MARKET.
            No symbol appears in more than one bucket.
        """
        buckets: Dict[str, ExposureBucket] = {}
        seen_symbols: set = set()

        for symbol, weight in weights.items():
            if symbol in seen_symbols:
                continue  # prevent duplicate counting
            seen_symbols.add(symbol)

            market = market_data.get(symbol, "UNKNOWN")
            if market not in VALID_MARKET_TYPES:
                market = "UNKNOWN"

            if market not in buckets:
                buckets[market] = ExposureBucket(
                    exposure_type=ExposureType.MARKET,
                    key=market,
                    display_name=market,
                    gross_weight=0.0,
                    status="VALID",
                )

            buckets[market].gross_weight += weight

        total = sum(b.gross_weight for b in buckets.values())
        for b in buckets.values():
            b.normalized_weight = b.gross_weight / total if total > 0 else 0.0

        return sorted(buckets.values(), key=lambda b: -b.gross_weight)
