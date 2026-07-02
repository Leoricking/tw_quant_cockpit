"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.attribution_input_v167 import AttributionInput
from paper_trading.performance_attribution.enums_v167 import BenchmarkMode, DataQualityStatus


def _make_input(**kwargs):
    defaults = dict(
        run_id="run-001",
        portfolio_id="port-001",
        session_id="sess-001",
        strategy_id="strat-001",
        attribution_period_start="2026-01-01",
        attribution_period_end="2026-06-30",
        benchmark_id=None,
        benchmark_mode=BenchmarkMode.NONE,
        initial_equity=100_000.0,
        ending_equity=105_000.0,
    )
    defaults.update(kwargs)
    return AttributionInput(**defaults)


def test_attribution_input_instantiates():
    inp = _make_input()
    assert inp is not None


def test_attribution_input_required_fields_stored():
    inp = _make_input()
    assert inp.run_id == "run-001"
    assert inp.portfolio_id == "port-001"
    assert inp.session_id == "sess-001"
    assert inp.strategy_id == "strat-001"


def test_attribution_input_period_stored():
    inp = _make_input()
    assert inp.attribution_period_start == "2026-01-01"
    assert inp.attribution_period_end == "2026-06-30"


def test_attribution_input_equity_stored():
    inp = _make_input()
    assert inp.initial_equity == 100_000.0
    assert inp.ending_equity == 105_000.0


def test_attribution_input_paper_only_default_true():
    inp = _make_input()
    assert inp.paper_only is True


def test_attribution_input_research_only_default_true():
    inp = _make_input()
    assert inp.research_only is True


def test_attribution_input_no_real_orders_default_true():
    inp = _make_input()
    assert inp.no_real_orders is True


def test_attribution_input_source_lineage_default_empty_string():
    inp = _make_input()
    assert inp.source_lineage == ""


def test_attribution_input_data_quality_default_complete():
    inp = _make_input()
    assert inp.data_quality == DataQualityStatus.COMPLETE


def test_attribution_input_benchmark_id_none():
    inp = _make_input(benchmark_id=None)
    assert inp.benchmark_id is None


def test_attribution_input_benchmark_id_provided():
    inp = _make_input(benchmark_id="SPX")
    assert inp.benchmark_id == "SPX"


def test_attribution_input_benchmark_mode_none():
    inp = _make_input(benchmark_mode=BenchmarkMode.NONE)
    assert inp.benchmark_mode == BenchmarkMode.NONE


def test_attribution_input_benchmark_mode_market():
    inp = _make_input(benchmark_mode=BenchmarkMode.MARKET_BENCHMARK, benchmark_id="SPX")
    assert inp.benchmark_mode == BenchmarkMode.MARKET_BENCHMARK


def test_attribution_input_not_for_production_attribute_exists():
    inp = _make_input()
    assert hasattr(inp, "not_for_production")


def test_attribution_input_multiple_instances_independent():
    a = _make_input(run_id="r1", initial_equity=100_000.0)
    b = _make_input(run_id="r2", initial_equity=200_000.0)
    assert a.run_id != b.run_id
    assert a.initial_equity != b.initial_equity
