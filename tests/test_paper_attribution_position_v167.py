"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.position_attribution_v167 import PositionAttributionEngine


def _engine():
    return PositionAttributionEngine()


def _get_position_state():
    try:
        from paper_trading.performance_attribution.position_attribution_v167 import PositionState
        return list(PositionState)[0]
    except (ImportError, IndexError):
        try:
            from paper_trading.enums import PositionState
            return list(PositionState)[0]
        except Exception:
            return "OPEN"


def _compute(**kwargs):
    state = _get_position_state()
    defaults = dict(
        position_id="pos-001",
        symbol="AAPL",
        open_date="2026-01-10",
        close_date=None,
        average_cost=150.0,
        current_price=160.0,
        quantity=100.0,
        state=state,
        realized_pnl=0.0,
        unrealized_pnl=1000.0,
        cost=50.0,
        risk_contribution=0.005,
        drawdown=-0.01,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_position_engine_instantiates():
    assert _engine() is not None


def test_position_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_position_compute_returns_dict():
    result = _compute()
    assert isinstance(result, dict)


def test_position_compute_position_id_stored():
    result = _compute(position_id="pos-XYZ")
    assert result.get("position_id") == "pos-XYZ"


def test_position_compute_symbol_stored():
    result = _compute(symbol="TSLA")
    assert result.get("symbol") == "TSLA"


def test_position_compute_paper_only_true():
    result = _compute()
    assert result.get("paper_only") is True


def test_position_compute_research_only_true():
    result = _compute()
    assert result.get("research_only") is True


def test_position_compute_no_real_orders_true():
    result = _compute()
    assert result.get("no_real_orders") is True


def test_position_compute_unrealized_pnl_stored():
    result = _compute(unrealized_pnl=2000.0)
    assert isinstance(result.get("unrealized_pnl"), float)


def test_position_compute_with_close_date():
    result = _compute(close_date="2026-06-30", realized_pnl=1000.0)
    assert isinstance(result, dict)


def test_position_compute_with_add_on_trades():
    result = _compute(add_on_trades=[{"trade_id": "t2", "quantity": 50.0}])
    assert isinstance(result, dict)


def test_position_compute_with_holding_days():
    result = _compute(holding_days=30)
    assert isinstance(result, dict)
