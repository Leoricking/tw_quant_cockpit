"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.drawdown_attribution_v167 import DrawdownAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel


def _engine():
    return DrawdownAttributionEngine()


def _equity_point(date, equity):
    return {"date": date, "value": equity}


def _compute(**kwargs):
    equity_curve = [
        _equity_point("2026-01-01", 100_000.0),
        _equity_point("2026-01-02", 98_000.0),
        _equity_point("2026-01-03", 97_000.0),
        _equity_point("2026-01-04", 99_000.0),
    ]
    defaults = dict(
        entity_id="p1",
        level=AttributionLevel.PORTFOLIO,
        equity_curve=equity_curve,
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_drawdown_engine_instantiates():
    assert _engine() is not None


def test_drawdown_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_drawdown_compute_returns_drawdown_contribution():
    result = _compute()
    assert type(result).__name__ == "DrawdownContribution"


def test_drawdown_compute_entity_id_stored():
    result = _compute(entity_id="portfolio-DD")
    assert result.entity_id == "portfolio-DD"


def test_drawdown_compute_level_stored():
    result = _compute(level=AttributionLevel.STRATEGY)
    assert result.level == AttributionLevel.STRATEGY


def test_drawdown_compute_paper_only_true():
    result = _compute()
    assert result.paper_only is True


def test_drawdown_compute_research_only_true():
    result = _compute()
    assert result.research_only is True


def test_drawdown_compute_no_real_orders_true():
    result = _compute()
    assert result.no_real_orders is True


def test_drawdown_compute_with_symbol_contributions():
    result = _compute(symbol_contributions={"AAPL": -0.02})
    assert type(result).__name__ == "DrawdownContribution"


def test_drawdown_compute_with_strategy_contributions():
    result = _compute(strategy_contributions={"mean_reversion": -0.015})
    assert type(result).__name__ == "DrawdownContribution"


def test_drawdown_compute_single_point_curve():
    result = _compute(equity_curve=[_equity_point("2026-01-01", 100_000.0)])
    assert type(result).__name__ == "DrawdownContribution"


def test_drawdown_compute_status_exists():
    result = _compute()
    assert hasattr(result, "status")
