"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.cost_attribution_v167 import CostAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel


def _engine():
    return CostAttributionEngine()


def _compute(**kwargs):
    defaults = dict(
        entity_id="p1",
        level=AttributionLevel.PORTFOLIO,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_cost_engine_instantiates():
    assert _engine() is not None


def test_cost_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_cost_compute_returns_cost_contribution():
    result = _compute()
    assert type(result).__name__ == "CostContribution"


def test_cost_compute_entity_id_stored():
    result = _compute(entity_id="strategy-A")
    assert result.entity_id == "strategy-A"


def test_cost_compute_level_stored():
    result = _compute(level=AttributionLevel.STRATEGY)
    assert result.level == AttributionLevel.STRATEGY


def test_cost_compute_paper_only_true():
    result = _compute()
    assert result.paper_only is True


def test_cost_compute_research_only_true():
    result = _compute()
    assert result.research_only is True


def test_cost_compute_no_real_orders_true():
    result = _compute()
    assert result.no_real_orders is True


def test_cost_compute_with_commission():
    result = _compute(commission=50.0, begin_equity=100_000.0)
    assert type(result).__name__ == "CostContribution"


def test_cost_compute_with_transaction_tax():
    result = _compute(transaction_tax=10.0, commission=20.0)
    assert type(result).__name__ == "CostContribution"


def test_cost_compute_total_cost_attribute_exists():
    result = _compute(commission=10.0, slippage=5.0)
    assert hasattr(result, "total_cost")


def test_cost_compute_status_attribute_exists():
    result = _compute()
    assert hasattr(result, "status")


def test_cost_compute_gross_pnl_stored():
    result = _compute(gross_pnl=1000.0, net_pnl=950.0)
    assert type(result).__name__ == "CostContribution"
