"""
strategies/momentum.py - Momentum strategy.

Each trading day, rank all stocks by a composite momentum score
(weighted sum of 1d/5d/20d returns + model predicted return) and buy the
top N stocks with equal weight.  Rebalances weekly (every 5 trading days).
"""

import logging
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from strategies.base import BaseStrategy

logger = logging.getLogger(__name__)


class MomentumStrategy(BaseStrategy):
    """
    Momentum strategy: rank stocks by composite score, buy top N.

    Score = w1 * ret_1d + w2 * ret_5d + w3 * ret_20d + w4 * predicted_return

    Rebalances every ``rebalance_freq`` trading days.
    """

    def __init__(
        self,
        top_n: int = None,
        rebalance_freq: int = None,
        ret_1d_weight: float = 0.1,
        ret_5d_weight: float = 0.2,
        ret_20d_weight: float = 0.3,
        pred_return_weight: float = 0.4,
    ):
        """
        Parameters
        ----------
        top_n : int
            Number of stocks to hold at any one time.
        rebalance_freq : int
            Rebalance every N trading days.
        ret_1d_weight, ret_5d_weight, ret_20d_weight, pred_return_weight : float
            Weights for each component of the composite score.
        """
        super().__init__(name="Momentum")
        self.top_n = top_n if top_n is not None else config.MOMENTUM_TOP_N
        self.rebalance_freq = rebalance_freq if rebalance_freq is not None else config.REBALANCE_FREQ
        self.ret_1d_weight = ret_1d_weight
        self.ret_5d_weight = ret_5d_weight
        self.ret_20d_weight = ret_20d_weight
        self.pred_return_weight = pred_return_weight

    def _compute_score(self, snapshot: pd.DataFrame) -> pd.Series:
        """
        Compute composite momentum score for each stock in the snapshot.

        Parameters
        ----------
        snapshot : pd.DataFrame
            One row per stock on the current date.

        Returns
        -------
        pd.Series
            Score indexed by the same index as snapshot.
        """
        score = pd.Series(0.0, index=snapshot.index)

        if "ret_1d" in snapshot.columns:
            score += self.ret_1d_weight * snapshot["ret_1d"].fillna(0)
        if "ret_5d" in snapshot.columns:
            score += self.ret_5d_weight * snapshot["ret_5d"].fillna(0)
        if "ret_20d" in snapshot.columns:
            score += self.ret_20d_weight * snapshot["ret_20d"].fillna(0)
        if "predicted_return" in snapshot.columns:
            score += self.pred_return_weight * snapshot["predicted_return"].fillna(0)

        return score

    def generate_signals(
        self,
        feature_snapshot: pd.DataFrame,
        positions: Dict[str, float],
        portfolio_value: float,
    ) -> List[Dict[str, Any]]:
        """
        Generate buy/sell signals based on momentum ranking.

        Logic:
        1. Compute score for all stocks.
        2. Select top-N by score.
        3. Sell stocks currently held that are no longer in top-N.
        4. Buy stocks in top-N that are not currently held.

        Parameters
        ----------
        feature_snapshot : pd.DataFrame
            Current-date feature rows, one per stock.
        positions : dict
            Currently held positions {stock_id: shares}.
        portfolio_value : float
            Total portfolio value.

        Returns
        -------
        list of signal dicts
        """
        signals = []

        if feature_snapshot.empty:
            return signals

        # Get the date from the snapshot for rebalance check
        if "date" in feature_snapshot.columns:
            current_date = pd.Timestamp(feature_snapshot["date"].iloc[0])
        else:
            current_date = pd.Timestamp("today")

        # Only rebalance on schedule
        if not self._needs_rebalance(current_date, self.rebalance_freq):
            return signals

        # Filter out stocks with insufficient data
        valid = feature_snapshot.dropna(subset=["ret_5d", "ret_20d"]) if "ret_5d" in feature_snapshot.columns else feature_snapshot.copy()

        if valid.empty:
            return signals

        scores = self._compute_score(valid)
        valid = valid.copy()
        valid["_score"] = scores.values

        # Rank and select top N
        top = valid.nlargest(self.top_n, "_score")
        top_ids = set(top["stock_id"].tolist()) if "stock_id" in top.columns else set()

        current_ids = set(sid for sid, qty in positions.items() if qty > 0)

        # Sell stocks no longer in top-N
        for stock_id in current_ids - top_ids:
            signals.append(
                self._make_signal(
                    stock_id=stock_id,
                    action="sell",
                    quantity=0,  # 0 = sell entire position
                    reason="Dropped out of momentum top-N",
                    score=0.0,
                )
            )

        # Buy new top-N stocks
        n_to_buy = len(top_ids - current_ids)
        if n_to_buy > 0 and portfolio_value > 0:
            per_stock_value = portfolio_value / self.top_n  # equal weight

        for _, row in top.iterrows():
            sid = row["stock_id"] if "stock_id" in row else str(row.name)
            if sid not in current_ids:
                close = row.get("close", None)
                if close and close > 0:
                    qty = per_stock_value / close
                else:
                    qty = 0
                signals.append(
                    self._make_signal(
                        stock_id=sid,
                        action="buy",
                        quantity=qty,
                        reason=f"Momentum top-{self.top_n} entry",
                        score=float(row["_score"]),
                    )
                )

        self._mark_rebalanced(current_date)
        return signals
