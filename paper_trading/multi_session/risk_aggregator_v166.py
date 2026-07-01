"""
paper_trading/multi_session/risk_aggregator_v166.py — Risk Aggregator v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No automatic risk limit modification. Output only: PASS/WARN/BLOCK/DEGRADE/REQUIRE_REVIEW.
"""
from __future__ import annotations
from typing import Any, Dict, List
from paper_trading.multi_session.enums_v166 import CoordinationOutcome
from paper_trading.multi_session.models_v166 import SessionDescriptor

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_AUTO_RISK_MODIFICATION = True


class RiskAggregator:
    """Aggregates cross-session risk. Paper budgets only. No real limits."""

    def aggregate(
        self,
        sessions: List[SessionDescriptor],
        rules: Dict[str, Any],
    ) -> Dict[str, Any]:
        total_risk = sum(s.risk_budget for s in sessions)
        total_capital = sum(s.capital_budget for s in sessions)
        session_risks = {s.session_id: s.risk_budget for s in sessions}

        gross_limit = rules.get("aggregate_gross_limit", 1.0) * 100
        concentration_limit = rules.get("concentration_limit", 0.3)

        outcome = CoordinationOutcome.PASS
        warnings: List[str] = []

        if total_risk > gross_limit:
            outcome = CoordinationOutcome.BLOCK
            warnings.append(f"Aggregate gross risk {total_risk:.1f} exceeds limit {gross_limit:.1f}")
        elif total_risk > gross_limit * 0.8:
            if outcome == CoordinationOutcome.PASS:
                outcome = CoordinationOutcome.WARN
            warnings.append(f"Aggregate risk {total_risk:.1f} approaching limit")

        # Concentration check
        for sid, risk in session_risks.items():
            if total_risk > 0 and risk / total_risk > concentration_limit:
                if outcome == CoordinationOutcome.PASS:
                    outcome = CoordinationOutcome.WARN
                warnings.append(f"Session {sid} concentration {risk/total_risk:.1%} exceeds {concentration_limit:.1%}")

        return {
            "outcome": outcome.value,
            "total_risk_budget": total_risk,
            "total_capital_budget": total_capital,
            "session_risks": session_risks,
            "warnings": warnings,
            "gross_limit": gross_limit,
            "concentration_limit": concentration_limit,
        }
