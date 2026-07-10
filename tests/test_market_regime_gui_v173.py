"""
tests/test_market_regime_gui_v173.py
Tests for Market Regime Position Control GUI panel v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS, _TABS_V173_REGIME,
    get_tab_names, get_regime_tab_names,
    render_regime_overview_tab, render_regime_detection_tab,
    render_regime_trend_filter_tab, render_regime_volatility_filter_tab,
    render_regime_breadth_filter_tab, render_regime_risk_off_detection_tab,
    render_regime_cash_ratio_tab, render_regime_exposure_control_tab,
    render_regime_bucket_adjustment_tab, render_regime_candidate_permission_tab,
    render_regime_abc_compatibility_tab, render_regime_scorecard_tab,
    render_regime_report_tab, render_regime_health_gate_tab,
)


class TestPanelVersion:
    def test_panel_version_173(self):
        assert PANEL_VERSION == "1.7.8"

    def test_panel_title_contains_173(self):
        assert "1.7.8" in PANEL_TITLE


class TestTabCounts:
    def test_total_tab_count_69(self):
        assert len(_TABS) == 117

    def test_regime_tab_count_14(self):
        assert len(_TABS_V173_REGIME) == 14

    def test_get_tab_names_length_69(self):
        assert len(get_tab_names()) == 117

    def test_get_regime_tab_names_length_14(self):
        assert len(get_regime_tab_names()) == 14


class TestRegimeTabs:
    def test_regime_overview_in_tabs(self):
        assert "regime_overview" in _TABS_V173_REGIME

    def test_regime_health_gate_in_tabs(self):
        assert "regime_health_gate" in _TABS_V173_REGIME

    def test_regime_detection_in_tabs(self):
        assert "regime_detection" in _TABS_V173_REGIME


class TestRenderFunctions:
    def test_render_overview_returns_dict(self):
        result = render_regime_overview_tab()
        assert isinstance(result, dict)

    def test_render_overview_paper_only(self):
        result = render_regime_overview_tab()
        assert result.get("paper_only") is True

    def test_render_overview_no_real_orders(self):
        result = render_regime_overview_tab()
        assert result.get("no_real_orders") is True

    def test_render_detection_returns_dict(self):
        result = render_regime_detection_tab()
        assert isinstance(result, dict)

    def test_render_detection_paper_only(self):
        result = render_regime_detection_tab()
        assert result.get("paper_only") is True

    def test_render_trend_filter_returns_dict(self):
        result = render_regime_trend_filter_tab()
        assert isinstance(result, dict)

    def test_render_volatility_filter_returns_dict(self):
        result = render_regime_volatility_filter_tab()
        assert isinstance(result, dict)

    def test_render_breadth_filter_returns_dict(self):
        result = render_regime_breadth_filter_tab()
        assert isinstance(result, dict)

    def test_render_risk_off_returns_dict(self):
        result = render_regime_risk_off_detection_tab()
        assert isinstance(result, dict)

    def test_render_cash_ratio_returns_dict(self):
        result = render_regime_cash_ratio_tab()
        assert isinstance(result, dict)

    def test_render_cash_ratio_paper_only(self):
        result = render_regime_cash_ratio_tab()
        assert result.get("paper_only") is True

    def test_render_exposure_control_returns_dict(self):
        result = render_regime_exposure_control_tab()
        assert isinstance(result, dict)

    def test_render_bucket_adjustment_returns_dict(self):
        result = render_regime_bucket_adjustment_tab()
        assert isinstance(result, dict)

    def test_render_candidate_permission_returns_dict(self):
        result = render_regime_candidate_permission_tab()
        assert isinstance(result, dict)

    def test_render_abc_compatibility_returns_dict(self):
        result = render_regime_abc_compatibility_tab()
        assert isinstance(result, dict)

    def test_render_scorecard_returns_dict(self):
        result = render_regime_scorecard_tab()
        assert isinstance(result, dict)

    def test_render_scorecard_weights_sum(self):
        result = render_regime_scorecard_tab()
        assert result.get("weights_sum") == 100

    def test_render_report_returns_dict(self):
        result = render_regime_report_tab()
        assert isinstance(result, dict)

    def test_render_report_14_sections(self):
        result = render_regime_report_tab()
        assert result.get("section_count") == 14

    def test_render_health_gate_returns_dict(self):
        result = render_regime_health_gate_tab()
        assert isinstance(result, dict)

    def test_render_health_gate_paper_only(self):
        result = render_regime_health_gate_tab()
        assert result.get("paper_only") is True
