"""
portfolio/correlation/asset_exposure_v152.py — Asset Exposure Calculator v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict, List

from portfolio.correlation.enums_v152 import ExposureType
from portfolio.correlation.models_v152 import ExposureBucket

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"

VALID_ASSET_CLASSES = {"COMMON_STOCK", "ETF", "CASH", "UNKNOWN"}


class AssetExposureCalculator:
    """
    Aggregates portfolio weight by asset class.
    ETF is never treated as COMMON_STOCK.
    """

    RESEARCH_ONLY = True

    def calculate(
        self,
        weights: Dict[str, float],
        asset_types: Dict[str, str],
    ) -> List[ExposureBucket]:
        """
        Args:
            weights: {symbol: weight}
            asset_types: {symbol: asset_class}
                         asset_class in: COMMON_STOCK, ETF, CASH, UNKNOWN

        Returns:
            List of ExposureBucket with exposure_type=ASSET_CLASS.
        """
        buckets: Dict[str, ExposureBucket] = {}

        for symbol, weight in weights.items():
            asset_class = asset_types.get(symbol, "UNKNOWN")
            if asset_class not in VALID_ASSET_CLASSES:
                asset_class = "UNKNOWN"

            # Ensure ETF is never classified as COMMON_STOCK
            # (if caller mislabelled it, keep it as-is; we only prevent UNKNOWN→COMMON_STOCK)

            if asset_class not in buckets:
                buckets[asset_class] = ExposureBucket(
                    exposure_type=ExposureType.ASSET_CLASS,
                    key=asset_class,
                    display_name=asset_class,
                    gross_weight=0.0,
                    status="VALID",
                )

            buckets[asset_class].gross_weight += weight

        total = sum(b.gross_weight for b in buckets.values())
        for b in buckets.values():
            b.normalized_weight = b.gross_weight / total if total > 0 else 0.0

        return sorted(buckets.values(), key=lambda b: -b.gross_weight)
