"""
quality_gates.gate_override — QualityGateOverrideManager v1.1.4

Research-only. Override is disabled by default. Only allows downgrade of
BLOCKED → OBSERVATIONAL for research purposes. NEVER enables trading.
BLOCKED_MOCK_DATA, BLOCKED_INVALID_DATA, BLOCKED_CONFLICT cannot be
overridden to FORMAL.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
OVERRIDE_DISABLED_BY_DEFAULT = True


class QualityGateOverrideManager:
    """Manages research-only gate overrides. Override is DISABLED by default."""

    OVERRIDE_DISABLED_BY_DEFAULT = True

    # Decisions that can NEVER be overridden to FORMAL
    UNOVERRIDABLE_TO_FORMAL = [
        "BLOCKED_MOCK_DATA",
        "BLOCKED_INVALID_DATA",
        "BLOCKED_CONFLICT",
    ]

    # Reason codes that prevent formal override
    BLOCKING_REASON_CODES_FOR_FORMAL = [
        "FUTURE_DATE", "DATE_REGRESSION", "INVALID_OHLC",
        "CONFLICTING_ROWS", "MOCK_SOURCE", "FIXTURE_SOURCE",
    ]

    def __init__(self):
        self._overrides: List[Dict] = []

    def request_override(self, decision_id: str, requested_level: str,
                         reason: str, allow_override: bool = False):
        """Request a gate override. Requires explicit allow_override=True.
        Result is always OBSERVATIONAL max — never FORMAL for blocked data.
        Override does NOT affect broker execution or VALIDATED safety."""
        from quality_gates.gate_schema import GateOverrideRecord, GATE_LEVEL_FORMAL, GATE_LEVEL_OBSERVATIONAL

        if not allow_override:
            raise ValueError(
                "Gate override is DISABLED by default. Pass --allow-research-override explicitly."
            )

        if requested_level == GATE_LEVEL_FORMAL:
            raise ValueError(
                f"Override to FORMAL is not permitted. Max override level is OBSERVATIONAL. "
                f"This protects research integrity. Override does NOT enable trading."
            )

        rec = GateOverrideRecord(
            decision_id=decision_id,
            requested_decision=requested_level,
            reason=reason,
            approved=False,
            approval_note="Pending audit review. Override is research-only.",
            audit_only=True,
            research_only=True,
            no_real_orders=True,
        )
        self._overrides.append(rec.to_dict())
        logger.info("Override requested for decision %s → %s (audit only, research only)",
                    decision_id, requested_level)
        return rec

    def validate_override_request(self, original_decision: str,
                                   requested_level: str) -> Tuple[bool, str]:
        """Returns (valid, reason_message). Validates override is permitted."""
        from quality_gates.gate_schema import GATE_LEVEL_FORMAL

        if original_decision in self.UNOVERRIDABLE_TO_FORMAL and requested_level == GATE_LEVEL_FORMAL:
            return False, (
                f"{original_decision} cannot be overridden to FORMAL. "
                f"Mock data, invalid data, and conflict data cannot pass formal gate."
            )
        if requested_level == GATE_LEVEL_FORMAL:
            return False, "Override to FORMAL is not permitted for any blocked decision."
        return True, "Override to OBSERVATIONAL is permitted (audit only, research only)."

    def record_override(self, override_record) -> Dict:
        """Record an approved override. Returns the record dict."""
        d = override_record.to_dict() if hasattr(override_record, "to_dict") else override_record
        self._overrides.append(d)
        return d

    def list_overrides(self) -> List[Dict]:
        """Return all recorded overrides."""
        return list(self._overrides)

    def expire_override(self, override_id: str) -> bool:
        """Mark an override as expired."""
        for rec in self._overrides:
            if rec.get("override_id") == override_id:
                rec["approval_note"] = "EXPIRED — " + rec.get("approval_note", "")
                return True
        return False

    def explain_override(self, override_id: str) -> str:
        """Return a human-readable explanation of an override."""
        for rec in self._overrides:
            if rec.get("override_id") == override_id:
                return (
                    f"Override {override_id}\n"
                    f"  Decision: {rec.get('decision_id', '?')}\n"
                    f"  Symbol: {rec.get('symbol', '?')}\n"
                    f"  Original: {rec.get('original_decision', '?')}\n"
                    f"  Requested: {rec.get('requested_decision', '?')}\n"
                    f"  Reason: {rec.get('reason', '?')}\n"
                    f"  Approved: {rec.get('approved', False)}\n"
                    f"  Audit Only: {rec.get('audit_only', True)}\n"
                    f"  [!] Override is research-only. Does NOT enable trading."
                )
        return f"Override {override_id} not found."
