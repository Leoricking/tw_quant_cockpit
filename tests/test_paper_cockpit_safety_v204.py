"""
tests/test_paper_cockpit_safety_v204.py
v2.0.4 Paper Portfolio Review Loop & Weekly Improvement Pack — Safety Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

def test_no_real_orders_constant_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True

def test_safety_paper_only_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["paper_only"] is True

def test_safety_research_only_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["research_only"] is True

def test_safety_review_only_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["review_only"] is True

def test_safety_no_real_orders_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["no_real_orders"] is True

def test_safety_no_broker_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["no_broker"] is True

def test_safety_no_margin_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["no_margin"] is True

def test_safety_no_leverage_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["no_leverage"] is True

def test_safety_no_production_db_write_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["no_production_db_write"] is True

def test_safety_no_real_account_sync_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["no_real_account_sync"] is True

def test_safety_no_automatic_rebalance_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["no_automatic_rebalance"] is True

def test_safety_not_investment_advice_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["not_investment_advice"] is True

def test_safety_human_review_required_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["human_review_required"] is True

def test_safety_should_auto_apply_always_false_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["should_auto_apply_always_false"] is True

def test_safety_paper_only_data_only_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["paper_only_data_only"] is True

def test_safety_broker_execution_disabled_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["broker_execution_disabled"] is True

def test_safety_production_trading_blocked_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["production_trading_blocked"] is True

def test_all_safety_flags_are_bool():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    for k, v in SAFETY_FLAGS_V204.items():
        assert isinstance(v, bool), f"Safety flag {k} is not bool: {type(v)}"

def test_should_auto_apply_invariant_recommendation():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ImprovementRecommendation
    for _ in range(5):
        rec = ImprovementRecommendation(should_auto_apply=True)
        assert rec.should_auto_apply is False, "should_auto_apply must always be False"

def test_should_auto_apply_invariant_weekly_pack():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import WeeklyImprovementPack
    for _ in range(5):
        pack = WeeklyImprovementPack(should_auto_apply=True)
        assert pack.should_auto_apply is False, "WeeklyImprovementPack.should_auto_apply must always be False"

def test_portfolio_review_result_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import PortfolioReviewResult
    result = PortfolioReviewResult()
    assert result.no_broker is True

def test_portfolio_review_result_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import PortfolioReviewResult
    result = PortfolioReviewResult()
    assert result.not_investment_advice is True

def test_portfolio_review_result_research_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import PortfolioReviewResult
    result = PortfolioReviewResult()
    assert result.research_only is True

def test_portfolio_review_result_review_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import PortfolioReviewResult
    result = PortfolioReviewResult()
    assert result.review_only is True

def test_no_real_orders_in_portfolio_review_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import PortfolioReviewInput
    inp = PortfolioReviewInput()
    assert inp.no_real_orders is True
    assert inp.paper_only is True

def test_no_real_orders_in_improvement_recommendation():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ImprovementRecommendation
    rec = ImprovementRecommendation()
    assert rec.no_real_orders is True
    assert rec.paper_only is True

def test_no_real_orders_in_risk_usage_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RiskUsageReview
    review = RiskUsageReview()
    assert review.no_real_orders is True
    assert review.paper_only is True

def test_no_real_orders_in_blocked_reason_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import BlockedReasonReview
    review = BlockedReasonReview()
    assert review.no_real_orders is True
    assert review.paper_only is True

def test_no_real_orders_in_weekly_improvement_pack():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import WeeklyImprovementPack
    pack = WeeklyImprovementPack()
    assert pack.no_real_orders is True
    assert pack.paper_only is True

def test_review_export_result_paper_only_confirmed():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ReviewExportResult
    result = ReviewExportResult()
    assert result.paper_only_confirmed is True

def test_run_portfolio_review_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.paper_only_safety_snapshot is True

def test_audit_snapshot_safety_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, build_review_audit_snapshot
    result = run_portfolio_review()
    snapshot = build_review_audit_snapshot(result)
    assert "PRODUCTION_TRADING_BLOCKED=True" in snapshot.safety_snapshot
    assert "BROKER_EXECUTION_ENABLED=False" in snapshot.safety_snapshot
