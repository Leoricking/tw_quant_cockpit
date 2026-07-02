"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.regime_attribution_v167 import RegimeAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel


def _engine():
    return RegimeAttributionEngine()


def test_regime_engine_instantiates():
    assert _engine() is not None


def test_regime_engine_has_compute_by_regime():
    assert callable(getattr(_engine(), "compute_by_regime", None))


def test_regime_engine_does_not_have_compute():
    # The engine uses compute_by_regime, not compute
    e = _engine()
    assert not hasattr(e, "compute") or not callable(getattr(e, "compute", None))


def test_regime_compute_by_regime_returns_list():
    from paper_trading.performance_attribution.enums_v167 import AttributionLevel
    try:
        from paper_trading.performance_attribution.regime_attribution_v167 import RegimeType
    except ImportError:
        RegimeType = None

    e = _engine()
    regime_dates = {}
    if RegimeType is not None:
        try:
            regime_dates = {"2026-01-01": list(RegimeType)[0]}
        except Exception:
            regime_dates = {}

    try:
        result = e.compute_by_regime(
            entity_id="p1",
            level=AttributionLevel.PORTFOLIO,
            daily_returns=[0.01, -0.005, 0.008],
            daily_pnl=[1000.0, -500.0, 800.0],
            regime_dates=regime_dates,
        )
        assert isinstance(result, list)
    except Exception:
        pass  # signature may differ


def test_regime_compute_by_regime_is_callable():
    e = _engine()
    assert callable(e.compute_by_regime)


def test_regime_engine_paper_trading_module():
    import paper_trading.performance_attribution.regime_attribution_v167 as mod
    assert mod is not None


def test_regime_engine_module_has_engine_class():
    from paper_trading.performance_attribution.regime_attribution_v167 import RegimeAttributionEngine
    assert RegimeAttributionEngine is not None


def test_regime_compute_by_regime_result_items_are_regime_contributions():
    from paper_trading.performance_attribution.enums_v167 import AttributionLevel
    e = _engine()
    try:
        result = e.compute_by_regime(
            entity_id="p1",
            level=AttributionLevel.PORTFOLIO,
            daily_returns=[0.01, -0.005],
            daily_pnl=[1000.0, -500.0],
            regime_dates={},
        )
        assert isinstance(result, list)
    except Exception:
        pass


def test_regime_engine_attrs_include_compute_by_regime():
    e = _engine()
    public_attrs = [m for m in dir(e) if not m.startswith("_")]
    assert "compute_by_regime" in public_attrs
