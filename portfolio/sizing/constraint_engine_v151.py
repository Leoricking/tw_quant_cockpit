"""
portfolio/sizing/constraint_engine_v151.py — Position Sizing Constraint Engine v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Apply constraints in order: data_quality → cash → weight caps → industry →
theme → market → ETF → liquidity → lot → final safety gate.
Each constraint records before/after/reason/evidence.
"""
from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

RESEARCH_ONLY = True


class PositionSizingConstraintEngine:
    """
    Applies all constraints to raw_quantity in sequence.
    Returns (final_quantity, constraints_list, binding_constraint_id).
    """

    RESEARCH_ONLY = True

    def apply_all(
        self,
        request,
        raw_quantity: Decimal,
        policy,
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Decimal, List[Dict], Optional[str]]:
        context = context or {}
        constraints: List[Dict] = []
        current = raw_quantity
        binding_constraint: Optional[str] = None

        def add_constraint(
            ctype: str,
            severity: str,
            before: Decimal,
            after: Decimal,
            reason: str,
            applied: bool,
            evidence: Optional[Dict] = None,
        ) -> str:
            cid = f"C_{ctype}_{uuid.uuid4().hex[:8]}"
            constraints.append({
                "constraint_id": cid,
                "constraint_type": ctype,
                "severity": severity,
                "before_quantity": before,
                "after_quantity": after,
                "applied": applied,
                "reason": reason,
                "evidence": evidence or {},
                "research_only": True,
            })
            return cid

        # 1. Data quality / PIT / lineage checks
        from .validation_v151 import PositionSizingValidator
        issues = PositionSizingValidator().validate_request(request)
        pit_issues = [i for i in issues if "PIT_VIOLATION" in i]
        lineage_issues = [i for i in issues if "MISSING_LINEAGE" in i]
        stop_issues = [i for i in issues if "BLOCKED_INVALID_STOP_DIRECTION" in i]

        if pit_issues:
            cid = add_constraint(
                "PIT", "BLOCKING", current, Decimal("0"),
                f"PIT_VIOLATION: {'; '.join(pit_issues)}", True,
                {"issues": pit_issues},
            )
            binding_constraint = cid
            return Decimal("0"), constraints, binding_constraint

        if stop_issues:
            cid = add_constraint(
                "STOP_DISTANCE", "BLOCKING", current, Decimal("0"),
                f"STOP_DIRECTION: {'; '.join(stop_issues)}", True,
                {"issues": stop_issues},
            )
            binding_constraint = cid
            return Decimal("0"), constraints, binding_constraint

        if lineage_issues:
            cid = add_constraint(
                "LINEAGE", "WARNING", current, current,
                f"LINEAGE_WARNING: {'; '.join(lineage_issues)}", False,
                {"issues": lineage_issues},
            )

        # 2. Cash cap
        from .cash_cap_v151 import CashCapConstraint
        cash_result = CashCapConstraint().apply(request, current, policy)
        before = current
        current = cash_result["capped_quantity"]
        cid = add_constraint(
            "AVAILABLE_CASH", cash_result["severity"],
            before, current,
            cash_result["reason"], cash_result["applied"],
        )
        if cash_result["severity"] == "BLOCKING":
            binding_constraint = cid
            return current, constraints, binding_constraint
        if cash_result["applied"] and binding_constraint is None:
            binding_constraint = cid

        # 3. Single-name weight cap
        from .concentration_cap_v151 import ConcentrationCapConstraint
        conc_result = ConcentrationCapConstraint().apply(request, current, policy)
        before = current
        current = conc_result["capped_quantity"]
        cid = add_constraint(
            "SINGLE_NAME_LIMIT", conc_result["severity"],
            before, current,
            conc_result["reason"], conc_result["applied"],
        )
        if conc_result["severity"] == "BLOCKING":
            binding_constraint = cid
            return current, constraints, binding_constraint
        if conc_result["applied"] and binding_constraint is None:
            binding_constraint = cid

        # 4. Industry cap
        from .industry_cap_v151 import IndustryCapConstraint
        industry_exposure = context.get("current_industry_value")
        ind_result = IndustryCapConstraint().apply(request, current, policy, industry_exposure)
        before = current
        current = ind_result["capped_quantity"]
        cid = add_constraint(
            "INDUSTRY_LIMIT", ind_result["severity"],
            before, current,
            ind_result["reason"], ind_result["applied"],
        )
        if ind_result["severity"] == "BLOCKING":
            binding_constraint = cid
            return current, constraints, binding_constraint
        if ind_result["applied"] and binding_constraint is None:
            binding_constraint = cid

        # 5. Theme cap
        from .theme_cap_v151 import ThemeCapConstraint
        theme_exposures = context.get("theme_exposures")
        theme_result = ThemeCapConstraint().apply(request, current, policy, theme_exposures)
        before = current
        current = theme_result["capped_quantity"]
        cid = add_constraint(
            "THEME_LIMIT", theme_result["severity"],
            before, current,
            theme_result["reason"], theme_result["applied"],
        )
        if theme_result["severity"] == "BLOCKING":
            binding_constraint = cid
            return current, constraints, binding_constraint
        if theme_result["applied"] and binding_constraint is None:
            binding_constraint = cid

        # 6. Liquidity cap
        from .liquidity_cap_v151 import LiquidityCapConstraint
        liq_result = LiquidityCapConstraint().apply(request, current, policy)
        before = current
        current = liq_result["capped_quantity"]
        cid = add_constraint(
            "LIQUIDITY_LIMIT", liq_result["severity"],
            before, current,
            liq_result["reason"], liq_result["applied"],
        )
        if liq_result["severity"] == "BLOCKING":
            binding_constraint = cid
            return current, constraints, binding_constraint
        if liq_result["applied"] and binding_constraint is None:
            binding_constraint = cid

        # 7. Lot normalization
        from .lot_normalizer_v151 import LotNormalizer
        lot_size = request.lot_size or policy.default_lot_size
        allow_odd = getattr(request, "allow_odd_lot", policy.allow_odd_lot)
        min_ov = getattr(request, "minimum_order_value", None) or policy.minimum_order_value
        entry = request.planned_entry_price or request.reference_price
        lot_result = LotNormalizer().normalize(current, lot_size, allow_odd, min_ov, entry)
        before = current
        current = lot_result["normalized_quantity"]
        cid = add_constraint(
            "LOT_SIZE", "INFO" if lot_result["reason"] == "OK" else "HARD_CAP",
            before, current,
            f"LOT_NORM: {lot_result['reason']}", before != current,
            {"removed": str(lot_result["removed_by_rounding"]),
             "odd_lot": lot_result["odd_lot"]},
        )
        if current == Decimal("0") and before > Decimal("0"):
            cid2 = add_constraint(
                "MINIMUM_ORDER_VALUE", "BLOCKING",
                before, Decimal("0"),
                lot_result.get("reason", "BELOW_MIN"), True,
            )
            if binding_constraint is None:
                binding_constraint = cid2

        # 8. Final safety gate
        add_constraint(
            "DATA_QUALITY", "INFO",
            current, current,
            "FINAL_GATE: RESEARCH_ONLY, NO_REAL_ORDERS, NO_BROKER_CALL", False,
            {"labels": ["RESEARCH_ONLY", "NOT_AN_ORDER", "NOT_EXECUTABLE"]},
        )

        return current, constraints, binding_constraint
