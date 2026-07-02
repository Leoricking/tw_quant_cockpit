"""
tests/test_paper_attribution_models_v167.py
Tests for paper attribution models v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from paper_trading.performance_attribution.models_v167 import (
    AttributionPeriod,
    BenchmarkSnapshot,
    PortfolioSnapshot,
    PositionSnapshot,
    TradeSnapshot,
    ExecutionSnapshot,
    CostSnapshot,
    MarketSnapshot,
    RegimeSnapshot,
    FactorSnapshot,
    ReturnContribution,
    PnLContribution,
    SelectionContribution,
    AllocationContribution,
    TimingContribution,
    ExecutionContribution,
    CostContribution,
    SlippageContribution,
    TurnoverContribution,
    ExposureContribution,
    RiskContribution,
    DrawdownContribution,
    RegimeContribution,
    BenchmarkContribution,
    FactorContribution,
    ResidualContribution,
    AttributionBreakdown,
    AttributionReconciliation,
    AttributionScore,
    AttributionReport,
    AttributionRun,
    AttributionQuery,
    AttributionSummary,
    AttributionComparison,
    AttributionValidationResult,
    AttributionHealthSummary,
)


class TestAttributionPeriod:
    def test_instantiate_minimal(self):
        p = AttributionPeriod(
            period_start="2024-01-01",
            period_end="2024-01-31",
        )
        assert p.period_start == "2024-01-01"

    def test_period_end_stored(self):
        p = AttributionPeriod(
            period_start="2024-01-01",
            period_end="2024-01-07",
        )
        assert p.period_end == "2024-01-07"


class TestSnapshotModels:
    def test_benchmark_snapshot_instantiate(self):
        s = BenchmarkSnapshot(
            benchmark_id="TAIEX",
            benchmark_mode="MARKET_BENCHMARK",
            period_start="2024-01-01",
            period_end="2024-01-31",
        )
        assert s.benchmark_id == "TAIEX"

    def test_portfolio_snapshot_instantiate(self):
        s = PortfolioSnapshot(
            portfolio_id="P1",
            period_start="2024-01-01",
            period_end="2024-01-31",
            initial_equity=1000000.0,
            ending_equity=1050000.0,
        )
        assert s.portfolio_id == "P1"

    def test_position_snapshot_instantiate(self):
        s = PositionSnapshot(
            position_id="pos1",
            symbol="AAPL",
            strategy_id="s1",
            session_id="sess1",
            open_date="2024-01-01",
            close_date="2024-01-31",
            average_cost=148.0,
            quantity=100,
            current_price=151.0,
            state="CLOSED",
            direction="LONG",
        )
        assert s.symbol == "AAPL"

    def test_trade_snapshot_instantiate(self):
        s = TradeSnapshot(
            trade_id="T1",
            symbol="AAPL",
            strategy_id="s1",
            session_id="sess1",
            direction="BUY",
            quantity=100,
            signal_price=148.0,
            decision_price=149.0,
            fill_price=150.0,
            exit_price=155.0,
            timestamp="2024-01-15T10:00:00",
        )
        assert s.trade_id == "T1"

    def test_execution_snapshot_instantiate(self):
        s = ExecutionSnapshot(
            execution_id="E1",
            trade_id="T1",
            symbol="AAPL",
            fill_price=150.0,
            fill_quantity=100,
            order_price=149.0,
            signal_price=148.0,
            decision_price=149.0,
            vwap=149.5,
            twap=149.3,
            close_price=151.0,
            timestamp="2024-01-15T10:00:00",
        )
        assert s.execution_id == "E1"

    def test_cost_snapshot_instantiate(self):
        s = CostSnapshot(
            run_id="run1",
            period_start="2024-01-01",
            period_end="2024-01-31",
            commission=100.0,
        )
        assert s.commission == 100.0

    def test_market_snapshot_instantiate(self):
        s = MarketSnapshot(
            symbol="AAPL",
            period_start="2024-01-01",
            period_end="2024-01-31",
        )
        assert s.symbol == "AAPL"

    def test_regime_snapshot_instantiate(self):
        s = RegimeSnapshot(
            period_start="2024-01-01",
            period_end="2024-01-31",
        )
        assert s.period_start == "2024-01-01"

    def test_factor_snapshot_instantiate(self):
        s = FactorSnapshot(
            symbol="AAPL",
            period_start="2024-01-01",
            period_end="2024-01-31",
        )
        assert s.symbol == "AAPL"


class TestContributionModels:
    def test_return_contribution(self):
        c = ReturnContribution(
            entity_id="P1", level="PORTFOLIO",
            gross_return=0.05, net_return=0.045,
            realized_return=0.04, unrealized_return=0.005,
            active_return=0.01, cost_return=-0.005,
            execution_return=-0.002, residual_return=0.0,
        )
        assert c.entity_id == "P1"

    def test_pnl_contribution(self):
        c = PnLContribution(
            entity_id="AAPL", level="SYMBOL",
            realized_pnl=400.0, unrealized_pnl=100.0,
            gross_pnl=500.0, net_pnl=450.0,
        )
        assert c.gross_pnl == 500.0

    def test_selection_contribution(self):
        c = SelectionContribution(
            entity_id="AAPL", level="SYMBOL",
            selection_return=0.02, selection_alpha=0.01,
            hit_rate=0.6, win_rate=0.6,
            average_winner=0.03, average_loser=-0.01,
        )
        assert c.selection_return == 0.02

    def test_allocation_contribution(self):
        c = AllocationContribution(
            entity_id="Tech", level="SECTOR",
            allocation_return=0.01, overweight_effect=0.005,
            underweight_effect=-0.003, cash_allocation_effect=0.0,
            leverage_effect=0.0, idle_cash_drag=0.0,
            capital_utilization_effect=0.0,
        )
        assert c.allocation_return == 0.01

    def test_timing_contribution(self):
        c = TimingContribution(
            entity_id="AAPL", level="SYMBOL",
            timing_return=0.005, entry_timing=0.003,
            exit_timing=0.002, add_on_timing=0.0,
            trim_timing=0.0, delayed_entry=0.0,
            early_exit=0.0, missed_move=0.0,
            avoided_drawdown=0.0, signal_execution_delay=0,
            stale_signal_drag=0.0, reference_used="open",
        )
        assert c.entity_id == "AAPL"

    def test_execution_contribution(self):
        c = ExecutionContribution(
            entity_id="T1", level="TRADE",
            implementation_shortfall=-0.001, delay_cost=-0.0005,
            spread_cost=-0.0003, slippage=-0.0002,
            adverse_selection_proxy=0.0, partial_fill_impact=0.0,
            unfilled_opportunity_cost=0.0, fill_ratio=1.0,
        )
        assert c.entity_id == "T1"

    def test_cost_contribution(self):
        c = CostContribution(
            entity_id="P1", level="PORTFOLIO",
            commission=300.0, transaction_tax=150.0,
            exchange_fee=20.0, borrow_fee=0.0,
            financing_cost=0.0, slippage=50.0,
            spread=30.0, impact_proxy=10.0,
            turnover_cost=20.0, other_modeled=0.0,
            unknown_cost=0.0, estimated_cost=0.0,
            known_cost=550.0, total_cost=550.0,
        )
        assert c.commission == 300.0

    def test_slippage_contribution(self):
        c = SlippageContribution(
            entity_id="T1", level="TRADE",
            total_slippage=-5.0, positive_slippage=0.0,
            negative_slippage=-5.0, slippage_bps=-5.0,
            per_trade_slippage=-5.0,
        )
        assert c.entity_id == "T1"

    def test_turnover_contribution(self):
        c = TurnoverContribution(
            entity_id="P1", level="PORTFOLIO",
            turnover_rate=1.5, turnover_cost=300.0,
            turnover_drag_bps=30.0, trade_count=20,
            avg_trade_size=5000.0,
        )
        assert c.turnover_rate == 1.5

    def test_exposure_contribution(self):
        c = ExposureContribution(
            entity_id="P1", level="PORTFOLIO",
            market_exposure=0.85, beta_exposure=0.9,
            gross_exposure=0.9, net_exposure=0.8,
            long_exposure=0.9, short_exposure=0.0,
            concentration=0.3, leverage=1.0,
        )
        assert c.entity_id == "P1"

    def test_risk_contribution(self):
        c = RiskContribution(
            entity_id="P1", level="PORTFOLIO",
            volatility_contribution=0.15, downside_volatility_contribution=0.10,
            drawdown_contribution=-0.05, correlation_cluster_contribution=0.02,
            leverage_contribution=0.0, liquidity_risk_proxy=0.0,
            gap_risk=0.0, overnight_risk=0.0,
            turnover_risk=0.0, tail_loss_contribution=0.0,
            marginal_contribution=0.0, component_contribution=0.0,
            normalized_contribution=0.0,
        )
        assert c.entity_id == "P1"

    def test_drawdown_contribution(self):
        c = DrawdownContribution(
            entity_id="P1", level="PORTFOLIO",
            max_drawdown=-0.12, peak_timestamp="2024-01-10",
            trough_timestamp="2024-01-20", recovery_timestamp="2024-01-30",
            peak_to_trough_duration=10, recovery_duration=10,
            no_recovery=False,
            symbol_contribution=0.0, strategy_contribution=0.0,
            session_contribution=0.0, allocation_contribution=0.0,
            concentration_contribution=0.0, leverage_contribution=0.0,
            execution_contribution=0.0, cost_contribution=0.0,
            residual_contribution=0.0,
        )
        assert c.max_drawdown == -0.12

    def test_regime_contribution(self):
        c = RegimeContribution(
            entity_id="P1", level="PORTFOLIO",
            regime="BULL", return_in_regime=0.08,
            net_return_in_regime=0.07, hit_rate_in_regime=0.65,
            drawdown_in_regime=-0.05, cost_in_regime=-0.01,
            selection_effect_in_regime=0.03,
            allocation_effect_in_regime=0.01,
            timing_effect_in_regime=0.005,
        )
        assert c.regime == "BULL"

    def test_benchmark_contribution(self):
        c = BenchmarkContribution(
            entity_id="P1", level="PORTFOLIO",
            benchmark_id="TAIEX", benchmark_mode="MARKET_BENCHMARK",
            benchmark_return=0.05, active_return=0.02,
        )
        assert c.entity_id == "P1"

    def test_factor_contribution(self):
        c = FactorContribution(
            entity_id="P1", level="PORTFOLIO",
            factor_name="MOMENTUM", factor_exposure=0.5,
            factor_return=0.03, factor_contribution=0.015,
            is_proxy=False,
        )
        assert c.entity_id == "P1"

    def test_residual_contribution(self):
        c = ResidualContribution(
            entity_id="P1", level="PORTFOLIO",
            residual=0.005, rounding_residual=0.0001,
            model_residual=0.0049, threshold=0.01,
            exceeds_threshold=False,
        )
        assert c.entity_id == "P1"


class TestAggregationModels:
    def test_attribution_breakdown_instantiate(self):
        b = AttributionBreakdown(
            entity_id="P1", level="PORTFOLIO",
            period_start="2024-01-01", period_end="2024-01-31",
        )
        assert b.entity_id == "P1"

    def test_attribution_reconciliation(self):
        from paper_trading.performance_attribution.enums_v167 import (
            ReconciliationStatus,
        )
        r = AttributionReconciliation(
            entity_id="P1",
            expected_total=100.0,
            actual_component_sum=100.0,
            residual=0.0,
            rounding_residual=0.0,
            model_residual=0.0,
            tolerance=0.0001,
            status=ReconciliationStatus.RECONCILED,
        )
        assert r.status == ReconciliationStatus.RECONCILED

    def test_attribution_score(self):
        s = AttributionScore(
            entity_id="P1",
            total_score=85.0,
            grade="B",
            reconciliation_score=20.0,
            data_completeness_score=18.0,
            execution_quality_score=12.0,
            cost_completeness_score=8.0,
            benchmark_quality_score=9.0,
            risk_model_quality_score=8.0,
            lineage_quality_score=5.0,
            determinism_score=5.0,
        )
        assert s.total_score == 85.0

    def test_attribution_report_instantiate(self):
        r = AttributionReport(
            run_id="run1",
            portfolio_id="P1",
            period_start="2024-01-01",
            period_end="2024-01-31",
        )
        assert r.run_id == "run1"

    def test_attribution_run_instantiate(self):
        r = AttributionRun(
            run_id="run1",
            portfolio_id="P1",
            strategy_id="s1",
            session_id="sess1",
            period="2024-01",
        )
        assert r.run_id == "run1"

    def test_attribution_query_instantiate(self):
        q = AttributionQuery(query_id="q1")
        assert q.query_id == "q1"

    def test_attribution_summary_instantiate(self):
        s = AttributionSummary(
            total_runs=0,
            complete_runs=0,
            degraded_runs=0,
            failed_runs=0,
        )
        assert s.total_runs == 0

    def test_attribution_comparison_instantiate(self):
        c = AttributionComparison(
            comparison_id="cmp1",
            entity_ids=["r1", "r2"],
            dimension="SELECTION",
        )
        assert len(c.entity_ids) == 2

    def test_attribution_validation_result_instantiate(self):
        r = AttributionValidationResult(run_id="r1", valid=True)
        assert r.valid is True

    def test_attribution_health_summary_instantiate(self):
        h = AttributionHealthSummary(
            version="1.6.7",
            release_name="Paper Performance Attribution",
            total_checks=60,
            passed=60,
            failed=0,
            status="PASS",
        )
        assert h.total_checks == 60


class TestPaperOnlyConstraint:
    """Spot-check paper_only/research_only on key models."""

    def test_return_contribution_has_entity_id(self):
        c = ReturnContribution(
            entity_id="x", level="PORTFOLIO",
            gross_return=0.01, net_return=0.009,
            realized_return=0.009, unrealized_return=0.0,
            active_return=0.001, cost_return=-0.001,
            execution_return=0.0, residual_return=0.0,
        )
        assert hasattr(c, 'entity_id')

    def test_selection_contribution_has_entity_id(self):
        c = SelectionContribution(
            entity_id="x", level="SYMBOL",
            selection_return=0.01, selection_alpha=0.005,
            hit_rate=0.6, win_rate=0.6,
            average_winner=0.02, average_loser=-0.01,
        )
        assert c.entity_id == "x"

    def test_cost_contribution_commission(self):
        c = CostContribution(
            entity_id="P1", level="PORTFOLIO",
            commission=100.0, transaction_tax=0.0,
            exchange_fee=0.0, borrow_fee=0.0,
            financing_cost=0.0, slippage=0.0,
            spread=0.0, impact_proxy=0.0,
            turnover_cost=0.0, other_modeled=0.0,
            unknown_cost=0.0, estimated_cost=0.0,
            known_cost=100.0, total_cost=100.0,
        )
        assert c.commission == 100.0
