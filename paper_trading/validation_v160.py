"""paper_trading/validation_v160.py — Paper Trading Validation v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
"""
from __future__ import annotations
from decimal import Decimal
from typing import List, Optional, Tuple

from .enums_v160 import PaperOrderSide, DataMode


def validate_symbol(symbol: str) -> Tuple[bool, str]:
    if not symbol or not isinstance(symbol, str):
        return False, "symbol must be non-empty string"
    if len(symbol) > 20:
        return False, f"symbol too long: {symbol}"
    return True, ""


def validate_quantity(quantity) -> Tuple[bool, str]:
    try:
        q = Decimal(str(quantity))
    except Exception:
        return False, "quantity must be numeric"
    if q <= Decimal("0"):
        return False, "quantity must be positive"
    return True, ""


def validate_price(price) -> Tuple[bool, str]:
    if price is None:
        return True, ""
    try:
        p = Decimal(str(price))
    except Exception:
        return False, "price must be numeric"
    if p <= Decimal("0"):
        return False, "price must be positive"
    return True, ""


def validate_cash(amount) -> Tuple[bool, str]:
    try:
        a = Decimal(str(amount))
    except Exception:
        return False, "cash must be numeric"
    if a < Decimal("0"):
        return False, "cash cannot be negative"
    return True, ""


def validate_no_short(side: PaperOrderSide, existing_quantity: Decimal, sell_quantity: Decimal) -> Tuple[bool, str]:
    if side == PaperOrderSide.SELL:
        if sell_quantity > existing_quantity:
            return False, f"insufficient paper position: have {existing_quantity}, selling {sell_quantity}"
    return True, ""


def validate_data_mode(data_mode: DataMode) -> Tuple[bool, str]:
    if data_mode is None:
        return False, "data_mode must not be None"
    if data_mode not in DataMode:
        return False, f"unknown data mode: {data_mode}"
    return True, ""


def validate_session_config(config) -> Tuple[bool, List[str]]:
    errors = []
    if not config.session_id:
        errors.append("session_id required")
    if not config.name:
        errors.append("name required")
    ok, msg = validate_cash(config.initial_cash)
    if not ok:
        errors.append(f"initial_cash: {msg}")
    if config.initial_cash <= Decimal("0"):
        errors.append("initial_cash must be positive")
    if config.research_only is not True:
        errors.append("research_only must be True")
    if config.broker_enabled is not False:
        errors.append("broker_enabled must be False")
    if config.real_order_enabled is not False:
        errors.append("real_order_enabled must be False")
    if config.formal_ledger_write_enabled is not False:
        errors.append("formal_ledger_write_enabled must be False")
    return len(errors) == 0, errors
