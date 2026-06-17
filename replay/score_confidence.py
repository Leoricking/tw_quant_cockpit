"""
replay/score_confidence.py — ReplayScoreConfidence for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Single entry: OBSERVATIONAL.
[!] Missing data: INSUFFICIENT.
[!] entries < 10: INSUFFICIENT.
[!] entries 10-29: OBSERVATIONAL.
[!] entries >= 30 AND sessions >= 10: RELIABLE (unless over-concentrated).
[!] Mock: DEMO_ONLY.
[!] Real mode never falls back to mock.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayScoreConfidence:
    """
    Determines confidence level for replay scores.

    [!] Single entry: OBSERVATIONAL.
    [!] Missing data: INSUFFICIENT.
    [!] Mock: DEMO_ONLY (labeled).
    [!] Real mode never falls back to mock.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    # Thresholds
    INSUFFICIENT_ENTRIES = 10
    OBSERVATIONAL_ENTRIES = 30
    RELIABLE_SESSIONS = 10
    OVER_CONCENTRATED_PCT = 0.80   # > 80% same symbol → over-concentrated

    def assess(
        self,
        entry_count: int = 0,
        session_count: int = 0,
        is_mock: bool = False,
        symbol_distribution: Optional[Dict[str, int]] = None,
        notes: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Return (confidence_level, note).
        confidence_level: DEMO_ONLY | INSUFFICIENT | OBSERVATIONAL | RELIABLE
        """
        if is_mock:
            return "DEMO_ONLY", (
                "Mock mode: scores are DEMO_ONLY. Not a real research conclusion. "
                "Real mode never falls back to mock."
            )

        if entry_count == 0 or entry_count is None:
            return "INSUFFICIENT", (
                "No entries available for confidence assessment. INSUFFICIENT."
            )

        if entry_count == 1:
            return "OBSERVATIONAL", (
                "Single entry: OBSERVATIONAL only. Not a pattern conclusion."
            )

        if entry_count < self.INSUFFICIENT_ENTRIES:
            return "INSUFFICIENT", (
                f"entries={entry_count} < {self.INSUFFICIENT_ENTRIES}: INSUFFICIENT. "
                "More sessions required."
            )

        if entry_count < self.OBSERVATIONAL_ENTRIES:
            return "OBSERVATIONAL", (
                f"entries={entry_count} ({self.INSUFFICIENT_ENTRIES}-{self.OBSERVATIONAL_ENTRIES - 1}): "
                "OBSERVATIONAL. Not statistically reliable."
            )

        # >= 30 entries — check session count and concentration
        if session_count < self.RELIABLE_SESSIONS:
            return "OBSERVATIONAL", (
                f"entries={entry_count} but sessions={session_count} < "
                f"{self.RELIABLE_SESSIONS}: OBSERVATIONAL."
            )

        # Check for over-concentration
        if symbol_distribution:
            total = sum(symbol_distribution.values())
            if total > 0:
                max_pct = max(symbol_distribution.values()) / total
                if max_pct > self.OVER_CONCENTRATED_PCT:
                    top_symbol = max(symbol_distribution, key=lambda k: symbol_distribution[k])
                    return "OBSERVATIONAL", (
                        f"Over-concentrated: {top_symbol} = {max_pct:.0%} of entries. "
                        "Diversify sessions for RELIABLE confidence."
                    )

        return "RELIABLE", (
            f"entries={entry_count} >= {self.OBSERVATIONAL_ENTRIES}, "
            f"sessions={session_count} >= {self.RELIABLE_SESSIONS}: RELIABLE. "
            "[!] Research Only. Not Investment Advice."
        )

    def assess_single(self, is_mock: bool = False) -> Tuple[str, str]:
        """Convenience method for a single score."""
        return self.assess(entry_count=1, is_mock=is_mock)

    def safety_note(self) -> str:
        return (
            "[!] Score confidence is for research training purposes only. "
            "RELIABLE does not mean trading-ready. Not Investment Advice. "
            "Mock scores are always DEMO_ONLY. Real mode never falls back to mock."
        )
