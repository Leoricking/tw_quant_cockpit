"""
portfolio/models_v150.py — Portfolio Dataclass Models v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


@dataclass
class PortfolioDefinition:
    portfolio_id: str
    name: str
    description: str = ""
    base_currency: str = "TWD"
    benchmark_symbol: str = ""
    status: str = "DRAFT"
    created_at: Optional[str] = None
    effective_from: Optional[str] = None
    archived_at: Optional[str] = None
    research_only: bool = True
    broker_linked: bool = False
    real_order_enabled: bool = False
    cost_basis_method: str = "WEIGHTED_AVERAGE"
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must be True"
        assert self.broker_linked is False, "broker_linked must be False"
        assert self.real_order_enabled is False, "real_order_enabled must be False"


@dataclass
class PortfolioAccount:
    account_id: str
    portfolio_id: str
    account_name: str = ""
    account_type: str = "RESEARCH"
    currency: str = "TWD"
    research_only: bool = True
    external_broker_id: Optional[str] = None
    enabled: bool = True
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.external_broker_id is None, "external_broker_id must be None"
        assert self.research_only is True, "research_only must be True"


@dataclass
class PortfolioTransaction:
    transaction_id: str
    portfolio_id: str
    account_id: str
    transaction_type: str
    symbol: str
    market: str = "TWSE"
    asset_type: str = "COMMON_STOCK"
    trade_date: str = ""
    effective_at: str = ""
    available_from: str = ""
    quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    price: Decimal = field(default_factory=lambda: Decimal("0"))
    gross_amount: Decimal = field(default_factory=lambda: Decimal("0"))
    fee: Decimal = field(default_factory=lambda: Decimal("0"))
    tax: Decimal = field(default_factory=lambda: Decimal("0"))
    net_amount: Decimal = field(default_factory=lambda: Decimal("0"))
    currency: str = "TWD"
    source_type: str = "MANUAL_RESEARCH"
    source_lineage_id: str = ""
    import_batch_id: str = ""
    research_only: bool = True
    created_at: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class PortfolioPosition:
    portfolio_id: str
    account_id: str
    symbol: str
    market: str = "TWSE"
    asset_type: str = "COMMON_STOCK"
    quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    average_cost: Decimal = field(default_factory=lambda: Decimal("0"))
    total_cost: Decimal = field(default_factory=lambda: Decimal("0"))
    realized_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    last_transaction_at: str = ""
    effective_at: str = ""
    source_transaction_ids: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class CashBalance:
    portfolio_id: str
    account_id: str
    currency: str = "TWD"
    amount: Decimal = field(default_factory=lambda: Decimal("0"))
    effective_at: str = ""
    transaction_ids: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class PortfolioValuation:
    valuation_id: str
    portfolio_id: str
    as_of: str
    available_from: str = ""
    base_currency: str = "TWD"
    cash_value: Decimal = field(default_factory=lambda: Decimal("0"))
    securities_value: Decimal = field(default_factory=lambda: Decimal("0"))
    total_value: Decimal = field(default_factory=lambda: Decimal("0"))
    total_cost: Decimal = field(default_factory=lambda: Decimal("0"))
    unrealized_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    realized_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    valuation_status: str = "VALID"
    missing_symbols: list = field(default_factory=list)
    stale_symbols: list = field(default_factory=list)
    blocked_symbols: list = field(default_factory=list)
    price_lineage_ids: dict = field(default_factory=dict)
    generated_at: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class PositionValuation:
    symbol: str
    quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    average_cost: Decimal = field(default_factory=lambda: Decimal("0"))
    market_price: Decimal = field(default_factory=lambda: Decimal("0"))
    market_value: Decimal = field(default_factory=lambda: Decimal("0"))
    cost_value: Decimal = field(default_factory=lambda: Decimal("0"))
    unrealized_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    unrealized_return: Decimal = field(default_factory=lambda: Decimal("0"))
    portfolio_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    price_as_of: str = ""
    price_available_from: str = ""
    price_authority: str = ""
    price_quality: str = ""
    price_freshness: str = ""
    price_lineage_id: str = ""
    valuation_status: str = "VALID"
    metadata: dict = field(default_factory=dict)


@dataclass
class PortfolioSnapshot:
    snapshot_id: str
    portfolio_id: str
    as_of: str
    available_from: str = ""
    positions: list = field(default_factory=list)       # list of PositionValuation
    cash: list = field(default_factory=list)            # list of CashBalance
    valuation: Optional[object] = None                  # PortfolioValuation
    exposures: dict = field(default_factory=dict)
    concentration: dict = field(default_factory=dict)
    return_summary: dict = field(default_factory=dict)
    benchmark_summary: dict = field(default_factory=dict)
    eligibility: dict = field(default_factory=dict)
    source_lineage_ids: list = field(default_factory=list)
    calculation_version: str = "1.5.0"
    generated_at: str = ""
    immutable: bool = True
    metadata: dict = field(default_factory=dict)


@dataclass
class PortfolioReturnPoint:
    portfolio_id: str
    period_start: str
    period_end: str
    beginning_value: Decimal = field(default_factory=lambda: Decimal("0"))
    ending_value: Decimal = field(default_factory=lambda: Decimal("0"))
    external_cash_flow: Decimal = field(default_factory=lambda: Decimal("0"))
    income: Decimal = field(default_factory=lambda: Decimal("0"))
    fee: Decimal = field(default_factory=lambda: Decimal("0"))
    tax: Decimal = field(default_factory=lambda: Decimal("0"))
    simple_return: Optional[Decimal] = None
    time_weighted_return: Optional[Decimal] = None
    money_weighted_return: Optional[Decimal] = None     # EXPERIMENTAL
    calculation_status: str = "VALID"
    metadata: dict = field(default_factory=dict)


@dataclass
class PortfolioExposureSummary:
    gross_exposure: Decimal = field(default_factory=lambda: Decimal("0"))
    net_exposure: Decimal = field(default_factory=lambda: Decimal("0"))
    cash_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    equity_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    etf_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    listed_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    otc_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    unknown_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    top_positions: list = field(default_factory=list)
    industry_exposure: dict = field(default_factory=dict)
    theme_exposure: dict = field(default_factory=dict)
    market_exposure: dict = field(default_factory=dict)
    overlapping_themes: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class PortfolioConcentrationSummary:
    largest_position_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    top_3_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    top_5_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    herfindahl_index: Decimal = field(default_factory=lambda: Decimal("0"))
    effective_number_of_positions: Decimal = field(default_factory=lambda: Decimal("0"))
    concentration_status: str = "NORMAL"
    warnings: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class BenchmarkComparison:
    benchmark_symbol: str
    portfolio_return: Optional[Decimal] = None
    benchmark_return: Optional[Decimal] = None
    excess_return: Optional[Decimal] = None
    tracking_period: str = ""
    portfolio_data_status: str = "VALID"
    benchmark_data_status: str = "VALID"
    is_proxy: bool = False
    proxy_disclosure: str = ""
    metadata: dict = field(default_factory=dict)
