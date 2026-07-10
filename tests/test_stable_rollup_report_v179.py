"""
tests/test_stable_rollup_report_v179.py
Tests for stable_rollup_report_v179 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_report_v179 import (
    build_report,
    get_report_sections,
)


def test_get_report_sections_returns_list():
    sections = get_report_sections()
    assert isinstance(sections, list)


def test_get_report_sections_count_11():
    sections = get_report_sections()
    assert len(sections) == 11


def test_get_report_sections_contains_executive_summary():
    sections = get_report_sections()
    assert "executive_summary" in sections


def test_get_report_sections_contains_version_info():
    sections = get_report_sections()
    assert "version_info" in sections


def test_get_report_sections_contains_compatibility():
    sections = get_report_sections()
    assert "compatibility" in sections


def test_get_report_sections_contains_safety_audit():
    sections = get_report_sections()
    assert "safety_audit" in sections


def test_get_report_sections_contains_safety_disclaimer():
    sections = get_report_sections()
    assert "safety_disclaimer" in sections


def test_build_report_returns_dict():
    report = build_report()
    assert isinstance(report, dict)


def test_build_report_version_179():
    report = build_report()
    assert report["version"] == "1.7.9"


def test_build_report_release_name():
    report = build_report()
    assert report["release_name"] == "Small Capital Strategy Stable Rollup"


def test_build_report_paper_only():
    report = build_report()
    assert report["paper_only"] is True


def test_build_report_research_only():
    report = build_report()
    assert report["research_only"] is True


def test_build_report_no_real_orders():
    report = build_report()
    assert report["no_real_orders"] is True


def test_build_report_no_broker():
    report = build_report()
    assert report["no_broker"] is True


def test_build_report_not_investment_advice():
    report = build_report()
    assert report["not_investment_advice"] is True


def test_build_report_demo_only():
    report = build_report()
    assert report["demo_only"] is True


def test_build_report_section_count_11():
    report = build_report()
    assert report["section_count"] == 11


def test_build_report_all_audits_pass():
    report = build_report()
    assert report["all_audits_pass"] is True


def test_build_report_schema_version():
    report = build_report()
    assert report["schema_version"] == "179"


def test_build_report_sections_is_list():
    report = build_report()
    assert isinstance(report["sections"], list)
