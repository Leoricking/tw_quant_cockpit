"""
backtest/validation_split.py — Walk-forward and out-of-sample validation split (v0.3.26).

[!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False
    logger.warning("pandas not available — ValidationSplit will operate in degraded mode")


class ValidationSplit:
    """
    Walk-forward and out-of-sample validation split for backtest hardening.

    Methods:
    - walk_forward: rolling train/test windows
    - out_of_sample: single train/test split at oos_ratio cutoff
    - expanding_window: growing training window, fixed test window
    - in_sample_only: full range as both train and test

    [!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only = True
    no_real_orders = True
    production_blocked = True

    VALID_METHODS = ("walk_forward", "out_of_sample", "expanding_window", "in_sample_only")

    def __init__(
        self,
        method: str = "walk_forward",
        train_window_days: int = 252,
        test_window_days: int = 63,
        step_days: int = 21,
        oos_ratio: float = 0.3,
    ) -> None:
        if method not in self.VALID_METHODS:
            logger.warning("Unknown split method '%s', defaulting to 'walk_forward'", method)
            method = "walk_forward"
        self.method = method
        self.train_window_days = train_window_days
        self.test_window_days = test_window_days
        self.step_days = step_days
        self.oos_ratio = max(0.1, min(0.5, oos_ratio))

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def split(self, price_df) -> list[dict]:
        """
        Generate splits based on the configured method.

        price_df: DataFrame with DatetimeIndex or 'date' column.
        Returns list of split dicts.
        """
        dates = self._extract_dates(price_df)
        if not dates:
            logger.warning("ValidationSplit.split: no dates available")
            return self.in_sample_only([])

        if self.method == "walk_forward":
            return self.walk_forward_splits(dates)
        elif self.method == "out_of_sample":
            return self.out_of_sample_split(dates)
        elif self.method == "expanding_window":
            return self.expanding_window_splits(dates)
        elif self.method == "in_sample_only":
            return self.in_sample_only(dates)
        else:
            return self.walk_forward_splits(dates)

    # ------------------------------------------------------------------
    # Walk-forward
    # ------------------------------------------------------------------

    def walk_forward_splits(self, dates: list) -> list[dict]:
        """
        Generate rolling train/test windows stepping by step_days.

        Returns at minimum 1 split even if data is short.
        """
        if not dates:
            return [self._make_split(0, None, None, None, None, "walk_forward", warning="no_dates")]

        dates = sorted(set(str(d) for d in dates))
        n = len(dates)
        splits = []
        split_id = 0

        train_w = min(self.train_window_days, n - 1)
        test_w = min(self.test_window_days, max(1, n - train_w))
        step = max(1, self.step_days)

        start_idx = 0
        while start_idx + train_w + test_w <= n:
            train_start = dates[start_idx]
            train_end = dates[start_idx + train_w - 1]
            test_start = dates[start_idx + train_w]
            test_end_idx = min(start_idx + train_w + test_w - 1, n - 1)
            test_end = dates[test_end_idx]

            splits.append(self._make_split(
                split_id, train_start, train_end, test_start, test_end, "walk_forward"
            ))
            split_id += 1
            start_idx += step

        if not splits:
            # Data too short — return one split covering everything
            logger.warning("walk_forward_splits: data too short, returning single fallback split")
            mid = n // 2
            train_start = dates[0]
            train_end = dates[mid - 1] if mid > 0 else dates[0]
            test_start = dates[mid] if mid < n else dates[-1]
            test_end = dates[-1]
            splits.append(self._make_split(
                0, train_start, train_end, test_start, test_end, "walk_forward",
                warning="data_too_short"
            ))

        return splits

    # ------------------------------------------------------------------
    # Out-of-sample
    # ------------------------------------------------------------------

    def out_of_sample_split(self, dates: list) -> list[dict]:
        """Split at (1 - oos_ratio) cutoff."""
        if not dates:
            return [self._make_split(0, None, None, None, None, "out_of_sample", warning="no_dates")]

        dates = sorted(set(str(d) for d in dates))
        n = len(dates)
        cutoff = max(1, int(n * (1.0 - self.oos_ratio)))
        cutoff = min(cutoff, n - 1)

        train_start = dates[0]
        train_end = dates[cutoff - 1]
        test_start = dates[cutoff]
        test_end = dates[-1]

        return [self._make_split(0, train_start, train_end, test_start, test_end, "out_of_sample")]

    # ------------------------------------------------------------------
    # Expanding window
    # ------------------------------------------------------------------

    def expanding_window_splits(self, dates: list) -> list[dict]:
        """Growing training window, fixed test window."""
        if not dates:
            return [self._make_split(0, None, None, None, None, "expanding_window", warning="no_dates")]

        dates = sorted(set(str(d) for d in dates))
        n = len(dates)
        splits = []
        split_id = 0

        test_w = min(self.test_window_days, max(1, n // 4))
        step = max(1, self.step_days)
        min_train = min(self.train_window_days, n - test_w)

        start_test = min_train
        while start_test + test_w <= n:
            train_start = dates[0]
            train_end = dates[start_test - 1]
            test_start = dates[start_test]
            test_end_idx = min(start_test + test_w - 1, n - 1)
            test_end = dates[test_end_idx]

            splits.append(self._make_split(
                split_id, train_start, train_end, test_start, test_end, "expanding_window"
            ))
            split_id += 1
            start_test += step

        if not splits:
            return self.in_sample_only(dates)

        return splits

    # ------------------------------------------------------------------
    # In-sample only
    # ------------------------------------------------------------------

    def in_sample_only(self, dates: list) -> list[dict]:
        """Return one split covering full range as both train and test."""
        if not dates:
            return [self._make_split(0, None, None, None, None, "in_sample_only", warning="no_dates")]

        dates = sorted(set(str(d) for d in dates))
        return [self._make_split(
            0, dates[0], dates[-1], dates[0], dates[-1], "in_sample_only",
            warning="in_sample_only_overfitting_risk"
        )]

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def build_assumption_dict(self) -> dict:
        """Return all model parameters as a dictionary for reporting."""
        return {
            "method": self.method,
            "train_window_days": self.train_window_days,
            "test_window_days": self.test_window_days,
            "step_days": self.step_days,
            "oos_ratio": self.oos_ratio,
            "read_only": self.read_only,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _extract_dates(self, price_df) -> list:
        """Extract sorted date strings from a DataFrame."""
        if not _PANDAS_AVAILABLE:
            return []
        if price_df is None:
            return []
        try:
            if hasattr(price_df, "index"):
                if isinstance(price_df.index, pd.DatetimeIndex):
                    return [str(d.date()) for d in price_df.index]
                elif hasattr(price_df, "columns") and "date" in price_df.columns:
                    return sorted(price_df["date"].astype(str).tolist())
                else:
                    return sorted([str(i) for i in price_df.index])
            return []
        except Exception as exc:
            logger.error("_extract_dates error: %s", exc)
            return []

    @staticmethod
    def _make_split(
        split_id: int,
        train_start,
        train_end,
        test_start,
        test_end,
        split_type: str,
        warning: str | None = None,
    ) -> dict:
        result = {
            "split_id": split_id,
            "train_start": train_start,
            "train_end": train_end,
            "test_start": test_start,
            "test_end": test_end,
            "split_type": split_type,
        }
        if warning:
            result["warning"] = warning
        return result
