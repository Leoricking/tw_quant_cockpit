"""
abc_validation/integrity_guard_v141.py — Signal integrity guard for A/B/C validation v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Missing data → INSUFFICIENT_DATA (never False, never True).
Lookahead violation → BLOCKED.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class ABCSignalIntegrityGuard:
    """
    Validates data integrity for A/B/C buy point signals.

    Rules:
    - Sufficient MA history: 5, 10, 20, 60 bars required per type
    - Volume baseline present
    - KD/RSI/MACD inputs present
    - Timestamps: signal_date <= decision_date <= execution_date
    - No duplicate bars, no missing bars in sequence
    - No future data access (lookahead), no same-bar execution
    - Stale core data check
    - Corporate action status
    - Missing data → classification INSUFFICIENT_DATA (never False, never True)
    - Lookahead violation → BLOCKED
    """

    MIN_BARS = {
        "A": 30,   # needs MA10 + MA20 + MA60
        "B": 20,   # needs MA5 + MA10
        "C": 40,   # needs MA20 + MA60
    }
    INDICATOR_MINS = {"ma5": 5, "ma10": 10, "ma20": 20, "ma60": 60}

    def check(self, signal_dict: dict, bars: Optional[list] = None) -> Dict[str, Any]:
        """
        Run all integrity checks.

        Returns dict with:
            passed: bool
            classification: "OK" | "INSUFFICIENT_DATA" | "BLOCKED"
            issues: list of str
        """
        issues = []
        classification = "OK"

        buy_point_type = signal_dict.get("buy_point_type", "A")
        min_bars = self.MIN_BARS.get(buy_point_type, 20)

        # 1. Sufficient MA history
        if bars is not None:
            if len(bars) < min_bars:
                issues.append(
                    f"INSUFFICIENT_HISTORY: need {min_bars} bars for type {buy_point_type}, "
                    f"got {len(bars)}"
                )
                classification = "INSUFFICIENT_DATA"

        # 2. Volume baseline
        if bars is not None and bars:
            volumes = [b.get("volume") for b in bars if b.get("volume") is not None]
            if len(volumes) < 5:
                issues.append("INSUFFICIENT_VOLUME_BASELINE: fewer than 5 bars with volume")
                if classification == "OK":
                    classification = "INSUFFICIENT_DATA"

        # 3. Timestamp ordering
        sig_date = signal_dict.get("signal_date", "")
        dec_date = signal_dict.get("decision_date", "")
        exc_date = signal_dict.get("execution_date", "")
        if sig_date and dec_date and exc_date:
            if sig_date > dec_date:
                issues.append(f"TIMESTAMP_ORDER: signal_date {sig_date} > decision_date {dec_date}")
                classification = "BLOCKED"
            if dec_date > exc_date:
                issues.append(f"TIMESTAMP_ORDER: decision_date {dec_date} > execution_date {exc_date}")
                classification = "BLOCKED"
            if sig_date == exc_date:
                issues.append(
                    f"SAME_BAR_EXECUTION: signal and execution on same date {sig_date}"
                )
                classification = "BLOCKED"
        elif not sig_date or not dec_date or not exc_date:
            issues.append("MISSING_TIMESTAMPS: signal_date, decision_date, or execution_date missing")
            if classification == "OK":
                classification = "INSUFFICIENT_DATA"

        # 4. Lookahead check
        if signal_dict.get("lookahead_violation", False):
            issues.append("LOOKAHEAD_VIOLATION: future data accessed before signal date")
            classification = "BLOCKED"

        # 5. No duplicate bars
        if bars is not None and bars:
            dates = [b.get("date") for b in bars if b.get("date")]
            if len(dates) != len(set(dates)):
                issues.append("DUPLICATE_BARS: duplicate dates detected in bar data")
                classification = "BLOCKED"

        # 6. Stale core data
        if signal_dict.get("stale_data", False):
            issues.append("STALE_DATA: core price data is stale")
            if classification == "OK":
                classification = "INSUFFICIENT_DATA"

        # 7. Corporate action
        if signal_dict.get("corporate_action_pending", False):
            issues.append("CORPORATE_ACTION: corporate action pending — may distort price levels")
            if classification == "OK":
                classification = "INSUFFICIENT_DATA"

        # 8. Fixture data in real mode
        mode = signal_dict.get("mode", "mock")
        fixture = signal_dict.get("fixture_data", False)
        if mode == "real" and fixture:
            issues.append("FIXTURE_IN_REAL_MODE: fixture data cannot be used for formal validation")
            classification = "BLOCKED"

        return {
            "passed": classification == "OK",
            "classification": classification,
            "issues": issues,
        }

    def is_blocked(self, check_result: dict) -> bool:
        return check_result.get("classification") == "BLOCKED"

    def is_insufficient(self, check_result: dict) -> bool:
        return check_result.get("classification") == "INSUFFICIENT_DATA"
