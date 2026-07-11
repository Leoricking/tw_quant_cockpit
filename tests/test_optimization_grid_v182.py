"""
tests/test_optimization_grid_v182.py
Tests for ParameterGrid v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.optimization_models_v182 import ParameterGrid


# --- Dimension counts ---
def test_grid_initial_capital_3():
    assert len(ParameterGrid().initial_capital_values) == 3

def test_grid_risk_pct_3():
    assert len(ParameterGrid().single_trade_risk_pct_values) == 3

def test_grid_max_positions_3():
    assert len(ParameterGrid().max_positions_values) == 3

def test_grid_stop_loss_3():
    assert len(ParameterGrid().stop_loss_pct_values) == 3

def test_grid_take_profit_4():
    assert len(ParameterGrid().take_profit_pct_values) == 4

def test_grid_trailing_stop_3():
    assert len(ParameterGrid().trailing_stop_pct_values) == 3

def test_grid_drawdown_4():
    assert len(ParameterGrid().max_drawdown_limit_pct_values) == 4

def test_grid_theme_3():
    assert len(ParameterGrid().theme_score_threshold_values) == 3

def test_grid_watchlist_3():
    assert len(ParameterGrid().watchlist_score_threshold_values) == 3

def test_grid_abc_3():
    assert len(ParameterGrid().abc_score_threshold_values) == 3

def test_grid_behavior_3():
    assert len(ParameterGrid().behavior_risk_limit_values) == 3

def test_grid_risk_dashboard_2():
    assert len(ParameterGrid().risk_dashboard_limit_values) == 2

def test_grid_12_dimensions():
    g = ParameterGrid()
    dims = [f for f in dir(g) if f.endswith("_values")]
    assert len(dims) == 12


# --- Value contents ---
def test_grid_capital_300k():
    assert 300000.0 in ParameterGrid().initial_capital_values

def test_grid_capital_500k():
    assert 500000.0 in ParameterGrid().initial_capital_values

def test_grid_capital_1m():
    assert 1000000.0 in ParameterGrid().initial_capital_values

def test_grid_risk_08():
    assert 0.8 in ParameterGrid().single_trade_risk_pct_values

def test_grid_risk_10():
    assert 1.0 in ParameterGrid().single_trade_risk_pct_values

def test_grid_risk_15():
    assert 1.5 in ParameterGrid().single_trade_risk_pct_values

def test_grid_positions_3():
    assert 3 in ParameterGrid().max_positions_values

def test_grid_positions_4():
    assert 4 in ParameterGrid().max_positions_values

def test_grid_positions_5():
    assert 5 in ParameterGrid().max_positions_values

def test_grid_sl_5():
    assert 5.0 in ParameterGrid().stop_loss_pct_values

def test_grid_sl_7():
    assert 7.0 in ParameterGrid().stop_loss_pct_values

def test_grid_sl_10():
    assert 10.0 in ParameterGrid().stop_loss_pct_values

def test_grid_tp_10():
    assert 10.0 in ParameterGrid().take_profit_pct_values

def test_grid_tp_15():
    assert 15.0 in ParameterGrid().take_profit_pct_values

def test_grid_tp_20():
    assert 20.0 in ParameterGrid().take_profit_pct_values

def test_grid_tp_30():
    assert 30.0 in ParameterGrid().take_profit_pct_values

def test_grid_trailing_5():
    assert 5.0 in ParameterGrid().trailing_stop_pct_values

def test_grid_trailing_8():
    assert 8.0 in ParameterGrid().trailing_stop_pct_values

def test_grid_trailing_12():
    assert 12.0 in ParameterGrid().trailing_stop_pct_values

def test_grid_dd_8():
    assert 8.0 in ParameterGrid().max_drawdown_limit_pct_values

def test_grid_dd_12():
    assert 12.0 in ParameterGrid().max_drawdown_limit_pct_values

def test_grid_dd_15():
    assert 15.0 in ParameterGrid().max_drawdown_limit_pct_values

def test_grid_dd_20():
    assert 20.0 in ParameterGrid().max_drawdown_limit_pct_values

def test_grid_theme_50():
    assert 50.0 in ParameterGrid().theme_score_threshold_values

def test_grid_theme_65():
    assert 65.0 in ParameterGrid().theme_score_threshold_values

def test_grid_theme_80():
    assert 80.0 in ParameterGrid().theme_score_threshold_values

def test_grid_behavior_pass():
    assert "PASS" in ParameterGrid().behavior_risk_limit_values

def test_grid_behavior_watch():
    assert "WATCH" in ParameterGrid().behavior_risk_limit_values

def test_grid_behavior_warning():
    assert "WARNING" in ParameterGrid().behavior_risk_limit_values

def test_grid_rdl_pass():
    assert "PASS" in ParameterGrid().risk_dashboard_limit_values

def test_grid_rdl_warning():
    assert "WARNING" in ParameterGrid().risk_dashboard_limit_values


# --- Safety ---
def test_grid_paper_only():
    assert ParameterGrid().paper_only is True

def test_grid_schema_version():
    assert ParameterGrid().schema_version == "182"

def test_grid_all_values_lists():
    g = ParameterGrid()
    for f in dir(g):
        if f.endswith("_values"):
            assert isinstance(getattr(g, f), list), f"{f} should be a list"

def test_grid_no_empty_lists():
    g = ParameterGrid()
    for f in dir(g):
        if f.endswith("_values"):
            assert len(getattr(g, f)) > 0, f"{f} should not be empty"
