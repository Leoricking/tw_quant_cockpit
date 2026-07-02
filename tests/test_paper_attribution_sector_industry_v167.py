"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.sector_attribution_v167 import SectorAttributionEngine
from paper_trading.performance_attribution.industry_attribution_v167 import IndustryAttributionEngine


def _sector_engine():
    return SectorAttributionEngine()


def _industry_engine():
    return IndustryAttributionEngine()


def _sector_compute(engine=None, **kwargs):
    if engine is None:
        engine = _sector_engine()
    defaults = dict(
        sector="Technology",
        portfolio_weight=0.30,
        benchmark_weight=0.25,
        portfolio_return=0.06,
        benchmark_return=0.04,
        risk_contribution=0.008,
        drawdown_contribution=-0.002,
        concentration=0.30,
    )
    defaults.update(kwargs)
    return engine.compute(**defaults)


def test_sector_engine_instantiates():
    assert _sector_engine() is not None


def test_industry_engine_instantiates():
    assert _industry_engine() is not None


def test_sector_engine_has_compute():
    assert callable(getattr(_sector_engine(), "compute", None))


def test_industry_engine_has_compute():
    assert callable(getattr(_industry_engine(), "compute", None))


def test_sector_engine_has_aggregate_sectors():
    assert callable(getattr(_sector_engine(), "aggregate_sectors", None))


def test_industry_engine_has_aggregate_sectors():
    assert callable(getattr(_industry_engine(), "aggregate_sectors", None))


def test_industry_engine_has_compute_industry():
    assert callable(getattr(_industry_engine(), "compute_industry", None))


def test_sector_compute_returns_dict():
    result = _sector_compute()
    assert isinstance(result, dict)


def test_sector_compute_sector_stored():
    result = _sector_compute(sector="Financials")
    assert result.get("sector") == "Financials"


def test_sector_compute_paper_only_true():
    result = _sector_compute()
    assert result.get("paper_only") is True


def test_sector_compute_research_only_true():
    result = _sector_compute()
    assert result.get("research_only") is True


def test_sector_compute_no_real_orders_true():
    result = _sector_compute()
    assert result.get("no_real_orders") is True


def test_industry_compute_returns_dict():
    result = _sector_compute(engine=_industry_engine(), sector="Software")
    assert isinstance(result, dict)


def test_industry_compute_paper_only_true():
    result = _sector_compute(engine=_industry_engine())
    assert result.get("paper_only") is True


def test_industry_compute_no_real_orders_true():
    result = _sector_compute(engine=_industry_engine())
    assert result.get("no_real_orders") is True


def test_sector_compute_portfolio_return_stored():
    result = _sector_compute(portfolio_return=0.07)
    assert isinstance(result.get("portfolio_return"), float)
