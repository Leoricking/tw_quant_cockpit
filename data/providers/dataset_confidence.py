"""
data/providers/dataset_confidence.py - Dataset confidence scorer (v0.3.24).

Computes a 0-100 confidence score per dataset based on:
  provider reliability, freshness, coverage, schema, source priority,
  row count, missing symbols, mock contamination.

[!] Read Only. No Real Orders.
"""

from __future__ import annotations

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Confidence levels
_LEVELS = [
    (90, "HIGH"),
    (75, "GOOD"),
    (60, "PARTIAL"),
    (40, "WEAK"),
    (0,  "LOW"),
]

# Known intraday / placeholder datasets
_INTRADAY_DATASETS = {"intraday", "tick", "bidask"}

# Source priority scores (higher = better)
_SOURCE_PRIORITY = {
    "finmind":                1.0,
    "twse":                   0.9,
    "tpex":                   0.85,
    "mops":                   0.85,
    "csv":                    0.7,
    "xq_export":              0.65,
    "planned_tick_provider":  0.0,
    "planned_bidask_provider":0.0,
}

# Dataset-specific caps (applied BEFORE formula)
_DATASET_CAPS: Dict[str, dict] = {
    "tick":   {"score_max": 30, "reason": "planned provider only"},
    "bidask": {"score_max": 30, "reason": "planned provider only"},
}


class DatasetConfidenceScorer:
    """
    Compute dataset-level confidence score.

    Parameters
    ----------
    freshness_data  : dict from DataFreshnessChecker.run_all()["datasets"]
    provider_metrics: dict from ProviderMetricsCollector.collect()
    health_data     : dict {pname: health_record}
    mode            : 'real' or 'mock'
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        freshness_data:   Optional[dict] = None,
        provider_metrics: Optional[dict] = None,
        health_data:      Optional[dict] = None,
        mode:             str = "real",
    ):
        self._freshness  = freshness_data  or {}
        self._metrics    = provider_metrics or {}
        self._health     = health_data     or {}
        self.mode        = mode

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def score_all(self) -> Dict[str, dict]:
        """Score all known datasets."""
        from data.providers.reliability_matrix import _DATASET_FALLBACK_CHAINS
        results = {}
        for dataset in _DATASET_FALLBACK_CHAINS:
            results[dataset] = self.score_dataset(dataset)
        return results

    def score_dataset(self, dataset_name: str) -> dict:
        """Compute confidence score for a single dataset."""
        # Hard cap for planned-only datasets
        cap = _DATASET_CAPS.get(dataset_name)
        if cap:
            return {
                "dataset":      dataset_name,
                "score":        cap["score_max"],
                "level":        self._classify(cap["score_max"]),
                "cap_applied":  True,
                "cap_reason":   cap["reason"],
                "components":   {},
            }

        freshness = self._freshness.get(dataset_name) or self._freshness.get(
            dataset_name.replace("daily_price", "daily_k"), {}
        )
        freshness_status = freshness.get("status", "UNKNOWN") if freshness else "UNKNOWN"
        coverage_ratio   = freshness.get("coverage_ratio", 0.0) if freshness else 0.0
        missing_symbols  = freshness.get("missing_symbols", []) if freshness else []
        rows             = freshness.get("rows", 0) if freshness else 0

        # Check mock contamination (real mode only)
        mock_contaminated = self._check_mock_contamination(dataset_name)
        if mock_contaminated and self.mode == "real":
            return {
                "dataset":      dataset_name,
                "score":        40,
                "level":        self._classify(40),
                "cap_applied":  True,
                "cap_reason":   "mock contamination in real mode (max 40)",
                "components":   {},
            }

        # --- Component scores ---
        provider_rel   = self._provider_reliability_score(dataset_name)
        freshness_sc   = self._freshness_score(freshness_status)
        coverage_sc    = self._coverage_score(coverage_ratio)
        schema_sc      = self._schema_score(dataset_name, freshness)
        source_prio_sc = self._source_priority_score(dataset_name)
        mock_clean_sc  = 1.0 if not mock_contaminated else 0.0

        # Formula
        raw = (
            0.30 * provider_rel   +
            0.25 * freshness_sc   +
            0.20 * coverage_sc    +
            0.10 * schema_sc      +
            0.10 * source_prio_sc +
            0.05 * mock_clean_sc
        ) * 100

        # Degradation rules
        if freshness_status == "MISSING":
            raw = min(raw, 30)
        elif freshness_status == "OLD":
            raw = min(raw, 75)
        elif freshness_status == "STALE":
            raw = min(raw, 80)

        # Missing required columns (schema partial) — max 60
        if schema_sc < 0.5:
            raw = min(raw, 60)

        # Estimated timing (fundamental) — max 80
        if dataset_name == "fundamental":
            raw = min(raw, 80)

        # No provider and no local fallback — max 30
        from data.providers.reliability_matrix import _DATASET_FALLBACK_CHAINS, _LOCAL_FALLBACK_PROVIDERS
        chain = _DATASET_FALLBACK_CHAINS.get(dataset_name, [])
        has_local = any(p in _LOCAL_FALLBACK_PROVIDERS for p in chain)
        if not chain or (provider_rel == 0 and not has_local):
            raw = min(raw, 30)

        # Token missing but local fallback available — max 80
        if not self._token_configured(dataset_name) and has_local:
            raw = min(raw, 80)

        score = round(max(0.0, min(100.0, raw)), 1)

        return {
            "dataset":      dataset_name,
            "score":        score,
            "level":        self._classify(score),
            "cap_applied":  False,
            "cap_reason":   "",
            "freshness_status": freshness_status,
            "coverage_ratio":   coverage_ratio,
            "missing_symbols_count": len(missing_symbols),
            "components": {
                "provider_reliability": round(provider_rel, 3),
                "freshness":            round(freshness_sc, 3),
                "coverage":             round(coverage_sc, 3),
                "schema_completeness":  round(schema_sc, 3),
                "source_priority":      round(source_prio_sc, 3),
                "mock_clean":           round(mock_clean_sc, 3),
            },
        }

    # ------------------------------------------------------------------
    # Component scorers
    # ------------------------------------------------------------------

    def _provider_reliability_score(self, dataset_name: str) -> float:
        """0-1: mean reliability of providers in fallback chain."""
        from data.providers.reliability_matrix import _DATASET_FALLBACK_CHAINS
        chain = _DATASET_FALLBACK_CHAINS.get(dataset_name, [])
        if not chain:
            return 0.0
        scores = []
        for pname in chain[:3]:  # Consider top 3 only
            pm = self._metrics.get("providers", {}).get(pname, {})
            sr = pm.get("success_rate")
            h  = self._health.get(pname, {})
            if sr is not None:
                scores.append(float(sr))
            elif h.get("status") in ("OK", "PARTIAL"):
                scores.append(0.7)
            elif h.get("status") == "NOT_CONFIGURED":
                scores.append(0.3)
        return sum(scores) / len(scores) if scores else 0.5

    def _freshness_score(self, status: str) -> float:
        return {
            "FRESH":               1.0,
            "STALE":               0.6,
            "OLD":                 0.3,
            "PARTIAL":             0.6,
            "HISTORICAL_INTRADAY": 0.5,
            "TIMING_ESTIMATED":    0.6,
            "MISSING":             0.0,
            "UNKNOWN":             0.4,
        }.get(status, 0.4)

    def _coverage_score(self, coverage_ratio: float) -> float:
        return float(min(1.0, max(0.0, coverage_ratio)))

    def _schema_score(self, dataset_name: str, freshness: dict) -> float:
        if not freshness or freshness.get("rows", 0) == 0:
            return 0.0
        return 0.85  # We don't have full schema introspection here

    def _source_priority_score(self, dataset_name: str) -> float:
        from data.providers.reliability_matrix import _DATASET_FALLBACK_CHAINS
        chain = _DATASET_FALLBACK_CHAINS.get(dataset_name, [])
        primary = chain[0] if chain else ""
        return _SOURCE_PRIORITY.get(primary, 0.5)

    def _check_mock_contamination(self, dataset_name: str) -> bool:
        return False  # No mock contamination detection in v0.3.24

    def _token_configured(self, dataset_name: str) -> bool:
        """Check if primary provider token is configured."""
        from data.providers.reliability_matrix import _DATASET_FALLBACK_CHAINS
        chain = _DATASET_FALLBACK_CHAINS.get(dataset_name, [])
        primary = chain[0] if chain else ""
        h = self._health.get(primary, {})
        return h.get("token_configured", True)  # optimistic if no health data

    @staticmethod
    def _classify(score: float) -> str:
        for threshold, level in _LEVELS:
            if score >= threshold:
                return level
        return "LOW"
