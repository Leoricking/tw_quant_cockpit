"""
tests/test_stable_rollup_models_v179.py
Tests for stable_rollup_models_v179 dataclass models.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_models_v179 import (
    StableRollupVersionEntry,
    StableRollupCompatResult,
    StableRollupAuditResult,
    StableRollupHealthSummary,
    StableRollupReport,
    get_all_model_names,
)


# ── StableRollupVersionEntry ────────────────────────────────────────────────

def test_version_entry_default_paper_only():
    entry = StableRollupVersionEntry()
    assert entry.paper_only is True


def test_version_entry_default_research_only():
    entry = StableRollupVersionEntry()
    assert entry.research_only is True


def test_version_entry_default_no_real_orders():
    entry = StableRollupVersionEntry()
    assert entry.no_real_orders is True


def test_version_entry_default_not_investment_advice():
    entry = StableRollupVersionEntry()
    assert entry.not_investment_advice is True


def test_version_entry_set_version():
    entry = StableRollupVersionEntry(version="1.7.9", release_name="Test")
    assert entry.version == "1.7.9"
    assert entry.release_name == "Test"


def test_version_entry_default_is_importable_false():
    entry = StableRollupVersionEntry()
    assert entry.is_importable is False


def test_version_entry_health_pass_default_false():
    entry = StableRollupVersionEntry()
    assert entry.health_pass is False


# ── StableRollupCompatResult ────────────────────────────────────────────────

def test_compat_result_default_paper_only():
    result = StableRollupCompatResult()
    assert result.paper_only is True


def test_compat_result_default_no_real_orders():
    result = StableRollupCompatResult()
    assert result.no_real_orders is True


def test_compat_result_default_not_investment_advice():
    result = StableRollupCompatResult()
    assert result.not_investment_advice is True


def test_compat_result_default_importable_false():
    result = StableRollupCompatResult()
    assert result.importable is False


def test_compat_result_default_version_match_false():
    result = StableRollupCompatResult()
    assert result.version_match is False


def test_compat_result_set_version():
    result = StableRollupCompatResult(version="v1.7.0", module="paper_trading.small_capital_strategy.version_v170")
    assert result.version == "v1.7.0"


def test_compat_result_error_default_none():
    result = StableRollupCompatResult()
    assert result.error is None


# ── StableRollupAuditResult ─────────────────────────────────────────────────

def test_audit_result_default_paper_only():
    result = StableRollupAuditResult()
    assert result.paper_only is True


def test_audit_result_default_no_broker():
    result = StableRollupAuditResult()
    assert result.no_broker is True


def test_audit_result_default_all_passed_false():
    result = StableRollupAuditResult()
    assert result.all_passed is False


def test_audit_result_default_status_fail():
    result = StableRollupAuditResult()
    assert result.status == "FAIL"


def test_audit_result_schema_version():
    result = StableRollupAuditResult()
    assert result.schema_version == "179"


def test_audit_result_policy_version():
    result = StableRollupAuditResult()
    assert "1.7.9" in result.policy_version


def test_audit_result_checks_default_empty():
    result = StableRollupAuditResult()
    assert result.checks == []


# ── StableRollupHealthSummary ───────────────────────────────────────────────

def test_health_summary_default_paper_only():
    summary = StableRollupHealthSummary()
    assert summary.paper_only is True


def test_health_summary_default_not_investment_advice():
    summary = StableRollupHealthSummary()
    assert summary.not_investment_advice is True


def test_health_summary_default_demo_only():
    summary = StableRollupHealthSummary()
    assert summary.demo_only is True


def test_health_summary_default_not_for_production():
    summary = StableRollupHealthSummary()
    assert summary.not_for_production is True


def test_health_summary_default_status_fail():
    summary = StableRollupHealthSummary()
    assert summary.status == "FAIL"


def test_health_summary_set_status_pass():
    summary = StableRollupHealthSummary(status="PASS", all_passed=True)
    assert summary.status == "PASS"
    assert summary.all_passed is True


# ── StableRollupReport ──────────────────────────────────────────────────────

def test_report_default_version():
    report = StableRollupReport()
    assert report.version == "1.7.9"


def test_report_default_release_name():
    report = StableRollupReport()
    assert report.release_name == "Small Capital Strategy Stable Rollup"


def test_report_default_paper_only():
    report = StableRollupReport()
    assert report.paper_only is True


def test_report_default_no_real_orders():
    report = StableRollupReport()
    assert report.no_real_orders is True


def test_report_default_demo_only():
    report = StableRollupReport()
    assert report.demo_only is True


def test_report_schema_version():
    report = StableRollupReport()
    assert report.schema_version == "179"


def test_report_sections_default_empty():
    report = StableRollupReport()
    assert report.sections == []


# ── get_all_model_names ─────────────────────────────────────────────────────

def test_get_all_model_names_returns_list():
    names = get_all_model_names()
    assert isinstance(names, list)


def test_get_all_model_names_count_5():
    names = get_all_model_names()
    assert len(names) == 5


def test_get_all_model_names_contains_version_entry():
    names = get_all_model_names()
    assert "StableRollupVersionEntry" in names


def test_get_all_model_names_contains_report():
    names = get_all_model_names()
    assert "StableRollupReport" in names


def test_get_all_model_names_contains_health_summary():
    names = get_all_model_names()
    assert "StableRollupHealthSummary" in names
