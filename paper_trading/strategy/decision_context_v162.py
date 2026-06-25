"""
paper_trading/strategy/decision_context_v162.py — Decision context builder for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from paper_trading.strategy.enums_v162 import ApprovalMode, EligibilityResult
from paper_trading.strategy.models_v162 import (
    DecisionContext,
    PaperSignal,
    StrategyConfig,
    _new_id,
    _now_iso,
)

logger = logging.getLogger(__name__)


def build_decision_context(
    signal: PaperSignal,
    strategy_config: StrategyConfig,
    market_open: bool = False,
    data_quality_ok: bool = False,
    pit_valid: bool = False,
    eligibility: EligibilityResult = EligibilityResult.UNCERTAIN,
    suggested_size: Optional[float] = None,
    correlation_breach: bool = False,
    risk_blocked: bool = False,
    conflict_tickers: Optional[List[str]] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> DecisionContext:
    """
    Build a DecisionContext for a signal.

    This is the input to the 19-step decision pipeline.
    All values are research/paper context — no real market data integration.
    """
    return DecisionContext(
        context_id=_new_id(),
        signal=signal,
        strategy_config=strategy_config,
        market_open=market_open,
        data_quality_ok=data_quality_ok,
        pit_valid=pit_valid,
        eligibility=eligibility.value,
        suggested_size=suggested_size,
        correlation_breach=correlation_breach,
        risk_blocked=risk_blocked,
        conflict_tickers=conflict_tickers or [],
        approval_mode=strategy_config.approval_mode.value,
        pipeline_step=0,
        pipeline_log=[],
        created_at=_now_iso(),
        extra=extra or {},
    )


class DecisionContextBuilder:
    """
    Fluent builder for DecisionContext.

    Useful for tests and manual pipeline invocation.
    """

    def __init__(
        self,
        signal: PaperSignal,
        strategy_config: StrategyConfig,
    ) -> None:
        self._signal = signal
        self._config = strategy_config
        self._market_open: bool = False
        self._data_quality_ok: bool = False
        self._pit_valid: bool = False
        self._eligibility: EligibilityResult = EligibilityResult.UNCERTAIN
        self._suggested_size: Optional[float] = None
        self._correlation_breach: bool = False
        self._risk_blocked: bool = False
        self._conflict_tickers: List[str] = []
        self._extra: Dict[str, Any] = {}

    def with_market_open(self, value: bool = True) -> "DecisionContextBuilder":
        self._market_open = value
        return self

    def with_data_quality_ok(self, value: bool = True) -> "DecisionContextBuilder":
        self._data_quality_ok = value
        return self

    def with_pit_valid(self, value: bool = True) -> "DecisionContextBuilder":
        self._pit_valid = value
        return self

    def with_eligibility(self, result: EligibilityResult) -> "DecisionContextBuilder":
        self._eligibility = result
        return self

    def with_suggested_size(self, size: float) -> "DecisionContextBuilder":
        self._suggested_size = size
        return self

    def with_correlation_breach(self, value: bool = True) -> "DecisionContextBuilder":
        self._correlation_breach = value
        return self

    def with_risk_blocked(self, value: bool = True) -> "DecisionContextBuilder":
        self._risk_blocked = value
        return self

    def with_conflict_tickers(self, tickers: List[str]) -> "DecisionContextBuilder":
        self._conflict_tickers = list(tickers)
        return self

    def with_extra(self, key: str, value: Any) -> "DecisionContextBuilder":
        self._extra[key] = value
        return self

    def build(self) -> DecisionContext:
        return build_decision_context(
            signal=self._signal,
            strategy_config=self._config,
            market_open=self._market_open,
            data_quality_ok=self._data_quality_ok,
            pit_valid=self._pit_valid,
            eligibility=self._eligibility,
            suggested_size=self._suggested_size,
            correlation_breach=self._correlation_breach,
            risk_blocked=self._risk_blocked,
            conflict_tickers=self._conflict_tickers,
            extra=self._extra,
        )
