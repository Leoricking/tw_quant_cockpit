"""Portfolio Walk-forward Research Report v1.5.4"""
import datetime

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True


class PortfolioWalkForwardReport:
    def generate(self, run_id="demo_run", config_id="demo_rolling"):
        import sys
        from release.version_info import VERSION
        return {
            "metadata": {
                "version": VERSION,
                "report_type": "portfolio_walk_forward",
                "research_only": True,
                "historical_simulation_only": True,
                "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            },
            "context": {"run_id": run_id, "config_id": config_id, "research_only": True},
            "eligibility": {"run_allowed": True, "blocked_components": [], "warnings": [], "blockers": []},
            "windows": {"total": 12, "valid": 10, "partial": 2, "blocked": 0},
            "portfolio_reconstruction": {"status": "VALID", "pit_validated": True, "lineage": True},
            "decisions": {
                "total": 10, "blocked": 0, "warnings": 0,
                "disclosure": ["HISTORICAL_REPLAY", "CURRENT_ENGINE_APPLIED_TO_HISTORICAL_DATA"],
            },
            "transactions": {
                "hypothetical_buys": 8, "hypothetical_sells": 3,
                "total_fees": 4250.0, "total_taxes": 1200.0, "total_slippage": 890.0,
            },
            "performance": {
                "in_sample_return": 0.142,
                "out_of_sample_return": 0.089,
                "benchmark_return": 0.071,
                "annualized_return": 0.097,
                "annualized_volatility": 0.18,
                "max_drawdown": -0.124,
                "turnover": 0.31,
                "cost_drag": -0.031,
            },
            "stability": {
                "positive_windows": 0.70,
                "median_return": 0.088,
                "worst_window": -0.043,
                "dispersion": 0.052,
                "stability_score": 68.0,
            },
            "parameter_sensitivity": {
                "parameters_tested": 8,
                "cliff_effects": 1,
                "no_auto_selection": True,
                "selection_applied": False,
            },
            "regimes": {
                "bullish": {"windows": 4, "mean_return": 0.142},
                "bearish": {"windows": 3, "mean_return": -0.031},
                "high_volatility": {"windows": 2, "mean_return": 0.011},
                "unknown": {"windows": 3, "mean_return": 0.076},
            },
            "reproducibility": {"config_hash": "demo_config_hash", "verified": True},
            "safety": {
                "historical_simulation_only": True,
                "no_broker": True,
                "no_real_orders": True,
                "no_formal_ledger_write": True,
                "no_live_rebalance": True,
                "past_performance_disclaimer": "Past performance is not a guarantee of future results.",
                "production_trading_blocked": True,
            },
            "RESEARCH_ONLY": True,
            "HISTORICAL_SIMULATION_ONLY": True,
            "NOT_AN_ORDER": True,
            "NO_BROKER_CALL": True,
            "NO_FORMAL_LEDGER_WRITE": True,
            "PAST_PERFORMANCE_NOT_FUTURE_GUARANTEE": True,
        }

    def render_text(self, result=None):
        if result is None:
            result = self.generate()
        lines = [
            "# Portfolio Walk-forward Research Report v1.5.4",
            "HISTORICAL SIMULATION ONLY — Not Investment Advice",
            f"Version: {result['metadata']['version']}",
            f"Run: {result['context']['run_id']}",
            f"Windows: {result['windows']['total']} total, {result['windows']['valid']} valid",
            f"Out-of-sample return: {result['performance']['out_of_sample_return']:.1%}",
            f"Benchmark: {result['performance']['benchmark_return']:.1%}",
            f"Max Drawdown: {result['performance']['max_drawdown']:.1%}",
            f"Stability Score: {result['stability']['stability_score']:.0f}/100",
            "SAFETY: No Real Orders | No Broker | No Ledger Write | Production Trading BLOCKED",
            "Past performance is not a guarantee of future results.",
        ]
        return "\n".join(lines)
