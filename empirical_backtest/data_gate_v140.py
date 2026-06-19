"""
empirical_backtest/data_gate_v140.py — Data Gate for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations


class StrategyBacktestDataGate:
    """Validates data before allowing a formal backtest."""

    def validate(self, data: dict, config: dict = None) -> dict:
        block_reasons = []
        warnings = []
        data_mode = data.get("data_mode", "unknown")

        # Blocks
        if data_mode in ("mock", "demo", "fixture", "DEMO_ONLY", "TEST_FIXTURE"):
            block_reasons.append(
                "MOCK_DATA_BLOCKED: Mock/Demo/Fixture data cannot be used for formal backtest"
            )

        if data.get("is_fixture") is True:
            block_reasons.append("FIXTURE_BLOCKED")

        for price in data.get("close_prices", []):
            if price <= 0:
                block_reasons.append("INVALID_CLOSE_PRICE")
                break

        if data.get("has_duplicate_bars") is True:
            block_reasons.append("DUPLICATE_BARS_NOT_HANDLED")

        if data.get("missing_bar_pct", 0) > 0.05:
            block_reasons.append("SEVERE_MISSING_BARS")

        if data.get("has_future_timestamp") is True:
            block_reasons.append("FUTURE_TIMESTAMP_DETECTED")

        if data.get("has_lookahead_timestamp") is True:
            block_reasons.append("LOOKAHEAD_TIMESTAMP_DETECTED")

        if (
            data.get("corporate_action_status") == "UNKNOWN"
            and data.get("crosses_corporate_action") is True
        ):
            block_reasons.append("CORPORATE_ACTION_UNKNOWN")

        if data.get("source") in (None, "", "unknown", "UNKNOWN"):
            block_reasons.append("UNKNOWN_DATA_SOURCE")

        if data.get("freshness_status") in ("STALE", "CRITICALLY_STALE", "NEVER_RECEIVED"):
            block_reasons.append("STALE_CORE_DATA")

        if data.get("bar_count", 0) < data.get("minimum_history_bars", 20):
            block_reasons.append("INSUFFICIENT_HISTORY")

        if data.get("has_source_conflict") is True:
            block_reasons.append("SOURCE_CONFLICT")

        # Warnings
        if data.get("corporate_action_status") == "UNADJUSTED":
            warnings.append("Data is unadjusted — long-term return accuracy may be affected")

        if data.get("survivorship_risk") is True:
            warnings.append("SURVIVORSHIP_RISK: Universe built from current survivors")

        blocked = len(block_reasons) > 0
        passed = not blocked

        quality_score = 100 if passed else max(0, 100 - len(block_reasons) * 20)

        return {
            "passed": passed,
            "blocked": blocked,
            "block_reasons": block_reasons,
            "warnings": warnings,
            "data_mode": data_mode,
            "quality_score": quality_score,
        }
