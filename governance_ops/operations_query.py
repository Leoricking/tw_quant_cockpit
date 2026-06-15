"""
governance_ops.operations_query — OperationsQuery v1.1.6

Query functions for governance operations runtime data.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from governance_ops.governance_schema import (
    GovernanceSummary,
    GovernanceModuleStatus,
    GovernanceSymbolStatus,
    GovernanceActionItem,
    GovernanceRunSummary,
)
from governance_ops.operations_store import OperationsStore
from governance_ops.priority_engine import GovernancePriorityEngine

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class OperationsQuery:
    """Query API for governance operations runtime data."""

    def __init__(self):
        self._store = OperationsStore()
        self._engine = GovernancePriorityEngine()

    def latest_summary(self) -> Optional[GovernanceSummary]:
        """Return latest governance summary, or None if not available."""
        data = self._store.load_summary()
        if not data:
            return None
        try:
            return GovernanceSummary.from_dict(data)
        except Exception as exc:
            logger.warning("latest_summary parse error: %s", exc)
            return None

    def module_health(self) -> List[GovernanceModuleStatus]:
        """Return list of module health statuses."""
        rows = self._store.load_module_health()
        result = []
        for row in rows:
            try:
                result.append(GovernanceModuleStatus.from_dict(row))
            except Exception as exc:
                logger.warning("module_health parse error: %s", exc)
        return result

    def symbol_matrix(self) -> List[GovernanceSymbolStatus]:
        """Return list of symbol governance statuses."""
        rows = self._store.load_symbol_status()
        result = []
        for row in rows:
            try:
                result.append(GovernanceSymbolStatus.from_dict(row))
            except Exception as exc:
                logger.warning("symbol_matrix parse error: %s", exc)
        return result

    def action_queue(self) -> List[GovernanceActionItem]:
        """Return list of governance action items."""
        rows = self._store.load_action_queue()
        result = []
        for row in rows:
            try:
                result.append(GovernanceActionItem.from_dict(row))
            except Exception as exc:
                logger.warning("action_queue parse error: %s", exc)
        return result

    def top_actions(self, limit: int = 10) -> List[GovernanceActionItem]:
        """Return top N actions by priority."""
        actions = self.action_queue()
        return self._engine.top_actions(actions, limit=limit)

    def list_p0(self) -> List[GovernanceActionItem]:
        """Return P0 actions."""
        return [a for a in self.action_queue() if a.priority == "P0"]

    def list_p1(self) -> List[GovernanceActionItem]:
        """Return P1 actions."""
        return [a for a in self.action_queue() if a.priority == "P1"]

    def list_stale(self) -> List[GovernanceSymbolStatus]:
        """Return stale symbols."""
        return [s for s in self.symbol_matrix() if s.freshness_status in ("STALE", "DELAYED")]

    def list_blocked(self) -> List[GovernanceSymbolStatus]:
        """Return blocked symbols."""
        return [s for s in self.symbol_matrix() if s.blocked]

    def list_formal_eligible(self) -> List[GovernanceSymbolStatus]:
        """Return formal-eligible symbols."""
        return [s for s in self.symbol_matrix() if s.formal_eligible]

    def list_observational(self) -> List[GovernanceSymbolStatus]:
        """Return observational-eligible symbols (not formal)."""
        return [s for s in self.symbol_matrix() if s.observational_eligible and not s.formal_eligible]

    def source_interruptions(self) -> List[dict]:
        """Return source interruptions from latest summary."""
        summary = self.latest_summary()
        if not summary:
            return []
        # Source interruptions are tracked in summary
        count = getattr(summary, "source_interruptions", 0)
        if count == 0:
            return []
        return [{"source_interruption_count": count, "from_summary": True}]

    def audit_failures(self) -> List[dict]:
        """Return audit chain failures."""
        rows = self._store.load_audit_summary()
        return rows

    def latest_runs(self) -> List[GovernanceRunSummary]:
        """Return latest enforcement runs."""
        rows = self._store.load_enforcement_runs()
        result = []
        for row in rows:
            try:
                result.append(GovernanceRunSummary.from_dict(row))
            except Exception as exc:
                logger.warning("latest_runs parse error: %s", exc)
        return result

    def daily_history(self) -> List[dict]:
        """Return daily history snapshots."""
        return self._store.load_daily_history()

    def compare_days(self, date_a: str, date_b: str) -> dict:
        """
        Compare two governance snapshots by date.
        Returns dict with change fields.
        """
        history = self.daily_history()
        snap_a = None
        snap_b = None
        for snap in history:
            gen_at = snap.get("generated_at", "")
            if date_a in gen_at:
                snap_a = snap
            if date_b in gen_at:
                snap_b = snap

        if not snap_a or not snap_b:
            return {
                "error": f"Could not find snapshots for {date_a} and/or {date_b}",
                "date_a": date_a,
                "date_b": date_b,
                "found_a": snap_a is not None,
                "found_b": snap_b is not None,
            }

        def _delta(key: str) -> int:
            return int(snap_b.get(key, 0)) - int(snap_a.get(key, 0))

        return {
            "date_a": date_a,
            "date_b": date_b,
            "ready_change": _delta("ready_symbols"),
            "stale_change": _delta("stale_symbols"),
            "missing_change": _delta("missing_symbols"),
            "formal_change": _delta("formal_eligible"),
            "blocked_change": _delta("blocked_symbols"),
            "p0_change": _delta("p0_actions"),
            "p1_change": _delta("p1_actions"),
            "source_interruption_change": _delta("source_interruptions"),
            "audit_failure_change": _delta("audit_chain_failures"),
            "overall_status_a": snap_a.get("overall_status", "UNKNOWN"),
            "overall_status_b": snap_b.get("overall_status", "UNKNOWN"),
        }
