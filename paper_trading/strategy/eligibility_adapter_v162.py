"""
paper_trading/strategy/eligibility_adapter_v162.py — Eligibility adapter for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Set

from paper_trading.strategy.enums_v162 import EligibilityResult

logger = logging.getLogger(__name__)

# Tickers explicitly blocked for any research signal (e.g. suspended, delisted)
_DEFAULT_BLOCKED_TICKERS: Set[str] = set()


class EligibilityAdapter:
    """
    Checks whether a ticker is eligible for a paper signal evaluation.

    Research-only. Does NOT connect to any real market feed or broker API.
    Eligibility is determined by:
      - Explicit block list (suspended/delisted tickers)
      - Explicit allow list (if set, only these are eligible)
      - Minimum confidence threshold

    [!] This is a simulation adapter. Results do NOT reflect real market eligibility.
    """

    def __init__(
        self,
        blocked_tickers: Optional[Set[str]] = None,
        allowed_tickers: Optional[Set[str]] = None,
        min_confidence: float = 0.0,
    ) -> None:
        self._blocked: Set[str] = set(blocked_tickers or _DEFAULT_BLOCKED_TICKERS)
        self._allowed: Optional[Set[str]] = set(allowed_tickers) if allowed_tickers else None
        self.min_confidence = min_confidence
        self._check_count: int = 0
        self._eligible_count: int = 0
        self._ineligible_count: int = 0

    def check(
        self,
        ticker: str,
        confidence: float = 1.0,
        extra: Optional[Dict[str, Any]] = None,
    ) -> EligibilityResult:
        """
        Return EligibilityResult for a ticker.
        UNCERTAIN is returned when eligibility cannot be definitively determined.
        """
        self._check_count += 1

        if ticker in self._blocked:
            logger.debug("[v1.6.2][eligibility] %s BLOCKED (explicit block list)", ticker)
            self._ineligible_count += 1
            return EligibilityResult.INELIGIBLE

        if self._allowed is not None and ticker not in self._allowed:
            logger.debug("[v1.6.2][eligibility] %s INELIGIBLE (not in allow list)", ticker)
            self._ineligible_count += 1
            return EligibilityResult.INELIGIBLE

        if confidence < self.min_confidence:
            logger.debug(
                "[v1.6.2][eligibility] %s INELIGIBLE (confidence %.2f < min %.2f)",
                ticker, confidence, self.min_confidence
            )
            self._ineligible_count += 1
            return EligibilityResult.INELIGIBLE

        logger.debug("[v1.6.2][eligibility] %s ELIGIBLE", ticker)
        self._eligible_count += 1
        return EligibilityResult.ELIGIBLE

    def block_ticker(self, ticker: str) -> None:
        self._blocked.add(ticker)

    def unblock_ticker(self, ticker: str) -> None:
        self._blocked.discard(ticker)

    def set_allow_list(self, tickers: List[str]) -> None:
        self._allowed = set(tickers)

    def clear_allow_list(self) -> None:
        self._allowed = None

    def is_blocked(self, ticker: str) -> bool:
        return ticker in self._blocked

    def stats(self) -> Dict[str, Any]:
        return {
            "check_count": self._check_count,
            "eligible_count": self._eligible_count,
            "ineligible_count": self._ineligible_count,
            "blocked_tickers": sorted(self._blocked),
            "allow_list_size": len(self._allowed) if self._allowed is not None else None,
            "min_confidence": self.min_confidence,
            "paper_only": True,
            "research_only": True,
        }
