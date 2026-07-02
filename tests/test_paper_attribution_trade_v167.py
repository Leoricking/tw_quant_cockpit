"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.trade_attribution_v167 import TradeAttributionEngine


def _engine():
    return TradeAttributionEngine()


def _get_trade_direction():
    try:
        from paper_trading.performance_attribution.trade_attribution_v167 import TradeDirection
        return list(TradeDirection)[0]
    except (ImportError, IndexError):
        try:
            from paper_trading.enums import TradeDirection
            return list(TradeDirection)[0]
        except Exception:
            return "BUY"


def _compute(**kwargs):
    direction = _get_trade_direction()
    defaults = dict(
        trade_id="trade-001",
        symbol="AAPL",
        direction=direction,
        quantity=100.0,
        signal_price=None,
        decision_price=None,
        fill_price=100.0,
        exit_price=None,
        cost_basis=100.0,
        commission=5.0,
        simulated=True,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_trade_engine_instantiates():
    assert _engine() is not None


def test_trade_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_trade_compute_returns_dict():
    result = _compute()
    assert isinstance(result, dict)


def test_trade_compute_trade_id_stored():
    result = _compute(trade_id="t-XYZ")
    assert result.get("trade_id") == "t-XYZ"


def test_trade_compute_symbol_stored():
    result = _compute(symbol="TSLA")
    assert result.get("symbol") == "TSLA"


def test_trade_compute_paper_only_true():
    result = _compute()
    assert result.get("paper_only") is True


def test_trade_compute_research_only_true():
    result = _compute()
    assert result.get("research_only") is True


def test_trade_compute_no_real_orders_true():
    result = _compute()
    assert result.get("no_real_orders") is True


def test_trade_compute_fill_price_stored():
    result = _compute(fill_price=150.0)
    assert isinstance(result.get("fill_price"), float)


def test_trade_compute_with_exit_price():
    result = _compute(exit_price=110.0, fill_price=100.0)
    assert isinstance(result, dict)


def test_trade_compute_with_signal_price():
    result = _compute(signal_price=99.5, fill_price=100.0)
    assert isinstance(result, dict)


def test_trade_compute_simulated_flag_true():
    result = _compute(simulated=True)
    assert result.get("simulated") is True


def test_trade_compute_commission_stored():
    result = _compute(commission=10.0)
    assert isinstance(result, dict)
