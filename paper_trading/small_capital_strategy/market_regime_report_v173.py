"""
paper_trading/small_capital_strategy/market_regime_report_v173.py
Report builder for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
from typing import Any, Dict

from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    MarketRegimeReport, MarketRegimeDetectionResult, CashRatioPlan,
    ExposureControlPlan, BucketAdjustmentPlan, CandidateRegimePermission,
    ABCRegimePermission, MarketRegimeScorecard,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.market_regime_report_v173"

REPORT_SECTION_NAMES = [
    "version",
    "regime_summary",
    "detection_detail",
    "trend_filter",
    "volatility_filter",
    "breadth_filter",
    "risk_off_detection",
    "cash_ratio_plan",
    "exposure_control_plan",
    "bucket_adjustment_plan",
    "candidate_permission",
    "abc_regime_compatibility",
    "scorecard",
    "safety_summary",
]


def _build_sections(
    regime: MarketRegime,
    detection: MarketRegimeDetectionResult,
    cash_plan: CashRatioPlan,
    exposure_plan: ExposureControlPlan,
    bucket_plan: BucketAdjustmentPlan,
    candidate_perm: CandidateRegimePermission,
    abc_perm: ABCRegimePermission,
    scorecard: MarketRegimeScorecard,
) -> Dict[str, Any]:
    return {
        "version": {
            "schema_version": _SCHEMA,
            "policy_version": _POLICY,
            "paper_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        },
        "regime_summary": {
            "regime": regime.value,
            "status": detection.status.value,
            "confidence": detection.confidence,
            "detection_note": detection.detection_note,
        },
        "detection_detail": {
            "regime": detection.regime.value,
            "block_reasons": [br.value for br in detection.block_reasons],
            "warnings": [w.value for w in detection.warnings],
        },
        "trend_filter": {
            "trend_signal": detection.trend.trend_signal.value,
            "trend_score": detection.trend.trend_score,
            "detail": detection.trend.detail,
        },
        "volatility_filter": {
            "volatility_level": detection.volatility.volatility_level.value,
            "volatility_score": detection.volatility.volatility_score,
            "volatility_controlled": detection.volatility.volatility_controlled,
        },
        "breadth_filter": {
            "breadth_signal": detection.breadth.breadth_signal.value,
            "advance_decline_ratio": detection.breadth.advance_decline_ratio,
            "breadth_healthy": detection.breadth.breadth_healthy,
        },
        "risk_off_detection": {
            "risk_off_signal": detection.risk_off.risk_off_signal.value,
            "volatility_spike": detection.risk_off.volatility_spike,
            "risk_event_active": detection.risk_off.risk_event_active,
        },
        "cash_ratio_plan": {
            "max_invested_pct": cash_plan.max_invested_pct,
            "cash_pct": cash_plan.cash_pct,
            "core_pct": cash_plan.core_pct,
            "main_theme_swing_pct": cash_plan.main_theme_swing_pct,
            "second_wave_setup_pct": cash_plan.second_wave_setup_pct,
            "short_term_training_pct": cash_plan.short_term_training_pct,
            "total_pct": cash_plan.total_pct,
            "allocation_valid": cash_plan.allocation_valid,
        },
        "exposure_control_plan": {
            "max_total_exposure_pct": exposure_plan.max_total_exposure_pct,
            "max_single_position_pct": exposure_plan.max_single_position_pct,
            "margin_allowed": exposure_plan.margin_allowed,
            "leverage_allowed": exposure_plan.leverage_allowed,
        },
        "bucket_adjustment_plan": {
            "capital_twd": bucket_plan.capital_twd,
            "core_amount": bucket_plan.core_amount,
            "main_theme_swing_amount": bucket_plan.main_theme_swing_amount,
            "second_wave_setup_amount": bucket_plan.second_wave_setup_amount,
            "short_term_training_amount": bucket_plan.short_term_training_amount,
            "cash_amount": bucket_plan.cash_amount,
            "total_amount": bucket_plan.total_amount,
        },
        "candidate_permission": {
            "tier": candidate_perm.tier,
            "permission": candidate_perm.permission.value,
            "max_candidates": candidate_perm.max_candidates,
            "buy_points_allowed": candidate_perm.buy_points_allowed,
        },
        "abc_regime_compatibility": {
            "a_allowed": abc_perm.a_allowed,
            "b_allowed": abc_perm.b_allowed,
            "c_allowed": abc_perm.c_allowed,
        },
        "scorecard": {
            "total_score": scorecard.total_score,
            "grade": scorecard.grade.value,
            "regime_detection_score": scorecard.regime_detection_score,
            "cash_ratio_score": scorecard.cash_ratio_score,
            "exposure_control_score": scorecard.exposure_control_score,
            "candidate_permission_score": scorecard.candidate_permission_score,
            "abc_compatibility_score": scorecard.abc_compatibility_score,
            "safety_score": scorecard.safety_score,
        },
        "safety_summary": {
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        },
    }


def build_market_regime_report(
    regime: MarketRegime,
    detection: MarketRegimeDetectionResult,
    cash_plan: CashRatioPlan,
    exposure_plan: ExposureControlPlan,
    bucket_plan: BucketAdjustmentPlan,
    candidate_perm: CandidateRegimePermission,
    abc_perm: ABCRegimePermission,
    scorecard: MarketRegimeScorecard,
) -> MarketRegimeReport:
    """Build full 14-section market regime report. Paper only."""
    sections = _build_sections(
        regime, detection, cash_plan, exposure_plan, bucket_plan,
        candidate_perm, abc_perm, scorecard,
    )
    return MarketRegimeReport(
        regime=regime,
        sections=sections,
        report_format="JSON",
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )


def render_report_json(report: MarketRegimeReport) -> str:
    """Render report as JSON string."""
    data = {
        "regime": report.regime.value,
        "sections": report.sections,
        "report_format": report.report_format,
        "schema_version": report.schema_version,
        "policy_version": report.policy_version,
        "paper_only": report.paper_only,
        "no_real_orders": report.no_real_orders,
        "not_investment_advice": report.not_investment_advice,
    }
    return json.dumps(data, indent=2, default=str)


def render_report_markdown(report: MarketRegimeReport) -> str:
    """Render report as markdown string."""
    lines = [
        "# Market Regime Position Control Report",
        f"**Regime:** {report.regime.value}",
        f"**Schema:** {report.schema_version}",
        f"**Policy:** {report.policy_version}",
        "",
        "> [!] Research Only. Paper Only. No Real Orders. Not Investment Advice.",
        "",
    ]
    for section_name in REPORT_SECTION_NAMES:
        if section_name in report.sections:
            lines.append(f"## {section_name.replace('_', ' ').title()}")
            section = report.sections[section_name]
            for k, v in section.items():
                lines.append(f"- **{k}**: {v}")
            lines.append("")
    return "\n".join(lines)


def render_report_console(report: MarketRegimeReport) -> str:
    """Render report as console-friendly text."""
    lines = [
        f"=== Market Regime Report ===",
        f"Regime: {report.regime.value}",
        f"[PAPER ONLY / NO REAL ORDERS]",
    ]
    scorecard = report.sections.get("scorecard", {})
    if scorecard:
        lines.append(f"Score: {scorecard.get('total_score', '?')} Grade: {scorecard.get('grade', '?')}")
    return "\n".join(lines)


def get_section_names() -> list:
    """Return list of all 14 section names."""
    return list(REPORT_SECTION_NAMES)
