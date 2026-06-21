"""
portfolio/eligibility_v150.py — Data eligibility gate for v1.5.0.

PortfolioDataEligibilityGate: 17+ structured checks.
Returns structured output (not a boolean). Never raises on check failure.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True

_CHECK_NAMES = [
    "research_only_flag",
    "broker_linked_false",
    "real_order_disabled",
    "position_sizing_disabled",
    "auto_rebalance_disabled",
    "portfolio_id_present",
    "portfolio_name_present",
    "at_least_one_position",
    "no_negative_quantities",
    "valuation_status_not_blocked",
    "no_missing_prices",
    "cash_not_negative",
    "cost_basis_method_valid",
    "pit_dates_consistent",
    "transaction_ids_unique",
    "no_unsupported_asset_types",
    "decimal_monetary_fields",
]


class PortfolioDataEligibilityGate:
    RESEARCH_ONLY = True

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all 17+ eligibility checks against context dict.

        context keys (all optional; missing → specific check fails):
          portfolio_def, positions, cash_twd, valuation, transactions,
          ledger_flags, pit_report

        Returns:
          {
            "eligible": bool,
            "status": "ELIGIBLE" | "ELIGIBLE_WITH_WARNING" | "RESTRICTED" | "BLOCKED",
            "checks": list of {name, passed, severity, message},
            "failed_checks": list[str],
            "warning_checks": list[str],
            "research_only": True,
          }
        """
        checks: List[Dict[str, Any]] = []
        portfolio_def = context.get("portfolio_def", {}) or {}
        positions = context.get("positions", []) or []
        cash_twd = context.get("cash_twd")
        valuation = context.get("valuation", {}) or {}
        transactions = context.get("transactions", []) or []
        ledger_flags = context.get("ledger_flags", {}) or {}
        pit_report = context.get("pit_report", {}) or {}

        def add(name: str, passed: bool, severity: str, message: str):
            checks.append({"name": name, "passed": passed, "severity": severity, "message": message})

        # 1
        ro = portfolio_def.get("research_only", False)
        add("research_only_flag", bool(ro), "BLOCK", "portfolio.research_only must be True")
        # 2
        bl = portfolio_def.get("broker_linked", True)
        add("broker_linked_false", not bool(bl), "BLOCK", "portfolio.broker_linked must be False")
        # 3
        ro2 = not portfolio_def.get("real_order_enabled", True)
        add("real_order_disabled", ro2, "BLOCK", "portfolio.real_order_enabled must be False")
        # 4
        ps = not portfolio_def.get("position_sizing_available", True)
        add("position_sizing_disabled", ps, "BLOCK", "position_sizing_available must be False")
        # 5
        ar = not portfolio_def.get("auto_rebalance_enabled", True)
        add("auto_rebalance_disabled", ar, "BLOCK", "auto_rebalance_enabled must be False")
        # 6
        pid = bool(portfolio_def.get("portfolio_id"))
        add("portfolio_id_present", pid, "BLOCK", "portfolio_id is required")
        # 7
        pname = bool(portfolio_def.get("name"))
        add("portfolio_name_present", pname, "WARN", "portfolio name is recommended")
        # 8
        has_pos = len(positions) > 0
        add("at_least_one_position", has_pos, "WARN", "no open positions")
        # 9
        neg_qty = any(Decimal(str(p.get("quantity", 0))) < 0 for p in positions)
        add("no_negative_quantities", not neg_qty, "BLOCK", "negative quantities detected")
        # 10
        val_status = valuation.get("valuation_status", "MISSING")
        val_ok = val_status not in ("BLOCKED",)
        add("valuation_status_not_blocked", val_ok, "BLOCK", f"valuation_status={val_status}")
        # 11
        missing = valuation.get("missing_symbols", [])
        add("no_missing_prices", len(missing) == 0, "WARN", f"missing prices: {missing}")
        # 12
        cash_neg = False
        if cash_twd is not None:
            try:
                cash_neg = Decimal(str(cash_twd)) < Decimal("0")
            except Exception:
                pass
        add("cash_not_negative", not cash_neg, "WARN", "cash balance is negative")
        # 13
        cb_method = portfolio_def.get("cost_basis_method", "WEIGHTED_AVERAGE")
        valid_cb = cb_method in ("WEIGHTED_AVERAGE", "FIFO")
        add("cost_basis_method_valid", valid_cb, "BLOCK", f"unsupported cost_basis_method: {cb_method}")
        # 14
        pit_ok = pit_report.get("consistent", True)
        add("pit_dates_consistent", pit_ok, "BLOCK", "PIT date violations detected")
        # 15
        txn_ids = [t.get("transaction_id") for t in transactions if t.get("transaction_id")]
        unique_ids = len(txn_ids) == len(set(txn_ids))
        add("transaction_ids_unique", unique_ids, "BLOCK", "duplicate transaction IDs")
        # 16
        UNSUPPORTED = {"OPTIONS", "FUTURES", "CRYPTO", "FOREX", "BOND", "WARRANT",
                       "CONVERTIBLE_BOND", "PREFERRED_STOCK", "ADR", "OTHER_DERIVATIVE"}
        has_unsupported = any(p.get("asset_type") in UNSUPPORTED for p in positions)
        add("no_unsupported_asset_types", not has_unsupported, "BLOCK", "unsupported asset types present")
        # 17
        decimal_ok = ledger_flags.get("decimal_safe", True)
        add("decimal_monetary_fields", bool(decimal_ok), "BLOCK", "non-Decimal monetary fields detected")

        failed = [c["name"] for c in checks if not c["passed"] and c["severity"] == "BLOCK"]
        warned = [c["name"] for c in checks if not c["passed"] and c["severity"] == "WARN"]

        if failed:
            status = "BLOCKED"
            eligible = False
        elif warned:
            status = "ELIGIBLE_WITH_WARNING"
            eligible = True
        else:
            status = "ELIGIBLE"
            eligible = True

        return {
            "eligible": eligible,
            "status": status,
            "checks": checks,
            "failed_checks": failed,
            "warning_checks": warned,
            "research_only": True,
        }
