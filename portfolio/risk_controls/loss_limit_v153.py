"""
portfolio/risk_controls/loss_limit_v153.py — Daily/Weekly/Monthly Loss Limits v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from portfolio.risk_controls.enums_v153 import RiskActionType, RiskControlStatus, RiskControlType
from portfolio.risk_controls.models_v153 import RiskControlCheck

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class LossLimitChecker:
    """Checks daily, weekly, monthly loss limits against policy thresholds."""

    RESEARCH_ONLY = True

    def check_daily(
        self,
        check_id: str,
        policy_id: str,
        daily_pnl_pct: float,
        warn_threshold: float = -0.015,
        breach_threshold: float = -0.03,
    ) -> RiskControlCheck:
        return self._check(
            check_id, policy_id, RiskControlType.DAILY_LOSS_LIMIT,
            daily_pnl_pct, warn_threshold, breach_threshold,
            label="Daily P&L",
        )

    def check_weekly(
        self,
        check_id: str,
        policy_id: str,
        weekly_pnl_pct: float,
        warn_threshold: float = -0.03,
        breach_threshold: float = -0.05,
    ) -> RiskControlCheck:
        return self._check(
            check_id, policy_id, RiskControlType.WEEKLY_LOSS_LIMIT,
            weekly_pnl_pct, warn_threshold, breach_threshold,
            label="Weekly P&L",
        )

    def check_monthly(
        self,
        check_id: str,
        policy_id: str,
        monthly_pnl_pct: float,
        warn_threshold: float = -0.05,
        breach_threshold: float = -0.10,
    ) -> RiskControlCheck:
        return self._check(
            check_id, policy_id, RiskControlType.MONTHLY_LOSS_LIMIT,
            monthly_pnl_pct, warn_threshold, breach_threshold,
            label="Monthly P&L",
        )

    def _check(
        self,
        check_id: str,
        policy_id: str,
        control_type: RiskControlType,
        pnl_pct: float,
        warn_threshold: float,
        breach_threshold: float,
        label: str,
    ) -> RiskControlCheck:
        # breach_threshold is more negative than warn_threshold
        if pnl_pct <= breach_threshold:
            status = RiskControlStatus.BREACH
            action = RiskActionType.HALT_RECOMMENDED
        elif pnl_pct <= warn_threshold:
            status = RiskControlStatus.WARN
            action = RiskActionType.REVIEW_RECOMMENDED
        else:
            status = RiskControlStatus.PASS
            action = RiskActionType.NO_ACTION

        return RiskControlCheck(
            check_id=check_id,
            policy_id=policy_id,
            control_type=control_type,
            status=status,
            current_value=pnl_pct,
            warn_threshold=warn_threshold,
            breach_threshold=breach_threshold,
            recommended_action=action,
            detail=f"{label} {pnl_pct:.2%} vs limit {breach_threshold:.2%}",
        )
