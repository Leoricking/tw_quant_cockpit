"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.contribution_engine_v167 import ContributionEngine


def test_contribution_engine_instantiates():
    engine = ContributionEngine()
    assert engine is not None


def test_contribution_engine_has_return_contribution():
    engine = ContributionEngine()
    assert hasattr(engine, "return_contribution")
    assert callable(engine.return_contribution)


def test_contribution_engine_has_percent_contribution():
    engine = ContributionEngine()
    assert hasattr(engine, "percent_contribution")
    assert callable(engine.percent_contribution)


def test_contribution_engine_has_amount_contribution():
    engine = ContributionEngine()
    assert hasattr(engine, "amount_contribution")
    assert callable(engine.amount_contribution)


def test_contribution_engine_has_top_n():
    engine = ContributionEngine()
    assert hasattr(engine, "top_n")
    assert callable(engine.top_n)


def test_contribution_engine_has_reconcile_parent_child():
    engine = ContributionEngine()
    assert hasattr(engine, "reconcile_parent_child")
    assert callable(engine.reconcile_parent_child)


def test_return_contribution_basic():
    engine = ContributionEngine()
    result = engine.return_contribution("AAPL", entity_return=0.05, entity_weight=0.5)
    assert isinstance(result, float)
    assert abs(result - 0.025) < 1e-9


def test_return_contribution_zero_weight():
    engine = ContributionEngine()
    result = engine.return_contribution("AAPL", entity_return=0.10, entity_weight=0.0)
    assert result == 0.0


def test_percent_contribution_basic():
    engine = ContributionEngine()
    # percent_contribution returns a percentage value (50.0 means 50%)
    result = engine.percent_contribution("AAPL", entity_pnl=500.0, portfolio_pnl=1000.0)
    assert isinstance(result, float)
    assert abs(result - 50.0) < 1e-9


def test_percent_contribution_full_portfolio():
    engine = ContributionEngine()
    result = engine.percent_contribution("p", entity_pnl=1000.0, portfolio_pnl=1000.0)
    assert abs(result - 100.0) < 1e-9


def test_amount_contribution_basic():
    engine = ContributionEngine()
    result = engine.amount_contribution("TSLA", pnl=200.0, portfolio_pnl=1000.0)
    assert isinstance(result, float)


def test_top_n_returns_list():
    engine = ContributionEngine()
    items = [
        {"id": "A", "val": 0.10},
        {"id": "B", "val": 0.05},
        {"id": "C", "val": 0.20},
    ]
    result = engine.top_n(items, value_key="val", id_key="id", n=2)
    assert isinstance(result, list)
    assert len(result) == 2


def test_reconcile_parent_child_exact_match():
    engine = ContributionEngine()
    result = engine.reconcile_parent_child(parent_value=1000.0, child_sum=1000.0)
    assert result["reconciled"] is True


def test_reconcile_parent_child_within_tolerance():
    engine = ContributionEngine()
    result = engine.reconcile_parent_child(parent_value=1000.0, child_sum=1000.000000005, tolerance=1e-6)
    assert isinstance(result, dict)
