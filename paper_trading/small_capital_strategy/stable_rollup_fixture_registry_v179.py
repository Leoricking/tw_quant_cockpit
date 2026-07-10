"""
paper_trading/small_capital_strategy/stable_rollup_fixture_registry_v179.py
Fixture registry for Small Capital Strategy Stable Rollup v1.7.9. 50 fixtures.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "179"
_POLICY  = "1.7.9-small-capital-strategy-stable-rollup"

_SAFETY = {
    "paper_only": True, "research_only": True, "no_real_orders": True,
    "no_broker": True, "not_investment_advice": True,
    "demo_only": True, "not_for_production": True,
    "production_trading_blocked": True,
}


def _f(fid: str, name: str, action: str, **kw) -> Dict[str, Any]:
    d = {
        "fixture_id": fid, "name": name, "expected_action": action,
        "schema_version": _SCHEMA, "policy_version": _POLICY,
    }
    d.update(_SAFETY)
    d.update(kw)
    return d


_FIXTURES: List[Dict[str, Any]] = [
    # ── PAPER_ENTRY_ALLOWED (10) ─────────────────────────────────────────────
    _f("FX179-001", "All 9 versions compat + health + gate PASS", "PAPER_ENTRY_ALLOWED",
       compat_versions=9, health_all_pass=True, gate_all_pass=True),
    _f("FX179-002", "v1.7.0 compat importable + version_match", "PAPER_ENTRY_ALLOWED",
       target="v1.7.0", importable=True, version_match=True),
    _f("FX179-003", "v1.7.1 compat importable + version_match", "PAPER_ENTRY_ALLOWED",
       target="v1.7.1", importable=True, version_match=True),
    _f("FX179-004", "v1.7.2 compat importable + version_match", "PAPER_ENTRY_ALLOWED",
       target="v1.7.2", importable=True, version_match=True),
    _f("FX179-005", "v1.7.3 compat importable + version_match", "PAPER_ENTRY_ALLOWED",
       target="v1.7.3", importable=True, version_match=True),
    _f("FX179-006", "v1.7.4 compat importable + version_match", "PAPER_ENTRY_ALLOWED",
       target="v1.7.4", importable=True, version_match=True),
    _f("FX179-007", "v1.7.5 compat importable + version_match", "PAPER_ENTRY_ALLOWED",
       target="v1.7.5", importable=True, version_match=True),
    _f("FX179-008", "v1.7.6 compat importable + version_match", "PAPER_ENTRY_ALLOWED",
       target="v1.7.6", importable=True, version_match=True),
    _f("FX179-009", "v1.7.7 compat importable + version_match", "PAPER_ENTRY_ALLOWED",
       target="v1.7.7", importable=True, version_match=True),
    _f("FX179-010", "v1.7.8 compat importable + version_match", "PAPER_ENTRY_ALLOWED",
       target="v1.7.8", importable=True, version_match=True),
    # ── PAPER_PLAN_READY (8) ────────────────────────────────────────────────
    _f("FX179-011", "Safety all_safe=True, all flags correct", "PAPER_PLAN_READY",
       safety_all_safe=True, no_margin=True, no_leverage=True),
    _f("FX179-012", "CLI all 12 stable commands registered", "PAPER_PLAN_READY",
       cli_registered=12, all_registered=True),
    _f("FX179-013", "GUI 3 stable tabs present", "PAPER_PLAN_READY",
       gui_tabs=["stable_rollup", "stable_health", "stable_report"], tabs_present=True),
    _f("FX179-014", "render_all_tabs no error strings", "PAPER_PLAN_READY",
       render_clean=True, error_count=0),
    _f("FX179-015", "50 stable fixtures all have safety flags", "PAPER_PLAN_READY",
       fixture_count=50, all_safe=True),
    _f("FX179-016", "50 stable scenarios no forbidden actions", "PAPER_PLAN_READY",
       scenario_count=50, all_clean=True),
    _f("FX179-017", "Regression audit clean, no forbidden words", "PAPER_PLAN_READY",
       regression_clean=True, issue_count=0),
    _f("FX179-018", "Manifest validate_manifest() returns True", "PAPER_PLAN_READY",
       manifest_valid=True, included_releases=9),
    # ── PAPER_ADD_ALLOWED (7) ────────────────────────────────────────────────
    _f("FX179-019", "Health 50+ checks all PASS", "PAPER_ADD_ALLOWED",
       health_total_ge=50, health_all_pass=True),
    _f("FX179-020", "Gate 50+ checks all PASS", "PAPER_ADD_ALLOWED",
       gate_total_ge=50, gate_all_pass=True),
    _f("FX179-021", "Report build succeeds, 11 sections", "PAPER_ADD_ALLOWED",
       report_sections=11, all_audits_pass=True),
    _f("FX179-022", "v1.7.0 health PASS", "PAPER_ADD_ALLOWED",
       target="v1.7.0", health_pass=True),
    _f("FX179-023", "v1.7.8 gate PASS", "PAPER_ADD_ALLOWED",
       target="v1.7.8", gate_pass=True),
    _f("FX179-024", "Models 5 dataclasses importable", "PAPER_ADD_ALLOWED",
       model_count=5, importable=True),
    _f("FX179-025", "version_v179 verify_version=True", "PAPER_ADD_ALLOWED",
       version="1.7.9", verify_version=True),
    # ── OBSERVE (5) ──────────────────────────────────────────────────────────
    _f("FX179-026", "Version metadata VERSION=1.7.9", "OBSERVE",
       version="1.7.9", schema="179"),
    _f("FX179-027", "RELEASE_NAME=Small Capital Strategy Stable Rollup", "OBSERVE",
       release_name="Small Capital Strategy Stable Rollup"),
    _f("FX179-028", "BASE_RELEASE=1.7.8 Small Capital Strategy Integration", "OBSERVE",
       base_release="1.7.8 Small Capital Strategy Integration"),
    _f("FX179-029", "INCLUDED_RELEASES has 9 entries", "OBSERVE",
       included_count=9),
    _f("FX179-030", "get_version_info() returns dict with paper_only=True", "OBSERVE",
       version_info_dict=True),
    # ── WAIT (5) ─────────────────────────────────────────────────────────────
    _f("FX179-031", "Compat check in progress", "WAIT",
       audit_status="in_progress", check="compat"),
    _f("FX179-032", "Health check loading", "WAIT",
       audit_status="loading", check="health"),
    _f("FX179-033", "Report generating", "WAIT",
       audit_status="generating", check="report"),
    _f("FX179-034", "CLI audit scanning", "WAIT",
       audit_status="scanning", check="cli"),
    _f("FX179-035", "GUI audit rendering", "WAIT",
       audit_status="rendering", check="gui"),
    # ── REDUCE_RISK (5) ──────────────────────────────────────────────────────
    _f("FX179-036", "Fixture safety violation found", "REDUCE_RISK",
       fixture_violation=True, missing_key="demo_only"),
    _f("FX179-037", "Scenario forbidden action detected", "REDUCE_RISK",
       forbidden_action=True, action_word="SELL"),
    _f("FX179-038", "CLI command missing from registry", "REDUCE_RISK",
       missing_command="small-capital-stable-gate"),
    _f("FX179-039", "GUI render error in stable_rollup tab", "REDUCE_RISK",
       render_error=True, tab="stable_rollup"),
    _f("FX179-040", "Regression safety flag anomaly", "REDUCE_RISK",
       regression_issue=True, flag="no_production_db_writes"),
    # ── REVIEW_REQUIRED (5) ──────────────────────────────────────────────────
    _f("FX179-041", "One version compat fail", "REVIEW_REQUIRED",
       compat_fail_count=1, compat_fail_version="v1.7.3"),
    _f("FX179-042", "One health check fail", "REVIEW_REQUIRED",
       health_fail_count=1, failed_check="compat_v173"),
    _f("FX179-043", "One gate check fail", "REVIEW_REQUIRED",
       gate_fail_count=1, failed_check="compat_v173"),
    _f("FX179-044", "Missing GUI tab", "REVIEW_REQUIRED",
       missing_tab="stable_health"),
    _f("FX179-045", "Safety flag warning", "REVIEW_REQUIRED",
       safety_warning=True, flag="not_for_production"),
    # ── BLOCKED (4) ──────────────────────────────────────────────────────────
    _f("FX179-046", "real_order=True blocked", "BLOCKED",
       real_order=True, block_reason="REAL_ORDER_BLOCKED"),
    _f("FX179-047", "broker_execution=True blocked", "BLOCKED",
       broker_execution=True, block_reason="BROKER_BLOCKED"),
    _f("FX179-048", "margin=True blocked", "BLOCKED",
       margin=True, block_reason="MARGIN_BLOCKED"),
    _f("FX179-049", "production_db_write blocked", "BLOCKED",
       production_write=True, block_reason="PRODUCTION_WRITE_ATTEMPTED"),
    # ── NO_TRADE (1) ─────────────────────────────────────────────────────────
    _f("FX179-050", "All audits fail → NO_TRADE", "NO_TRADE",
       all_fail=True, reason="ALL_AUDITS_FAIL"),
]


def get_all_fixtures() -> List[Dict[str, Any]]:
    return list(_FIXTURES)


def count_fixtures() -> int:
    return len(_FIXTURES)


def get_fixture_by_id(fid: str) -> Any:
    for f in _FIXTURES:
        if f["fixture_id"] == fid:
            return f
    return None


def validate_registry() -> bool:
    required_keys = ["paper_only", "research_only", "no_real_orders",
                     "no_broker", "not_investment_advice", "demo_only", "not_for_production"]
    for fx in _FIXTURES:
        for key in required_keys:
            if not fx.get(key):
                raise AssertionError(f"Fixture {fx['fixture_id']} missing {key}")
    return True
