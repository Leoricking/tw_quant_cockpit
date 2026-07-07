"""tests/test_small_capital_paper_sim_v170.py — paper simulation bridge tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.paper_simulation_bridge_v170 import (
    run_paper_simulation, get_simulation_safety_summary,
    _REAL_EXECUTION, _BROKER_CONNECTED, _LIVE_ACCOUNT,
)
from paper_trading.small_capital_strategy.models_v170 import SmallCapitalSimulationInput
from paper_trading.small_capital_strategy.enums_v170 import BuyPointType, MarketRegime

TEMPLATE_ID = "small_capital_300k_v170"


def _make_input(**kwargs):
    defaults = {
        "template_id": TEMPLATE_ID,
        "symbol": "2330",
        "buy_point_type": BuyPointType.A_10MA_PULLBACK,
        "entry_price": 500.0,
        "stop_loss_pct": 0.06,
        "capital_twd": 300000.0,
        "regime": MarketRegime.BULL,
    }
    defaults.update(kwargs)
    return SmallCapitalSimulationInput(**defaults)


def test_real_execution_disabled():
    assert _REAL_EXECUTION is False


def test_broker_not_connected():
    assert _BROKER_CONNECTED is False


def test_live_account_disabled():
    assert _LIVE_ACCOUNT is False


def test_run_simulation_returns_result():
    inp = _make_input()
    result = run_paper_simulation(inp)
    assert result is not None


def test_run_simulation_paper_only():
    inp = _make_input()
    result = run_paper_simulation(inp)
    assert result.paper_only is True


def test_run_simulation_no_real_orders():
    inp = _make_input()
    result = run_paper_simulation(inp)
    assert result.no_real_orders is True


def test_run_simulation_position_size_positive():
    inp = _make_input()
    result = run_paper_simulation(inp)
    assert result.position_size_twd > 0


def test_run_simulation_stop_loss_below_entry():
    inp = _make_input(entry_price=500.0, stop_loss_pct=0.06)
    result = run_paper_simulation(inp)
    assert result.stop_loss_price < 500.0


def test_run_simulation_stop_loss_formula():
    inp = _make_input(entry_price=500.0, stop_loss_pct=0.06)
    result = run_paper_simulation(inp)
    expected = 500.0 * (1 - 0.06)
    assert abs(result.stop_loss_price - expected) < 0.01


def test_run_simulation_symbol_preserved():
    inp = _make_input(symbol="2454")
    result = run_paper_simulation(inp)
    assert result.symbol == "2454"


def test_run_simulation_template_id_preserved():
    inp = _make_input()
    result = run_paper_simulation(inp)
    assert result.template_id == TEMPLATE_ID


def test_get_simulation_safety_summary_dict():
    summary = get_simulation_safety_summary()
    assert isinstance(summary, dict)


def test_get_simulation_safety_real_exec_false():
    summary = get_simulation_safety_summary()
    assert summary["real_execution_enabled"] is False


def test_get_simulation_safety_broker_false():
    summary = get_simulation_safety_summary()
    assert summary["broker_connected"] is False


def test_get_simulation_safety_live_account_false():
    summary = get_simulation_safety_summary()
    assert summary["live_account_enabled"] is False


def test_get_simulation_safety_paper_only():
    summary = get_simulation_safety_summary()
    assert summary["paper_only"] is True


def test_get_simulation_safety_no_real_orders():
    summary = get_simulation_safety_summary()
    assert summary["no_real_orders"] is True
