"""tests/test_strategy_promotion_engine_v193.py — v1.9.3 engine tests."""
import pytest
from paper_trading.small_capital_strategy.strategy_promotion_engine_v193 import (
    build_promotion_package, build_rollback_plan, validate_rollback_plan,
    build_promotion_approval_checklist, build_promotion_recommendation,
    build_promotion_evidence_pack, build_promotion_audit_trail,
    build_promotion_dashboard, build_promotion_export_manifest,
    validate_promotion_action, validate_promotion_approval_state,
    get_engine_info,
)


# ── build_promotion_package ───────────────────────────────────────────────────
def test_pkg_blocked_empty_sandbox():
    r = build_promotion_package("p1", "", "shadow_001", "cand_001", "base_001")
    assert r["blocked"] is True

def test_pkg_blocked_empty_shadow():
    r = build_promotion_package("p1", "sandbox_001", "", "cand_001", "base_001")
    assert r["blocked"] is True

def test_pkg_blocked_empty_baseline():
    r = build_promotion_package("p1", "sandbox_001", "shadow_001", "cand_001", "")
    assert r["blocked"] is True

def test_pkg_blocked_empty_promotion_id():
    r = build_promotion_package("", "sandbox_001", "shadow_001", "cand_001", "base_001")
    assert r["blocked"] is True

def test_pkg_passes_all_inputs():
    r = build_promotion_package("p1", "sandbox_001", "shadow_001", "cand_001", "base_001")
    assert r["blocked"] is False

def test_pkg_valid_true():
    r = build_promotion_package("p1", "sandbox_001", "shadow_001", "cand_001", "base_001")
    assert r["valid"] is True

def test_pkg_paper_only():
    r = build_promotion_package("p1", "sandbox_001", "shadow_001", "cand_001", "base_001")
    assert r["paper_only"] is True

def test_pkg_no_real_orders():
    r = build_promotion_package("p1", "sandbox_001", "shadow_001", "cand_001", "base_001")
    assert r["no_real_orders"] is True

def test_pkg_promotion_package_only():
    r = build_promotion_package("p1", "sandbox_001", "shadow_001", "cand_001", "base_001")
    assert r["promotion_package_only"] is True

def test_pkg_schema_version():
    r = build_promotion_package("p1", "sandbox_001", "shadow_001", "cand_001", "base_001")
    assert r["schema_version"] == "193"

def test_pkg_has_promotion_id():
    r = build_promotion_package("p1", "sandbox_001", "shadow_001", "cand_001", "base_001")
    assert r["promotion_id"] == "p1"

def test_pkg_blocked_has_block_reason():
    r = build_promotion_package("p1", "", "shadow_001", "cand_001", "base_001")
    assert "block_reason" in r

def test_pkg_rollback_plan_only():
    r = build_promotion_package("p1", "sandbox_001", "shadow_001", "cand_001", "base_001")
    assert r["rollback_plan_only"] is True

# ── build_rollback_plan ───────────────────────────────────────────────────────
def test_rollback_blocked_empty_baseline():
    r = build_rollback_plan("r1", "pkg1", "")
    assert r["blocked"] is True

def test_rollback_blocked_empty_plan_id():
    r = build_rollback_plan("", "pkg1", "base_001")
    assert r["blocked"] is True

def test_rollback_blocked_empty_package_id():
    r = build_rollback_plan("r1", "", "base_001")
    assert r["blocked"] is True

def test_rollback_passes_with_baseline():
    r = build_rollback_plan("r1", "pkg1", "base_001", ["WIN_RATE_DETERIORATION"], ["step1"])
    assert r["blocked"] is False

def test_rollback_valid_with_baseline():
    r = build_rollback_plan("r1", "pkg1", "base_001", ["WIN_RATE_DETERIORATION"], ["step1"])
    assert r["valid"] is True

def test_rollback_paper_only():
    r = build_rollback_plan("r1", "pkg1", "base_001")
    assert r["paper_only"] is True

def test_rollback_no_real_orders():
    r = build_rollback_plan("r1", "pkg1", "base_001")
    assert r["no_real_orders"] is True

def test_rollback_rollback_plan_only():
    r = build_rollback_plan("r1", "pkg1", "base_001")
    assert r["rollback_plan_only"] is True

def test_rollback_schema_version():
    r = build_rollback_plan("r1", "pkg1", "base_001")
    assert r["schema_version"] == "193"

def test_rollback_has_plan_id():
    r = build_rollback_plan("r1", "pkg1", "base_001")
    assert r["plan_id"] == "r1"

# ── validate_rollback_plan ────────────────────────────────────────────────────
def test_validate_rollback_missing_plan_id():
    r = validate_rollback_plan("", "base_001")
    assert r["valid"] is False

def test_validate_rollback_missing_baseline():
    r = validate_rollback_plan("r1", "")
    assert r["valid"] is False

def test_validate_rollback_passes():
    r = validate_rollback_plan("r1", "base_001")
    assert r["valid"] is True

def test_validate_rollback_paper_only():
    r = validate_rollback_plan("r1", "base_001")
    assert r["paper_only"] is True

def test_validate_rollback_schema():
    r = validate_rollback_plan("r1", "base_001")
    assert r["schema_version"] == "193"

# ── build_promotion_approval_checklist ────────────────────────────────────────
def test_checklist_blocked_no_rollback():
    r = build_promotion_approval_checklist("cl1", "pkg1", rollback_plan_present=False)
    assert r["blocked"] is True

def test_checklist_passes_with_rollback():
    r = build_promotion_approval_checklist("cl1", "pkg1", rollback_plan_present=True)
    assert r["blocked"] is False

def test_checklist_valid_with_rollback():
    r = build_promotion_approval_checklist("cl1", "pkg1", rollback_plan_present=True)
    assert r["valid"] is True

def test_checklist_paper_only():
    r = build_promotion_approval_checklist("cl1", "pkg1", rollback_plan_present=True)
    assert r["paper_only"] is True

def test_checklist_no_broker():
    r = build_promotion_approval_checklist("cl1", "pkg1", rollback_plan_present=True)
    assert r["no_broker"] is True

def test_checklist_schema():
    r = build_promotion_approval_checklist("cl1", "pkg1", rollback_plan_present=True)
    assert r["schema_version"] == "193"

def test_checklist_blocked_empty_checklist_id():
    r = build_promotion_approval_checklist("", "pkg1", rollback_plan_present=True)
    assert r["blocked"] is True

# ── build_promotion_recommendation ───────────────────────────────────────────
def test_recommendation_blocked_no_evidence():
    r = build_promotion_recommendation("rec1", "pkg1", "NO_CHANGE", "test", [])
    assert r["blocked"] is True

def test_recommendation_blocked_empty_id():
    r = build_promotion_recommendation("", "pkg1", "NO_CHANGE", "test", ["ev1"])
    assert r["blocked"] is True

def test_recommendation_blocked_empty_rationale():
    r = build_promotion_recommendation("rec1", "pkg1", "NO_CHANGE", "", ["ev1"])
    assert r["blocked"] is True

def test_recommendation_passes_with_evidence():
    r = build_promotion_recommendation("rec1", "pkg1", "PROMOTE_TO_PAPER_PACKAGE", "strong evidence", ["ev1", "ev2"])
    assert r["blocked"] is False

def test_recommendation_valid():
    r = build_promotion_recommendation("rec1", "pkg1", "PROMOTE_TO_PAPER_PACKAGE", "strong evidence", ["ev1"])
    assert r["valid"] is True

def test_recommendation_paper_only():
    r = build_promotion_recommendation("rec1", "pkg1", "NO_CHANGE", "test", ["ev1"])
    assert r["paper_only"] is True

def test_recommendation_schema():
    r = build_promotion_recommendation("rec1", "pkg1", "NO_CHANGE", "test", ["ev1"])
    assert r["schema_version"] == "193"

# ── build_promotion_evidence_pack ─────────────────────────────────────────────
def test_evidence_pack_paper_only():
    r = build_promotion_evidence_pack("ep1", "pkg1")
    assert r["paper_only"] is True

def test_evidence_pack_audit_only():
    r = build_promotion_evidence_pack("ep1", "pkg1")
    assert r["audit_only"] is True

def test_evidence_pack_no_real_orders():
    r = build_promotion_evidence_pack("ep1", "pkg1")
    assert r["no_real_orders"] is True

def test_evidence_pack_schema():
    r = build_promotion_evidence_pack("ep1", "pkg1")
    assert r["schema_version"] == "193"

def test_evidence_pack_blocked_empty_id():
    r = build_promotion_evidence_pack("", "pkg1")
    assert r["blocked"] is True

# ── build_promotion_audit_trail ───────────────────────────────────────────────
def test_audit_trail_paper_only():
    r = build_promotion_audit_trail("at1", "pkg1")
    assert r["paper_only"] is True

def test_audit_trail_promotion_package_only():
    r = build_promotion_audit_trail("at1", "pkg1")
    assert r["promotion_package_only"] is True

def test_audit_trail_schema():
    r = build_promotion_audit_trail("at1", "pkg1")
    assert r["schema_version"] == "193"

def test_audit_trail_deterministic_ts():
    r = build_promotion_audit_trail("at1", "pkg1")
    assert r["deterministic_timestamp_policy"] == "date_label_only_no_wall_clock"

def test_audit_trail_blocked_empty_id():
    r = build_promotion_audit_trail("", "pkg1")
    assert r["blocked"] is True

# ── build_promotion_dashboard ─────────────────────────────────────────────────
def test_dashboard_paper_only():
    r = build_promotion_dashboard("d1", "pkg1")
    assert r["paper_only"] is True

def test_dashboard_rollback_plan_only():
    r = build_promotion_dashboard("d1", "pkg1")
    assert r["rollback_plan_only"] is True

def test_dashboard_schema():
    r = build_promotion_dashboard("d1", "pkg1")
    assert r["schema_version"] == "193"

def test_dashboard_default_approval_state():
    r = build_promotion_dashboard("d1", "pkg1")
    assert r["approval_state"] == "DRAFT"

def test_dashboard_blocked_empty_id():
    r = build_promotion_dashboard("", "pkg1")
    assert r["blocked"] is True

# ── build_promotion_export_manifest ──────────────────────────────────────────
def test_export_manifest_paper_only():
    r = build_promotion_export_manifest("em1", "pkg1")
    assert r["paper_only"] is True

def test_export_manifest_report_only():
    r = build_promotion_export_manifest("em1", "pkg1")
    assert r["report_only"] is True

def test_export_manifest_default_path():
    r = build_promotion_export_manifest("em1", "pkg1")
    assert r["export_path"] == "reports/"

def test_export_manifest_schema():
    r = build_promotion_export_manifest("em1", "pkg1")
    assert r["schema_version"] == "193"

def test_export_manifest_blocked_empty_id():
    r = build_promotion_export_manifest("", "pkg1")
    assert r["blocked"] is True

# ── validate_promotion_action (engine) ───────────────────────────────────────
def test_engine_validate_action_buy_blocked():
    r = validate_promotion_action("BUY")
    assert r["blocked"] is True

def test_engine_validate_action_review_valid():
    r = validate_promotion_action("REVIEW")
    assert r["valid"] is True

def test_engine_validate_action_unknown():
    r = validate_promotion_action("UNKNOWN")
    assert r["blocked"] is False
    assert r["valid"] is False

# ── validate_promotion_approval_state ────────────────────────────────────────
def test_validate_approval_state_draft():
    r = validate_promotion_approval_state("DRAFT")
    assert r["valid"] is True

def test_validate_approval_state_paper_ready():
    r = validate_promotion_approval_state("PAPER_PROMOTION_READY")
    assert r["valid"] is True

def test_validate_approval_state_unknown():
    r = validate_promotion_approval_state("UNKNOWN_STATE")
    assert r["valid"] is False

def test_validate_approval_state_blocked():
    r = validate_promotion_approval_state("BLOCKED")
    assert r["valid"] is True

# ── get_engine_info ───────────────────────────────────────────────────────────
def test_engine_info_paper_only(): assert get_engine_info()["paper_only"] is True
def test_engine_info_schema(): assert get_engine_info()["schema_version"] == "193"
def test_engine_info_no_real_orders(): assert get_engine_info()["no_real_orders"] is True
def test_engine_info_promotion_package_only(): assert get_engine_info()["promotion_package_only"] is True
def test_engine_info_rollback_plan_only(): assert get_engine_info()["rollback_plan_only"] is True
def test_engine_info_is_dict(): assert isinstance(get_engine_info(), dict)
