"""
tests/test_operational_integration_gui_panel_v168.py — GUI Panel tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from gui.operational_integration_panel import (
    OperationalIntegrationPanel, PANEL_TABS, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)


class TestGUIPanelSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestGUIPanelCore:
    def setup_method(self):
        self.panel = OperationalIntegrationPanel()

    def test_panel_tabs_count_22(self):
        assert len(PANEL_TABS) == 22

    def test_get_tab_names_returns_list(self):
        tabs = self.panel.get_tab_names()
        assert isinstance(tabs, list)

    def test_get_tab_names_count_22(self):
        tabs = self.panel.get_tab_names()
        assert len(tabs) == 22

    def test_get_tab_names_includes_overview(self):
        tabs = self.panel.get_tab_names()
        assert "Overview" in tabs

    def test_get_tab_names_includes_safety(self):
        tabs = self.panel.get_tab_names()
        assert "Safety" in tabs

    def test_get_tab_names_includes_pipeline(self):
        tabs = self.panel.get_tab_names()
        assert "Pipeline" in tabs

    def test_get_tab_names_includes_scorecard(self):
        tabs = self.panel.get_tab_names()
        assert "Scorecard" in tabs

    def test_render_tab_returns_dict(self):
        result = self.panel.render_tab(0)
        assert isinstance(result, dict)

    def test_render_tab_paper_only(self):
        result = self.panel.render_tab(0)
        assert result["paper_only"] is True

    def test_render_tab_has_tab_name(self):
        result = self.panel.render_tab(0)
        assert "tab_name" in result
        assert result["tab_name"] == "Overview"

    def test_render_tab_has_tab_index(self):
        result = self.panel.render_tab(0)
        assert result["tab_index"] == 0

    def test_render_tab_invalid_index_error(self):
        result = self.panel.render_tab(100)
        assert "error" in result

    def test_render_tab_invalid_negative_error(self):
        result = self.panel.render_tab(-1)
        assert "error" in result

    def test_render_all_tabs_count(self):
        all_tabs = self.panel.render_all_tabs()
        assert len(all_tabs) == 22

    def test_render_text_returns_string(self):
        text = self.panel.render_text()
        assert isinstance(text, str)
        assert len(text) > 0

    def test_render_text_has_version(self):
        text = self.panel.render_text()
        assert "1.6.8" in text

    def test_render_text_has_paper_only_warning(self):
        text = self.panel.render_text()
        assert "Paper" in text or "paper" in text

    def test_render_gui_model_returns_dict(self):
        model = self.panel.render_gui_model()
        assert isinstance(model, dict)

    def test_render_gui_model_paper_only(self):
        model = self.panel.render_gui_model()
        assert model.get("paper_only") is True

    def test_render_gui_model_tab_count(self):
        model = self.panel.render_gui_model()
        assert model.get("tab_count") == 22

    def test_render_safety_returns_dict(self):
        safety = self.panel.render_safety()
        assert isinstance(safety, dict)

    def test_render_safety_paper_only(self):
        safety = self.panel.render_safety()
        assert safety.get("paper_only") is True

    def test_render_safety_no_real_orders(self):
        safety = self.panel.render_safety()
        assert safety.get("no_real_orders") is True

    def test_render_tab_each_valid_index(self):
        for i in range(22):
            result = self.panel.render_tab(i)
            assert result["tab_index"] == i
            assert result["tab_name"] == PANEL_TABS[i]
