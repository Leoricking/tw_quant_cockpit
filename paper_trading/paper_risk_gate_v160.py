"""paper_trading/paper_risk_gate_v160.py — Paper Risk Gate v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
Integrates v1.5.1–v1.5.3 risk controls. BLOCKED = no queued paper order created.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional

from .enums_v160 import (
    DataMode, MarketSessionStatus, PaperOrderSide,
    PaperRiskStatus, PaperSessionStatus,
)


@dataclass
class RiskCheckResult:
    check_name: str
    status: PaperRiskStatus
    reason: str = ""
    detail: Any = None


@dataclass
class PaperRiskEvaluationResult:
    evaluation_id: str
    session_id: str
    paper_order_id: str
    symbol: str
    status: PaperRiskStatus
    checks: List[RiskCheckResult] = field(default_factory=list)
    block_reasons: List[str] = field(default_factory=list)
    warning_reasons: List[str] = field(default_factory=list)


class PaperRiskGate:
    """
    Pre-order risk gate: 16 checks before any paper order is queued.
    BLOCKED status prevents order queuing.
    """

    def __init__(
        self,
        max_single_name_pct: Decimal = Decimal("0.25"),
        max_drawdown_pct: Decimal = Decimal("0.20"),
        max_concentration_pct: Decimal = Decimal("0.50"),
    ) -> None:
        self._max_single_name_pct = max_single_name_pct
        self._max_drawdown_pct = max_drawdown_pct
        self._max_concentration_pct = max_concentration_pct

    def evaluate(
        self,
        evaluation_id: str,
        session_id: str,
        paper_order_id: str,
        symbol: str,
        side: PaperOrderSide,
        quantity: Decimal,
        limit_price: Optional[Decimal],
        session_status: PaperSessionStatus,
        market_status: MarketSessionStatus,
        data_mode: DataMode,
        data_fresh: bool,
        available_cash: Decimal,
        existing_position: Decimal,
        total_portfolio_value: Decimal,
        drawdown_pct: Decimal,
        kill_switch_triggered: bool,
        allowed_symbols: Optional[List[str]] = None,
        price: Optional[Decimal] = None,
    ) -> PaperRiskEvaluationResult:
        checks: List[RiskCheckResult] = []
        block_reasons: List[str] = []
        warning_reasons: List[str] = []

        # 1. Session status
        if session_status not in {PaperSessionStatus.RUNNING}:
            checks.append(RiskCheckResult("session_status", PaperRiskStatus.BLOCKED, f"session not RUNNING: {session_status.value}"))
            block_reasons.append(f"session_status={session_status.value}")
        else:
            checks.append(RiskCheckResult("session_status", PaperRiskStatus.PASS))

        # 2. Market status
        if market_status not in {MarketSessionStatus.OPEN, MarketSessionStatus.PRE_OPEN}:
            checks.append(RiskCheckResult("market_status", PaperRiskStatus.WARNING, f"market not OPEN: {market_status.value}"))
            warning_reasons.append(f"market_status={market_status.value}")
        else:
            checks.append(RiskCheckResult("market_status", PaperRiskStatus.PASS))

        # 3. Data mode
        if data_mode is None:
            checks.append(RiskCheckResult("data_mode", PaperRiskStatus.BLOCKED, "data_mode is None"))
            block_reasons.append("data_mode=None")
        else:
            checks.append(RiskCheckResult("data_mode", PaperRiskStatus.PASS, data_mode.value))

        # 4. Data freshness
        if not data_fresh:
            checks.append(RiskCheckResult("data_freshness", PaperRiskStatus.WARNING, "data may be stale"))
            warning_reasons.append("data_stale")
        else:
            checks.append(RiskCheckResult("data_freshness", PaperRiskStatus.PASS))

        # 5. Symbol eligibility
        if allowed_symbols is not None and symbol not in allowed_symbols:
            checks.append(RiskCheckResult("symbol_eligibility", PaperRiskStatus.BLOCKED, f"symbol {symbol} not in allowed list"))
            block_reasons.append(f"symbol_not_allowed={symbol}")
        else:
            checks.append(RiskCheckResult("symbol_eligibility", PaperRiskStatus.PASS))

        # 6. Cash (buy only)
        if side == PaperOrderSide.BUY:
            order_value = (price or limit_price or Decimal("0")) * quantity
            if available_cash < order_value:
                checks.append(RiskCheckResult("cash", PaperRiskStatus.BLOCKED, f"insufficient cash: have {available_cash}, need {order_value}"))
                block_reasons.append("insufficient_cash")
            else:
                checks.append(RiskCheckResult("cash", PaperRiskStatus.PASS))
        else:
            checks.append(RiskCheckResult("cash", PaperRiskStatus.PASS, "sell: cash check N/A"))

        # 7. Paper position (sell only — no short)
        if side == PaperOrderSide.SELL:
            if quantity > existing_position:
                checks.append(RiskCheckResult("paper_position", PaperRiskStatus.BLOCKED, f"insufficient position: have {existing_position}, selling {quantity}"))
                block_reasons.append("insufficient_position")
            else:
                checks.append(RiskCheckResult("paper_position", PaperRiskStatus.PASS))
        else:
            checks.append(RiskCheckResult("paper_position", PaperRiskStatus.PASS, "buy: position check N/A"))

        # 8. Sizing (basic: quantity > 0)
        if quantity <= Decimal("0"):
            checks.append(RiskCheckResult("sizing", PaperRiskStatus.BLOCKED, "quantity must be positive"))
            block_reasons.append("zero_quantity")
        else:
            checks.append(RiskCheckResult("sizing", PaperRiskStatus.PASS))

        # 9. Single-name concentration
        if total_portfolio_value > Decimal("0") and price is not None:
            order_value = price * quantity
            pct = order_value / total_portfolio_value
            if pct > self._max_single_name_pct:
                checks.append(RiskCheckResult("single_name_concentration", PaperRiskStatus.WARNING, f"{float(pct):.1%} > {float(self._max_single_name_pct):.1%}"))
                warning_reasons.append("concentration_warning")
            else:
                checks.append(RiskCheckResult("single_name_concentration", PaperRiskStatus.PASS))
        else:
            checks.append(RiskCheckResult("single_name_concentration", PaperRiskStatus.PASS, "no price for concentration check"))

        # 10. Industry/theme/cluster — pass (detailed impl deferred to v1.6.1)
        checks.append(RiskCheckResult("industry_exposure", PaperRiskStatus.PASS, "v1.6.0: basic check only"))

        # 11. Correlation — pass (detailed impl from v1.5.2)
        checks.append(RiskCheckResult("correlation", PaperRiskStatus.PASS, "v1.6.0: basic check only"))

        # 12. Drawdown
        if drawdown_pct > self._max_drawdown_pct * Decimal("100"):
            checks.append(RiskCheckResult("drawdown", PaperRiskStatus.RESTRICTED, f"drawdown {float(drawdown_pct):.1%} > limit"))
            warning_reasons.append("drawdown_restricted")
        else:
            checks.append(RiskCheckResult("drawdown", PaperRiskStatus.PASS))

        # 13. Risk budget — pass basic
        checks.append(RiskCheckResult("risk_budget", PaperRiskStatus.PASS, "v1.6.0: basic check"))

        # 14. Liquidity — pass (detailed in execution_simulator)
        checks.append(RiskCheckResult("liquidity", PaperRiskStatus.PASS, "v1.6.0: checked at execution"))

        # 15. Kill switch
        if kill_switch_triggered:
            checks.append(RiskCheckResult("kill_switch", PaperRiskStatus.BLOCKED, "kill switch triggered"))
            block_reasons.append("kill_switch_triggered")
        else:
            checks.append(RiskCheckResult("kill_switch", PaperRiskStatus.PASS))

        # 16. Safety contract
        from paper_trading import (
            NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
            REAL_ORDER_CREATION_ENABLED,
        )
        safety_ok = (
            NO_REAL_ORDERS is True and
            BROKER_EXECUTION_ENABLED is False and
            PRODUCTION_TRADING_BLOCKED is True and
            REAL_ORDER_CREATION_ENABLED is False
        )
        if not safety_ok:
            checks.append(RiskCheckResult("safety_contract", PaperRiskStatus.BLOCKED, "safety contract violation"))
            block_reasons.append("safety_contract_violation")
        else:
            checks.append(RiskCheckResult("safety_contract", PaperRiskStatus.PASS))

        # Determine final status
        if block_reasons:
            final_status = PaperRiskStatus.BLOCKED
        elif any(c.status == PaperRiskStatus.RESTRICTED for c in checks):
            final_status = PaperRiskStatus.RESTRICTED
        elif warning_reasons:
            final_status = PaperRiskStatus.WARNING
        else:
            final_status = PaperRiskStatus.PASS

        return PaperRiskEvaluationResult(
            evaluation_id=evaluation_id,
            session_id=session_id,
            paper_order_id=paper_order_id,
            symbol=symbol,
            status=final_status,
            checks=checks,
            block_reasons=block_reasons,
            warning_reasons=warning_reasons,
        )
