"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.factor_attribution_v167 import FactorAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel


def _engine():
    return FactorAttributionEngine()


def _compute(**kwargs):
    defaults = dict(
        entity_id="p1",
        level=AttributionLevel.PORTFOLIO,
        factor_name="momentum",
        factor_exposure=None,
        factor_return=None,
        is_proxy=True,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_factor_engine_instantiates():
    assert _engine() is not None


def test_factor_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_factor_engine_has_compute_all_factors():
    assert callable(getattr(_engine(), "compute_all_factors", None))


def test_factor_compute_returns_factor_contribution():
    result = _compute()
    assert type(result).__name__ == "FactorContribution"


def test_factor_compute_entity_id_stored():
    result = _compute(entity_id="factor-entity")
    assert result.entity_id == "factor-entity"


def test_factor_compute_factor_name_stored():
    result = _compute(factor_name="value")
    assert result.factor_name == "value"


def test_factor_compute_level_stored():
    result = _compute(level=AttributionLevel.STRATEGY)
    assert result.level == AttributionLevel.STRATEGY


def test_factor_compute_paper_only_true():
    result = _compute()
    assert result.paper_only is True


def test_factor_compute_research_only_true():
    result = _compute()
    assert result.research_only is True


def test_factor_compute_no_real_orders_true():
    result = _compute()
    assert result.no_real_orders is True


def test_factor_compute_with_exposure_and_return():
    result = _compute(factor_exposure=0.8, factor_return=0.02)
    assert type(result).__name__ == "FactorContribution"


def test_factor_compute_is_proxy_stored():
    result = _compute(is_proxy=True)
    assert result.is_proxy is True


def test_factor_compute_status_exists():
    result = _compute()
    assert hasattr(result, "status")


def test_factor_compute_factor_return_attribute_exists():
    result = _compute()
    assert hasattr(result, "factor_return")
