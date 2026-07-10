"""
paper_trading/small_capital_strategy/mistake_taxonomy_report_v176.py
Report generation for Mistake Taxonomy & Weekly Review Dashboard v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import ReviewDashboard

_SCHEMA = "176"
_POLICY = "1.7.6-mistake-taxonomy-weekly-review"

REPORT_SECTION_NAMES: List[str] = [
    "summary",
    "behavior_score",
    "mistake_events",
    "cost_summary",
    "repeat_patterns",
    "weekly_review",
    "monthly_review",
    "top_actions",
    "blocking_risks",
    "improvement_plan",
    "safety_audit",
    "version_info",
    "disclaimer",
]


def get_report_sections() -> List[str]:
    """Return all report section names."""
    return list(REPORT_SECTION_NAMES)


def build_report_dict(dashboard: ReviewDashboard) -> Dict[str, Any]:
    """Build a report dict from a ReviewDashboard."""
    bs = dashboard.behavior_score
    weekly = dashboard.weekly_result
    monthly = dashboard.monthly_result

    sections: Dict[str, Any] = {
        "summary": {
            "events_count": dashboard.events_count,
            "entries_count": dashboard.entries_count,
            "paper_only": True,
            "not_investment_advice": True,
        },
        "behavior_score": {
            "score": bs.score if bs else 0.0,
            "level": bs.level.value if bs else "PASS",
            "description": bs.description if bs else "",
            "factors": bs.factors if bs else {},
        },
        "mistake_events": {
            "count": dashboard.events_count,
        },
        "cost_summary": {},
        "repeat_patterns": {
            "count": 0,
        },
        "weekly_review": {
            "week_start": weekly.week_start if weekly else "",
            "week_end": weekly.week_end if weekly else "",
            "total_events": weekly.total_events if weekly else 0,
            "risk_level": weekly.risk_level.value if weekly else "PASS",
        },
        "monthly_review": {
            "month_label": monthly.month_label if monthly else "",
            "total_events": monthly.total_events if monthly else 0,
            "behavior_trend": monthly.behavior_trend if monthly else "STABLE",
        },
        "top_actions": [
            {"action_id": a.action_id, "description": a.description, "priority": a.priority}
            for a in dashboard.top_actions
        ],
        "blocking_risks": [],
        "improvement_plan": {
            "actions_count": len(dashboard.top_actions),
            "paper_only": True,
        },
        "safety_audit": {
            "paper_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "no_margin": True,
        },
        "version_info": {
            "schema_version": _SCHEMA,
            "policy_version": _POLICY,
        },
        "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
    }
    return {"sections": sections, "paper_only": True, "not_investment_advice": True}


def render_json(report_dict: Dict[str, Any]) -> str:
    """Render report dict as JSON string."""
    return json.dumps(report_dict, indent=2, default=str)


def render_markdown(report_dict: Dict[str, Any]) -> str:
    """Render report dict as Markdown string."""
    sections = report_dict.get("sections", {})
    lines: List[str] = [
        "# Mistake Taxonomy & Weekly Review Report v1.7.6",
        "",
        "> Research Only | Paper Only | No Real Orders | Not Investment Advice",
        "",
    ]
    for name in REPORT_SECTION_NAMES:
        if name in sections:
            lines.append(f"## {name.replace('_', ' ').title()}")
            data = sections[name]
            if isinstance(data, dict):
                for k, v in data.items():
                    lines.append(f"- **{k}**: {v}")
            elif isinstance(data, list):
                for item in data:
                    lines.append(f"- {item}")
            lines.append("")
    return "\n".join(lines)
