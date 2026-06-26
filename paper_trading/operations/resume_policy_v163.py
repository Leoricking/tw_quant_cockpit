"""
Resume Policy v1.6.3 — Pre-flight checks mandatory.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from paper_trading.operations.enums_v163 import OperationalStatus, HealthStatus


BLOCKED       = "RESUME_BLOCKED"
RESUME_OK     = "RESUMED"


@dataclass
class ResumeResult:
    success:        bool
    status:         str
    session_id:     str
    message:        str
    blocked_checks: List[str] = field(default_factory=list)


class ResumePolicy:
    """
    Resume pre-checks (spec §二十八):
    - previous status PAUSED or RECOVERED
    - dependencies healthy
    - Market Data valid
    - Paper Trading valid
    - Strategy valid
    - no critical alerts
    - no unresolved critical incidents
    - kill switch inactive
    - checkpoint valid
    - lineage valid
    - safety contract valid

    Any failure → RESUME_BLOCKED (no auto-bypass).
    """

    def execute(
        self,
        session_id:              str,
        current_status:          OperationalStatus,
        *,
        dependency_health:       HealthStatus = HealthStatus.HEALTHY,
        market_data_valid:       bool         = True,
        paper_trading_valid:     bool         = True,
        strategy_valid:          bool         = True,
        critical_alerts:         int          = 0,
        critical_incidents:      int          = 0,
        kill_switch_active:      bool         = False,
        checkpoint_valid:        bool         = True,
        lineage_valid:           bool         = True,
        safety_contract_valid:   bool         = True,
    ) -> ResumeResult:
        blocks = []

        if current_status not in (OperationalStatus.PAUSED, OperationalStatus.RECOVERED):
            blocks.append(f"previous_status={current_status} — must be PAUSED or RECOVERED")

        if dependency_health in (HealthStatus.CRITICAL, HealthStatus.BLOCKED, HealthStatus.UNHEALTHY):
            blocks.append(f"dependency_health={dependency_health}")

        if not market_data_valid:
            blocks.append("market_data_not_valid")

        if not paper_trading_valid:
            blocks.append("paper_trading_not_valid")

        if not strategy_valid:
            blocks.append("strategy_not_valid")

        if critical_alerts > 0:
            blocks.append(f"critical_alerts={critical_alerts}")

        if critical_incidents > 0:
            blocks.append(f"unresolved_critical_incidents={critical_incidents}")

        if kill_switch_active:
            blocks.append("kill_switch_active")

        if not checkpoint_valid:
            blocks.append("checkpoint_invalid")

        if not lineage_valid:
            blocks.append("lineage_invalid")

        if not safety_contract_valid:
            blocks.append("safety_contract_invalid")

        if blocks:
            return ResumeResult(
                success=False,
                status=BLOCKED,
                session_id=session_id,
                message=f"Resume blocked: {'; '.join(blocks)}",
                blocked_checks=blocks,
            )

        return ResumeResult(
            success=True,
            status=RESUME_OK,
            session_id=session_id,
            message=f"Session {session_id} resumed",
        )


__all__ = ["ResumePolicy", "ResumeResult", "BLOCKED", "RESUME_OK"]
