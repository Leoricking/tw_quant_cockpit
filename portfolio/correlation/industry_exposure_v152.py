"""
portfolio/correlation/industry_exposure_v152.py — Industry Exposure Calculator v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from portfolio.correlation.enums_v152 import ExposureType
from portfolio.correlation.models_v152 import ExposureBucket

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


class IndustryExposureCalculator:
    """
    Aggregates portfolio weight by industry classification.
    Unknown industry → "UNKNOWN" bucket (NOT zero, NOT distributed).
    Performs PIT check: available_from <= as_of.
    """

    RESEARCH_ONLY = True

    def calculate(
        self,
        weights: Dict[str, float],
        classifications: Dict[str, Dict[str, Any]],
        as_of: Optional[str] = None,
    ) -> List[ExposureBucket]:
        """
        Args:
            weights: {symbol: weight}
            classifications: {symbol: {industry, effective_from, available_from, source, lineage_ids}}
            as_of: ISO date string for PIT check

        Returns:
            List of ExposureBucket with exposure_type=INDUSTRY
        """
        buckets: Dict[str, ExposureBucket] = {}

        for symbol, weight in weights.items():
            cls = classifications.get(symbol, {})
            industry = cls.get("industry", "UNKNOWN") or "UNKNOWN"
            available_from = cls.get("available_from", "")
            effective_from = cls.get("effective_from", "")
            source = cls.get("source", "")
            lineage_ids = cls.get("lineage_ids", [])

            # PIT check
            pit_status = "VALID"
            if as_of and available_from and available_from > as_of:
                industry = "UNKNOWN"
                pit_status = "PIT_VIOLATION"

            key = industry
            if key not in buckets:
                buckets[key] = ExposureBucket(
                    exposure_type=ExposureType.INDUSTRY,
                    key=key,
                    display_name=key,
                    gross_weight=0.0,
                    source=source,
                    effective_from=effective_from,
                    available_from=available_from,
                    lineage_ids=list(lineage_ids),
                    status=pit_status,
                )

            buckets[key].gross_weight += weight
            if lineage_ids:
                buckets[key].lineage_ids = list(set(buckets[key].lineage_ids) | set(lineage_ids))

        # Compute normalized weight (out of gross weights sum)
        total_gross = sum(b.gross_weight for b in buckets.values())
        for b in buckets.values():
            b.normalized_weight = b.gross_weight / total_gross if total_gross > 0 else 0.0

        return sorted(buckets.values(), key=lambda b: -b.gross_weight)
