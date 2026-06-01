"""
ml/split_manager.py — ML Train/Validation/Test Split Manager (v0.4.2).

Default: time-series split (no random split to prevent data leakage).
Random split is available but emits a leakage risk warning.

[!] ML Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

SPLIT_TRAIN      = "train"
SPLIT_VALIDATION = "validation"
SPLIT_TEST       = "test"
SPLIT_OOS        = "oos"


class MLSplitManager:
    """
    Train / Validation / Test split manager.

    Methods:
        assign_splits(dataset_df)  — main entry; returns df with 'split' column
        time_series_split(df)
        symbol_grouped_split(df)
        walk_forward_split(df)

    [!] Default: time_series split (no future data leak).
    [!] Random split will warn about leakage risk.
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        method:           str   = "time_series",
        train_ratio:      float = 0.6,
        validation_ratio: float = 0.2,
        test_ratio:       float = 0.2,
        walk_forward:     bool  = False,
        n_folds:          int   = 5,
    ):
        self.method           = method
        self.train_ratio      = train_ratio
        self.validation_ratio = validation_ratio
        self.test_ratio       = test_ratio
        self.walk_forward     = walk_forward
        self.n_folds          = n_folds

        if abs(train_ratio + validation_ratio + test_ratio - 1.0) > 0.01:
            logger.warning("MLSplitManager: ratios do not sum to 1.0 — using as-is")

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def assign_splits(self, dataset_df) -> tuple:
        """
        Assign split labels to dataset.

        Returns (df_with_split_column, summary_dict).
        """
        try:
            if self.walk_forward:
                return self.walk_forward_split(dataset_df)
            if self.method == "time_series":
                return self.time_series_split(dataset_df)
            if self.method == "symbol_grouped":
                return self.symbol_grouped_split(dataset_df)
            if self.method == "random":
                logger.warning(
                    "MLSplitManager: random split requested — DATA LEAKAGE RISK. "
                    "Use time_series split for time-series data."
                )
                return self._random_split(dataset_df)
            # fallback
            logger.warning("MLSplitManager: unknown method '%s' — falling back to time_series", self.method)
            return self.time_series_split(dataset_df)
        except Exception as exc:
            logger.warning("MLSplitManager.assign_splits: %s", exc)
            return dataset_df, {"error": str(exc)}

    # ------------------------------------------------------------------
    # Time-series split (default)
    # ------------------------------------------------------------------

    def time_series_split(self, df) -> tuple:
        """
        Split by date rank — earliest dates → train, next → validation, last → test.
        Prevents any future data leaking into earlier splits.
        """
        try:
            import pandas as pd

            df = df.copy()
            if "date" not in df.columns:
                raise ValueError("'date' column required for time_series_split")

            dates = df["date"].sort_values().unique()
            n = len(dates)
            train_end = int(n * self.train_ratio)
            val_end   = int(n * (self.train_ratio + self.validation_ratio))

            train_dates = set(dates[:train_end])
            val_dates   = set(dates[train_end:val_end])
            test_dates  = set(dates[val_end:])

            def _assign(d):
                if d in train_dates:
                    return SPLIT_TRAIN
                if d in val_dates:
                    return SPLIT_VALIDATION
                return SPLIT_TEST

            df["split"] = df["date"].map(_assign)

            summary = self._build_summary(df, dates, train_end, val_end)
            return df, summary

        except Exception as exc:
            logger.warning("MLSplitManager.time_series_split: %s", exc)
            return df, {"error": str(exc)}

    # ------------------------------------------------------------------
    # Symbol-grouped split
    # ------------------------------------------------------------------

    def symbol_grouped_split(self, df) -> tuple:
        """
        Assign train/validation/test by date within each symbol group.
        Each symbol is split independently by its own date range.
        """
        try:
            import pandas as pd

            df = df.copy()
            if "date" not in df.columns or "symbol" not in df.columns:
                raise ValueError("'date' and 'symbol' columns required for symbol_grouped_split")

            splits = []
            for sym, grp in df.groupby("symbol"):
                dates = grp["date"].sort_values().unique()
                n = len(dates)
                t_end = int(n * self.train_ratio)
                v_end = int(n * (self.train_ratio + self.validation_ratio))
                td = set(dates[:t_end])
                vd = set(dates[t_end:v_end])

                for idx, row in grp.iterrows():
                    d = row["date"]
                    if d in td:
                        splits.append((idx, SPLIT_TRAIN))
                    elif d in vd:
                        splits.append((idx, SPLIT_VALIDATION))
                    else:
                        splits.append((idx, SPLIT_TEST))

            idx_list, split_list = zip(*splits) if splits else ([], [])
            import pandas as pd
            split_s = pd.Series(split_list, index=idx_list)
            df["split"] = split_s

            summary = {
                "method":        "symbol_grouped",
                "train_ratio":   self.train_ratio,
                "val_ratio":     self.validation_ratio,
                "test_ratio":    self.test_ratio,
                "split_counts":  df["split"].value_counts().to_dict() if "split" in df.columns else {},
            }
            return df, summary

        except Exception as exc:
            logger.warning("MLSplitManager.symbol_grouped_split: %s", exc)
            return df, {"error": str(exc)}

    # ------------------------------------------------------------------
    # Walk-forward split
    # ------------------------------------------------------------------

    def walk_forward_split(self, df) -> tuple:
        """
        Walk-forward split: assigns fold labels walk_forward_fold_1..N.
        Each fold: train on all data before fold window, test on fold window.
        """
        try:
            import pandas as pd
            import numpy as np

            df = df.copy()
            if "date" not in df.columns:
                raise ValueError("'date' column required for walk_forward_split")

            dates = sorted(df["date"].unique())
            n = len(dates)
            fold_size = max(1, n // self.n_folds)

            df["split"] = SPLIT_TRAIN  # default

            fold_summaries = []
            for fold_idx in range(self.n_folds):
                start_i = fold_idx * fold_size
                end_i   = min(start_i + fold_size, n)
                fold_dates = set(dates[start_i:end_i])
                fold_label = f"walk_forward_fold_{fold_idx + 1}"
                mask = df["date"].isin(fold_dates)
                df.loc[mask, "split"] = fold_label
                fold_summaries.append({
                    "fold":       fold_idx + 1,
                    "start_date": str(dates[start_i]) if start_i < n else "",
                    "end_date":   str(dates[min(end_i - 1, n - 1)]) if end_i > 0 else "",
                    "rows":       int(mask.sum()),
                })

            summary = {
                "method":       "walk_forward",
                "n_folds":      self.n_folds,
                "folds":        fold_summaries,
                "split_counts": df["split"].value_counts().to_dict() if "split" in df.columns else {},
            }
            return df, summary

        except Exception as exc:
            logger.warning("MLSplitManager.walk_forward_split: %s", exc)
            return df, {"error": str(exc)}

    # ------------------------------------------------------------------
    # Random split (leakage warning)
    # ------------------------------------------------------------------

    def _random_split(self, df) -> tuple:
        """Random split — LEAKAGE RISK for time-series data."""
        try:
            import pandas as pd
            import numpy as np

            df = df.copy()
            n = len(df)
            idx = np.random.permutation(n)
            t_end = int(n * self.train_ratio)
            v_end = int(n * (self.train_ratio + self.validation_ratio))

            splits = [SPLIT_TEST] * n
            for i in idx[:t_end]:
                splits[i] = SPLIT_TRAIN
            for i in idx[t_end:v_end]:
                splits[i] = SPLIT_VALIDATION

            df["split"] = splits
            summary = {
                "method":            "random",
                "leakage_warning":   "RANDOM_SPLIT_RISK — use time_series split for time-series data",
                "split_counts":      df["split"].value_counts().to_dict(),
            }
            return df, summary
        except Exception as exc:
            logger.warning("MLSplitManager._random_split: %s", exc)
            return df, {"error": str(exc)}

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def _build_summary(self, df, dates, train_end: int, val_end: int) -> dict:
        try:
            n = len(dates)
            counts = df["split"].value_counts().to_dict() if "split" in df.columns else {}
            return {
                "method":               "time_series",
                "train_ratio":          self.train_ratio,
                "validation_ratio":     self.validation_ratio,
                "test_ratio":           self.test_ratio,
                "total_dates":          n,
                "train_dates":          train_end,
                "validation_dates":     max(0, val_end - train_end),
                "test_dates":           max(0, n - val_end),
                "train_date_range":     (str(dates[0]), str(dates[min(train_end - 1, n - 1)])) if train_end > 0 else ("", ""),
                "validation_date_range":(str(dates[train_end]), str(dates[min(val_end - 1, n - 1)])) if val_end > train_end else ("", ""),
                "test_date_range":      (str(dates[val_end]),   str(dates[-1])) if val_end < n else ("", ""),
                "split_row_counts":     counts,
            }
        except Exception as exc:
            return {"error": str(exc)}
