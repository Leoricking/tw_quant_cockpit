"""data_stabilization/feature_readiness_checker.py — FeatureReadinessChecker v0.5.5.

Checks whether each feature group / dataset is available, fresh, and leakage-free.

[!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import glob
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
STATUS_READY        = "READY"
STATUS_PARTIAL      = "PARTIAL"
STATUS_MISSING      = "MISSING"
STATUS_STALE        = "STALE"
STATUS_LEAKAGE_RISK = "LEAKAGE_RISK"
STATUS_FAILED       = "FAILED"

# ---------------------------------------------------------------------------
# Feature group definitions
# ---------------------------------------------------------------------------
_FEATURE_GROUPS = {
    "technical_features": {
        "file_patterns": ["data/backtest_results/technical_features*.csv",
                          "data/backtest_results/feature_store*.csv"],
        "required_columns": ["date", "symbol", "ma5", "ma20", "ma60", "rsi14"],
        "freshness_days": 3,
        "leakage_columns": ["future_return", "next_close", "next_high", "next_low",
                             "label", "target", "forward", "tomorrow"],
    },
    "microstructure_features": {
        "file_patterns": ["data/backtest_results/microstructure*.csv"],
        "required_columns": ["datetime", "symbol"],
        "freshness_days": 2,
        "leakage_columns": ["future_price", "next_tick", "label"],
    },
    "financial_features": {
        "file_patterns": ["data/backtest_results/financial_features*.csv"],
        "required_columns": ["date", "symbol", "eps_ttm", "gross_margin"],
        "freshness_days": 120,
        "leakage_columns": ["future_revenue", "next_eps", "label", "target"],
    },
    "chip_features": {
        "file_patterns": ["data/backtest_results/chip_features*.csv"],
        "required_columns": ["date", "symbol", "institutional_net_3d"],
        "freshness_days": 3,
        "leakage_columns": ["future_price", "label", "target"],
    },
    "strategy_filter_features": {
        "file_patterns": ["data/backtest_results/strategy_filter_pack*.csv"],
        "required_columns": ["date", "symbol"],
        "freshness_days": 3,
        "leakage_columns": ["label", "target", "future"],
    },
    "ml_knowledge_features": {
        "file_patterns": ["data/backtest_results/ml_feature_store/*.csv",
                          "data/backtest_results/ml_knowledge*.csv"],
        "required_columns": ["date", "symbol"],
        "freshness_days": 7,
        "leakage_columns": ["future_return", "realized_return", "label", "target"],
    },
}


class FeatureReadinessChecker:
    """Checks feature group readiness: availability, freshness, leakage.

    [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        schema_registry=None,
        data_root: str = "data",
    ) -> None:
        self.data_root = os.path.join(BASE_DIR, data_root)
        self._schema_registry = schema_registry

    def get_feature_groups(self) -> List[str]:
        """Return list of defined feature group names."""
        return list(_FEATURE_GROUPS.keys())

    def check_all(self) -> List[dict]:
        """Check all feature groups. Returns list of readiness dicts."""
        results = []
        for group_name in _FEATURE_GROUPS:
            result = self.check_feature_group(group_name)
            results.append(result)
        return results

    def check_feature_group(self, group_name: str) -> dict:
        """Check a single feature group."""
        try:
            defn = _FEATURE_GROUPS.get(group_name)
            if defn is None:
                return {
                    "feature_group":   group_name,
                    "dataset_name":    group_name,
                    "status":          STATUS_MISSING,
                    "readiness_score": 0.0,
                    "missing_columns": [],
                    "stale":           False,
                    "row_count":       0,
                    "last_updated":    "",
                    "leakage_risk":    False,
                    "notes":           f"No definition for feature group '{group_name}'",
                }

            # Find latest matching file
            found_path = ""
            for pattern in defn["file_patterns"]:
                full = os.path.join(BASE_DIR, pattern)
                matches = sorted(glob.glob(full))
                if matches:
                    found_path = matches[-1]
                    break

            if not found_path:
                return {
                    "feature_group":   group_name,
                    "dataset_name":    group_name,
                    "status":          STATUS_MISSING,
                    "readiness_score": 0.0,
                    "missing_columns": defn["required_columns"],
                    "stale":           False,
                    "row_count":       0,
                    "last_updated":    "",
                    "leakage_risk":    False,
                    "notes":           f"No file found for {group_name}",
                }

            return self.check_feature_file(found_path, defn, group_name)

        except Exception as exc:
            logger.warning("FeatureReadinessChecker.check_feature_group(%s): %s", group_name, exc)
            return {
                "feature_group":   group_name,
                "dataset_name":    group_name,
                "status":          STATUS_FAILED,
                "readiness_score": 0.0,
                "missing_columns": [],
                "stale":           False,
                "row_count":       0,
                "last_updated":    "",
                "leakage_risk":    False,
                "notes":           str(exc),
            }

    def check_feature_file(self, path: str, schema: dict, group_name: str = "") -> dict:
        """Check a specific file against its schema definition."""
        try:
            import csv as csv_mod
            # Read header only
            header_cols = []
            row_count   = 0
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv_mod.reader(f)
                hdr = next(reader, None)
                if hdr:
                    header_cols = [c.strip().lower() for c in hdr]
                for _ in reader:
                    row_count += 1
                    if row_count >= 1000:
                        # Estimate the rest from file size
                        break

            required = [c.lower() for c in schema.get("required_columns", [])]
            missing  = [c for c in required if c not in header_cols]
            leakage_cols = schema.get("leakage_columns", [])
            leakage_risk = any(lc.lower() in header_cols for lc in leakage_cols)

            # Freshness
            mtime = os.path.getmtime(path)
            age_days = (datetime.now().timestamp() - mtime) / 86400
            fresh_threshold = schema.get("freshness_days", 3)
            stale = age_days > fresh_threshold
            last_updated = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

            # Score
            if leakage_risk:
                status = STATUS_LEAKAGE_RISK
                score  = 0.0
            elif missing and stale:
                status = STATUS_PARTIAL
                score  = 30.0
            elif missing:
                status = STATUS_PARTIAL
                score  = max(0.0, 100.0 - len(missing) * 15.0)
            elif stale:
                status = STATUS_STALE
                score  = 60.0
            elif row_count == 0:
                status = STATUS_PARTIAL
                score  = 50.0
            else:
                status = STATUS_READY
                score  = 100.0

            notes = ""
            if leakage_risk:
                risky = [lc for lc in leakage_cols if lc.lower() in header_cols]
                notes = f"Leakage risk: columns {risky} detected"
            elif missing:
                notes = f"Missing required columns: {missing}"
            elif stale:
                notes = f"Stale: {age_days:.1f} days old (threshold: {fresh_threshold})"

            return {
                "feature_group":   group_name or os.path.basename(path),
                "dataset_name":    group_name or os.path.basename(path),
                "status":          status,
                "readiness_score": round(score, 1),
                "missing_columns": missing,
                "stale":           stale,
                "row_count":       row_count,
                "last_updated":    last_updated,
                "leakage_risk":    leakage_risk,
                "notes":           notes,
            }

        except Exception as exc:
            logger.warning("FeatureReadinessChecker.check_feature_file(%s): %s", path, exc)
            return {
                "feature_group":   group_name,
                "dataset_name":    group_name,
                "status":          STATUS_FAILED,
                "readiness_score": 0.0,
                "missing_columns": [],
                "stale":           False,
                "row_count":       0,
                "last_updated":    "",
                "leakage_risk":    False,
                "notes":           str(exc),
            }
