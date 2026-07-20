"""
tests/test_paper_cockpit_review_loop_v204.py
v2.0.4 Portfolio Review Loop Engine Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

def test_portfolio_review_loop_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.all_passed is True
    assert result.paper_only is True
    assert result.no_real_orders is True

def test_portfolio_review_loop_with_period():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, PortfolioReviewInput
    inp = PortfolioReviewInput(review_period="2026-W29")
    result = run_portfolio_review(inp)
    assert result.review_period == "2026-W29"

def test_portfolio_review_loop_with_decisions():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, PortfolioReviewInput
    inp = PortfolioReviewInput(decision_snapshot=["2330", "2317", "2454"])
    result = run_portfolio_review(inp)
    assert len(result.decision_snapshot) == 3

def test_portfolio_review_loop_with_profiles():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, PortfolioReviewInput
    inp = PortfolioReviewInput(strategy_profile_ids=["P001", "P002"])
    result = run_portfolio_review(inp)
    assert len(result.strategy_profile_summary) == 2

def test_portfolio_review_loop_blocked_reasons():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, PortfolioReviewInput
    inp = PortfolioReviewInput(blocked_reason_summary=["low_score", "high_risk"])
    result = run_portfolio_review(inp)
    assert result.blocked_reason_summary.total_blocked == 2

def test_portfolio_review_loop_risk_usage():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, PortfolioReviewInput
    inp = PortfolioReviewInput(risk_usage_summary={"total_risk_budget_pct": 20.0, "used_risk_pct": 10.0})
    result = run_portfolio_review(inp)
    assert result.risk_usage_summary.used_risk_pct == 10.0

def test_portfolio_review_loop_recommendations_non_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert len(result.improvement_recommendations) > 0

def test_portfolio_review_loop_all_recs_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    for rec in result.improvement_recommendations:
        assert rec.should_auto_apply is False

def test_portfolio_review_loop_all_recs_human_approval():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    for rec in result.improvement_recommendations:
        assert rec.requires_human_approval is True

def test_portfolio_review_loop_review_id_non_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.review_id != ""

def test_portfolio_review_loop_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.review_version == "2.0.4"

def test_portfolio_review_loop_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.schema_version == "204"

def test_portfolio_review_loop_blocked_reason_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.blocked_reason_summary.paper_only is True

def test_portfolio_review_loop_risk_usage_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.risk_usage_summary.paper_only is True

def test_portfolio_review_loop_strategy_profile_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    for pr in result.strategy_profile_summary:
        assert pr.paper_only is True

def test_weekly_pack_from_review_loop():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, build_weekly_improvement_pack
    review = run_portfolio_review()
    pack = build_weekly_improvement_pack(review, "2026-W29")
    assert pack.should_auto_apply is False
    assert pack.paper_only is True

def test_weekly_pack_week_id_non_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, build_weekly_improvement_pack
    review = run_portfolio_review()
    pack = build_weekly_improvement_pack(review, "2026-W29")
    assert pack.week_id != ""

def test_weekly_pack_review_metrics_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, build_weekly_improvement_pack
    review = run_portfolio_review()
    pack = build_weekly_improvement_pack(review)
    assert pack.review_metrics is not None
    assert pack.review_metrics.final_review_grade in ("A", "B", "C", "D")

def test_weekly_pack_simulation_vs_decision_gap():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, build_weekly_improvement_pack
    review = run_portfolio_review()
    pack = build_weekly_improvement_pack(review)
    assert isinstance(pack.simulation_vs_decision_gap, dict)

def test_weekly_pack_reviewed_decision_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, build_weekly_improvement_pack, PortfolioReviewInput
    inp = PortfolioReviewInput(decision_snapshot=["2330", "2317"])
    review = run_portfolio_review(inp)
    pack = build_weekly_improvement_pack(review)
    assert pack.reviewed_decision_count == 2

def test_weekly_pack_do_not_change_rules_non_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert len(pack.do_not_change_rules) > 0

def test_weekly_pack_human_review_required_items():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert len(pack.human_review_required_items) > 0

def test_strategy_profile_review_has_allowed_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _build_strategy_profile_review
    pr = _build_strategy_profile_review("R001", "P001", ["2330", "2317"], [])
    assert pr.allowed_count == 2
    assert pr.blocked_count == 0

def test_strategy_profile_review_with_blocks():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _build_strategy_profile_review
    pr = _build_strategy_profile_review("R001", "P001", ["2330", "2317"], ["2317"])
    assert pr.blocked_count == 1

def test_strategy_profile_review_gap_structure():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _build_strategy_profile_review
    pr = _build_strategy_profile_review("R001", "P001", ["2330"], [])
    assert "simulation_allowed" in pr.simulation_vs_decision_gap
    assert "actual_decisions" in pr.simulation_vs_decision_gap
