"""
backtest/gap_risk_model.py — Gap risk model for hardened backtest (v0.3.26).

[!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)


class GapRiskModel:
    """
    Gap risk model for Taiwan stock backtesting.

    Taiwan stocks have daily price limits (typically ±10%), meaning gaps
    can cause stop-loss orders to execute at worse prices than intended.

    Classifications:
    - NO_GAP: normal overnight change
    - GAP_UP_WARNING / GAP_UP_BLOCK: upside gap
    - GAP_DOWN_WARNING / GAP_DOWN_STOP: downside gap (stop-loss cannot execute at intended price)

    [!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only = True
    no_real_orders = True
    production_blocked = True

    # Gap classification labels
    NO_GAP = "NO_GAP"
    GAP_UP_WARNING = "GAP_UP_WARNING"
    GAP_UP_BLOCK = "GAP_UP_BLOCK"
    GAP_DOWN_WARNING = "GAP_DOWN_WARNING"
    GAP_DOWN_STOP = "GAP_DOWN_STOP"
    UNKNOWN = "UNKNOWN"

    def __init__(
        self,
        gap_warning_pct: float = 0.03,
        gap_block_pct: float = 0.06,
        no_chase_gap_pct: float = 0.04,
    ) -> None:
        self.gap_warning_pct = gap_warning_pct
        self.gap_block_pct = gap_block_pct
        self.no_chase_gap_pct = no_chase_gap_pct

    # ------------------------------------------------------------------
    # Gap calculation
    # ------------------------------------------------------------------

    def calculate_gap(
        self,
        previous_close: float | None,
        next_open: float | None,
    ) -> float:
        """
        Calculate the gap percentage between previous close and next open.

        Returns (next_open - previous_close) / previous_close.
        Returns 0.0 if either value is None or zero.
        """
        try:
            if previous_close is None or next_open is None:
                return 0.0
            if float(previous_close) == 0.0:
                return 0.0
            return (float(next_open) - float(previous_close)) / float(previous_close)
        except (TypeError, ValueError, ZeroDivisionError):
            return 0.0

    # ------------------------------------------------------------------
    # Gap classification
    # ------------------------------------------------------------------

    def classify_gap(self, gap_pct: float) -> str:
        """
        Classify a gap percentage into a category.

        Returns one of: NO_GAP, GAP_UP_WARNING, GAP_UP_BLOCK,
                        GAP_DOWN_WARNING, GAP_DOWN_STOP, UNKNOWN
        """
        try:
            gap = float(gap_pct)
        except (TypeError, ValueError):
            return self.UNKNOWN

        if abs(gap) < self.gap_warning_pct:
            return self.NO_GAP
        elif gap >= self.gap_block_pct:
            return self.GAP_UP_BLOCK
        elif self.gap_warning_pct <= gap < self.gap_block_pct:
            return self.GAP_UP_WARNING
        elif gap <= -self.gap_block_pct:
            return self.GAP_DOWN_STOP
        elif -self.gap_block_pct < gap <= -self.gap_warning_pct:
            return self.GAP_DOWN_WARNING
        else:
            return self.UNKNOWN

    # ------------------------------------------------------------------
    # Entry blocking
    # ------------------------------------------------------------------

    def should_block_entry(
        self,
        gap_pct: float,
        signal_type: str | None = None,
    ) -> bool:
        """
        Determine if entry should be blocked due to gap risk.

        Blocks on:
        - GAP_UP_BLOCK (chasing a large gap-up)
        - GAP_DOWN_STOP (gap down exceeds stop threshold)
        - abs(gap_pct) >= no_chase_gap_pct
        """
        try:
            gap = float(gap_pct)
        except (TypeError, ValueError):
            return False

        classification = self.classify_gap(gap)

        if classification in (self.GAP_UP_BLOCK, self.GAP_DOWN_STOP):
            return True

        if abs(gap) >= self.no_chase_gap_pct:
            return True

        return False

    # ------------------------------------------------------------------
    # Gap stop loss
    # ------------------------------------------------------------------

    def apply_gap_stop_loss(
        self,
        entry_price: float,
        next_open: float,
        stop_price: float,
    ) -> dict:
        """
        Apply gap stop-loss logic.

        If next_open < stop_price, the gap stop is triggered and the effective
        exit is next_open (cannot exit at a better price when gapped through).

        Returns:
            gap_stop_triggered, effective_exit, gap_pct
        """
        try:
            gap_pct = self.calculate_gap(entry_price, next_open)

            if next_open < stop_price:
                return {
                    "gap_stop_triggered": True,
                    "effective_exit": float(next_open),
                    "gap_pct": round(gap_pct, 6),
                }
            else:
                return {
                    "gap_stop_triggered": False,
                    "effective_exit": None,
                    "gap_pct": round(gap_pct, 6),
                }
        except Exception as exc:
            logger.error("apply_gap_stop_loss error: %s", exc)
            return {
                "gap_stop_triggered": False,
                "effective_exit": None,
                "gap_pct": 0.0,
            }

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def build_assumption_dict(self) -> dict:
        """Return all model parameters as a dictionary for reporting."""
        return {
            "gap_warning_pct": self.gap_warning_pct,
            "gap_block_pct": self.gap_block_pct,
            "no_chase_gap_pct": self.no_chase_gap_pct,
            "taiwan_context": "Taiwan stocks have ±10% daily price limits; gap-through stop loss common",
            "read_only": self.read_only,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
        }
