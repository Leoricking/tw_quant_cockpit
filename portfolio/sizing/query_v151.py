"""
portfolio/sizing/query_v151.py — Position Sizing Query Service v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] NO submit_order, NO execute_order, NO sync_broker, NO apply_to_portfolio.
"""
from __future__ import annotations

import uuid
import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True

# Blocked methods — safety
_BLOCKED_METHODS = [
    "submit_order", "execute_order", "sync_broker",
    "apply_to_portfolio", "auto_rebalance",
]


class PositionSizingQueryService:
    """
    High-level query service for position sizing operations.
    All methods return research-only results with safety labels.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    BROKER_EXECUTION_ENABLED = False

    def __init__(self, store=None):
        from .store_v151 import PositionSizingStore
        self._store = store or PositionSizingStore(use_temp_db=True)

    # -----------------------------------------------------------------------
    # Policy methods
    # -----------------------------------------------------------------------

    def create_sizing_policy(self, policy) -> str:
        return self._store.save_policy(policy)

    def get_sizing_policy(self, policy_id: str) -> Optional[Dict]:
        return self._store.get_policy(policy_id)

    def list_sizing_policies(self) -> List[Dict]:
        return self._store.list_policies()

    # -----------------------------------------------------------------------
    # Eligibility
    # -----------------------------------------------------------------------

    def evaluate_sizing_eligibility(self, request, policy):
        from .eligibility_v151 import PositionSizingEligibilityGate
        return PositionSizingEligibilityGate().evaluate(request, policy)

    # -----------------------------------------------------------------------
    # Sizing methods
    # -----------------------------------------------------------------------

    def size_fixed_fractional(self, request, policy) -> Dict[str, Any]:
        from .fixed_fractional_v151 import FixedFractionalSizer
        return FixedFractionalSizer().calculate(request, policy)

    def size_by_stop_distance(self, request, policy) -> Dict[str, Any]:
        from .stop_distance_v151 import StopDistanceSizer
        return StopDistanceSizer().calculate(request, policy)

    def size_by_atr(self, request, policy) -> Dict[str, Any]:
        from .atr_sizing_v151 import ATRSizer
        return ATRSizer().calculate(request, policy)

    def size_by_volatility_target(self, request, policy) -> Dict[str, Any]:
        from .volatility_target_v151 import VolatilityTargetSizer
        return VolatilityTargetSizer().calculate(request, policy)

    def size_by_target_weight(self, request, policy) -> Dict[str, Any]:
        """Fixed portfolio weight sizing."""
        entry = request.planned_entry_price or request.reference_price
        pv = request.portfolio_value
        tw = request.target_weight
        if tw is None:
            return {"raw_quantity": Decimal("0"), "blocked": True,
                    "blocker_reason": "MISSING_TARGET_WEIGHT", "research_only": True,
                    "method": "FIXED_PORTFOLIO_WEIGHT"}
        if entry is None or entry <= Decimal("0"):
            return {"raw_quantity": Decimal("0"), "blocked": True,
                    "blocker_reason": "MISSING_ENTRY_PRICE", "research_only": True,
                    "method": "FIXED_PORTFOLIO_WEIGHT"}
        if pv is None or pv <= Decimal("0"):
            return {"raw_quantity": Decimal("0"), "blocked": True,
                    "blocker_reason": "MISSING_PORTFOLIO_VALUE", "research_only": True,
                    "method": "FIXED_PORTFOLIO_WEIGHT"}
        target_value = pv * tw
        raw_qty = (target_value / entry).quantize(Decimal("1"), rounding="ROUND_DOWN")
        return {"raw_quantity": raw_qty, "target_weight": tw, "target_value": target_value,
                "blocked": False, "blocker_reason": "", "research_only": True,
                "method": "FIXED_PORTFOLIO_WEIGHT"}

    def size_by_cash_limit(self, request, policy) -> Dict[str, Any]:
        """Cash-limited sizing: max quantity given available cash."""
        entry = request.planned_entry_price or request.reference_price
        cash = request.available_cash
        reserve_pct = policy.minimum_cash_reserve_percent
        pv = request.portfolio_value
        if cash is None:
            return {"raw_quantity": Decimal("0"), "blocked": True,
                    "blocker_reason": "MISSING_CASH", "research_only": True,
                    "method": "CASH_LIMITED"}
        if entry is None or entry <= Decimal("0"):
            return {"raw_quantity": Decimal("0"), "blocked": True,
                    "blocker_reason": "MISSING_ENTRY_PRICE", "research_only": True,
                    "method": "CASH_LIMITED"}
        reserve = (pv * reserve_pct) if pv else Decimal("0")
        spendable = cash - reserve
        if spendable <= Decimal("0"):
            return {"raw_quantity": Decimal("0"), "blocked": True,
                    "blocker_reason": "INSUFFICIENT_CASH", "research_only": True,
                    "method": "CASH_LIMITED"}
        raw_qty = (spendable / entry).quantize(Decimal("1"), rounding="ROUND_DOWN")
        return {"raw_quantity": raw_qty, "spendable_cash": spendable,
                "blocked": False, "blocker_reason": "", "research_only": True,
                "method": "CASH_LIMITED"}

    # -----------------------------------------------------------------------
    # Constraints & Lot normalization
    # -----------------------------------------------------------------------

    def apply_constraints(self, request, raw_quantity: Decimal, policy, context=None):
        from .constraint_engine_v151 import PositionSizingConstraintEngine
        return PositionSizingConstraintEngine().apply_all(request, raw_quantity, policy, context)

    def normalize_lot_size(self, raw_quantity: Decimal, lot_size: int, allow_odd_lot: bool,
                           minimum_order_value, reference_price) -> Dict[str, Any]:
        from .lot_normalizer_v151 import LotNormalizer
        return LotNormalizer().normalize(
            raw_quantity, lot_size, allow_odd_lot, minimum_order_value, reference_price
        )

    # -----------------------------------------------------------------------
    # Build proposal (main entry point)
    # -----------------------------------------------------------------------

    def build_sizing_proposal(self, request, policy):
        from .models_v151 import PositionSizingProposal
        from .eligibility_v151 import PositionSizingEligibilityGate

        method = request.method

        # Compute raw quantity
        raw_result = self._dispatch_sizer(request, policy, method)
        raw_qty = raw_result.get("raw_quantity", Decimal("0"))
        blocked = raw_result.get("blocked", False)
        blocker_reason = raw_result.get("blocker_reason", "")

        if blocked:
            proposal = PositionSizingProposal(
                proposal_id=f"PSP_{uuid.uuid4().hex[:12]}",
                request_id=request.request_id,
                portfolio_id=request.portfolio_id,
                symbol=request.symbol,
                method=method,
                as_of=request.as_of,
                reference_price=request.planned_entry_price or request.reference_price,
                raw_quantity=Decimal("0"),
                capped_quantity=Decimal("0"),
                normalized_quantity=Decimal("0"),
                proposed_final_quantity=Decimal("0"),
                sizing_status="BLOCKED",
                blockers=[blocker_reason],
            )
            return proposal

        # Apply constraints
        final_qty, constraints, binding = self.apply_constraints(request, raw_qty, policy)

        # Compute incremental and values
        entry = request.planned_entry_price or request.reference_price or Decimal("0")
        incremental = final_qty - (request.current_quantity or Decimal("0"))
        est_value = final_qty * entry if entry > Decimal("0") else Decimal("0")
        pv = request.portfolio_value or Decimal("0")
        est_weight = (est_value / pv) if pv > Decimal("0") else Decimal("0")

        stop = request.stop_price
        stop_distance = (entry - stop) if (stop is not None and entry > Decimal("0")) else Decimal("0")
        stop_dist_pct = (stop_distance / entry) if (entry > Decimal("0") and stop_distance > Decimal("0")) else Decimal("0")

        rp = getattr(request, "risk_budget_percent", None) or policy.risk_per_trade_percent
        risk_amount = pv * rp if pv > Decimal("0") else Decimal("0")
        risk_pct = rp

        status = "VALID"
        if binding:
            status = "CAPPED"
        if final_qty == Decimal("0") and raw_qty > Decimal("0"):
            status = "BLOCKED"

        eligibility_result = PositionSizingEligibilityGate().evaluate(request, policy)

        proposal = PositionSizingProposal(
            proposal_id=f"PSP_{uuid.uuid4().hex[:12]}",
            request_id=request.request_id,
            portfolio_id=request.portfolio_id,
            symbol=request.symbol,
            method=method,
            as_of=request.as_of,
            reference_price=entry if entry > Decimal("0") else None,
            raw_quantity=raw_qty,
            capped_quantity=final_qty,
            normalized_quantity=final_qty,
            current_quantity=request.current_quantity or Decimal("0"),
            proposed_final_quantity=final_qty,
            incremental_quantity=incremental,
            estimated_position_value=est_value,
            estimated_final_weight=est_weight,
            risk_amount=risk_amount,
            risk_percent=risk_pct,
            stop_distance=stop_distance,
            stop_distance_percent=stop_dist_pct,
            constraints=constraints,
            binding_constraint=binding,
            sizing_status=status,
            eligibility={
                "sizing_allowed": eligibility_result.sizing_allowed,
                "eligibility_status": eligibility_result.eligibility_status,
                "warnings": eligibility_result.warnings,
                "blockers": eligibility_result.blockers,
            },
            warnings=eligibility_result.warnings,
            blockers=eligibility_result.blockers,
            source_lineage_ids=request.source_lineage_ids,
        )
        return proposal

    def _dispatch_sizer(self, request, policy, method: str) -> Dict[str, Any]:
        if method == "FIXED_FRACTIONAL":
            return self.size_fixed_fractional(request, policy)
        elif method == "STOP_DISTANCE":
            return self.size_by_stop_distance(request, policy)
        elif method == "ATR_BASED":
            return self.size_by_atr(request, policy)
        elif method == "VOLATILITY_TARGET":
            return self.size_by_volatility_target(request, policy)
        elif method == "FIXED_PORTFOLIO_WEIGHT":
            return self.size_by_target_weight(request, policy)
        elif method == "CASH_LIMITED":
            return self.size_by_cash_limit(request, policy)
        else:  # MANUAL_RESEARCH or unknown
            return {"raw_quantity": Decimal("0"), "blocked": False,
                    "blocker_reason": "", "research_only": True, "method": method}

    # -----------------------------------------------------------------------
    # Explainability
    # -----------------------------------------------------------------------

    def explain_sizing_proposal(self, proposal) -> Dict[str, Any]:
        from .explain_v151 import PositionSizingExplainer
        return PositionSizingExplainer().explain(proposal)

    # -----------------------------------------------------------------------
    # What-if
    # -----------------------------------------------------------------------

    def run_sizing_what_if(self, baseline_request, scenario_overrides, policy):
        from .what_if_v151 import SizingWhatIfEngine
        return SizingWhatIfEngine().run(baseline_request, scenario_overrides, policy)

    # -----------------------------------------------------------------------
    # Persistence (research store only)
    # -----------------------------------------------------------------------

    def save_sizing_proposal(self, proposal) -> str:
        return self._store.save_proposal(proposal)

    def get_sizing_proposal(self, proposal_id: str) -> Optional[Dict]:
        return self._store.get_proposal(proposal_id)

    def list_sizing_proposals(self, portfolio_id: Optional[str] = None) -> List[Dict]:
        return self._store.list_proposals(portfolio_id)

    def get_sizing_lineage(self, proposal_id: str) -> Dict[str, Any]:
        p = self._store.get_proposal(proposal_id)
        if p is None:
            return {"proposal_id": proposal_id, "lineage_ids": [], "found": False}
        lineage = p.get("source_lineage_ids", []) if isinstance(p, dict) else getattr(p, "source_lineage_ids", [])
        return {"proposal_id": proposal_id, "lineage_ids": lineage, "found": True}
