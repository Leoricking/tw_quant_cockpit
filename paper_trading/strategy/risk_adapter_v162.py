"""
paper_trading/strategy/risk_adapter_v162.py — Risk controls adapter for Paper Strategy Orchestration v1.6.2.
Integrates with v1.5.3 drawdown/risk controls + v1.5.9 portfolio stable rollup.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class RiskAdapter:
    """
    Applies risk control gates before approving a paper signal.

    Integrates with portfolio.risk_controls (v1.5.3) and portfolio.drawdown (v1.5.9)
    when available. Falls back to permissive mode when unavailable.

    Risk blocks:
      - Max drawdown breach
      - Position count limit
      - Daily loss limit
      - Volatility spike gate

    [!] Research-only. No real portfolio is inspected.
    [!] A risk block causes RISK_BLOCKED outcome in the pipeline.
    """

    def __init__(
        self,
        max_drawdown_pct: float = 0.15,
        max_positions: int = 20,
        max_daily_loss_pct: float = 0.05,
        max_volatility_multiplier: float = 3.0,
        use_portfolio_risk: bool = True,
    ) -> None:
        self.max_drawdown_pct = max_drawdown_pct
        self.max_positions = max_positions
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_volatility_multiplier = max_volatility_multiplier
        self.use_portfolio_risk = use_portfolio_risk
        self._available: Optional[bool] = None
        self._check_count: int = 0
        self._block_count: int = 0
        self._fallback_count: int = 0
        self._block_reasons: List[str] = []

    def _check_available(self) -> bool:
        if self._available is None:
            try:
                from portfolio import risk_controls  # noqa: F401
                self._available = True
            except ImportError:
                self._available = False
                logger.info(
                    "[v1.6.2][risk] portfolio.risk_controls not available — permissive fallback"
                )
        return self._available

    def is_blocked(
        self,
        ticker: str,
        current_drawdown_pct: float = 0.0,
        open_position_count: int = 0,
        daily_loss_pct: float = 0.0,
        volatility_multiplier: float = 1.0,
        extra: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Return True if the risk controls block this signal.
        Records blocking reasons for diagnostics.

        [!] Research-only simulation check. Not connected to real risk system.
        """
        self._check_count += 1

        if self.use_portfolio_risk and self._check_available():
            try:
                from portfolio.risk_controls import check_risk_block
                blocked, reason = check_risk_block(
                    ticker=ticker,
                    current_drawdown_pct=current_drawdown_pct,
                    max_drawdown_pct=self.max_drawdown_pct,
                    open_position_count=open_position_count,
                    max_positions=self.max_positions,
                    daily_loss_pct=daily_loss_pct,
                    max_daily_loss_pct=self.max_daily_loss_pct,
                    paper_only=True,
                )
                if blocked:
                    self._block_count += 1
                    self._block_reasons.append(reason)
                    logger.debug("[v1.6.2][risk] Blocked %s: %s", ticker, reason)
                return blocked
            except Exception as exc:
                logger.warning(
                    "[v1.6.2][risk] Check error for %s: %s — permissive fallback", ticker, exc
                )
                self._fallback_count += 1
                return False

        # Local heuristic checks (fallback)
        reasons: List[str] = []
        if current_drawdown_pct > self.max_drawdown_pct:
            reasons.append(f"drawdown {current_drawdown_pct:.1%} > max {self.max_drawdown_pct:.1%}")
        if open_position_count >= self.max_positions:
            reasons.append(f"positions {open_position_count} >= max {self.max_positions}")
        if daily_loss_pct > self.max_daily_loss_pct:
            reasons.append(f"daily_loss {daily_loss_pct:.1%} > max {self.max_daily_loss_pct:.1%}")
        if volatility_multiplier > self.max_volatility_multiplier:
            reasons.append(f"vol_multiplier {volatility_multiplier:.1f} > max {self.max_volatility_multiplier:.1f}")

        if reasons:
            self._block_count += 1
            self._block_reasons.extend(reasons)
            logger.debug("[v1.6.2][risk] Blocked %s (local): %s", ticker, "; ".join(reasons))
            return True

        self._fallback_count += 1
        return False

    def stats(self) -> Dict[str, Any]:
        return {
            "check_count": self._check_count,
            "block_count": self._block_count,
            "fallback_count": self._fallback_count,
            "recent_block_reasons": self._block_reasons[-5:],
            "max_drawdown_pct": self.max_drawdown_pct,
            "max_positions": self.max_positions,
            "max_daily_loss_pct": self.max_daily_loss_pct,
            "portfolio_risk_available": self._available,
            "paper_only": True,
            "research_only": True,
        }
