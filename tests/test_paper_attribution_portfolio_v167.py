"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.portfolio_attribution_v167 import PortfolioAttributionEngine
from paper_trading.performance_attribution.enums_v167 import BenchmarkMode


def _engine():
    return PortfolioAttributionEngine()


def _compute(**kwargs):
    defaults = dict(
        portfolio_id="port-001",
        total_return=0.05,
        gross_return=0.055,
        net_return=0.05,
        benchmark_return=0.03,
        active_return=0.02,
        gross_pnl=5000.0,
        net_pnl=4800.0,
        realized_pnl=3000.0,
        unrealized_pnl=1800.0,
        cost_drag=-0.005,
        execution_drag=-0.001,
        selection_effect=0.02,
        allocation_effect=0.01,
        timing_effect=0.005,
        exposure_effect=0.003,
        risk_effect=-0.002,
        drawdown_effect=-0.001,
        regime_effect=0.0,
        benchmark_effect=0.0,
        factor_effect=0.0,
        residual=0.0,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_portfolio_engine_instantiates():
    assert _engine() is not None


def test_portfolio_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_portfolio_compute_returns_dict():
    result = _compute()
    assert isinstance(result, dict)


def test_portfolio_compute_portfolio_id_stored():
    result = _compute(portfolio_id="my-portfolio")
    assert result.get("portfolio_id") == "my-portfolio"


def test_portfolio_compute_total_return_stored():
    result = _compute(total_return=0.07)
    assert abs(result.get("total_return", 0) - 0.07) < 1e-9


def test_portfolio_compute_paper_only_true():
    result = _compute()
    assert result.get("paper_only") is True


def test_portfolio_compute_research_only_true():
    result = _compute()
    assert result.get("research_only") is True


def test_portfolio_compute_no_real_orders_true():
    result = _compute()
    assert result.get("no_real_orders") is True


def test_portfolio_compute_active_return_stored():
    result = _compute(active_return=0.025)
    assert isinstance(result.get("active_return"), float)


def test_portfolio_compute_benchmark_return_stored():
    result = _compute(benchmark_return=0.04)
    assert isinstance(result.get("benchmark_return"), float)


def test_portfolio_compute_with_benchmark_mode():
    result = _compute(benchmark_mode=BenchmarkMode.MARKET_BENCHMARK)
    assert isinstance(result, dict)


def test_portfolio_compute_gross_pnl_stored():
    result = _compute(gross_pnl=8000.0)
    assert isinstance(result.get("gross_pnl"), float)


def test_portfolio_compute_selection_effect_stored():
    result = _compute(selection_effect=0.03)
    assert isinstance(result.get("selection_effect"), float)


def test_portfolio_compute_zero_return():
    result = _compute(total_return=0.0, gross_return=0.0, net_return=0.0,
                     active_return=0.0, benchmark_return=0.0)
    assert isinstance(result, dict)
