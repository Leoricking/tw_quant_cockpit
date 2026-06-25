"""
paper_trading/strategy/sizing_adapter_v162.py — Position sizing adapter for Paper Strategy Orchestration v1.6.2.
Integrates with v1.5.1 position sizing module.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from paper_trading.strategy.models_v162 import PaperSignal

logger = logging.getLogger(__name__)

_FALLBACK_FIXED_SIZE = 100.0    # default paper position size when no sizing model available
_MAX_PAPER_SIZE = 10000.0       # hard cap: no paper position exceeds this


class SizingAdapter:
    """
    Computes a suggested position size for a paper signal.

    Integrates with portfolio.sizing (v1.5.1) when available.
    Falls back to fixed_size when the sizing module is unavailable.

    [!] Sizes are RESEARCH ONLY. They do not represent real portfolio positions.
    [!] No real capital is allocated. This is a paper simulation.
    """

    def __init__(
        self,
        fixed_size: float = _FALLBACK_FIXED_SIZE,
        max_size: float = _MAX_PAPER_SIZE,
        use_portfolio_sizing: bool = True,
    ) -> None:
        assert fixed_size > 0, "fixed_size must be positive"
        assert max_size > 0, "max_size must be positive"
        self.fixed_size = fixed_size
        self.max_size = max_size
        self.use_portfolio_sizing = use_portfolio_sizing
        self._sizing_available: Optional[bool] = None
        self._call_count: int = 0
        self._fallback_count: int = 0

    def _check_sizing_available(self) -> bool:
        if self._sizing_available is None:
            try:
                from portfolio import sizing  # noqa: F401
                self._sizing_available = True
            except ImportError:
                self._sizing_available = False
                logger.info(
                    "[v1.6.2][sizing] portfolio.sizing not available — using fixed_size=%.1f",
                    self.fixed_size
                )
        return self._sizing_available

    def compute(
        self,
        signal: PaperSignal,
        portfolio_value: float = 0.0,
        current_position: float = 0.0,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Optional[float]:
        """
        Compute a suggested paper position size for the signal.

        Returns None if no size can be computed (e.g. risk veto).
        Returns a positive float (shares/units) otherwise.

        [!] This is a paper simulation — no real capital is allocated.
        """
        self._call_count += 1
        size: Optional[float] = None

        if self.use_portfolio_sizing and self._check_sizing_available():
            try:
                from portfolio.sizing import compute_position_size
                size = compute_position_size(
                    ticker=signal.ticker,
                    signal_strength=signal.strength,
                    confidence=signal.confidence,
                    portfolio_value=portfolio_value,
                    current_position=current_position,
                    paper_only=True,
                )
                logger.debug(
                    "[v1.6.2][sizing] portfolio.sizing returned %.2f for %s",
                    size or 0, signal.ticker
                )
            except Exception as exc:
                logger.warning(
                    "[v1.6.2][sizing] portfolio.sizing error for %s: %s — using fallback",
                    signal.ticker, exc
                )
                size = None

        if size is None:
            size = self.fixed_size * signal.confidence
            self._fallback_count += 1

        # Clamp to max_size
        if size is not None:
            size = min(size, self.max_size)
            size = max(0.0, size)

        return size

    def stats(self) -> Dict[str, Any]:
        return {
            "call_count": self._call_count,
            "fallback_count": self._fallback_count,
            "fixed_size": self.fixed_size,
            "max_size": self.max_size,
            "portfolio_sizing_available": self._sizing_available,
            "paper_only": True,
            "research_only": True,
        }
