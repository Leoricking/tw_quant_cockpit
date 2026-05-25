"""
strategies/mean_reversion.py - Mean reversion strategy.

Entry condition : RSI(14) < 30 AND close < lower Bollinger Band
Exit condition  : RSI > 55 OR close crosses above SMA20
Max positions   : 15
"""

import logging
from typing import Any, Dict, List, Optional

import pandas as pd
import numpy as np

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from strategies.base import BaseStrategy

logger = logging.getLogger(__name__)


class MeanReversionStrategy(BaseStrategy):
    """
    Mean reversion strategy based on RSI and Bollinger Band oversold signals.

    - Buy when RSI < 30 AND price < lower Bollinger Band.
    - Sell when RSI > 55 OR price > SMA20.
    - Maximum ``max_positions`` open at a time.
    """

    def __init__(
        self,
        rsi_buy_threshold: float = None,
        rsi_sell_threshold: float = 55.0,
        max_positions: int = None,
    ):
        """
        Parameters
        ----------
        rsi_buy_threshold : float
            RSI level below which a stock is considered oversold.
        rsi_sell_threshold : float
            RSI level above which a position is closed.
        max_positions : int
            Maximum number of simultaneous open positions.
        """
        super().__init__(name="MeanReversion")
        self.rsi_buy_threshold = (
            rsi_buy_threshold if rsi_buy_threshold is not None else config.RSI_OVERSOLD
        )
        self.rsi_sell_threshold = rsi_sell_threshold
        self.max_positions = (
            max_positions if max_positions is not None else config.MEAN_REVERSION_MAX_POS
        )

    def _is_oversold(self, row: pd.Series) -> bool:
        """Return True if the stock meets the oversold entry criteria."""
        rsi = row.get("rsi_14", float("nan"))
        bb_position = row.get("bb_position", float("nan"))  # (close - lower) / (upper - lower)
        close = row.get("close", float("nan"))
        bb_lower = row.get("bb_lower", float("nan"))

        if pd.isna(rsi) or pd.isna(close):
            return False

        rsi_cond = rsi < self.rsi_buy_threshold

        # Use bb_lower if available, fallback to bb_position
        if not pd.isna(bb_lower):
            bb_cond = close < bb_lower
        elif not pd.isna(bb_position):
            bb_cond = bb_position < 0  # below lower band
        else:
            bb_cond = False

        return bool(rsi_cond and bb_cond)

    def _should_exit(self, row: pd.Series) -> bool:
        """Return True if an existing position should be closed."""
        rsi = row.get("rsi_14", float("nan"))
        close = row.get("close", float("nan"))
        sma20 = row.get("sma_20", float("nan"))

        if pd.isna(rsi) or pd.isna(close):
            return False

        rsi_exit = rsi > self.rsi_sell_threshold

        if not pd.isna(sma20):
            price_exit = close > sma20
        else:
            price_exit = False

        return bool(rsi_exit or price_exit)

    def generate_signals(
        self,
        feature_snapshot: pd.DataFrame,
        positions: Dict[str, float],
        portfolio_value: float,
    ) -> List[Dict[str, Any]]:
        """
        Generate mean reversion buy/sell signals.

        Parameters
        ----------
        feature_snapshot : pd.DataFrame
            One row per stock, current date.
        positions : dict
            {stock_id: shares_held}
        portfolio_value : float
            Current portfolio value.

        Returns
        -------
        list of signal dicts
        """
        signals = []

        if feature_snapshot.empty:
            return signals

        current_long_count = sum(1 for qty in positions.values() if qty > 0)

        for _, row in feature_snapshot.iterrows():
            sid = row.get("stock_id", None)
            if sid is None:
                continue

            held = positions.get(str(sid), 0)
            close = row.get("close", float("nan"))

            # ---- Exit logic ------------------------------------------------
            if held > 0 and self._should_exit(row):
                signals.append(
                    self._make_signal(
                        stock_id=str(sid),
                        action="sell",
                        quantity=0,  # sell all
                        reason=f"Mean reversion exit: RSI={row.get('rsi_14', 'N/A'):.1f}"
                        if not pd.isna(row.get("rsi_14", float("nan")))
                        else "Mean reversion exit",
                        score=float(row.get("rsi_14", 50)),
                    )
                )

            # ---- Entry logic -----------------------------------------------
            elif held == 0 and current_long_count < self.max_positions:
                if self._is_oversold(row) and not pd.isna(close) and close > 0:
                    # Determine quantity: equal allocation per position
                    alloc = portfolio_value / self.max_positions
                    qty = alloc / close

                    rsi_val = row.get("rsi_14", float("nan"))
                    score = float(self.rsi_buy_threshold - rsi_val) if not pd.isna(rsi_val) else 0.0

                    signals.append(
                        self._make_signal(
                            stock_id=str(sid),
                            action="buy",
                            quantity=qty,
                            reason=f"Oversold entry: RSI={rsi_val:.1f}, below BB lower"
                            if not pd.isna(rsi_val)
                            else "Oversold entry",
                            score=score,
                        )
                    )
                    current_long_count += 1

        return signals
