"""
tests/test_risk_dashboard_report_v174.py
Tests for risk dashboard report v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
import json
from paper_trading.small_capital_strategy.risk_dashboard_report_v174 import (
    get_section_names, REPORT_SECTION_NAMES, build_report,
    render_markdown, render_json, render_csv, render_console_summary,
)
from paper_trading.small_capital_strategy.small_capital_risk_adapter_v174 import (
    build_risk_dashboard, get_default_pass_input,
)
from paper_trading.small_capital_strategy.risk_dashboard_scorecard_v174 import compute_scorecard


def _setup():
    dashboard = build_risk_dashboard(get_default_pass_input())
    scorecard = compute_scorecard(dashboard)
    report = build_report(dashboard, scorecard)
    return dashboard, scorecard, report


class TestSectionNames:
    def test_17_sections(self):
        assert len(REPORT_SECTION_NAMES) == 17

    def test_get_section_names_17(self):
        assert len(get_section_names()) == 17

    def test_has_summary_section(self):
        assert "small_account_risk_summary" in REPORT_SECTION_NAMES

    def test_has_scorecard_section(self):
        assert "scorecard" in REPORT_SECTION_NAMES

    def test_has_not_investment_advice(self):
        assert "not_investment_advice" in REPORT_SECTION_NAMES

    def test_has_safety(self):
        assert "safety" in REPORT_SECTION_NAMES

    def test_section_names_list_type(self):
        assert isinstance(get_section_names(), list)


class TestBuildReport:
    def setup_method(self):
        _, _, self.report = _setup()

    def test_paper_only(self):
        assert self.report.paper_only is True

    def test_no_real_orders(self):
        assert self.report.no_real_orders is True

    def test_not_investment_advice(self):
        assert self.report.not_investment_advice is True

    def test_sections_dict(self):
        assert isinstance(self.report.sections, dict)

    def test_sections_not_empty(self):
        assert len(self.report.sections) > 0


class TestMarkdownRender:
    def test_markdown_returns_string(self):
        _, _, report = _setup()
        assert isinstance(render_markdown(report), str)

    def test_markdown_not_empty(self):
        _, _, report = _setup()
        assert len(render_markdown(report)) > 0

    def test_markdown_contains_research_only(self):
        _, _, report = _setup()
        assert "Research Only" in render_markdown(report)

    def test_markdown_contains_no_real_orders(self):
        _, _, report = _setup()
        assert "No Real Orders" in render_markdown(report)


class TestJsonRender:
    def test_json_returns_string(self):
        _, _, report = _setup()
        assert isinstance(render_json(report), str)

    def test_json_parseable(self):
        _, _, report = _setup()
        parsed = json.loads(render_json(report))
        assert isinstance(parsed, dict)

    def test_json_has_sections(self):
        _, _, report = _setup()
        parsed = json.loads(render_json(report))
        assert "sections" in parsed

    def test_json_paper_only(self):
        _, _, report = _setup()
        parsed = json.loads(render_json(report))
        assert parsed["paper_only"] is True


class TestCsvRender:
    def test_csv_returns_string(self):
        _, _, report = _setup()
        assert isinstance(render_csv(report), str)

    def test_csv_not_empty(self):
        _, _, report = _setup()
        assert len(render_csv(report)) > 0

    def test_csv_has_header(self):
        _, _, report = _setup()
        assert "section" in render_csv(report)


class TestConsoleSummary:
    def test_console_returns_string(self):
        _, _, report = _setup()
        assert isinstance(render_console_summary(report), str)

    def test_console_has_version(self):
        _, _, report = _setup()
        assert "1.7.4" in render_console_summary(report)

    def test_console_has_research_only(self):
        _, _, report = _setup()
        assert "Research Only" in render_console_summary(report)
