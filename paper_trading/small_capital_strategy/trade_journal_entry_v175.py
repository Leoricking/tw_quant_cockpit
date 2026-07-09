"""
paper_trading/small_capital_strategy/trade_journal_entry_v175.py
Trade journal entry creation and management for v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Optional

from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeDirection, TradeOutcome, ABCPattern, JournalEntryStatus,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import TradeJournalEntry

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"


def create_journal_entry(
    symbol: str,
    direction: TradeDirection,
    entry_date: str,
    entry_price: float,
    position_size_twd: float,
    stop_loss_price: float,
    stop_loss_pct: float,
    abc_pattern: ABCPattern = ABCPattern.UNKNOWN,
    market_regime: str = "UNKNOWN",
    watchlist_tier: int = 0,
    notes: str = "",
) -> TradeJournalEntry:
    """Create a new open TradeJournalEntry."""
    return TradeJournalEntry(
        symbol=symbol,
        direction=direction,
        entry_date=entry_date,
        entry_price=entry_price,
        position_size_twd=position_size_twd,
        stop_loss_price=stop_loss_price,
        stop_loss_pct=stop_loss_pct,
        outcome=TradeOutcome.OPEN,
        status=JournalEntryStatus.OPEN,
        abc_pattern=abc_pattern,
        market_regime=market_regime,
        watchlist_tier=watchlist_tier,
        notes=notes,
    )


def close_journal_entry(
    entry: TradeJournalEntry,
    exit_date: str,
    exit_price: float,
) -> TradeJournalEntry:
    """Close a journal entry and compute outcome."""
    entry.exit_date = exit_date
    entry.exit_price = exit_price
    entry.status = JournalEntryStatus.CLOSED

    if entry.entry_price <= 0:
        entry.outcome = TradeOutcome.UNKNOWN
        return entry

    if exit_price > entry.entry_price:
        if entry.direction == TradeDirection.LONG:
            entry.outcome = TradeOutcome.WIN
        else:
            entry.outcome = TradeOutcome.LOSS
    elif exit_price < entry.entry_price:
        if entry.direction == TradeDirection.LONG:
            entry.outcome = TradeOutcome.LOSS
        else:
            entry.outcome = TradeOutcome.WIN
    else:
        entry.outcome = TradeOutcome.BREAKEVEN

    return entry


def validate_entry(entry: TradeJournalEntry) -> bool:
    """Return True if a journal entry is valid."""
    if not entry.symbol:
        return False
    if entry.entry_price <= 0:
        return False
    if entry.position_size_twd < 0:
        return False
    if entry.stop_loss_pct < 0:
        return False
    if not entry.entry_date:
        return False
    if not entry.paper_only:
        return False
    if not entry.no_real_orders:
        return False
    return True
