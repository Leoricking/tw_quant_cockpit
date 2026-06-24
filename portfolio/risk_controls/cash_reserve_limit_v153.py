"""
portfolio/risk_controls/cash_reserve_limit_v153.py — Cash Reserve Controls v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from portfolio.risk_controls.enums_v153 import RiskActionType, RiskControlStatus, RiskControlType
from portfolio.risk_controls.models_v153 import RiskControlCheck

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class CashReserveLimitChecker:
    """Checks that sufficient cash reserve is maintained."""

    RESEARCH_ONLY = True

    def check(
        self,
        check_id: str,
        policy_id: str,
        cash_weight: float,
        min_cash_warn: float = 0.05,
        min_cash_breach: float = 0.02,
    ) -> RiskControlCheck:
        """Check if cash reserve is below required minimum."""
        # Below breach_threshold (too low cash) is a breach
        if cash_weight < min_cash_breach:
            status = RiskControlStatus.BREACH
            action = RiskActionType.REVIEW_RECOMMENDED
        elif cash_weight < min_cash_warn:
            status = RiskControlStatus.WARN
            action = RiskActionType.WARN_ONLY
        else:
            status = RiskControlStatus.PASS
            action = RiskActionType.NO_ACTION

        return RiskControlCheck(
            check_id=check_id,
            policy_id=policy_id,
            control_type=RiskControlType.CASH_RESERVE,
            status=status,
            current_value=cash_weight,
            warn_threshold=min_cash_warn,
            breach_threshold=min_cash_breach,
            recommended_action=action,
            detail=f"Cash {cash_weight:.1%} vs minimum {min_cash_breach:.1%}",
        )
