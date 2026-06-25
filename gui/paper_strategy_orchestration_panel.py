"""
gui/paper_strategy_orchestration_panel.py — GUI panel for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class PaperStrategyOrchestrationPanel:
    """
    GUI panel summarizing paper strategy orchestration state.

    Displays:
      - Registered strategies (count, status breakdown)
      - Recent decisions (outcome distribution)
      - Open proposals (pending approvals)
      - Health check summary
      - Safety status banner

    [!] PAPER STRATEGY ONLY. NOT INVESTMENT ADVICE. NO REAL ORDERS.
    """

    TITLE = "Paper Strategy Orchestration [v1.6.2]"
    SAFETY_BANNER = (
        "[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. "
        "PRODUCTION TRADING: BLOCKED. RESEARCH ONLY. NOT INVESTMENT ADVICE."
    )

    def __init__(self) -> None:
        self._last_health: Optional[Dict[str, Any]] = None

    def render(
        self,
        registry_summary: Optional[List[Dict]] = None,
        decision_distribution: Optional[Dict[str, int]] = None,
        pending_proposals: Optional[List[Dict]] = None,
        health_result: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Render the panel state as a dict (for CLI/GUI consumption).
        Returns structured display data.
        """
        if health_result is not None:
            self._last_health = health_result

        strategies = registry_summary or []
        status_counts: Dict[str, int] = {}
        for s in strategies:
            status = s.get("status", "UNKNOWN")
            status_counts[status] = status_counts.get(status, 0) + 1

        health_status = "UNKNOWN"
        health_passed = 0
        health_total = 0
        if self._last_health:
            health_status = self._last_health.get("status", "UNKNOWN")
            health_passed = self._last_health.get("passed", 0)
            health_total = self._last_health.get("total", 0)

        return {
            "title": self.TITLE,
            "safety_banner": self.SAFETY_BANNER,
            "strategies": {
                "total": len(strategies),
                "by_status": status_counts,
            },
            "decisions": {
                "outcome_distribution": decision_distribution or {},
            },
            "proposals": {
                "pending_count": len(pending_proposals or []),
                "pending": pending_proposals or [],
            },
            "health": {
                "status": health_status,
                "passed": health_passed,
                "total": health_total,
            },
            "paper_only": True,
            "research_only": True,
            "not_investment_advice": True,
        }

    def render_health_only(self) -> Dict[str, Any]:
        """Render just the health check section."""
        try:
            from paper_trading.strategy.health_v162 import (
                PaperStrategyOrchestrationHealthCheck
            )
            result = PaperStrategyOrchestrationHealthCheck().run()
            self._last_health = result
        except Exception as exc:
            result = {
                "status": "ERROR",
                "passed": 0,
                "failed": 1,
                "total": 1,
                "error": str(exc),
            }
        return {
            "title": self.TITLE,
            "safety_banner": self.SAFETY_BANNER,
            "health": result,
            "paper_only": True,
            "research_only": True,
        }

    def format_text_summary(
        self,
        registry_summary: Optional[List[Dict]] = None,
        decision_distribution: Optional[Dict[str, int]] = None,
        pending_proposals: Optional[List[Dict]] = None,
        health_result: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Return a text-formatted summary string for CLI display."""
        data = self.render(
            registry_summary=registry_summary,
            decision_distribution=decision_distribution,
            pending_proposals=pending_proposals,
            health_result=health_result,
        )
        lines = [
            "=" * 70,
            f"  {data['title']}",
            "=" * 70,
            data["safety_banner"],
            "-" * 70,
            f"Strategies: {data['strategies']['total']} total",
        ]
        for status, count in data["strategies"]["by_status"].items():
            lines.append(f"  {status}: {count}")
        lines.append(f"Pending Proposals: {data['proposals']['pending_count']}")
        lines.append(f"Health: {data['health']['status']} "
                     f"({data['health']['passed']}/{data['health']['total']} checks)")
        lines.append("=" * 70)
        return "\n".join(lines)
