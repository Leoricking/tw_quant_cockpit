"""
portfolio/risk_controls/liquidity_limit_v153.py — Liquidity Risk Controls v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict

from portfolio.risk_controls.enums_v153 import RiskActionType, RiskControlStatus, RiskControlType
from portfolio.risk_controls.models_v153 import RiskControlCheck

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class LiquidityLimitChecker:
    """Checks liquidity risk controls for the portfolio."""

    RESEARCH_ONLY = True

    def check_illiquid_fraction(
        self,
        check_id: str,
        policy_id: str,
        illiquid_weight: float,
        warn_threshold: float = 0.20,
        breach_threshold: float = 0.35,
    ) -> RiskControlCheck:
        """Check fraction of portfolio in illiquid positions."""
        if illiquid_weight >= breach_threshold:
            status = RiskControlStatus.BREACH
            action = RiskActionType.REDUCE_RECOMMENDED
        elif illiquid_weight >= warn_threshold:
            status = RiskControlStatus.WARN
            action = RiskActionType.REVIEW_RECOMMENDED
        else:
            status = RiskControlStatus.PASS
            action = RiskActionType.NO_ACTION

        return RiskControlCheck(
            check_id=check_id,
            policy_id=policy_id,
            control_type=RiskControlType.LIQUIDITY_LIMIT,
            status=status,
            current_value=illiquid_weight,
            warn_threshold=warn_threshold,
            breach_threshold=breach_threshold,
            recommended_action=action,
            detail=f"Illiquid weight {illiquid_weight:.1%} vs limit {breach_threshold:.1%}",
        )
