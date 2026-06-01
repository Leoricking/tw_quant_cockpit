"""
ml/knowledge_feature_catalog.py — KnowledgeFeatureCatalog (v0.4.2.1).

Manages transcript-derived feature catalog:
  - register features from KnowledgeFeatureBridge output
  - list/get/export by readiness, source, type
  - export to knowledge_feature_catalog.csv

Safety invariants:
  auto_enabled = False (always)
  confidence   ≤ PARTIAL (transcript-only cap)

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_OUTPUT_DIR = os.path.join(BASE_DIR, "data", "backtest_results", "ml_feature_store")

_CATALOG_FILENAME = "knowledge_feature_catalog.csv"

_CATALOG_FIELDS = [
    "feature_id", "feature_name", "feature_source", "source_category",
    "feature_type", "timeframe", "description", "readiness", "confidence",
    "auto_enabled", "experimental", "expected_direction",
    "not_for_short_term_label", "leakage_note",
    "source_rule_id", "source_item_id", "notes",
]


class KnowledgeFeatureCatalog:
    """
    Transcript-derived feature catalog.

    Immutable safety:
      auto_enabled = False for all registered features.

    [!] ML Research Only. No Real Orders.
    """

    read_only: bool = True
    no_real_orders: bool = True
    auto_enabled: bool = False

    def __init__(self, output_dir: str = _OUTPUT_DIR):
        if os.path.isabs(output_dir):
            self._output_dir = output_dir
        else:
            self._output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(self._output_dir, exist_ok=True)
        self._features: Dict[str, dict] = {}

    # ------------------------------------------------------------------
    # Register
    # ------------------------------------------------------------------

    def register_features(self, features: List[dict]) -> int:
        """
        Register a list of feature metadata dicts.
        Enforces auto_enabled=False on all.
        Returns count of newly registered features.
        """
        added = 0
        for feat in features:
            feat = dict(feat)
            feat["auto_enabled"] = False  # enforce invariant
            fid = feat.get("feature_id", "")
            if not fid:
                logger.warning("KnowledgeFeatureCatalog: skipping feature without feature_id")
                continue
            if fid not in self._features:
                self._features[fid] = feat
                added += 1
            else:
                logger.debug("KnowledgeFeatureCatalog: duplicate feature_id=%s, skipping", fid)
        return added

    def clear(self) -> None:
        self._features.clear()

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def list_features(
        self,
        readiness: Optional[str] = None,
        feature_source: Optional[str] = None,
        feature_type: Optional[str] = None,
        experimental_only: bool = False,
    ) -> List[dict]:
        result = list(self._features.values())
        if readiness:
            result = [f for f in result if f.get("readiness") == readiness]
        if feature_source:
            result = [f for f in result if f.get("feature_source") == feature_source]
        if feature_type:
            result = [f for f in result if f.get("feature_type") == feature_type]
        if experimental_only:
            result = [f for f in result if f.get("experimental", False)]
        return result

    def get_feature(self, feature_id: str) -> Optional[dict]:
        return self._features.get(feature_id)

    def count(self) -> int:
        return len(self._features)

    def summary(self) -> dict:
        all_f = list(self._features.values())
        by_readiness: Dict[str, int] = {}
        by_source: Dict[str, int] = {}
        by_type: Dict[str, int] = {}
        for f in all_f:
            r = f.get("readiness", "UNKNOWN")
            by_readiness[r] = by_readiness.get(r, 0) + 1
            s = f.get("feature_source", "unknown")
            by_source[s] = by_source.get(s, 0) + 1
            t = f.get("feature_type", "unknown")
            by_type[t] = by_type.get(t, 0) + 1
        return {
            "total_features":           len(all_f),
            "auto_enabled_count":       0,  # always 0
            "by_readiness":             by_readiness,
            "by_source":                by_source,
            "by_type":                  by_type,
            "metadata_only_count":      by_readiness.get("METADATA_ONLY", 0),
            "needs_backtest_count":     by_readiness.get("NEEDS_BACKTEST", 0),
            "needs_mapping_count":      by_readiness.get("NEEDS_MAPPING", 0),
            "partial_ready_count":      by_readiness.get("PARTIAL", 0),
            "not_short_term_label_count": sum(
                1 for f in all_f if f.get("not_for_short_term_label", False)
            ),
        }

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_csv(self, dry_run: bool = False) -> str:
        """Export catalog to knowledge_feature_catalog.csv. Returns path."""
        path = os.path.join(self._output_dir, _CATALOG_FILENAME)
        if dry_run:
            logger.info("KnowledgeFeatureCatalog.export_csv: dry_run — would write %d features → %s",
                        len(self._features), path)
            return path

        rows = []
        for feat in self._features.values():
            row = {field: feat.get(field, "") for field in _CATALOG_FIELDS}
            row["auto_enabled"] = False  # enforce on export
            rows.append(row)

        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=_CATALOG_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

        logger.info("KnowledgeFeatureCatalog: exported %d features → %s", len(rows), path)
        return path

    def export_json_summary(self, dry_run: bool = False) -> str:
        """Export catalog summary JSON. Returns path."""
        path = os.path.join(self._output_dir, "knowledge_feature_catalog_summary.json")
        if dry_run:
            return path
        data = {
            "generated_at":   datetime.now().isoformat(),
            "ml_research_only": True,
            "no_real_orders":   True,
            "auto_enabled_count": 0,
            "summary":          self.summary(),
            "features":         list(self._features.values()),
        }
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        return path

    # ------------------------------------------------------------------
    # Load from CSV (for downstream reads)
    # ------------------------------------------------------------------

    def load_from_csv(self) -> int:
        """Load catalog from existing knowledge_feature_catalog.csv. Returns count loaded."""
        path = os.path.join(self._output_dir, _CATALOG_FILENAME)
        if not os.path.isfile(path):
            logger.info("KnowledgeFeatureCatalog: no catalog CSV found at %s", path)
            return 0
        try:
            with open(path, "r", newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                rows = list(reader)
            self.clear()
            for row in rows:
                row["auto_enabled"] = False  # enforce on load
                fid = row.get("feature_id", "")
                if fid:
                    self._features[fid] = row
            logger.info("KnowledgeFeatureCatalog: loaded %d features from %s", len(rows), path)
            return len(rows)
        except Exception as exc:
            logger.warning("KnowledgeFeatureCatalog.load_from_csv: %s", exc)
            return 0
