"""
paper_trading/small_capital_strategy/trade_journal_dashboard_v175.py
Dashboard builder for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeOutcome, JournalEntryStatus,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeJournalEntry, TradeJournalDashboard,
)
from paper_trading.small_capital_strategy.trade_journal_scorecard_v175 import build_scorecard
from paper_trading.small_capital_strategy.trade_journal_regime_review_v175 import review_regime_outcome
from paper_trading.small_capital_strategy.trade_journal_risk_review_v175 import review_risk_violations

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"

_KNOWN_REGIMES = ["BULL", "RANGE", "BEAR", "RISK_OFF", "UNKNOWN"]


def build_dashboard(entries: List[TradeJournalEntry]) -> TradeJournalDashboard:
    """Build a TradeJournalDashboard from a list of journal entries."""
    total = len(entries)
    open_count   = sum(1 for e in entries if e.status == JournalEntryStatus.OPEN)
    closed_count = sum(1 for e in entries if e.status == JournalEntryStatus.CLOSED)
    win_count    = sum(1 for e in entries if e.outcome == TradeOutcome.WIN)
    loss_count   = sum(1 for e in entries if e.outcome == TradeOutcome.LOSS)

    win_rate_pct = round(win_count / closed_count * 100.0, 2) if closed_count > 0 else 0.0

    # Avg return pct (simplified)
    closed_entries = [e for e in entries if e.status == JournalEntryStatus.CLOSED
                      and e.entry_price > 0 and e.exit_price > 0]
    if closed_entries:
        returns = [(e.exit_price - e.entry_price) / e.entry_price * 100.0 for e in closed_entries]
        avg_return_pct = round(sum(returns) / len(returns), 2)
    else:
        avg_return_pct = 0.0

    # Total PnL
    total_pnl_twd = sum(
        (e.exit_price - e.entry_price) / e.entry_price * e.position_size_twd
        for e in closed_entries
        if e.entry_price > 0
    )
    total_pnl_twd = round(total_pnl_twd, 2)

    # Scorecard
    scorecard = build_scorecard(entries)

    # Violations
    violations_count = sum(
        1 for e in entries
        if len(review_risk_violations(e).violation_type.split(",")) > 0
        and review_risk_violations(e).violation_type != "NONE"
    )

    # Regime reviews
    regime_reviews = [review_regime_outcome(r, entries) for r in _KNOWN_REGIMES]

    return TradeJournalDashboard(
        entries_count=total,
        open_count=open_count,
        closed_count=closed_count,
        win_count=win_count,
        loss_count=loss_count,
        win_rate_pct=win_rate_pct,
        avg_return_pct=avg_return_pct,
        total_pnl_twd=total_pnl_twd,
        scorecard=scorecard,
        violations_count=violations_count,
        regime_reviews=regime_reviews,
    )
