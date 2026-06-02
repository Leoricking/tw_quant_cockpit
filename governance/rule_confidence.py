"""
governance/rule_confidence.py — Rule confidence scorer (v0.3.28).
[!] Research Only. No Real Orders. No Auto Weight Apply. Production Trading: BLOCKED.

Safety invariants:
  read_only = True
  no_real_orders = True
  production_blocked = True
  Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
"""

import os
import logging

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOG = logging.getLogger(__name__)

from governance.rule_metadata import (
    RULE_STATUS_BLOCKED,
    RULE_STATUS_DISABLED,
    RULE_STATUS_DEPRECATED,
    CONFIDENCE_HIGH,
    CONFIDENCE_GOOD,
    CONFIDENCE_PARTIAL,
    CONFIDENCE_WEAK,
    CONFIDENCE_LOW,
    CONFIDENCE_UNKNOWN,
    CONFIDENCE_PLANNED,
)


class RuleConfidenceScorer:
    """
    Scores each rule's confidence level based on validation data and heuristics.

    Safety invariants:
      read_only = True
      no_real_orders = True
      production_blocked = True
      Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(self, registry=None, results_dir: str = "data/backtest_results"):
        self._registry = registry
        self._results_dir = results_dir
        # Resolve to absolute path
        if not os.path.isabs(self._results_dir):
            self._results_dir = os.path.join(_BASE_DIR, self._results_dir)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Score all rules in registry and return summary dict.
        """
        result = {
            "rules_scored": 0,
            "high_confidence": [],
            "good_confidence": [],
            "partial_confidence": [],
            "weak_confidence": [],
            "low_confidence": [],
            "unknown_confidence": [],
            "planned": [],
            "details": {},
            "read_only": True,
        }

        if self._registry is None:
            return result

        try:
            rules = self._registry.list_rules()
        except Exception as exc:
            _LOG.warning("RuleConfidenceScorer.run: failed to list rules: %s", exc)
            return result

        validation_data = self.load_validation_results()

        for rule in rules:
            try:
                score_dict = self.score_rule(rule)
                level = score_dict.get("confidence_level", CONFIDENCE_UNKNOWN)
                rid = rule.rule_id
                result["details"][rid] = score_dict
                result["rules_scored"] += 1

                bucket_map = {
                    CONFIDENCE_HIGH: "high_confidence",
                    CONFIDENCE_GOOD: "good_confidence",
                    CONFIDENCE_PARTIAL: "partial_confidence",
                    CONFIDENCE_WEAK: "weak_confidence",
                    CONFIDENCE_LOW: "low_confidence",
                    CONFIDENCE_UNKNOWN: "unknown_confidence",
                    CONFIDENCE_PLANNED: "planned",
                }
                bucket = bucket_map.get(level, "unknown_confidence")
                result[bucket].append(rid)
            except Exception as exc:
                _LOG.warning(
                    "RuleConfidenceScorer.run: error scoring %s: %s",
                    getattr(rule, "rule_id", "?"),
                    exc,
                )

        # Suppress unused variable warning — validation_data used implicitly via score_rule
        _ = validation_data
        return result

    # ------------------------------------------------------------------
    # Score a single rule
    # ------------------------------------------------------------------

    def score_rule(self, rule_metadata) -> dict:
        """
        Score a single rule.
        Returns: {rule_id, score, confidence_level, factors}
        """
        rid = getattr(rule_metadata, "rule_id", "")
        status = getattr(rule_metadata, "status", "")
        experimental = getattr(rule_metadata, "experimental", False)
        sample_count = int(getattr(rule_metadata, "sample_count", 0))
        confidence_hint = getattr(rule_metadata, "confidence_level", CONFIDENCE_UNKNOWN)

        factors = []

        # Hard overrides
        if confidence_hint == CONFIDENCE_PLANNED:
            return {
                "rule_id": rid,
                "score": 0.0,
                "confidence_level": CONFIDENCE_PLANNED,
                "factors": ["PLANNED — no real data yet"],
            }

        # v0.4.1.1 transcript-only candidate rules: confidence capped at PARTIAL.
        # Rules sourced exclusively from transcript ingestion must not reach HIGH
        # before backtest validation. Long-cycle crash watch rules stay at PLANNED.
        _transcript_only_prefixes = ("RISK.TECHNICAL.TOP_PATTERN", "RISK.RELATIVE_WEAKNESS.",
                                     "RISK.CYCLE.CRASH_WATCH", "RISK.FUNDAMENTAL.",
                                     "RISK.PORTFOLIO.")
        if rid.startswith(_transcript_only_prefixes):
            if rid.startswith("RISK.CYCLE.CRASH_WATCH"):
                return {
                    "rule_id": rid,
                    "score": 0.0,
                    "confidence_level": CONFIDENCE_PLANNED,
                    "factors": [
                        "Long-cycle crash watch: qualitative risk only.",
                        "NOT a short-term validated signal.",
                        "Transcript-only source — confidence capped at PLANNED.",
                    ],
                }
            # Other transcript-candidate risk rules: cap at PARTIAL
            return {
                "rule_id": rid,
                "score": 30.0,
                "confidence_level": CONFIDENCE_PARTIAL,
                "factors": [
                    "Transcript-only source: confidence capped at PARTIAL.",
                    "No backtest validation yet — cannot reach HIGH.",
                    "auto_activated=False.",
                ],
            }

        if status == RULE_STATUS_BLOCKED:
            return {
                "rule_id": rid,
                "score": 0.0,
                "confidence_level": CONFIDENCE_LOW,
                "factors": ["Status is BLOCKED"],
            }

        if status in (RULE_STATUS_DISABLED, RULE_STATUS_DEPRECATED):
            return {
                "rule_id": rid,
                "score": 0.0,
                "confidence_level": CONFIDENCE_LOW,
                "factors": [f"Status is {status}"],
            }

        # Check for validation data
        validation_data = self.load_validation_results()
        if not validation_data:
            factors.append("No validation data available")
            return {
                "rule_id": rid,
                "score": 0.0,
                "confidence_level": CONFIDENCE_UNKNOWN,
                "factors": factors,
            }

        # Base score from performance quality
        perf_score = self.infer_performance_quality(rid)
        score = perf_score
        factors.append(f"Performance quality score: {perf_score:.2f}")

        # Sample count adjustments
        inferred_sample = self.infer_sample_count(rid)
        effective_sample = max(sample_count, inferred_sample)

        if effective_sample < 10:
            factors.append(f"Sample count {effective_sample} < 10 — capped at WEAK")
            level = self.classify_confidence(score, effective_sample)
            level = self._cap_level(level, CONFIDENCE_WEAK)
        elif effective_sample < 20:
            factors.append(f"Sample count {effective_sample} < 20 — capped at PARTIAL")
            level = self.classify_confidence(score, effective_sample)
            level = self._cap_level(level, CONFIDENCE_PARTIAL)
        else:
            level = self.classify_confidence(score, effective_sample)

        # Experimental cap
        if experimental:
            factors.append("Experimental flag — capped at PARTIAL")
            level = self._cap_level(level, CONFIDENCE_PARTIAL)

        return {
            "rule_id": rid,
            "score": round(score, 4),
            "confidence_level": level,
            "factors": factors,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _cap_level(level: str, max_level: str) -> str:
        """Cap confidence level at max_level (lower of the two)."""
        order = [
            CONFIDENCE_PLANNED,
            CONFIDENCE_UNKNOWN,
            CONFIDENCE_LOW,
            CONFIDENCE_WEAK,
            CONFIDENCE_PARTIAL,
            CONFIDENCE_GOOD,
            CONFIDENCE_HIGH,
        ]
        try:
            current_idx = order.index(level)
            max_idx = order.index(max_level)
            return order[min(current_idx, max_idx)]
        except ValueError:
            return level

    def load_validation_results(self) -> dict:
        """
        Scan results_dir for CSV files and return summary dict.
        On any error, returns empty dict.
        """
        try:
            if not os.path.isdir(self._results_dir):
                return {}
            summary = {}
            for fname in os.listdir(self._results_dir):
                if not fname.endswith(".csv"):
                    continue
                fpath = os.path.join(self._results_dir, fname)
                try:
                    rows = []
                    with open(fpath, "r", encoding="utf-8", errors="replace") as fh:
                        for line in fh:
                            rows.append(line.rstrip("\n"))
                    summary[fname] = {"rows": len(rows), "path": fpath}
                except Exception:
                    pass
            return summary
        except Exception:
            return {}

    def infer_sample_count(self, rule_id: str) -> int:
        """
        Attempt to infer sample count from validation data.
        Returns 0 if unavailable.
        """
        try:
            data = self.load_validation_results()
            # Look for a CSV whose name contains a fragment of the rule_id
            fragment = rule_id.replace(".", "_").lower()
            for fname, info in data.items():
                if fragment in fname.lower():
                    row_count = info.get("rows", 0)
                    # Subtract 1 for header row
                    return max(0, row_count - 1)
            # Generic fallback: if any CSVs present, assume some data
            if data:
                return 5  # conservative assumption
            return 0
        except Exception:
            return 0

    def infer_performance_quality(self, rule_id: str) -> float:
        """
        Infer a 0.0–1.0 performance quality score from available data.
        Returns 0.0 if no data available.
        """
        try:
            data = self.load_validation_results()
            if not data:
                return 0.0
            fragment = rule_id.replace(".", "_").lower()
            for fname in data:
                if fragment in fname.lower():
                    # Found specific data — assign moderate score
                    return 0.6
            # Generic CSVs present but no rule-specific match
            return 0.3
        except Exception:
            return 0.0

    def classify_confidence(self, score: float, sample_count: int) -> str:
        """
        Classify confidence level from score (0.0–1.0) and sample_count.
        """
        if sample_count < 10:
            return CONFIDENCE_WEAK
        if sample_count < 20:
            if score >= 0.7:
                return CONFIDENCE_PARTIAL
            return CONFIDENCE_WEAK
        # Sufficient samples
        if score >= 0.85:
            return CONFIDENCE_HIGH
        if score >= 0.70:
            return CONFIDENCE_GOOD
        if score >= 0.50:
            return CONFIDENCE_PARTIAL
        if score >= 0.30:
            return CONFIDENCE_WEAK
        return CONFIDENCE_LOW

    # ------------------------------------------------------------------
    # v0.4.7 Research Review Dashboard integration
    # ------------------------------------------------------------------

    def rules_needing_review(self) -> dict:
        """
        Return a summary of rules needing manual review for the Research Review Dashboard.

        Does NOT auto-change rule status or weights.

        [!] Research Only. No Real Orders. No Auto Weight Apply.
        """
        try:
            result = self.run()
            weak     = result.get("weak_confidence", [])
            low      = result.get("low_confidence",  [])
            unknown  = result.get("unknown_confidence", [])
            exp      = result.get("experimental", result.get("planned_confidence", []))
            needing  = weak + low + unknown
            return {
                "total_rules":          result.get("rules_scored", 0),
                "rules_needing_review": needing,
                "experimental_rules":   exp,
                "weak_count":           len(weak),
                "low_count":            len(low),
                "unknown_count":        len(unknown),
                "read_only":            True,
                "no_real_orders":       True,
                "production_blocked":   True,
            }
        except Exception as exc:
            _LOG.warning("RuleConfidenceScorer.rules_needing_review: %s", exc)
            return {
                "total_rules": 0, "rules_needing_review": [],
                "experimental_rules": [], "weak_count": 0,
                "low_count": 0, "unknown_count": 0, "no_real_orders": True,
            }

    # ------------------------------------------------------------------
    # v0.4.8 Research Assistant / Coach integration
    # ------------------------------------------------------------------

    def coach_rule_review_candidates(self) -> dict:
        """
        Return rule review candidates for the Research Assistant / Coach.

        Does NOT auto-change rule status or weights.

        [!] Coaching Only. Research Only. No Real Orders. No Auto Weight Apply.
        """
        try:
            result = self.run()
            weak    = result.get("weak_confidence", [])
            low     = result.get("low_confidence", [])
            unknown = result.get("unknown_confidence", [])
            planned = result.get("planned", [])
            details = result.get("details", {})

            def _to_dict(rule_ids, conf_label):
                items = []
                for rid in rule_ids:
                    d = details.get(rid, {})
                    items.append({
                        "rule_id":      rid,
                        "confidence":   d.get("confidence_level", conf_label),
                        "sample_count": 0,
                    })
                return items

            low_confidence_rules     = _to_dict(low,     "low")
            weak_rules               = _to_dict(weak,    "weak")
            insufficient_sample_rules = _to_dict(unknown, "unknown")
            transcript_candidates    = _to_dict(planned,  "planned")

            return {
                "low_confidence_rules":      low_confidence_rules,
                "weak_rules":                weak_rules,
                "insufficient_sample_rules": insufficient_sample_rules,
                "transcript_candidates":     transcript_candidates,
                "ml_needs_backtest":         [],
                "total_rules":               result.get("rules_scored", 0),
                "read_only":                 True,
                "no_real_orders":            True,
                "coaching_only":             True,
            }
        except Exception as exc:
            _LOG.warning("RuleConfidenceScorer.coach_rule_review_candidates: %s", exc)
            return {
                "low_confidence_rules": [], "weak_rules": [],
                "insufficient_sample_rules": [], "transcript_candidates": [],
                "ml_needs_backtest": [], "total_rules": 0, "no_real_orders": True,
            }
