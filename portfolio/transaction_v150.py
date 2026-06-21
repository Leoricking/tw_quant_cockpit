"""
portfolio/transaction_v150.py — Portfolio Transaction Service v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional
import datetime

_TRANSACTION_VERSION = "1.5.0"
RESEARCH_ONLY = True
NOT_BROKER_EXECUTION = True


def make_transaction_id(portfolio_id: str, symbol: str, trade_date: str, seq: int) -> str:
    """Generate a deterministic transaction ID."""
    return f"{portfolio_id}_{symbol}_{trade_date}_{seq:06d}"


def build_research_transaction(
    portfolio_id: str,
    account_id: str,
    transaction_type: str,
    symbol: str,
    trade_date: str,
    effective_at: str,
    available_from: str,
    quantity: Decimal,
    price: Decimal,
    fee: Decimal = Decimal("0"),
    tax: Decimal = Decimal("0"),
    currency: str = "TWD",
    market: str = "TWSE",
    asset_type: str = "COMMON_STOCK",
    source_lineage_id: str = "",
    import_batch_id: str = "",
    transaction_id: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> Dict[str, Any]:
    """Build a research-only transaction dict. Never creates a broker order."""
    gross = quantity * price
    net = gross - fee - tax if transaction_type in ("RESEARCH_BUY",) else gross - fee - tax
    txn_id = transaction_id or make_transaction_id(portfolio_id, symbol, trade_date, 0)
    return {
        "transaction_id": txn_id,
        "portfolio_id": portfolio_id,
        "account_id": account_id,
        "transaction_type": transaction_type,
        "symbol": symbol,
        "market": market,
        "asset_type": asset_type,
        "trade_date": trade_date,
        "effective_at": effective_at,
        "available_from": available_from,
        "quantity": quantity,
        "price": price,
        "gross_amount": gross,
        "fee": fee,
        "tax": tax,
        "net_amount": net,
        "currency": currency,
        "source_type": "MANUAL_RESEARCH",
        "source_lineage_id": source_lineage_id,
        "import_batch_id": import_batch_id,
        "research_only": True,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "metadata": metadata or {},
        "_NOT_BROKER_EXECUTION": True,
        "_NOT_REAL_ORDER": True,
    }
