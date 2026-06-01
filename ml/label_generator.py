"""
ml/label_generator.py — ML Label Generator (v0.4.2).

Generates forward-return labels, classification labels, and triple-barrier labels.
Labels use future price data — they must ALWAYS be in separate label columns,
never mixed with feature columns.

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] Labels are for research only. Not for live prediction. Not for auto-trading.
"""
from __future__ import annotations

import logging
from typing import Optional, Sequence, Tuple

logger = logging.getLogger(__name__)

# Default thresholds
_DEFAULT_UP_THRESHOLDS   = {5: 0.03, 10: 0.05, 20: 0.08}
_DEFAULT_DOWN_THRESHOLDS = {5: -0.03, 10: -0.05, 20: -0.08}

# Triple barrier defaults
_TRIPLE_BARRIER_UPPER = 0.05
_TRIPLE_BARRIER_LOWER = -0.03
_TRIPLE_BARRIER_HORIZON = 10


class LabelGenerator:
    """
    ML Label Generator.

    Generates:
        - fwd_return_{N}d          : forward returns
        - label_up_{N}d_{X}pct     : threshold classification
        - label_down_{N}d_{X}pct   : threshold classification
        - label_direction_{N}d     : binary direction (1=up, 0=down)
        - label_triple_barrier_10d : triple barrier {1, 0, -1}
        - label_max_drawdown_10d   : max drawdown in 10-day horizon
        - label_max_runup_10d      : max run-up in 10-day horizon

    [!] Labels use future data — keep strictly separated from features.
    [!] Research only. No live prediction. No real orders.
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        horizons: Sequence[int] = (1, 5, 10, 20),
        up_thresholds:   Optional[dict] = None,
        down_thresholds: Optional[dict] = None,
        use_next_open:   bool = False,
    ):
        self.horizons        = list(horizons)
        self.up_thresholds   = up_thresholds   or _DEFAULT_UP_THRESHOLDS
        self.down_thresholds = down_thresholds or _DEFAULT_DOWN_THRESHOLDS
        self.use_next_open   = use_next_open

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def generate(self, price_df) -> Tuple[object, dict]:
        """
        Generate all labels for a price DataFrame.

        Parameters
        ----------
        price_df : pd.DataFrame with at least columns: date, symbol, close
                   Optionally: high, low, open

        Returns
        -------
        (label_df, summary)
        """
        try:
            import pandas as pd

            df = price_df.copy()
            df = df.sort_values(["symbol", "date"]).reset_index(drop=True)

            # Forward returns
            df = self.generate_forward_return_labels(df)

            # Classification labels (5d default)
            df = self.generate_classification_labels(df)

            # Triple barrier (10d)
            df = self.generate_triple_barrier_labels(df)

            # Summary
            label_cols = [c for c in df.columns if c.startswith("fwd_") or c.startswith("label_")]
            summary = self._build_summary(df, label_cols)

            return df, summary

        except Exception as exc:
            logger.warning("LabelGenerator.generate: %s", exc)
            return price_df, {"error": str(exc), "label_columns": []}

    # ------------------------------------------------------------------
    # Forward returns
    # ------------------------------------------------------------------

    def generate_forward_return_labels(self, df):
        """Add fwd_return_{N}d columns. Uses future close prices — label only."""
        try:
            import pandas as pd

            for h in self.horizons:
                col = f"fwd_return_{h}d"
                df[col] = (
                    df.groupby("symbol")["close"]
                    .transform(lambda x: x.shift(-h) / x - 1)
                )
        except Exception as exc:
            logger.warning("generate_forward_return_labels: %s", exc)
        return df

    # ------------------------------------------------------------------
    # Classification labels
    # ------------------------------------------------------------------

    def generate_classification_labels(self, df):
        """
        Generate:
          - label_direction_{N}d (1=up, 0=down/flat)
          - label_up_{N}d_{X}pct and label_down_{N}d_{X}pct for configured thresholds
        """
        try:
            import numpy as np

            # Direction (5d by default, all horizons)
            for h in self.horizons:
                fwd_col = f"fwd_return_{h}d"
                if fwd_col not in df.columns:
                    continue
                df[f"label_direction_{h}d"] = (df[fwd_col] > 0).astype("Int64")

            # Threshold labels (5d main)
            for h in [5]:
                fwd_col = f"fwd_return_{h}d"
                if fwd_col not in df.columns:
                    continue
                up_thresh   = self.up_thresholds.get(h, 0.03)
                down_thresh = self.down_thresholds.get(h, -0.03)
                up_pct   = int(abs(up_thresh) * 100)
                down_pct = int(abs(down_thresh) * 100)
                df[f"label_up_{h}d_{up_pct}pct"]   = (df[fwd_col] >= up_thresh).astype("Int64")
                df[f"label_down_{h}d_{down_pct}pct"] = (df[fwd_col] <= down_thresh).astype("Int64")

        except Exception as exc:
            logger.warning("generate_classification_labels: %s", exc)
        return df

    # ------------------------------------------------------------------
    # Triple barrier
    # ------------------------------------------------------------------

    def generate_triple_barrier_labels(
        self,
        df,
        horizon:     int   = _TRIPLE_BARRIER_HORIZON,
        upper_pct:   float = _TRIPLE_BARRIER_UPPER,
        lower_pct:   float = _TRIPLE_BARRIER_LOWER,
    ):
        """
        Triple barrier label:
            +1 if upper barrier (+upper_pct) hit first within horizon
            -1 if lower barrier (lower_pct, negative) hit first within horizon
             0 if neither hit within horizon

        Also generates:
            label_max_drawdown_{horizon}d
            label_max_runup_{horizon}d
        """
        try:
            import pandas as pd
            import numpy as np

            results_tb  = []
            results_mdd = []
            results_mru = []

            close_arr = df["close"].values
            symbol_arr = df["symbol"].values
            n = len(df)

            for i in range(n):
                entry_price = close_arr[i]
                sym = symbol_arr[i]
                if entry_price is None or entry_price == 0 or (hasattr(entry_price, '__class__') and entry_price != entry_price):
                    results_tb.append(None)
                    results_mdd.append(None)
                    results_mru.append(None)
                    continue

                # Gather same-symbol forward prices
                forward_prices = []
                for j in range(i + 1, min(i + 1 + horizon, n)):
                    if symbol_arr[j] != sym:
                        break
                    forward_prices.append(close_arr[j])

                if not forward_prices:
                    results_tb.append(None)
                    results_mdd.append(None)
                    results_mru.append(None)
                    continue

                upper = entry_price * (1 + upper_pct)
                lower = entry_price * (1 + lower_pct)

                tb_label = 0
                max_dd   = 0.0
                max_ru   = 0.0

                for fp in forward_prices:
                    ret = (fp - entry_price) / entry_price
                    if ret < max_dd:
                        max_dd = ret
                    if ret > max_ru:
                        max_ru = ret
                    if tb_label == 0:
                        if fp >= upper:
                            tb_label = 1
                        elif fp <= lower:
                            tb_label = -1

                results_tb.append(tb_label)
                results_mdd.append(round(max_dd, 6))
                results_mru.append(round(max_ru, 6))

            df[f"label_triple_barrier_{horizon}d"] = results_tb
            df[f"label_max_drawdown_{horizon}d"]   = results_mdd
            df[f"label_max_runup_{horizon}d"]       = results_mru

        except Exception as exc:
            logger.warning("generate_triple_barrier_labels: %s", exc)
        return df

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def _build_summary(self, df, label_cols: list) -> dict:
        try:
            import pandas as pd
            summary: dict = {
                "horizons":      self.horizons,
                "label_columns": label_cols,
                "row_count":     len(df),
                "label_balance": {},
            }
            for col in label_cols:
                if col not in df.columns:
                    continue
                s = df[col].dropna()
                if s.empty:
                    continue
                if col.startswith("label_direction") or col.startswith("label_up") or col.startswith("label_down"):
                    vc = s.value_counts(normalize=True)
                    summary["label_balance"][col] = {str(k): round(float(v), 4) for k, v in vc.items()}
                elif col.startswith("label_triple_barrier"):
                    vc = s.value_counts()
                    summary["label_balance"][col] = {str(k): int(v) for k, v in vc.items()}
                else:
                    summary["label_balance"][col] = {
                        "mean":  round(float(s.mean()), 6),
                        "std":   round(float(s.std()), 6),
                        "count": int(s.count()),
                    }
            return summary
        except Exception as exc:
            logger.warning("LabelGenerator._build_summary: %s", exc)
            return {"label_columns": label_cols, "error": str(exc)}
