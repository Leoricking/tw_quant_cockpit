"""paper_trading/audit_v160.py — Paper Trading Audit Trail v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
Append-only audit records. No credential storage.
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class AuditRecord:
    audit_id: str
    session_id: str
    actor: str
    action: str
    timestamp: str
    reason: str = ""
    before: Optional[Any] = None
    after: Optional[Any] = None
    event_id: str = ""
    order_id: str = ""
    code_version: str = "1.6.0"
    policy_versions: Dict[str, str] = field(default_factory=dict)
    data_source: str = ""
    data_mode: str = ""
    safety_flags: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    # No credentials stored


class PaperAuditTrail:
    """Append-only audit trail for paper session state changes."""

    def __init__(self, session_id: str, code_version: str = "1.6.0") -> None:
        self._session_id = session_id
        self._code_version = code_version
        self._records: List[AuditRecord] = []

    def record(
        self,
        actor: str,
        action: str,
        reason: str = "",
        before: Optional[Any] = None,
        after: Optional[Any] = None,
        event_id: str = "",
        order_id: str = "",
        data_source: str = "",
        data_mode: str = "",
        policy_versions: Optional[Dict[str, str]] = None,
        safety_flags: Optional[Dict[str, Any]] = None,
    ) -> AuditRecord:
        from paper_trading import (
            NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
        )
        rec = AuditRecord(
            audit_id=f"aud_{uuid.uuid4().hex[:12]}",
            session_id=self._session_id,
            actor=actor,
            action=action,
            timestamp=datetime.now(timezone.utc).isoformat(),
            reason=reason,
            before=before,
            after=after,
            event_id=event_id,
            order_id=order_id,
            code_version=self._code_version,
            policy_versions=policy_versions or {},
            data_source=data_source,
            data_mode=data_mode,
            safety_flags=safety_flags or {
                "NO_REAL_ORDERS": NO_REAL_ORDERS,
                "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
                "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
            },
        )
        self._records.append(rec)
        return rec

    def get_records(self) -> List[AuditRecord]:
        return list(self._records)

    def count(self) -> int:
        return len(self._records)
