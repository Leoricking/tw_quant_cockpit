"""
release/position_sizing_release_gate_v151.py — Position Sizing Release Gate v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
22 gate checks.
"""
from __future__ import annotations

from typing import Any, Dict, List

RESEARCH_ONLY = True
GATE_VERSION = "1.5.1"


class PositionSizingReleaseGate:
    """
    22-check release gate for Position Sizing v1.5.1.
    """

    RESEARCH_ONLY = True

    def run(self) -> Dict[str, Any]:
        results: List[Dict] = []
        passed_count = 0
        failed_count = 0

        def check(name: str, fn) -> bool:
            nonlocal passed_count, failed_count
            try:
                ok, detail = fn()
            except Exception as e:
                ok, detail = False, str(e)
            results.append({"check": name, "passed": ok, "detail": detail})
            if ok:
                passed_count += 1
            else:
                failed_count += 1
            return ok

        # 1. POSITION_SIZING_MODELS_VALID
        def _models():
            from portfolio.sizing.models_v151 import (
                PositionSizingRequest, PositionSizingProposal, PositionSizingPolicy
            )
            from decimal import Decimal
            p = PositionSizingPolicy(policy_id="G1", name="Gate")
            assert p.full_kelly_enabled is False
            return True, "models valid"
        check("POSITION_SIZING_MODELS_VALID", _models)

        # 2. POSITION_SIZING_POLICY_VALID
        def _policy():
            from portfolio.sizing.models_v151 import PositionSizingPolicy
            from decimal import Decimal
            p = PositionSizingPolicy(
                policy_id="G2", name="Gate",
                risk_per_trade_percent=Decimal("0.01"),
                max_single_position_weight=Decimal("0.15"),
            )
            assert p.leverage_enabled is False
            assert p.short_enabled is False
            return True, "policy valid"
        check("POSITION_SIZING_POLICY_VALID", _policy)

        # 3. FIXED_FRACTIONAL_VALID
        def _ff():
            from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            from decimal import Decimal
            req = PositionSizingRequest(
                request_id="G3", portfolio_id="P", account_id="A",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="FIXED_FRACTIONAL",
                portfolio_value=Decimal("1000000"),
                planned_entry_price=Decimal("1000"),
                stop_price=Decimal("950"),
                source_lineage_ids=["L1"],
            )
            pol = PositionSizingPolicy(policy_id="G", name="Test")
            r = FixedFractionalSizer().calculate(req, pol)
            assert not r["blocked"]
            assert r["raw_quantity"] > Decimal("0")
            return True, f"ff qty={r['raw_quantity']}"
        check("FIXED_FRACTIONAL_VALID", _ff)

        # 4. STOP_DISTANCE_VALID
        def _sd():
            from portfolio.sizing.stop_distance_v151 import StopDistanceSizer
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            from decimal import Decimal
            req = PositionSizingRequest(
                request_id="G4", portfolio_id="P", account_id="A",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="STOP_DISTANCE",
                portfolio_value=Decimal("1000000"),
                planned_entry_price=Decimal("500"),
                stop_price=Decimal("475"),
                source_lineage_ids=["L1"],
            )
            pol = PositionSizingPolicy(policy_id="G", name="Test")
            r = StopDistanceSizer().calculate(req, pol)
            assert not r["blocked"]
            return True, "stop_distance valid"
        check("STOP_DISTANCE_VALID", _sd)

        # 5. ATR_SIZING_VALID
        def _atr():
            from portfolio.sizing.atr_sizing_v151 import ATRSizer
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            from decimal import Decimal
            req = PositionSizingRequest(
                request_id="G5", portfolio_id="P", account_id="A",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="ATR_BASED", atr=Decimal("25"),
                portfolio_value=Decimal("1000000"),
                planned_entry_price=Decimal("500"),
                source_lineage_ids=["L1"],
            )
            pol = PositionSizingPolicy(policy_id="G", name="Test")
            r = ATRSizer().calculate(req, pol)
            assert not r["blocked"]
            return True, "atr valid"
        check("ATR_SIZING_VALID", _atr)

        # 6. VOLATILITY_SIZING_VALID
        def _vol():
            from portfolio.sizing.volatility_target_v151 import VolatilityTargetSizer
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            from decimal import Decimal
            req = PositionSizingRequest(
                request_id="G6", portfolio_id="P", account_id="A",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="VOLATILITY_TARGET", volatility=Decimal("0.25"),
                portfolio_value=Decimal("1000000"),
                planned_entry_price=Decimal("500"),
                source_lineage_ids=["L1"],
            )
            pol = PositionSizingPolicy(policy_id="G", name="Test")
            r = VolatilityTargetSizer().calculate(req, pol)
            assert not r["blocked"]
            return True, "vol_target valid"
        check("VOLATILITY_SIZING_VALID", _vol)

        # 7. TARGET_WEIGHT_VALID
        def _tw():
            from portfolio.sizing.query_v151 import PositionSizingQueryService
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            from decimal import Decimal
            req = PositionSizingRequest(
                request_id="G7", portfolio_id="P", account_id="A",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="FIXED_PORTFOLIO_WEIGHT",
                target_weight=Decimal("0.10"),
                portfolio_value=Decimal("1000000"),
                planned_entry_price=Decimal("500"),
                source_lineage_ids=["L1"],
            )
            pol = PositionSizingPolicy(policy_id="G", name="Test")
            r = PositionSizingQueryService().size_by_target_weight(req, pol)
            assert not r["blocked"]
            return True, "target_weight valid"
        check("TARGET_WEIGHT_VALID", _tw)

        # 8. CASH_LIMIT_VALID
        def _cash():
            from portfolio.sizing.query_v151 import PositionSizingQueryService
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            from decimal import Decimal
            req = PositionSizingRequest(
                request_id="G8", portfolio_id="P", account_id="A",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="CASH_LIMITED",
                available_cash=Decimal("200000"),
                portfolio_value=Decimal("1000000"),
                planned_entry_price=Decimal("500"),
                source_lineage_ids=["L1"],
            )
            pol = PositionSizingPolicy(policy_id="G", name="Test")
            r = PositionSizingQueryService().size_by_cash_limit(req, pol)
            assert not r["blocked"]
            return True, "cash_limit valid"
        check("CASH_LIMIT_VALID", _cash)

        # 9. POSITION_CONSTRAINTS_VALID
        def _constr():
            from portfolio.sizing.constraint_engine_v151 import PositionSizingConstraintEngine
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            from decimal import Decimal
            req = PositionSizingRequest(
                request_id="G9", portfolio_id="P", account_id="A",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="FIXED_FRACTIONAL",
                portfolio_value=Decimal("1000000"),
                available_cash=Decimal("200000"),
                planned_entry_price=Decimal("500"),
                stop_price=Decimal("475"),
                source_lineage_ids=["L1"],
            )
            pol = PositionSizingPolicy(policy_id="G", name="Test")
            fq, cs, bc = PositionSizingConstraintEngine().apply_all(req, Decimal("400"), pol)
            assert fq >= Decimal("0")
            return True, f"constraints applied, final={fq}"
        check("POSITION_CONSTRAINTS_VALID", _constr)

        # 10. LIQUIDITY_CAP_VALID
        def _liq():
            from portfolio.sizing.liquidity_cap_v151 import LiquidityCapConstraint
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            from decimal import Decimal
            req = PositionSizingRequest(
                request_id="G10", portfolio_id="P", account_id="A",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="FIXED_FRACTIONAL",
                average_daily_value=Decimal("5000000"),
                planned_entry_price=Decimal("500"),
                source_lineage_ids=["L1"],
            )
            pol = PositionSizingPolicy(policy_id="G", name="Test")
            r = LiquidityCapConstraint().apply(req, Decimal("2000"), pol)
            return True, f"liquidity cap: {r['reason']}"
        check("LIQUIDITY_CAP_VALID", _liq)

        # 11. LOT_NORMALIZATION_VALID
        def _lot():
            from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
            from decimal import Decimal
            r = LotNormalizer().normalize(Decimal("1500"), 1000, False, None, None)
            assert r["normalized_quantity"] == Decimal("1000")
            return True, "lot normalization valid"
        check("LOT_NORMALIZATION_VALID", _lot)

        # 12. POSITION_SIZING_ELIGIBILITY_VALID
        def _elig():
            from portfolio.sizing.eligibility_v151 import PositionSizingEligibilityGate
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            from decimal import Decimal
            req = PositionSizingRequest(
                request_id="G12", portfolio_id="P", account_id="A",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="FIXED_FRACTIONAL",
                portfolio_value=Decimal("1000000"),
                planned_entry_price=Decimal("500"),
                source_lineage_ids=["L1"],
            )
            pol = PositionSizingPolicy(policy_id="G", name="Test")
            r = PositionSizingEligibilityGate().evaluate(req, pol)
            return True, f"eligibility: {r.eligibility_status}"
        check("POSITION_SIZING_ELIGIBILITY_VALID", _elig)

        # 13. POSITION_SIZING_PIT_VALID
        def _pit():
            from portfolio.sizing.atr_sizing_v151 import ATRSizer
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            from decimal import Decimal
            req = PositionSizingRequest(
                request_id="G13", portfolio_id="P", account_id="A",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-20", available_from="2026-06-20",
                method="ATR_BASED", atr=Decimal("25"),
                atr_available_from="2026-06-22",  # future → PIT violation
                portfolio_value=Decimal("1000000"),
                planned_entry_price=Decimal("500"),
                source_lineage_ids=["L1"],
            )
            pol = PositionSizingPolicy(policy_id="G", name="Test")
            r = ATRSizer().calculate(req, pol)
            assert r["blocked"] is True
            assert "PIT_VIOLATION" in r["blocker_reason"]
            return True, "PIT violation correctly blocked"
        check("POSITION_SIZING_PIT_VALID", _pit)

        # 14. POSITION_SIZING_LINEAGE_VALID
        def _lin():
            from portfolio.sizing.validation_v151 import PositionSizingValidator
            from portfolio.sizing.models_v151 import PositionSizingRequest
            req = PositionSizingRequest(
                request_id="G14", portfolio_id="P", account_id="A",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="FIXED_FRACTIONAL",
                source_lineage_ids=[],  # empty → lineage issue
            )
            issues = PositionSizingValidator().validate_request(req)
            lin_issues = [i for i in issues if "LINEAGE" in i]
            assert len(lin_issues) > 0
            return True, "lineage validation works"
        check("POSITION_SIZING_LINEAGE_VALID", _lin)

        # 15. POSITION_SIZING_EXPLAINABILITY_VALID
        def _explain():
            from portfolio.sizing.explain_v151 import PositionSizingExplainer
            from portfolio.sizing.models_v151 import PositionSizingProposal
            prop = PositionSizingProposal(
                proposal_id="G15", request_id="R15",
                portfolio_id="P", symbol="2330",
                method="FIXED_FRACTIONAL", as_of="2026-06-22",
            )
            r = PositionSizingExplainer().explain(prop)
            assert "steps" in r
            assert r["research_only"] is True
            return True, "explainability valid"
        check("POSITION_SIZING_EXPLAINABILITY_VALID", _explain)

        # 16. POSITION_SIZING_WHAT_IF_SAFE
        def _whatif():
            from portfolio.sizing.what_if_v151 import SizingWhatIfEngine, WHAT_IF_LABELS
            assert "HYPOTHETICAL_ONLY" in WHAT_IF_LABELS
            assert "NO_LEDGER_WRITE" in WHAT_IF_LABELS
            assert "NO_ORDER_CREATED" in WHAT_IF_LABELS
            eng = SizingWhatIfEngine()
            assert eng.RESEARCH_ONLY is True
            assert eng.NO_LEDGER_WRITE is True
            assert eng.NO_ORDER_CREATED is True
            assert eng.NO_BROKER_CALL is True
            return True, "what-if safety confirmed"
        check("POSITION_SIZING_WHAT_IF_SAFE", _whatif)

        # 17. NO_POSITION_SIZING_ORDER_CREATION
        def _no_create():
            from portfolio.sizing import POSITION_SIZING_ORDER_CREATION_ENABLED
            assert POSITION_SIZING_ORDER_CREATION_ENABLED is False
            return True, "order creation disabled"
        check("NO_POSITION_SIZING_ORDER_CREATION", _no_create)

        # 18. NO_POSITION_SIZING_ORDER_EXECUTION
        def _no_exec():
            from portfolio.sizing import POSITION_SIZING_ORDER_EXECUTION_ENABLED
            assert POSITION_SIZING_ORDER_EXECUTION_ENABLED is False
            return True, "order execution disabled"
        check("NO_POSITION_SIZING_ORDER_EXECUTION", _no_exec)

        # 19. NO_POSITION_SIZING_BROKER
        def _no_broker():
            from portfolio.sizing import POSITION_SIZING_BROKER_ENABLED
            assert POSITION_SIZING_BROKER_ENABLED is False
            return True, "broker disabled"
        check("NO_POSITION_SIZING_BROKER", _no_broker)

        # 20. NO_POSITION_SIZING_LEDGER_WRITE
        def _no_ledger():
            from portfolio.sizing.store_v151 import PositionSizingStore
            assert PositionSizingStore.RESEARCH_ONLY is True
            # No order table
            assert not hasattr(PositionSizingStore, "_orders")
            return True, "no ledger write"
        check("NO_POSITION_SIZING_LEDGER_WRITE", _no_ledger)

        # 21. NO_POSITION_SIZING_AUTO_APPLY
        def _no_apply():
            from portfolio.sizing import POSITION_SIZING_AUTO_APPLY_ENABLED
            assert POSITION_SIZING_AUTO_APPLY_ENABLED is False
            from portfolio.sizing.query_v151 import PositionSizingQueryService
            svc = PositionSizingQueryService()
            assert not hasattr(svc, "apply_to_portfolio")
            assert not hasattr(svc, "submit_order")
            return True, "no auto apply"
        check("NO_POSITION_SIZING_AUTO_APPLY", _no_apply)

        # 22. NO_POSITION_SIZING_AUTO_REBALANCE
        def _no_rebalance():
            from portfolio.sizing import POSITION_SIZING_AUTO_REBALANCE_ENABLED
            assert POSITION_SIZING_AUTO_REBALANCE_ENABLED is False
            from portfolio.sizing.query_v151 import PositionSizingQueryService
            svc = PositionSizingQueryService()
            assert not hasattr(svc, "auto_rebalance")
            return True, "no auto rebalance"
        check("NO_POSITION_SIZING_AUTO_REBALANCE", _no_rebalance)

        gate_passed = failed_count == 0
        return {
            "gate_passed": gate_passed,
            "status": "PASS" if gate_passed else "FAIL",
            "version": GATE_VERSION,
            "passed": passed_count,
            "failed": failed_count,
            "total": len(results),
            "checks": results,
            "research_only": True,
        }
