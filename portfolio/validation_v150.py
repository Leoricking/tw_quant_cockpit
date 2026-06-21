"""
portfolio/validation_v150.py — Portfolio Validation v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List

_VALIDATION_VERSION = "1.5.0"

# Safety
RESEARCH_ONLY = True
BROKER_LINKED = False
REAL_ORDER_ENABLED = False


def validate_portfolio_definition(portfolio: dict) -> Dict[str, Any]:
    """Validate a portfolio definition dict. Returns {valid, errors, warnings}."""
    errors = []
    warnings = []
    if not portfolio.get("portfolio_id"):
        errors.append("portfolio_id required")
    if portfolio.get("research_only") is not True:
        errors.append("research_only must be True")
    if portfolio.get("broker_linked") is not False:
        errors.append("broker_linked must be False")
    if portfolio.get("real_order_enabled") is not False:
        errors.append("real_order_enabled must be False")
    if portfolio.get("external_broker_id") is not None:
        errors.append("external_broker_id must be None")
    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def validate_transaction(txn: dict) -> Dict[str, Any]:
    """Validate a transaction dict."""
    errors = []
    warnings = []
    required = ["transaction_id", "portfolio_id", "transaction_type", "symbol",
                "trade_date", "effective_at", "available_from"]
    for f in required:
        if not txn.get(f):
            errors.append(f"{f} required")
    q = txn.get("quantity")
    if q is not None:
        try:
            d = Decimal(str(q))
            if d < Decimal("0") and txn.get("transaction_type") not in (
                    "RESEARCH_SELL", "CASH_WITHDRAWAL", "FEE", "TAX"):
                warnings.append("negative quantity on non-sell transaction")
        except Exception:
            errors.append("quantity must be numeric")
    p = txn.get("price")
    if p is not None:
        try:
            Decimal(str(p))
        except Exception:
            errors.append("price must be numeric")
    if txn.get("research_only") is not True:
        errors.append("transaction research_only must be True")
    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def validate_decimal_safe(value: Any, field_name: str = "value") -> Dict[str, Any]:
    """Validate a value is safely representable as Decimal."""
    try:
        Decimal(str(value))
        return {"valid": True, "error": None}
    except Exception as e:
        return {"valid": False, "error": f"{field_name}: {e}"}


def validate_pit_dates(effective_at: str, available_from: str, as_of: str) -> Dict[str, Any]:
    """Validate PIT: effective_at <= as_of and available_from <= as_of."""
    errors = []
    try:
        if effective_at > as_of:
            errors.append(f"future effective_at={effective_at} > as_of={as_of}")
        if available_from > as_of:
            errors.append(f"future available_from={available_from} > as_of={as_of}")
    except Exception as e:
        errors.append(f"date comparison error: {e}")
    return {"valid": len(errors) == 0, "errors": errors}
