"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.turnover_attribution_v167 import TurnoverAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel


def _engine():
    return TurnoverAttributionEngine()


def _trade(quantity=100.0, fill_price=100.0, direction=1):
    return {
        "trade_id": "t1",
        "quantity": quantity,
        "fill_price": fill_price,
        "direction": direction,
        "simulated": True,
    }


def _compute(**kwargs):
    defaults = dict(
        entity_id="p1",
        level=AttributionLevel.PORTFOLIO,
        trades=[_trade()],
        begin_equity=100_000.0,
        cost_per_turn=0.002,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_turnover_engine_instantiates():
    assert _engine() is not None


def test_turnover_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_turnover_compute_returns_turnover_contribution():
    result = _compute()
    assert type(result).__name__ == "TurnoverContribution"


def test_turnover_compute_entity_id_stored():
    result = _compute(entity_id="strategy-B")
    assert result.entity_id == "strategy-B"


def test_turnover_compute_level_stored():
    result = _compute(level=AttributionLevel.STRATEGY)
    assert result.level == AttributionLevel.STRATEGY


def test_turnover_compute_paper_only_true():
    result = _compute()
    assert result.paper_only is True


def test_turnover_compute_research_only_true():
    result = _compute()
    assert result.research_only is True


def test_turnover_compute_no_real_orders_true():
    result = _compute()
    assert result.no_real_orders is True


def test_turnover_compute_empty_trades():
    result = _compute(trades=[])
    assert type(result).__name__ == "TurnoverContribution"


def test_turnover_compute_multiple_trades():
    trades = [_trade(), _trade(quantity=200.0), _trade(direction=-1)]
    result = _compute(trades=trades)
    assert type(result).__name__ == "TurnoverContribution"


def test_turnover_compute_status_exists():
    result = _compute()
    assert hasattr(result, "status")


def test_turnover_compute_turnover_rate_exists():
    result = _compute()
    assert hasattr(result, "turnover_rate")
