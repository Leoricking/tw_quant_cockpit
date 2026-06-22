"""
reports/position_sizing_report.py — Position Sizing Report v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Runtime reports not committed (gitignored).
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

RESEARCH_ONLY = True
REPORT_VERSION = "1.5.1"


class PositionSizingReport:
    """
    Generates comprehensive position sizing research reports.
    Sections: context, inputs, calculation, constraints, final_proposal,
              data_quality, explainability, safety.
    """

    RESEARCH_ONLY = True
    REPORT_VERSION = REPORT_VERSION

    def generate(
        self,
        portfolio_id: str,
        symbol: str,
        as_of: str,
        request=None,
        policy=None,
        proposal=None,
    ) -> Dict[str, Any]:
        """
        Generate a full position sizing report.
        Returns dict with all sections.
        """
        generated_at = datetime.datetime.utcnow().isoformat()

        report = {
            "report_version": REPORT_VERSION,
            "generated_at": generated_at,
            "portfolio_id": portfolio_id,
            "symbol": symbol,
            "as_of": as_of,
            "sections": {
                "context": self._section_context(portfolio_id, symbol, as_of),
                "inputs": self._section_inputs(request, policy),
                "calculation": self._section_calculation(proposal),
                "constraints": self._section_constraints(proposal),
                "final_proposal": self._section_final_proposal(proposal),
                "data_quality": self._section_data_quality(request),
                "explainability": self._section_explainability(proposal),
                "safety": self._section_safety(),
            },
            "research_only": True,
            "executable": False,
            "order_created": False,
            "broker_called": False,
        }
        return report

    def _section_context(self, portfolio_id: str, symbol: str, as_of: str) -> Dict:
        return {
            "portfolio_id": portfolio_id,
            "symbol": symbol,
            "as_of": as_of,
            "report_type": "POSITION_SIZING_RESEARCH",
            "research_only": True,
        }

    def _section_inputs(self, request, policy) -> Dict:
        if request is None:
            return {"status": "NO_REQUEST_PROVIDED"}
        return {
            "request_id": getattr(request, "request_id", ""),
            "method": getattr(request, "method", ""),
            "portfolio_value": str(getattr(request, "portfolio_value", "") or ""),
            "available_cash": str(getattr(request, "available_cash", "") or ""),
            "reference_price": str(getattr(request, "reference_price", "") or ""),
            "planned_entry_price": str(getattr(request, "planned_entry_price", "") or ""),
            "stop_price": str(getattr(request, "stop_price", "") or ""),
            "atr": str(getattr(request, "atr", "") or ""),
            "volatility": str(getattr(request, "volatility", "") or ""),
            "risk_budget_percent": str(getattr(request, "risk_budget_percent", "") or ""),
            "lot_size": getattr(request, "lot_size", 1000),
            "allow_odd_lot": getattr(request, "allow_odd_lot", False),
            "policy_id": getattr(policy, "policy_id", "") if policy else "",
        }

    def _section_calculation(self, proposal) -> Dict:
        if proposal is None:
            return {"status": "NO_PROPOSAL_PROVIDED"}
        return {
            "method": getattr(proposal, "method", ""),
            "raw_quantity": str(getattr(proposal, "raw_quantity", "0")),
            "capped_quantity": str(getattr(proposal, "capped_quantity", "0")),
            "normalized_quantity": str(getattr(proposal, "normalized_quantity", "0")),
            "risk_amount": str(getattr(proposal, "risk_amount", "0")),
            "risk_percent": str(getattr(proposal, "risk_percent", "0")),
            "stop_distance": str(getattr(proposal, "stop_distance", "0")),
        }

    def _section_constraints(self, proposal) -> Dict:
        if proposal is None:
            return {"status": "NO_PROPOSAL_PROVIDED"}
        constraints = getattr(proposal, "constraints", [])
        return {
            "count": len(constraints),
            "binding_constraint": getattr(proposal, "binding_constraint", None),
            "constraints": [
                {k: str(v) if hasattr(v, "__str__") else v
                 for k, v in (c.items() if isinstance(c, dict) else vars(c).items())}
                for c in constraints
            ],
        }

    def _section_final_proposal(self, proposal) -> Dict:
        if proposal is None:
            return {"status": "NO_PROPOSAL_PROVIDED"}
        return {
            "proposal_id": getattr(proposal, "proposal_id", ""),
            "proposed_final_quantity": str(getattr(proposal, "proposed_final_quantity", "0")),
            "incremental_quantity": str(getattr(proposal, "incremental_quantity", "0")),
            "estimated_position_value": str(getattr(proposal, "estimated_position_value", "0")),
            "estimated_final_weight": str(getattr(proposal, "estimated_final_weight", "0")),
            "sizing_status": getattr(proposal, "sizing_status", ""),
            "warnings": getattr(proposal, "warnings", []),
            "blockers": getattr(proposal, "blockers", []),
            "research_only": True,
            "executable": False,
            "order_created": False,
        }

    def _section_data_quality(self, request) -> Dict:
        if request is None:
            return {"status": "NO_REQUEST_PROVIDED"}
        from portfolio.sizing.validation_v151 import PositionSizingValidator
        issues = PositionSizingValidator().validate_request(request)
        return {
            "issues_count": len(issues),
            "issues": issues,
            "lineage_ids": getattr(request, "source_lineage_ids", []),
            "as_of": getattr(request, "as_of", ""),
            "available_from": getattr(request, "available_from", ""),
        }

    def _section_explainability(self, proposal) -> Dict:
        if proposal is None:
            return {"status": "NO_PROPOSAL_PROVIDED"}
        from portfolio.sizing.explain_v151 import PositionSizingExplainer
        return PositionSizingExplainer().explain(proposal)

    def _section_safety(self) -> Dict:
        from portfolio.sizing import (
            POSITION_SIZING_RESEARCH_ONLY, POSITION_SIZING_ORDER_CREATION_ENABLED,
            POSITION_SIZING_ORDER_EXECUTION_ENABLED, POSITION_SIZING_BROKER_ENABLED,
            POSITION_SIZING_AUTO_REBALANCE_ENABLED, POSITION_SIZING_AUTO_APPLY_ENABLED,
            NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
        )
        return {
            "research_only": POSITION_SIZING_RESEARCH_ONLY,
            "order_creation_enabled": POSITION_SIZING_ORDER_CREATION_ENABLED,
            "order_execution_enabled": POSITION_SIZING_ORDER_EXECUTION_ENABLED,
            "broker_enabled": POSITION_SIZING_BROKER_ENABLED,
            "auto_rebalance_enabled": POSITION_SIZING_AUTO_REBALANCE_ENABLED,
            "auto_apply_enabled": POSITION_SIZING_AUTO_APPLY_ENABLED,
            "no_real_orders": NO_REAL_ORDERS,
            "broker_execution_enabled": BROKER_EXECUTION_ENABLED,
            "production_trading_blocked": PRODUCTION_TRADING_BLOCKED,
            "labels": [
                "RESEARCH_ONLY", "NOT_AN_ORDER", "NOT_EXECUTABLE",
                "NO_BROKER_CALL", "NO_LEDGER_WRITE", "NO_AUTO_REBALANCE",
            ],
        }
