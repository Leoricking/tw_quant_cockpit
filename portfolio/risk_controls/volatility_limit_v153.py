"""
portfolio/risk_controls/volatility_limit_v153.py — Volatility Limit Check v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from portfolio.risk_controls.enums_v153 import RiskActionType, RiskControlStatus, RiskControlType
from portfolio.risk_controls.models_v153 import RiskControlCheck

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class VolatilityLimitChecker:
    """Checks annualized portfolio volatility against policy limits."""

    RESEARCH_ONLY = True

    def check(
        self,
        check_id: str,
        policy_id: str,
        annualized_volatility: float,
        warn_threshold: float = 0.20,
        breach_threshold: float = 0.30,
    ) -> RiskControlCheck:
        if annualized_volatility >= breach_threshold:
            status = RiskControlStatus.BREACH
            action = RiskActionType.REDUCE_RECOMMENDED
        elif annualized_volatility >= warn_threshold:
            status = RiskControlStatus.WARN
            action = RiskActionType.REVIEW_RECOMMENDED
        else:
            status = RiskControlStatus.PASS
            action = RiskActionType.NO_ACTION

        return RiskControlCheck(
            check_id=check_id,
            policy_id=policy_id,
            control_type=RiskControlType.VOLATILITY_LIMIT,
            status=status,
            current_value=annualized_volatility,
            warn_threshold=warn_threshold,
            breach_threshold=breach_threshold,
            recommended_action=action,
            detail=f"Annualized volatility {annualized_volatility:.1%} vs limit {breach_threshold:.1%}",
        )
