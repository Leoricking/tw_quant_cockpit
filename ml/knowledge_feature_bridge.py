"""
ml/knowledge_feature_bridge.py — KnowledgeFeatureBridge (v0.4.2.1).

Converts transcript-derived knowledge (factor_candidates, rule_candidates,
avoid_conditions, risk_conditions) from v0.4.1.1 StrategyKnowledgeStore
into ML feature metadata dicts suitable for KnowledgeFeatureCatalog.

Mapping rules:
  factor_candidates  → feature_source=transcript_knowledge, readiness=NEEDS_MAPPING or PARTIAL
  rule_candidates    → feature_source=rule_candidate,       readiness=NEEDS_BACKTEST, auto_enabled=False
  avoid_conditions   → feature_source=avoid_condition,      feature_type=avoid_flag,  readiness=PARTIAL or NEEDS_BACKTEST
  risk_conditions    → feature_source=risk_condition,       feature_type=risk_flag,   readiness=PARTIAL or METADATA_ONLY
  long_cycle_risk    → feature_type=regime_flag,            timeframe=cycle,          readiness=METADATA_ONLY, not_for_short_term_label=True

Safety invariants:
  auto_enabled = False (always)
  confidence   ≤ PARTIAL (transcript-only cap)
  long_cycle_risk → METADATA_ONLY, not_for_short_term_label=True

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Knowledge Only.
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Feature source tags
SOURCE_TRANSCRIPT = "transcript_knowledge"
SOURCE_RULE_CANDIDATE = "rule_candidate"
SOURCE_AVOID_CONDITION = "avoid_condition"
SOURCE_RISK_CONDITION = "risk_condition"

# Readiness values (mirror KnowledgeFeatureReadinessChecker)
READINESS_READY             = "READY"
READINESS_PARTIAL           = "PARTIAL"
READINESS_METADATA_ONLY     = "METADATA_ONLY"
READINESS_NEEDS_MAPPING     = "NEEDS_MAPPING"
READINESS_NEEDS_BACKTEST    = "NEEDS_BACKTEST"
READINESS_BLOCKED           = "BLOCKED"
READINESS_LEAKAGE_RISK      = "LEAKAGE_RISK"
READINESS_INSUFFICIENT_DATA = "INSUFFICIENT_DATA"

# Long-cycle risk keywords (from v0.4.1.1 rule governance)
_LONG_CYCLE_KEYWORDS = [
    "long_cycle", "crash_watch", "crash", "cycle.crash",
    "market_cycle", "long cycle", "stock_crash", "bubble",
    "systemic_risk", "regime",
]

# Fundamental / financial data keywords → POST_EVENT_KNOWLEDGE risk
_FUNDAMENTAL_KEYWORDS = [
    "eps", "revenue", "gross_margin", "operating_margin",
    "pe_ratio", "earnings", "financial", "fundamental",
    "profit", "income", "quarter", "annual", "yoy", "mom",
]


def _is_long_cycle(name: str, description: str = "") -> bool:
    text = (name + " " + description).lower()
    return any(kw in text for kw in _LONG_CYCLE_KEYWORDS)


def _is_fundamental(name: str, description: str = "") -> bool:
    text = (name + " " + description).lower()
    return any(kw in text for kw in _FUNDAMENTAL_KEYWORDS)


def _make_feature_id(prefix: str, name: str) -> str:
    """Convert a human-readable name to a stable feature ID."""
    safe = name.lower().strip()
    for ch in (" ", "/", "(", ")", ",", ";", ":", ".", "—", "-"):
        safe = safe.replace(ch, "_")
    # Collapse repeated underscores
    while "__" in safe:
        safe = safe.replace("__", "_")
    safe = safe.strip("_")[:60]
    return f"{prefix}.{safe}"


class KnowledgeFeatureBridge:
    """
    Converts v0.4.1.1 transcript-derived knowledge CSVs to ML feature metadata.

    Safety:
      auto_enabled = False (always, regardless of input)
      confidence   capped at PARTIAL
      long_cycle_risk → METADATA_ONLY, not_for_short_term_label=True

    [!] ML Research Only. No Real Orders.
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True
    auto_enabled: bool = False   # class-level guarantee

    def __init__(
        self,
        knowledge_dir: str = "data/backtest_results/strategy_knowledge",
    ):
        if os.path.isabs(knowledge_dir):
            self._knowledge_dir = knowledge_dir
        else:
            self._knowledge_dir = os.path.join(BASE_DIR, knowledge_dir)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def convert_all(self) -> Dict[str, List[dict]]:
        """
        Load all knowledge CSVs and convert to feature metadata dicts.

        Returns dict with keys:
            factor_features, rule_features, avoid_features, risk_features,
            all_features (combined), summary
        """
        from knowledge.knowledge_store import StrategyKnowledgeStore
        store = StrategyKnowledgeStore(output_dir=self._knowledge_dir)

        factor_rows   = store.load_factor_candidates()
        rule_rows     = store.load_rule_candidates()
        avoid_rows    = store.load_avoid_conditions()
        risk_rows     = store.load_risk_conditions()

        factor_features = self.convert_factor_candidates(factor_rows)
        rule_features   = self.convert_rule_candidates(rule_rows)
        avoid_features  = self.convert_avoid_conditions(avoid_rows)
        risk_features   = self.convert_risk_conditions(risk_rows)

        all_features = factor_features + rule_features + avoid_features + risk_features

        # Deduplicate by feature_id (keep first)
        seen: dict[str, dict] = {}
        for feat in all_features:
            fid = feat.get("feature_id", "")
            if fid and fid not in seen:
                seen[fid] = feat
        all_features = list(seen.values())

        # Enforce auto_enabled=False on all
        for feat in all_features:
            feat["auto_enabled"] = False

        summary = {
            "factor_features_count":  len(factor_features),
            "rule_features_count":    len(rule_features),
            "avoid_features_count":   len(avoid_features),
            "risk_features_count":    len(risk_features),
            "total_features_count":   len(all_features),
            "auto_enabled_count":     0,
            "knowledge_dir":          self._knowledge_dir,
            "source_rows": {
                "factor_candidates":   len(factor_rows),
                "rule_candidates":     len(rule_rows),
                "avoid_conditions":    len(avoid_rows),
                "risk_conditions":     len(risk_rows),
            },
        }

        return {
            "factor_features": factor_features,
            "rule_features":   rule_features,
            "avoid_features":  avoid_features,
            "risk_features":   risk_features,
            "all_features":    all_features,
            "summary":         summary,
        }

    # ------------------------------------------------------------------
    # Per-category converters
    # ------------------------------------------------------------------

    def convert_factor_candidates(self, rows: List[dict]) -> List[dict]:
        """
        factor_candidates → feature_source=transcript_knowledge
        readiness = NEEDS_MAPPING (default) or PARTIAL if description is richer
        """
        results = []
        for row in rows:
            name = row.get("factor_name", row.get("name", "")).strip()
            if not name:
                continue
            description = row.get("description", row.get("factor_description", ""))
            feature_id  = _make_feature_id("kf.factor", name)
            long_cycle  = _is_long_cycle(name, description)
            fundamental = _is_fundamental(name, description)

            readiness = READINESS_NEEDS_MAPPING
            if long_cycle:
                readiness = READINESS_METADATA_ONLY
            elif fundamental:
                readiness = READINESS_NEEDS_MAPPING

            feat = {
                "feature_id":              feature_id,
                "feature_name":            name,
                "feature_source":          SOURCE_TRANSCRIPT,
                "source_category":         "factor_candidate",
                "feature_type":            _infer_feature_type(name, description),
                "timeframe":               "cycle" if long_cycle else "daily",
                "description":             description,
                "readiness":               readiness,
                "confidence":              _cap_confidence(row.get("confidence", "PARTIAL")),
                "auto_enabled":            False,
                "experimental":            True,
                "not_for_short_term_label": long_cycle,
                "leakage_note":            "TIMING_ESTIMATED" if fundamental else "",
                "source_rule_id":          row.get("rule_id", row.get("source_rule_id", "")),
                "source_item_id":          row.get("item_id", row.get("source_item_id", "")),
                "notes":                   row.get("notes", ""),
            }
            results.append(feat)
        return results

    def convert_rule_candidates(self, rows: List[dict]) -> List[dict]:
        """
        rule_candidates → feature_source=rule_candidate, readiness=NEEDS_BACKTEST
        auto_enabled=False always
        """
        results = []
        for row in rows:
            rule_id   = row.get("rule_id", "").strip()
            name      = row.get("rule_name", row.get("name", rule_id)).strip()
            if not name:
                continue
            description = row.get("description", row.get("rule_description", ""))
            long_cycle  = _is_long_cycle(rule_id + " " + name, description)

            feature_id = _make_feature_id("kf.rule", name)
            readiness  = READINESS_METADATA_ONLY if long_cycle else READINESS_NEEDS_BACKTEST

            feat = {
                "feature_id":              feature_id,
                "feature_name":            name,
                "feature_source":          SOURCE_RULE_CANDIDATE,
                "source_category":         "rule_candidate",
                "feature_type":            "boolean",
                "timeframe":               "cycle" if long_cycle else "daily",
                "description":             description,
                "readiness":               readiness,
                "confidence":              _cap_confidence(row.get("confidence", "PARTIAL")),
                "auto_enabled":            False,
                "experimental":            True,
                "not_for_short_term_label": long_cycle,
                "leakage_note":            "POST_EVENT_KNOWLEDGE: rule candidate not yet back-tested",
                "source_rule_id":          rule_id,
                "source_item_id":          row.get("item_id", ""),
                "notes":                   row.get("notes", ""),
            }
            results.append(feat)
        return results

    def convert_avoid_conditions(self, rows: List[dict]) -> List[dict]:
        """
        avoid_conditions → feature_source=avoid_condition, feature_type=avoid_flag
        expected_direction = negative / avoid
        readiness = PARTIAL or NEEDS_BACKTEST
        """
        results = []
        for row in rows:
            name = row.get("condition_name", row.get("name", "")).strip()
            if not name:
                continue
            description = row.get("description", row.get("condition_description", ""))
            long_cycle  = _is_long_cycle(name, description)
            # Check if it's a pattern-based condition (M-head/head-shoulders → needs pattern_confirmed_date)
            pattern_based = any(kw in (name + " " + description).lower()
                                for kw in ["m頭", "頭肩頂", "top pattern", "double top", "pattern"])

            readiness = READINESS_METADATA_ONLY if long_cycle else (
                READINESS_PARTIAL if not pattern_based else READINESS_NEEDS_BACKTEST
            )

            feat = {
                "feature_id":              _make_feature_id("kf.avoid", name),
                "feature_name":            name,
                "feature_source":          SOURCE_AVOID_CONDITION,
                "source_category":         "avoid_condition",
                "feature_type":            "avoid_flag",
                "timeframe":               "cycle" if long_cycle else "daily",
                "description":             description,
                "readiness":               readiness,
                "confidence":              _cap_confidence(row.get("confidence", "PARTIAL")),
                "auto_enabled":            False,
                "experimental":            True,
                "expected_direction":      "negative",
                "not_for_short_term_label": long_cycle,
                "leakage_note":            (
                    "PATTERN_INCOMPLETE: pattern_confirmed_date required"
                    if pattern_based else ""
                ),
                "source_rule_id":          row.get("rule_id", ""),
                "source_item_id":          row.get("item_id", ""),
                "notes":                   row.get("notes", ""),
            }
            results.append(feat)
        return results

    def convert_risk_conditions(self, rows: List[dict]) -> List[dict]:
        """
        risk_conditions → feature_source=risk_condition, feature_type=risk_flag or regime_flag
        readiness = PARTIAL or METADATA_ONLY
        long_cycle_risk → regime_flag, METADATA_ONLY, not_for_short_term_label=True
        """
        results = []
        for row in rows:
            name = row.get("condition_name", row.get("name", "")).strip()
            if not name:
                continue
            description = row.get("description", row.get("condition_description", ""))
            long_cycle  = _is_long_cycle(name, description)

            if long_cycle:
                feature_type = "regime_flag"
                readiness    = READINESS_METADATA_ONLY
                timeframe    = "cycle"
                leakage_note = "LONG_CYCLE_RISK: regime/cycle metadata only — not_for_short_term_label=True"
            else:
                feature_type = "risk_flag"
                readiness    = READINESS_PARTIAL
                timeframe    = "daily"
                leakage_note = ""

            feat = {
                "feature_id":              _make_feature_id("kf.risk", name),
                "feature_name":            name,
                "feature_source":          SOURCE_RISK_CONDITION,
                "source_category":         "risk_condition",
                "feature_type":            feature_type,
                "timeframe":               timeframe,
                "description":             description,
                "readiness":               readiness,
                "confidence":              _cap_confidence(row.get("confidence", "PARTIAL")),
                "auto_enabled":            False,
                "experimental":            True,
                "not_for_short_term_label": long_cycle,
                "leakage_note":            leakage_note,
                "source_rule_id":          row.get("rule_id", ""),
                "source_item_id":          row.get("item_id", ""),
                "notes":                   row.get("notes", ""),
            }
            results.append(feat)
        return results

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def knowledge_dir_exists(self) -> bool:
        return os.path.isdir(self._knowledge_dir)

    def knowledge_files_present(self) -> Dict[str, bool]:
        files = [
            "factor_candidates.csv",
            "rule_candidates.csv",
            "avoid_conditions.csv",
            "risk_conditions.csv",
            "knowledge_items.csv",
        ]
        return {f: os.path.isfile(os.path.join(self._knowledge_dir, f)) for f in files}


# ------------------------------------------------------------------
# Module-level helpers
# ------------------------------------------------------------------

_CONFIDENCE_ORDER = ["HIGH", "GOOD", "PARTIAL", "WEAK", "LOW", "UNKNOWN", "PLANNED"]
_CONFIDENCE_CAP   = "PARTIAL"
_CAP_INDEX        = _CONFIDENCE_ORDER.index(_CONFIDENCE_CAP)


def _cap_confidence(confidence: str) -> str:
    """Cap transcript-only confidence at PARTIAL."""
    c = str(confidence).strip().upper()
    if c not in _CONFIDENCE_ORDER:
        return _CONFIDENCE_CAP
    idx = _CONFIDENCE_ORDER.index(c)
    return _CONFIDENCE_ORDER[max(idx, _CAP_INDEX)]


def _infer_feature_type(name: str, description: str = "") -> str:
    text = (name + " " + description).lower()
    if any(kw in text for kw in ["flag", "boolean", "是否", "whether", "binary"]):
        return "boolean"
    if any(kw in text for kw in ["ratio", "rate", "return", "growth", "pct", "%", "score", "value"]):
        return "numeric"
    if any(kw in text for kw in ["regime", "cycle", "market_phase"]):
        return "metadata"
    return "numeric"
