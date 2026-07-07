"""tests/test_small_capital_models_v170.py — model tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.models_v170 import (
    CapitalProfile, RiskBudget, AllocationTemplate, MarketRegimeResult,
    WatchlistProfile, BuyPointSignal, EntryPlan, ExitPlan,
    StopLossPlan, TakeProfitPlan, PositionSizingResult, CashControlPlan,
    ForbiddenTradeCheck, TradePlanValidationResult, SmallCapitalSimulationInput,
    SmallCapitalSimulationResult, SmallCapitalScorecard, SmallCapitalReport,
    SmallCapitalStrategyTemplate, ThemeFilterResult, PositionSizingInput,
)
from paper_trading.small_capital_strategy.enums_v170 import (
    MarketRegime, AllocationBucket, SmallCapitalGrade, BuyPointType,
    StrategyTemplateStatus,
)


def test_capital_profile_paper_only():
    cp = CapitalProfile(
        template_id="t1",
        capital_twd=300000.0,
        max_loss_default=3000.0,
        max_loss_min=2400.0,
        max_loss_max=4500.0,
        risk_pct_default=0.01,
        risk_pct_min=0.008,
        risk_pct_max=0.015,
        max_holdings_default=4,
        max_holdings_min=1,
        max_holdings_max=4,
    )
    assert cp.paper_only is True
    assert cp.research_only is True
    assert cp.no_real_orders is True
    assert cp.not_investment_advice is True


def test_capital_profile_schema_version():
    cp = CapitalProfile(
        template_id="t1",
        capital_twd=300000.0,
        max_loss_default=3000.0,
        max_loss_min=2400.0,
        max_loss_max=4500.0,
        risk_pct_default=0.01,
        risk_pct_min=0.008,
        risk_pct_max=0.015,
        max_holdings_default=4,
        max_holdings_min=1,
        max_holdings_max=4,
    )
    assert cp.schema_version == "170"


def test_risk_budget_paper_only():
    from paper_trading.small_capital_strategy.capital_profile_v170 import get_300k_template
    from paper_trading.small_capital_strategy.risk_budget_v170 import compute_risk_budget
    profile = get_300k_template()
    rb = compute_risk_budget(profile)
    assert rb.paper_only is True
    assert rb.no_real_orders is True


def test_allocation_template_paper_only():
    from paper_trading.small_capital_strategy.allocation_template_v170 import get_allocation_for_regime
    from paper_trading.small_capital_strategy.capital_profile_v170 import TEMPLATE_300K_ID
    at = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, 300000.0)
    assert at.paper_only is True
    assert at.no_real_orders is True


def test_allocation_template_total_100():
    from paper_trading.small_capital_strategy.allocation_template_v170 import get_allocation_for_regime
    from paper_trading.small_capital_strategy.capital_profile_v170 import TEMPLATE_300K_ID
    at = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, 300000.0)
    total = sum(b.target_pct for b in at.buckets)
    assert abs(total - 1.0) < 0.001


def test_market_regime_result_paper_only():
    mr = MarketRegimeResult(
        regime=MarketRegime.BULL,
        max_invested_pct=0.95,
        cash_min_pct=0.05,
        short_term_training_allowed=True,
    )
    assert mr.paper_only is True


def test_scorecard_paper_only():
    sc = SmallCapitalScorecard(
        template_id="t1",
        score=85.0,
        grade=SmallCapitalGrade.A,
        risk_budget_compliance=1.0,
        position_sizing_correctness=1.0,
        buy_point_quality=1.0,
        market_regime_alignment=1.0,
        watchlist_quality=0.6,
        exit_plan_completeness=0.6,
        safety_compliance=1.0,
        safety_blocked=False,
    )
    assert sc.paper_only is True
    assert sc.no_real_orders is True


def test_scorecard_schema_version():
    sc = SmallCapitalScorecard(
        template_id="t1",
        score=85.0,
        grade=SmallCapitalGrade.A,
        risk_budget_compliance=1.0,
        position_sizing_correctness=1.0,
        buy_point_quality=1.0,
        market_regime_alignment=1.0,
        watchlist_quality=0.6,
        exit_plan_completeness=0.6,
        safety_compliance=1.0,
        safety_blocked=False,
    )
    assert sc.schema_version == "170"


def test_report_paper_only():
    sc = SmallCapitalScorecard(
        template_id="t1",
        score=85.0,
        grade=SmallCapitalGrade.A,
        risk_budget_compliance=1.0,
        position_sizing_correctness=1.0,
        buy_point_quality=1.0,
        market_regime_alignment=1.0,
        watchlist_quality=0.6,
        exit_plan_completeness=0.6,
        safety_compliance=1.0,
        safety_blocked=False,
    )
    report = SmallCapitalReport(
        template_id="t1",
        sections={},
        scorecard=sc,
    )
    assert report.paper_only is True
    assert report.research_only is True
    assert report.no_real_orders is True
    assert report.not_investment_advice is True


def test_report_to_dict():
    sc = SmallCapitalScorecard(
        template_id="t1",
        score=85.0,
        grade=SmallCapitalGrade.A,
        risk_budget_compliance=1.0,
        position_sizing_correctness=1.0,
        buy_point_quality=1.0,
        market_regime_alignment=1.0,
        watchlist_quality=0.6,
        exit_plan_completeness=0.6,
        safety_compliance=1.0,
        safety_blocked=False,
    )
    report = SmallCapitalReport(
        template_id="t1",
        sections={},
        scorecard=sc,
    )
    d = report.to_dict()
    assert isinstance(d, dict)
    assert d["template_id"] == "t1"


def test_simulation_input_paper_only():
    from paper_trading.small_capital_strategy.enums_v170 import BuyPointType, MarketRegime
    si = SmallCapitalSimulationInput(
        template_id="t1",
        symbol="2330",
        buy_point_type=BuyPointType.A_10MA_PULLBACK,
        entry_price=500.0,
        stop_loss_pct=0.06,
        capital_twd=300000.0,
        regime=MarketRegime.BULL,
    )
    assert si.paper_only is True


def test_simulation_result_paper_only():
    sr = SmallCapitalSimulationResult(
        template_id="t1",
        symbol="2330",
        position_size_twd=50000.0,
        stop_loss_price=470.0,
        status="OK",
    )
    assert sr.paper_only is True


def test_position_sizing_input_fields():
    psi = PositionSizingInput(
        symbol="2330",
        capital_twd=300000.0,
        max_loss_amount=3000.0,
        stop_loss_pct=0.06,
        bucket=AllocationBucket.MAIN_THEME_SWING,
        bucket_remaining_budget=105000.0,
    )
    assert psi.symbol == "2330"
    assert psi.stop_loss_pct == 0.06


def test_theme_filter_result_paper_only():
    tfr = ThemeFilterResult(
        symbol="2330",
        theme="AI",
        theme_strength="STRONG",
        passed=True,
    )
    assert tfr.paper_only is True
