"""tests/test_theme_rotation_integration_v177.py — v1.7.7 integration tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory, ThemeGrade, ThemeSignalType
from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeSignal, ThemeStrengthScore
from paper_trading.small_capital_strategy.theme_rotation_breadth_v177 import calculate_breadth_score
from paper_trading.small_capital_strategy.theme_rotation_momentum_v177 import calculate_momentum_score
from paper_trading.small_capital_strategy.theme_rotation_continuation_v177 import calculate_continuation_score
from paper_trading.small_capital_strategy.theme_rotation_risk_v177 import calculate_risk_score
from paper_trading.small_capital_strategy.theme_rotation_rank_v177 import rank_themes, get_top_n_themes, get_leader_themes
from paper_trading.small_capital_strategy.theme_rotation_dashboard_v177 import build_dashboard
from paper_trading.small_capital_strategy.theme_rotation_report_v177 import build_report


def _make_theme_scores():
    return [
        ThemeStrengthScore(theme=ThemeCategory.AI_SERVER,        score=90.0, grade=ThemeGrade.LEADER),
        ThemeStrengthScore(theme=ThemeCategory.SEMICONDUCTOR,    score=82.0, grade=ThemeGrade.LEADER),
        ThemeStrengthScore(theme=ThemeCategory.GPU_SERVER,       score=72.0, grade=ThemeGrade.STRONG),
        ThemeStrengthScore(theme=ThemeCategory.COOLING,          score=65.0, grade=ThemeGrade.STRONG),
        ThemeStrengthScore(theme=ThemeCategory.HIGH_SPEED_TRANSMISSION, score=55.0, grade=ThemeGrade.WATCH),
        ThemeStrengthScore(theme=ThemeCategory.PCB,              score=45.0, grade=ThemeGrade.WEAK),
        ThemeStrengthScore(theme=ThemeCategory.BIOTECH,          score=20.0, grade=ThemeGrade.EXCLUDED),
    ]


class TestEndToEndPipeline:
    def test_full_pipeline_creates_report(self):
        scores = _make_theme_scores()
        ranks = rank_themes(scores)
        dashboard = build_dashboard(ranks, "2026-07-10", "BULL")
        report = build_report(dashboard)
        assert report.paper_only is True
        assert len(report.sections) == 5

    def test_top_theme_is_ai_server(self):
        scores = _make_theme_scores()
        ranks = rank_themes(scores)
        dashboard = build_dashboard(ranks, "2026-07-10")
        report = build_report(dashboard)
        assert report.top_theme == ThemeCategory.AI_SERVER

    def test_leader_count_correct(self):
        scores = _make_theme_scores()
        ranks = rank_themes(scores)
        dashboard = build_dashboard(ranks, "2026-07-10")
        assert dashboard.leader_count == 2

    def test_strong_count_correct(self):
        scores = _make_theme_scores()
        ranks = rank_themes(scores)
        dashboard = build_dashboard(ranks, "2026-07-10")
        assert dashboard.strong_count == 2

    def test_top_5_themes(self):
        scores = _make_theme_scores()
        ranks = rank_themes(scores)
        top5 = get_top_n_themes(ranks, 5)
        assert len(top5) == 5

    def test_leader_filter(self):
        scores = _make_theme_scores()
        ranks = rank_themes(scores)
        leaders = get_leader_themes(ranks)
        assert len(leaders) == 2

    def test_all_scores_bounded(self):
        bs = calculate_breadth_score(8, 2, 10, ThemeCategory.AI_SERVER)
        ms = calculate_momentum_score(ThemeCategory.AI_SERVER, 15.0, 25.0, 35.0)
        cs = calculate_continuation_score(ThemeCategory.AI_SERVER, 4, True, True)
        rs = calculate_risk_score(ThemeCategory.AI_SERVER, 0.3, False, False, False)
        assert 0 <= bs.score <= 100
        assert 0 <= ms.score <= 100
        assert 0 <= cs.score <= 100
        assert 0 <= rs.score <= 100


class TestSafetyInvariantsAcrossModules:
    def test_all_models_paper_only(self):
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import (
            ThemeSignal, ThemeStrengthScore, ThemeMomentumScore, ThemeBreadthScore,
            ThemeContinuationScore, ThemeRiskScore, ThemeRotationRank,
        )
        models = [
            ThemeSignal(), ThemeStrengthScore(), ThemeMomentumScore(),
            ThemeBreadthScore(), ThemeContinuationScore(), ThemeRiskScore(),
            ThemeRotationRank(),
        ]
        for m in models:
            assert m.paper_only is True
            assert m.no_broker is True

    def test_safety_audit_passes(self):
        from paper_trading.small_capital_strategy.theme_rotation_safety_v177 import run_safety_audit
        result = run_safety_audit()
        assert result["all_safe"] is True

    def test_health_check_passes(self):
        from paper_trading.small_capital_strategy.theme_rotation_health_v177 import run_health_check
        result = run_health_check()
        assert result.all_passed is True

    def test_no_broker_in_safety_flags(self):
        from paper_trading.small_capital_strategy.theme_rotation_safety_v177 import SAFETY_FLAGS
        assert SAFETY_FLAGS["no_broker"] is True

    def test_no_margin_in_safety_flags(self):
        from paper_trading.small_capital_strategy.theme_rotation_safety_v177 import SAFETY_FLAGS
        assert SAFETY_FLAGS["no_margin"] is True

    def test_scenarios_and_fixtures_both_paper_only(self):
        from paper_trading.small_capital_strategy.theme_rotation_scenarios_v177 import get_scenarios
        from paper_trading.small_capital_strategy.theme_rotation_fixture_registry_v177 import get_fixtures
        for s in get_scenarios():
            assert s["paper_only"] is True
        for f in get_fixtures():
            assert f["paper_only"] is True

    def test_version_matches_throughout(self):
        from paper_trading.small_capital_strategy.version_v177 import VERSION
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeSignal
        sig = ThemeSignal()
        assert sig.schema_version == "177"
        assert VERSION == "1.7.7"

    def test_gui_panel_version_177(self):
        from gui.small_capital_strategy_panel import PANEL_VERSION
        assert PANEL_VERSION == "1.8.2"
