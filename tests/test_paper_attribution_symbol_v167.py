"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.symbol_attribution_v167 import SymbolAttributionEngine


def _engine():
    return SymbolAttributionEngine()


def _compute(**kwargs):
    defaults = dict(
        symbol="AAPL",
        portfolio_value=100_000.0,
        position_value=10_000.0,
        symbol_return=0.05,
        gross_pnl=500.0,
        net_pnl=450.0,
        cost=50.0,
        slippage=10.0,
        turnover=0.2,
        risk_contribution=0.005,
        drawdown_contribution=-0.002,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_symbol_engine_instantiates():
    assert _engine() is not None


def test_symbol_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_symbol_compute_returns_dict():
    result = _compute()
    assert isinstance(result, dict)


def test_symbol_compute_symbol_stored():
    result = _compute(symbol="TSLA")
    assert result.get("symbol") == "TSLA"


def test_symbol_compute_return_stored():
    # result dict uses key "return" for symbol_return
    result = _compute(symbol_return=0.08)
    assert isinstance(result.get("return"), float)


def test_symbol_compute_paper_only_true():
    result = _compute()
    assert result.get("paper_only") is True


def test_symbol_compute_research_only_true():
    result = _compute()
    assert result.get("research_only") is True


def test_symbol_compute_no_real_orders_true():
    result = _compute()
    assert result.get("no_real_orders") is True


def test_symbol_compute_gross_pnl_stored():
    result = _compute(gross_pnl=800.0)
    assert isinstance(result.get("gross_pnl"), float)


def test_symbol_compute_with_selection_return():
    result = _compute(selection_return=0.01, allocation_return=0.005)
    assert isinstance(result, dict)


def test_symbol_compute_with_benchmark():
    result = _compute(benchmark_weight=0.1, benchmark_return=0.03)
    assert isinstance(result, dict)


def test_symbol_compute_with_regime_returns():
    result = _compute(regime_returns={"bull": 0.06, "bear": -0.02})
    assert isinstance(result, dict)
