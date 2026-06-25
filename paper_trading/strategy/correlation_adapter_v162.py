"""
paper_trading/strategy/correlation_adapter_v162.py — Correlation/exposure adapter for Paper Strategy Orchestration v1.6.2.
Integrates with v1.5.2 correlation/exposure module.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_DEFAULT_MAX_CORR_BREACH_COUNT = 1   # block if 1 or more tickers breach


class CorrelationAdapter:
    """
    Checks paper portfolio correlation/exposure limits before approving a signal.

    Integrates with portfolio.correlation (v1.5.2) when available.
    Falls back to a permissive pass-through when unavailable.

    [!] Research-only. No real portfolio is inspected.
    [!] Correlation breaches block the signal in the decision pipeline.
    """

    def __init__(
        self,
        max_correlation: float = 0.85,
        max_sector_exposure: float = 0.40,
        use_portfolio_correlation: bool = True,
    ) -> None:
        self.max_correlation = max_correlation
        self.max_sector_exposure = max_sector_exposure
        self.use_portfolio_correlation = use_portfolio_correlation
        self._available: Optional[bool] = None
        self._check_count: int = 0
        self._breach_count: int = 0
        self._fallback_count: int = 0

    def _check_available(self) -> bool:
        if self._available is None:
            try:
                from portfolio import correlation  # noqa: F401
                self._available = True
            except ImportError:
                self._available = False
                logger.info(
                    "[v1.6.2][correlation] portfolio.correlation not available — using permissive fallback"
                )
        return self._available

    def check_breach(
        self,
        ticker: str,
        open_tickers: Optional[List[str]] = None,
        sector: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Return True if adding ticker would breach correlation/exposure limits.

        [!] Research-only simulation check. No real portfolio data.
        """
        self._check_count += 1
        open_tickers = open_tickers or []

        if self.use_portfolio_correlation and self._check_available():
            try:
                from portfolio.correlation import check_correlation_breach
                breach = check_correlation_breach(
                    ticker=ticker,
                    open_tickers=open_tickers,
                    max_correlation=self.max_correlation,
                    max_sector_exposure=self.max_sector_exposure,
                    sector=sector,
                    paper_only=True,
                )
                if breach:
                    self._breach_count += 1
                    logger.debug(
                        "[v1.6.2][correlation] Breach detected for %s", ticker
                    )
                return breach
            except Exception as exc:
                logger.warning(
                    "[v1.6.2][correlation] Check error for %s: %s — permissive fallback",
                    ticker, exc
                )
                self._fallback_count += 1
                return False

        # Permissive fallback — no breach
        self._fallback_count += 1
        return False

    def stats(self) -> Dict[str, Any]:
        return {
            "check_count": self._check_count,
            "breach_count": self._breach_count,
            "fallback_count": self._fallback_count,
            "max_correlation": self.max_correlation,
            "max_sector_exposure": self.max_sector_exposure,
            "portfolio_correlation_available": self._available,
            "paper_only": True,
            "research_only": True,
        }
