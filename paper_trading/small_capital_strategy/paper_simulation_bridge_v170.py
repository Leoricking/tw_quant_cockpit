"""
paper_trading/small_capital_strategy/paper_simulation_bridge_v170.py
Paper simulation bridge for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
Fixture/mock result. Does NOT connect to live systems, broker, or real accounts.
"""
from __future__ import annotations
from typing import Any, Dict, Optional

from paper_trading.small_capital_strategy.enums_v170 import (
    BuyPointType, MarketRegime, AllocationBucket,
)
from paper_trading.small_capital_strategy.models_v170 import (
    SmallCapitalSimulationInput, SmallCapitalSimulationResult,
)
from paper_trading.small_capital_strategy.position_sizing_v170 import (
    compute_position_size, PositionSizingInput,
)
from paper_trading.small_capital_strategy.stop_loss_plan_v170 import build_stop_loss_plan

# Safety: always False
_REAL_EXECUTION = False
_BROKER_CONNECTED = False
_LIVE_ACCOUNT = False


def run_paper_simulation(inp: SmallCapitalSimulationInput) -> SmallCapitalSimulationResult:
    """
    Run a paper simulation for a trade setup.
    Uses position sizing formula: position_size = max_loss / stop_loss_pct.
    Paper only — never executes real orders.
    """
    assert not _REAL_EXECUTION, "Real execution must never be enabled"
    assert not _BROKER_CONNECTED, "Broker must never be connected"
    assert not _LIVE_ACCOUNT, "Live account must never be used"

    # Compute position size
    from paper_trading.small_capital_strategy.capital_profile_v170 import (
        TEMPLATE_300K_MAX_LOSS_DEFAULT,
    )
    max_loss = TEMPLATE_300K_MAX_LOSS_DEFAULT
    bucket_budget = inp.capital_twd * 0.35  # conservative bucket

    sizing_input = PositionSizingInput(
        symbol=inp.symbol,
        capital_twd=inp.capital_twd,
        max_loss_amount=max_loss,
        stop_loss_pct=inp.stop_loss_pct,
        bucket=AllocationBucket.MAIN_THEME_SWING,
        bucket_remaining_budget=bucket_budget,
    )
    sizing = compute_position_size(sizing_input)

    # Compute stop loss price
    stop_price = inp.entry_price * (1.0 - inp.stop_loss_pct) if inp.stop_loss_pct > 0 else 0.0

    return SmallCapitalSimulationResult(
        template_id=inp.template_id,
        symbol=inp.symbol,
        position_size_twd=sizing.position_size_twd,
        stop_loss_price=round(stop_price, 2),
        status=sizing.status,
    )


def get_simulation_safety_summary() -> Dict[str, Any]:
    """Return simulation safety summary."""
    return {
        "real_execution_enabled": _REAL_EXECUTION,
        "broker_connected": _BROKER_CONNECTED,
        "live_account_enabled": _LIVE_ACCOUNT,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }
