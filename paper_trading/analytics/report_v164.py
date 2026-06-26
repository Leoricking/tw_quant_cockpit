"""
paper_trading/analytics/report_v164.py — Analytics Report Generator v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Outputs: Markdown, JSON, CSV, HTML.
No investment advice. No auto trading instructions.
"""
from __future__ import annotations
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
PAPER_ONLY = True
INVESTMENT_ADVICE_ENABLED = False
AUTO_TRADING_INSTRUCTIONS_ENABLED = False

SAFETY_DISCLAIMER = (
    "[!] RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER. "
    "NOT INVESTMENT ADVICE. NOT FINANCIAL ADVICE. "
    "This report does not generate trading instructions."
)

REPORT_SECTIONS = [
    "Executive Summary",
    "Session Summary",
    "Data Quality",
    "Strategy Performance",
    "Execution Quality",
    "Operational Events",
    "Attribution",
    "Incidents and Recovery",
    "Anomalies",
    "Scorecard",
    "Root Cause Analysis",
    "Mistakes",
    "Lessons",
    "Action Items",
    "Limitations",
    "Safety Disclaimer",
    "Lineage",
    "Reproducibility",
]


class AnalyticsReportGenerator:
    """
    Generates analytics reports in multiple formats.
    All reports include Safety Disclaimer.
    No investment advice. No trading instructions.
    """

    def generate_json(
        self,
        analytics_result: Any,
        review: Optional[Any] = None,
        scorecard: Optional[Any] = None,
    ) -> str:
        data = self._build_report_dict(analytics_result, review, scorecard)
        return json.dumps(data, indent=2, default=str)

    def generate_markdown(
        self,
        analytics_result: Any,
        review: Optional[Any] = None,
        scorecard: Optional[Any] = None,
    ) -> str:
        data = self._build_report_dict(analytics_result, review, scorecard)
        lines: List[str] = []
        lines.append(f"# Operational Analytics Report")
        lines.append(f"")
        lines.append(f"**{SAFETY_DISCLAIMER}**")
        lines.append(f"")
        lines.append(f"## Executive Summary")
        lines.append(f"- Session: `{data['session_id']}`")
        lines.append(f"- Scope: {data['scope']}")
        lines.append(f"- As-of: {data['as_of']}")
        lines.append(f"- Data Quality: {data['data_quality']}")
        lines.append(f"")
        lines.append(f"## Session Summary")
        for k, v in data.get("session_summary", {}).items():
            lines.append(f"- {k}: {v}")
        lines.append(f"")
        lines.append(f"## Anomalies")
        for a in data.get("anomalies", []):
            lines.append(f"- [{a.get('severity')}] {a.get('metric')}: {a.get('observed')}")
        lines.append(f"")
        lines.append(f"## Scorecard")
        sc = data.get("scorecard", {})
        if sc:
            lines.append(f"- Overall: {sc.get('overall_score')}")
        lines.append(f"")
        lines.append(f"## {REPORT_SECTIONS[-3]}")  # Limitations
        lines.append(f"- All results are paper simulation only.")
        lines.append(f"- Missing data is reported as UNKNOWN, never assumed zero.")
        lines.append(f"")
        lines.append(f"## Safety Disclaimer")
        lines.append(SAFETY_DISCLAIMER)
        lines.append(f"")
        lines.append(f"## Lineage")
        lines.append(f"```json")
        lines.append(json.dumps(data.get("lineage", {}), indent=2, default=str))
        lines.append(f"```")
        return "\n".join(lines)

    def generate_csv(self, analytics_result: Any) -> str:
        """Generate a simple CSV of metrics."""
        lines: List[str] = ["metric,value,unit,quality"]
        metrics = getattr(analytics_result, "metrics", {})
        for name, obs in metrics.items():
            value = getattr(obs, "value", obs)
            unit = getattr(obs, "unit", "")
            quality = getattr(obs, "quality", "UNKNOWN")
            lines.append(f"{name},{value},{unit},{quality}")
        return "\n".join(lines)

    def generate_html(
        self,
        analytics_result: Any,
        review: Optional[Any] = None,
        scorecard: Optional[Any] = None,
    ) -> str:
        """Generate a minimal HTML report."""
        md = self.generate_markdown(analytics_result, review, scorecard)
        body = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        body = body.replace("\n", "<br>")
        return (
            "<!DOCTYPE html><html><head><title>Operational Analytics Report</title></head>"
            f"<body><p><strong>{SAFETY_DISCLAIMER}</strong></p><p>{body}</p></body></html>"
        )

    def _build_report_dict(
        self,
        analytics_result: Any,
        review: Optional[Any],
        scorecard: Optional[Any],
    ) -> Dict[str, Any]:
        session_id = getattr(analytics_result, "session_id", "UNKNOWN")
        scope = getattr(analytics_result, "scope", "UNKNOWN")
        as_of = getattr(analytics_result, "as_of", None)
        data_quality = getattr(analytics_result, "data_quality", "UNKNOWN")
        metrics = getattr(analytics_result, "metrics", {})
        anomalies = getattr(analytics_result, "anomalies", [])
        lineage = getattr(analytics_result, "lineage", {})
        repro_hash = getattr(analytics_result, "reproducibility_hash", None)

        data: Dict[str, Any] = {
            "session_id": session_id,
            "scope": str(scope),
            "as_of": as_of.isoformat() if as_of else None,
            "data_quality": str(data_quality),
            "session_summary": {k: str(getattr(v, "value", v)) for k, v in metrics.items()},
            "anomalies": [
                {
                    "metric": getattr(a, "metric", ""),
                    "observed": str(getattr(a, "observed", "")),
                    "severity": str(getattr(a, "severity", "")),
                    "rule_id": getattr(a, "rule_id", ""),
                }
                for a in anomalies
            ],
            "lineage": lineage,
            "reproducibility_hash": repro_hash,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "safety_disclaimer": SAFETY_DISCLAIMER,
            "report_sections": REPORT_SECTIONS,
        }

        if scorecard is not None:
            data["scorecard"] = {
                "overall_score": str(getattr(scorecard, "overall_score", "")),
                "quality": str(getattr(scorecard, "quality", "")),
                "blocking_failures": getattr(scorecard, "blocking_failures", []),
                "warnings": getattr(scorecard, "warnings", []),
            }

        if review is not None:
            data["review"] = {
                "review_id": getattr(review, "review_id", ""),
                "status": str(getattr(review, "status", "")),
                "scope": str(getattr(review, "review_scope", "")),
                "lessons": len(getattr(review, "lessons", [])),
                "action_items": len(getattr(review, "action_items", [])),
                "mistakes": len(getattr(review, "mistakes", [])),
            }

        return data


__all__ = ["AnalyticsReportGenerator", "SAFETY_DISCLAIMER", "REPORT_SECTIONS"]
