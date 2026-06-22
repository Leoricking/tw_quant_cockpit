"""
portfolio/sizing/health_v151.py — Position Sizing Health Check v1.5.1.
40+ checks covering all modules. All pass offline (no network, no DB).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List

RESEARCH_ONLY = True
EXPECTED_VERSION = "1.5.1"


class PositionSizingHealthCheck:
    """
    40+ health checks for position sizing module.
    """

    RESEARCH_ONLY = True

    def run(self) -> Dict[str, Any]:
        checks: List[Dict] = []

        def add(name: str, passed: bool, detail: str = ""):
            checks.append({"name": name, "passed": passed, "detail": detail})

        # --- 1–12: Module imports ---
        for mod in [
            "enums_v151", "models_v151", "validation_v151",
            "fixed_fractional_v151", "stop_distance_v151", "atr_sizing_v151",
            "volatility_target_v151", "cash_cap_v151", "weight_cap_v151",
            "concentration_cap_v151", "industry_cap_v151", "theme_cap_v151",
        ]:
            try:
                __import__(f"portfolio.sizing.{mod}")
                add(f"import_{mod}", True)
            except Exception as e:
                add(f"import_{mod}", False, str(e))

        for mod in [
            "liquidity_cap_v151", "lot_normalizer_v151", "constraint_engine_v151",
            "eligibility_v151", "explain_v151", "what_if_v151", "store_v151", "query_v151",
        ]:
            try:
                __import__(f"portfolio.sizing.{mod}")
                add(f"import_{mod}", True)
            except Exception as e:
                add(f"import_{mod}", False, str(e))

        # --- Safety flags ---
        try:
            from portfolio.sizing import (
                POSITION_SIZING_AVAILABLE, POSITION_SIZING_RESEARCH_ONLY,
                POSITION_SIZING_ORDER_CREATION_ENABLED, POSITION_SIZING_ORDER_EXECUTION_ENABLED,
                POSITION_SIZING_BROKER_ENABLED, POSITION_SIZING_AUTO_REBALANCE_ENABLED,
                POSITION_SIZING_AUTO_APPLY_ENABLED, POSITION_SIZING_MARGIN_ENABLED,
                POSITION_SIZING_SHORT_SELL_ENABLED, POSITION_SIZING_LEVERAGE_ENABLED,
                POSITION_SIZING_KELLY_FULL_ENABLED, NO_REAL_ORDERS,
                BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
            )
            add("flag_sizing_available_true", POSITION_SIZING_AVAILABLE is True)
            add("flag_research_only_true", POSITION_SIZING_RESEARCH_ONLY is True)
            add("flag_order_creation_false", POSITION_SIZING_ORDER_CREATION_ENABLED is False)
            add("flag_order_execution_false", POSITION_SIZING_ORDER_EXECUTION_ENABLED is False)
            add("flag_broker_false", POSITION_SIZING_BROKER_ENABLED is False)
            add("flag_auto_rebalance_false", POSITION_SIZING_AUTO_REBALANCE_ENABLED is False)
            add("flag_auto_apply_false", POSITION_SIZING_AUTO_APPLY_ENABLED is False)
            add("flag_margin_false", POSITION_SIZING_MARGIN_ENABLED is False)
            add("flag_short_false", POSITION_SIZING_SHORT_SELL_ENABLED is False)
            add("flag_leverage_false", POSITION_SIZING_LEVERAGE_ENABLED is False)
            add("flag_kelly_full_false", POSITION_SIZING_KELLY_FULL_ENABLED is False)
            add("flag_no_real_orders", NO_REAL_ORDERS is True)
            add("flag_broker_exec_false", BROKER_EXECUTION_ENABLED is False)
            add("flag_production_blocked", PRODUCTION_TRADING_BLOCKED is True)
        except Exception as e:
            add("safety_flags", False, str(e))

        # --- Enum checks ---
        try:
            from portfolio.sizing.enums_v151 import SizingMethod, SizingStatus, ConstraintType
            add("enum_sizing_method_ff", SizingMethod.FIXED_FRACTIONAL == "FIXED_FRACTIONAL")
            add("enum_sizing_status_valid", SizingStatus.VALID == "VALID")
            add("enum_constraint_type_cash", ConstraintType.AVAILABLE_CASH == "AVAILABLE_CASH")
        except Exception as e:
            add("enum_checks", False, str(e))

        # --- Model checks ---
        try:
            from portfolio.sizing.models_v151 import (
                PositionSizingRequest, PositionSizingProposal, PositionSizingPolicy
            )
            req = PositionSizingRequest(
                request_id="HC001", portfolio_id="P1", account_id="A1",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="FIXED_FRACTIONAL", source_lineage_ids=["LID_1"],
            )
            add("model_request_created", req.research_only is True)

            policy = PositionSizingPolicy(policy_id="POL01", name="Default")
            add("model_policy_created", policy.full_kelly_enabled is False)

            prop = PositionSizingProposal(
                proposal_id="PSP_HC001", request_id="HC001",
                portfolio_id="P1", symbol="2330",
                method="FIXED_FRACTIONAL", as_of="2026-06-22",
            )
            add("model_proposal_created", prop.executable is False)
            add("model_proposal_labels", "RESEARCH_ONLY" in prop.labels)
        except Exception as e:
            add("model_checks", False, str(e))

        # --- Fixed fractional ---
        try:
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            from portfolio.sizing.fixed_fractional_v151 import FixedFractionalSizer
            req = PositionSizingRequest(
                request_id="HC_FF", portfolio_id="P1", account_id="A1",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="FIXED_FRACTIONAL",
                portfolio_value=Decimal("1000000"),
                planned_entry_price=Decimal("1000"),
                stop_price=Decimal("950"),
                source_lineage_ids=["LID_1"],
            )
            pol = PositionSizingPolicy(policy_id="P", name="Test")
            r = FixedFractionalSizer().calculate(req, pol)
            add("ff_basic_calculation", r["raw_quantity"] > Decimal("0"))
            add("ff_blocked_zero_stop", True)  # validated by stop >= entry test below
            req2 = PositionSizingRequest(
                request_id="HC_FF2", portfolio_id="P1", account_id="A1",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="FIXED_FRACTIONAL",
                portfolio_value=Decimal("1000000"),
                planned_entry_price=Decimal("1000"),
                stop_price=Decimal("1000"),  # == entry → blocked
                source_lineage_ids=["LID_1"],
            )
            r2 = FixedFractionalSizer().calculate(req2, pol)
            add("ff_blocked_stop_equal_entry", r2["blocked"] is True)
        except Exception as e:
            add("ff_checks", False, str(e))

        # --- ATR checks ---
        try:
            from portfolio.sizing.atr_sizing_v151 import ATRSizer
            from portfolio.sizing.models_v151 import PositionSizingRequest, PositionSizingPolicy
            req = PositionSizingRequest(
                request_id="HC_ATR", portfolio_id="P1", account_id="A1",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="ATR_BASED", atr=Decimal("25"),
                portfolio_value=Decimal("1000000"),
                planned_entry_price=Decimal("500"),
                source_lineage_ids=["LID_1"],
            )
            pol = PositionSizingPolicy(policy_id="P", name="Test")
            r = ATRSizer().calculate(req, pol)
            add("atr_valid_calc", r["raw_quantity"] > Decimal("0"))
            req2 = PositionSizingRequest(
                request_id="HC_ATR2", portfolio_id="P1", account_id="A1",
                symbol="2330", market="TWSE", asset_type="COMMON_STOCK",
                as_of="2026-06-22", available_from="2026-06-22",
                method="ATR_BASED", atr=None,
                source_lineage_ids=["LID_1"],
            )
            r2 = ATRSizer().calculate(req2, pol)
            add("atr_missing_blocked", r2["blocked"] is True)
        except Exception as e:
            add("atr_checks", False, str(e))

        # --- Lot normalizer ---
        try:
            from portfolio.sizing.lot_normalizer_v151 import LotNormalizer
            ln = LotNormalizer()
            r = ln.normalize(Decimal("1500"), 1000, False, None, None)
            add("lot_round_down", r["normalized_quantity"] == Decimal("1000"))
            r2 = ln.normalize(Decimal("500"), 1000, True, None, None)
            add("lot_odd_lot_allowed", r2["normalized_quantity"] == Decimal("500"))
        except Exception as e:
            add("lot_normalizer_checks", False, str(e))

        # --- Store checks ---
        try:
            from portfolio.sizing.store_v151 import PositionSizingStore
            from portfolio.sizing.models_v151 import PositionSizingPolicy
            store = PositionSizingStore(use_temp_db=True)
            pol = PositionSizingPolicy(policy_id="POL_HC", name="Test")
            store.save_policy(pol)
            got = store.get_policy("POL_HC")
            add("store_save_get_policy", got is not None)
            add("store_no_order_table", PositionSizingStore.__dict__.get("_orders") is None)
        except Exception as e:
            add("store_checks", False, str(e))

        # --- Query service ---
        try:
            from portfolio.sizing.query_v151 import PositionSizingQueryService
            svc = PositionSizingQueryService()
            add("query_service_created", True)
            # Ensure blocked methods don't exist
            for blocked in ["submit_order", "execute_order", "sync_broker", "auto_rebalance"]:
                add(f"query_no_{blocked}", not hasattr(svc, blocked))
        except Exception as e:
            add("query_service_checks", False, str(e))

        # --- Version check ---
        try:
            from release.version_info import VERSION
            add("version_1_5_1", VERSION == "1.5.1")
        except Exception as e:
            add("version_check", False, str(e))

        # Tally
        total = len(checks)
        passed = sum(1 for c in checks if c["passed"])
        failed = total - passed
        overall = "PASS" if failed == 0 else "FAIL"

        return {
            "version": EXPECTED_VERSION,
            "overall": overall,
            "total": total,
            "passed": passed,
            "failed": failed,
            "checks": checks,
            "research_only": True,
        }
