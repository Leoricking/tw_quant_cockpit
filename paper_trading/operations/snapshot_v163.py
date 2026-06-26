"""
Operational Snapshot v1.6.3 — Immutable, deterministic hash.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
No credentials. No runtime machine path.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from paper_trading.operations.enums_v163 import OperationalStatus, HealthStatus
from paper_trading.operations.models_v163 import OperationalSnapshot, _new_id, _now_utc, _semantic_hash


class SnapshotService:
    """Creates and verifies operational snapshots."""

    def create(
        self,
        supervisor_id:         str,
        market_data_status:    OperationalStatus,
        paper_trading_status:  OperationalStatus,
        paper_strategy_status: OperationalStatus,
        composite_status:      OperationalStatus,
        composite_health:      HealthStatus,
        metrics:               Optional[Dict[str, Any]] = None,
        alerts:                Optional[List[str]]      = None,
        incidents:             Optional[List[str]]      = None,
        kill_switch:           bool                     = False,
        policy_versions:       Optional[Dict[str, str]] = None,
        lineage_ids:           Optional[List[str]]      = None,
        metadata:              Optional[Dict[str, Any]] = None,
    ) -> OperationalSnapshot:
        snap = OperationalSnapshot(
            snapshot_id=_new_id("snap_"),
            supervisor_id=supervisor_id,
            captured_at=_now_utc(),
            market_data_status=market_data_status,
            paper_trading_status=paper_trading_status,
            paper_strategy_status=paper_strategy_status,
            composite_status=composite_status,
            composite_health=composite_health,
            metrics=metrics or {},
            alerts=alerts or [],
            incidents=incidents or [],
            kill_switch_status=kill_switch,
            safety_contract=self._safety_contract(),
            policy_versions=policy_versions or {"default": "1.6.3"},
            lineage_ids=lineage_ids or [],
            metadata=metadata or {},
        )
        # Compute semantic hash
        snap.content_hash = _semantic_hash({
            "snapshot_id":           snap.snapshot_id,
            "supervisor_id":         supervisor_id,
            "composite_status":      str(composite_status),
            "composite_health":      str(composite_health),
            "market_data_status":    str(market_data_status),
            "paper_trading_status":  str(paper_trading_status),
            "paper_strategy_status": str(paper_strategy_status),
            "kill_switch_status":    kill_switch,
            "alert_count":           len(alerts or []),
            "incident_count":        len(incidents or []),
        })
        return snap

    def verify(self, snapshot: OperationalSnapshot) -> bool:
        recomputed = _semantic_hash({
            "snapshot_id":           snapshot.snapshot_id,
            "supervisor_id":         snapshot.supervisor_id,
            "composite_status":      str(snapshot.composite_status),
            "composite_health":      str(snapshot.composite_health),
            "market_data_status":    str(snapshot.market_data_status),
            "paper_trading_status":  str(snapshot.paper_trading_status),
            "paper_strategy_status": str(snapshot.paper_strategy_status),
            "kill_switch_status":    snapshot.kill_switch_status,
            "alert_count":           len(snapshot.alerts),
            "incident_count":        len(snapshot.incidents),
        })
        return recomputed == snapshot.content_hash

    def _safety_contract(self) -> Dict[str, Any]:
        from paper_trading.operations import (
            NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED,
            PRODUCTION_TRADING_BLOCKED, REAL_PORTFOLIO_LEDGER_WRITE_ENABLED,
        )
        return {
            "NO_REAL_ORDERS":                   NO_REAL_ORDERS,
            "BROKER_EXECUTION_ENABLED":         BROKER_EXECUTION_ENABLED,
            "PRODUCTION_TRADING_BLOCKED":       PRODUCTION_TRADING_BLOCKED,
            "REAL_PORTFOLIO_LEDGER_WRITE_ENABLED": REAL_PORTFOLIO_LEDGER_WRITE_ENABLED,
            "version":                          "1.6.3",
        }


__all__ = ["SnapshotService"]
