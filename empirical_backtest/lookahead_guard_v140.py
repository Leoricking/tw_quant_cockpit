"""
empirical_backtest/lookahead_guard_v140.py — Lookahead Bias Guard for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations


class LookaheadBiasGuard:
    """Checks signals for lookahead bias violations."""

    def check(self, signal: dict, data_context: dict = None) -> dict:
        violations = []
        warnings = []

        # Violations (blocking)
        if signal.get("same_bar_close_execution") is True and not signal.get("explicitly_not_conservative"):
            violations.append(
                "SAME_BAR_CLOSE_EXECUTION: Signal generated from close price cannot be filled "
                "at same bar's close without explicit non-conservative flag"
            )

        if signal.get("has_future_bar_access") is True:
            violations.append("FUTURE_BAR_ACCESS_DETECTED")

        if signal.get("uses_financial_before_release_date") is True:
            violations.append("FINANCIAL_DATA_BEFORE_RELEASE")

        if signal.get("uses_revenue_before_release_date") is True:
            violations.append("MONTHLY_REVENUE_BEFORE_RELEASE")

        if signal.get("uses_future_universe_membership") is True:
            violations.append("FUTURE_UNIVERSE_MEMBERSHIP")

        if signal.get("uses_survivor_only_universe") is True and not signal.get("survivorship_bias_flagged"):
            violations.append("SURVIVORSHIP_BIAS_NOT_FLAGGED")

        # Warnings (non-blocking)
        if signal.get("institutional_data_delay_days", 0) < 1:
            warnings.append("Institutional data may not account for publication delay")

        passed = len(violations) == 0

        return {
            "passed": passed,
            "violations": violations,
            "warnings": warnings,
        }
