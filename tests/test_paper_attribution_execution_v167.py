"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.execution_attribution_v167 import ExecutionAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel, ExecutionQuality


def _engine():
    return ExecutionAttributionEngine()


def _compute(**kwargs):
    defaults = dict(
        entity_id="t1",
        level=AttributionLevel.TRADE,
        fill_price=100.0,
        signal_price=None,
        decision_price=None,
        order_price=None,
        close_price=None,
        vwap=None,
        twap=None,
        quantity=100.0,
        direction=1,
        filled_quantity=100.0,
        ordered_quantity=100.0,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_execution_engine_instantiates():
    assert _engine() is not None


def test_execution_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_execution_compute_returns_execution_contribution():
    result = _compute()
    assert type(result).__name__ == "ExecutionContribution"


def test_execution_compute_entity_id_stored():
    result = _compute(entity_id="trade-42")
    assert result.entity_id == "trade-42"


def test_execution_compute_level_stored():
    result = _compute(level=AttributionLevel.TRADE)
    assert result.level == AttributionLevel.TRADE


def test_execution_compute_paper_only_true():
    result = _compute()
    assert result.paper_only is True


def test_execution_compute_research_only_true():
    result = _compute()
    assert result.research_only is True


def test_execution_compute_no_real_orders_true():
    result = _compute()
    assert result.no_real_orders is True


def test_execution_compute_with_signal_price():
    result = _compute(signal_price=99.5, fill_price=100.0)
    assert isinstance(result.entity_id, str)


def test_execution_compute_with_vwap():
    result = _compute(vwap=100.2, fill_price=100.0)
    assert type(result).__name__ == "ExecutionContribution"


def test_execution_compute_slippage_attribute_exists():
    result = _compute()
    assert hasattr(result, "slippage")


def test_execution_compute_fill_ratio_exists():
    result = _compute(filled_quantity=90.0, ordered_quantity=100.0)
    assert hasattr(result, "fill_ratio")


def test_execution_compute_status_attribute_exists():
    result = _compute()
    assert hasattr(result, "status")


def test_execution_compute_short_direction():
    result = _compute(direction=-1, fill_price=100.0, close_price=90.0)
    assert type(result).__name__ == "ExecutionContribution"
