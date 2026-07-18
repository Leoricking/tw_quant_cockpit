"""
paper_trading/small_capital_strategy/strategy_monitoring_fixtures_v194.py
75 JSON fixtures for Paper Strategy Monitoring & Drift Detection Lab v1.9.4.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SCHEMA = "194"
_SAFETY: Dict[str, Any] = dict(
    paper_only=True,
    research_only=True,
    simulate_only=True,
    validation_only=True,
    monitoring_only=True,
    drift_detection_only=True,
    rollback_trigger_only=True,
    review_only=True,
    report_only=True,
    audit_only=True,
    no_real_orders=True,
    no_broker=True,
    no_margin=True,
    no_leverage=True,
    no_production_strategy_mutation=True,
    no_live_strategy_activation=True,
    not_investment_advice=True,
    demo_only=True,
    not_for_production=True,
    production_trading_blocked=True,
)

_DRIFT_CATEGORIES: List[str] = [
    "WIN_RATE_DRIFT", "EXPECTANCY_DRIFT", "PROFIT_FACTOR_DRIFT",
    "DRAWDOWN_DRIFT", "AVERAGE_LOSS_DRIFT", "SIGNAL_COUNT_DRIFT",
    "SIGNAL_QUALITY_DRIFT", "MISTAKE_RATE_DRIFT", "CHASE_HIGH_DRIFT",
    "EARLY_ENTRY_DRIFT", "OVER_CONCENTRATION_DRIFT", "CASH_RESERVE_DRIFT",
    "GUARDRAIL_FALSE_POSITIVE_DRIFT", "GUARDRAIL_FALSE_NEGATIVE_DRIFT",
    "OPPORTUNITY_LOSS_DRIFT", "EVIDENCE_COMPLETENESS_DRIFT",
    "MARKET_REGIME_MISMATCH_DRIFT",
]

_MONITORING_STATUSES: List[str] = [
    "HEALTHY", "WATCH", "REVIEW_REQUIRED",
    "ROLLBACK_REQUIRED", "BLOCKED", "INVALID",
]

_RECOMMENDATIONS: List[str] = [
    "CONTINUE_MONITORING", "KEEP_SHADOW_ONLY", "REQUIRE_MANUAL_REVIEW",
    "TRIGGER_ROLLBACK_REVIEW", "ROLLBACK_TO_BASELINE",
    "EXTEND_MONITORING_WINDOW", "REQUIRE_MORE_DATA",
    "TIGHTEN_GUARDRAIL", "LOOSEN_GUARDRAIL",
    "LOWER_POSITION_SIZE", "RAISE_CASH_RESERVE",
    "SUSPEND_CANDIDATE_RULE", "NO_CHANGE",
]

_SEVERITIES: List[str] = ["NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"]


def _f(fid: str, cat: str, status: str = "HEALTHY", sev: str = "NONE",
        drift: bool = False, blocked: bool = False,
        drift_category: Optional[str] = None, **kw: Any) -> Dict[str, Any]:
    return {
        "fixture_id": fid,
        "schema_version": _SCHEMA,
        "drift_category": kw.pop("drift_category", drift_category or cat),
        "monitoring_status": status,
        "drift_severity": sev,
        "drift_detected": drift,
        "blocked": blocked,
        **_SAFETY,
        **kw,
    }


def get_all_fixtures() -> List[Dict[str, Any]]:
    """Return all 75 monitoring fixtures."""
    return [
        # ── Complete / Healthy (1-10) ─────────────────────────────────────────
        _f("SMF194-001", "WIN_RATE_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-001", baseline_win_rate=0.55, current_win_rate=0.55),
        _f("SMF194-002", "EXPECTANCY_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-002", baseline_expectancy=1.8, current_expectancy=1.8),
        _f("SMF194-003", "PROFIT_FACTOR_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-003", baseline_pf=2.1, current_pf=2.1),
        _f("SMF194-004", "DRAWDOWN_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-004", baseline_dd=0.08, current_dd=0.08),
        _f("SMF194-005", "SIGNAL_COUNT_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-005", baseline_signals=12, current_signals=12),
        _f("SMF194-006", "GUARDRAIL_FALSE_POSITIVE_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-006", fp_rate=0.05),
        _f("SMF194-007", "OPPORTUNITY_LOSS_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-007", opportunity_loss_pct=0.02),
        _f("SMF194-008", "MISTAKE_RATE_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-008", baseline_mistake_rate=0.10, current_mistake_rate=0.10),
        _f("SMF194-009", "EVIDENCE_COMPLETENESS_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-009", evidence_completeness=1.0),
        _f("SMF194-010", "MARKET_REGIME_MISMATCH_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-010", regime_match=True),

        # ── Win Rate Drift (11-18) ────────────────────────────────────────────
        _f("SMF194-011", "WIN_RATE_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-011", baseline_win_rate=0.55, current_win_rate=0.52),
        _f("SMF194-012", "WIN_RATE_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-012", baseline_win_rate=0.55, current_win_rate=0.45),
        _f("SMF194-013", "WIN_RATE_DRIFT", "ROLLBACK_REQUIRED", "HIGH", drift=True,
           monitoring_id="MON-013", baseline_win_rate=0.55, current_win_rate=0.38),
        _f("SMF194-014", "WIN_RATE_DRIFT", "ROLLBACK_REQUIRED", "CRITICAL", drift=True,
           monitoring_id="MON-014", baseline_win_rate=0.55, current_win_rate=0.28),
        _f("SMF194-015", "WIN_RATE_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-015", recommendation="CONTINUE_MONITORING"),
        _f("SMF194-016", "WIN_RATE_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-016", recommendation="REQUIRE_MANUAL_REVIEW"),
        _f("SMF194-017", "WIN_RATE_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-017", extend_window=True, recommendation="EXTEND_MONITORING_WINDOW"),
        _f("SMF194-018", "WIN_RATE_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-018", require_more_data=True, recommendation="REQUIRE_MORE_DATA"),

        # ── Expectancy Drift (19-23) ──────────────────────────────────────────
        _f("SMF194-019", "EXPECTANCY_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-019", baseline_expectancy=1.8, current_expectancy=1.6),
        _f("SMF194-020", "EXPECTANCY_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-020", baseline_expectancy=1.8, current_expectancy=1.3),
        _f("SMF194-021", "EXPECTANCY_DRIFT", "ROLLBACK_REQUIRED", "HIGH", drift=True,
           monitoring_id="MON-021", baseline_expectancy=1.8, current_expectancy=0.9),
        _f("SMF194-022", "EXPECTANCY_DRIFT", "ROLLBACK_REQUIRED", "CRITICAL", drift=True,
           monitoring_id="MON-022", baseline_expectancy=1.8, current_expectancy=0.5),
        _f("SMF194-023", "EXPECTANCY_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-023", recommendation="TRIGGER_ROLLBACK_REVIEW"),

        # ── Profit Factor Drift (24-27) ───────────────────────────────────────
        _f("SMF194-024", "PROFIT_FACTOR_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-024", baseline_pf=2.1, current_pf=1.9),
        _f("SMF194-025", "PROFIT_FACTOR_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-025", baseline_pf=2.1, current_pf=1.5),
        _f("SMF194-026", "PROFIT_FACTOR_DRIFT", "ROLLBACK_REQUIRED", "HIGH", drift=True,
           monitoring_id="MON-026", baseline_pf=2.1, current_pf=1.0),
        _f("SMF194-027", "PROFIT_FACTOR_DRIFT", "ROLLBACK_REQUIRED", "CRITICAL", drift=True,
           monitoring_id="MON-027", baseline_pf=2.1, current_pf=0.8),

        # ── Drawdown Drift (28-31) ────────────────────────────────────────────
        _f("SMF194-028", "DRAWDOWN_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-028", baseline_dd=0.08, current_dd=0.10),
        _f("SMF194-029", "DRAWDOWN_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-029", baseline_dd=0.08, current_dd=0.14),
        _f("SMF194-030", "DRAWDOWN_DRIFT", "ROLLBACK_REQUIRED", "HIGH", drift=True,
           monitoring_id="MON-030", baseline_dd=0.08, current_dd=0.20),
        _f("SMF194-031", "DRAWDOWN_DRIFT", "ROLLBACK_REQUIRED", "CRITICAL", drift=True,
           monitoring_id="MON-031", baseline_dd=0.08, current_dd=0.30),

        # ── Signal Count Drift (32-34) ────────────────────────────────────────
        _f("SMF194-032", "SIGNAL_COUNT_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-032", baseline_signals=12, current_signals=9),
        _f("SMF194-033", "SIGNAL_COUNT_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-033", baseline_signals=12, current_signals=5,
           recommendation="REQUIRE_MANUAL_REVIEW"),
        _f("SMF194-034", "SIGNAL_COUNT_DRIFT", "ROLLBACK_REQUIRED", "HIGH", drift=True,
           monitoring_id="MON-034", baseline_signals=12, current_signals=2,
           recommendation="ROLLBACK_TO_BASELINE"),

        # ── Guardrail Drift (35-38) ───────────────────────────────────────────
        _f("SMF194-035", "GUARDRAIL_FALSE_POSITIVE_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-035", fp_rate=0.15, recommendation="TIGHTEN_GUARDRAIL"),
        _f("SMF194-036", "GUARDRAIL_FALSE_POSITIVE_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-036", fp_rate=0.30, recommendation="LOOSEN_GUARDRAIL"),
        _f("SMF194-037", "GUARDRAIL_FALSE_NEGATIVE_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-037", fn_rate=0.20),
        _f("SMF194-038", "GUARDRAIL_FALSE_NEGATIVE_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-038", fn_rate=0.35),

        # ── Opportunity Loss Drift (39-41) ────────────────────────────────────
        _f("SMF194-039", "OPPORTUNITY_LOSS_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-039", opportunity_loss_pct=0.10),
        _f("SMF194-040", "OPPORTUNITY_LOSS_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-040", opportunity_loss_pct=0.25),
        _f("SMF194-041", "OPPORTUNITY_LOSS_DRIFT", "ROLLBACK_REQUIRED", "HIGH", drift=True,
           monitoring_id="MON-041", opportunity_loss_pct=0.40),

        # ── Market Regime Mismatch (42-44) ────────────────────────────────────
        _f("SMF194-042", "MARKET_REGIME_MISMATCH_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-042", regime_match=False, expected_regime="BULL",
           actual_regime="BEAR"),
        _f("SMF194-043", "MARKET_REGIME_MISMATCH_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-043", regime_match=False, expected_regime="BULL",
           actual_regime="CHOPPY"),
        _f("SMF194-044", "MARKET_REGIME_MISMATCH_DRIFT", "ROLLBACK_REQUIRED", "HIGH", drift=True,
           monitoring_id="MON-044", regime_match=False),

        # ── Cash Reserve / Concentration Drift (45-47) ───────────────────────
        _f("SMF194-045", "CASH_RESERVE_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-045", baseline_cash_pct=30, current_cash_pct=22,
           recommendation="RAISE_CASH_RESERVE"),
        _f("SMF194-046", "OVER_CONCENTRATION_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-046", concentration_pct=45,
           recommendation="LOWER_POSITION_SIZE"),
        _f("SMF194-047", "AVERAGE_LOSS_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-047", baseline_avg_loss=2500, current_avg_loss=3200),

        # ── Mistake Rate / Chase / Early Entry Drift (48-52) ─────────────────
        _f("SMF194-048", "MISTAKE_RATE_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-048", baseline_mistake_rate=0.10, current_mistake_rate=0.18),
        _f("SMF194-049", "MISTAKE_RATE_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-049", baseline_mistake_rate=0.10, current_mistake_rate=0.30),
        _f("SMF194-050", "CHASE_HIGH_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-050", chase_high_count=3,
           recommendation="SUSPEND_CANDIDATE_RULE"),
        _f("SMF194-051", "EARLY_ENTRY_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-051", early_entry_count=4),
        _f("SMF194-052", "SIGNAL_QUALITY_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-052", signal_quality_score=0.55),

        # ── Evidence Completeness Drift (53-55) ───────────────────────────────
        _f("SMF194-053", "EVIDENCE_COMPLETENESS_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-053", evidence_completeness=0.80),
        _f("SMF194-054", "EVIDENCE_COMPLETENESS_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-054", evidence_completeness=0.60),
        _f("SMF194-055", "EVIDENCE_COMPLETENESS_DRIFT", "ROLLBACK_REQUIRED", "HIGH", drift=True,
           monitoring_id="MON-055", evidence_completeness=0.40),

        # ── Blocked / Safety (56-65) ──────────────────────────────────────────
        _f("SMF194-056", "WIN_RATE_DRIFT", "BLOCKED", "NONE", blocked=True,
           monitoring_id="", block_reason="missing_monitoring_id"),
        _f("SMF194-057", "WIN_RATE_DRIFT", "BLOCKED", "NONE", blocked=True,
           monitoring_id="MON-057",
           block_reason="missing_promotion_package_source", promotion_package_source=""),
        _f("SMF194-058", "WIN_RATE_DRIFT", "BLOCKED", "NONE", blocked=True,
           monitoring_id="MON-058",
           block_reason="missing_rollback_plan_source", rollback_plan_source=""),
        _f("SMF194-059", "WIN_RATE_DRIFT", "BLOCKED", "NONE", blocked=True,
           monitoring_id="MON-059",
           block_reason="missing_baseline_monitoring_snapshot", baseline_snapshot_id=""),
        _f("SMF194-060", "WIN_RATE_DRIFT", "BLOCKED", "NONE", blocked=True,
           monitoring_id="MON-060",
           block_reason="missing_current_monitoring_snapshot", current_snapshot_id=""),
        _f("SMF194-061", "WIN_RATE_DRIFT", "BLOCKED", "NONE", blocked=True,
           monitoring_id="MON-061",
           block_reason="missing_monitoring_window", monitoring_window_id=""),
        _f("SMF194-062", "WIN_RATE_DRIFT", "BLOCKED", "NONE", blocked=True,
           monitoring_id="MON-062",
           block_reason="real_order_requested", action="BUY"),
        _f("SMF194-063", "WIN_RATE_DRIFT", "BLOCKED", "NONE", blocked=True,
           monitoring_id="MON-063",
           block_reason="production_strategy_mutation_attempted"),
        _f("SMF194-064", "WIN_RATE_DRIFT", "BLOCKED", "NONE", blocked=True,
           monitoring_id="MON-064",
           block_reason="live_strategy_activation_attempted"),
        _f("SMF194-065", "WIN_RATE_DRIFT", "BLOCKED", "NONE", blocked=True,
           monitoring_id="MON-065",
           block_reason="unsafe_export_path", export_path="production_db/strategy"),

        # ── Recommendations (66-70) ───────────────────────────────────────────
        _f("SMF194-066", "WIN_RATE_DRIFT", "HEALTHY", "NONE",
           monitoring_id="MON-066", recommendation="CONTINUE_MONITORING"),
        _f("SMF194-067", "WIN_RATE_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-067", recommendation="KEEP_SHADOW_ONLY"),
        _f("SMF194-068", "WIN_RATE_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-068", recommendation="EXTEND_MONITORING_WINDOW"),
        _f("SMF194-069", "WIN_RATE_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-069", recommendation="NO_CHANGE"),
        _f("SMF194-070", "WIN_RATE_DRIFT", "ROLLBACK_REQUIRED", "HIGH", drift=True,
           monitoring_id="MON-070", recommendation="ROLLBACK_TO_BASELINE"),

        # ── Multi-Drift / Complex (71-75) ─────────────────────────────────────
        _f("SMF194-071", "WIN_RATE_DRIFT", "ROLLBACK_REQUIRED", "CRITICAL", drift=True,
           monitoring_id="MON-071",
           secondary_drift="EXPECTANCY_DRIFT", multi_drift=True,
           recommendation="ROLLBACK_TO_BASELINE"),
        _f("SMF194-072", "SIGNAL_COUNT_DRIFT", "REVIEW_REQUIRED", "MEDIUM", drift=True,
           monitoring_id="MON-072",
           secondary_drift="GUARDRAIL_FALSE_POSITIVE_DRIFT", multi_drift=True),
        _f("SMF194-073", "DRAWDOWN_DRIFT", "ROLLBACK_REQUIRED", "HIGH", drift=True,
           monitoring_id="MON-073",
           secondary_drift="CASH_RESERVE_DRIFT", multi_drift=True),
        _f("SMF194-074", "MARKET_REGIME_MISMATCH_DRIFT", "WATCH", "LOW", drift=True,
           monitoring_id="MON-074",
           secondary_drift="OPPORTUNITY_LOSS_DRIFT", multi_drift=True),
        _f("SMF194-075", "EVIDENCE_COMPLETENESS_DRIFT", "BLOCKED", "NONE", blocked=True,
           monitoring_id="MON-075",
           block_reason="missing_evidence", evidence_completeness=0.0),
    ]


def get_fixture_by_id(fixture_id: str) -> Optional[Dict[str, Any]]:
    """Return a fixture dict by ID, or None if not found."""
    for fx in get_all_fixtures():
        if fx["fixture_id"] == fixture_id:
            return fx
    return None


def get_fixture_ids() -> List[str]:
    """Return list of all fixture IDs."""
    return [fx["fixture_id"] for fx in get_all_fixtures()]


def get_fixtures_by_status(status: str) -> List[Dict[str, Any]]:
    """Return fixtures filtered by monitoring_status."""
    return [fx for fx in get_all_fixtures() if fx.get("monitoring_status") == status]


def get_fixtures_by_severity(severity: str) -> List[Dict[str, Any]]:
    """Return fixtures filtered by drift_severity."""
    return [fx for fx in get_all_fixtures() if fx.get("drift_severity") == severity]


def get_blocked_fixtures() -> List[Dict[str, Any]]:
    """Return all blocked fixtures."""
    return [fx for fx in get_all_fixtures() if fx.get("blocked") is True]


def get_drift_fixtures() -> List[Dict[str, Any]]:
    """Return all fixtures with drift detected."""
    return [fx for fx in get_all_fixtures() if fx.get("drift_detected") is True]
