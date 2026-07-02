"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.timing_attribution_v167 import TimingAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel


def _engine():
    return TimingAttributionEngine()


def _compute(entity_id="p1", level=AttributionLevel.PORTFOLIO,
             actual_result=0.05, signal_time_result=None,
             decision_time_result=None, next_bar_result=None,
             vwap_result=None, twap_result=None, close_result=None):
    return _engine().compute(
        entity_id=entity_id,
        level=level,
        actual_result=actual_result,
        signal_time_result=signal_time_result,
        decision_time_result=decision_time_result,
        next_bar_result=next_bar_result,
        vwap_result=vwap_result,
        twap_result=twap_result,
        close_result=close_result,
    )


def test_timing_engine_instantiates():
    assert _engine() is not None


def test_timing_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_timing_compute_returns_timing_contribution():
    result = _compute()
    assert type(result).__name__ == "TimingContribution"


def test_timing_compute_entity_id_stored():
    result = _compute(entity_id="my-entity")
    assert result.entity_id == "my-entity"


def test_timing_compute_level_stored():
    result = _compute(level=AttributionLevel.SYMBOL)
    assert result.level == AttributionLevel.SYMBOL


def test_timing_compute_timing_return_is_float():
    result = _compute(actual_result=0.05)
    assert isinstance(result.timing_return, float)


def test_timing_compute_paper_only_true():
    result = _compute()
    assert result.paper_only is True


def test_timing_compute_research_only_true():
    result = _compute()
    assert result.research_only is True


def test_timing_compute_no_real_orders_true():
    result = _compute()
    assert result.no_real_orders is True


def test_timing_compute_with_signal_time_result():
    result = _compute(actual_result=0.05, signal_time_result=0.04)
    assert isinstance(result.timing_return, float)


def test_timing_compute_with_vwap():
    result = _compute(actual_result=0.05, vwap_result=0.045)
    assert isinstance(result.timing_return, float)


def test_timing_compute_with_all_optionals():
    result = _compute(
        actual_result=0.05,
        signal_time_result=0.04,
        decision_time_result=0.042,
        next_bar_result=0.048,
        vwap_result=0.045,
        twap_result=0.046,
        close_result=0.050,
    )
    assert type(result).__name__ == "TimingContribution"


def test_timing_compute_status_attribute_exists():
    result = _compute()
    assert hasattr(result, "status")
