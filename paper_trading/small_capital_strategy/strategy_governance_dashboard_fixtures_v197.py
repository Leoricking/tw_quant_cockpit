"""
paper_trading/small_capital_strategy/strategy_governance_dashboard_fixtures_v197.py
JSON fixtures for Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only. Quality Analytics Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_BASE_FLAGS = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "governance_analytics_only": True,
    "dashboard_only": True,
    "quality_analytics_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_strategy_mutation": True,
    "no_automatic_rollback": True,
    "no_live_strategy_activation": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
    "schema_version": "197",
}


def _f(fid: str, name: str, **kwargs) -> Dict[str, Any]:
    return {**_BASE_FLAGS, "id": fid, "fixture_id": fid, "name": name, **kwargs}


_FIXTURES: List[Dict[str, Any]] = [
    # ── Version / schema fixtures (1-5) ──────────────────────────────────────
    _f("SMF197-001", "version_197_fixture",
       version="1.9.7", schema_version="197", verify_version=True),
    _f("SMF197-002", "release_name_fixture",
       release_name="Paper Strategy Governance Dashboard & Decision Quality Analytics Lab"),
    _f("SMF197-003", "policy_version_fixture",
       policy_version="1.9.7-small-capital-strategy-paper-strategy-governance-dashboard-decision-quality-analytics-lab"),
    _f("SMF197-004", "included_releases_fixture",
       included_release_count=27, includes_v196=True, includes_v190=True),
    _f("SMF197-005", "schema_197_paper_only_fixture",
       schema_version="197", paper_only=True, governance_analytics_only=True),

    # ── Decision quality metric fixtures (6-17) ──────────────────────────────
    _f("SMF197-006", "metric_evidence_coverage_score",
       metric_name="evidence_coverage_score", weight=1.0, paper_only=True),
    _f("SMF197-007", "metric_rationale_completeness_score",
       metric_name="rationale_completeness_score", weight=1.0, paper_only=True),
    _f("SMF197-008", "metric_checklist_completeness_score",
       metric_name="checklist_completeness_score", weight=1.0, paper_only=True),
    _f("SMF197-009", "metric_lineage_completeness_score",
       metric_name="lineage_completeness_score", weight=1.0, paper_only=True),
    _f("SMF197-010", "metric_audit_trail_completeness_score",
       metric_name="audit_trail_completeness_score", weight=1.0, paper_only=True),
    _f("SMF197-011", "metric_outcome_consistency_score",
       metric_name="outcome_consistency_score", weight=1.0, paper_only=True),
    _f("SMF197-012", "metric_rollback_review_frequency_score",
       metric_name="rollback_review_frequency_score", weight=1.0, paper_only=True),
    _f("SMF197-013", "metric_governance_violation_score",
       metric_name="governance_violation_score", weight=1.0, paper_only=True),
    _f("SMF197-014", "metric_paper_only_safety_score",
       metric_name="paper_only_safety_score", weight=1.0, paper_only=True),
    _f("SMF197-015", "metric_decision_latency_score",
       metric_name="decision_latency_score", weight=1.0, paper_only=True),
    _f("SMF197-016", "metric_review_quality_score",
       metric_name="review_quality_score", weight=1.0, paper_only=True),
    _f("SMF197-017", "metric_registry_integrity_score",
       metric_name="registry_integrity_score", weight=1.0, paper_only=True),

    # ── Decision quality grade fixtures (18-22) ──────────────────────────────
    _f("SMF197-018", "grade_excellent",
       grade="EXCELLENT", min_score=0.85, paper_only=True),
    _f("SMF197-019", "grade_good",
       grade="GOOD", min_score=0.70, paper_only=True),
    _f("SMF197-020", "grade_watch",
       grade="WATCH", min_score=0.50, paper_only=True),
    _f("SMF197-021", "grade_weak",
       grade="WEAK", min_score=0.01, paper_only=True),
    _f("SMF197-022", "grade_invalid",
       grade="INVALID", score=0.0, paper_only=True),

    # ── Analytics window fixtures (23-27) ────────────────────────────────────
    _f("SMF197-023", "analytics_window_daily",
       window_type="DAILY", paper_only=True, valid=True),
    _f("SMF197-024", "analytics_window_weekly",
       window_type="WEEKLY", paper_only=True, valid=True),
    _f("SMF197-025", "analytics_window_monthly",
       window_type="MONTHLY", paper_only=True, valid=True),
    _f("SMF197-026", "analytics_window_quarterly",
       window_type="QUARTERLY", paper_only=True, valid=True),
    _f("SMF197-027", "analytics_window_full_history",
       window_type="FULL_HISTORY", paper_only=True, valid=True),

    # ── Dashboard panel fixtures (28-39) ─────────────────────────────────────
    _f("SMF197-028", "panel_quality_overview",
       panel_name="quality_overview", paper_only=True, dashboard_only=True),
    _f("SMF197-029", "panel_evidence_coverage",
       panel_name="evidence_coverage", paper_only=True, research_only=True),
    _f("SMF197-030", "panel_decision_outcome",
       panel_name="decision_outcome", paper_only=True, governance_analytics_only=True),
    _f("SMF197-031", "panel_approval_quality",
       panel_name="approval_quality", auto_approval=False, no_production_mutation=True),
    _f("SMF197-032", "panel_rejection_quality",
       panel_name="rejection_quality", paper_only=True),
    _f("SMF197-033", "panel_keep_monitoring_quality",
       panel_name="keep_monitoring_quality", paper_only=True),
    _f("SMF197-034", "panel_rollback_review_frequency",
       panel_name="rollback_review_frequency", auto_rollback=False, requires_human_review=True),
    _f("SMF197-035", "panel_governance_violations",
       panel_name="governance_violations", paper_only=True, governance_analytics_only=True),
    _f("SMF197-036", "panel_decision_lineage_health",
       panel_name="decision_lineage_health", paper_only=True, immutable=True),
    _f("SMF197-037", "panel_audit_trail_health",
       panel_name="audit_trail_health", paper_only=True, audit_only=True),
    _f("SMF197-038", "panel_safety_summary",
       panel_name="safety_summary", paper_only=True, no_real_orders=True, no_broker=True),
    _f("SMF197-039", "panel_export_manifest",
       panel_name="export_manifest", paper_only=True, safe_path_only=True),

    # ── Safety flag fixtures (40-47) ─────────────────────────────────────────
    _f("SMF197-040", "safety_flags_all_set",
       all_safety_flags_set=True, paper_only=True, no_real_orders=True,
       no_broker=True, governance_analytics_only=True, dashboard_only=True),
    _f("SMF197-041", "safety_no_production_mutation",
       no_production_strategy_mutation=True, production_mutation_blocked=True),
    _f("SMF197-042", "safety_no_automatic_rollback",
       no_automatic_rollback=True, auto_rollback=False, requires_human_review=True),
    _f("SMF197-043", "safety_no_live_activation",
       no_live_strategy_activation=True, live_activation_blocked=True),
    _f("SMF197-044", "safety_analytics_does_not_execute",
       analytics_executes_decision=False, dashboard_mutates_strategy=False),
    _f("SMF197-045", "safety_forbidden_actions_count_9",
       forbidden_action_count=9, no_real_orders=True),
    _f("SMF197-046", "safety_allowed_actions_count_18",
       allowed_action_count=18, paper_only=True, governance_analytics_only=True),
    _f("SMF197-047", "safety_hard_block_conditions_count_17",
       hard_block_count=17, all_blocks_defined=True),

    # ── Hard block condition fixtures (48-57) ────────────────────────────────
    _f("SMF197-048", "hard_block_real_order_requested",
       block_condition="real_order_requested", blocked=True, paper_only=True),
    _f("SMF197-049", "hard_block_broker_requested",
       block_condition="broker_requested", blocked=True, no_broker=True),
    _f("SMF197-050", "hard_block_margin_or_leverage_requested",
       block_condition="margin_or_leverage_requested", blocked=True, no_margin=True),
    _f("SMF197-051", "hard_block_production_db_write",
       block_condition="production_db_write_attempted", blocked=True),
    _f("SMF197-052", "hard_block_production_mutation",
       block_condition="production_strategy_mutation_attempted", blocked=True),
    _f("SMF197-053", "hard_block_automatic_rollback",
       block_condition="automatic_rollback_attempted", blocked=True, auto_rollback=False),
    _f("SMF197-054", "hard_block_live_activation",
       block_condition="live_strategy_activation_attempted", blocked=True),
    _f("SMF197-055", "hard_block_missing_registry_source",
       block_condition="missing_registry_source", blocked=True, registry_source=""),
    _f("SMF197-056", "hard_block_malformed_analytics_input",
       block_condition="malformed_analytics_input", blocked=True),
    _f("SMF197-057", "hard_block_unsafe_export_path",
       block_condition="unsafe_export_path", blocked=True,
       export_path="C:/production/analytics.json"),

    # ── Engine function fixtures (58-67) ─────────────────────────────────────
    _f("SMF197-058", "engine_build_dashboard_input_valid",
       registry_source="REG-ENG-001", analytics_window="FULL_HISTORY",
       expected_valid=True, expected_blocked=False),
    _f("SMF197-059", "engine_build_quality_score_valid",
       decision_id="DEC-QS-001", metrics={"evidence_coverage_score": 0.9},
       expected_valid=True),
    _f("SMF197-060", "engine_build_quality_grade_excellent",
       decision_id="DEC-GR-001", composite_score=0.90, expected_grade="EXCELLENT"),
    _f("SMF197-061", "engine_build_quality_grade_good",
       decision_id="DEC-GR-002", composite_score=0.75, expected_grade="GOOD"),
    _f("SMF197-062", "engine_build_quality_grade_watch",
       decision_id="DEC-GR-003", composite_score=0.55, expected_grade="WATCH"),
    _f("SMF197-063", "engine_build_quality_grade_weak",
       decision_id="DEC-GR-004", composite_score=0.30, expected_grade="WEAK"),
    _f("SMF197-064", "engine_build_evidence_coverage_valid",
       registry_source="REG-ENG-002", analytics_window="MONTHLY",
       expected_valid=True),
    _f("SMF197-065", "engine_build_outcome_summary_valid",
       registry_source="REG-ENG-002", analytics_window="WEEKLY",
       expected_valid=True),
    _f("SMF197-066", "engine_build_violation_summary_valid",
       registry_source="REG-ENG-003", analytics_window="FULL_HISTORY",
       expected_valid=True),
    _f("SMF197-067", "engine_build_dashboard_panel_valid",
       panel_name="quality_overview", expected_valid=True),

    # ── Report section fixtures (68-75) ──────────────────────────────────────
    _f("SMF197-068", "report_sections_count_12",
       report_section_count=12, all_sections_paper_only=True),
    _f("SMF197-069", "report_export_quality_overview",
       registry_source="REG-RPT-001", section="quality_overview_report",
       expected_valid=True, paper_only=True),
    _f("SMF197-070", "report_export_evidence_coverage",
       registry_source="REG-RPT-001", section="evidence_coverage_report",
       expected_valid=True, paper_only=True),
    _f("SMF197-071", "report_export_decision_outcome",
       registry_source="REG-RPT-002", section="decision_outcome_report",
       expected_valid=True, paper_only=True),
    _f("SMF197-072", "report_export_approval_quality",
       registry_source="REG-RPT-002", section="approval_quality_report",
       expected_valid=True, auto_approval=False),
    _f("SMF197-073", "report_export_governance_violations",
       registry_source="REG-RPT-003", section="governance_violations_report",
       expected_valid=True, paper_only=True),
    _f("SMF197-074", "report_export_scorecard",
       registry_source="REG-RPT-003", section="scorecard_report",
       expected_valid=True, scorecard_metrics=12),
    _f("SMF197-075", "report_export_full_dashboard_pack",
       registry_source="REG-RPT-004", section="full_dashboard_pack",
       expected_valid=True, auto_rollback=False, auto_approval=False,
       analytics_executes_decision=False, dashboard_mutates_strategy=False,
       all_sections_included=True),
]

assert len(_FIXTURES) == 75, f"Expected 75 fixtures, got {len(_FIXTURES)}"


def get_all_fixtures() -> List[Dict[str, Any]]:
    """Return all 75 governance dashboard fixtures."""
    return list(_FIXTURES)


def get_fixture_count() -> int:
    """Return total fixture count."""
    return len(_FIXTURES)


def get_fixture_by_id(fixture_id: str) -> Optional[Dict[str, Any]]:
    """Return a fixture by ID, or None if not found."""
    for f in _FIXTURES:
        if f.get("fixture_id") == fixture_id:
            return dict(f)
    return None
