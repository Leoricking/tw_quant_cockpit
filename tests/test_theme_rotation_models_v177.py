"""tests/test_theme_rotation_models_v177.py — v1.7.7 model tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory, ThemeGrade, ThemeSignalType
from paper_trading.small_capital_strategy.theme_rotation_models_v177 import (
    ThemeSignal, ThemeStrengthScore, ThemeMomentumScore, ThemeBreadthScore,
    ThemeContinuationScore, ThemeRiskScore, ThemeRotationRank, ThemeStockMapping,
    ThemeWatchlistCandidate, ThemeRotationDashboard, ThemeRotationReport,
    ThemeRotationHealthSummary,
)


class TestThemeSignal:
    def test_paper_only_default(self):
        sig = ThemeSignal()
        assert sig.paper_only is True

    def test_research_only_default(self):
        sig = ThemeSignal()
        assert sig.research_only is True

    def test_no_real_orders_default(self):
        sig = ThemeSignal()
        assert sig.no_real_orders is True

    def test_no_broker_default(self):
        sig = ThemeSignal()
        assert sig.no_broker is True

    def test_not_investment_advice_default(self):
        sig = ThemeSignal()
        assert sig.not_investment_advice is True

    def test_schema_version_177(self):
        sig = ThemeSignal()
        assert sig.schema_version == "177"

    def test_policy_version_correct(self):
        sig = ThemeSignal()
        assert sig.policy_version == "1.7.7-theme-rotation-scanner"

    def test_instantiate_with_values(self):
        sig = ThemeSignal(
            theme=ThemeCategory.AI_SERVER,
            signal_type=ThemeSignalType.BREADTH,
            value=0.85,
            date="2026-07-10",
        )
        assert sig.theme == ThemeCategory.AI_SERVER
        assert sig.value == 0.85


class TestThemeStrengthScore:
    def test_paper_only_default(self):
        ss = ThemeStrengthScore()
        assert ss.paper_only is True

    def test_no_broker_default(self):
        ss = ThemeStrengthScore()
        assert ss.no_broker is True

    def test_schema_version_177(self):
        ss = ThemeStrengthScore()
        assert ss.schema_version == "177"

    def test_default_grade_watch(self):
        ss = ThemeStrengthScore()
        assert ss.grade == ThemeGrade.WATCH

    def test_default_score_zero(self):
        ss = ThemeStrengthScore()
        assert ss.score == 0.0


class TestThemeMomentumScore:
    def test_paper_only_default(self):
        ms = ThemeMomentumScore()
        assert ms.paper_only is True

    def test_no_real_orders_default(self):
        ms = ThemeMomentumScore()
        assert ms.no_real_orders is True

    def test_schema_version_177(self):
        ms = ThemeMomentumScore()
        assert ms.schema_version == "177"


class TestThemeBreadthScore:
    def test_paper_only_default(self):
        bs = ThemeBreadthScore()
        assert bs.paper_only is True

    def test_no_broker_default(self):
        bs = ThemeBreadthScore()
        assert bs.no_broker is True

    def test_schema_version_177(self):
        bs = ThemeBreadthScore()
        assert bs.schema_version == "177"

    def test_default_total_zero(self):
        bs = ThemeBreadthScore()
        assert bs.total == 0


class TestThemeContinuationScore:
    def test_paper_only_default(self):
        cs = ThemeContinuationScore()
        assert cs.paper_only is True

    def test_schema_version_177(self):
        cs = ThemeContinuationScore()
        assert cs.schema_version == "177"

    def test_default_consecutive_zero(self):
        cs = ThemeContinuationScore()
        assert cs.consecutive_up_days == 0


class TestThemeRiskScore:
    def test_paper_only_default(self):
        rs = ThemeRiskScore()
        assert rs.paper_only is True

    def test_no_real_orders_default(self):
        rs = ThemeRiskScore()
        assert rs.no_real_orders is True

    def test_schema_version_177(self):
        rs = ThemeRiskScore()
        assert rs.schema_version == "177"

    def test_default_risk_false(self):
        rs = ThemeRiskScore()
        assert rs.institutional_selling is False


class TestThemeRotationRank:
    def test_paper_only_default(self):
        rr = ThemeRotationRank()
        assert rr.paper_only is True

    def test_no_broker_default(self):
        rr = ThemeRotationRank()
        assert rr.no_broker is True

    def test_schema_version_177(self):
        rr = ThemeRotationRank()
        assert rr.schema_version == "177"

    def test_default_rank_zero(self):
        rr = ThemeRotationRank()
        assert rr.rank == 0


class TestThemeStockMapping:
    def test_paper_only_default(self):
        sm = ThemeStockMapping()
        assert sm.paper_only is True

    def test_no_real_orders_default(self):
        sm = ThemeStockMapping()
        assert sm.no_real_orders is True

    def test_schema_version_177(self):
        sm = ThemeStockMapping()
        assert sm.schema_version == "177"

    def test_instantiate_with_symbol(self):
        sm = ThemeStockMapping(symbol="2330", theme=ThemeCategory.SEMICONDUCTOR)
        assert sm.symbol == "2330"


class TestThemeWatchlistCandidate:
    def test_paper_only_default(self):
        wc = ThemeWatchlistCandidate()
        assert wc.paper_only is True

    def test_not_eligible_default(self):
        wc = ThemeWatchlistCandidate()
        assert wc.eligible is False

    def test_schema_version_177(self):
        wc = ThemeWatchlistCandidate()
        assert wc.schema_version == "177"


class TestThemeRotationDashboard:
    def test_paper_only_default(self):
        d = ThemeRotationDashboard()
        assert d.paper_only is True

    def test_no_broker_default(self):
        d = ThemeRotationDashboard()
        assert d.no_broker is True

    def test_schema_version_177(self):
        d = ThemeRotationDashboard()
        assert d.schema_version == "177"

    def test_default_market_regime_bull(self):
        d = ThemeRotationDashboard()
        assert d.market_regime == "BULL"


class TestThemeRotationReport:
    def test_paper_only_default(self):
        r = ThemeRotationReport()
        assert r.paper_only is True

    def test_no_real_orders_default(self):
        r = ThemeRotationReport()
        assert r.no_real_orders is True

    def test_schema_version_177(self):
        r = ThemeRotationReport()
        assert r.schema_version == "177"

    def test_default_format_text(self):
        r = ThemeRotationReport()
        assert r.report_format == "text"


class TestThemeRotationHealthSummary:
    def test_paper_only_default(self):
        hs = ThemeRotationHealthSummary()
        assert hs.paper_only is True

    def test_no_broker_default(self):
        hs = ThemeRotationHealthSummary()
        assert hs.no_broker is True

    def test_schema_version_177(self):
        hs = ThemeRotationHealthSummary()
        assert hs.schema_version == "177"

    def test_all_passed_default_true(self):
        hs = ThemeRotationHealthSummary()
        assert hs.all_passed is True
