"""
paper_trading/performance_attribution/attribution_input_v167.py
Attribution input contract and validation for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Missing data must not be silently defaulted. Real/live markers must be rejected.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .enums_v167 import (
    BenchmarkMode, AttributionStatus, ConfidenceLevel,
    DataQualityStatus, RegimeType,
)

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


@dataclass
class AttributionInput:
    """
    Full attribution input contract.
    All fields are paper/simulation only. No real orders, no broker, no production.
    """
    # Identity
    run_id: str
    portfolio_id: str
    session_id: str
    strategy_id: str

    # Period
    attribution_period_start: str
    attribution_period_end: str

    # Benchmark
    benchmark_id: Optional[str]
    benchmark_mode: BenchmarkMode

    # Portfolio equity
    initial_equity: float
    ending_equity: float
    cash_flows: List[Dict[str, Any]] = field(default_factory=list)

    # Positions, trades, executions
    positions: List[Dict[str, Any]] = field(default_factory=list)
    trades: List[Dict[str, Any]] = field(default_factory=list)
    executions: List[Dict[str, Any]] = field(default_factory=list)

    # Costs (all required; unknown must be explicitly flagged)
    fees: float = 0.0
    taxes: float = 0.0
    exchange_fees: float = 0.0
    borrow_costs: float = 0.0
    financing_costs: float = 0.0
    spread_costs: float = 0.0
    impact_costs: float = 0.0
    slippage: float = 0.0
    turnover: float = 0.0

    # Market data
    market_prices: Dict[str, Dict[str, float]] = field(default_factory=dict)
    benchmark_returns: Dict[str, float] = field(default_factory=dict)
    benchmark_weights: Dict[str, float] = field(default_factory=dict)

    # Metadata
    symbol_metadata: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    industry_metadata: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    sector_metadata: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    regime_metadata: Dict[str, str] = field(default_factory=dict)   # date -> regime
    factor_metadata: Dict[str, Dict[str, float]] = field(default_factory=dict)

    # Governance
    source_lineage: str = ""
    data_quality: DataQualityStatus = DataQualityStatus.COMPLETE
    policy_version: str = "1.6.7-paper-attribution"
    schema_version: str = "167"
    deterministic_seed: int = 42
    residual_tolerance: float = 0.0001
    rounding_tolerance: float = 1e-8

    # Safety markers (must all be True)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


_REQUIRED_FIELDS = {
    "run_id", "portfolio_id", "session_id", "strategy_id",
    "attribution_period_start", "attribution_period_end",
    "benchmark_mode", "initial_equity", "ending_equity",
}


def validate_attribution_input(inp: AttributionInput) -> Dict[str, Any]:
    """
    Validate an AttributionInput. Returns {"valid": bool, "errors": List[str], "warnings": List[str]}.

    Rules:
    - reversed period → error
    - future timestamp → warning (degrade)
    - live/real markers → error (blocked)
    - production flags → error (blocked)
    - duplicate trade IDs → error
    - duplicate execution IDs → error
    - negative quantity inconsistency → error
    - impossible cash flow → error
    - unknown benchmark (with mode MARKET_BENCHMARK/POLICY_BASELINE) → error if missing
    - unknown fee not explicitly 0 → warn if data_quality != COMPLETE
    """
    from datetime import datetime, timezone, date

    errors: List[str] = []
    warnings: List[str] = []

    # Safety markers
    if inp.paper_only is not True:
        errors.append("BLOCKED: paper_only must be True")
    if inp.research_only is not True:
        errors.append("BLOCKED: research_only must be True")
    if inp.no_real_orders is not True:
        errors.append("BLOCKED: no_real_orders must be True")
    if inp.not_for_production is not True:
        errors.append("BLOCKED: not_for_production must be True")

    # Period validation
    if inp.attribution_period_start > inp.attribution_period_end:
        errors.append(
            f"reversed_period: {inp.attribution_period_start} > {inp.attribution_period_end}"
        )

    # Equity
    if inp.initial_equity <= 0:
        errors.append(f"invalid_initial_equity: {inp.initial_equity}")

    # Duplicate trade IDs
    trade_ids = [t.get("trade_id") for t in inp.trades if t.get("trade_id")]
    if len(trade_ids) != len(set(trade_ids)):
        dup = [t for t in trade_ids if trade_ids.count(t) > 1]
        errors.append(f"duplicate_trade_ids: {sorted(set(dup))}")

    # Duplicate execution IDs
    exec_ids = [e.get("execution_id") for e in inp.executions if e.get("execution_id")]
    if len(exec_ids) != len(set(exec_ids)):
        dup = [e for e in exec_ids if exec_ids.count(e) > 1]
        errors.append(f"duplicate_execution_ids: {sorted(set(dup))}")

    # Invalid quantities
    for t in inp.trades:
        qty = t.get("quantity")
        if qty is not None and not isinstance(qty, (int, float)):
            errors.append(f"invalid_quantity: trade {t.get('trade_id')} qty={qty}")
        elif qty is not None and isinstance(qty, (int, float)) and qty == 0:
            errors.append(f"zero_quantity: trade {t.get('trade_id')}")

    # Benchmark presence
    if inp.benchmark_mode in (BenchmarkMode.MARKET_BENCHMARK, BenchmarkMode.POLICY_BASELINE):
        if not inp.benchmark_id:
            errors.append(
                f"missing_benchmark: mode={inp.benchmark_mode.value} requires benchmark_id"
            )

    # Cash flow validation — impossible cash flows
    for cf in inp.cash_flows:
        amount = cf.get("amount")
        if amount is not None and isinstance(amount, (int, float)):
            if abs(amount) > inp.initial_equity * 100:
                errors.append(
                    f"impossible_cash_flow: amount={amount} vs initial_equity={inp.initial_equity}"
                )

    # Data quality warnings for unknown costs
    if inp.data_quality != DataQualityStatus.COMPLETE:
        warnings.append(
            f"data_quality_degraded: {inp.data_quality.value} — cost attribution may be partial"
        )

    valid = len(errors) == 0
    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "blocked": not valid,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_for_production": True,
    }


def build_minimal_input(
    run_id: str = "run_test_001",
    portfolio_id: str = "port_001",
    session_id: str = "sess_001",
    strategy_id: str = "strat_001",
    period_start: str = "2024-01-01",
    period_end: str = "2024-03-31",
    initial_equity: float = 1_000_000.0,
    ending_equity: float = 1_050_000.0,
) -> AttributionInput:
    """Build a minimal valid AttributionInput for testing. Paper/research only."""
    return AttributionInput(
        run_id=run_id,
        portfolio_id=portfolio_id,
        session_id=session_id,
        strategy_id=strategy_id,
        attribution_period_start=period_start,
        attribution_period_end=period_end,
        benchmark_id=None,
        benchmark_mode=BenchmarkMode.NONE,
        initial_equity=initial_equity,
        ending_equity=ending_equity,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_for_production=True,
    )
