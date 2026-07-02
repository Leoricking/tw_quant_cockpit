"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.strategy_attribution_v167 import StrategyAttributionEngine
from paper_trading.performance_attribution.enums_v167 import BenchmarkMode


def _engine():
    return StrategyAttributionEngine()


def _compute(**kwargs):
    defaults = dict(
        strategy_id="strat-A",
        strategy_return=0.04,
        strategy_gross_pnl=4000.0,
        strategy_net_pnl=3800.0,
        strategy_cost=200.0,
        selection_effect=0.02,
        allocation_effect=0.01,
        timing_effect=0.005,
        risk_contribution=0.003,
        drawdown_contribution=-0.001,
        turnover=0.5,
        capital_usage=0.8,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_strategy_engine_instantiates():
    assert _engine() is not None


def test_strategy_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_strategy_compute_returns_dict():
    result = _compute()
    assert isinstance(result, dict)


def test_strategy_compute_strategy_id_stored():
    result = _compute(strategy_id="my-strategy")
    assert result.get("strategy_id") == "my-strategy"


def test_strategy_compute_strategy_return_stored():
    result = _compute(strategy_return=0.06)
    assert abs(result.get("strategy_return", 0) - 0.06) < 1e-9


def test_strategy_compute_paper_only_true():
    result = _compute()
    assert result.get("paper_only") is True


def test_strategy_compute_research_only_true():
    result = _compute()
    assert result.get("research_only") is True


def test_strategy_compute_no_real_orders_true():
    result = _compute()
    assert result.get("no_real_orders") is True


def test_strategy_compute_with_benchmark_return():
    result = _compute(benchmark_return=0.03, benchmark_mode=BenchmarkMode.MARKET_BENCHMARK)
    assert isinstance(result, dict)


def test_strategy_compute_selection_effect_stored():
    result = _compute(selection_effect=0.015)
    assert isinstance(result.get("selection_effect"), float)


def test_strategy_compute_allocation_effect_stored():
    result = _compute(allocation_effect=0.008)
    assert isinstance(result.get("allocation_effect"), float)


def test_strategy_compute_timing_effect_stored():
    result = _compute(timing_effect=0.003)
    assert isinstance(result.get("timing_effect"), float)


def test_strategy_compute_gross_pnl_stored():
    result = _compute(strategy_gross_pnl=5000.0)
    assert isinstance(result.get("strategy_gross_pnl"), float)


def test_strategy_compute_zero_return():
    result = _compute(strategy_return=0.0)
    assert isinstance(result, dict)
