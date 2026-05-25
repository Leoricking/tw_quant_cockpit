"""
strategies/breakout.py - Breakout strategy.

Entry  : price breaks above 20-day high AND volume > 1.5x 20-day avg volume
Stop   : 2 × ATR below entry price
Target : 3 × ATR above entry price
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


class BreakoutStrategy(BaseStrategy):
    """
    Breakout strategy: buy on 20-day high breakout with volume confirmation.

    Tracks stop-loss and take-profit levels per position.
    """

    def __init__(
        self,
        lookback: int = None,
        volume_multiplier: float = None,
        atr_stop: float = None,
        atr_target: float = None,
    ):
        """
        Parameters
        ----------
        lookback : int
            Number of days for the high breakout lookback.
        volume_multiplier : float
            Minimum volume ratio (today / avg) to confirm breakout.
        atr_stop : float
            Stop-loss distance in ATR multiples below entry.
        atr_target : float
            Take-profit distance in ATR multiples above entry.
        """
        super().__init__(name="Breakout")
        self.lookback = lookback if lookback is not None else config.BREAKOUT_LOOKBACK
        self.volume_multiplier = (
            volume_multiplier if volume_multiplier is not None else config.BREAKOUT_VOLUME_MULTIPLIER
        )
        self.atr_stop = atr_stop if atr_stop is not None else config.ATR_STOP_MULTIPLIER
        self.atr_target = atr_target if atr_target is not None else config.ATR_TARGET_MULTIPLIER

        # Per-position tracking: {stock_id: {"stop": float, "target": float, "entry": float}}
        self._position_meta: Dict[str, Dict] = {}

    def reset(self) -> None:
        """Clear position metadata as well as base state."""
        super().reset()
        self._position_meta.clear()

    def _is_breakout(self, row: pd.Series) -> bool:
        """
        Return True if the stock's current price breaks the 20-day high
        with sufficient volume.
        """
        close = row.get("close", float("nan"))
        volume_spike = row.get("volume_spike", float("nan"))
        dist_from_20d_high = row.get("dist_from_20d_high", float("nan"))

        if pd.isna(close) or pd.isna(volume_spike):
            return False

        # dist_from_20d_high = (close - 20d_high) / 20d_high
        # A value >= 0 means close is AT or ABOVE the 20-day high
        price_breaks_high = (
            not pd.isna(dist_from_20d_high) and dist_from_20d_high >= 0
        )
        volume_confirm = volume_spike >= self.volume_multiplier

        return bool(price_breaks_high and volume_confirm)

    def _should_stop_or_target(self, stock_id: str, close: float) -> Optional[str]:
        """
        Check whether a position has hit its stop loss or take-profit target.

        Returns
        -------
        str or None
            "stop", "target", or None.
        """
        meta = self._position_meta.get(str(stock_id))
        if not meta:
            return None
        if close <= meta["stop"]:
            return "stop"
        if close >= meta["target"]:
            return "target"
        return None

    def generate_signals(
        self,
        feature_snapshot: pd.DataFrame,
        positions: Dict[str, float],
        portfolio_value: float,
    ) -> List[Dict[str, Any]]:
        """
        Generate breakout buy/sell signals.

        Parameters
        ----------
        feature_snapshot : pd.DataFrame
            One row per stock on the current date.
        positions : dict
            Currently held positions.
        portfolio_value : float

        Returns
        -------
        list of signal dicts
        """
        signals = []

        if feature_snapshot.empty:
            return signals

        for _, row in feature_snapshot.iterrows():
            sid = str(row.get("stock_id", ""))
            if not sid:
                continue

            close = row.get("close", float("nan"))
            atr = row.get("atr", float("nan"))
            held = positions.get(sid, 0)

            if pd.isna(close) or close <= 0:
                continue

            # ---- Exit: stop-loss / take-profit ----------------------------
            if held > 0:
                exit_reason = self._should_stop_or_target(sid, close)
                if exit_reason:
                    signals.append(
                        self._make_signal(
                            stock_id=sid,
                            action="sell",
                            quantity=0,
                            reason=f"Breakout exit: {exit_reason}",
                            score=0.0,
                        )
                    )
                    self._position_meta.pop(sid, None)

            # ---- Entry: breakout signal -----------------------------------
            elif held == 0 and self._is_breakout(row):
                if not pd.isna(atr) and atr > 0:
                    stop_price = close - self.atr_stop * atr
                    target_price = close + self.atr_target * atr
                else:
                    # Fallback: 2% stop / 3% target
                    stop_price = close * 0.98
                    target_price = close * 1.03

                # Position sizing via risk manager (rough estimate here)
                risk_amount = portfolio_value * config.RISK_PER_TRADE
                risk_per_share = close - stop_price
                if risk_per_share > 0:
                    qty = risk_amount / risk_per_share
                    # Cap at MAX_POSITION_SIZE
                    max_qty = (portfolio_value * config.MAX_POSITION_SIZE) / close
                    qty = min(qty, max_qty)
                else:
                    qty = 0

                if qty > 0:
                    self._position_meta[sid] = {
                        "entry": close,
                        "stop": stop_price,
                        "target": target_price,
                    }

                    volume_spike = row.get("volume_spike", float("nan"))
                    signals.append(
                        self._make_signal(
                            stock_id=sid,
                            action="buy",
                            quantity=qty,
                            reason=f"Breakout: price at 20d high, vol_spike={volume_spike:.2f}"
                            if not pd.isna(volume_spike)
                            else "Breakout entry",
                            score=float(row.get("volume_spike", 0)),
                        )
                    )

        return signals
