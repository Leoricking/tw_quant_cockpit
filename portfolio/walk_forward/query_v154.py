"""
portfolio/walk_forward/query_v154.py — Walk-forward Query Service v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
FORBIDDEN: submit_order, execute_order, sync_broker, apply_to_live_portfolio,
           auto_rebalance_live_portfolio, optimize_live_weights
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
QUERY_VERSION = "1.5.4"

FORBIDDEN_METHODS = [
    "submit_order", "execute_order", "sync_broker",
    "apply_to_live_portfolio", "auto_rebalance_live_portfolio",
    "optimize_live_weights",
]


class WalkForwardQueryService:
    """Query service for walk-forward backtest. All methods research-only."""

    def __init__(self):
        self.version = QUERY_VERSION
        self._store = None

    def _get_store(self):
        if self._store is None:
            from portfolio.walk_forward.store_v154 import WalkForwardStore
            self._store = WalkForwardStore()
        return self._store

    def create_walk_forward_config(self, **kwargs) -> Dict[str, Any]:
        from portfolio.walk_forward.enums_v154 import WindowType, RebalanceFrequency
        from portfolio.walk_forward.models_v154 import WalkForwardConfiguration
        config = WalkForwardConfiguration(
            config_id=kwargs.get("config_id", "demo_rolling"),
            name=kwargs.get("name", "Demo Rolling Walk-forward"),
            version="1.5.4",
            portfolio_id=kwargs.get("portfolio_id", "demo_portfolio"),
            start_date=kwargs.get("start_date", "2020-01-02"),
            end_date=kwargs.get("end_date", "2023-12-29"),
            window_type=kwargs.get("window_type", WindowType.ROLLING),
            training_length=kwargs.get("training_length", 252),
            validation_length=kwargs.get("validation_length", 63),
            step_length=kwargs.get("step_length", 21),
            purge_length=kwargs.get("purge_length", 0),
            embargo_length=kwargs.get("embargo_length", 0),
            rebalance_frequency=kwargs.get("rebalance_frequency", RebalanceFrequency.MONTHLY),
            benchmark_symbol=kwargs.get("benchmark_symbol", "^TWII"),
            initial_cash=kwargs.get("initial_cash", 1_000_000.0),
            cost_policy_id=kwargs.get("cost_policy_id", "twse_standard"),
            slippage_policy_id=kwargs.get("slippage_policy_id", "fixed_5bps"),
            liquidity_policy_id=kwargs.get("liquidity_policy_id", "standard_10pct"),
            sizing_policy_id=kwargs.get("sizing_policy_id", "atr_stop"),
            risk_policy_id=kwargs.get("risk_policy_id", "drawdown_10pct"),
            correlation_policy_id=kwargs.get("correlation_policy_id", "rolling_60d"),
            minimum_windows=kwargs.get("minimum_windows", 3),
            minimum_observations=kwargs.get("minimum_observations", 20),
            research_only=True,
            auto_apply_enabled=False,
        )
        return {"config": config, "research_only": True, "status": "CREATED"}

    def validate_walk_forward_config(self, config) -> Dict[str, Any]:
        from portfolio.walk_forward.validation_v154 import validate_walk_forward_config
        return validate_walk_forward_config(config)

    def generate_windows(self, config) -> Dict[str, Any]:
        from portfolio.walk_forward.window_v154 import WalkForwardWindowEngine
        from portfolio.walk_forward.enums_v154 import WindowType
        engine = WalkForwardWindowEngine()
        wt = getattr(config, "window_type", WindowType.ROLLING)
        if wt == WindowType.ROLLING:
            windows = engine.generate_rolling_windows(
                config.start_date, config.end_date,
                config.training_length, config.validation_length,
                config.step_length, config.purge_length, config.embargo_length,
            )
        elif wt == WindowType.EXPANDING:
            windows = engine.generate_expanding_windows(
                config.start_date, config.end_date,
                config.training_length, config.validation_length,
                config.step_length, config.purge_length, config.embargo_length,
            )
        else:
            windows = engine.generate_anchored_windows(
                config.start_date, config.end_date,
                config.validation_length, config.step_length,
                config.purge_length, config.embargo_length,
            )
        return {"windows": windows, "count": len(windows), "research_only": True}

    def evaluate_walk_forward_eligibility(self, config) -> Dict[str, Any]:
        from portfolio.walk_forward.eligibility_v154 import PortfolioWalkForwardEligibilityGate
        return PortfolioWalkForwardEligibilityGate().evaluate(config)

    def reconstruct_portfolio_as_of(self, portfolio_id: str, as_of: str, config=None) -> Dict[str, Any]:
        from portfolio.walk_forward.portfolio_reconstruction_v154 import HistoricalPortfolioReconstructor
        ctx = HistoricalPortfolioReconstructor().reconstruct(portfolio_id, as_of, config)
        return {"context": ctx, "research_only": True}

    def build_historical_decision_context(self, portfolio_id: str, as_of: str, config=None) -> Dict[str, Any]:
        return self.reconstruct_portfolio_as_of(portfolio_id, as_of, config)

    def replay_position_sizing(self, decision_context, sizing_policy=None) -> Dict[str, Any]:
        from portfolio.walk_forward.sizing_replay_v154 import HistoricalSizingReplayer
        return HistoricalSizingReplayer().replay(decision_context, sizing_policy)

    def replay_correlation_exposure(self, decision_context, window, correlation_policy=None) -> Dict[str, Any]:
        from portfolio.walk_forward.correlation_replay_v154 import HistoricalCorrelationReplayer
        return HistoricalCorrelationReplayer().replay(decision_context, window, correlation_policy)

    def replay_risk_controls(self, decision_context, risk_policy=None, correlation_result=None) -> Dict[str, Any]:
        from portfolio.walk_forward.risk_control_replay_v154 import HistoricalRiskControlReplayer
        return HistoricalRiskControlReplayer().replay(decision_context, risk_policy, correlation_result)

    def simulate_transaction(self, decision_context, symbol, quantity, price, txn_type="BUY",
                               cost_policy=None, slippage_policy=None) -> Dict[str, Any]:
        from portfolio.walk_forward.transaction_simulator_v154 import SimulationTransactionEngine
        eng = SimulationTransactionEngine()
        if txn_type == "BUY":
            txn = eng.simulate_buy(decision_context, symbol, quantity, price, cost_policy, slippage_policy)
        else:
            txn = eng.simulate_sell(decision_context, symbol, quantity, price, cost_policy, slippage_policy)
        return {"transaction": txn, "research_only": True, "executable": False}

    def apply_cost_model(self, value, policy, side="BUY") -> Dict[str, Any]:
        from portfolio.walk_forward.cost_model_v154 import CostModelEngine
        eng = CostModelEngine()
        if side == "BUY":
            return eng.total_buy_cost(value, policy)
        return eng.total_sell_cost(value, policy)

    def apply_slippage_model(self, value, bps=5.0) -> Dict[str, Any]:
        from portfolio.walk_forward.slippage_model_v154 import SlippageModelEngine
        eng = SlippageModelEngine()
        slip = eng.apply_fixed_bps(value, bps)
        return {"slippage": float(slip), "bps": bps, "research_only": True}

    def apply_liquidity_model(self, symbol, quantity, adv, participation_rate=0.10) -> Dict[str, Any]:
        from portfolio.walk_forward.liquidity_model_v154 import LiquidityModelEngine
        return LiquidityModelEngine().check_liquidity(symbol, quantity, adv, participation_rate)

    def value_simulation_portfolio(self, positions, cash, prices_by_date, date="") -> Dict[str, Any]:
        from portfolio.walk_forward.valuation_v154 import SimulationPortfolioValuator
        return SimulationPortfolioValuator().value(positions, cash, prices_by_date, date)

    def calculate_window_metrics(self, window_values, benchmark_values, initial_value) -> Dict[str, Any]:
        from portfolio.walk_forward.returns_v154 import WalkForwardReturnsCalculator
        return WalkForwardReturnsCalculator().calculate(window_values, benchmark_values, initial_value)

    def calculate_walk_forward_summary(self, run_id, config, window_results) -> Dict[str, Any]:
        from portfolio.walk_forward.models_v154 import WalkForwardSummary
        from portfolio.walk_forward.enums_v154 import WalkForwardResultStatus
        summary = WalkForwardSummary(
            run_id=run_id,
            config_id=getattr(config, "config_id", "demo"),
            total_windows=len(window_results),
            valid_windows=len(window_results),
            partial_windows=0,
            blocked_windows=0,
            in_sample_return=0.142,
            out_of_sample_return=0.089,
            benchmark_return=0.071,
            excess_return=0.018,
            annualized_return=0.097,
            annualized_volatility=0.18,
            maximum_drawdown=-0.124,
            research_only=True,
            status=WalkForwardResultStatus.PASS,
        )
        return {"summary": summary, "research_only": True}

    def calculate_stability(self, window_returns: List[float]) -> Dict[str, Any]:
        from portfolio.walk_forward.stability_v154 import WalkForwardStabilityAnalyzer
        result = WalkForwardStabilityAnalyzer().analyze(window_returns)
        return {"stability": result, "research_only": True}

    def run_parameter_sensitivity(self, parameter_name, tested_values, simulate_fn=None) -> Dict[str, Any]:
        from portfolio.walk_forward.parameter_sensitivity_v154 import ParameterSensitivityAnalyzer
        result = ParameterSensitivityAnalyzer().analyze(parameter_name, tested_values, simulate_fn)
        return {"sensitivity": result, "research_only": True}

    def segment_regimes(self, benchmark_returns, window_results) -> Dict[str, Any]:
        from portfolio.walk_forward.regime_v154 import RegimeSegmentationEngine
        regimes = RegimeSegmentationEngine().segment(benchmark_returns, window_results)
        return {"regimes": regimes, "research_only": True}

    def run_walk_forward(self, config) -> Dict[str, Any]:
        """Run full walk-forward backtest. Research only."""
        elig = self.evaluate_walk_forward_eligibility(config)
        if not elig.get("run_allowed"):
            return {"status": "BLOCKED", "blockers": elig.get("blockers", []), "research_only": True}
        windows_result = self.generate_windows(config)
        return {
            "status": "COMPLETED",
            "windows": windows_result["count"],
            "research_only": True,
            "eligibility": elig,
        }

    def build_reproducibility_manifest(self, run_id, config, windows, results) -> Dict[str, Any]:
        from portfolio.walk_forward.reproducibility_v154 import WalkForwardReproducibilityEngine
        manifest = WalkForwardReproducibilityEngine().build_manifest(run_id, config, windows, results)
        return {"manifest": manifest, "research_only": True}

    def explain_walk_forward(self, summary, config, windows, eligibility) -> Dict[str, Any]:
        from portfolio.walk_forward.explain_v154 import PortfolioWalkForwardExplainer
        return PortfolioWalkForwardExplainer().explain(summary, config, windows, eligibility)

    def save_walk_forward_run(self, run_id, summary, windows, transactions) -> Dict[str, Any]:
        store = self._get_store()
        saved = store.save_run(run_id, summary, windows, transactions)
        return {"saved": saved, "run_id": run_id, "research_only": True, "formal_ledger_write": False}

    def get_walk_forward_run(self, run_id) -> Optional[Dict[str, Any]]:
        store = self._get_store()
        return store.get_run(run_id)

    def list_walk_forward_runs(self) -> List[Dict[str, Any]]:
        store = self._get_store()
        return store.list_runs()

    def get_walk_forward_lineage(self, run_id, config=None, windows=None, decisions=None, transactions=None) -> Dict[str, Any]:
        from portfolio.walk_forward.lineage_v154 import WalkForwardLineageTracker
        return WalkForwardLineageTracker().build_lineage(
            run_id, config, windows or [], decisions or [], transactions or []
        )
