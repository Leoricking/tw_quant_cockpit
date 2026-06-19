"""
empirical_backtest/cost_model_v140.py — Transaction Cost and Slippage Models for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from .models_v140 import SlippageModelType, SignalType


class TaiwanTransactionCostModel:
    """Taiwan stock market transaction cost model."""

    def __init__(
        self,
        brokerage_rate: float = 0.001425,
        min_fee: float = 20.0,
        transaction_tax_stock: float = 0.003,
        transaction_tax_etf: float = 0.001,
        effective_date: str = "2024-01-01",
    ):
        self.brokerage_rate = brokerage_rate
        self.min_fee = min_fee
        self.transaction_tax_stock = transaction_tax_stock
        self.transaction_tax_etf = transaction_tax_etf
        self.effective_date = effective_date
        self.source_note = (
            f"Taiwan standard brokerage + STT as of {effective_date}. "
            "May change — verify current rates."
        )

    def buy_cost(self, price: float, quantity: float, is_etf: bool = False) -> float:
        """Brokerage cost only (no tax on buy)."""
        brokerage = price * quantity * self.brokerage_rate
        return max(brokerage, self.min_fee)

    def sell_cost(self, price: float, quantity: float, is_etf: bool = False) -> float:
        """Brokerage + transaction tax on sell."""
        brokerage = max(price * quantity * self.brokerage_rate, self.min_fee)
        tax_rate = self.transaction_tax_etf if is_etf else self.transaction_tax_stock
        tax = price * quantity * tax_rate
        return brokerage + tax

    def round_trip_cost(self, price: float, quantity: float, is_etf: bool = False) -> float:
        """Total buy + sell cost."""
        return self.buy_cost(price, quantity, is_etf) + self.sell_cost(price, quantity, is_etf)

    def to_dict(self) -> dict:
        return {
            "brokerage_rate": self.brokerage_rate,
            "min_fee": self.min_fee,
            "transaction_tax_stock": self.transaction_tax_stock,
            "transaction_tax_etf": self.transaction_tax_etf,
            "effective_date": self.effective_date,
            "source_note": self.source_note,
        }


class SlippageModel:
    """Slippage model for backtest simulation."""

    def __init__(
        self,
        model_type: str = SlippageModelType.CONSERVATIVE_FIXED,
        bps: float = 10.0,
    ):
        self.model_type = model_type
        self.bps = bps

    def apply(self, price: float, signal_type: str, volume=None) -> float:
        """Apply slippage to price based on model type and signal direction."""
        is_buy = signal_type in (SignalType.ENTRY, "BUY", "ENTRY")

        if self.model_type == SlippageModelType.NONE:
            return price

        elif self.model_type in (SlippageModelType.FIXED_BPS, SlippageModelType.PERCENTAGE):
            factor = self.bps / 10000.0
            if is_buy:
                return price * (1 + factor)
            else:
                return price * (1 - factor)

        elif self.model_type == SlippageModelType.CONSERVATIVE_FIXED:
            factor = self.bps / 10000.0
            if is_buy:
                adjusted = price * (1 + factor)
            else:
                adjusted = price * (1 - factor)
            # Additional penalty for low volume
            if volume is not None and volume < 1000:
                adjusted = adjusted * (1 + 5 / 10000.0) if is_buy else adjusted * (1 - 5 / 10000.0)
            return adjusted

        elif self.model_type == SlippageModelType.VOLUME_AWARE_SIMPLE:
            factor = self.bps / 10000.0
            if is_buy:
                adjusted = price * (1 + factor)
            else:
                adjusted = price * (1 - factor)
            if volume is not None and volume < 1000:
                adjusted = adjusted * (1 + 5 / 10000.0) if is_buy else adjusted * (1 - 5 / 10000.0)
            return adjusted

        return price

    def to_dict(self) -> dict:
        return {
            "model_type": self.model_type,
            "bps": self.bps,
        }
