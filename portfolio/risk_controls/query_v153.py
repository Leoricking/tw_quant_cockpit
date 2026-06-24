"""
portfolio/risk_controls/query_v153.py — Drawdown Risk Controls Query Service v1.5.3.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from portfolio.risk_controls.models_v153 import (
    DrawdownAnalysisRequest,
    DrawdownSummary,
    RiskControlEvaluation,
)

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"


class DrawdownRiskControlsQueryService:
    """
    Main query service for drawdown & risk controls.
    Research-only. Never creates orders, never contacts broker.
    """

    RESEARCH_ONLY = True

    # Blocked methods — these must NOT exist:
    # optimize_weights, rebalance_portfolio, submit_order,
    # execute_order, sync_broker, apply_risk_control, execute_stop

    def build_equity_curve(
        self,
        portfolio_id: str,
        as_of: str,
        daily_values: Dict[str, float] = None,
    ) -> List:
        """Build equity curve. Returns list of EquityCurvePoint."""
        from portfolio.risk_controls.equity_curve_v153 import PortfolioEquityCurveBuilder
        if daily_values:
            return PortfolioEquityCurveBuilder().build(daily_values, {}, as_of)
        return PortfolioEquityCurveBuilder().build_demo(portfolio_id, as_of)

    def build_underwater_curve(self, equity_curve: List) -> List:
        """Build underwater curve from equity curve."""
        from portfolio.risk_controls.underwater_v153 import UnderwaterCurveCalculator
        return UnderwaterCurveCalculator().calculate(equity_curve)

    def calculate_drawdown_summary(
        self,
        portfolio_id: str,
        as_of: str,
        equity_curve: List = None,
    ) -> DrawdownSummary:
        """Calculate full drawdown summary."""
        from portfolio.risk_controls.underwater_v153 import UnderwaterCurveCalculator
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator

        if equity_curve is None:
            equity_curve = self.build_equity_curve(portfolio_id, as_of)

        uw = UnderwaterCurveCalculator().calculate(equity_curve)
        return MaxDrawdownCalculator().calculate(portfolio_id, as_of, uw)

    def detect_episodes(self, equity_curve: List) -> List:
        """Detect drawdown episodes."""
        from portfolio.risk_controls.underwater_v153 import UnderwaterCurveCalculator
        from portfolio.risk_controls.drawdown_episode_v153 import DrawdownEpisodeDetector
        uw = UnderwaterCurveCalculator().calculate(equity_curve)
        return DrawdownEpisodeDetector().detect(uw)

    def calculate_rolling_drawdown(
        self,
        equity_curve: List,
        window: int,
        as_of: str,
    ) -> List[Dict[str, Any]]:
        """Calculate rolling maximum drawdown."""
        from portfolio.risk_controls.underwater_v153 import UnderwaterCurveCalculator
        from portfolio.risk_controls.drawdown_v153 import MaxDrawdownCalculator
        uw_points = UnderwaterCurveCalculator().calculate(equity_curve)
        return MaxDrawdownCalculator().calculate_rolling(uw_points, window, as_of)

    def calculate_attribution(
        self,
        portfolio_id: str,
        as_of: str,
        weights: Dict[str, float] = None,
        pnl_by_symbol: Dict[str, float] = None,
        industry_map: Dict[str, str] = None,
        portfolio_value: float = 1_000_000.0,
    ) -> Dict[str, List]:
        """Calculate drawdown attribution by position/industry/theme/cluster."""
        from portfolio.risk_controls.drawdown_attribution_v153 import DrawdownAttributionCalculator
        calc = DrawdownAttributionCalculator()

        weights = weights or {"2330": 0.40, "2308": 0.30, "2317": 0.20, "Cash": 0.10}
        pnl_by_symbol = pnl_by_symbol or {
            "2330": -20_000.0, "2308": -10_000.0, "2317": 5_000.0, "Cash": 0.0
        }
        industry_map = industry_map or {
            "2330": "Semiconductor", "2308": "Electronics",
            "2317": "Electronics", "Cash": "CASH"
        }

        by_position = calc.attribute_by_position(weights, pnl_by_symbol, portfolio_value)
        by_industry = calc.attribute_by_industry(industry_map, weights, pnl_by_symbol, portfolio_value)

        return {
            "by_position": by_position,
            "by_industry": by_industry,
            "by_theme":    [],
            "by_cluster":  [],
        }

    def evaluate_risk_controls(
        self,
        portfolio_id: str,
        as_of: str,
        drawdown_summary: DrawdownSummary = None,
    ) -> RiskControlEvaluation:
        """Run full risk controls evaluation."""
        from portfolio.risk_controls.constraint_engine_v153 import RiskControlConstraintEngine
        return RiskControlConstraintEngine().build_demo_evaluation(portfolio_id, as_of)

    def analyze_sizing_impact(self, proposal_id: str, as_of: str) -> Any:
        """Analyze risk impact of a sizing proposal."""
        from portfolio.risk_controls.sizing_impact_v153 import SizingRiskImpactAnalyzer
        return SizingRiskImpactAnalyzer().build_demo(proposal_id)

    def run_stress_scenario(
        self,
        portfolio_id: str,
        scenario_fixture: Dict[str, Any] = None,
    ) -> Any:
        """Run a stress scenario from fixture or defaults."""
        from portfolio.risk_controls.stress_v153 import DrawdownStressAnalyzer
        if scenario_fixture:
            return DrawdownStressAnalyzer().run_from_fixture(scenario_fixture)
        from portfolio.risk_controls.enums_v153 import StressScenarioType
        return DrawdownStressAnalyzer().run(portfolio_id, 1_000_000.0, StressScenarioType.COMBINED)

    def explain_evaluation(self, evaluation, drawdown_summary=None) -> Dict[str, Any]:
        """Generate explanation for evaluation."""
        from portfolio.risk_controls.explain_v153 import DrawdownRiskControlsExplainer
        return DrawdownRiskControlsExplainer().explain(evaluation, drawdown_summary)

    def get_policies(self) -> List[Dict[str, Any]]:
        """Return demo policy list."""
        from portfolio.risk_controls.enums_v153 import RiskControlType
        from portfolio.risk_controls.models_v153 import RiskControlPolicy
        policies = [
            RiskControlPolicy(
                policy_id="POL_VOL_001",
                control_type=RiskControlType.VOLATILITY_LIMIT,
                name="Annualized Volatility Limit",
                description="Portfolio annualized volatility must not exceed 30%.",
                warn_threshold=0.20, breach_threshold=0.30,
            ),
            RiskControlPolicy(
                policy_id="POL_DLY_001",
                control_type=RiskControlType.DAILY_LOSS_LIMIT,
                name="Daily Loss Limit",
                description="Daily P&L must not fall below -3%.",
                warn_threshold=-0.015, breach_threshold=-0.03,
            ),
            RiskControlPolicy(
                policy_id="POL_WKL_001",
                control_type=RiskControlType.WEEKLY_LOSS_LIMIT,
                name="Weekly Loss Limit",
                description="Weekly P&L must not fall below -5%.",
                warn_threshold=-0.03, breach_threshold=-0.05,
            ),
            RiskControlPolicy(
                policy_id="POL_MTH_001",
                control_type=RiskControlType.MONTHLY_LOSS_LIMIT,
                name="Monthly Loss Limit",
                description="Monthly P&L must not fall below -10%.",
                warn_threshold=-0.05, breach_threshold=-0.10,
            ),
            RiskControlPolicy(
                policy_id="POL_CON_001",
                control_type=RiskControlType.CONCENTRATION_LIMIT,
                name="Single Name Concentration Limit",
                description="Single name weight must not exceed 30%.",
                warn_threshold=0.20, breach_threshold=0.30,
            ),
            RiskControlPolicy(
                policy_id="POL_COR_001",
                control_type=RiskControlType.CORRELATION_LIMIT,
                name="Portfolio Correlation Limit",
                description="High-correlation pair fraction must not exceed 40%.",
                warn_threshold=0.20, breach_threshold=0.40,
            ),
            RiskControlPolicy(
                policy_id="POL_LIQ_001",
                control_type=RiskControlType.LIQUIDITY_LIMIT,
                name="Liquidity Limit",
                description="Illiquid position weight must not exceed 35%.",
                warn_threshold=0.20, breach_threshold=0.35,
            ),
            RiskControlPolicy(
                policy_id="POL_CSH_001",
                control_type=RiskControlType.CASH_RESERVE,
                name="Minimum Cash Reserve",
                description="Cash must not fall below 2% of portfolio.",
                warn_threshold=0.05, breach_threshold=0.02,
            ),
        ]
        return [
            {
                "policy_id":        p.policy_id,
                "control_type":     p.control_type.value,
                "name":             p.name,
                "description":      p.description,
                "warn_threshold":   p.warn_threshold,
                "breach_threshold": p.breach_threshold,
                "research_only":    True,
                "executable":       False,
                "order_created":    False,
            }
            for p in policies
        ]
