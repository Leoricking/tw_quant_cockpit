"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.exposure_attribution_v167 import ExposureAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel


def _engine():
    return ExposureAttributionEngine()


def _position(symbol="AAPL", value=10_000.0, direction=1):
    return {
        "symbol": symbol,
        "market_value": value,
        "quantity": 100.0,
        "direction": direction,
        "simulated": True,
    }


def _compute(**kwargs):
    defaults = dict(
        entity_id="p1",
        level=AttributionLevel.PORTFOLIO,
        positions=[_position()],
        portfolio_value=100_000.0,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_exposure_engine_instantiates():
    assert _engine() is not None


def test_exposure_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_exposure_compute_returns_exposure_contribution():
    result = _compute()
    assert type(result).__name__ == "ExposureContribution"


def test_exposure_compute_entity_id_stored():
    result = _compute(entity_id="portfolio-X")
    assert result.entity_id == "portfolio-X"


def test_exposure_compute_level_stored():
    result = _compute(level=AttributionLevel.SYMBOL)
    assert result.level == AttributionLevel.SYMBOL


def test_exposure_compute_paper_only_true():
    result = _compute()
    assert result.paper_only is True


def test_exposure_compute_research_only_true():
    result = _compute()
    assert result.research_only is True


def test_exposure_compute_no_real_orders_true():
    result = _compute()
    assert result.no_real_orders is True


def test_exposure_compute_empty_positions():
    result = _compute(positions=[])
    assert type(result).__name__ == "ExposureContribution"


def test_exposure_compute_with_beta_map():
    result = _compute(beta_map={"AAPL": 1.2})
    assert type(result).__name__ == "ExposureContribution"


def test_exposure_compute_with_sector_map():
    result = _compute(sector_map={"AAPL": "Technology"})
    assert type(result).__name__ == "ExposureContribution"


def test_exposure_compute_status_exists():
    result = _compute()
    assert hasattr(result, "status")
