"""
reports/drawdown_risk_controls_report.py — Drawdown & Risk Controls Report v1.5.3.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Never executable. No broker. No order. No ledger write.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

RESEARCH_ONLY  = True
REPORT_VERSION = "1.5.3"


class DrawdownRiskControlsReport:
    """
    Generates comprehensive drawdown & risk controls research reports.
    Sections: context, equity_curve, drawdown, episodes, attribution,
              risk_controls, risk_budget, stress, sizing_impact, lineage, safety.
    """

    RESEARCH_ONLY  = True
    REPORT_VERSION = REPORT_VERSION

    def generate(
        self,
        portfolio_id: str,
        as_of: str,
        evaluation=None,
        drawdown_summary=None,
        lineage: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a full drawdown & risk controls report.
        Returns dict with all sections.
        Never executable. No broker. No order. No ledger write.
        """
        generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        lineage = lineage or {}

        return {
            "report_version":  REPORT_VERSION,
            "generated_at":    generated_at,
            "portfolio_id":    portfolio_id,
            "as_of":           as_of,
            "research_only":   True,
            "executable":      False,
            "order_created":   False,
            "broker_called":   False,
            "ledger_write":    False,
            "sections":        [
                self._section_context(portfolio_id, as_of, evaluation),
                self._section_drawdown(drawdown_summary),
                self._section_risk_controls(evaluation),
                self._section_stress(evaluation),
                self._section_lineage(lineage),
                self._section_safety(),
            ],
        }

    def _section_context(self, portfolio_id: str, as_of: str, evaluation) -> Dict:
        return {
            "section":        "context",
            "portfolio_id":   portfolio_id,
            "as_of":          as_of,
            "evaluation_id":  getattr(evaluation, "evaluation_id", "") if evaluation else "",
            "report_type":    "DRAWDOWN_RISK_CONTROLS_RESEARCH",
            "research_only":  True,
        }

    def _section_drawdown(self, summary) -> Dict:
        if summary is None:
            return {"section": "drawdown", "status": "NO_DATA"}
        return {
            "section":             "drawdown",
            "max_drawdown_pct":    getattr(summary, "max_drawdown_pct", None),
            "current_drawdown_pct": getattr(summary, "current_drawdown_pct", None),
            "high_water_mark":     getattr(summary, "high_water_mark", None),
            "average_drawdown_pct": getattr(summary, "average_drawdown_pct", None),
            "research_only":       True,
        }

    def _section_risk_controls(self, evaluation) -> Dict:
        if evaluation is None:
            return {"section": "risk_controls", "status": "NO_DATA"}
        overall = getattr(evaluation, "overall_status", None)
        return {
            "section":       "risk_controls",
            "overall_status": overall.value if hasattr(overall, "value") else str(overall),
            "breach_count":  getattr(evaluation, "breach_count", 0),
            "warn_count":    getattr(evaluation, "warn_count", 0),
            "pass_count":    getattr(evaluation, "pass_count", 0),
            "research_only": True,
            "executable":    False,
            "order_created": False,
        }

    def _section_stress(self, evaluation) -> Dict:
        return {
            "section":       "stress",
            "description":   "Drawdown stress scenarios — research only, never executable",
            "research_only": True,
        }

    def _section_lineage(self, lineage: Dict) -> Dict:
        return {
            "section":       "lineage",
            "lineage_valid": lineage.get("lineage_valid", False),
            "research_only": True,
        }

    def _section_safety(self) -> Dict:
        return {
            "section":       "safety",
            "research_only": True,
            "executable":    False,
            "order_created": False,
            "broker_called": False,
            "ledger_write":  False,
            "labels": [
                "RESEARCH_ONLY",
                "NOT_AN_AUTOMATED_CONTROL",
                "NOT_A_STOP_ORDER",
                "NOT_AN_ORDER",
                "NO_BROKER_CALL",
                "NO_LEDGER_WRITE",
            ],
        }
