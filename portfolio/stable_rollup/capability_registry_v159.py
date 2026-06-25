"""portfolio/stable_rollup/capability_registry_v159.py — Stable capability registry v1.5.9."""
from .models_v159 import StableCapabilityRecord

STABLE_CAPABILITIES = [
    StableCapabilityRecord(
        capability_id="portfolio_foundation",
        display_name="Portfolio Research Foundation",
        module="portfolio",
        introduced_version="1.5.0",
        stable_version="1.5.0",
        stage="STABLE",
        implementation_path="portfolio/",
        cli_commands=["portfolio-health", "portfolio-snapshot", "portfolio-positions"],
        health_check="portfolio.health_v150.PortfolioHealthCheck",
        release_gate="release.portfolio_research_release_gate",
        tests=["tests/test_portfolio_research_v150.py"],
        docs="docs/portfolio_research_v1.5.0.md",
        known_limitations=["research-only", "no-live-trading"],
    ),
    StableCapabilityRecord(
        capability_id="position_sizing",
        display_name="Position Sizing",
        module="portfolio.sizing",
        introduced_version="1.5.1",
        stable_version="1.5.1",
        stage="STABLE",
        implementation_path="portfolio/sizing/",
        health_check="portfolio.sizing.health_v151.PositionSizingHealthCheck",
        release_gate="release.position_sizing_release_gate_v151",
        tests=["tests/test_position_sizing_v151.py"],
        docs="docs/position_sizing_v1.5.1.md",
        known_limitations=["research-only", "no-auto-sizing"],
    ),
    StableCapabilityRecord(
        capability_id="correlation_exposure",
        display_name="Correlation & Exposure",
        module="portfolio.correlation",
        introduced_version="1.5.2",
        stable_version="1.5.2",
        stage="STABLE",
        implementation_path="portfolio/correlation/",
        health_check="portfolio.correlation.health_v152.CorrelationExposureHealthCheck",
        release_gate="release.correlation_exposure_release_gate_v152",
        tests=["tests/test_correlation_exposure_v152.py"],
        docs="docs/correlation_exposure_v1.5.2.md",
        known_limitations=["research-only", "no-auto-rebalance"],
    ),
    StableCapabilityRecord(
        capability_id="drawdown_risk_controls",
        display_name="Drawdown & Risk Controls",
        module="portfolio.risk_controls",
        introduced_version="1.5.3",
        stable_version="1.5.3",
        stage="STABLE",
        implementation_path="portfolio/risk_controls/",
        health_check="portfolio.risk_controls.health_v153.DrawdownRiskControlsHealthCheck",
        release_gate="release.drawdown_risk_controls_release_gate_v153",
        tests=["tests/test_drawdown_risk_controls_v153.py"],
        docs="docs/drawdown_risk_controls_v1.5.3.md",
        known_limitations=["research-only", "no-auto-stop", "no-auto-reduction"],
    ),
    StableCapabilityRecord(
        capability_id="portfolio_walk_forward",
        display_name="Portfolio Walk-forward Backtest",
        module="portfolio.walk_forward",
        introduced_version="1.5.4",
        stable_version="1.5.4",
        stage="STABLE",
        implementation_path="portfolio/walk_forward/",
        health_check="portfolio.walk_forward.health_v154.PortfolioWalkForwardHealthCheck",
        release_gate="release.portfolio_walk_forward_release_gate_v154",
        tests=["tests/test_portfolio_walk_forward_v154.py"],
        docs="docs/portfolio_walk_forward_v1.5.4.md",
        known_limitations=["research-only", "historical-simulation-only", "no-live-apply"],
    ),
    StableCapabilityRecord(
        capability_id="portfolio_stable_rollup",
        display_name="Portfolio Stable Rollup",
        module="portfolio.stable_rollup",
        introduced_version="1.5.9",
        stable_version="1.5.9",
        stage="STABLE",
        implementation_path="portfolio/stable_rollup/",
        health_check="portfolio.stable_rollup.health_v159.PortfolioStableRollupHealthCheck",
        release_gate="release.portfolio_stable_release_gate_v159",
        tests=["tests/test_portfolio_stable_rollup_v159.py"],
        docs="docs/portfolio_stable_rollup_v1.5.9.md",
        known_limitations=["research-only", "freeze-only", "no-new-features"],
    ),
]

PLANNED_CAPABILITIES = [
    StableCapabilityRecord(
        capability_id="live_paper_trading",
        display_name="Live Paper Trading",
        module="PLANNED",
        introduced_version="PLANNED",
        stable_version="PLANNED",
        stage="PLANNED",
        implementation_path="PLANNED",
    ),
    StableCapabilityRecord(
        capability_id="broker_integration",
        display_name="Broker Integration",
        module="PLANNED",
        introduced_version="PLANNED",
        stable_version="PLANNED",
        stage="PLANNED",
        implementation_path="PLANNED",
    ),
    StableCapabilityRecord(
        capability_id="production_trading",
        display_name="Production Trading",
        module="BLOCKED",
        introduced_version="BLOCKED",
        stable_version="BLOCKED",
        stage="DISABLED",
        implementation_path="BLOCKED",
    ),
    StableCapabilityRecord(
        capability_id="auto_rebalance",
        display_name="Auto Rebalance",
        module="PLANNED",
        introduced_version="PLANNED",
        stable_version="PLANNED",
        stage="PLANNED",
        implementation_path="PLANNED",
    ),
    StableCapabilityRecord(
        capability_id="portfolio_optimization",
        display_name="Portfolio Optimization",
        module="PLANNED",
        introduced_version="PLANNED",
        stable_version="PLANNED",
        stage="PLANNED",
        implementation_path="PLANNED",
    ),
    StableCapabilityRecord(
        capability_id="efficient_frontier",
        display_name="Efficient Frontier",
        module="PLANNED",
        introduced_version="PLANNED",
        stable_version="PLANNED",
        stage="PLANNED",
        implementation_path="PLANNED",
    ),
    StableCapabilityRecord(
        capability_id="black_litterman",
        display_name="Black-Litterman",
        module="PLANNED",
        introduced_version="PLANNED",
        stable_version="PLANNED",
        stage="PLANNED",
        implementation_path="PLANNED",
    ),
    StableCapabilityRecord(
        capability_id="hedging_execution",
        display_name="Hedging Execution",
        module="PLANNED",
        introduced_version="PLANNED",
        stable_version="PLANNED",
        stage="PLANNED",
        implementation_path="PLANNED",
    ),
]


class CapabilityRegistryV159:
    def get_stable(self):
        return list(STABLE_CAPABILITIES)

    def get_planned(self):
        return list(PLANNED_CAPABILITIES)

    def get_disabled(self):
        return [c for c in PLANNED_CAPABILITIES if c.stage == "DISABLED"]

    def get_by_id(self, cid):
        return next(
            (c for c in STABLE_CAPABILITIES + PLANNED_CAPABILITIES if c.capability_id == cid),
            None,
        )

    def validate(self):
        issues = []
        ids = [c.capability_id for c in STABLE_CAPABILITIES + PLANNED_CAPABILITIES]
        if len(ids) != len(set(ids)):
            issues.append("DUPLICATE_CAPABILITY_ID")
        for c in STABLE_CAPABILITIES:
            if c.stage != "STABLE":
                issues.append(f"NON_STABLE_IN_STABLE_LIST:{c.capability_id}")
        for c in PLANNED_CAPABILITIES:
            if c.stage == "STABLE":
                issues.append(f"PLANNED_MARKED_STABLE:{c.capability_id}")
        return {"valid": len(issues) == 0, "issues": issues}
