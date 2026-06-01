"""
gui/ml_knowledge_integration_adapter.py — MLKnowledgeIntegrationAdapter (v0.4.2.1).

GUI bridge between MLKnowledgeIntegrationPanel and the ml.knowledge_* package.
All operations run through the adapter to keep the panel import-safe.

Safety invariants:
  read_only          = True
  no_real_orders     = True
  production_blocked = True
  auto_enabled       = False

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_KNOWLEDGE_DIR = "data/backtest_results/strategy_knowledge"
_DEFAULT_OUTPUT_DIR    = "data/backtest_results/ml_feature_store"
_DEFAULT_REPORT_DIR    = "reports"


class MLKnowledgeIntegrationAdapter:
    """
    GUI adapter for ML Knowledge Integration.

    All methods return dicts — never raise (GUI-safe).

    [!] ML Research Only. No Real Orders.
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True
    auto_enabled: bool = False

    def __init__(
        self,
        mode:          str = "real",
        knowledge_dir: str = _DEFAULT_KNOWLEDGE_DIR,
        output_dir:    str = _DEFAULT_OUTPUT_DIR,
        report_dir:    str = _DEFAULT_REPORT_DIR,
    ):
        self.mode = mode
        self._knowledge_dir = (
            knowledge_dir if os.path.isabs(knowledge_dir)
            else os.path.join(BASE_DIR, knowledge_dir)
        )
        self._output_dir = (
            output_dir if os.path.isabs(output_dir)
            else os.path.join(BASE_DIR, output_dir)
        )
        self._report_dir = (
            report_dir if os.path.isabs(report_dir)
            else os.path.join(BASE_DIR, report_dir)
        )

    # ------------------------------------------------------------------
    # Run integration
    # ------------------------------------------------------------------

    def run_integration(self, dry_run: bool = True) -> dict:
        """
        Run ML knowledge integration pipeline.

        Steps:
          1. KnowledgeFeatureBridge.convert_all()
          2. KnowledgeFeatureCatalog.register_features()
          3. KnowledgeFeatureReadinessChecker.check_features()
          4. KnowledgeLeakageChecker.check_features()
          5. KnowledgeDatasetExporter.export_all()

        Returns result dict. auto_enabled always 0.
        """
        try:
            from ml.knowledge_feature_bridge import KnowledgeFeatureBridge
            from ml.knowledge_feature_catalog import KnowledgeFeatureCatalog
            from ml.knowledge_feature_readiness import KnowledgeFeatureReadinessChecker
            from ml.knowledge_leakage_checker import KnowledgeLeakageChecker
            from ml.knowledge_dataset_exporter import KnowledgeDatasetExporter

            # 1. Bridge
            bridge = KnowledgeFeatureBridge(knowledge_dir=self._knowledge_dir)
            if not bridge.knowledge_dir_exists():
                return {
                    "status":  "WARNING",
                    "warning": (
                        "Strategy knowledge directory not found: "
                        f"{self._knowledge_dir}. "
                        "Run 'strategy-knowledge-ingest' first."
                    ),
                    "auto_enabled_count": 0,
                    "total_features": 0,
                    "dry_run": dry_run,
                }
            bridge_result = bridge.convert_all()
            all_features  = bridge_result.get("all_features", [])
            bridge_summary = bridge_result.get("summary", {})

            if not all_features:
                return {
                    "status":  "WARNING",
                    "warning": (
                        "No knowledge features found — "
                        "strategy knowledge CSVs are empty or not present."
                    ),
                    "auto_enabled_count": 0,
                    "total_features": 0,
                    "dry_run": dry_run,
                    "source_rows": bridge_summary.get("source_rows", {}),
                }

            # 2. Catalog
            catalog = KnowledgeFeatureCatalog(output_dir=self._output_dir)
            catalog.register_features(all_features)

            # 3. Readiness
            readiness_checker = KnowledgeFeatureReadinessChecker()
            readiness_results = readiness_checker.check_features(all_features)

            # 4. Leakage
            leakage_checker = KnowledgeLeakageChecker()
            leakage_result  = leakage_checker.check_features(all_features)

            # 5. Export
            exporter = KnowledgeDatasetExporter(output_dir=self._output_dir)
            export_summary = exporter.export_all(
                catalog_features=all_features,
                readiness_results=readiness_results,
                leakage_result=leakage_result,
                dry_run=dry_run,
            )

            result = {
                "status":             "OK",
                "dry_run":            dry_run,
                "auto_enabled_count": 0,
                "total_features":     len(all_features),
                "model_ready_features": export_summary.get("model_ready_features", 0),
                "leakage_status":     leakage_result.get("status", ""),
                "leakage_findings":   leakage_result.get("total_findings", 0),
                "critical_leakage":   leakage_result.get("critical_count", 0),
                "readiness_summary":  readiness_checker.build_summary(readiness_results),
                "source_summary":     bridge_summary,
                "output_files":       export_summary.get("output_files", {}),
                "ml_research_only":   True,
                "no_real_orders":     True,
            }
            return result

        except Exception as exc:
            logger.warning("MLKnowledgeIntegrationAdapter.run_integration: %s", exc)
            return {
                "status": "ERROR",
                "error":  str(exc),
                "auto_enabled_count": 0,
            }

    # ------------------------------------------------------------------
    # Leakage check
    # ------------------------------------------------------------------

    def check_leakage(self) -> dict:
        """Run leakage check on existing catalog CSV. Returns leakage result dict."""
        try:
            from ml.knowledge_feature_catalog import KnowledgeFeatureCatalog
            from ml.knowledge_leakage_checker import KnowledgeLeakageChecker

            catalog = KnowledgeFeatureCatalog(output_dir=self._output_dir)
            count = catalog.load_from_csv()
            if count == 0:
                return {
                    "status":  "WARNING",
                    "warning": "No knowledge feature catalog found. Run integration first.",
                    "auto_enabled_count": 0,
                }
            features = catalog.list_features()
            checker  = KnowledgeLeakageChecker()
            result   = checker.check_features(features)
            result["auto_enabled_count"] = 0
            return result
        except Exception as exc:
            logger.warning("MLKnowledgeIntegrationAdapter.check_leakage: %s", exc)
            return {"status": "ERROR", "error": str(exc), "auto_enabled_count": 0}

    # ------------------------------------------------------------------
    # Generate report
    # ------------------------------------------------------------------

    def generate_report(self, dry_run: bool = False) -> dict:
        """Generate ML Knowledge Integration Markdown report. Returns dict with path."""
        try:
            integration_result = self.run_integration(dry_run=True)
            if integration_result.get("status") not in ("OK", "WARNING"):
                return integration_result

            from ml.knowledge_feature_bridge import KnowledgeFeatureBridge
            from ml.knowledge_feature_readiness import KnowledgeFeatureReadinessChecker
            from ml.knowledge_leakage_checker import KnowledgeLeakageChecker
            from reports.ml_knowledge_integration_report import MLKnowledgeIntegrationReport

            bridge    = KnowledgeFeatureBridge(knowledge_dir=self._knowledge_dir)
            br_result = bridge.convert_all()
            features  = br_result.get("all_features", [])

            readiness_checker = KnowledgeFeatureReadinessChecker()
            readiness_results = readiness_checker.check_features(features)

            leakage_checker = KnowledgeLeakageChecker()
            leakage_result  = leakage_checker.check_features(features)

            schema_summary = {
                "total_model_ready": integration_result.get("model_ready_features", 0),
                "features": [],
            }

            reporter = MLKnowledgeIntegrationReport(report_dir=self._report_dir)
            path = reporter.generate(
                integration_summary=br_result.get("summary", {}),
                catalog_features=features,
                readiness_results=readiness_results,
                leakage_result=leakage_result,
                schema_summary=schema_summary,
                mode=self.mode,
                dry_run=dry_run,
            )
            return {"status": "OK", "report_path": path}

        except Exception as exc:
            logger.warning("MLKnowledgeIntegrationAdapter.generate_report: %s", exc)
            return {"status": "ERROR", "error": str(exc)}

    # ------------------------------------------------------------------
    # Load summary / report path
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """Load the latest integration summary JSON. Returns empty dict if not found."""
        try:
            from ml.knowledge_dataset_exporter import KnowledgeDatasetExporter
            exporter = KnowledgeDatasetExporter(output_dir=self._output_dir)
            return exporter.load_latest_summary()
        except Exception as exc:
            logger.warning("MLKnowledgeIntegrationAdapter.load_latest_summary: %s", exc)
            return {}

    def load_latest_report_path(self) -> Optional[str]:
        """Return path to latest report file, or None."""
        try:
            import glob
            pattern = os.path.join(self._report_dir, "ml_knowledge_integration_report_*.md")
            files = sorted(glob.glob(pattern))
            return files[-1] if files else None
        except Exception:
            return None

    def load_catalog_features(self) -> list:
        """Load features from existing catalog CSV. Returns list of dicts."""
        try:
            from ml.knowledge_feature_catalog import KnowledgeFeatureCatalog
            catalog = KnowledgeFeatureCatalog(output_dir=self._output_dir)
            catalog.load_from_csv()
            return catalog.list_features()
        except Exception as exc:
            logger.warning("MLKnowledgeIntegrationAdapter.load_catalog_features: %s", exc)
            return []

    def check_knowledge_files_present(self) -> dict:
        """Check which knowledge CSV files are present."""
        try:
            from ml.knowledge_feature_bridge import KnowledgeFeatureBridge
            bridge = KnowledgeFeatureBridge(knowledge_dir=self._knowledge_dir)
            return bridge.knowledge_files_present()
        except Exception as exc:
            return {"error": str(exc)}
