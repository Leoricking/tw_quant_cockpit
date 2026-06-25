"""
paper_trading/strategy/conflict_resolution_v162.py — Conflict resolution for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

from paper_trading.strategy.enums_v162 import ConflictPolicy, SignalStrength, SignalType
from paper_trading.strategy.models_v162 import PaperSignal

logger = logging.getLogger(__name__)

_STRENGTH_ORDER = {
    SignalStrength.STRONG.value:   4,
    SignalStrength.MODERATE.value: 3,
    SignalStrength.WEAK.value:     2,
    SignalStrength.NEUTRAL.value:  1,
}

# Conservative priority: prefer EXIT > BLOCK > REDUCE > HOLD > ENTRY
_CONSERVATIVE_PRIORITY = {
    SignalType.BLOCK.value:           5,
    SignalType.EXIT_LONG.value:       4,
    SignalType.REDUCE_RESEARCH.value: 3,
    SignalType.HOLD.value:            2,
    SignalType.ALERT.value:           1,
    SignalType.ENTRY_LONG.value:      0,
}


class ConflictResolver:
    """
    Resolves conflicts when multiple paper signals target the same ticker.

    Policies (default: MOST_CONSERVATIVE):
      MOST_CONSERVATIVE — prefer EXIT/BLOCK over ENTRY; highest defensive priority wins
      FIRST_WINS        — first signal in list wins
      HIGHEST_STRENGTH  — signal with highest strength wins
      LATEST_WINS       — last signal in list wins
      BLOCK_ALL         — any conflict → reject all signals

    [!] Research-only. No real portfolio state is consulted.
    """

    def __init__(self, policy: ConflictPolicy = ConflictPolicy.MOST_CONSERVATIVE) -> None:
        self.policy = policy
        self._conflict_count: int = 0
        self._resolved_count: int = 0

    def has_conflict(self, signals: List[PaperSignal]) -> bool:
        """Return True if multiple signals target the same ticker."""
        tickers = [s.ticker for s in signals]
        return len(tickers) != len(set(tickers))

    def conflicting_tickers(self, signals: List[PaperSignal]) -> List[str]:
        """Return list of tickers that have more than one signal."""
        from collections import Counter
        counts = Counter(s.ticker for s in signals)
        return [t for t, c in counts.items() if c > 1]

    def resolve(self, signals: List[PaperSignal]) -> Tuple[List[PaperSignal], List[str]]:
        """
        Resolve conflicts among a list of signals.
        Returns (resolved_signals, conflict_log).

        Non-conflicting signals pass through unchanged.
        Conflicting signals are resolved per policy.
        """
        if not self.has_conflict(signals):
            return list(signals), []

        self._conflict_count += 1
        conflict_log: List[str] = []
        conflicting = set(self.conflicting_tickers(signals))
        resolved: List[PaperSignal] = []

        # Separate conflicting from clean
        clean = [s for s in signals if s.ticker not in conflicting]
        resolved.extend(clean)

        for ticker in conflicting:
            competing = [s for s in signals if s.ticker == ticker]
            log_msg = (
                f"Conflict on {ticker}: {len(competing)} signals "
                f"({[s.signal_type for s in competing]})"
            )
            conflict_log.append(log_msg)
            logger.debug("[v1.6.2][conflict] %s", log_msg)

            winner = self._pick_winner(competing, ticker)
            if winner is not None:
                resolved.append(winner)
                self._resolved_count += 1
                conflict_log.append(
                    f"Resolved {ticker}: winner={winner.signal_type} "
                    f"policy={self.policy.value}"
                )

        return resolved, conflict_log

    def _pick_winner(
        self, competing: List[PaperSignal], ticker: str
    ) -> Optional[PaperSignal]:
        if not competing:
            return None

        if self.policy == ConflictPolicy.BLOCK_ALL:
            logger.debug("[v1.6.2][conflict] BLOCK_ALL: all %s signals rejected", ticker)
            return None

        if self.policy == ConflictPolicy.FIRST_WINS:
            return competing[0]

        if self.policy == ConflictPolicy.LATEST_WINS:
            return competing[-1]

        if self.policy == ConflictPolicy.HIGHEST_STRENGTH:
            return max(
                competing,
                key=lambda s: (_STRENGTH_ORDER.get(s.strength, 0), s.confidence)
            )

        # Default: MOST_CONSERVATIVE
        return max(
            competing,
            key=lambda s: (
                _CONSERVATIVE_PRIORITY.get(s.signal_type, 0),
                _STRENGTH_ORDER.get(s.strength, 0),
            )
        )

    def stats(self) -> Dict[str, Any]:
        return {
            "policy": self.policy.value,
            "conflict_count": self._conflict_count,
            "resolved_count": self._resolved_count,
            "paper_only": True,
            "research_only": True,
        }
