"""tests/test_small_capital_allocation_v170.py — allocation template tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.enums_v170 import MarketRegime, AllocationBucket
from paper_trading.small_capital_strategy.capital_profile_v170 import (
    get_300k_template, TEMPLATE_300K_ID,
)
from paper_trading.small_capital_strategy.allocation_template_v170 import (
    get_allocation_for_regime, validate_allocation,
    BULL_ALLOCATION, RANGE_ALLOCATION, BEAR_ALLOCATION, UNKNOWN_ALLOCATION,
)


def _bucket_pct(alloc, bucket):
    for b in alloc.buckets:
        if b.bucket == bucket:
            return b.target_pct
    return 0.0


def test_bull_allocation_core_40pct():
    assert BULL_ALLOCATION[AllocationBucket.CORE] == 0.40


def test_bull_allocation_swing_35pct():
    assert BULL_ALLOCATION[AllocationBucket.MAIN_THEME_SWING] == 0.35


def test_bull_allocation_cash_5pct():
    assert BULL_ALLOCATION[AllocationBucket.CASH] == 0.05


def test_range_allocation_cash_25pct():
    assert RANGE_ALLOCATION[AllocationBucket.CASH] == 0.25


def test_bear_allocation_cash_50pct():
    assert BEAR_ALLOCATION[AllocationBucket.CASH] == 0.50


def test_bear_allocation_short_term_0pct():
    assert BEAR_ALLOCATION[AllocationBucket.SHORT_TERM_TRAINING] == 0.0


def test_unknown_allocation_cash_40pct():
    assert UNKNOWN_ALLOCATION[AllocationBucket.CASH] == 0.40


def test_get_allocation_bull():
    alloc = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, 300000.0)
    assert alloc is not None
    assert alloc.regime == MarketRegime.BULL


def test_get_allocation_range():
    alloc = get_allocation_for_regime(MarketRegime.RANGE, TEMPLATE_300K_ID, 300000.0)
    assert alloc.regime == MarketRegime.RANGE


def test_get_allocation_bear_cash():
    alloc = get_allocation_for_regime(MarketRegime.BEAR, TEMPLATE_300K_ID, 300000.0)
    assert alloc.cash_pct >= 0.49


def test_get_allocation_risk_off():
    alloc = get_allocation_for_regime(MarketRegime.RISK_OFF, TEMPLATE_300K_ID, 300000.0)
    assert alloc.cash_pct >= 0.49


def test_get_allocation_unknown():
    alloc = get_allocation_for_regime(MarketRegime.UNKNOWN, TEMPLATE_300K_ID, 300000.0)
    assert alloc.cash_pct >= 0.39


def test_allocation_total_100_pct_bull():
    alloc = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, 300000.0)
    total = sum(b.target_pct for b in alloc.buckets)
    assert abs(total - 1.0) < 0.001


def test_allocation_total_100_pct_bear():
    alloc = get_allocation_for_regime(MarketRegime.BEAR, TEMPLATE_300K_ID, 300000.0)
    total = sum(b.target_pct for b in alloc.buckets)
    assert abs(total - 1.0) < 0.001


def test_validate_allocation_bull_pass():
    alloc = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, 300000.0)
    result = validate_allocation(alloc)
    assert result["valid"] is True


def test_validate_allocation_bear_pass():
    alloc = get_allocation_for_regime(MarketRegime.BEAR, TEMPLATE_300K_ID, 300000.0)
    result = validate_allocation(alloc)
    assert result["valid"] is True


def test_allocation_paper_only():
    alloc = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, 300000.0)
    assert alloc.paper_only is True


def test_allocation_no_real_orders():
    alloc = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, 300000.0)
    assert alloc.no_real_orders is True


def test_short_term_training_max_5pct_bull():
    alloc = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, 300000.0)
    st_pct = _bucket_pct(alloc, AllocationBucket.SHORT_TERM_TRAINING)
    assert st_pct <= 0.05


def test_allocation_buckets_is_list():
    alloc = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, 300000.0)
    assert isinstance(alloc.buckets, list)
    assert len(alloc.buckets) == 5
