"""tests/test_small_capital_position_sizing_v170.py — position sizing tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.enums_v170 import AllocationBucket
from paper_trading.small_capital_strategy.position_sizing_v170 import (
    compute_position_size, PositionSizingInput,
    MAX_SINGLE_POSITION_PCT, MAX_SINGLE_POSITION_AMOUNT, SHORT_TERM_TRAINING_MAX as SHORT_TERM_TRAINING_CAP,
)


def _make_input(**kwargs):
    defaults = dict(
        symbol="2330",
        capital_twd=300000.0,
        max_loss_amount=3000.0,
        stop_loss_pct=0.06,
        bucket=AllocationBucket.MAIN_THEME_SWING,
        bucket_remaining_budget=105000.0,
    )
    defaults.update(kwargs)
    return PositionSizingInput(**defaults)


def test_position_sizing_formula_6pct():
    inp = _make_input(stop_loss_pct=0.06)
    result = compute_position_size(inp)
    assert abs(result.position_size_twd - 50000.0) < 1.0


def test_position_sizing_formula_3pct():
    inp = _make_input(stop_loss_pct=0.03, bucket_remaining_budget=200000.0)
    result = compute_position_size(inp)
    assert result.position_size_twd <= 105000.0


def test_position_sizing_formula_10pct():
    inp = _make_input(stop_loss_pct=0.10)
    result = compute_position_size(inp)
    assert abs(result.position_size_twd - 30000.0) < 1.0


def test_position_sizing_status_ok():
    inp = _make_input(stop_loss_pct=0.06)
    result = compute_position_size(inp)
    assert result.status == "VALID"


def test_position_sizing_blocked_zero_stop():
    inp = _make_input(stop_loss_pct=0.0)
    result = compute_position_size(inp)
    assert result.status == "BLOCKED"


def test_position_sizing_blocked_negative_stop():
    inp = _make_input(stop_loss_pct=-0.01)
    result = compute_position_size(inp)
    assert result.status == "BLOCKED"


def test_position_sizing_degraded_over_20pct():
    inp = _make_input(stop_loss_pct=0.25, bucket_remaining_budget=200000.0)
    result = compute_position_size(inp)
    assert result.status == "DEGRADED"


def test_position_sizing_short_term_cap():
    inp = _make_input(
        bucket=AllocationBucket.SHORT_TERM_TRAINING,
        stop_loss_pct=0.03,
        bucket_remaining_budget=50000.0,
    )
    result = compute_position_size(inp)
    assert result.position_size_twd <= SHORT_TERM_TRAINING_CAP


def test_position_sizing_max_single_position_pct():
    assert MAX_SINGLE_POSITION_PCT == 0.35


def test_position_sizing_max_single_position_amount():
    assert MAX_SINGLE_POSITION_AMOUNT == 105000.0


def test_position_sizing_short_term_cap_value():
    assert SHORT_TERM_TRAINING_CAP == 15000.0


def test_position_sizing_capped_by_bucket():
    inp = _make_input(stop_loss_pct=0.03, bucket_remaining_budget=20000.0)
    result = compute_position_size(inp)
    assert result.position_size_twd <= 20000.0


def test_position_sizing_paper_only():
    inp = _make_input(stop_loss_pct=0.06)
    result = compute_position_size(inp)
    assert result.paper_only is True


def test_position_sizing_no_real_orders():
    inp = _make_input(stop_loss_pct=0.06)
    result = compute_position_size(inp)
    assert result.no_real_orders is True


def test_position_sizing_symbol_preserved():
    inp = _make_input(stop_loss_pct=0.06)
    result = compute_position_size(inp)
    assert result.symbol == "2330"
