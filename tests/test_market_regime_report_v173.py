"""
tests/test_market_regime_report_v173.py
Tests for Market Regime Position Control report_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import json
import pytest
from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    MarketRegimeInput, MarketRegimeReport,
)
from paper_trading.small_capital_strategy.market_regime_detector_v173 import detect_market_regime
from paper_trading.small_capital_strategy.cash_ratio_engine_v173 import build_cash_ratio_plan
from paper_trading.small_capital_strategy.exposure_control_engine_v173 import build_exposure_control_plan
from paper_trading.small_capital_strategy.bucket_adjustment_engine_v173 import build_bucket_adjustment_plan
from paper_trading.small_capital_strategy.candidate_permission_engine_v173 import (
    get_candidate_permission, get_abc_regime_permission,
)
from paper_trading.small_capital_strategy.market_regime_scorecard_v173 import build_regime_scorecard
from paper_trading.small_capital_strategy.market_regime_report_v173 import (
    build_market_regime_report, render_report_json, render_report_markdown,
    render_report_console, get_section_names, REPORT_SECTION_NAMES,
)


def _build_report(regime=MarketRegime.BULL):
    inp = MarketRegimeInput(
        index_close=20000, index_ma20=19500, index_ma60=18800, index_ma120=17500,
        index_ma240=16000, advance_decline_ratio=1.8, volatility_score=20.0,
        risk_event_flag=False, major_index_trend_score=1.0,
    )
    detection     = detect_market_regime(inp)
    cash_plan     = build_cash_ratio_plan(regime)
    exposure_plan = build_exposure_control_plan(regime)
    bucket_plan   = build_bucket_adjustment_plan(regime)
    cand_perm     = get_candidate_permission(regime, "MAIN_THEME_SWING")
    abc_perm      = get_abc_regime_permission(regime)
    scorecard     = build_regime_scorecard(regime, detection, cash_plan, exposure_plan, cand_perm, abc_perm)
    return build_market_regime_report(
        regime, detection, cash_plan, exposure_plan, bucket_plan, cand_perm, abc_perm, scorecard
    )


class TestBuildMarketRegimeReport:
    def test_returns_report_object(self):
        report = _build_report()
        assert isinstance(report, MarketRegimeReport)

    def test_has_14_sections(self):
        report = _build_report()
        assert len(report.sections) == 14

    def test_paper_only(self):
        report = _build_report()
        assert report.paper_only is True

    def test_no_real_orders(self):
        report = _build_report()
        assert report.no_real_orders is True

    def test_not_investment_advice(self):
        report = _build_report()
        assert report.not_investment_advice is True

    def test_regime_stored(self):
        report = _build_report(MarketRegime.BULL)
        assert report.regime == MarketRegime.BULL

    def test_report_format_json(self):
        report = _build_report()
        assert report.report_format == "JSON"

    def test_schema_version(self):
        report = _build_report()
        assert report.schema_version == "173"


class TestSectionNames:
    def test_get_section_names_returns_14(self):
        assert len(get_section_names()) == 14

    def test_version_section_present(self):
        assert "version" in REPORT_SECTION_NAMES

    def test_safety_summary_section_present(self):
        assert "safety_summary" in REPORT_SECTION_NAMES

    def test_scorecard_section_present(self):
        assert "scorecard" in REPORT_SECTION_NAMES

    def test_regime_summary_section_present(self):
        assert "regime_summary" in REPORT_SECTION_NAMES


class TestRenderJson:
    def test_returns_string(self):
        report = _build_report()
        assert isinstance(render_report_json(report), str)

    def test_valid_json(self):
        report = _build_report()
        data = json.loads(render_report_json(report))
        assert isinstance(data, dict)

    def test_json_paper_only(self):
        report = _build_report()
        data = json.loads(render_report_json(report))
        assert data["paper_only"] is True

    def test_json_no_real_orders(self):
        report = _build_report()
        data = json.loads(render_report_json(report))
        assert data["no_real_orders"] is True

    def test_json_not_investment_advice(self):
        report = _build_report()
        data = json.loads(render_report_json(report))
        assert data["not_investment_advice"] is True


class TestRenderMarkdown:
    def test_returns_string(self):
        report = _build_report()
        assert isinstance(render_report_markdown(report), str)

    def test_contains_title(self):
        report = _build_report()
        md = render_report_markdown(report)
        assert "Market Regime" in md

    def test_contains_disclaimer(self):
        report = _build_report()
        md = render_report_markdown(report)
        assert "Research Only" in md or "Paper Only" in md


class TestRenderConsole:
    def test_returns_string(self):
        report = _build_report()
        assert isinstance(render_report_console(report), str)

    def test_contains_regime(self):
        report = _build_report()
        console = render_report_console(report)
        assert "BULL" in console or "Regime" in console
