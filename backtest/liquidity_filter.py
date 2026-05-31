"""
backtest/liquidity_filter.py — Liquidity filter for hardened backtest (v0.3.26).

[!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)


class LiquidityFilter:
    """
    Liquidity filter for backtest trade entry validation.

    Checks minimum daily volume, minimum daily turnover, and maximum
    participation rate to ensure simulated trades are realistic.

    [!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only = True
    no_real_orders = True
    production_blocked = True

    def __init__(
        self,
        min_daily_volume: float = 500,
        min_daily_turnover: float = 10_000_000,
        max_participation_rate: float = 0.05,
    ) -> None:
        self.min_daily_volume = min_daily_volume
        self.min_daily_turnover = min_daily_turnover
        self.max_participation_rate = max_participation_rate

    # ------------------------------------------------------------------
    # Main check
    # ------------------------------------------------------------------

    def check_entry_allowed(
        self,
        row: dict,
        trade_value: float | None = None,
    ) -> dict:
        """
        Check whether a trade entry is allowed given liquidity constraints.

        Args:
            row: dict with keys 'volume' and 'close'
            trade_value: optional trade size in NTD

        Returns:
            allowed, liquidity_score, warning, rejection_reason
        """
        rejection_reason = None
        warnings = []

        try:
            volume = self._safe_float(row.get("volume"))
            close = self._safe_float(row.get("close"))
            turnover = (close * volume) if (close is not None and volume is not None) else None

            # Volume check
            if volume is None:
                rejection_reason = "volume data missing"
                return self._build_result(False, 0.0, "volume missing", rejection_reason)

            if volume < self.min_daily_volume:
                rejection_reason = (
                    f"volume {volume:.0f} < min_daily_volume {self.min_daily_volume:.0f}"
                )
                score = self.calculate_liquidity_score(row)
                return self._build_result(False, score, None, rejection_reason)

            # Turnover check
            if turnover is None:
                warnings.append("close missing; turnover not computed")
            elif turnover < self.min_daily_turnover:
                rejection_reason = (
                    f"turnover {turnover:,.0f} < min_daily_turnover {self.min_daily_turnover:,.0f}"
                )
                score = self.calculate_liquidity_score(row)
                return self._build_result(False, score, None, rejection_reason)

            # Participation rate check
            if trade_value is not None and turnover is not None and turnover > 0:
                participation = trade_value / turnover
                if participation > self.max_participation_rate:
                    rejection_reason = (
                        f"participation {participation:.1%} > max {self.max_participation_rate:.1%}"
                    )
                    score = self.calculate_liquidity_score(row)
                    return self._build_result(False, score, None, rejection_reason)
                elif participation > self.max_participation_rate * 0.5:
                    warnings.append(
                        f"participation {participation:.1%} approaching limit {self.max_participation_rate:.1%}"
                    )

            score = self.calculate_liquidity_score(row)
            warning = "; ".join(warnings) if warnings else None
            return self._build_result(True, score, warning, None)

        except Exception as exc:
            logger.error("check_entry_allowed error: %s", exc)
            return self._build_result(False, 0.0, f"error: {exc}", "internal_error")

    # ------------------------------------------------------------------
    # Score
    # ------------------------------------------------------------------

    def calculate_liquidity_score(self, row: dict) -> float:
        """
        Calculate a 0–100 liquidity score.

        100 if all checks pass; proportional degradation otherwise.
        """
        try:
            volume = self._safe_float(row.get("volume"))
            close = self._safe_float(row.get("close"))
            turnover = (close * volume) if (close is not None and volume is not None) else None

            score = 100.0

            if volume is None:
                return 0.0

            # Volume component (40 pts)
            if volume < self.min_daily_volume:
                vol_score = 40.0 * (volume / self.min_daily_volume)
            else:
                vol_score = 40.0

            # Turnover component (60 pts)
            if turnover is None:
                turn_score = 30.0  # partial credit if close missing
            elif turnover < self.min_daily_turnover:
                turn_score = 60.0 * (turnover / self.min_daily_turnover)
            else:
                turn_score = 60.0

            score = vol_score + turn_score
            return round(max(0.0, min(100.0, score)), 2)

        except Exception as exc:
            logger.error("calculate_liquidity_score error: %s", exc)
            return 0.0

    # ------------------------------------------------------------------
    # Explanation
    # ------------------------------------------------------------------

    def explain_rejection(self, row: dict) -> str:
        """Return a human-readable rejection reason."""
        result = self.check_entry_allowed(row)
        if result["allowed"]:
            return "No rejection — trade allowed"
        if result["rejection_reason"]:
            return f"Rejected: {result['rejection_reason']}"
        return "Rejected: unknown reason"

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def build_assumption_dict(self) -> dict:
        """Return all model parameters as a dictionary for reporting."""
        return {
            "min_daily_volume": self.min_daily_volume,
            "min_daily_turnover": self.min_daily_turnover,
            "max_participation_rate": self.max_participation_rate,
            "read_only": self.read_only,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _safe_float(val) -> float | None:
        """Safely convert a value to float."""
        if val is None:
            return None
        try:
            f = float(val)
            if f != f:  # NaN check without numpy
                return None
            return f
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _build_result(
        allowed: bool,
        score: float,
        warning: str | None,
        rejection_reason: str | None,
    ) -> dict:
        return {
            "allowed": allowed,
            "liquidity_score": score,
            "warning": warning,
            "rejection_reason": rejection_reason,
        }
