"""
tests/test_paper_attribution_report_v167.py
Tests for paper attribution report engine v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import json
import pytest
from paper_trading.performance_attribution.attribution_report_v167 import (
    AttributionReportEngine,
    REPORT_SECTIONS,
)


def _run_data(**extra):
    base = {
        "run_id": "rpt_test",
        "portfolio_id": "P_RPT",
        "period_start": "2024-01-01",
        "period_end": "2024-01-31",
        "status": "COMPLETE",
        "paper_only": True,
        "research_only": True,
        "portfolio_attribution": {
            "active_return": 0.03,
            "gross_return": 0.04,
            "net_return": 0.035,
            "total_cost_pct": 0.005,
            "reconciled": True,
            "confidence": "HIGH",
        },
        "quality_score": {
            "total_score": 85.0,
            "grade": "B",
        },
        "symbol_attribution": {
            "AAPL": {"return": 0.08},
            "MSFT": {"return": 0.05},
            "TSLA": {"return": -0.03},
        },
    }
    base.update(extra)
    return base


class TestReportSections:
    def test_exactly_31_sections(self):
        assert len(REPORT_SECTIONS) == 31

    def test_attribution_summary_first(self):
        assert REPORT_SECTIONS[0] == "attribution_summary"

    def test_not_for_real_trading_last(self):
        assert REPORT_SECTIONS[-1] == "not_for_real_trading"

    def test_disclaimer_second_to_last(self):
        assert REPORT_SECTIONS[-2] == "disclaimer"

    def test_reconciliation_status_in_sections(self):
        assert "reconciliation_status" in REPORT_SECTIONS

    def test_quality_scorecard_in_sections(self):
        assert "quality_scorecard" in REPORT_SECTIONS

    def test_all_sections_unique(self):
        assert len(REPORT_SECTIONS) == len(set(REPORT_SECTIONS))


class TestBuildSection:
    def setup_method(self):
        self.engine = AttributionReportEngine(_run_data())

    def test_unknown_section_returns_error(self):
        r = self.engine.build_section("nonexistent_section")
        assert "error" in r

    def test_attribution_summary_has_active_return(self):
        r = self.engine.build_section("attribution_summary")
        assert r["active_return"] == 0.03

    def test_attribution_summary_paper_only(self):
        r = self.engine.build_section("attribution_summary")
        assert r["paper_only"] is True

    def test_gross_vs_net_has_gross_return(self):
        r = self.engine.build_section("gross_vs_net_return")
        assert r["gross_return"] == 0.04

    def test_not_for_real_trading_has_warning(self):
        r = self.engine.build_section("not_for_real_trading")
        assert "NOT FOR REAL TRADING" in r.get("warning", "")

    def test_disclaimer_has_text(self):
        r = self.engine.build_section("disclaimer")
        assert len(r.get("text", "")) > 20

    def test_top_bottom_contributors_has_both(self):
        r = self.engine.build_section("top_bottom_contributors")
        assert "top_contributors" in r
        assert "bottom_contributors" in r

    def test_empty_run_returns_empty_status(self):
        empty_engine = AttributionReportEngine({})
        r = empty_engine.build_section("attribution_summary")
        assert r.get("status") == "EMPTY"


class TestBuildAllSections:
    def setup_method(self):
        self.engine = AttributionReportEngine(_run_data())

    def test_returns_31_sections(self):
        report = self.engine.build_all_sections()
        assert len(report["sections"]) == 31

    def test_section_count_correct(self):
        report = self.engine.build_all_sections()
        assert report["section_count"] == 31

    def test_header_present(self):
        report = self.engine.build_all_sections()
        assert "header" in report

    def test_paper_only_in_output(self):
        report = self.engine.build_all_sections()
        assert report["paper_only"] is True

    def test_all_section_names_present(self):
        report = self.engine.build_all_sections()
        for s in REPORT_SECTIONS:
            assert s in report["sections"], f"Missing section: {s}"


class TestMarkdownOutput:
    def setup_method(self):
        self.engine = AttributionReportEngine(_run_data())

    def test_returns_string(self):
        md = self.engine.to_markdown()
        assert isinstance(md, str)

    def test_has_title(self):
        md = self.engine.to_markdown()
        assert "Paper Performance Attribution Report" in md

    def test_has_disclaimer(self):
        md = self.engine.to_markdown()
        assert "RESEARCH ONLY" in md

    def test_has_not_for_real_trading(self):
        md = self.engine.to_markdown()
        assert "NOT FOR REAL TRADING" in md

    def test_has_31_numbered_sections(self):
        md = self.engine.to_markdown()
        # Check that all 31 section headers appear
        for i in range(1, 32):
            assert f"## {i}." in md, f"Missing section header ## {i}."

    def test_has_run_id(self):
        md = self.engine.to_markdown()
        assert "rpt_test" in md

    def test_has_portfolio_id(self):
        md = self.engine.to_markdown()
        assert "P_RPT" in md


class TestJsonOutput:
    def setup_method(self):
        self.engine = AttributionReportEngine(_run_data())

    def test_returns_valid_json(self):
        j = self.engine.to_json()
        data = json.loads(j)  # should not raise
        assert isinstance(data, dict)

    def test_has_sections(self):
        j = self.engine.to_json()
        data = json.loads(j)
        assert "sections" in data

    def test_paper_only_in_json(self):
        j = self.engine.to_json()
        data = json.loads(j)
        assert data.get("paper_only") is True

    def test_all_31_sections_in_json(self):
        j = self.engine.to_json()
        data = json.loads(j)
        assert len(data["sections"]) == 31


class TestCsvOutput:
    def setup_method(self):
        self.engine = AttributionReportEngine(_run_data())

    def test_returns_string(self):
        csv = self.engine.to_csv()
        assert isinstance(csv, str)

    def test_has_header_row(self):
        csv = self.engine.to_csv()
        assert "run_id" in csv

    def test_has_active_return_column(self):
        csv = self.engine.to_csv()
        assert "active_return" in csv

    def test_has_data_row(self):
        csv = self.engine.to_csv()
        lines = csv.strip().split("\n")
        assert len(lines) == 2  # header + data

    def test_paper_only_in_csv(self):
        csv = self.engine.to_csv()
        assert "True" in csv


class TestConsoleOutput:
    def setup_method(self):
        self.engine = AttributionReportEngine(_run_data())

    def test_returns_string(self):
        console = self.engine.to_console()
        assert isinstance(console, str)

    def test_has_title(self):
        console = self.engine.to_console()
        assert "PAPER ATTRIBUTION REPORT" in console

    def test_has_not_for_real_trading(self):
        console = self.engine.to_console()
        assert "NOT FOR REAL TRADING" in console

    def test_has_active_return(self):
        console = self.engine.to_console()
        assert "Active Return" in console or "active_return" in console.lower()


class TestGuiModelOutput:
    def setup_method(self):
        self.engine = AttributionReportEngine(_run_data())

    def test_returns_dict(self):
        gui = self.engine.to_gui_model()
        assert isinstance(gui, dict)

    def test_tab_count_31(self):
        gui = self.engine.to_gui_model()
        assert gui["tab_count"] == 31

    def test_tabs_list_length_31(self):
        gui = self.engine.to_gui_model()
        assert len(gui["tabs"]) == 31

    def test_each_tab_has_index(self):
        gui = self.engine.to_gui_model()
        for i, tab in enumerate(gui["tabs"]):
            assert tab["tab_index"] == i + 1

    def test_each_tab_paper_only(self):
        gui = self.engine.to_gui_model()
        for tab in gui["tabs"]:
            assert tab["paper_only"] is True

    def test_paper_only_in_gui_model(self):
        gui = self.engine.to_gui_model()
        assert gui["paper_only"] is True

    def test_not_for_real_trading_in_gui_model(self):
        gui = self.engine.to_gui_model()
        assert gui["not_for_real_trading"] is True

    def test_report_type_correct(self):
        gui = self.engine.to_gui_model()
        assert gui["report_type"] == "paper_attribution"
