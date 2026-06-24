"""
portfolio/risk_controls/constraint_engine_v153.py — Risk Control Constraint Engine v1.5.3.
21-step evaluation order. Research-only. No auto-execution.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import datetime
import uuid
from typing import Any, Dict, List, Optional

from portfolio.risk_controls.enums_v153 import RiskControlStatus, RiskControlType
from portfolio.risk_controls.models_v153 import RiskControlCheck, RiskControlEvaluation

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"

# 21-step evaluation order
EVALUATION_ORDER = [
    "eligibility_gate",
    "pit_validation",
    "equity_curve",
    "underwater_curve",
    "max_drawdown",
    "drawdown_episodes",
    "drawdown_duration",
    "drawdown_recovery",
    "drawdown_attribution",
    "risk_budget",
    "volatility_limit",
    "daily_loss_limit",
    "weekly_loss_limit",
    "monthly_loss_limit",
    "concentration_limit",
    "correlation_limit",
    "liquidity_limit",
    "cash_reserve",
    "sizing_impact",
    "stress_scenarios",
    "lineage_and_explain",
]


class RiskControlConstraintEngine:
    """
    Evaluates all risk controls in the prescribed 21-step order.
    Research-only. Never auto-applies any control action.
    """

    RESEARCH_ONLY = True

    def evaluate(
        self,
        portfolio_id: str,
        as_of: str,
        checks: List[RiskControlCheck],
    ) -> RiskControlEvaluation:
        """Aggregate individual checks into a full evaluation."""
        breach_count = sum(1 for c in checks if c.status == RiskControlStatus.BREACH)
        warn_count   = sum(1 for c in checks if c.status == RiskControlStatus.WARN)
        pass_count   = sum(1 for c in checks if c.status == RiskControlStatus.PASS)

        if breach_count > 0:
            overall = RiskControlStatus.BREACH
        elif warn_count > 0:
            overall = RiskControlStatus.WARN
        elif pass_count > 0:
            overall = RiskControlStatus.PASS
        else:
            overall = RiskControlStatus.UNKNOWN

        return RiskControlEvaluation(
            evaluation_id=f"EVAL_{portfolio_id}_{as_of}_{uuid.uuid4().hex[:6]}",
            portfolio_id=portfolio_id,
            as_of=as_of,
            checks=checks,
            overall_status=overall,
            breach_count=breach_count,
            warn_count=warn_count,
            pass_count=pass_count,
            generated_at=datetime.datetime.utcnow().isoformat(),
        )

    def build_demo_evaluation(
        self,
        portfolio_id: str = "demo_portfolio",
        as_of: str = "2026-06-21",
    ) -> RiskControlEvaluation:
        """Build a demo evaluation with a set of synthetic checks."""
        from portfolio.risk_controls.volatility_limit_v153 import VolatilityLimitChecker
        from portfolio.risk_controls.loss_limit_v153 import LossLimitChecker
        from portfolio.risk_controls.concentration_limit_v153 import ConcentrationLimitChecker
        from portfolio.risk_controls.correlation_limit_v153 import CorrelationLimitChecker
        from portfolio.risk_controls.liquidity_limit_v153 import LiquidityLimitChecker
        from portfolio.risk_controls.cash_reserve_limit_v153 import CashReserveLimitChecker

        checks: List[RiskControlCheck] = []

        checks.append(VolatilityLimitChecker().check("CHK_VOL_001", "POL_VOL_001", 0.18))
        checks.append(LossLimitChecker().check_daily("CHK_DLY_001", "POL_DLY_001", -0.008))
        checks.append(LossLimitChecker().check_weekly("CHK_WKL_001", "POL_WKL_001", -0.022))
        checks.append(LossLimitChecker().check_monthly("CHK_MTH_001", "POL_MTH_001", -0.035))
        checks.append(ConcentrationLimitChecker().check_single_name(
            "CHK_CON_001", "POL_CON_001",
            {"2330": 0.25, "2308": 0.20, "2317": 0.15, "Cash": 0.40},
        ))
        checks.append(CorrelationLimitChecker().check_max_pairwise(
            "CHK_COR_001", "POL_COR_001",
            high_correlation_pair_count=1, total_pairs=3,
        ))
        checks.append(LiquidityLimitChecker().check_illiquid_fraction(
            "CHK_LIQ_001", "POL_LIQ_001", illiquid_weight=0.05,
        ))
        checks.append(CashReserveLimitChecker().check(
            "CHK_CSH_001", "POL_CSH_001", cash_weight=0.40,
        ))

        return self.evaluate(portfolio_id, as_of, checks)
