"""
empirical_backtest/models_v140.py — Data models for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
BACKTEST_MOCK_FORMAL_CONCLUSION_ALLOWED = False


# ---------------------------------------------------------------------------
# String constant classes (not Enum)
# ---------------------------------------------------------------------------

class RuleCategory:
    TREND = "TREND"
    BREAKOUT = "BREAKOUT"
    PULLBACK = "PULLBACK"
    SECOND_WAVE = "SECOND_WAVE"
    FUNDAMENTAL_TURNAROUND = "FUNDAMENTAL_TURNAROUND"
    INSTITUTIONAL = "INSTITUTIONAL"
    VOLUME_PRICE = "VOLUME_PRICE"
    SAKATA = "SAKATA"
    ABC_BUY_POINT = "ABC_BUY_POINT"
    COMPOSITE = "COMPOSITE"
    RISK_FILTER = "RISK_FILTER"
    UNKNOWN = "UNKNOWN"


class SignalType:
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    STOP_LOSS = "STOP_LOSS"
    TAKE_PROFIT = "TAKE_PROFIT"
    TIME_EXIT = "TIME_EXIT"
    RISK_EXIT = "RISK_EXIT"
    NO_ACTION = "NO_ACTION"


class BacktestStatus:
    PASS = "PASS"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NO_TRADES = "NO_TRADES"
    FAILED = "FAILED"
    DEMO_ONLY = "DEMO_ONLY"


class ConfidenceLevel:
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INSUFFICIENT = "INSUFFICIENT"
    BLOCKED = "BLOCKED"


class ExecutionModelType:
    NEXT_OPEN = "NEXT_OPEN"
    NEXT_CLOSE = "NEXT_CLOSE"
    NEXT_BAR_VWAP_APPROXIMATION = "NEXT_BAR_VWAP_APPROXIMATION"
    LIMIT_NOT_FILLED = "LIMIT_NOT_FILLED"
    STOP_TRIGGERED = "STOP_TRIGGERED"
    END_OF_DATA_EXIT = "END_OF_DATA_EXIT"


class SlippageModelType:
    NONE = "NONE"
    FIXED_BPS = "FIXED_BPS"
    PERCENTAGE = "PERCENTAGE"
    VOLUME_AWARE_SIMPLE = "VOLUME_AWARE_SIMPLE"
    CONSERVATIVE_FIXED = "CONSERVATIVE_FIXED"


class BenchmarkType:
    BUY_AND_HOLD_SYMBOL = "BUY_AND_HOLD_SYMBOL"
    MARKET_INDEX = "MARKET_INDEX"
    EQUAL_WEIGHT_UNIVERSE = "EQUAL_WEIGHT_UNIVERSE"
    CASH = "CASH"
    NONE = "NONE"


class MarketRegime:
    BULL = "BULL"
    BEAR = "BEAR"
    SIDEWAYS = "SIDEWAYS"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"
    UNKNOWN = "UNKNOWN"


class PeriodType:
    IN_SAMPLE = "IN_SAMPLE"
    VALIDATION = "VALIDATION"
    OUT_OF_SAMPLE = "OUT_OF_SAMPLE"
    WALK_FORWARD = "WALK_FORWARD"


class CorporateActionStatus:
    ADJUSTED = "ADJUSTED"
    UNADJUSTED = "UNADJUSTED"
    PARTIALLY_ADJUSTED = "PARTIALLY_ADJUSTED"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class StrategyRule:
    rule_id: str
    rule_name: str
    rule_version: str
    category: str
    description: str
    source: str
    source_reference: str
    enabled: bool = True
    experimental: bool = False
    required_datasets: list = field(default_factory=list)
    required_fields: list = field(default_factory=list)
    required_indicators: list = field(default_factory=list)
    minimum_history_bars: int = 20
    supported_markets: list = field(default_factory=list)
    supported_security_types: list = field(default_factory=list)
    entry_conditions: list = field(default_factory=list)
    exit_conditions: list = field(default_factory=list)
    stop_loss_rule: Optional[str] = None
    take_profit_rule: Optional[str] = None
    holding_period_rule: Optional[str] = None
    cooldown_rule: Optional[str] = None
    position_sizing_rule: Optional[str] = None
    lookahead_safe: bool = True
    backtestable: bool = True
    parameter_schema: dict = field(default_factory=dict)
    default_parameters: dict = field(default_factory=dict)
    tags: list = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "rule_version": self.rule_version,
            "category": self.category,
            "description": self.description,
            "source": self.source,
            "source_reference": self.source_reference,
            "enabled": self.enabled,
            "experimental": self.experimental,
            "required_datasets": self.required_datasets,
            "required_fields": self.required_fields,
            "required_indicators": self.required_indicators,
            "minimum_history_bars": self.minimum_history_bars,
            "supported_markets": self.supported_markets,
            "supported_security_types": self.supported_security_types,
            "entry_conditions": self.entry_conditions,
            "exit_conditions": self.exit_conditions,
            "stop_loss_rule": self.stop_loss_rule,
            "take_profit_rule": self.take_profit_rule,
            "holding_period_rule": self.holding_period_rule,
            "cooldown_rule": self.cooldown_rule,
            "position_sizing_rule": self.position_sizing_rule,
            "lookahead_safe": self.lookahead_safe,
            "backtestable": self.backtestable,
            "parameter_schema": self.parameter_schema,
            "default_parameters": self.default_parameters,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyRule":
        known = {f for f in cls.__dataclass_fields__}
        kwargs = {k: v for k, v in d.items() if k in known}
        return cls(**kwargs)


@dataclass
class StrategyRuleSnapshot:
    snapshot_id: str
    rule_id: str
    rule_version: str
    parameters: dict
    parameter_hash: str
    source_commit: str
    application_version: str
    dataset_snapshot_id: str
    universe_snapshot_id: str
    provider_snapshot: dict
    quality_policy_version: str
    freshness_policy_version: str
    transaction_cost_model: dict
    slippage_model: dict
    benchmark_definition: dict
    created_at: str
    metadata: dict = field(default_factory=dict)

    def build_hash(self) -> str:
        payload = json.dumps(
            {"rule_id": self.rule_id, "rule_version": self.rule_version, "parameters": self.parameters},
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "rule_id": self.rule_id,
            "rule_version": self.rule_version,
            "parameters": copy.deepcopy(self.parameters),
            "parameter_hash": self.parameter_hash,
            "source_commit": self.source_commit,
            "application_version": self.application_version,
            "dataset_snapshot_id": self.dataset_snapshot_id,
            "universe_snapshot_id": self.universe_snapshot_id,
            "provider_snapshot": copy.deepcopy(self.provider_snapshot),
            "quality_policy_version": self.quality_policy_version,
            "freshness_policy_version": self.freshness_policy_version,
            "transaction_cost_model": copy.deepcopy(self.transaction_cost_model),
            "slippage_model": copy.deepcopy(self.slippage_model),
            "benchmark_definition": copy.deepcopy(self.benchmark_definition),
            "created_at": self.created_at,
            "metadata": copy.deepcopy(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyRuleSnapshot":
        known = {f for f in cls.__dataclass_fields__}
        kwargs = {k: v for k, v in d.items() if k in known}
        return cls(**kwargs)


@dataclass
class BacktestConfiguration:
    backtest_id: str
    strategy_snapshot_id: str
    universe_id: str
    symbols: list
    market: str
    start_date: str
    end_date: str
    warmup_bars: int = 20
    initial_capital: float = 1_000_000.0
    position_size_mode: str = "equal_weight"
    max_positions: int = 10
    max_position_weight: float = 0.2
    transaction_cost_model: str = "taiwan_default"
    slippage_model: str = SlippageModelType.CONSERVATIVE_FIXED
    execution_model: str = ExecutionModelType.NEXT_OPEN
    benchmark: str = BenchmarkType.CASH
    train_period: Optional[dict] = None
    validation_period: Optional[dict] = None
    test_period: Optional[dict] = None
    walk_forward: bool = False
    random_seed: int = 42
    data_mode: str = "real"
    quality_profile: str = "backtest"
    dry_run: bool = True
    create_repair_tasks: bool = False
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "backtest_id": self.backtest_id,
            "strategy_snapshot_id": self.strategy_snapshot_id,
            "universe_id": self.universe_id,
            "symbols": self.symbols,
            "market": self.market,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "warmup_bars": self.warmup_bars,
            "initial_capital": self.initial_capital,
            "position_size_mode": self.position_size_mode,
            "max_positions": self.max_positions,
            "max_position_weight": self.max_position_weight,
            "transaction_cost_model": self.transaction_cost_model,
            "slippage_model": self.slippage_model,
            "execution_model": self.execution_model,
            "benchmark": self.benchmark,
            "train_period": self.train_period,
            "validation_period": self.validation_period,
            "test_period": self.test_period,
            "walk_forward": self.walk_forward,
            "random_seed": self.random_seed,
            "data_mode": self.data_mode,
            "quality_profile": self.quality_profile,
            "dry_run": self.dry_run,
            "create_repair_tasks": self.create_repair_tasks,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "BacktestConfiguration":
        known = {f for f in cls.__dataclass_fields__}
        kwargs = {k: v for k, v in d.items() if k in known}
        return cls(**kwargs)


@dataclass
class BacktestSignal:
    signal_id: str
    rule_id: str
    symbol: str
    signal_type: str
    signal_timestamp: str
    decision_timestamp: str
    intended_execution_timestamp: str
    strength: float = 0.0
    confidence: float = 0.0
    conditions_met: list = field(default_factory=list)
    conditions_failed: list = field(default_factory=list)
    input_snapshot: dict = field(default_factory=dict)
    quality_status: str = "unknown"
    freshness_status: str = "unknown"
    provenance: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "signal_id": self.signal_id,
            "rule_id": self.rule_id,
            "symbol": self.symbol,
            "signal_type": self.signal_type,
            "signal_timestamp": self.signal_timestamp,
            "decision_timestamp": self.decision_timestamp,
            "intended_execution_timestamp": self.intended_execution_timestamp,
            "strength": self.strength,
            "confidence": self.confidence,
            "conditions_met": self.conditions_met,
            "conditions_failed": self.conditions_failed,
            "input_snapshot": self.input_snapshot,
            "quality_status": self.quality_status,
            "freshness_status": self.freshness_status,
            "provenance": self.provenance,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "BacktestSignal":
        known = {f for f in cls.__dataclass_fields__}
        kwargs = {k: v for k, v in d.items() if k in known}
        return cls(**kwargs)


@dataclass
class SimulatedTrade:
    trade_id: str
    symbol: str
    rule_id: str
    entry_signal_id: str
    entry_date: str
    entry_price: float
    entry_cost: float = 0.0
    exit_date: str = ""
    exit_price: float = 0.0
    exit_cost: float = 0.0
    quantity: float = 0.0
    gross_return: float = 0.0
    net_return: float = 0.0
    pnl: float = 0.0
    holding_days: int = 0
    max_favorable_excursion: float = 0.0
    max_adverse_excursion: float = 0.0
    exit_reason: str = ""
    slippage: float = 0.0
    fees: float = 0.0
    taxes: float = 0.0
    provenance: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "trade_id": self.trade_id,
            "symbol": self.symbol,
            "rule_id": self.rule_id,
            "entry_signal_id": self.entry_signal_id,
            "entry_date": self.entry_date,
            "entry_price": self.entry_price,
            "entry_cost": self.entry_cost,
            "exit_date": self.exit_date,
            "exit_price": self.exit_price,
            "exit_cost": self.exit_cost,
            "quantity": self.quantity,
            "gross_return": self.gross_return,
            "net_return": self.net_return,
            "pnl": self.pnl,
            "holding_days": self.holding_days,
            "max_favorable_excursion": self.max_favorable_excursion,
            "max_adverse_excursion": self.max_adverse_excursion,
            "exit_reason": self.exit_reason,
            "slippage": self.slippage,
            "fees": self.fees,
            "taxes": self.taxes,
            "provenance": self.provenance,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "SimulatedTrade":
        known = {f for f in cls.__dataclass_fields__}
        kwargs = {k: v for k, v in d.items() if k in known}
        return cls(**kwargs)


@dataclass
class BacktestResult:
    backtest_id: str
    strategy_snapshot_id: str
    configuration: dict = field(default_factory=dict)
    status: str = BacktestStatus.BLOCKED
    symbols_requested: list = field(default_factory=list)
    symbols_tested: list = field(default_factory=list)
    symbols_blocked: list = field(default_factory=list)
    date_range: dict = field(default_factory=dict)
    trades: list = field(default_factory=list)
    trade_count: int = 0
    metrics: dict = field(default_factory=dict)
    benchmark_metrics: dict = field(default_factory=dict)
    validation_metrics: dict = field(default_factory=dict)
    quality_summary: dict = field(default_factory=dict)
    blocked_reasons: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    started_at: str = ""
    finished_at: str = ""
    reproducibility_hash: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "backtest_id": self.backtest_id,
            "strategy_snapshot_id": self.strategy_snapshot_id,
            "configuration": self.configuration,
            "status": self.status,
            "symbols_requested": self.symbols_requested,
            "symbols_tested": self.symbols_tested,
            "symbols_blocked": self.symbols_blocked,
            "date_range": self.date_range,
            "trades": self.trades,
            "trade_count": self.trade_count,
            "metrics": self.metrics,
            "benchmark_metrics": self.benchmark_metrics,
            "validation_metrics": self.validation_metrics,
            "quality_summary": self.quality_summary,
            "blocked_reasons": self.blocked_reasons,
            "warnings": self.warnings,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "reproducibility_hash": self.reproducibility_hash,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "BacktestResult":
        known = {f for f in cls.__dataclass_fields__}
        kwargs = {k: v for k, v in d.items() if k in known}
        return cls(**kwargs)


@dataclass
class BacktestPeriodSplit:
    train_start: str
    train_end: str
    validation_start: str
    validation_end: str
    test_start: str
    test_end: str
    embargo_days: int = 5
    purge_days: int = 5
    metadata: dict = field(default_factory=dict)

    def validate(self) -> list:
        """Return list of issues (empty = OK)."""
        from datetime import datetime
        issues = []
        try:
            ts = datetime.fromisoformat(self.train_start)
            te = datetime.fromisoformat(self.train_end)
            vs = datetime.fromisoformat(self.validation_start)
            ve = datetime.fromisoformat(self.validation_end)
            tes = datetime.fromisoformat(self.test_start)
            tee = datetime.fromisoformat(self.test_end)
            if te >= vs:
                issues.append("train_end overlaps validation_start")
            if ve >= tes:
                issues.append("validation_end overlaps test_start")
            if ts >= te:
                issues.append("train_start >= train_end")
            if vs >= ve:
                issues.append("validation_start >= validation_end")
            if tes >= tee:
                issues.append("test_start >= test_end")
        except Exception as exc:
            issues.append(f"Date parse error: {exc}")
        return issues

    def to_dict(self) -> dict:
        return {
            "train_start": self.train_start,
            "train_end": self.train_end,
            "validation_start": self.validation_start,
            "validation_end": self.validation_end,
            "test_start": self.test_start,
            "test_end": self.test_end,
            "embargo_days": self.embargo_days,
            "purge_days": self.purge_days,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "BacktestPeriodSplit":
        known = {f for f in cls.__dataclass_fields__}
        kwargs = {k: v for k, v in d.items() if k in known}
        return cls(**kwargs)


@dataclass
class WalkForwardFold:
    fold_id: str
    train_period: dict
    validation_period: dict
    test_period: dict
    rule_snapshot_id: str
    parameters: dict
    trades: list = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    confidence: str = ConfidenceLevel.INSUFFICIENT
    warnings: list = field(default_factory=list)
    status: str = BacktestStatus.BLOCKED
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "fold_id": self.fold_id,
            "train_period": self.train_period,
            "validation_period": self.validation_period,
            "test_period": self.test_period,
            "rule_snapshot_id": self.rule_snapshot_id,
            "parameters": self.parameters,
            "trades": self.trades,
            "metrics": self.metrics,
            "confidence": self.confidence,
            "warnings": self.warnings,
            "status": self.status,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "WalkForwardFold":
        known = {f for f in cls.__dataclass_fields__}
        kwargs = {k: v for k, v in d.items() if k in known}
        return cls(**kwargs)
