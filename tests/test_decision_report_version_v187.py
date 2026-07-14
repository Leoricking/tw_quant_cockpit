"""
tests/test_decision_report_version_v187.py
Tests for decision_report_version_v187 — v1.8.7 Decision Report Export & Evidence Pack.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_report_version_v187 import (
    VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
    INCLUDED_RELEASES, REPORT_TYPES, EXPORT_FORMATS, FINAL_REPORT_GRADES,
    MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH_CHECKS, KNOWN_RELEASE_NAMES,
    get_version_info, verify_version, is_known_release, check_minimum_version,
    get_report_types, get_export_formats, get_final_report_grades,
)


def test_version_is_187():
    assert VERSION == "1.8.7"


def test_release_name():
    assert RELEASE_NAME == "Decision Report Export & Evidence Pack"


def test_schema_version():
    assert SCHEMA_VERSION == "187"


def test_base_release_contains_186():
    assert "1.8.6" in BASE_RELEASE


def test_policy_version_contains_187():
    assert "1.8.7" in POLICY_VERSION


def test_verify_version_returns_true():
    assert verify_version() is True


def test_get_version_info_version():
    info = get_version_info()
    assert info["version"] == "1.8.7"


def test_get_version_info_schema_version():
    info = get_version_info()
    assert info["schema_version"] == "187"


def test_get_version_info_paper_only():
    info = get_version_info()
    assert info["paper_only"] is True


def test_get_version_info_no_real_orders():
    info = get_version_info()
    assert info["no_real_orders"] is True


def test_get_version_info_not_investment_advice():
    info = get_version_info()
    assert info["not_investment_advice"] is True


def test_get_version_info_production_trading_blocked():
    info = get_version_info()
    assert info["production_trading_blocked"] is True


def test_get_version_info_report_only():
    info = get_version_info()
    assert info["report_only"] is True


def test_get_version_info_audit_only():
    info = get_version_info()
    assert info["audit_only"] is True


def test_is_known_release_v187():
    assert is_known_release("Decision Report Export & Evidence Pack v1.8.7") is True


def test_is_known_release_v186():
    assert is_known_release("End-to-End Small Capital Decision Cockpit v1.8.6") is True


def test_is_known_release_unknown():
    assert is_known_release("Unknown Release v99.0") is False


def test_check_minimum_version_same():
    assert check_minimum_version("1.8.7") is True


def test_check_minimum_version_lower():
    assert check_minimum_version("1.8.0") is True


def test_get_report_types_contains_daily():
    assert "daily_decision_report" in get_report_types()


def test_get_report_types_contains_weekly():
    assert "weekly_decision_report" in get_report_types()


def test_get_report_types_contains_evidence_pack():
    assert "evidence_pack" in get_report_types()


def test_get_report_types_contains_audit_trail():
    assert "audit_trail" in get_report_types()


def test_get_report_types_count():
    assert len(get_report_types()) == 12


def test_get_export_formats_contains_json():
    assert "json" in get_export_formats()


def test_get_export_formats_contains_markdown():
    assert "markdown" in get_export_formats()


def test_get_export_formats_contains_csv_rows():
    assert "csv_rows" in get_export_formats()


def test_get_export_formats_contains_console_summary():
    assert "console_summary" in get_export_formats()


def test_get_export_formats_contains_dashboard_payload():
    assert "dashboard_payload" in get_export_formats()


def test_get_export_formats_count():
    assert len(get_export_formats()) == 5


def test_get_final_report_grades_contains_complete():
    assert "COMPLETE" in get_final_report_grades()


def test_get_final_report_grades_contains_review_required():
    assert "REVIEW_REQUIRED" in get_final_report_grades()


def test_get_final_report_grades_contains_blocked():
    assert "BLOCKED" in get_final_report_grades()


def test_get_final_report_grades_count():
    assert len(get_final_report_grades()) == 5


def test_min_scenarios():
    assert MIN_SCENARIOS == 75


def test_min_fixtures():
    assert MIN_FIXTURES == 75


def test_min_cli():
    assert MIN_CLI == 23


def test_min_health_checks():
    assert MIN_HEALTH_CHECKS == 60


def test_included_releases_count():
    assert len(INCLUDED_RELEASES) >= 17


def test_known_release_names_non_empty():
    assert len(KNOWN_RELEASE_NAMES) >= 1
