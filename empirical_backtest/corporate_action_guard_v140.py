"""
empirical_backtest/corporate_action_guard_v140.py — Corporate Action Guard for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from .models_v140 import CorporateActionStatus


class CorporateActionGuard:
    """Checks corporate action data quality for backtesting."""

    def check(self, symbol_data: dict) -> dict:
        notes = []
        status = symbol_data.get("corporate_action_status", CorporateActionStatus.UNKNOWN)
        blocked = False
        passed = False

        if status in (CorporateActionStatus.ADJUSTED, CorporateActionStatus.NOT_APPLICABLE):
            passed = True
            blocked = False
        elif status == CorporateActionStatus.UNKNOWN:
            if symbol_data.get("crosses_corporate_action") is True:
                blocked = True
                notes.append(
                    "Corporate action status UNKNOWN across corporate event — formal backtest blocked"
                )
        elif status == CorporateActionStatus.UNADJUSTED:
            blocked = False
            passed = False
            notes.append(
                "Data is unadjusted — price jumps from corporate actions may distort returns"
            )
        elif status == CorporateActionStatus.PARTIALLY_ADJUSTED:
            blocked = True
            notes.append(
                "Partially adjusted data may mix adjusted and unadjusted prices"
            )

        # Check specific corporate action types
        for action in symbol_data.get("corporate_actions", []):
            if action == "delisting":
                notes.append("Symbol has delisting event — survivorship bias risk")
            elif action == "trading_suspension":
                notes.append("Symbol has trading suspension — fill assumptions may be invalid")
            elif action == "symbol_change":
                notes.append("Symbol has changed — historical continuity may be broken")

        return {
            "status": status,
            "passed": passed,
            "blocked": blocked,
            "notes": notes,
        }
