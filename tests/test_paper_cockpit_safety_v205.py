"""
tests/test_paper_cockpit_safety_v205.py
v2.0.5 Safety & Paper-Only Guard Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


# -------------------------------------------------------------------------
# should_auto_apply always False
# -------------------------------------------------------------------------
def test_promotion_decision_should_auto_apply_always_false_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import PromotionDecision
    dec = PromotionDecision()
    assert dec.should_auto_apply is False

def test_promotion_decision_should_auto_apply_always_false_when_true_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import PromotionDecision
    dec = PromotionDecision(should_auto_apply=True)
    assert dec.should_auto_apply is False

def test_rotation_result_should_auto_apply_always_false_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WatchlistRotationResult
    res = WatchlistRotationResult()
    assert res.should_auto_apply is False

def test_rotation_result_should_auto_apply_always_false_when_true_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WatchlistRotationResult
    res = WatchlistRotationResult(should_auto_apply=True)
    assert res.should_auto_apply is False

def test_run_rotation_output_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.should_auto_apply is False

def test_all_promotion_queue_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    for dec in result.promotion_queue:
        assert dec.should_auto_apply is False

def test_all_demotion_queue_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    for dec in result.demotion_queue:
        assert dec.should_auto_apply is False

def test_all_remove_queue_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    for dec in result.remove_queue:
        assert dec.should_auto_apply is False

# -------------------------------------------------------------------------
# Paper-only flags
# -------------------------------------------------------------------------
def test_no_real_orders_global():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True

def test_safety_flag_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["paper_only"] is True

def test_safety_flag_research_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["research_only"] is True

def test_safety_flag_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["no_broker"] is True

def test_safety_flag_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["no_real_orders"] is True

def test_safety_flag_no_production_db_write():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["no_production_db_write"] is True

def test_safety_flag_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["no_real_account_sync"] is True

def test_safety_flag_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["no_automatic_rebalance"] is True

def test_safety_flag_no_live_strategy_activation():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["no_live_strategy_activation"] is True

def test_safety_flag_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["not_investment_advice"] is True

def test_safety_flag_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["human_review_required"] is True

def test_safety_flag_paper_only_data_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["paper_only_data_only"] is True

def test_safety_flag_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["broker_execution_disabled"] is True

def test_safety_flag_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["production_trading_blocked"] is True

def test_safety_flag_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["should_auto_apply_always_false"] is True

# -------------------------------------------------------------------------
# No broker / no real order guard
# -------------------------------------------------------------------------
def test_rotation_result_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.no_broker is True

def test_rotation_result_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.paper_only_safety_snapshot is True

def test_gui_tab_no_real_orders():
    from gui.small_capital_strategy_panel import render_watchlist_rotation_v205_tab
    result = render_watchlist_rotation_v205_tab()
    assert result["no_real_orders"] is True

def test_gui_tab_production_trading_blocked():
    from gui.small_capital_strategy_panel import render_watchlist_rotation_v205_tab
    result = render_watchlist_rotation_v205_tab()
    assert result["production_trading_blocked"] is True

def test_gui_tab_not_investment_advice():
    from gui.small_capital_strategy_panel import render_watchlist_rotation_v205_tab
    result = render_watchlist_rotation_v205_tab()
    assert result["not_investment_advice"] is True
