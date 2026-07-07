"""tests/test_abc_position_sizing_bridge_v172.py — Position sizing bridge tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_position_sizing_bridge_v172 import (
    compute_position_sizing, get_capital_constants,
    CAPITAL_300K, MAX_HOLDINGS, TRAINING_MAX_AMOUNT, MAX_RISK_PCT_PER_TRADE,
)
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCRiskPermission, ABCExecutionBlockReason,
)


def test_capital_300k():
    assert CAPITAL_300K == 300_000.0


def test_max_holdings_4():
    assert MAX_HOLDINGS == 4


def test_training_max_amount_15000():
    assert TRAINING_MAX_AMOUNT == 15_000.0


def test_max_risk_pct_1_pct():
    assert MAX_RISK_PCT_PER_TRADE == 0.01


def test_compute_sizing_allowed():
    # Tight stop (1%) to keep risk within budget for 1000-share units
    result = compute_position_sizing("2330", "MAIN_THEME", 100.0, 99.0, 0)
    assert result.risk_permission == ABCRiskPermission.ALLOWED


def test_compute_sizing_position_positive():
    result = compute_position_sizing("2330", "MAIN_THEME", 100.0, 99.0, 0)
    assert result.position_amount > 0


def test_compute_sizing_quantity_positive():
    result = compute_position_sizing("2330", "MAIN_THEME", 100.0, 99.0, 0)
    assert result.quantity_estimate > 0


def test_compute_sizing_excluded_blocked():
    result = compute_position_sizing("2330", "EXCLUDED", 100.0, 93.0, 0)
    assert result.risk_permission == ABCRiskPermission.BLOCKED
    assert ABCExecutionBlockReason.WATCHLIST_EXCLUDED in result.block_reasons


def test_compute_sizing_too_many_holdings_blocked():
    result = compute_position_sizing("2330", "MAIN_THEME", 100.0, 93.0, 4)
    assert result.risk_permission == ABCRiskPermission.BLOCKED
    assert ABCExecutionBlockReason.TOO_MANY_HOLDINGS in result.block_reasons


def test_compute_sizing_training_cap_applied():
    # Use tight stop so risk stays within budget
    result = compute_position_sizing("2330", "TRAINING", 100.0, 99.0, 0)
    assert result.training_cap_applied is True


def test_compute_sizing_training_degraded():
    result = compute_position_sizing("2330", "TRAINING", 100.0, 99.0, 0)
    assert result.risk_permission == ABCRiskPermission.DEGRADED


def test_compute_sizing_zero_entry_blocked():
    result = compute_position_sizing("2330", "MAIN_THEME", 0.0, 93.0, 0)
    assert result.risk_permission == ABCRiskPermission.BLOCKED


def test_compute_sizing_stop_above_entry_blocked():
    result = compute_position_sizing("2330", "MAIN_THEME", 90.0, 95.0, 0)
    assert result.risk_permission == ABCRiskPermission.BLOCKED


def test_compute_sizing_tight_stop_allowed():
    result = compute_position_sizing("2330", "CORE", 100.0, 99.5, 0)
    assert result.risk_permission == ABCRiskPermission.ALLOWED


def test_get_capital_constants_capital():
    c = get_capital_constants()
    assert c["capital_300k"] == 300_000.0


def test_get_capital_constants_max_holdings():
    c = get_capital_constants()
    assert c["max_holdings"] == 4


def test_compute_sizing_capital_stored():
    result = compute_position_sizing("2330", "MAIN_THEME", 100.0, 99.0, 0)
    assert result.capital_twd == CAPITAL_300K


def test_compute_sizing_paper_only():
    result = compute_position_sizing("2330", "MAIN_THEME", 100.0, 99.0, 0)
    assert result.paper_only is True


def test_compute_sizing_no_real_orders():
    result = compute_position_sizing("2330", "MAIN_THEME", 100.0, 99.0, 0)
    assert result.no_real_orders is True


def test_compute_sizing_max_holdings_stored():
    result = compute_position_sizing("2330", "MAIN_THEME", 100.0, 99.0, 0)
    assert result.max_holdings == 4


def test_compute_sizing_one_holding_ok():
    result = compute_position_sizing("2330", "MAIN_THEME", 100.0, 99.0, 1)
    assert result.risk_permission != ABCRiskPermission.BLOCKED


def test_compute_sizing_three_holdings_ok():
    result = compute_position_sizing("2330", "MAIN_THEME", 100.0, 99.0, 3)
    assert result.risk_permission != ABCRiskPermission.BLOCKED


def test_compute_sizing_core_tier_allowed():
    result = compute_position_sizing("2330", "CORE", 100.0, 99.0, 0)
    assert result.risk_permission == ABCRiskPermission.ALLOWED


def test_compute_sizing_second_wave_allowed():
    result = compute_position_sizing("2330", "SECOND_WAVE", 100.0, 99.0, 0)
    assert result.risk_permission == ABCRiskPermission.ALLOWED


def test_compute_sizing_training_risk_pct_low():
    # Training with tight stop: verify risk_pct is within limits
    result = compute_position_sizing("2330", "TRAINING", 100.0, 99.0, 0)
    assert result.risk_pct <= 0.02  # should not exceed 2x MAX_RISK_PCT


def test_get_capital_constants_max_risk_pct():
    c = get_capital_constants()
    assert c["max_risk_pct_per_trade"] == 0.01


def test_get_capital_constants_max_position_pct():
    c = get_capital_constants()
    assert c["max_position_pct"] == 0.25


def test_compute_sizing_not_investment_advice():
    result = compute_position_sizing("2330", "MAIN_THEME", 100.0, 99.0, 0)
    assert result.not_investment_advice is True
