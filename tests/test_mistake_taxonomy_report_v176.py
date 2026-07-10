"""tests/test_mistake_taxonomy_report_v176.py — v1.7.6 report tests."""
import json
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import MistakeCategory
from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import classify_event
from paper_trading.small_capital_strategy.mistake_taxonomy_dashboard_v176 import build_dashboard
from paper_trading.small_capital_strategy.mistake_taxonomy_report_v176 import (
    build_report_dict, render_json, render_markdown, get_report_sections, REPORT_SECTION_NAMES,
)


def _dash():
    ev = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0)
    return build_dashboard([ev], total_trades=1)


class TestReportSections:
    def test_section_names_ge_13(self):
        assert len(REPORT_SECTION_NAMES) >= 13

    def test_get_report_sections_ge_13(self):
        assert len(get_report_sections()) >= 13

    def test_get_report_sections_list(self):
        assert isinstance(get_report_sections(), list)

    def test_summary_section_exists(self):
        assert "summary" in REPORT_SECTION_NAMES

    def test_behavior_score_section_exists(self):
        assert "behavior_score" in REPORT_SECTION_NAMES

    def test_disclaimer_section_exists(self):
        assert "disclaimer" in REPORT_SECTION_NAMES


class TestBuildReportDict:
    def test_paper_only_in_report(self):
        rpt = build_report_dict(_dash())
        assert rpt["paper_only"] is True

    def test_not_investment_advice_in_report(self):
        rpt = build_report_dict(_dash())
        assert rpt["not_investment_advice"] is True

    def test_sections_key_exists(self):
        rpt = build_report_dict(_dash())
        assert "sections" in rpt

    def test_sections_is_dict(self):
        rpt = build_report_dict(_dash())
        assert isinstance(rpt["sections"], dict)

    def test_behavior_score_in_sections(self):
        rpt = build_report_dict(_dash())
        assert "behavior_score" in rpt["sections"]


class TestRenderJson:
    def test_render_json_is_str(self):
        rpt = build_report_dict(_dash())
        assert isinstance(render_json(rpt), str)

    def test_render_json_parseable(self):
        rpt = build_report_dict(_dash())
        parsed = json.loads(render_json(rpt))
        assert isinstance(parsed, dict)


class TestRenderMarkdown:
    def test_render_markdown_is_str(self):
        rpt = build_report_dict(_dash())
        assert isinstance(render_markdown(rpt), str)

    def test_render_markdown_contains_title(self):
        rpt = build_report_dict(_dash())
        md = render_markdown(rpt)
        assert "Mistake Taxonomy" in md

    def test_render_markdown_contains_disclaimer(self):
        rpt = build_report_dict(_dash())
        md = render_markdown(rpt)
        assert "Research Only" in md or "Paper Only" in md
