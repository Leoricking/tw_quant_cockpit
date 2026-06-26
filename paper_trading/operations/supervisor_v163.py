"""
Session Operations Supervisor v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
Supervisor must NOT: call Broker, create real orders, update real positions,
sync real accounts, write formal Portfolio Ledger, modify strategy rules,
modify investment decisions, auto-resume to RUNNING without policy.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from paper_trading.operations import (
    VERSION, NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED,
    PRODUCTION_TRADING_BLOCKED, AUTO_RESUME_RUNNING,
)
from paper_trading.operations.enums_v163 import (
    ManagedSessionType, OperationalStatus, HealthStatus,
)
from paper_trading.operations.models_v163 import _new_id, _now_utc
from paper_trading.operations.session_registry_v163 import SessionRegistry
from paper_trading.operations.operational_state_v163 import resolve_composite_status


SUPERVISOR_VERSION = "1.6.3"


class SessionOperationsSupervisor:
    """
    Coordinates Market Data, Paper Trading, Paper Strategy sessions.
    Creates Composite session.
    Aggregates state and health.
    Manages metrics, alerts, incidents, snapshots, checkpoints.
    Maintains audit trail.

    Safety invariants (permanently enforced):
    - NO_REAL_ORDERS = True
    - BROKER_EXECUTION_ENABLED = False
    - PRODUCTION_TRADING_BLOCKED = True
    - AUTO_RESUME_RUNNING = False
    """

    def __init__(self, supervisor_id: Optional[str] = None):
        self.supervisor_id  = supervisor_id or _new_id("sup_")
        self.version        = SUPERVISOR_VERSION
        self.created_at     = _now_utc()
        self._registry      = SessionRegistry(registry_id=self.supervisor_id)
        self._started       = False

        # Safety invariants — never mutable
        self._no_real_orders                = NO_REAL_ORDERS
        self._broker_execution_enabled      = BROKER_EXECUTION_ENABLED
        self._production_trading_blocked    = PRODUCTION_TRADING_BLOCKED
        self._auto_resume_running           = AUTO_RESUME_RUNNING

        assert self._no_real_orders,                    "NO_REAL_ORDERS must be True"
        assert not self._broker_execution_enabled,      "BROKER_EXECUTION_ENABLED must be False"
        assert self._production_trading_blocked,        "PRODUCTION_TRADING_BLOCKED must be True"
        assert not self._auto_resume_running,           "AUTO_RESUME_RUNNING must be False"

    def register_sessions(
        self,
        market_data_id:    str,
        paper_trading_id:  str,
        paper_strategy_id: str,
    ) -> Dict[str, str]:
        """Register the three managed sessions and composite."""
        results = {}
        for sid, stype in [
            (market_data_id,    ManagedSessionType.MARKET_DATA.value),
            (paper_trading_id,  ManagedSessionType.PAPER_TRADING.value),
            (paper_strategy_id, ManagedSessionType.PAPER_STRATEGY.value),
        ]:
            status, msg = self._registry.register(
                sid, stype, self.version,
                supervisor_id=self.supervisor_id,
            )
            results[sid] = status

        # Create composite
        composite_id = f"composite_{self.supervisor_id}"
        status, msg = self._registry.register(
            composite_id, ManagedSessionType.COMPOSITE.value, self.version,
            display_name="Composite Session",
            supervisor_id=self.supervisor_id,
        )
        results["composite"] = composite_id
        return results

    def get_composite_status(
        self,
        market_data:    OperationalStatus = OperationalStatus.UNINITIALIZED,
        paper_trading:  OperationalStatus = OperationalStatus.UNINITIALIZED,
        paper_strategy: OperationalStatus = OperationalStatus.UNINITIALIZED,
        *,
        safety_blocked: bool = False,
    ) -> Tuple[OperationalStatus, str]:
        return resolve_composite_status(
            market_data, paper_trading, paper_strategy,
            safety_blocked=safety_blocked,
        )

    def safety_contract(self) -> Dict[str, Any]:
        return {
            "NO_REAL_ORDERS":                   self._no_real_orders,
            "BROKER_EXECUTION_ENABLED":         self._broker_execution_enabled,
            "PRODUCTION_TRADING_BLOCKED":       self._production_trading_blocked,
            "AUTO_RESUME_RUNNING":              self._auto_resume_running,
            "version":                          self.version,
            "supervisor_id":                    self.supervisor_id,
        }

    def registry(self) -> SessionRegistry:
        return self._registry

    # Supervisor does NOT provide:
    # - call_broker()
    # - create_real_order()
    # - update_real_position()
    # - sync_real_account()
    # - write_formal_ledger()
    # - modify_strategy_rules()
    # - modify_investment_decision()


__all__ = ["SessionOperationsSupervisor", "SUPERVISOR_VERSION"]
