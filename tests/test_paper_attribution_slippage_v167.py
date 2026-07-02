"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.slippage_attribution_v167 import SlippageAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel


def _engine():
    return SlippageAttributionEngine()


def _trade(fill_price=100.0, signal_price=99.5, quantity=100.0, direction=1):
    return {
        "trade_id": "t1",
        "fill_price": fill_price,
        "signal_price": signal_price,
        "decision_price": signal_price,
        "order_price": signal_price,
        "close_price": 100.0,
        "vwap": 100.1,
        "twap": 100.05,
        "quantity": quantity,
        "direction": direction,
        "simulated": True,
    }


def _compute(**kwargs):
    defaults = dict(
        entity_id="p1",
        level=AttributionLevel.PORTFOLIO,
        trades=[_trade()],
        begin_equity=100_000.0,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_slippage_engine_instantiates():
    assert _engine() is not None


def test_slippage_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_slippage_compute_returns_slippage_contribution():
    result = _compute()
    assert type(result).__name__ == "SlippageContribution"


def test_slippage_compute_entity_id_stored():
    result = _compute(entity_id="sym-AAPL")
    assert result.entity_id == "sym-AAPL"


def test_slippage_compute_level_stored():
    result = _compute(level=AttributionLevel.SYMBOL)
    assert result.level == AttributionLevel.SYMBOL


def test_slippage_compute_paper_only_true():
    result = _compute()
    assert result.paper_only is True


def test_slippage_compute_research_only_true():
    result = _compute()
    assert result.research_only is True


def test_slippage_compute_no_real_orders_true():
    result = _compute()
    assert result.no_real_orders is True


def test_slippage_compute_empty_trades():
    result = _compute(trades=[])
    assert type(result).__name__ == "SlippageContribution"


def test_slippage_compute_multiple_trades():
    trades = [_trade(), _trade(fill_price=101.0), _trade(direction=-1)]
    result = _compute(trades=trades)
    assert type(result).__name__ == "SlippageContribution"


def test_slippage_compute_status_exists():
    result = _compute()
    assert hasattr(result, "status")


def test_slippage_compute_total_slippage_exists():
    result = _compute()
    assert hasattr(result, "total_slippage")
