"""tests/test_watchlist_enums_v171.py — enum tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, WatchlistCandidateStatus, WatchlistDecision,
    WatchlistExclusionReason, WatchlistSortKey,
    ThemeCategory, ThemeStrength, LiquidityGrade, RevenueGrowthGrade,
    TechnicalStrengthGrade, InstitutionalGrade, FinancingRiskGrade,
    CandidatePoolType, OverdiversificationStatus, RankingGrade,
    SmallCapitalTradability, WatchlistReportFormat, ValidationSeverity,
)


def test_watchlist_tier_core():
    assert WatchlistTier.CORE.value == "CORE"


def test_watchlist_tier_main_theme():
    assert WatchlistTier.MAIN_THEME.value == "MAIN_THEME"


def test_watchlist_tier_second_wave():
    assert WatchlistTier.SECOND_WAVE.value == "SECOND_WAVE"


def test_watchlist_tier_training():
    assert WatchlistTier.TRAINING.value == "TRAINING"


def test_watchlist_tier_excluded():
    assert WatchlistTier.EXCLUDED.value == "EXCLUDED"


def test_watchlist_tier_five_values():
    assert len(list(WatchlistTier)) == 5


def test_theme_strength_leading():
    assert ThemeStrength.LEADING.value == "LEADING"


def test_theme_strength_strong():
    assert ThemeStrength.STRONG.value == "STRONG"


def test_theme_strength_moderate():
    assert ThemeStrength.MODERATE.value == "MODERATE"


def test_theme_strength_weak():
    assert ThemeStrength.WEAK.value == "WEAK"


def test_theme_strength_unknown():
    assert ThemeStrength.UNKNOWN.value == "UNKNOWN"


def test_theme_strength_five_values():
    assert len(list(ThemeStrength)) == 5


def test_exclusion_reason_weak_theme():
    assert WatchlistExclusionReason.WEAK_THEME is not None


def test_exclusion_reason_low_liquidity():
    assert WatchlistExclusionReason.LOW_LIQUIDITY is not None


def test_exclusion_reason_below_20ma():
    assert WatchlistExclusionReason.BELOW_20MA is not None


def test_exclusion_reason_below_60ma():
    assert WatchlistExclusionReason.BELOW_60MA is not None


def test_exclusion_reason_financing_overheated():
    assert WatchlistExclusionReason.FINANCING_OVERHEATED is not None


def test_exclusion_reason_institutional_heavy_selling():
    assert WatchlistExclusionReason.INSTITUTIONAL_HEAVY_SELLING is not None


def test_exclusion_reason_real_trading_requested():
    assert WatchlistExclusionReason.REAL_TRADING_REQUESTED is not None


def test_exclusion_reason_broker_requested():
    assert WatchlistExclusionReason.BROKER_REQUESTED is not None


def test_exclusion_reason_margin_not_allowed():
    assert WatchlistExclusionReason.MARGIN_NOT_ALLOWED is not None


def test_exclusion_reason_not_research_safe():
    assert WatchlistExclusionReason.NOT_RESEARCH_SAFE is not None


def test_exclusion_reasons_count_gte_15():
    assert len(list(WatchlistExclusionReason)) >= 15


def test_ranking_grade_a():
    assert RankingGrade.A.value == "A"


def test_ranking_grade_no_a_plus():
    values = [g.value for g in RankingGrade]
    assert "A+" not in values


def test_ranking_grade_blocked():
    assert RankingGrade.BLOCKED.value == "BLOCKED"


def test_overdiversification_optimal():
    assert OverdiversificationStatus.OPTIMAL is not None


def test_overdiversification_overdiversified():
    assert OverdiversificationStatus.OVERDIVERSIFIED is not None


def test_overdiversification_insufficient():
    assert OverdiversificationStatus.INSUFFICIENT_COVERAGE is not None


def test_liquidity_grade_high():
    assert LiquidityGrade.HIGH.value == "HIGH"


def test_liquidity_grade_blocked():
    assert LiquidityGrade.BLOCKED.value == "BLOCKED"


def test_report_format_markdown():
    assert WatchlistReportFormat.MARKDOWN.value == "MARKDOWN"


def test_report_format_json():
    assert WatchlistReportFormat.JSON.value == "JSON"


def test_report_format_csv():
    assert WatchlistReportFormat.CSV.value == "CSV"


def test_sort_key_total_score():
    assert WatchlistSortKey.TOTAL_SCORE.value == "TOTAL_SCORE"


def test_small_capital_tradability_tradable():
    assert SmallCapitalTradability.TRADABLE.value == "TRADABLE"


def test_small_capital_tradability_excluded():
    assert SmallCapitalTradability.EXCLUDED.value == "EXCLUDED"
