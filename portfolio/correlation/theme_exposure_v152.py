"""
portfolio/correlation/theme_exposure_v152.py — Theme Exposure Calculator v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Overlapping themes: total can exceed 100%. OVERLAPPING_EXPOSURE, NOT_MUTUALLY_EXCLUSIVE.
"""
from __future__ import annotations

from typing import Any, Dict, List

from portfolio.correlation.enums_v152 import ExposureType
from portfolio.correlation.models_v152 import ExposureBucket

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


class ThemeExposureCalculator:
    """
    Aggregates portfolio weight by theme.
    Themes are NOT mutually exclusive — total exposure can exceed 100%.
    Forum-sourced themes: status="SUPPLEMENTARY_ONLY".
    """

    RESEARCH_ONLY = True

    def calculate(
        self,
        weights: Dict[str, float],
        theme_data: Dict[str, List[Dict[str, Any]]],
    ) -> List[ExposureBucket]:
        """
        Args:
            weights: {symbol: weight}
            theme_data: {symbol: [{theme, weight_in_theme, effective_from,
                                   available_from, source}]}

        Returns:
            List of ExposureBucket with exposure_type=THEME.
            Labels OVERLAPPING_EXPOSURE and NOT_MUTUALLY_EXCLUSIVE in metadata.
        """
        buckets: Dict[str, ExposureBucket] = {}

        for symbol, weight in weights.items():
            themes = theme_data.get(symbol, [])
            for entry in themes:
                theme_key = entry.get("theme", "UNKNOWN") or "UNKNOWN"
                theme_weight = float(entry.get("weight_in_theme", 1.0))
                source = entry.get("source", "")
                effective_from = entry.get("effective_from", "")
                available_from = entry.get("available_from", "")

                # Contribution = portfolio_weight × theme_participation_weight
                contribution = weight * theme_weight

                is_forum = "forum" in source.lower() if source else False
                status = "SUPPLEMENTARY_ONLY" if is_forum else "VALID"

                if theme_key not in buckets:
                    buckets[theme_key] = ExposureBucket(
                        exposure_type=ExposureType.THEME,
                        key=theme_key,
                        display_name=theme_key,
                        gross_weight=0.0,
                        overlapping_weight=0.0,
                        source=source,
                        effective_from=effective_from,
                        available_from=available_from,
                        status=status,
                        metadata={
                            "labels": ["OVERLAPPING_EXPOSURE", "NOT_MUTUALLY_EXCLUSIVE"],
                        },
                    )

                buckets[theme_key].gross_weight += contribution
                buckets[theme_key].overlapping_weight += contribution

        # Normalized weight: themes can exceed 1.0 total — flag this
        total = sum(b.gross_weight for b in buckets.values())
        for b in buckets.values():
            b.normalized_weight = b.gross_weight / total if total > 0 else 0.0
            if total > 1.0:
                b.metadata["note"] = "TOTAL_THEME_EXPOSURE_EXCEEDS_100_PCT"

        return sorted(buckets.values(), key=lambda b: -b.gross_weight)
