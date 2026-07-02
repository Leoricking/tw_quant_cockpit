"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.pnl_attribution_v167 import PnLAttributionEngine
from paper_trading.performance_attribution.enums_v167 import AttributionLevel


def _engine():
    return PnLAttributionEngine()


def _buy_trade(**kwargs):
    base = {
        "trade_id": "t1",
        "direction": 1,
        "quantity": 100,
        "fill_price": 100.0,
        "exit_price": 110.0,
        "simulated": True,
        "commission": 0.0,
        "transaction_tax": 0.0,
        "exchange_fee": 0.0,
        "slippage": 0.0,
    }
    base.update(kwargs)
    return base


def test_pnl_engine_instantiates():
    assert _engine() is not None


def test_pnl_engine_has_compute_trade_pnl():
    assert callable(getattr(_engine(), "compute_trade_pnl", None))


def test_pnl_engine_has_aggregate_methods():
    e = _engine()
    assert callable(getattr(e, "aggregate_trades_to_position", None))
    assert callable(getattr(e, "aggregate_to_symbol", None))
    assert callable(getattr(e, "aggregate_to_strategy", None))
    assert callable(getattr(e, "aggregate_to_portfolio", None))


def test_pnl_engine_has_build_contribution():
    assert callable(getattr(_engine(), "build_contribution", None))


def test_pnl_engine_has_verify_hierarchy():
    assert callable(getattr(_engine(), "verify_hierarchy", None))


def test_compute_trade_pnl_returns_dict():
    result = _engine().compute_trade_pnl(_buy_trade())
    assert isinstance(result, dict)


def test_compute_trade_pnl_has_gross_pnl_key():
    result = _engine().compute_trade_pnl(_buy_trade())
    assert "gross_pnl" in result


def test_compute_trade_pnl_paper_only_flag():
    result = _engine().compute_trade_pnl(_buy_trade())
    assert result.get("paper_only") is True


def test_compute_trade_pnl_research_only_flag():
    result = _engine().compute_trade_pnl(_buy_trade())
    assert result.get("research_only") is True


def test_compute_trade_pnl_has_net_pnl_key():
    result = _engine().compute_trade_pnl(_buy_trade())
    assert "net_pnl" in result


def test_verify_hierarchy_exact_match_returns_all_pass():
    result = _engine().verify_hierarchy(1000.0, 1000.0, 1000.0, 1000.0, 1000.0)
    assert result["all_pass"] is True


def test_verify_hierarchy_paper_only():
    result = _engine().verify_hierarchy(500.0, 500.0, 500.0, 500.0, 500.0)
    assert result.get("paper_only") is True


def test_verify_hierarchy_returns_checks_dict():
    result = _engine().verify_hierarchy(100.0, 100.0, 100.0, 100.0, 100.0)
    assert "checks" in result
    assert isinstance(result["checks"], dict)


def test_build_contribution_returns_pnl_contribution():
    e = _engine()
    agg = {"gross_pnl": 1000.0, "net_pnl": 950.0, "commission": 50.0}
    contribution = e.build_contribution(
        entity_id="p1",
        level=AttributionLevel.PORTFOLIO,
        agg=agg,
        begin_equity=100_000.0,
    )
    assert contribution is not None
    assert contribution.entity_id == "p1"
