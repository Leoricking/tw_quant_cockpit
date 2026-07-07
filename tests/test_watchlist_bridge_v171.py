"""tests/test_watchlist_bridge_v171.py — v1.7.0 bridge tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import WatchlistTier
from paper_trading.small_capital_strategy.small_capital_watchlist_bridge_v171 import (
    map_tier_to_allocation_bucket,
    check_training_position_constraint,
    check_holdings_limit,
    get_v170_bridge_summary,
    CAPITAL_300K, MAX_HOLDINGS, TRAINING_MAX_AMOUNT, TRAINING_MAX_PCT,
    BUCKET_CORE, BUCKET_MAIN_THEME_SWING, BUCKET_SECOND_WAVE, BUCKET_TRAINING,
)


def test_capital_300k_constant():
    assert CAPITAL_300K == 300_000.0


def test_max_holdings_constant():
    assert MAX_HOLDINGS == 4


def test_training_max_amount_constant():
    assert TRAINING_MAX_AMOUNT == 15_000.0


def test_training_max_pct_constant():
    assert TRAINING_MAX_PCT == 0.05


def test_map_core_to_bucket():
    assert map_tier_to_allocation_bucket(WatchlistTier.CORE) == BUCKET_CORE


def test_map_main_theme_to_bucket():
    assert map_tier_to_allocation_bucket(WatchlistTier.MAIN_THEME) == BUCKET_MAIN_THEME_SWING


def test_map_second_wave_to_bucket():
    assert map_tier_to_allocation_bucket(WatchlistTier.SECOND_WAVE) == BUCKET_SECOND_WAVE


def test_map_training_to_bucket():
    assert map_tier_to_allocation_bucket(WatchlistTier.TRAINING) == BUCKET_TRAINING


def test_map_excluded_returns_none():
    assert map_tier_to_allocation_bucket(WatchlistTier.EXCLUDED) is None


def test_training_constraint_valid():
    result = check_training_position_constraint(10_000.0)
    assert result["valid"] is True


def test_training_constraint_over_max():
    result = check_training_position_constraint(20_000.0)
    assert result["valid"] is False


def test_training_constraint_blocked_by():
    result = check_training_position_constraint(20_000.0)
    assert result["blocked_by"] == "TRAINING_POSITION_CAP"


def test_training_constraint_pct_based():
    # 5% of 200000 = 10000, which is less than 15000 cap
    result = check_training_position_constraint(12_000.0, capital_twd=200_000.0)
    assert result["valid"] is False


def test_training_constraint_boundary():
    result = check_training_position_constraint(15_000.0)
    assert result["valid"] is True


def test_holdings_limit_under():
    result = check_holdings_limit(3)
    assert result["valid"] is True


def test_holdings_limit_at_max():
    result = check_holdings_limit(4)
    assert result["valid"] is False


def test_holdings_limit_over():
    result = check_holdings_limit(5)
    assert result["valid"] is False


def test_holdings_limit_blocked_by():
    result = check_holdings_limit(4)
    assert result["blocked_by"] == "MAX_HOLDINGS"


def test_holdings_limit_zero():
    result = check_holdings_limit(0)
    assert result["valid"] is True


def test_bridge_summary_dict():
    summary = get_v170_bridge_summary()
    assert isinstance(summary, dict)


def test_bridge_summary_max_holdings():
    summary = get_v170_bridge_summary()
    assert summary["max_holdings"] == MAX_HOLDINGS


def test_bridge_summary_training_max():
    summary = get_v170_bridge_summary()
    assert summary["training_max_amount_twd"] == TRAINING_MAX_AMOUNT


def test_bridge_summary_paper_only():
    summary = get_v170_bridge_summary()
    assert summary["paper_only"] is True


def test_bridge_summary_not_investment_advice():
    summary = get_v170_bridge_summary()
    assert summary["not_investment_advice"] is True


def test_bridge_summary_tier_mapping_present():
    summary = get_v170_bridge_summary()
    assert "tier_to_bucket" in summary


def test_bridge_summary_excluded_maps_to_none():
    summary = get_v170_bridge_summary()
    assert summary["tier_to_bucket"][WatchlistTier.EXCLUDED.value] is None
