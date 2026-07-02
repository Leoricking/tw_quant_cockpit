"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.allocation_attribution_v167 import AllocationAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel, BenchmarkMode


def _engine():
    return AllocationAttributionEngine()


def _compute(entity_id="p1", level=AttributionLevel.PORTFOLIO,
             pw=None, bw=None, pr=None, br=None, bm=BenchmarkMode.NONE):
    pw = pw or {"AAPL": 0.5, "TSLA": 0.5}
    pr = pr or {"AAPL": 0.05, "TSLA": 0.03}
    return _engine().compute(
        entity_id=entity_id,
        level=level,
        portfolio_weights=pw,
        benchmark_weights=bw,
        portfolio_returns=pr,
        benchmark_returns=br,
        benchmark_mode=bm,
    )


def test_allocation_engine_instantiates():
    assert _engine() is not None


def test_allocation_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_allocation_compute_returns_allocation_contribution():
    result = _compute()
    assert type(result).__name__ == "AllocationContribution"


def test_allocation_compute_entity_id_stored():
    result = _compute(entity_id="strat-A")
    assert result.entity_id == "strat-A"


def test_allocation_compute_allocation_return_is_float():
    result = _compute()
    assert isinstance(result.allocation_return, float)


def test_allocation_compute_paper_only_true():
    result = _compute()
    assert result.paper_only is True


def test_allocation_compute_research_only_true():
    result = _compute()
    assert result.research_only is True


def test_allocation_compute_no_real_orders_true():
    result = _compute()
    assert result.no_real_orders is True


def test_allocation_compute_benchmark_mode_stored():
    result = _compute(bm=BenchmarkMode.NONE)
    assert result.benchmark_mode == BenchmarkMode.NONE


def test_allocation_compute_level_stored():
    result = _compute(level=AttributionLevel.STRATEGY)
    assert result.level == AttributionLevel.STRATEGY


def test_allocation_compute_with_benchmark_weights():
    result = _compute(
        bw={"AAPL": 0.6, "TSLA": 0.4},
        br={"AAPL": 0.04, "TSLA": 0.02},
        bm=BenchmarkMode.MARKET_BENCHMARK,
    )
    assert isinstance(result.allocation_return, float)


def test_allocation_compute_status_attribute_exists():
    result = _compute()
    assert hasattr(result, "status")


def test_allocation_compute_capital_utilization_effect_exists():
    result = _compute()
    assert hasattr(result, "capital_utilization_effect")


def test_allocation_compute_idle_cash_drag_exists():
    result = _compute()
    assert hasattr(result, "idle_cash_drag")
