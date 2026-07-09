"""
tests/test_trade_journal_report_v175.py
Tests for Trade Journal report v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
import json
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection
from paper_trading.small_capital_strategy.trade_journal_entry_v175 import (
    create_journal_entry, close_journal_entry,
)
from paper_trading.small_capital_strategy.trade_journal_dashboard_v175 import build_dashboard
from paper_trading.small_capital_strategy.trade_journal_models_v175 import TradeJournalReport
from paper_trading.small_capital_strategy.trade_journal_report_v175 import (
    build_report, get_report_sections, render_json, render_markdown,
    REPORT_SECTION_NAMES,
)


def _sample_dashboard():
    e1 = close_journal_entry(
        create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                             580.0, 50000.0, 552.0, 0.05), "2026-01-20", 638.0)
    return build_dashboard([e1])


class TestReportSectionNames:
    def test_section_count_ge_13(self):
        assert len(REPORT_SECTION_NAMES) >= 13

    def test_contains_summary_section(self):
        assert "trade_journal_summary" in REPORT_SECTION_NAMES

    def test_contains_safety_section(self):
        assert "safety_disclaimer" in REPORT_SECTION_NAMES

    def test_contains_not_investment_advice(self):
        assert "not_investment_advice" in REPORT_SECTION_NAMES

    def test_contains_scorecard_summary(self):
        assert "scorecard_summary" in REPORT_SECTION_NAMES


class TestGetReportSections:
    def test_returns_list(self):
        assert isinstance(get_report_sections(), list)

    def test_ge_13_sections(self):
        assert len(get_report_sections()) >= 13

    def test_matches_report_section_names(self):
        assert get_report_sections() == REPORT_SECTION_NAMES


class TestBuildReport:
    def test_returns_trade_journal_report(self):
        dash = _sample_dashboard()
        assert isinstance(build_report(dash), TradeJournalReport)

    def test_paper_only_true(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        assert r.paper_only is True

    def test_no_broker_true(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        assert r.no_broker is True

    def test_not_investment_advice_true(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        assert r.not_investment_advice is True

    def test_format_json_default(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        assert r.report_format == "JSON"

    def test_sections_not_empty(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        assert len(r.sections) > 0

    def test_safety_section_has_paper_only(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        assert r.sections["safety_disclaimer"]["paper_only"] is True

    def test_schema_version(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        assert r.schema_version == "175"


class TestRenderJSON:
    def test_returns_str(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        assert isinstance(render_json(r), str)

    def test_valid_json(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        parsed = json.loads(render_json(r))
        assert isinstance(parsed, dict)

    def test_json_has_paper_only(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        parsed = json.loads(render_json(r))
        assert parsed["paper_only"] is True

    def test_json_has_schema_version(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        parsed = json.loads(render_json(r))
        assert "schema_version" in parsed


class TestRenderMarkdown:
    def test_returns_str(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        assert isinstance(render_markdown(r), str)

    def test_contains_journal_title(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        md = render_markdown(r)
        assert "Trade Journal" in md

    def test_contains_disclaimer(self):
        dash = _sample_dashboard()
        r = build_report(dash)
        md = render_markdown(r)
        assert "Research Only" in md or "Not Investment Advice" in md
