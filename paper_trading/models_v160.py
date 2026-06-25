"""paper_trading/models_v160.py — Paper Trading Data Models v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY. NOT_A_REAL_ORDER.
[!] NO_BROKER_CALL. NO_REAL_ACCOUNT. NO_FORMAL_PORTFOLIO_LEDGER_WRITE.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional, Dict, Any

from .enums_v160 import (
    PaperSessionStatus, MarketSessionStatus, DataMode,
    PaperOrderType, PaperOrderSide, PaperOrderStatus,
    PaperFillStatus, PaperRiskStatus,
)

_PAPER_MARKER = "PAPER_ONLY"
_SIM_MARKER = "SIMULATION_ONLY"
_NOT_REAL_ORDER = "NOT_A_REAL_ORDER"
_NO_BROKER = "NO_BROKER_CALL"
_NO_ACCOUNT = "NO_REAL_ACCOUNT"
_NO_LEDGER = "NO_FORMAL_PORTFOLIO_LEDGER_WRITE"


@dataclass
class PaperSessionConfig:
    session_id: str
    name: str
    portfolio_template_id: str = ""
    initial_cash: Decimal = field(default_factory=lambda: Decimal("1000000"))
    currency: str = "TWD"
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    timezone: str = "Asia/Taipei"
    market: str = "TWSE"
    data_mode: DataMode = DataMode.FIXTURE
    delayed_minutes: int = 0
    execution_model_id: str = "default_v160"
    slippage_policy_id: str = "fixed_bps_v160"
    liquidity_policy_id: str = "participation_v160"
    risk_policy_id: str = "default_v160"
    sizing_policy_id: str = "default_v160"
    allowed_symbols: List[str] = field(default_factory=list)
    maximum_orders: int = 1000
    maximum_position_count: int = 50
    research_only: bool = True
    broker_enabled: bool = False
    real_order_enabled: bool = False
    formal_ledger_write_enabled: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must be True"
        assert self.broker_enabled is False, "broker_enabled must be False"
        assert self.real_order_enabled is False, "real_order_enabled must be False"
        assert self.formal_ledger_write_enabled is False, "formal_ledger_write_enabled must be False"


@dataclass
class PaperMarketEvent:
    event_id: str
    sequence: int
    symbol: str
    event_type: str
    exchange_timestamp: str
    received_timestamp: str
    available_from: str
    price: Optional[Decimal] = None
    volume: Optional[Decimal] = None
    bid: Optional[Decimal] = None
    ask: Optional[Decimal] = None
    source: str = "FIXTURE"
    data_mode: DataMode = DataMode.FIXTURE
    lineage_ids: List[str] = field(default_factory=list)
    content_hash: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def compute_hash(self) -> str:
        payload = f"{self.event_id}|{self.sequence}|{self.symbol}|{self.exchange_timestamp}|{self.price}|{self.volume}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


@dataclass
class PaperOrder:
    paper_order_id: str
    session_id: str
    client_order_id: str
    symbol: str
    side: PaperOrderSide
    order_type: PaperOrderType
    quantity: Decimal
    limit_price: Optional[Decimal] = None
    stop_price: Optional[Decimal] = None
    time_in_force: str = "DAY"
    created_at: Optional[str] = None
    decision_as_of: Optional[str] = None
    status: PaperOrderStatus = PaperOrderStatus.CREATED
    filled_quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    remaining_quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    average_fill_price: Optional[Decimal] = None
    rejection_reason: str = ""
    risk_evaluation_id: str = ""
    sizing_proposal_id: str = ""
    lineage_ids: List[str] = field(default_factory=list)
    research_only: bool = True
    executable_on_broker: bool = False
    real_order_created: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must be True"
        assert self.executable_on_broker is False, "executable_on_broker must be False"
        assert self.real_order_created is False, "real_order_created must be False"
        if self.remaining_quantity == Decimal("0"):
            self.remaining_quantity = self.quantity

    @property
    def paper_only(self) -> str:
        return _PAPER_MARKER

    @property
    def simulation_only(self) -> str:
        return _SIM_MARKER

    @property
    def not_a_real_order(self) -> str:
        return _NOT_REAL_ORDER


@dataclass
class PaperFill:
    fill_id: str
    paper_order_id: str
    session_id: str
    symbol: str
    side: PaperOrderSide
    quantity: Decimal
    price: Decimal
    gross_amount: Decimal
    fee: Decimal = field(default_factory=lambda: Decimal("0"))
    tax: Decimal = field(default_factory=lambda: Decimal("0"))
    slippage: Decimal = field(default_factory=lambda: Decimal("0"))
    net_amount: Decimal = field(default_factory=lambda: Decimal("0"))
    simulated_at: Optional[str] = None
    market_event_id: str = ""
    fill_status: PaperFillStatus = PaperFillStatus.SIMULATED
    liquidity_assumption: str = "PARTICIPATION"
    latency_assumption: str = "ZERO_DISCLOSED"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def paper_only(self) -> str:
        return _PAPER_MARKER

    @property
    def not_a_real_order(self) -> str:
        return _NOT_REAL_ORDER


@dataclass
class PaperPosition:
    session_id: str
    symbol: str
    quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    average_cost: Decimal = field(default_factory=lambda: Decimal("0"))
    market_price: Optional[Decimal] = None
    market_value: Decimal = field(default_factory=lambda: Decimal("0"))
    unrealized_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    realized_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    total_fees: Decimal = field(default_factory=lambda: Decimal("0"))
    total_taxes: Decimal = field(default_factory=lambda: Decimal("0"))
    last_updated: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def paper_only(self) -> str:
        return _PAPER_MARKER


@dataclass
class PaperCashBalance:
    session_id: str
    currency: str = "TWD"
    opening_cash: Decimal = field(default_factory=lambda: Decimal("0"))
    available_cash: Decimal = field(default_factory=lambda: Decimal("0"))
    reserved_cash: Decimal = field(default_factory=lambda: Decimal("0"))
    settled_cash: Decimal = field(default_factory=lambda: Decimal("0"))
    total_fees: Decimal = field(default_factory=lambda: Decimal("0"))
    total_taxes: Decimal = field(default_factory=lambda: Decimal("0"))
    realized_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def paper_only(self) -> str:
        return _PAPER_MARKER


@dataclass
class PaperLedgerEntry:
    entry_id: str
    session_id: str
    sequence: int
    event_type: str
    paper_order_id: str = ""
    fill_id: str = ""
    symbol: str = ""
    quantity_delta: Decimal = field(default_factory=lambda: Decimal("0"))
    cash_delta: Decimal = field(default_factory=lambda: Decimal("0"))
    fee: Decimal = field(default_factory=lambda: Decimal("0"))
    tax: Decimal = field(default_factory=lambda: Decimal("0"))
    timestamp: Optional[str] = None
    content_hash: str = ""
    previous_hash: str = ""
    paper_only: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.paper_only is True, "paper_only must be True"

    def compute_hash(self) -> str:
        payload = f"{self.entry_id}|{self.sequence}|{self.event_type}|{self.cash_delta}|{self.quantity_delta}|{self.previous_hash}"
        return hashlib.sha256(payload.encode()).hexdigest()[:32]


@dataclass
class PaperSessionSnapshot:
    snapshot_id: str
    session_id: str
    as_of: str
    positions: List[Dict[str, Any]] = field(default_factory=list)
    cash: Optional[Dict[str, Any]] = None
    orders: List[Dict[str, Any]] = field(default_factory=list)
    fills: List[Dict[str, Any]] = field(default_factory=list)
    realized_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    unrealized_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    total_pnl: Decimal = field(default_factory=lambda: Decimal("0"))
    exposure: Decimal = field(default_factory=lambda: Decimal("0"))
    drawdown: Decimal = field(default_factory=lambda: Decimal("0"))
    risk_status: str = "PASS"
    event_sequence: int = 0
    ledger_hash: str = ""
    content_hash: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def compute_content_hash(self) -> str:
        payload = json.dumps({
            "session_id": self.session_id,
            "as_of": self.as_of,
            "realized_pnl": str(self.realized_pnl),
            "unrealized_pnl": str(self.unrealized_pnl),
            "event_sequence": self.event_sequence,
            "ledger_hash": self.ledger_hash,
        }, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()[:32]


@dataclass
class PaperRiskEvaluation:
    evaluation_id: str
    session_id: str
    paper_order_id: str
    symbol: str
    status: PaperRiskStatus
    checks: Dict[str, Any] = field(default_factory=dict)
    block_reasons: List[str] = field(default_factory=list)
    warning_reasons: List[str] = field(default_factory=list)
    evaluated_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PaperSessionReproducibilityManifest:
    manifest_id: str
    session_id: str
    session_config_hash: str
    initial_cash: str
    allowed_symbols: List[str]
    policies: Dict[str, str]
    data_mode: str
    event_hashes: List[str] = field(default_factory=list)
    event_order: List[str] = field(default_factory=list)
    seed: Optional[int] = None
    execution_model: str = ""
    latency_model: str = ""
    slippage_model: str = ""
    liquidity_model: str = ""
    code_commit: str = ""
    python_version: str = ""
    dependency_versions: Dict[str, str] = field(default_factory=dict)
    timezone: str = "Asia/Taipei"
    calendar_version: str = "v160"
    final_ledger_hash: str = ""
    final_snapshot_hash: str = ""
    research_only: bool = True
    paper_only: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
