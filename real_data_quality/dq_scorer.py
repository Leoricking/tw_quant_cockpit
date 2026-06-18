"""
real_data_quality/dq_scorer.py — Quality Score calculator v1.3.0 (0-100, deterministic)
Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] Score is deterministic: same inputs always produce same score (no random weights).
[!] CRITICAL issue caps score at 49. Score 0 with no data -> UNAVAILABLE.
"""
from __future__ import annotations

import logging
from typing import List

from real_data_quality.dq_schema import (
    DataMode,
    DataQualityIssueSeverity,
    DataQualityIssue,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
MOCK_FALLBACK_ENABLED = False

# ---------------------------------------------------------------------------
# Scoring weights (must sum to 100)
# ---------------------------------------------------------------------------
_WEIGHT_CORE_PRICE_COMPLETENESS   = 25
_WEIGHT_FRESHNESS                 = 20
_WEIGHT_OHLCV_HISTORY             = 15
_WEIGHT_INDICATORS                = 10
_WEIGHT_CHIPS_INSTITUTIONAL       = 10
_WEIGHT_FUNDAMENTALS              = 10
_WEIGHT_SOURCE_TRUSTWORTHINESS    = 5
_WEIGHT_CROSS_SOURCE_CONSISTENCY  = 5

_TOTAL_WEIGHT = (
    _WEIGHT_CORE_PRICE_COMPLETENESS
    + _WEIGHT_FRESHNESS
    + _WEIGHT_OHLCV_HISTORY
    + _WEIGHT_INDICATORS
    + _WEIGHT_CHIPS_INSTITUTIONAL
    + _WEIGHT_FUNDAMENTALS
    + _WEIGHT_SOURCE_TRUSTWORTHINESS
    + _WEIGHT_CROSS_SOURCE_CONSISTENCY
)
assert _TOTAL_WEIGHT == 100, f"Weights must sum to 100, got {_TOTAL_WEIGHT}"

# Critical cap: any CRITICAL issue caps score at 49
_CRITICAL_SCORE_CAP = 49


class DataQualityScorer:
    """
    Deterministic quality score calculator (0-100).
    Separate from validator so it can be tested independently.

    Weights:
      core price completeness : 25
      freshness               : 20
      OHLCV history           : 15
      indicators              : 10
      chips/institutional     : 10
      fundamentals            : 10
      source trustworthiness  : 5
      cross-source consistency: 5

    CRITICAL issue -> score capped at 49.
    Stable, reproducible (no random weights).
    """

    NO_REAL_ORDERS = True
    MOCK_FALLBACK_ENABLED = False

    # Fields required for full core price score
    _CORE_PRICE_FIELDS = ["close", "open", "high", "low", "volume"]

    # Indicator fields we score
    _INDICATOR_FIELDS = [
        "MA5", "MA10", "MA20", "MA60",
        "KD_K", "KD_D", "RSI",
        "MACD_line", "MACD_signal", "MACD_hist",
    ]

    # Chips fields we score
    _CHIPS_FIELDS = [
        "foreign", "investment_trust", "dealer",
        "margin_balance", "major_holders", "retail_holders",
    ]

    # Fundamentals fields we score
    _FUNDAMENTALS_FIELDS = [
        "monthly_revenue", "yoy_revenue_growth",
        "financial_statement_period", "eps", "latest_reporting_period",
    ]

    def compute(self, data: dict, issues: List[DataQualityIssue]) -> int:
        """
        Compute quality score 0-100.
        Deterministic: same data + same issues -> same score.
        Returns int.
        """
        # Sub-scores (each 0.0-1.0), then weighted
        s_price = self._score_core_price(data, issues)
        s_fresh = self._score_freshness(data, issues)
        s_hist  = self._score_ohlcv_history(data, issues)
        s_ind   = self._score_indicators(data, issues)
        s_chips = self._score_chips(data, issues)
        s_fund  = self._score_fundamentals(data, issues)
        s_src   = self._score_source_trust(data, issues)
        s_cross = self._score_cross_source(data, issues)

        raw = (
            s_price * _WEIGHT_CORE_PRICE_COMPLETENESS
            + s_fresh * _WEIGHT_FRESHNESS
            + s_hist  * _WEIGHT_OHLCV_HISTORY
            + s_ind   * _WEIGHT_INDICATORS
            + s_chips * _WEIGHT_CHIPS_INSTITUTIONAL
            + s_fund  * _WEIGHT_FUNDAMENTALS
            + s_src   * _WEIGHT_SOURCE_TRUSTWORTHINESS
            + s_cross * _WEIGHT_CROSS_SOURCE_CONSISTENCY
        )

        score = int(round(raw))
        score = max(0, min(100, score))

        # Apply CRITICAL cap
        has_critical = any(
            iss.severity == DataQualityIssueSeverity.CRITICAL
            for iss in issues
        )
        if has_critical:
            score = min(score, _CRITICAL_SCORE_CAP)

        return score

    # ------------------------------------------------------------------
    # Sub-score methods (each returns float 0.0-1.0)
    # ------------------------------------------------------------------

    def _score_core_price(self, data: dict, issues: List[DataQualityIssue]) -> float:
        """Core price completeness sub-score."""
        present = sum(
            1 for f in self._CORE_PRICE_FIELDS
            if _field_present(data, f)
        )
        base = present / len(self._CORE_PRICE_FIELDS)

        # Penalty for invalid fields from issues
        invalid_penalty = sum(
            0.2 for iss in issues
            if iss.field in self._CORE_PRICE_FIELDS
            and iss.severity in (DataQualityIssueSeverity.ERROR, DataQualityIssueSeverity.CRITICAL)
        )
        return max(0.0, base - invalid_penalty)

    def _score_freshness(self, data: dict, issues: List[DataQualityIssue]) -> float:
        """Freshness sub-score based on stale issues."""
        stale_issues = [
            iss for iss in issues
            if "stale" in iss.code.lower() or "fresh" in iss.code.lower()
        ]
        if not stale_issues:
            # No stale issues -> check if we have a timestamp at all
            if data.get("date") or data.get("latest_market_timestamp"):
                return 1.0
            return 0.5  # No timestamp -> partial

        # Each stale issue penalizes
        penalty = 0.0
        for iss in stale_issues:
            if iss.severity == DataQualityIssueSeverity.CRITICAL:
                penalty += 0.5
            elif iss.severity == DataQualityIssueSeverity.ERROR:
                penalty += 0.35
            elif iss.severity == DataQualityIssueSeverity.WARNING:
                penalty += 0.2
            else:
                penalty += 0.05
        return max(0.0, 1.0 - penalty)

    def _score_ohlcv_history(self, data: dict, issues: List[DataQualityIssue]) -> float:
        """OHLCV history sub-score."""
        # If OHLCV fields present, start with 0.8; history depth issues reduce it
        base = 0.8 if all(_field_present(data, f) for f in ["open", "high", "low", "close", "volume"]) else 0.3

        history_issues = [
            iss for iss in issues
            if "history" in iss.code.lower() or "insufficient" in iss.code.lower()
        ]
        penalty = sum(0.2 for _ in history_issues)
        return max(0.0, min(1.0, base - penalty))

    def _score_indicators(self, data: dict, issues: List[DataQualityIssue]) -> float:
        """Technical indicators sub-score."""
        present = sum(
            1 for f in self._INDICATOR_FIELDS
            if _field_present(data, f)
        )
        base = present / len(self._INDICATOR_FIELDS) if self._INDICATOR_FIELDS else 0.0

        # NaN/invalid indicators reduce score
        indicator_issues = [
            iss for iss in issues
            if iss.field in self._INDICATOR_FIELDS
        ]
        penalty = sum(
            0.15 if iss.severity in (DataQualityIssueSeverity.ERROR, DataQualityIssueSeverity.CRITICAL)
            else 0.05
            for iss in indicator_issues
        )
        return max(0.0, min(1.0, base - penalty))

    def _score_chips(self, data: dict, issues: List[DataQualityIssue]) -> float:
        """Chips / institutional data sub-score."""
        present = sum(
            1 for f in self._CHIPS_FIELDS
            if _field_present(data, f)
        )
        base = present / len(self._CHIPS_FIELDS) if self._CHIPS_FIELDS else 0.0

        chips_issues = [
            iss for iss in issues
            if iss.field in self._CHIPS_FIELDS
        ]
        penalty = sum(0.1 for _ in chips_issues)
        return max(0.0, min(1.0, base - penalty))

    def _score_fundamentals(self, data: dict, issues: List[DataQualityIssue]) -> float:
        """Fundamentals sub-score."""
        present = sum(
            1 for f in self._FUNDAMENTALS_FIELDS
            if _field_present(data, f)
        )
        base = present / len(self._FUNDAMENTALS_FIELDS) if self._FUNDAMENTALS_FIELDS else 0.0

        fund_issues = [
            iss for iss in issues
            if iss.field in self._FUNDAMENTALS_FIELDS
        ]
        penalty = sum(0.1 for _ in fund_issues)
        return max(0.0, min(1.0, base - penalty))

    def _score_source_trust(self, data: dict, issues: List[DataQualityIssue]) -> float:
        """Source trustworthiness / traceability sub-score."""
        source = data.get("source", [])
        if isinstance(source, str):
            source = [source]

        _MOCK_SOURCES = {"mock", "demo", "fixture", "sample", "synthetic", "unknown", "test"}
        data_mode = data.get("data_mode", DataMode.UNAVAILABLE)

        if not source:
            return 0.3  # Unknown source — partial

        # Real mode with mock source -> trust = 0
        if data_mode == DataMode.REAL:
            if any(s.lower() in _MOCK_SOURCES for s in source):
                return 0.0

        source_issues = [
            iss for iss in issues
            if "source" in iss.code.lower() or iss.field == "source"
        ]
        penalty = sum(0.2 for _ in source_issues)
        return max(0.0, 1.0 - penalty)

    def _score_cross_source(self, data: dict, issues: List[DataQualityIssue]) -> float:
        """Cross-source consistency sub-score."""
        cross_issues = [
            iss for iss in issues
            if "cross" in iss.code.lower() or "inconsist" in iss.code.lower() or "conflict" in iss.code.lower()
        ]
        if not cross_issues:
            return 1.0

        penalty = sum(
            0.5 if iss.severity == DataQualityIssueSeverity.CRITICAL else 0.25
            for iss in cross_issues
        )
        return max(0.0, 1.0 - penalty)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _field_present(data: dict, field: str) -> bool:
    """Return True if field is in data and not None/empty/NaN."""
    import math
    val = data.get(field)
    if val is None:
        return False
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return False
    return True
