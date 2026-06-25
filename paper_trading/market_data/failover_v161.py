"""
paper_trading/market_data/failover_v161.py — Failover Policy v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
LIVE→FIXTURE failover: DISABLED.
LIVE→OFFLINE failover: DISABLED.
Only valid: PAUSE_ON_FAILURE or HALT_ON_FAILURE.
"""
from __future__ import annotations
from typing import Optional, Dict, Any

from paper_trading.market_data.enums_v161 import (
    FailoverPolicy, MarketDataSessionStatus, SourceClass,
)

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
LIVE_TO_FIXTURE_FAILOVER_DISABLED: bool = True
LIVE_TO_OFFLINE_FAILOVER_DISABLED: bool = True


class FailoverError(Exception):
    pass


class FailoverDecision:
    def __init__(
        self,
        action: str,
        new_status: MarketDataSessionStatus,
        reason: str,
        blocked: bool = False,
    ) -> None:
        self.action = action
        self.new_status = new_status
        self.reason = reason
        self.blocked = blocked


class FailoverManager:
    """
    Manages failover decisions on feed failure.
    LIVE→FIXTURE and LIVE→OFFLINE are BLOCKED.
    Valid actions: PAUSE (→PAUSED) or HALT (→HALTED).
    """

    def __init__(self, policy: FailoverPolicy) -> None:
        self._policy = policy

    @property
    def policy(self) -> FailoverPolicy:
        return self._policy

    def decide(
        self,
        current_source_class: SourceClass,
        proposed_failover_source: Optional[SourceClass] = None,
    ) -> FailoverDecision:
        """
        Decide what to do on failure.
        Blocks any attempt to failover LIVE→FIXTURE or LIVE→OFFLINE.
        """
        if proposed_failover_source is not None:
            if (current_source_class == SourceClass.LIVE_PUBLIC and
                    proposed_failover_source == SourceClass.FIXTURE):
                return FailoverDecision(
                    action="BLOCKED",
                    new_status=MarketDataSessionStatus.HALTED,
                    reason="LIVE→FIXTURE failover is DISABLED. LIVE_TO_FIXTURE_FAILOVER_DISABLED=True.",
                    blocked=True,
                )
            if (current_source_class == SourceClass.LIVE_PUBLIC and
                    proposed_failover_source == SourceClass.OFFLINE):
                return FailoverDecision(
                    action="BLOCKED",
                    new_status=MarketDataSessionStatus.HALTED,
                    reason="LIVE→OFFLINE failover is DISABLED. LIVE_TO_OFFLINE_FAILOVER_DISABLED=True.",
                    blocked=True,
                )

        if self._policy == FailoverPolicy.NO_FAILOVER:
            return FailoverDecision(
                action="NO_FAILOVER",
                new_status=MarketDataSessionStatus.HALTED,
                reason="FailoverPolicy=NO_FAILOVER: session halts on failure.",
            )
        elif self._policy == FailoverPolicy.PAUSE_ON_FAILURE:
            return FailoverDecision(
                action="PAUSE",
                new_status=MarketDataSessionStatus.PAUSED,
                reason="FailoverPolicy=PAUSE_ON_FAILURE: session pauses on failure.",
            )
        elif self._policy == FailoverPolicy.HALT_ON_FAILURE:
            return FailoverDecision(
                action="HALT",
                new_status=MarketDataSessionStatus.HALTED,
                reason="FailoverPolicy=HALT_ON_FAILURE: session halts on failure.",
            )

        return FailoverDecision(
            action="HALT",
            new_status=MarketDataSessionStatus.HALTED,
            reason="Unknown policy: defaulting to HALT.",
        )
