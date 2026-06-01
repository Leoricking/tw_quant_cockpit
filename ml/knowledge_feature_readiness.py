"""
ml/knowledge_feature_readiness.py — KnowledgeFeatureReadinessChecker (v0.4.2.1).

Checks readiness status for transcript-derived knowledge features.

Readiness levels:
  READY              — backtest validated, no leakage, can be in model schema
  PARTIAL            — partially mapped, some validation needed
  METADATA_ONLY      — regime/cycle metadata only, not usable as label
  NEEDS_MAPPING      — factor candidate, needs column mapping to actual data
  NEEDS_BACKTEST     — rule candidate, needs empirical backtest validation
  BLOCKED            — blocked due to leakage or missing confirmation
  LEAKAGE_RISK       — high leakage risk — requires review
  INSUFFICIENT_DATA  — not enough data to evaluate

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Readiness constants
READINESS_READY             = "READY"
READINESS_PARTIAL           = "PARTIAL"
READINESS_METADATA_ONLY     = "METADATA_ONLY"
READINESS_NEEDS_MAPPING     = "NEEDS_MAPPING"
READINESS_NEEDS_BACKTEST    = "NEEDS_BACKTEST"
READINESS_BLOCKED           = "BLOCKED"
READINESS_LEAKAGE_RISK      = "LEAKAGE_RISK"
READINESS_INSUFFICIENT_DATA = "INSUFFICIENT_DATA"

_READINESS_PRIORITY = {
    READINESS_READY:             100,
    READINESS_PARTIAL:           70,
    READINESS_METADATA_ONLY:     50,
    READINESS_NEEDS_MAPPING:     40,
    READINESS_NEEDS_BACKTEST:    30,
    READINESS_INSUFFICIENT_DATA: 20,
    READINESS_LEAKAGE_RISK:      10,
    READINESS_BLOCKED:           0,
}


class KnowledgeFeatureReadinessChecker:
    """
    Checks and assigns readiness to transcript-derived feature metadata.

    Rules:
      - transcript_knowledge factor_candidate  → NEEDS_MAPPING (default) or PARTIAL
      - rule_candidate                          → NEEDS_BACKTEST
      - avoid_condition (pattern-based)         → NEEDS_BACKTEST; else PARTIAL
      - risk_condition (long_cycle)             → METADATA_ONLY
      - risk_condition (non-cycle)              → PARTIAL
      - Any feature with leakage_note=LONG_CYCLE_RISK → METADATA_ONLY
      - Any feature with leakage_note containing POST_EVENT → NEEDS_BACKTEST or BLOCKED

    [!] ML Research Only. No Real Orders.
    """

    read_only: bool = True
    no_real_orders: bool = True

    def __init__(self):
        self._results: List[dict] = []

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def check_features(self, features: List[dict]) -> List[dict]:
        """
        Evaluate readiness for each feature. Returns list of readiness result dicts.
        Does NOT modify the input list.
        """
        self._results = []
        for feat in features:
            result = self._evaluate_one(feat)
            self._results.append(result)
        return self._results

    def check_one(self, feat: dict) -> dict:
        return self._evaluate_one(feat)

    # ------------------------------------------------------------------
    # Evaluation logic
    # ------------------------------------------------------------------

    def _evaluate_one(self, feat: dict) -> dict:
        feature_id     = feat.get("feature_id", "")
        feature_source = feat.get("feature_source", "")
        source_cat     = feat.get("source_category", "")
        leakage_note   = feat.get("leakage_note", "")
        timeframe      = feat.get("timeframe", "")
        feature_type   = feat.get("feature_type", "")
        confidence     = feat.get("confidence", "PARTIAL")
        existing_ready = feat.get("readiness", "")

        reasons: List[str] = []
        readiness = READINESS_NEEDS_MAPPING

        # 1. Long-cycle / regime — always METADATA_ONLY
        if (timeframe == "cycle"
                or "LONG_CYCLE" in leakage_note.upper()
                or feature_type in ("regime_flag",)):
            readiness = READINESS_METADATA_ONLY
            reasons.append("Long-cycle / regime metadata: not usable as short-term label")
            return self._result(feature_id, readiness, reasons, feat)

        # 2. Leakage-blocked
        if "PATTERN_INCOMPLETE" in leakage_note.upper():
            readiness = READINESS_BLOCKED
            reasons.append("Pattern-based condition: pattern_confirmed_date required before use")
            return self._result(feature_id, readiness, reasons, feat)

        # 3. Rule candidates → NEEDS_BACKTEST
        if source_cat == "rule_candidate" or feature_source == "rule_candidate":
            readiness = READINESS_NEEDS_BACKTEST
            reasons.append("Rule candidate: requires empirical backtest validation before use")
            return self._result(feature_id, readiness, reasons, feat)

        # 4. Avoid conditions
        if source_cat == "avoid_condition" or feature_source == "avoid_condition":
            if "POST_EVENT" in leakage_note.upper() or "TIMING_ESTIMATED" in leakage_note.upper():
                readiness = READINESS_LEAKAGE_RISK
                reasons.append("Avoid condition has leakage note: " + leakage_note)
            else:
                readiness = READINESS_PARTIAL
                reasons.append("Avoid condition: partially validated; needs backtest confirmation")
            return self._result(feature_id, readiness, reasons, feat)

        # 5. Risk conditions (non-long-cycle)
        if source_cat == "risk_condition" or feature_source == "risk_condition":
            readiness = READINESS_PARTIAL
            reasons.append("Risk condition: partially mapped; confidence capped at PARTIAL")
            return self._result(feature_id, readiness, reasons, feat)

        # 6. Factor candidates
        if source_cat == "factor_candidate" or feature_source == "transcript_knowledge":
            if "TIMING_ESTIMATED" in leakage_note.upper():
                readiness = READINESS_LEAKAGE_RISK
                reasons.append("Fundamental factor: announcement_date_is_estimated=True — timing leakage risk")
            elif confidence in ("LOW", "UNKNOWN", "PLANNED"):
                readiness = READINESS_INSUFFICIENT_DATA
                reasons.append("Factor candidate: confidence too low for current use")
            else:
                readiness = READINESS_NEEDS_MAPPING
                reasons.append("Factor candidate: needs column mapping to actual data source")
            return self._result(feature_id, readiness, reasons, feat)

        # 7. Default — respect existing readiness if present
        if existing_ready in _READINESS_PRIORITY:
            readiness = existing_ready
            reasons.append(f"Using existing readiness from metadata: {readiness}")
        else:
            readiness = READINESS_NEEDS_MAPPING
            reasons.append("Unknown source: defaulting to NEEDS_MAPPING")

        return self._result(feature_id, readiness, reasons, feat)

    @staticmethod
    def _result(feature_id: str, readiness: str, reasons: List[str], feat: dict) -> dict:
        return {
            "feature_id":              feature_id,
            "readiness":               readiness,
            "readiness_score":         _READINESS_PRIORITY.get(readiness, 0),
            "reasons":                 reasons,
            "auto_enabled":            False,  # always
            "not_for_short_term_label": feat.get("not_for_short_term_label", False),
            "leakage_note":            feat.get("leakage_note", ""),
            "confidence":              feat.get("confidence", "PARTIAL"),
        }

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def build_summary(self, results: Optional[List[dict]] = None) -> dict:
        r = results if results is not None else self._results
        by_readiness: Dict[str, int] = {}
        for item in r:
            rd = item.get("readiness", "UNKNOWN")
            by_readiness[rd] = by_readiness.get(rd, 0) + 1

        return {
            "total_checked":           len(r),
            "auto_enabled_count":      0,
            "by_readiness":            by_readiness,
            "metadata_only_count":     by_readiness.get(READINESS_METADATA_ONLY, 0),
            "needs_backtest_count":    by_readiness.get(READINESS_NEEDS_BACKTEST, 0),
            "needs_mapping_count":     by_readiness.get(READINESS_NEEDS_MAPPING, 0),
            "partial_count":           by_readiness.get(READINESS_PARTIAL, 0),
            "leakage_risk_count":      by_readiness.get(READINESS_LEAKAGE_RISK, 0),
            "blocked_count":           by_readiness.get(READINESS_BLOCKED, 0),
            "model_ready_count":       by_readiness.get(READINESS_READY, 0),
        }
