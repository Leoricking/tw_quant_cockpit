"""
portfolio/risk_controls/stress_v153.py — Drawdown Stress Scenarios v1.5.3.
8 scenario types. Research-only. Never auto-executes.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from portfolio.risk_controls.enums_v153 import StressScenarioType
from portfolio.risk_controls.models_v153 import DrawdownStressResult

RESEARCH_ONLY = True
MODULE_VERSION = "1.5.3"

# Default shock magnitudes by scenario type
_DEFAULT_SHOCKS = {
    StressScenarioType.HISTORICAL_REPEAT:     -0.25,
    StressScenarioType.VOLATILITY_SPIKE:      -0.15,
    StressScenarioType.CORRELATION_BREAKDOWN: -0.20,
    StressScenarioType.LIQUIDITY_CRISIS:      -0.30,
    StressScenarioType.FLASH_CRASH:           -0.10,
    StressScenarioType.BEAR_MARKET:           -0.40,
    StressScenarioType.SECTOR_ROTATION:       -0.18,
    StressScenarioType.COMBINED:              -0.45,
}


class DrawdownStressAnalyzer:
    """Runs drawdown stress scenarios. Research-only."""

    RESEARCH_ONLY = True

    def run(
        self,
        portfolio_id: str,
        portfolio_value: float,
        scenario_type: StressScenarioType,
        shock_magnitude: Optional[float] = None,
        drawdown_limit: float = -0.20,
        volatility_limit: float = 0.30,
        extra_params: Dict[str, Any] = None,
    ) -> DrawdownStressResult:
        """Run a single stress scenario. Returns descriptive result only."""
        extra_params = extra_params or {}
        if shock_magnitude is None:
            shock_magnitude = _DEFAULT_SHOCKS.get(scenario_type, -0.20)

        projected_dd = shock_magnitude  # simplified linear shock
        projected_loss = abs(projected_dd) * portfolio_value

        breached: List[str] = []
        if projected_dd <= drawdown_limit:
            breached.append("DRAWDOWN_LIMIT")
        # Volatility breach approximation
        implied_vol = abs(shock_magnitude) * 4  # annualize rough proxy
        if implied_vol >= volatility_limit:
            breached.append("VOLATILITY_LIMIT")

        return DrawdownStressResult(
            scenario_id=f"STRESS_{scenario_type.value}_{uuid.uuid4().hex[:6]}",
            scenario_type=scenario_type,
            portfolio_id=portfolio_id,
            shock_magnitude=shock_magnitude,
            projected_drawdown_pct=projected_dd,
            projected_loss=projected_loss,
            risk_controls_breached=breached,
            description=f"{scenario_type.value} stress: {shock_magnitude:.1%} shock",
        )

    def run_all(
        self,
        portfolio_id: str,
        portfolio_value: float,
        drawdown_limit: float = -0.20,
        volatility_limit: float = 0.30,
    ) -> List[DrawdownStressResult]:
        """Run all 8 scenario types."""
        results: List[DrawdownStressResult] = []
        for scenario_type in StressScenarioType:
            results.append(self.run(
                portfolio_id, portfolio_value, scenario_type,
                drawdown_limit=drawdown_limit,
                volatility_limit=volatility_limit,
            ))
        return results

    def run_from_fixture(self, fixture: Dict[str, Any]) -> DrawdownStressResult:
        """Run stress from a JSON fixture dict."""
        portfolio_id = fixture.get("portfolio_id", "demo_portfolio")
        portfolio_value = float(fixture.get("portfolio_value", 1_000_000.0))
        scenario_str = fixture.get("scenario_type", "COMBINED")
        try:
            scenario_type = StressScenarioType(scenario_str)
        except ValueError:
            scenario_type = StressScenarioType.COMBINED
        shock = fixture.get("shock_magnitude", None)
        if shock is not None:
            shock = float(shock)
        return self.run(
            portfolio_id, portfolio_value, scenario_type,
            shock_magnitude=shock,
        )
