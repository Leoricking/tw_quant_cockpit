"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.selection_attribution_v167 import SelectionAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel, BenchmarkMode


def _engine():
    return SelectionAttributionEngine()


def _compute(entity_id="p1", level=AttributionLevel.PORTFOLIO,
             pw=None, pr=None, bw=None, br=None,
             bm=BenchmarkMode.NONE):
    pw = pw or {"AAPL": 0.5, "TSLA": 0.5}
    pr = pr or {"AAPL": 0.05, "TSLA": 0.03}
    return _engine().compute(
        entity_id=entity_id,
        level=level,
        portfolio_weights=pw,
        portfolio_returns=pr,
        benchmark_weights=bw,
        benchmark_returns=br,
        benchmark_mode=bm,
    )


def test_selection_engine_instantiates():
    assert _engine() is not None


def test_selection_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_selection_compute_returns_selection_contribution():
    result = _compute()
    assert type(result).__name__ == "SelectionContribution"


def test_selection_compute_entity_id_stored():
    result = _compute(entity_id="my-portfolio")
    assert result.entity_id == "my-portfolio"


def test_selection_compute_level_stored():
    result = _compute(level=AttributionLevel.STRATEGY)
    assert result.level == AttributionLevel.STRATEGY


def test_selection_compute_selection_return_is_float():
    result = _compute()
    assert isinstance(result.selection_return, float)


def test_selection_compute_paper_only_true():
    result = _compute()
    assert result.paper_only is True


def test_selection_compute_research_only_true():
    result = _compute()
    assert result.research_only is True


def test_selection_compute_no_real_orders_true():
    result = _compute()
    assert result.no_real_orders is True


def test_selection_compute_benchmark_mode_stored():
    result = _compute(bm=BenchmarkMode.NONE)
    assert result.benchmark_mode == BenchmarkMode.NONE


def test_selection_compute_with_market_benchmark():
    result = _compute(
        bm=BenchmarkMode.MARKET_BENCHMARK,
        bw={"AAPL": 0.6, "TSLA": 0.4},
        br={"AAPL": 0.04, "TSLA": 0.02},
    )
    assert isinstance(result.selection_return, float)


def test_selection_compute_portfolio_level():
    result = _compute(level=AttributionLevel.PORTFOLIO)
    assert result.level == AttributionLevel.PORTFOLIO


def test_selection_compute_symbol_level():
    result = _compute(level=AttributionLevel.SYMBOL)
    assert result.level == AttributionLevel.SYMBOL


def test_selection_compute_status_attribute_exists():
    result = _compute()
    assert hasattr(result, "status")
