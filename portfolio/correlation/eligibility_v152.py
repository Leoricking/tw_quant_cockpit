"""
portfolio/correlation/eligibility_v152.py — Correlation Exposure Eligibility Gate v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

from portfolio.correlation.models_v152 import CorrelationAnalysisRequest

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


class CorrelationExposureEligibilityGate:
    """
    Evaluates whether all analyses in a correlation & exposure run can proceed.

    Checks:
    - research_only = True
    - broker_linked = False (from portfolio snapshot)
    - len(symbols) >= 2
    - observations >= minimum
    - PIT: available_from <= as_of
    - no blocking conflict
    """

    RESEARCH_ONLY = True

    def evaluate(
        self,
        request: CorrelationAnalysisRequest,
        portfolio_snapshot: Dict[str, Any],
        price_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Returns dict with per-analysis allow flags, blockers, warnings, evidence.
        """
        blockers: List[str] = []
        warnings: List[str] = []
        evidence: Dict[str, Any] = {}

        # 1. research_only must be True
        if not getattr(request, "research_only", False):
            blockers.append("RESEARCH_ONLY_FALSE")

        # 2. broker_linked must be False
        broker_linked = portfolio_snapshot.get("broker_linked", False)
        if broker_linked:
            blockers.append("BROKER_LINKED_TRUE")
            evidence["broker_linked"] = broker_linked

        # 3. symbols >= 2
        symbols = getattr(request, "symbols", [])
        if len(symbols) < 2:
            blockers.append(f"INSUFFICIENT_SYMBOLS: {len(symbols)} < 2")

        # 4. Estimate available observations
        min_obs = getattr(request, "minimum_observations", 60)
        # Count dates in price_data
        max_dates = 0
        for sym in symbols:
            sym_prices = price_data.get(sym, {})
            as_of = getattr(request, "as_of", "")
            valid_dates = [d for d in sym_prices if d <= as_of] if as_of else list(sym_prices.keys())
            max_dates = max(max_dates, len(valid_dates))

        obs_ok = max_dates >= min_obs + 1  # +1 because returns need n+1 prices
        if not obs_ok:
            warnings.append(f"OBSERVATION_COUNT_LOW: ~{max_dates} dates available, need {min_obs + 1}")

        # 5. PIT: available_from <= as_of
        as_of = getattr(request, "as_of", "")
        available_from = getattr(request, "available_from", "")
        if as_of and available_from and available_from > as_of:
            blockers.append(f"PIT_VIOLATION: available_from={available_from} > as_of={as_of}")

        # Determine per-analysis eligibility
        hard_blocked = len(blockers) > 0

        def _allow(extra_cond: bool = True) -> bool:
            return not hard_blocked and extra_cond

        result = {
            "correlation_allowed":         _allow(obs_ok),
            "covariance_allowed":          _allow(obs_ok),
            "risk_contribution_allowed":   _allow(obs_ok),
            "beta_allowed":                _allow(
                                               obs_ok and
                                               getattr(request, "benchmark_symbol", None) is not None
                                           ),
            "clustering_allowed":          _allow(obs_ok),
            "exposure_allowed":            _allow(),
            "ETF_overlap_allowed":         _allow(),
            "sizing_impact_allowed":       _allow(),
            "blocked_analyses":            [],
            "warnings":                    warnings,
            "blockers":                    blockers,
            "evidence":                    evidence,
            "eligibility_status":          "BLOCKED" if hard_blocked else ("PARTIAL" if warnings else "ELIGIBLE"),
        }

        if hard_blocked:
            for key in ["correlation_allowed", "covariance_allowed", "risk_contribution_allowed",
                        "beta_allowed", "clustering_allowed", "exposure_allowed",
                        "ETF_overlap_allowed", "sizing_impact_allowed"]:
                result[key] = False
            result["blocked_analyses"] = list(blockers)

        return result
