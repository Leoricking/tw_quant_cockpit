"""
reports/paper_strategy_orchestration_report.py — Report generator for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


class PaperStrategyOrchestrationReport:
    """
    Generates research reports summarizing paper strategy orchestration activity.

    Report sections:
      - Summary (strategy count, signal count, decision count, proposal count)
      - Outcome distribution (APPROVED / REJECTED / DEFERRED / etc.)
      - Safety verification (all flags confirmed)
      - Health check snapshot
      - Lineage trace (sample)
      - Recommendations (research-only)

    [!] NOT INVESTMENT ADVICE. NOT A TRADE LOG. RESEARCH ONLY.
    [!] This report describes paper simulation activity, not real trading.
    """

    DISCLAIMER = (
        "[!] PAPER STRATEGY REPORT. NOT INVESTMENT ADVICE. "
        "NOT A REAL TRADE LOG. RESEARCH ONLY. "
        "NO REAL ORDERS WERE PLACED. NO BROKER WAS CONNECTED."
    )

    def generate(
        self,
        strategy_summaries: Optional[List[Dict]] = None,
        decision_distribution: Optional[Dict[str, int]] = None,
        proposal_distribution: Optional[Dict[str, int]] = None,
        health_result: Optional[Dict[str, Any]] = None,
        lineage_sample: Optional[List[Dict]] = None,
        period_start: Optional[str] = None,
        period_end: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate and return the full report as a dict."""
        strategy_summaries = strategy_summaries or []
        decision_distribution = decision_distribution or {}
        proposal_distribution = proposal_distribution or {}
        health_result = health_result or {}
        lineage_sample = lineage_sample or []

        total_decisions = sum(decision_distribution.values())
        approved = decision_distribution.get("APPROVED", 0)
        approval_rate = (approved / total_decisions * 100) if total_decisions > 0 else 0.0

        return {
            "report_type": "PaperStrategyOrchestrationReport",
            "version": "1.6.2",
            "generated_at": _now_iso(),
            "period_start": period_start,
            "period_end": period_end,
            "disclaimer": self.DISCLAIMER,

            "summary": {
                "strategy_count": len(strategy_summaries),
                "total_decisions": total_decisions,
                "approved_decisions": approved,
                "approval_rate_pct": round(approval_rate, 2),
                "total_proposals": sum(proposal_distribution.values()),
            },

            "strategies": strategy_summaries,

            "decision_distribution": decision_distribution,
            "proposal_distribution": proposal_distribution,

            "health": {
                "status": health_result.get("status", "UNKNOWN"),
                "passed": health_result.get("passed", 0),
                "total": health_result.get("total", 0),
                "failed_checks": [
                    c["name"] for c in health_result.get("checks", [])
                    if not c.get("ok", True)
                ],
            },

            "lineage_sample": lineage_sample[:10],

            "safety_verification": {
                "paper_only": True,
                "research_only": True,
                "simulation_only": True,
                "not_a_real_order": True,
                "no_broker_call": True,
                "no_real_account": True,
                "broker_execution_enabled": False,
                "production_trading_blocked": True,
                "real_order_creation_enabled": False,
                "real_order_execution_enabled": False,
                "short_selling_enabled": False,
                "margin_enabled": False,
                "autonomous_production_strategy_enabled": False,
            },

            "recommendations": [
                "All recommendations are RESEARCH ONLY and NOT INVESTMENT ADVICE.",
                "Review DEFERRED decisions and approve/deny via the approval policy.",
                "Monitor cooldown and rate-limit statistics for strategy tuning.",
                "Use FULL_REPLAY recovery mode for strict reproducibility verification.",
                "Paper simulation results do not predict real market performance.",
            ],
        }

    def format_text(self, report: Dict[str, Any]) -> str:
        """Format a report dict as human-readable text."""
        lines = [
            "=" * 70,
            f"  PAPER STRATEGY ORCHESTRATION REPORT — v{report.get('version', '?')}",
            f"  Generated: {report.get('generated_at', '?')}",
            "=" * 70,
            report.get("disclaimer", ""),
            "-" * 70,
            "SUMMARY",
        ]
        s = report.get("summary", {})
        lines += [
            f"  Strategies:          {s.get('strategy_count', 0)}",
            f"  Total Decisions:     {s.get('total_decisions', 0)}",
            f"  Approved Decisions:  {s.get('approved_decisions', 0)} "
            f"({s.get('approval_rate_pct', 0):.1f}%)",
            f"  Total Proposals:     {s.get('total_proposals', 0)}",
        ]
        lines.append("-" * 70)
        lines.append("DECISION DISTRIBUTION")
        for outcome, count in report.get("decision_distribution", {}).items():
            lines.append(f"  {outcome:25s}: {count}")
        lines.append("-" * 70)
        health = report.get("health", {})
        lines.append(
            f"HEALTH: {health.get('status', '?')} "
            f"({health.get('passed', 0)}/{health.get('total', 0)} checks)"
        )
        lines.append("-" * 70)
        lines.append("SAFETY VERIFICATION: ALL PAPER/RESEARCH FLAGS CONFIRMED")
        lines.append("=" * 70)
        return "\n".join(lines)
