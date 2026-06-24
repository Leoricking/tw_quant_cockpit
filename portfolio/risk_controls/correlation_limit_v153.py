"""
portfolio/risk_controls/correlation_limit_v153.py — Correlation Risk Controls v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import List, Tuple

from portfolio.risk_controls.enums_v153 import RiskActionType, RiskControlStatus, RiskControlType
from portfolio.risk_controls.models_v153 import RiskControlCheck

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class CorrelationLimitChecker:
    """Checks portfolio correlation risk controls."""

    RESEARCH_ONLY = True

    def check_max_pairwise(
        self,
        check_id: str,
        policy_id: str,
        high_correlation_pair_count: int,
        total_pairs: int,
        warn_threshold: float = 0.20,
        breach_threshold: float = 0.40,
    ) -> RiskControlCheck:
        """Check fraction of high-correlation pairs."""
        ratio = (high_correlation_pair_count / total_pairs
                 if total_pairs > 0 else 0.0)

        if ratio >= breach_threshold:
            status = RiskControlStatus.BREACH
            action = RiskActionType.REDUCE_RECOMMENDED
        elif ratio >= warn_threshold:
            status = RiskControlStatus.WARN
            action = RiskActionType.REVIEW_RECOMMENDED
        else:
            status = RiskControlStatus.PASS
            action = RiskActionType.NO_ACTION

        return RiskControlCheck(
            check_id=check_id,
            policy_id=policy_id,
            control_type=RiskControlType.CORRELATION_LIMIT,
            status=status,
            current_value=ratio,
            warn_threshold=warn_threshold,
            breach_threshold=breach_threshold,
            recommended_action=action,
            detail=(
                f"{high_correlation_pair_count}/{total_pairs} high-correlation pairs "
                f"({ratio:.0%}) vs limit {breach_threshold:.0%}"
            ),
        )
