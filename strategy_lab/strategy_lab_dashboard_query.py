"""
strategy_lab/strategy_lab_dashboard_query.py — Strategy Lab Dashboard Query v0.9.3

Query helpers for Strategy Lab Dashboard stored data.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StrategyLabDashboardQuery:
    """Query interface for Strategy Lab Dashboard data.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, store=None) -> None:
        if store is None:
            try:
                from strategy_lab.strategy_lab_dashboard_store import StrategyLabDashboardStore
                store = StrategyLabDashboardStore()
            except Exception:
                store = None
        self._store = store

    # ------------------------------------------------------------------
    # Cards
    # ------------------------------------------------------------------

    def list_cards(self, status: Optional[str] = None, severity: Optional[str] = None) -> list:
        """Return cards, optionally filtered by status and/or severity."""
        if self._store is None:
            return []
        cards = self._store.load_latest_cards()
        if status:
            cards = [c for c in cards if c.status == status]
        if severity:
            cards = [c for c in cards if c.severity == severity]
        return cards

    # ------------------------------------------------------------------
    # Rows
    # ------------------------------------------------------------------

    def list_rows(
        self,
        category: Optional[str] = None,
        status: Optional[str] = None,
        grade: Optional[str] = None,
        source_module: Optional[str] = None,
    ) -> list:
        """Return rows, optionally filtered."""
        if self._store is None:
            return []
        rows = self._store.load_latest_rows()
        if category:
            rows = [r for r in rows if r.category == category]
        if status:
            rows = [r for r in rows if r.status == status]
        if grade:
            rows = [r for r in rows if r.grade == grade]
        if source_module:
            rows = [r for r in rows if r.source_module == source_module]
        return rows

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def list_actions(
        self,
        action_type: Optional[str] = None,
        priority: Optional[str] = None,
        source_module: Optional[str] = None,
    ) -> list:
        """Return actions, optionally filtered."""
        if self._store is None:
            return []
        actions = self._store.load_latest_actions()
        if action_type:
            actions = [a for a in actions if a.action_type == action_type]
        if priority:
            actions = [a for a in actions if a.priority == priority]
        if source_module:
            actions = [a for a in actions if a.source_module == source_module]
        return actions

    # ------------------------------------------------------------------
    # Special queries
    # ------------------------------------------------------------------

    def top_priorities(self, limit: int = 10) -> list:
        """Return top priority action items (P0 first, then P1, etc.)."""
        if self._store is None:
            return []
        actions = self._store.load_latest_actions()
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        actions.sort(key=lambda a: priority_order.get(a.priority, 9))
        return actions[:limit]

    def needs_backtest(self, limit: int = 10) -> list:
        """Return rows/actions needing more backtest."""
        if self._store is None:
            return []
        actions = [
            a for a in self._store.load_latest_actions()
            if a.action_type == "BACKTEST_MORE"
        ]
        return actions[:limit]

    def needs_replay(self, limit: int = 10) -> list:
        """Return rows/actions needing more replay practice."""
        if self._store is None:
            return []
        actions = [
            a for a in self._store.load_latest_actions()
            if a.action_type == "PRACTICE_REPLAY"
        ]
        return actions[:limit]

    def needs_data(self, limit: int = 10) -> list:
        """Return rows/actions needing data fixes."""
        if self._store is None:
            return []
        actions = [
            a for a in self._store.load_latest_actions()
            if a.action_type == "FIX_DATA"
        ]
        return actions[:limit]

    def conflicted(self, limit: int = 10) -> list:
        """Return rows in CONFLICTED state."""
        if self._store is None:
            return []
        rows = [
            r for r in self._store.load_latest_rows()
            if r.grade == "CONFLICTED" or r.status == "WARNING"
        ]
        return rows[:limit]

    def explain_dashboard(self) -> str:
        """Return a human-readable explanation of the current dashboard state."""
        if self._store is None:
            return "Dashboard store not available. Run: python main.py strategy-lab-dashboard --mode real"

        summary = self._store.load_latest_summary()
        if summary is None:
            return "No dashboard summary found. Run: python main.py strategy-lab-dashboard --mode real"

        sd = summary.to_dict()
        lines = [
            "Strategy Lab Dashboard — Research Only / No Real Orders",
            "=" * 60,
            f"Generated:        {sd.get('generated_at', 'unknown')}",
            f"Mode:             {sd.get('mode', 'real')}",
            f"Overall Status:   {sd.get('overall_status', 'UNKNOWN')}",
            f"Health Score:     {sd.get('overall_health_score', 0):.1f} / 100",
            f"Strategy Count:   {sd.get('strategy_count', 0)}",
            f"  VALIDATED:      {sd.get('validated_count', 0)}",
            f"  VALIDATING:     {sd.get('validating_count', 0)}",
            f"  OBSERVATIONAL:  {sd.get('observational_count', 0)}",
            f"  INSUFFICIENT:   {sd.get('insufficient_count', 0)}",
            f"  CONFLICTED:     {sd.get('conflicted_count', 0)}",
            f"  REJECTED:       {sd.get('rejected_count', 0)}",
            f"Evidence Threads: {sd.get('evidence_thread_count', 0)}",
            f"Graph Gaps:       {sd.get('graph_gap_count', 0)}",
            f"Crash Warnings:   {sd.get('crash_reversal_warning_count', 0)}",
            f"Needs Backtest:   {sd.get('needs_backtest_count', 0)}",
            f"Needs Replay:     {sd.get('needs_replay_count', 0)}",
            f"Needs Data:       {sd.get('needs_data_count', 0)}",
            f"Forbidden Actions: {sd.get('forbidden_action_count', 0)}",
            "=" * 60,
            "RESEARCH ONLY — Not Investment Advice — No Real Orders",
            "VALIDATED = Research Validated Only — does NOT enable trading",
        ]
        return "\n".join(lines)
