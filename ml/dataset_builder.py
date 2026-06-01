"""
ml/dataset_builder.py — ML Feature Dataset Builder (v0.4.2).

Builds model-ready datasets: features + labels + split + metadata.
Output: data/ml_features/model_ready_dataset_YYYYMMDD_HHMMSS.csv (not committed).

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] Do not commit model-ready datasets.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import List, Optional, Sequence, Tuple

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MLFeatureDatasetBuilder:
    """
    ML Feature Dataset Builder.

    Combines:
        1. Feature snapshot (from FeatureSnapshotBuilder)
        2. Label generation (from LabelGenerator)
        3. Train/validation/test split (from MLSplitManager)
        4. Dataset validation

    Output columns:
        symbol, date, <feature cols>, <label cols>, split, <metadata cols>

    [!] Research only. Not for live trading.
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        mode:        str = "real",
        output_root: str = "data/ml_features",
        results_dir: str = "data/backtest_results",
        universe:    Optional[str] = None,
    ):
        self.mode        = mode
        self.output_root = os.path.join(_BASE_DIR, output_root) if not os.path.isabs(output_root) else output_root
        self.results_dir = os.path.join(_BASE_DIR, results_dir) if not os.path.isabs(results_dir) else results_dir
        self.universe    = universe
        os.makedirs(self.output_root, exist_ok=True)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def build_dataset(
        self,
        symbols:        Optional[List[str]] = None,
        start_date:     Optional[str] = None,
        end_date:       Optional[str] = None,
        label_horizons: Sequence[int] = (5, 10, 20),
    ) -> Tuple[object, dict]:
        """
        Build a complete model-ready dataset.

        Returns (dataset_df, summary).
        """
        try:
            import pandas as pd

            # 1. Build feature snapshot
            from ml.feature_snapshot import FeatureSnapshotBuilder
            snap_builder = FeatureSnapshotBuilder(mode=self.mode, universe=self.universe)
            features_df, snap_summary = snap_builder.build(
                symbols=symbols, start_date=start_date, end_date=end_date
            )
            if features_df is None or (hasattr(features_df, "empty") and features_df.empty):
                return pd.DataFrame(), {
                    "status":   "NO_DATA",
                    "warnings": snap_summary.get("warnings", ["No feature data available"]),
                }

            # 2. Generate labels
            from ml.label_generator import LabelGenerator
            label_gen = LabelGenerator(horizons=list(label_horizons))
            labeled_df, label_summary = label_gen.generate(features_df)

            # 3. Join features and labels (already joined since generate works in-place)
            dataset_df = self.join_features_and_labels(labeled_df, None)

            # 4. Assign train/val/test split
            from ml.split_manager import MLSplitManager
            splitter = MLSplitManager(method="time_series")
            dataset_df, split_summary = splitter.assign_splits(dataset_df)

            # 5. Add metadata columns
            dataset_df["meta_mode"]         = self.mode
            dataset_df["meta_research_only"] = True
            dataset_df["meta_no_real_orders"] = True
            dataset_df["meta_generated_at"]  = datetime.now().isoformat()

            # 6. Validate
            validation = self.validate_dataset(dataset_df)

            # 7. Write
            path, summary_path = self.write_dataset(dataset_df)

            summary = {
                "status":         "OK" if not validation.get("blocked") else "BLOCKED",
                "mode":           self.mode,
                "feature_count":  snap_summary.get("feature_count", 0),
                "row_count":      len(dataset_df),
                "symbol_count":   dataset_df["symbol"].nunique() if "symbol" in dataset_df.columns else 0,
                "date_range":     snap_summary.get("date_range", ("", "")),
                "label_summary":  label_summary,
                "split_summary":  split_summary,
                "validation":     validation,
                "output_path":    path,
                "summary_path":   summary_path,
                "research_only":  True,
                "no_real_orders": True,
            }
            return dataset_df, summary

        except Exception as exc:
            logger.warning("MLFeatureDatasetBuilder.build_dataset: %s", exc)
            try:
                import pandas as pd
                return pd.DataFrame(), {"status": "ERROR", "error": str(exc)}
            except Exception:
                return None, {"status": "ERROR", "error": str(exc)}

    # ------------------------------------------------------------------
    # Join
    # ------------------------------------------------------------------

    def join_features_and_labels(self, features_df, labels_df):
        """
        Join features and labels DataFrames on [symbol, date].
        If labels_df is None, assumes labels are already in features_df.
        """
        try:
            if labels_df is None:
                return features_df
            import pandas as pd
            return features_df.merge(labels_df, on=["symbol", "date"], how="left", suffixes=("", "_label"))
        except Exception as exc:
            logger.warning("join_features_and_labels: %s", exc)
            return features_df

    # ------------------------------------------------------------------
    # Validate
    # ------------------------------------------------------------------

    def validate_dataset(self, df) -> dict:
        """
        Basic validation: check for required columns, label columns, split column.
        Returns {"ok": bool, "blocked": bool, "warnings": list}.
        """
        warnings = []
        blocked  = False
        try:
            required = {"symbol", "date"}
            missing  = required - set(df.columns)
            if missing:
                warnings.append(f"Missing required columns: {missing}")
                blocked = True

            label_cols = [c for c in df.columns if c.startswith("label_") or c.startswith("fwd_")]
            if not label_cols:
                warnings.append("No label columns found (label_* or fwd_*)")

            if "split" not in df.columns:
                warnings.append("No 'split' column found")

            feature_cols = [
                c for c in df.columns
                if c not in ("symbol", "date", "split")
                   and not c.startswith("label_")
                   and not c.startswith("fwd_")
                   and not c.startswith("meta_")
            ]
            if not feature_cols:
                warnings.append("No feature columns found")

            return {
                "ok":            not blocked,
                "blocked":       blocked,
                "feature_count": len(feature_cols),
                "label_count":   len(label_cols),
                "warnings":      warnings,
            }
        except Exception as exc:
            return {"ok": False, "blocked": True, "warnings": [str(exc)]}

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def write_dataset(self, df, name: Optional[str] = None) -> Tuple[str, str]:
        """Write dataset CSV and summary JSON. Returns (csv_path, summary_path)."""
        ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = name or "model_ready_dataset"
        csv_path  = os.path.join(self.output_root, f"{prefix}_{ts}.csv")
        json_path = os.path.join(self.output_root, f"{prefix}_summary_{ts}.json")
        try:
            if df is not None and not (hasattr(df, "empty") and df.empty):
                df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            summary = {
                "dataset_name":   prefix,
                "generated_at":   datetime.now().isoformat(),
                "mode":           self.mode,
                "output_path":    csv_path,
                "row_count":      len(df) if df is not None else 0,
                "research_only":  True,
                "no_real_orders": True,
                "not_committed":  True,
            }
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.warning("MLFeatureDatasetBuilder.write_dataset: %s", exc)
        return csv_path, json_path
