"""
tests/test_strategy_monitoring_engine_v194.py
Tests for strategy_monitoring_engine_v194.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_monitoring_engine_v194 import (
    validate_monitoring_action, validate_monitoring_status, validate_drift_category,
    run_drift_detection, build_monitoring_package_snapshot, build_rollback_alert,
    build_monitoring_recommendation, build_monitoring_evidence_pack,
    build_monitoring_audit_trail, build_monitoring_dashboard,
    build_monitoring_export_manifest, get_engine_info,
)


# ── get_engine_info ───────────────────────────────────────────────────────────

def test_engine_info_returns_dict():
    assert isinstance(get_engine_info(), dict)


def test_engine_info_version():
    assert get_engine_info()["version"] == "1.9.4"


def test_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True


def test_engine_info_monitoring_only():
    assert get_engine_info()["monitoring_only"] is True


def test_engine_info_schema():
    assert get_engine_info()["schema_version"] == "194"


# ── validate_monitoring_action ────────────────────────────────────────────────

def test_validate_monitoring_action_monitor_valid():
    result = validate_monitoring_action("MONITOR")
    assert result["valid"] is True
    assert result["blocked"] is False


def test_validate_monitoring_action_drift_check_valid():
    result = validate_monitoring_action("DRIFT_CHECK")
    assert result["valid"] is True


def test_validate_monitoring_action_rollback_alert_valid():
    result = validate_monitoring_action("ROLLBACK_ALERT")
    assert result["valid"] is True


def test_validate_monitoring_action_buy_blocked():
    result = validate_monitoring_action("BUY")
    assert result["blocked"] is True
    assert result["valid"] is False


def test_validate_monitoring_action_sell_blocked():
    result = validate_monitoring_action("SELL")
    assert result["blocked"] is True


def test_validate_monitoring_action_broker_order_blocked():
    result = validate_monitoring_action("BROKER_ORDER")
    assert result["blocked"] is True


# ── validate_monitoring_status ────────────────────────────────────────────────

def test_validate_monitoring_status_healthy():
    result = validate_monitoring_status("HEALTHY")
    assert result["valid"] is True
    assert result["blocked"] is False


def test_validate_monitoring_status_watch():
    result = validate_monitoring_status("WATCH")
    assert result["valid"] is True


def test_validate_monitoring_status_review_required():
    result = validate_monitoring_status("REVIEW_REQUIRED")
    assert result["valid"] is True


def test_validate_monitoring_status_rollback_required():
    result = validate_monitoring_status("ROLLBACK_REQUIRED")
    assert result["valid"] is True


def test_validate_monitoring_status_blocked():
    result = validate_monitoring_status("BLOCKED")
    assert result["valid"] is True


def test_validate_monitoring_status_invalid_unknown():
    result = validate_monitoring_status("UNKNOWN_STATUS")
    assert result["blocked"] is True


# ── validate_drift_category ───────────────────────────────────────────────────

def test_validate_drift_category_win_rate():
    result = validate_drift_category("WIN_RATE_DRIFT")
    assert result["valid"] is True


def test_validate_drift_category_expectancy():
    result = validate_drift_category("EXPECTANCY_DRIFT")
    assert result["valid"] is True


def test_validate_drift_category_market_regime():
    result = validate_drift_category("MARKET_REGIME_MISMATCH_DRIFT")
    assert result["valid"] is True


def test_validate_drift_category_unknown_blocked():
    result = validate_drift_category("FAKE_DRIFT")
    assert result["blocked"] is True


# ── run_drift_detection ───────────────────────────────────────────────────────

def test_run_drift_detection_blocked_missing_baseline():
    result = run_drift_detection("m1", "", "current_001", "win_001")
    assert result["blocked"] is True


def test_run_drift_detection_blocked_missing_current():
    result = run_drift_detection("m1", "baseline_001", "", "win_001")
    assert result["blocked"] is True


def test_run_drift_detection_blocked_missing_window():
    result = run_drift_detection("m1", "baseline_001", "current_001", "")
    assert result["blocked"] is True


def test_run_drift_detection_passes_with_all_inputs():
    result = run_drift_detection("m1", "baseline_001", "current_001", "win_001")
    assert result["blocked"] is False


def test_run_drift_detection_paper_only():
    result = run_drift_detection("m1", "b1", "c1", "w1")
    assert result["paper_only"] is True


def test_run_drift_detection_monitoring_only():
    result = run_drift_detection("m1", "b1", "c1", "w1")
    assert result["monitoring_only"] is True


def test_run_drift_detection_no_real_orders():
    result = run_drift_detection("m1", "b1", "c1", "w1")
    assert result["no_real_orders"] is True


def test_run_drift_detection_schema_version():
    result = run_drift_detection("m1", "b1", "c1", "w1")
    assert result["schema_version"] == "194"


def test_run_drift_detection_has_drift_severity():
    result = run_drift_detection("m1", "b1", "c1", "w1")
    assert "drift_severity" in result


def test_run_drift_detection_drift_detected_field():
    result = run_drift_detection("m1", "b1", "c1", "w1")
    assert "drift_detected" in result


def test_run_drift_detection_blocked_missing_monitoring_id():
    result = run_drift_detection("", "b1", "c1", "w1")
    assert result["blocked"] is True


# ── build_monitoring_package_snapshot ────────────────────────────────────────

def test_build_monitoring_package_snapshot_passes():
    result = build_monitoring_package_snapshot("pkg1", "prom_pkg_001", "rollback_001")
    assert result["blocked"] is False


def test_build_monitoring_package_snapshot_blocked_missing_id():
    result = build_monitoring_package_snapshot("", "prom_pkg_001", "rollback_001")
    assert result["blocked"] is True


def test_build_monitoring_package_snapshot_blocked_missing_promotion():
    result = build_monitoring_package_snapshot("pkg1", "", "rollback_001")
    assert result["blocked"] is True


def test_build_monitoring_package_snapshot_blocked_missing_rollback():
    result = build_monitoring_package_snapshot("pkg1", "prom_pkg_001", "")
    assert result["blocked"] is True


def test_build_monitoring_package_snapshot_paper_only():
    result = build_monitoring_package_snapshot("pkg1", "prom1", "rp1")
    assert result["paper_only"] is True


def test_build_monitoring_package_snapshot_monitoring_only():
    result = build_monitoring_package_snapshot("pkg1", "prom1", "rp1")
    assert result["monitoring_only"] is True


# ── build_rollback_alert ──────────────────────────────────────────────────────

def test_build_rollback_alert_auto_rollback_false():
    result = build_rollback_alert("a1", "WIN_RATE_DRIFT")
    assert result["auto_rollback"] is False


def test_build_rollback_alert_requires_manual_review():
    result = build_rollback_alert("a1", "WIN_RATE_DRIFT")
    assert result["requires_manual_review"] is True


def test_build_rollback_alert_paper_only():
    result = build_rollback_alert("a1", "DRAWDOWN_DRIFT")
    assert result["paper_only"] is True


def test_build_rollback_alert_monitoring_only():
    result = build_rollback_alert("a1", "EXPECTANCY_DRIFT")
    assert result["monitoring_only"] is True


def test_build_rollback_alert_blocked_missing_id():
    result = build_rollback_alert("", "WIN_RATE_DRIFT")
    assert result["blocked"] is True


def test_build_rollback_alert_has_severity():
    result = build_rollback_alert("a1", "WIN_RATE_DRIFT", severity="HIGH")
    assert result["severity"] == "HIGH"


# ── build_monitoring_recommendation ──────────────────────────────────────────

def test_build_monitoring_recommendation_continue_monitoring():
    result = build_monitoring_recommendation("r1", "CONTINUE_MONITORING", rationale="no issues")
    assert result["blocked"] is False


def test_build_monitoring_recommendation_blocked_missing_id():
    result = build_monitoring_recommendation("", "CONTINUE_MONITORING", rationale="no issues")
    assert result["blocked"] is True


def test_build_monitoring_recommendation_blocked_missing_rationale():
    result = build_monitoring_recommendation("r1", "CONTINUE_MONITORING", rationale="")
    assert result["blocked"] is True


def test_build_monitoring_recommendation_blocked_invalid_type():
    result = build_monitoring_recommendation("r1", "INVALID_TYPE", rationale="test")
    assert result["blocked"] is True


def test_build_monitoring_recommendation_paper_only():
    result = build_monitoring_recommendation("r1", "NO_CHANGE", rationale="stable")
    assert result["paper_only"] is True


def test_build_monitoring_recommendation_rollback_to_baseline():
    result = build_monitoring_recommendation("r1", "ROLLBACK_TO_BASELINE", rationale="critical drift")
    assert result["blocked"] is False


# ── build_monitoring_evidence_pack ────────────────────────────────────────────

def test_build_monitoring_evidence_pack_returns_dict():
    result = build_monitoring_evidence_pack("ep1", "m1")
    assert isinstance(result, dict)


def test_build_monitoring_evidence_pack_paper_only():
    result = build_monitoring_evidence_pack("ep1", "m1")
    assert result["paper_only"] is True


def test_build_monitoring_evidence_pack_report_only():
    result = build_monitoring_evidence_pack("ep1", "m1")
    assert result["report_only"] is True


def test_build_monitoring_evidence_pack_schema_version():
    result = build_monitoring_evidence_pack("ep1", "m1")
    assert result["schema_version"] == "194"


# ── build_monitoring_audit_trail ──────────────────────────────────────────────

def test_build_monitoring_audit_trail_returns_dict():
    result = build_monitoring_audit_trail("at1", "m1")
    assert isinstance(result, dict)


def test_build_monitoring_audit_trail_paper_only():
    result = build_monitoring_audit_trail("at1", "m1")
    assert result["paper_only"] is True


def test_build_monitoring_audit_trail_audit_only():
    result = build_monitoring_audit_trail("at1", "m1")
    assert result["audit_only"] is True


# ── build_monitoring_dashboard ────────────────────────────────────────────────

def test_build_monitoring_dashboard_returns_dict():
    result = build_monitoring_dashboard("dash1", "m1")
    assert isinstance(result, dict)


def test_build_monitoring_dashboard_paper_only():
    result = build_monitoring_dashboard("dash1", "m1")
    assert result["paper_only"] is True


def test_build_monitoring_dashboard_monitoring_only():
    result = build_monitoring_dashboard("dash1", "m1")
    assert result["monitoring_only"] is True


def test_build_monitoring_dashboard_overall_status():
    result = build_monitoring_dashboard("dash1", "m1", overall_status="WATCH")
    assert result["overall_status"] == "WATCH"


# ── build_monitoring_export_manifest ─────────────────────────────────────────

def test_build_monitoring_export_manifest_returns_dict():
    result = build_monitoring_export_manifest("man1", "m1")
    assert isinstance(result, dict)


def test_build_monitoring_export_manifest_paper_only():
    result = build_monitoring_export_manifest("man1", "m1")
    assert result["paper_only"] is True


def test_build_monitoring_export_manifest_review_only():
    result = build_monitoring_export_manifest("man1", "m1")
    assert result["review_only"] is True


def test_build_monitoring_export_manifest_schema_version():
    result = build_monitoring_export_manifest("man1", "m1")
    assert result["schema_version"] == "194"
