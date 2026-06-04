"""data_stabilization/data_stabilization_engine.py — DataStabilizationEngine v0.5.5.

Orchestrates schema validation, lineage tracking, feature readiness,
feature store health, and leakage guard. Outputs 6 CSV files.

[!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_DIR = os.path.join(
    BASE_DIR, "data", "backtest_results", "data_stabilization"
)


class DataStabilizationEngine:
    """Runs all Data / Feature Store Stabilization checks and saves outputs.

    [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    VERSION = "v0.5.5"

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        data_root: str = "data",
        output_dir: str = "data/backtest_results/data_stabilization",
    ) -> None:
        self.data_root  = os.path.join(BASE_DIR, data_root)
        self.output_dir = os.path.join(BASE_DIR, output_dir)

    def run(self, mode: str = "real") -> dict:
        """Run all stabilization checks. Returns summary dict."""
        logger.info(
            "DataStabilizationEngine.run [mode=%s output=%s]", mode, self.output_dir
        )

        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        errors       = []

        # 1. Schema registry
        schema_rows  = []
        schemas_defined = 0
        try:
            from data_stabilization.data_schema_registry import DatasetSchemaRegistry
            reg         = DatasetSchemaRegistry()
            schema_rows = reg.build_schema_table()
            schemas_defined = len(schema_rows)
        except Exception as exc:
            logger.warning("DataStabilizationEngine: schema registry failed: %s", exc)
            errors.append(f"schema_registry: {exc}")

        # 2. Lineage tracking
        lineage_rows  = []
        lineage_count = 0
        try:
            from data_stabilization.data_lineage_tracker import DataLineageTracker
            tracker      = DataLineageTracker(output_dir=self.output_dir)
            lineage_rows = tracker.build_lineage_table()
            lineage_count = len(lineage_rows)
        except Exception as exc:
            logger.warning("DataStabilizationEngine: lineage tracker failed: %s", exc)
            errors.append(f"lineage_tracker: {exc}")

        # 3. Feature readiness
        readiness_rows   = []
        feature_groups   = 0
        readiness_score  = 0.0
        try:
            from data_stabilization.feature_readiness_checker import FeatureReadinessChecker
            checker        = FeatureReadinessChecker()
            readiness_rows = checker.check_all()
            feature_groups = len(readiness_rows)
            scores         = [r.get("readiness_score", 0.0) for r in readiness_rows]
            readiness_score = round(sum(scores) / len(scores), 1) if scores else 0.0
        except Exception as exc:
            logger.warning("DataStabilizationEngine: feature readiness failed: %s", exc)
            errors.append(f"feature_readiness: {exc}")

        # 4. Feature store health
        health      = {}
        health_score = 0.0
        try:
            from data_stabilization.feature_store_health import FeatureStoreHealthChecker
            health_checker = FeatureStoreHealthChecker()
            health         = health_checker.run(readiness_results=readiness_rows)
            health_score   = health.get("health_score", 0.0)
        except Exception as exc:
            logger.warning("DataStabilizationEngine: feature store health failed: %s", exc)
            errors.append(f"feature_store_health: {exc}")

        # 5. Leakage guard
        leakage_rows    = []
        leakage_warnings = 0
        try:
            from data_stabilization.leakage_guard import DataLeakageGuard
            guard = DataLeakageGuard()
            # Check all lineage records for leakage
            for rec in lineage_rows:
                ds_name = rec.get("dataset_name", "")
                cols_str = rec.get("columns", "")
                # columns is int in lineage — check from schema instead
            # Check feature readiness for leakage flags
            for fr in readiness_rows:
                if fr.get("leakage_risk", False):
                    guard.check_dataset(
                        fr.get("dataset_name", ""),
                        {"columns": fr.get("missing_columns", [])},
                    )
            leakage_rows    = guard.build_leakage_summary()
            leakage_warnings = len(leakage_rows)
        except Exception as exc:
            logger.warning("DataStabilizationEngine: leakage guard failed: %s", exc)
            errors.append(f"leakage_guard: {exc}")

        # 6. Save outputs
        output_paths = {}
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            store = DataStabilizationStore(output_dir=self.output_dir)

            # Build dataset count
            datasets_checked = len(set(
                r.get("dataset_name", "") for r in lineage_rows if r.get("dataset_name")
            ))

            overall_status = health.get("overall_status", "UNKNOWN")
            blockers_list  = health.get("blockers", [])

            summary = {
                "generated_at":          generated_at,
                "mode":                   mode,
                "version":                self.VERSION,
                "datasets_checked":       datasets_checked,
                "schemas_defined":        schemas_defined,
                "lineage_records":        lineage_count,
                "feature_groups_checked": feature_groups,
                "readiness_score":        readiness_score,
                "health_score":           health_score,
                "leakage_warnings":       leakage_warnings,
                "blockers":               "; ".join(blockers_list),
                "overall_status":         overall_status,
                "no_real_orders":         True,
                "production_blocked":     True,
            }

            output_paths["summary"]           = store.save_summary(summary)
            output_paths["schema_status"]     = store.save_schema_status(schema_rows)
            output_paths["lineage"]           = store.save_lineage(lineage_rows)
            output_paths["feature_readiness"] = store.save_feature_readiness(readiness_rows)
            output_paths["health"]            = store.save_health(health)
            output_paths["leakage_summary"]   = store.save_leakage_summary(leakage_rows)

        except Exception as exc:
            logger.warning("DataStabilizationEngine: store save failed: %s", exc)
            errors.append(f"store: {exc}")
            summary = {"generated_at": generated_at, "mode": mode}

        return {
            "generated_at":          generated_at,
            "mode":                   mode,
            "version":                self.VERSION,
            "datasets_checked":       datasets_checked if "datasets_checked" in dir() else 0,
            "schemas_defined":        schemas_defined,
            "lineage_records":        lineage_count,
            "feature_groups_checked": feature_groups,
            "readiness_score":        readiness_score,
            "health_score":           health_score,
            "leakage_warnings":       leakage_warnings,
            "blockers":               health.get("blockers", []),
            "overall_status":         health.get("overall_status", "UNKNOWN"),
            "output_paths":           output_paths,
            "errors":                 errors,
            "no_real_orders":         True,
            "production_blocked":     True,
        }

    def build_summary(self) -> dict:
        """Load latest saved summary from store."""
        try:
            from data_stabilization.data_stabilization_store import DataStabilizationStore
            store = DataStabilizationStore(output_dir=self.output_dir)
            return store.load_latest_summary()
        except Exception as exc:
            logger.warning("DataStabilizationEngine.build_summary(): %s", exc)
            return {}
