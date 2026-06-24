"""
portfolio/risk_controls/concentration_limit_v153.py — Concentration Risk Controls v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict

from portfolio.risk_controls.enums_v153 import RiskActionType, RiskControlStatus, RiskControlType
from portfolio.risk_controls.models_v153 import RiskControlCheck

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class ConcentrationLimitChecker:
    """Checks position/industry/theme concentration limits."""

    RESEARCH_ONLY = True

    def check_single_name(
        self,
        check_id: str,
        policy_id: str,
        weights: Dict[str, float],
        warn_threshold: float = 0.20,
        breach_threshold: float = 0.30,
    ) -> RiskControlCheck:
        max_weight = max(weights.values()) if weights else 0.0
        symbol = max(weights, key=weights.get) if weights else ""

        if max_weight >= breach_threshold:
            status = RiskControlStatus.BREACH
            action = RiskActionType.REDUCE_RECOMMENDED
        elif max_weight >= warn_threshold:
            status = RiskControlStatus.WARN
            action = RiskActionType.REVIEW_RECOMMENDED
        else:
            status = RiskControlStatus.PASS
            action = RiskActionType.NO_ACTION

        return RiskControlCheck(
            check_id=check_id,
            policy_id=policy_id,
            control_type=RiskControlType.CONCENTRATION_LIMIT,
            status=status,
            current_value=max_weight,
            warn_threshold=warn_threshold,
            breach_threshold=breach_threshold,
            recommended_action=action,
            detail=f"Max single-name weight {max_weight:.1%} ({symbol}) vs limit {breach_threshold:.1%}",
        )

    def check_industry(
        self,
        check_id: str,
        policy_id: str,
        industry_weights: Dict[str, float],
        warn_threshold: float = 0.35,
        breach_threshold: float = 0.50,
    ) -> RiskControlCheck:
        max_weight = max(industry_weights.values()) if industry_weights else 0.0
        top_industry = max(industry_weights, key=industry_weights.get) if industry_weights else ""

        if max_weight >= breach_threshold:
            status = RiskControlStatus.BREACH
            action = RiskActionType.REDUCE_RECOMMENDED
        elif max_weight >= warn_threshold:
            status = RiskControlStatus.WARN
            action = RiskActionType.REVIEW_RECOMMENDED
        else:
            status = RiskControlStatus.PASS
            action = RiskActionType.NO_ACTION

        return RiskControlCheck(
            check_id=check_id,
            policy_id=policy_id,
            control_type=RiskControlType.CONCENTRATION_LIMIT,
            status=status,
            current_value=max_weight,
            warn_threshold=warn_threshold,
            breach_threshold=breach_threshold,
            recommended_action=action,
            detail=f"Max industry weight {max_weight:.1%} ({top_industry}) vs limit {breach_threshold:.1%}",
        )
