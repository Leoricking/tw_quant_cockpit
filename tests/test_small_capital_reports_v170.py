"""tests/test_small_capital_reports_v170.py — strategy report tests for v1.7.0."""
import json
import pytest
from paper_trading.small_capital_strategy.small_capital_scorecard_v170 import (
    compute_scorecard, SCORE_WEIGHTS,
)
from paper_trading.small_capital_strategy.strategy_report_v170 import (
    build_report, to_markdown, to_json, to_csv, to_console_summary, get_section_names,
)

TEMPLATE_ID = "small_capital_300k_v170"

_SCORES = {k: 0.8 for k in SCORE_WEIGHTS}


def _make_scorecard():
    return compute_scorecard(TEMPLATE_ID, _SCORES)


def test_build_report_returns_report():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    assert report is not None


def test_build_report_template_id():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    assert report.template_id == TEMPLATE_ID


def test_build_report_paper_only():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    assert report.paper_only is True


def test_build_report_research_only():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    assert report.research_only is True


def test_build_report_no_real_orders():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    assert report.no_real_orders is True


def test_build_report_not_investment_advice():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    assert report.not_investment_advice is True


def test_build_report_disclaimer_in_sections():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    assert "not_investment_advice" in report.sections


def test_to_markdown_returns_string():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    md = to_markdown(report)
    assert isinstance(md, str)


def test_to_markdown_contains_disclaimer():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    md = to_markdown(report)
    assert "Not Investment Advice" in md


def test_to_markdown_contains_version():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    md = to_markdown(report)
    assert "1.7.0" in md


def test_to_markdown_contains_scorecard():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    md = to_markdown(report)
    assert "Scorecard" in md


def test_to_json_returns_string():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    js = to_json(report)
    assert isinstance(js, str)


def test_to_json_valid_json():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    js = to_json(report)
    parsed = json.loads(js)
    assert isinstance(parsed, dict)


def test_to_json_has_template_id():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    parsed = json.loads(to_json(report))
    assert parsed["template_id"] == TEMPLATE_ID


def test_to_csv_returns_string():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    csv = to_csv(report)
    assert isinstance(csv, str)


def test_to_csv_has_header():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    csv = to_csv(report)
    assert csv.startswith("field,value")


def test_to_csv_has_template_id():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    csv = to_csv(report)
    assert "template_id" in csv


def test_to_csv_has_paper_only():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    csv = to_csv(report)
    assert "paper_only" in csv


def test_to_console_summary_returns_string():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    summary = to_console_summary(report)
    assert isinstance(summary, str)


def test_to_console_summary_has_version():
    sc = _make_scorecard()
    report = build_report(TEMPLATE_ID, sc)
    summary = to_console_summary(report)
    assert "1.7.0" in summary


def test_get_section_names_returns_list():
    sections = get_section_names()
    assert isinstance(sections, list)


def test_get_section_names_15_sections():
    sections = get_section_names()
    assert len(sections) == 15


def test_section_names_has_scorecard():
    assert "scorecard" in get_section_names()


def test_section_names_has_not_investment_advice():
    assert "not_investment_advice" in get_section_names()


def test_build_report_with_sections():
    sc = _make_scorecard()
    sections = {"capital_profile": {"capital_twd": 300000.0}}
    report = build_report(TEMPLATE_ID, sc, sections=sections)
    assert report.sections["capital_profile"]["capital_twd"] == 300000.0
