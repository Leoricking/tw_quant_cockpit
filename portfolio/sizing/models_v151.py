"""
portfolio/sizing/models_v151.py — Position Sizing Dataclass Models v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] POSITION_SIZING_RESEARCH_ONLY = True. Not Investment Advice.
"""
from __future__ import annotations

import datetime
import hashlib
import json
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
MODELS_VERSION = "1.5.1"


def _decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f"Not serializable: {type(obj)}")


@dataclass
class PositionSizingRequest:
    """Input parameters for a single position sizing calculation."""
    request_id: str
    portfolio_id: str
    account_id: str
    symbol: str
    market: str
    asset_type: str
    as_of: str                                              # ISO date string
    available_from: str                                     # PIT: data available from
    method: str                                             # SizingMethod value
    portfolio_value: Optional[Decimal] = None
    available_cash: Optional[Decimal] = None
    current_quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    current_market_value: Decimal = field(default_factory=lambda: Decimal("0"))
    current_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    reference_price: Optional[Decimal] = None
    planned_entry_price: Optional[Decimal] = None
    stop_price: Optional[Decimal] = None
    atr: Optional[Decimal] = None
    atr_available_from: Optional[str] = None
    volatility: Optional[Decimal] = None
    risk_budget_percent: Optional[Decimal] = None
    target_weight: Optional[Decimal] = None
    max_position_weight: Optional[Decimal] = None
    max_industry_weight: Optional[Decimal] = None
    max_theme_weight: Optional[Decimal] = None
    max_market_weight: Optional[Decimal] = None
    max_order_value: Optional[Decimal] = None
    minimum_order_value: Optional[Decimal] = None
    average_daily_value: Optional[Decimal] = None
    average_daily_value_available_from: Optional[str] = None
    liquidity_participation_limit: Optional[Decimal] = None
    lot_size: int = 1000
    allow_odd_lot: bool = False
    industry: Optional[str] = None
    theme: Optional[str] = None
    source_lineage_ids: List[str] = field(default_factory=list)
    research_only: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must always be True"


@dataclass
class PositionSizingConstraint:
    """Records a single constraint applied during sizing."""
    constraint_id: str
    constraint_type: str                    # ConstraintType value
    severity: str                           # ConstraintSeverity value
    configured_limit: Optional[Decimal] = None
    observed_value: Optional[Decimal] = None
    allowed_value: Optional[Decimal] = None
    capped_quantity: Optional[Decimal] = None
    status: str = "INFO"                    # SizingStatus value
    reason: str = ""
    evidence: Dict[str, Any] = field(default_factory=dict)
    lineage_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PositionSizingProposal:
    """
    Output of a position sizing calculation.
    ALWAYS research_only=True, executable=False, order_created=False,
    persisted_to_ledger=False. Labels: RESEARCH_ONLY, NOT_AN_ORDER, etc.
    """
    proposal_id: str
    request_id: str
    portfolio_id: str
    symbol: str
    method: str
    as_of: str
    reference_price: Optional[Decimal] = None
    raw_quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    capped_quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    normalized_quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    current_quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    proposed_final_quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    incremental_quantity: Decimal = field(default_factory=lambda: Decimal("0"))
    estimated_position_value: Decimal = field(default_factory=lambda: Decimal("0"))
    estimated_final_weight: Decimal = field(default_factory=lambda: Decimal("0"))
    risk_amount: Decimal = field(default_factory=lambda: Decimal("0"))
    risk_percent: Decimal = field(default_factory=lambda: Decimal("0"))
    stop_distance: Decimal = field(default_factory=lambda: Decimal("0"))
    stop_distance_percent: Decimal = field(default_factory=lambda: Decimal("0"))
    constraints: List[PositionSizingConstraint] = field(default_factory=list)
    binding_constraint: Optional[str] = None
    sizing_status: str = "VALID"
    eligibility: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    source_lineage_ids: List[str] = field(default_factory=list)
    calculation_version: str = "1.5.1"
    content_hash: str = ""
    generated_at: str = ""
    # Safety flags — ALWAYS these values
    research_only: bool = True
    executable: bool = False
    order_created: bool = False
    persisted_to_ledger: bool = False
    labels: List[str] = field(default_factory=lambda: [
        "RESEARCH_ONLY", "NOT_AN_ORDER", "NOT_EXECUTABLE",
        "NO_BROKER_CALL", "NO_LEDGER_WRITE", "NO_AUTO_REBALANCE",
    ])
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.research_only is True, "research_only must be True"
        assert self.executable is False, "executable must be False"
        assert self.order_created is False, "order_created must be False"
        assert self.persisted_to_ledger is False, "persisted_to_ledger must be False"
        if not self.generated_at:
            self.generated_at = datetime.datetime.utcnow().isoformat()
        if not self.content_hash:
            self.content_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        payload = json.dumps({
            "proposal_id": self.proposal_id,
            "symbol": self.symbol,
            "raw_quantity": str(self.raw_quantity),
            "normalized_quantity": str(self.normalized_quantity),
            "method": self.method,
            "as_of": self.as_of,
        }, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


@dataclass
class PositionSizingPolicy:
    """
    Research-only position sizing policy.
    full_kelly_enabled=False, leverage_enabled=False, short_enabled=False always.
    """
    policy_id: str
    name: str
    version: str = "1.5.1"
    base_currency: str = "TWD"
    default_method: str = "FIXED_FRACTIONAL"
    risk_per_trade_percent: Decimal = field(default_factory=lambda: Decimal("0.01"))
    max_single_position_weight: Decimal = field(default_factory=lambda: Decimal("0.15"))
    max_industry_weight: Decimal = field(default_factory=lambda: Decimal("0.30"))
    max_theme_weight: Decimal = field(default_factory=lambda: Decimal("0.30"))
    max_market_weight: Decimal = field(default_factory=lambda: Decimal("0.50"))
    max_etf_weight: Decimal = field(default_factory=lambda: Decimal("0.20"))
    max_liquidity_participation: Decimal = field(default_factory=lambda: Decimal("0.10"))
    minimum_cash_reserve_percent: Decimal = field(default_factory=lambda: Decimal("0.05"))
    minimum_order_value: Decimal = field(default_factory=lambda: Decimal("10000"))
    maximum_order_value: Optional[Decimal] = None
    allow_odd_lot: bool = False
    default_lot_size: int = 1000
    full_kelly_enabled: bool = False
    leverage_enabled: bool = False
    short_enabled: bool = False
    effective_from: Optional[str] = None
    valid_to: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert self.full_kelly_enabled is False, "full_kelly_enabled must be False"
        assert self.leverage_enabled is False, "leverage_enabled must be False"
        assert self.short_enabled is False, "short_enabled must be False"
