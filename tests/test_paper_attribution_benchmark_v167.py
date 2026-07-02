"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.benchmark_attribution_v167 import BenchmarkAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel, BenchmarkMode


def _engine():
    return BenchmarkAttributionEngine()


def _compute(**kwargs):
    defaults = dict(
        entity_id="p1",
        level=AttributionLevel.PORTFOLIO,
        portfolio_return=0.05,
        benchmark_id=None,
        benchmark_mode=BenchmarkMode.NONE,
        benchmark_returns=None,
        benchmark_weights=None,
        benchmark_period_start=None,
        benchmark_period_end=None,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_benchmark_engine_instantiates():
    assert _engine() is not None


def test_benchmark_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_benchmark_compute_returns_benchmark_contribution():
    result = _compute()
    assert type(result).__name__ == "BenchmarkContribution"


def test_benchmark_compute_entity_id_stored():
    result = _compute(entity_id="port-bench")
    assert result.entity_id == "port-bench"


def test_benchmark_compute_level_stored():
    result = _compute(level=AttributionLevel.PORTFOLIO)
    assert result.level == AttributionLevel.PORTFOLIO


def test_benchmark_compute_paper_only_true():
    result = _compute()
    assert result.paper_only is True


def test_benchmark_compute_research_only_true():
    result = _compute()
    assert result.research_only is True


def test_benchmark_compute_no_real_orders_true():
    result = _compute()
    assert result.no_real_orders is True


def test_benchmark_compute_with_benchmark_id():
    result = _compute(
        benchmark_id="SPX",
        benchmark_mode=BenchmarkMode.MARKET_BENCHMARK,
        benchmark_returns={"SPX": 0.04},
        benchmark_weights={"SPX": 1.0},
        benchmark_period_start="2026-01-01",
        benchmark_period_end="2026-06-30",
    )
    assert type(result).__name__ == "BenchmarkContribution"


def test_benchmark_compute_none_mode():
    result = _compute(benchmark_mode=BenchmarkMode.NONE)
    assert result.benchmark_mode == BenchmarkMode.NONE


def test_benchmark_compute_status_exists():
    result = _compute()
    assert hasattr(result, "status")


def test_benchmark_compute_active_return_exists():
    result = _compute()
    assert hasattr(result, "active_return")
