"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.contribution_engine_v167 import ContributionEngine


def _engine():
    return ContributionEngine()


def test_contribution_engine_instantiates():
    assert _engine() is not None


def test_contribution_engine_has_return_contribution():
    assert callable(getattr(_engine(), "return_contribution", None))


def test_contribution_engine_has_percent_contribution():
    assert callable(getattr(_engine(), "percent_contribution", None))


def test_contribution_engine_has_amount_contribution():
    assert callable(getattr(_engine(), "amount_contribution", None))


def test_contribution_engine_has_top_n():
    assert callable(getattr(_engine(), "top_n", None))


def test_contribution_engine_has_bottom_n():
    assert callable(getattr(_engine(), "bottom_n", None))


def test_contribution_engine_has_reconcile_parent_child():
    assert callable(getattr(_engine(), "reconcile_parent_child", None))


def test_contribution_engine_has_hierarchical_aggregate():
    assert callable(getattr(_engine(), "hierarchical_aggregate", None))


def test_contribution_engine_has_normalized_contribution():
    assert callable(getattr(_engine(), "normalized_contribution", None))


def test_contribution_engine_has_bps_contribution():
    assert callable(getattr(_engine(), "bps_contribution", None))


def test_contribution_engine_has_handle_missing():
    assert callable(getattr(_engine(), "handle_missing", None))


def test_contribution_engine_has_rounding_control():
    assert callable(getattr(_engine(), "rounding_control", None))


def test_return_contribution_positive():
    e = _engine()
    result = e.return_contribution("AAPL", entity_return=0.10, entity_weight=0.4)
    assert abs(result - 0.04) < 1e-9


def test_return_contribution_negative():
    e = _engine()
    result = e.return_contribution("TSLA", entity_return=-0.05, entity_weight=0.2)
    assert abs(result - (-0.01)) < 1e-9


def test_percent_contribution_half():
    e = _engine()
    # percent_contribution returns a percentage value (50.0 = 50%)
    result = e.percent_contribution("X", entity_pnl=250.0, portfolio_pnl=500.0)
    assert abs(result - 50.0) < 1e-9


def test_reconcile_parent_child_exact():
    e = _engine()
    result = e.reconcile_parent_child(parent_value=1000.0, child_sum=1000.0)
    assert result["reconciled"] is True


def test_reconcile_parent_child_drift():
    e = _engine()
    result = e.reconcile_parent_child(parent_value=1000.0, child_sum=1001.0)
    assert isinstance(result, dict)
    assert "residual" in result or "reconciled" in result


def test_top_n_top_two():
    e = _engine()
    items = [
        {"id": "A", "val": 0.10},
        {"id": "B", "val": 0.25},
        {"id": "C", "val": 0.05},
        {"id": "D", "val": 0.15},
    ]
    result = e.top_n(items, value_key="val", id_key="id", n=2)
    assert len(result) == 2


def test_bottom_n_bottom_one():
    e = _engine()
    items = [
        {"id": "A", "val": 0.10},
        {"id": "B", "val": 0.25},
        {"id": "C", "val": 0.05},
    ]
    result = e.bottom_n(items, value_key="val", id_key="id", n=1)
    assert len(result) == 1
