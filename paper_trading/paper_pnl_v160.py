"""paper_trading/paper_pnl_v160.py — Paper P&L Calculator v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY. PAPER_ONLY.
Decimal-safe. No missing price as zero. Corporate action limitation disclosed.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


@dataclass
class PaperPnLSummary:
    session_id: str
    realized_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    unrealized_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    total_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    total_fees: Decimal = field(default_factory=lambda: Decimal("0"))
    total_taxes: Decimal = field(default_factory=lambda: Decimal("0"))
    total_slippage: Decimal = field(default_factory=lambda: Decimal("0"))
    gross_exposure: Decimal = field(default_factory=lambda: Decimal("0"))
    peak_value: Decimal = field(default_factory=lambda: Decimal("0"))
    drawdown: Decimal = field(default_factory=lambda: Decimal("0"))
    drawdown_pct: Decimal = field(default_factory=lambda: Decimal("0"))
    paper_only: bool = True
    corporate_action_complete: bool = False
    corporate_action_note: str = "CORPORATE_ACTIONS_NOT_FULLY_MODELED_v160"
    stale_price_symbols: list = field(default_factory=list)


class PaperPnLCalculator:
    """Decimal-safe P&L calculator. Paper-only."""

    def compute(
        self,
        session_id: str,
        realized_pnl: Decimal,
        unrealized_pnl: Decimal,
        total_fees: Decimal,
        total_taxes: Decimal,
        total_slippage: Decimal,
        gross_exposure: Decimal,
        initial_cash: Decimal,
        current_total_value: Optional[Decimal] = None,
        peak_value: Optional[Decimal] = None,
        stale_price_symbols: Optional[list] = None,
    ) -> PaperPnLSummary:
        total_pnl = realized_pnl + unrealized_pnl - total_fees - total_taxes - total_slippage
        if current_total_value is None:
            current_total_value = initial_cash + total_pnl
        pk = peak_value if peak_value is not None else max(initial_cash, current_total_value)
        if pk > Decimal("0"):
            dd = max(Decimal("0"), pk - current_total_value)
            dd_pct = dd / pk * Decimal("100")
        else:
            dd = Decimal("0")
            dd_pct = Decimal("0")

        return PaperPnLSummary(
            session_id=session_id,
            realized_pnl=realized_pnl,
            unrealized_pnl=unrealized_pnl,
            total_pnl=total_pnl,
            total_fees=total_fees,
            total_taxes=total_taxes,
            total_slippage=total_slippage,
            gross_exposure=gross_exposure,
            peak_value=pk,
            drawdown=dd,
            drawdown_pct=dd_pct,
            paper_only=True,
            corporate_action_complete=False,
            stale_price_symbols=stale_price_symbols or [],
        )
