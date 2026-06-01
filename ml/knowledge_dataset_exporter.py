"""
ml/knowledge_dataset_exporter.py — KnowledgeDatasetExporter (v0.4.2.1).

Exports transcript-derived knowledge feature metadata to:
  data/backtest_results/ml_feature_store/knowledge_feature_catalog.csv
  data/backtest_results/ml_feature_store/knowledge_feature_readiness.csv
  data/backtest_results/ml_feature_store/knowledge_feature_leakage.csv
  data/backtest_results/ml_feature_store/model_ready_knowledge_schema.json

model_ready_knowledge_schema.json contains ONLY features where:
  - readiness in (READY, PARTIAL)
  - no CRITICAL leakage findings
  - auto_enabled = False (always)

Safety invariants:
  auto_enabled = False (always)
  confidence   ≤ PARTIAL (transcript-only)
  Does NOT trigger model training
  Does NOT place orders

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

_DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "data", "backtest_results", "ml_feature_store")

_READINESS_FIELDS = [
    "feature_id", "readiness", "readiness_score",
    "auto_enabled", "not_for_short_term_label",
    "leakage_note", "confidence", "reasons",
]

_LEAKAGE_FIELDS = [
    "feature_id", "feature_name", "readiness",
    "leakage_types", "worst_severity", "leakage_count", "auto_enabled",
]

# Readiness values eligible for model-ready schema
_MODEL_READY_READINESS = {"READY", "PARTIAL"}


class KnowledgeDatasetExporter:
    """
    Exports knowledge feature metadata to CSV/JSON outputs.

    Output files:
      knowledge_feature_catalog.csv    — all features, all fields
      knowledge_feature_readiness.csv  — readiness assessment per feature
      knowledge_feature_leakage.csv    — leakage summary per feature
      model_ready_knowledge_schema.json — features eligible for optional use in ML

    [!] ML Research Only. No Real Orders.
    """

    read_only: bool = True
    no_real_orders: bool = True
    auto_enabled: bool = False

    def __init__(self, output_dir: str = _DEFAULT_OUTPUT_DIR):
        if os.path.isabs(output_dir):
            self._output_dir = output_dir
        else:
            self._output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(self._output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def export_all(
        self,
        catalog_features:    List[dict],
        readiness_results:   List[dict],
        leakage_result:      dict,
        dry_run:             bool = False,
    ) -> dict:
        """
        Export all four output files.

        Parameters
        ----------
        catalog_features   : feature metadata dicts from KnowledgeFeatureCatalog
        readiness_results  : readiness dicts from KnowledgeFeatureReadinessChecker
        leakage_result     : full result dict from KnowledgeLeakageChecker.check_features()
        dry_run            : if True, no files are written

        Returns output paths dict.
        """
        # Build leakage feature table
        leakage_features = leakage_result.get("findings_by_feature", {})
        leakage_rows = self._build_leakage_rows(catalog_features, leakage_features)

        # Build model-ready schema
        model_ready = self._build_model_ready_schema(
            catalog_features, readiness_results, leakage_result
        )

        catalog_path   = self._export_catalog(catalog_features, dry_run)
        readiness_path = self._export_readiness(readiness_results, dry_run)
        leakage_path   = self._export_leakage(leakage_rows, dry_run)
        schema_path    = self._export_model_ready_schema(model_ready, dry_run)

        summary = {
            "generated_at":           datetime.now().isoformat(),
            "dry_run":                dry_run,
            "ml_research_only":       True,
            "no_real_orders":         True,
            "auto_enabled_count":     0,
            "total_features":         len(catalog_features),
            "model_ready_features":   len(model_ready.get("features", [])),
            "leakage_findings":       leakage_result.get("total_findings", 0),
            "critical_leakage":       leakage_result.get("critical_count", 0),
            "output_files": {
                "catalog":    catalog_path,
                "readiness":  readiness_path,
                "leakage":    leakage_path,
                "schema":     schema_path,
            },
        }

        if not dry_run:
            self._write_integration_summary(summary)

        return summary

    # ------------------------------------------------------------------
    # Individual exporters
    # ------------------------------------------------------------------

    def _export_catalog(self, features: List[dict], dry_run: bool) -> str:
        path = os.path.join(self._output_dir, "knowledge_feature_catalog.csv")
        if dry_run:
            return path
        if not features:
            open(path, "w").close()
            return path

        all_keys = list(features[0].keys()) if features else []
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=all_keys, extrasaction="ignore")
            writer.writeheader()
            for feat in features:
                row = dict(feat)
                row["auto_enabled"] = False
                writer.writerow(row)
        logger.info("KnowledgeDatasetExporter: catalog → %s (%d rows)", path, len(features))
        return path

    def _export_readiness(self, readiness_results: List[dict], dry_run: bool) -> str:
        path = os.path.join(self._output_dir, "knowledge_feature_readiness.csv")
        if dry_run:
            return path
        rows = []
        for r in readiness_results:
            row = {f: r.get(f, "") for f in _READINESS_FIELDS}
            row["auto_enabled"] = False
            # reasons list → semicolon-joined string
            reasons = row.get("reasons", [])
            if isinstance(reasons, list):
                row["reasons"] = "; ".join(reasons)
            rows.append(row)
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=_READINESS_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        logger.info("KnowledgeDatasetExporter: readiness → %s (%d rows)", path, len(rows))
        return path

    def _export_leakage(self, leakage_rows: List[dict], dry_run: bool) -> str:
        path = os.path.join(self._output_dir, "knowledge_feature_leakage.csv")
        if dry_run:
            return path
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=_LEAKAGE_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(leakage_rows)
        logger.info("KnowledgeDatasetExporter: leakage → %s (%d rows)", path, len(leakage_rows))
        return path

    def _export_model_ready_schema(self, model_ready: dict, dry_run: bool) -> str:
        path = os.path.join(self._output_dir, "model_ready_knowledge_schema.json")
        if dry_run:
            return path
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(model_ready, fh, ensure_ascii=False, indent=2)
        n = len(model_ready.get("features", []))
        logger.info("KnowledgeDatasetExporter: schema → %s (%d model-ready features)", path, n)
        return path

    def _write_integration_summary(self, summary: dict) -> str:
        path = os.path.join(self._output_dir, "ml_knowledge_integration_summary.json")
        try:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(summary, fh, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.warning("KnowledgeDatasetExporter._write_integration_summary: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Build helpers
    # ------------------------------------------------------------------

    def _build_leakage_rows(
        self,
        features: List[dict],
        findings_by_feature: Dict[str, List[dict]],
    ) -> List[dict]:
        rows = []
        for feat in features:
            fid = feat.get("feature_id", "")
            feat_findings = findings_by_feature.get(fid, [])
            leakage_types = list({f.get("leakage_type", "") for f in feat_findings if f.get("leakage_type")})
            worst = ""
            for f in feat_findings:
                sv = f.get("severity", "")
                if sv == "CRITICAL":
                    worst = "CRITICAL"
                elif sv == "WARNING" and worst != "CRITICAL":
                    worst = "WARNING"
                elif sv == "INFO" and not worst:
                    worst = "INFO"
            rows.append({
                "feature_id":    fid,
                "feature_name":  feat.get("feature_name", ""),
                "readiness":     feat.get("readiness", ""),
                "leakage_types": "; ".join(leakage_types),
                "worst_severity": worst,
                "leakage_count": len(feat_findings),
                "auto_enabled":  False,
            })
        return rows

    def _build_model_ready_schema(
        self,
        features: List[dict],
        readiness_results: List[dict],
        leakage_result: dict,
    ) -> dict:
        """
        model_ready_knowledge_schema includes ONLY features where:
          - readiness in (READY, PARTIAL)
          - no CRITICAL leakage
          - auto_enabled = False (always)

        These are OPTIONAL features — they are NOT auto-enabled.
        """
        # Index readiness
        readiness_map: Dict[str, str] = {}
        for r in readiness_results:
            readiness_map[r.get("feature_id", "")] = r.get("readiness", "")

        # Index leakage critical findings
        critical_features: set = set()
        for finding in leakage_result.get("findings", []):
            if finding.get("severity") == "CRITICAL":
                critical_features.add(finding.get("feature_id", ""))

        model_ready_features = []
        for feat in features:
            fid = feat.get("feature_id", "")
            readiness = readiness_map.get(fid, feat.get("readiness", ""))
            if readiness not in _MODEL_READY_READINESS:
                continue
            if fid in critical_features:
                continue
            # long_cycle / regime → always excluded
            if (feat.get("timeframe") == "cycle"
                    or feat.get("feature_type") == "regime_flag"
                    or feat.get("not_for_short_term_label", False)):
                continue

            model_ready_features.append({
                "feature_id":    fid,
                "feature_name":  feat.get("feature_name", ""),
                "feature_source": feat.get("feature_source", ""),
                "feature_type":  feat.get("feature_type", ""),
                "readiness":     readiness,
                "confidence":    feat.get("confidence", "PARTIAL"),
                "auto_enabled":  False,
                "experimental":  True,
                "include_condition": (
                    "optional — must be explicitly included with "
                    "--include-knowledge-features flag; default=False"
                ),
                "notes": feat.get("notes", ""),
            })

        return {
            "schema_version":        "v0.4.2.1",
            "generated_at":          datetime.now().isoformat(),
            "ml_research_only":      True,
            "no_real_orders":        True,
            "auto_enabled_count":    0,
            "total_model_ready":     len(model_ready_features),
            "include_by_default":    False,
            "enable_flag":           "--include-knowledge-features (default False)",
            "safety_note": (
                "All features in this schema are OPTIONAL and auto_enabled=False. "
                "None are included in training by default. "
                "Long-cycle/regime features are excluded entirely."
            ),
            "features": model_ready_features,
        }

    # ------------------------------------------------------------------
    # Load summary (for CLI summary command)
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """Load the latest integration summary JSON. Returns empty dict if not found."""
        path = os.path.join(self._output_dir, "ml_knowledge_integration_summary.json")
        if not os.path.isfile(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as exc:
            logger.warning("KnowledgeDatasetExporter.load_latest_summary: %s", exc)
            return {}
