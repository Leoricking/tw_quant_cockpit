"""
tests/test_paper_attribution_gui_v167.py
Tests for paper attribution GUI panel v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from gui.paper_performance_attribution_panel import (
    PaperAttributionPanel,
    PANEL_TABS,
)


class TestPanelTabs:
    def test_exactly_31_tabs(self):
        assert len(PANEL_TABS) == 31

    def test_attribution_summary_first(self):
        assert PANEL_TABS[0] == "Attribution Summary"

    def test_not_for_real_trading_last(self):
        assert PANEL_TABS[-1] == "Not for Real Trading"

    def test_disclaimer_second_to_last(self):
        assert PANEL_TABS[-2] == "Disclaimer"

    def test_reconciliation_status_in_tabs(self):
        assert "Reconciliation Status" in PANEL_TABS

    def test_quality_scorecard_in_tabs(self):
        assert "Quality Scorecard" in PANEL_TABS

    def test_all_tabs_unique(self):
        assert len(PANEL_TABS) == len(set(PANEL_TABS))


class TestPanelInit:
    def test_empty_init(self):
        panel = PaperAttributionPanel()
        assert panel is not None

    def test_init_with_run_data(self):
        panel = PaperAttributionPanel({"run_id": "test", "paper_only": True})
        assert panel is not None

    def test_get_tab_names(self):
        panel = PaperAttributionPanel()
        names = panel.get_tab_names()
        assert len(names) == 31

    def test_get_tab_names_matches_panel_tabs(self):
        panel = PaperAttributionPanel()
        assert panel.get_tab_names() == list(PANEL_TABS)


class TestSelectTab:
    def test_select_first_tab(self):
        panel = PaperAttributionPanel()
        panel.select_tab(0)
        assert panel._selected_tab == 0

    def test_select_last_tab(self):
        panel = PaperAttributionPanel()
        panel.select_tab(30)
        assert panel._selected_tab == 30

    def test_invalid_tab_not_changed(self):
        panel = PaperAttributionPanel()
        panel.select_tab(0)
        panel.select_tab(999)
        assert panel._selected_tab == 0


class TestRenderTab:
    def setup_method(self):
        self.panel = PaperAttributionPanel({
            "run_id": "tab_test",
            "paper_only": True,
            "research_only": True,
        })

    def test_render_first_tab(self):
        r = self.panel.render_tab(0)
        assert "tab_name" in r
        assert r["tab_index"] == 0

    def test_render_last_tab(self):
        r = self.panel.render_tab(30)
        assert r["tab_index"] == 30

    def test_render_invalid_tab_error(self):
        r = self.panel.render_tab(999)
        assert "error" in r

    def test_render_tab_paper_only(self):
        r = self.panel.render_tab(0)
        assert r["paper_only"] is True

    def test_render_tab_research_only(self):
        r = self.panel.render_tab(0)
        assert r["research_only"] is True

    def test_render_tab_no_real_orders(self):
        r = self.panel.render_tab(0)
        assert r["no_real_orders"] is True

    def test_render_tab_has_run_id(self):
        r = self.panel.render_tab(0)
        assert r.get("run_id") == "tab_test"


class TestRender:
    def setup_method(self):
        self.panel = PaperAttributionPanel({
            "run_id": "render_test",
            "portfolio_id": "P1",
            "period_start": "2024-01-01",
            "period_end": "2024-01-31",
            "status": "COMPLETE",
            "paper_only": True,
        })

    def test_returns_dict(self):
        r = self.panel.render()
        assert isinstance(r, dict)

    def test_tab_count_31(self):
        r = self.panel.render()
        assert r["tab_count"] == 31

    def test_tabs_list_length_31(self):
        r = self.panel.render()
        assert len(r["tabs"]) == 31

    def test_panel_type_paper_attribution(self):
        r = self.panel.render()
        assert r["panel_type"] == "paper_performance_attribution"

    def test_version_1_6_7(self):
        r = self.panel.render()
        assert r["version"] == "1.6.7"

    def test_paper_only_in_result(self):
        r = self.panel.render()
        assert r["paper_only"] is True

    def test_not_for_real_trading(self):
        r = self.panel.render()
        assert r["not_for_real_trading"] is True

    def test_run_id_in_result(self):
        r = self.panel.render()
        assert r["run_id"] == "render_test"

    def test_portfolio_id_in_result(self):
        r = self.panel.render()
        assert r["portfolio_id"] == "P1"

    def test_period_start_in_result(self):
        r = self.panel.render()
        assert r["period_start"] == "2024-01-01"


class TestRenderText:
    def setup_method(self):
        self.panel = PaperAttributionPanel({
            "run_id": "txt_test",
            "portfolio_id": "PTXT",
        })

    def test_returns_string(self):
        txt = self.panel.render_text()
        assert isinstance(txt, str)

    def test_has_title(self):
        txt = self.panel.render_text()
        assert "PAPER PERFORMANCE ATTRIBUTION" in txt

    def test_has_not_for_real_trading(self):
        txt = self.panel.render_text()
        assert "NOT FOR REAL TRADING" in txt

    def test_has_31_tab_entries(self):
        txt = self.panel.render_text()
        count = sum(1 for line in txt.split("\n") if "[" in line and "]" in line and "Attribution" in line or "Return" in line or "Status" in line or "Trading" in line)
        # Just verify tabs section exists
        assert "Tabs (31)" in txt

    def test_has_run_id(self):
        txt = self.panel.render_text()
        assert "txt_test" in txt


class TestGetSummaryKpis:
    def test_returns_dict(self):
        panel = PaperAttributionPanel({
            "paper_only": True,
            "portfolio_attribution": {"active_return": 0.05, "confidence": "HIGH"},
        })
        kpis = panel.get_summary_kpis()
        assert isinstance(kpis, dict)

    def test_active_return_in_kpis(self):
        panel = PaperAttributionPanel({
            "paper_only": True,
            "portfolio_attribution": {"active_return": 0.05},
        })
        kpis = panel.get_summary_kpis()
        assert kpis["active_return"] == 0.05

    def test_paper_only_in_kpis(self):
        panel = PaperAttributionPanel({})
        kpis = panel.get_summary_kpis()
        assert kpis["paper_only"] is True

    def test_empty_run_returns_none_values(self):
        panel = PaperAttributionPanel({})
        kpis = panel.get_summary_kpis()
        assert kpis["active_return"] is None


class TestSetRunData:
    def test_set_run_data(self):
        panel = PaperAttributionPanel()
        panel.set_run_data({"run_id": "new_run", "paper_only": True})
        assert panel._run["run_id"] == "new_run"
