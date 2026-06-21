"""
portfolio/concentration_v150.py — Concentration analysis for v1.5.0.

HHI (Herfindahl-Hirschman Index), effective number of positions,
concentration warnings. All weights as Decimal fractions (0-1).

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from decimal import Decimal
from typing import List, Dict, Optional, Any
from .enums_v150 import ConcentrationLevel

RESEARCH_ONLY = True

# Thresholds
LARGEST_POSITION_WARN_THRESHOLD = Decimal("0.30")   # >30%
TOP3_CONCENTRATION_WARN_THRESHOLD = Decimal("0.70")  # >70%
HHI_WARN_THRESHOLD = Decimal("0.25")                 # >0.25


class PortfolioConcentrationAnalyzer:
    RESEARCH_ONLY = True

    def analyze(
        self,
        position_weights: Dict[str, Decimal],  # symbol -> weight (0-1 Decimal)
    ) -> Dict[str, Any]:
        """
        Compute concentration metrics.

        Returns dict with:
          hhi, effective_n_positions, largest_position_weight,
          largest_position_symbol, top3_weight, concentration_level,
          warnings (list[str])
        """
        if not position_weights:
            return {
                "hhi": Decimal("0"),
                "effective_n_positions": 0,
                "largest_position_weight": Decimal("0"),
                "largest_position_symbol": None,
                "top3_weight": Decimal("0"),
                "concentration_level": ConcentrationLevel.NORMAL,
                "warnings": [],
                "research_only": True,
            }

        weights = {k: Decimal(str(v)) for k, v in position_weights.items()}
        sorted_items = sorted(weights.items(), key=lambda x: x[1], reverse=True)

        hhi = sum(w * w for w in weights.values())
        effective_n = (Decimal("1") / hhi) if hhi > 0 else Decimal("0")

        largest_symbol = sorted_items[0][0]
        largest_weight = sorted_items[0][1]
        top3_weight = sum(w for _, w in sorted_items[:3])

        warnings: list[str] = []
        level = ConcentrationLevel.NORMAL

        if largest_weight > LARGEST_POSITION_WARN_THRESHOLD:
            warnings.append(
                f"Largest position {largest_symbol} = {largest_weight:.2%} exceeds 30% threshold"
            )
            level = ConcentrationLevel.HIGH_CONCENTRATION

        if top3_weight > TOP3_CONCENTRATION_WARN_THRESHOLD:
            top3_syms = [s for s, _ in sorted_items[:3]]
            warnings.append(
                f"Top-3 positions ({', '.join(top3_syms)}) = {top3_weight:.2%} exceeds 70% threshold"
            )
            if level == ConcentrationLevel.NORMAL:
                level = ConcentrationLevel.HIGH_TOP3_CONCENTRATION

        if hhi > HHI_WARN_THRESHOLD:
            warnings.append(f"HHI = {hhi:.4f} exceeds 0.25 threshold")
            level = ConcentrationLevel.HIGH_HHI

        return {
            "hhi": hhi,
            "effective_n_positions": float(effective_n),
            "largest_position_weight": largest_weight,
            "largest_position_symbol": largest_symbol,
            "top3_weight": top3_weight,
            "concentration_level": level,
            "warnings": warnings,
            "research_only": True,
        }
