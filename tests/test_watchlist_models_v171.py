"""tests/test_watchlist_models_v171.py — model tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, ThemeStrength, ThemeCategory, WatchlistExclusionReason,
    RankingGrade, OverdiversificationStatus, WatchlistReportFormat, WatchlistSortKey,
    CandidatePoolType,
)
from paper_trading.small_capital_strategy.watchlist_models_v171 import (
    WatchlistCandidate, WatchlistScoreInput, WatchlistScoreResult,
    ThemeRotationSignal, ThemeStrengthResult, LiquidityFilterResult,
    RevenueGrowthFilterResult, TechnicalStrengthResult, InstitutionalFilterResult,
    FinancingRiskResult, WatchlistFilterResult, WatchlistTierResult,
    OverdiversificationResult, CandidatePool, RankedCandidate,
    TopCandidateSelection, WatchlistStrategyInput, WatchlistStrategyResult,
    WatchlistStrategyReport, WatchlistHealthSummary,
    WatchlistDecision,
)
from paper_trading.small_capital_strategy.watchlist_candidate_v171 import make_sample_candidate


def test_candidate_paper_only():
    c = make_sample_candidate()
    assert c.paper_only is True


def test_candidate_research_only():
    c = make_sample_candidate()
    assert c.research_only is True


def test_candidate_no_real_orders():
    c = make_sample_candidate()
    assert c.no_real_orders is True


def test_candidate_not_investment_advice():
    c = make_sample_candidate()
    assert c.not_investment_advice is True


def test_candidate_schema_version():
    c = make_sample_candidate()
    assert c.schema_version == "171"


def test_candidate_to_dict_is_dict():
    c = make_sample_candidate()
    assert isinstance(c.to_dict(), dict)


def test_candidate_to_dict_paper_only():
    d = make_sample_candidate().to_dict()
    assert d["paper_only"] is True


def test_candidate_to_dict_not_investment_advice():
    d = make_sample_candidate().to_dict()
    assert d["not_investment_advice"] is True


def test_candidate_exclusion_reasons_list():
    c = make_sample_candidate()
    assert isinstance(c.exclusion_reasons, list)


def test_score_input_paper_only():
    inp = WatchlistScoreInput(
        symbol="X", theme_strength=ThemeStrength.STRONG,
        above_20ma=True, above_60ma=True,
        liquidity_avg_vol=10_000_000, revenue_growth_pct=0.10,
        inst_net_buy_days=8, financing_ratio=0.15,
        atr_pct=0.05, theme_concentration_count=0,
        paper_only=True, research_only=True, no_real_orders=True, not_investment_advice=True,
    )
    assert inp.paper_only is True


def test_score_result_to_dict():
    sr = WatchlistScoreResult(
        symbol="X", theme_strength_score=85.0, technical_score=80.0,
        revenue_growth_score=75.0, liquidity_score=70.0,
        institutional_score=65.0, financing_score=60.0,
        small_capital_fit_score=55.0, total_score=72.5,
        grade=RankingGrade.B,
    )
    d = sr.to_dict()
    assert isinstance(d, dict)
    assert d["symbol"] == "X"
    assert d["paper_only"] is True


def test_overdiversification_result_to_dict():
    ov = OverdiversificationResult(
        total_candidates=20, status=OverdiversificationStatus.OPTIMAL,
        focus_count=8, tradable_count=4, training_count=2, excluded_count=3,
    )
    d = ov.to_dict()
    assert d["status"] == "OPTIMAL"
    assert d["paper_only"] is True


def test_ranked_candidate_to_dict():
    c = make_sample_candidate()
    rc = RankedCandidate(rank=1, candidate=c, rank_reason="test")
    d = rc.to_dict()
    assert d["rank"] == 1
    assert d["paper_only"] is True


def test_top_candidate_selection_to_dict():
    c = make_sample_candidate()
    rc = RankedCandidate(rank=1, candidate=c)
    sel = TopCandidateSelection(
        profile_id="test",
        focus_candidates=[rc],
        tradable_candidates=[rc],
    )
    d = sel.to_dict()
    assert d["focus_count"] == 1
    assert d["tradable_count"] == 1
    assert d["paper_only"] is True


def test_tier_result_to_dict():
    from paper_trading.small_capital_strategy.watchlist_enums_v171 import SmallCapitalTradability
    tr = WatchlistTierResult(
        symbol="X", tier=WatchlistTier.CORE,
        tier_reason="core", small_capital_tradability=SmallCapitalTradability.TRADABLE,
    )
    d = tr.to_dict()
    assert d["tier"] == "CORE"
    assert d["paper_only"] is True


def test_report_to_dict():
    report = WatchlistStrategyReport(
        profile_id="test",
        sections={"not_investment_advice": "Research Only"},
    )
    d = report.to_dict()
    assert d["paper_only"] is True
    assert d["not_investment_advice"] is True


def test_health_summary_model():
    h = WatchlistHealthSummary(
        version="1.7.1", total=70, passed=70, failed=0, status="PASS",
    )
    assert h.paper_only is True
    assert h.status == "PASS"


def test_candidate_pool_total_count():
    c = make_sample_candidate()
    pool = CandidatePool(
        profile_id="test",
        pool_type=CandidatePoolType.FULL_WATCHLIST,
        candidates=[c, c],
    )
    assert pool.total_count == 2


def test_theme_rotation_signal_to_dict():
    sig = ThemeRotationSignal(
        theme="AI", theme_category=ThemeCategory.AI_SEMICONDUCTOR,
        theme_strength=ThemeStrength.STRONG, momentum_score=80.0,
        leader_count=5, breadth_score=0.7, rotation_phase="EARLY",
    )
    d = sig.to_dict()
    assert d["theme_strength"] == "STRONG"
    assert d["paper_only"] is True
